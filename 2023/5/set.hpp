#pragma once
#include <vector>

template<typename T>
class Set {
public:
    struct Interval {
        Interval(T const& s, T const& l) : start(s), length(l) {}
        Interval() : Interval(0, 0) {}

        T minVal() const { return start; }
        T maxVal() const { return start + length - 1; }

        bool overlaps(Interval const& other) const {
            return (minVal() <= other.minVal() && other.minVal() <= maxVal())
                || (minVal() <= other.maxVal() && other.maxVal() <= maxVal())
                || (other.minVal() <= minVal() && maxVal() <= other.maxVal());
        }

        Interval intersection(Interval const& other) const {
            if (!overlaps(other)) {
                return Interval();
            } else {
                T const intStart(std::max(minVal(), other.minVal()));
                T const intMaxVal(std::min(maxVal(), other.maxVal()));
                T const intLen(intMaxVal - intStart + 1);
                return Interval(intStart, intLen);
            }
        }

        bool adjacent(Interval const& other) const {
            return minVal() == (other.maxVal() + 1)
                   || other.minVal() == (maxVal() + 1);
        }

        Interval merge(Interval const& other) const {
            assert(adjacent(other));
            T const mergeStart(std::min(minVal(), other.minVal()));
            T const mergeMaxVal(std::max(maxVal(), other.maxVal()));
            T const mergeLen(mergeMaxVal - mergeStart + 1);
            return Interval(mergeStart, mergeLen);
        }

        bool contains(Interval const& other) const {
            return minVal() <= other.minVal() && other.maxVal() <= maxVal();
        }

        bool operator==(Interval const& other) const {
            return start == other.start && length == other.length;
        }

        T start;
        T length;
    };

    // Create an empty set.
    Set() = default;

    // Create a set from an interval.
    // @param interval: The interval defining the values contained in the set.
    Set(Interval const& interval) {
        m_ints.push_back(interval);
    }

    // Add an interval to this set.
    // @param interval: The interval to add.
    void add(Interval const& interval) {
        auto const insertPos(std::find_if(m_ints.begin(), m_ints.end(),
            [&](Interval const e) {
            return interval.minVal() < e.minVal(); 
        }));
        if (m_ints.begin() < insertPos) {
            // Check if we need to merge with the interval appearing before the
            // insert position.
            Interval const prev(*(insertPos - 1));
            if (prev.adjacent(interval)) {
                // We need to merge the two intervals. Easiest thing to do is to
                // remove prev and call add() with the merged interval.
                m_ints.erase(insertPos - 1);
                add(prev.merge(interval));
                return;
            }
        } else if (insertPos < m_ints.end()) {
            // Check if we need to merge with the interval after the insertPos.
            Interval const next(*(insertPos));
            if (next.adjacent(interval)) {
                // We need to merge the two intervals. Easiest thing to do is to
                // remove next and call add() with the merged interval.
                m_ints.erase(insertPos);
                add(next.merge(interval));
                return;
            }
        }
        // If we reach this point then no merging occured and we can insert the
        // interval.
        m_ints.insert(insertPos, interval);
    }

    // Add the contents of another set into this set.
    // @param other: The set to dump into this set.
    void add(Set const& other) {
        // Inserting intervals one-by-one is a bit inefficient but this keeps
        // things simple for now.
        for (Interval const& e : other.m_ints) {
            add(e);
        }
    }

    void remove(Interval const& interval) {
        auto const pred([&](Interval const& e) {
            return e.overlaps(interval);
        });
        auto it(std::find_if(m_ints.begin(), m_ints.end(), pred));
        while (it != m_ints.end()) {
            // *it and interval are overlapping, we have 3 cases:
            //  - 1: interval fully contains *it, in this case we need to remove
            //  it.
            //  - 2: *it fully contains interval, we need to split *it into two
            //  sub-interval.
            //  - 3: *it and interval are only overlapping, reduce the size of
            //  *it.
            Interval& curr(*it);
            if (interval.contains(curr)) {
                // Case #1.
                m_ints.erase(it);
            } else if (curr.contains(interval)) {
                // Case #2.
                // The == case is handled by the interval.contains(*it) case.
                assert(curr != interval);
                // Compute the left and right pieces left of *it.
                T const leftStart(curr.start);
                T const leftLen(interval.start - curr.start);
                T const rightStart(interval.maxVal() + 1);
                T const rightLen(curr.maxVal() - interval.maxVal());
                m_ints.erase(it);
                if (leftLen) {
                    add(Interval(leftStart, leftLen));
                }
                if (rightLen) {
                    add(Interval(rightStart, rightLen));
                }
            } else {
                // Case #3.
                if (interval.minVal() < curr.minVal()) {
                    T const newStart(interval.maxVal() + 1);
                    T const newLen(curr.maxVal() - newStart + 1);
                    curr.start = newStart;
                    curr.length = newLen;
                } else {
                    assert(interval.minVal() <= curr.maxVal());
                    T const newMaxVal(interval.minVal() - 1);
                    T const newLen(newMaxVal - curr.minVal() + 1);
                    curr.length = newLen;
                }
            }
            // Start the search from the beginning because erase invalidates the
            // iterator.
            // FIXME: This could be optimized by using the iterator returned by
            // erase().
            it = std::find_if(m_ints.begin(), m_ints.end(), pred);
        }
    }

    Set intersection(Interval const& interval) const {
        Set res;
        for (Interval const& e : m_ints) {
            if (e.overlaps(interval)) {
                res.add(e.intersection(interval));
            }
        }
        return res;
    }

    void shift(T const shiftVal) {
        for (Interval& e : m_ints) {
            e.start += shiftVal;
        }
    }

    T const min() const {
        assert(m_ints.size());
        return m_ints[0].minVal();
    }

    std::string toString() const {
        std::string acc("[");
        for (Interval const& e : m_ints) {
            if (acc.size() > 1) {
                acc += ", ";
            }
            acc += "(" + std::to_string(e.minVal()) + ";"
                   + std::to_string(e.maxVal()) + ")";
        }
        acc += "]";
        return acc;
    }
    
private:
    std::vector<Interval> m_ints;
};
