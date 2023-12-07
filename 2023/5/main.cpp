#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include <algorithm>
#include <stdint.h>
#include <assert.h>
#include "set.hpp"

using u8 = uint8_t;
using u16 = uint16_t;
using u32 = uint32_t;
using u64 = uint64_t;
using i8 = int8_t;
using i16 = int16_t;
using i32 = int32_t;
using i64 = int64_t;

// Check if a character is a digit.
// @param ch: The character to test.
// @return: true if `ch` is a digit [0-9], false otherwise.
static bool isDigit(char const ch) {
    return '0' <= ch && ch <= '9';
}

// Extract all numbers appearing in a string. Numbers can be separated by any
// character that is not a digit.
// @param line: The string to extract the numbers from.
// @return: A vector<u64> containing all numbers of the string, in the same
// order as they appear in the string.
static std::vector<u64> extractNums(std::string_view const line) {
    std::vector<u64> res;
    auto it(std::find_if(line.begin(), line.end(), isDigit));
    while (it != line.end()) {
        auto const endOfNum(std::find_if_not(it, line.end(), isDigit));
        u32 const len(endOfNum - it);
        // FIXME: std::stoll() does not support string_views, we need to copy the
        // view into a string before converting it to a u64.
        std::string const numStr(line.substr(it - line.begin(), len));
        res.push_back(std::stoll(numStr));
        it = std::find_if(endOfNum, line.end(), isDigit);
    }
    return res;
}

struct MappingEntry {
    u64 destinationStart;
    u64 sourceStart;
    u64 length;

    bool contains(u64 const sourceValue) const {
        return sourceStart <= sourceValue && sourceValue < sourceStart + length;
    }

    u64 map(u64 const sourceValue) const {
        u64 const delta(sourceValue - sourceStart);
        return destinationStart + delta;
    }

    bool operator<(MappingEntry const& other) const {
        return sourceStart < other.sourceStart;
    }
};

static MappingEntry parseEntry(std::string_view const& line) {
    std::vector<u64> const nums(extractNums(line));
    assert(nums.size() == 3);
    MappingEntry const res({
        .destinationStart = nums[0],
        .sourceStart = nums[1],
        .length = nums[2]
    });
    return res;
}

class Mapping {
public:
    Mapping(std::vector<MappingEntry> const& r) :
        m_entries(r), m_nextLevel(nullptr) {
        std::sort(m_entries.begin(), m_entries.end());
    }

    void nextLevel(Mapping const* const ptr) {
        m_nextLevel = ptr;
    }

    u64 map(u64 const sourceValue) const {
        for (MappingEntry const& r : m_entries) {
            if (r.contains(sourceValue)) {
                return r.map(sourceValue);
            }
        }
        // Any source numbers that aren't mapped correspond to the same
        // destination number.
        return sourceValue;
    }

    Set<u64> map(Set<u64> const& set) const {
        Set<u64> res;
        res.add(set);

        for (MappingEntry const& e : m_entries) {
            Set<u64>::Interval const srcInt(e.sourceStart, e.length);
            res.remove(srcInt);
        }
        for (MappingEntry const& e : m_entries) {
            Set<u64>::Interval const srcInt(e.sourceStart, e.length);
            Set<u64> inter(set.intersection(srcInt));
            u64 const shiftVal(e.destinationStart - e.sourceStart);
            inter.shift(shiftVal);
            res.add(inter);
        }
        return res;
    }

    u64 size() const {
        return m_entries.size();
    }
private:
    std::vector<MappingEntry> m_entries;
    Mapping const* m_nextLevel;
};

static Mapping parseMapping(
    std::vector<std::string>::const_iterator const from,
    std::vector<std::string>::const_iterator const last) {
    std::vector<MappingEntry> entries;
    for (auto it(from); it != last && !!it->size(); ++it) {
        MappingEntry const entry(parseEntry(*it));
        entries.push_back(entry);
    }
    return Mapping(entries);
}

static void run(std::vector<std::string> const& lines) {
    assert(lines.size() > 3);

    // Parse the seeds, which is the first line.
    std::vector<u64> const seeds(extractNums(lines[0]));

    // Parse all the mapping, we assume that the mapping always appear in the
    // same order, e.g. seed-to-soil, soil-to-fertilizer, fertilizer-to-water,
    // ...
    auto it(lines.cbegin() + 3);
    Mapping seedToSoil(parseMapping(it, lines.end()));
    it += seedToSoil.size() + 2;
    Mapping soilToFert(parseMapping(it, lines.end()));
    seedToSoil.nextLevel(&soilToFert);
    it += soilToFert.size() + 2;
    Mapping fertToWater(parseMapping(it, lines.end()));
    soilToFert.nextLevel(&fertToWater);
    it += fertToWater.size() + 2;
    Mapping waterToLight(parseMapping(it, lines.end()));
    fertToWater.nextLevel(&waterToLight);
    it += waterToLight.size() + 2;
    Mapping lightToTemp(parseMapping(it, lines.end()));
    waterToLight.nextLevel(&lightToTemp);
    it += lightToTemp.size() + 2;
    Mapping tempToHum(parseMapping(it, lines.end()));
    lightToTemp.nextLevel(&tempToHum);
    it += tempToHum.size() + 2;
    Mapping humToLoc(parseMapping(it, lines.end()));
    tempToHum.nextLevel(&humToLoc);
    assert(it + humToLoc.size() == lines.end());

    // Part 1.
    std::vector<u64> locations;
    std::for_each(seeds.begin(), seeds.end(), [&](u64 const seed) {
        // Behold the most beautiful line I've ever written in my life.
        u64 const loc(
                humToLoc.map(
                    tempToHum.map(
                        lightToTemp.map(
                            waterToLight.map(
                                fertToWater.map(
                                    soilToFert.map(
                                        seedToSoil.map(
                                            seed))))))));
        locations.push_back(loc);
    });
    u64 const part1(*std::min_element(locations.begin(), locations.end()));
    std::cout << "Part 1: " << part1 << std::endl;

    // Part 2.
    u64 part2(~0ULL);
    assert(!(seeds.size() % 2));
    for (u64 i(0); i < seeds.size(); i += 2) {
        u64 const rangeStart(seeds[i]);
        u64 const rangeLen(seeds[i+1]);
        Set<u64> seedSet(Set<u64>::Interval(rangeStart, rangeLen));
        seedSet = seedToSoil.map(seedSet);
        seedSet = soilToFert.map(seedSet);
        seedSet = fertToWater.map(seedSet);
        seedSet = waterToLight.map(seedSet);
        seedSet = lightToTemp.map(seedSet);
        seedSet = tempToHum.map(seedSet);
        seedSet = humToLoc.map(seedSet);
        part2 = std::min(part2, seedSet.min());
    }
    std::cout << "Part 2: " << part2 << std::endl;
}

int main(int const argc, char ** const argv) {
    if (argc < 2) {
        std::cerr << "Expected filename as argument" << std::endl;
        std::exit(1);
    } else {
        char const * const fileName(argv[1]);
        std::ifstream file(fileName, std::ios::in);
        if (!file) {
            std::cerr << "Cannot open file " << fileName << std::endl;
            std::exit(1);
        }
        std::vector<std::string> lines;
        std::string line;
        while (std::getline(file, line)) {
            lines.push_back(line);
        }
        run(lines);
        //Set<u64> s;
        //s.add(Set<u64>::Interval(10, 10));
        //std::cout << s.toString() << std::endl;
        //s.add(Set<u64>::Interval(20, 10));
        //std::cout << s.toString() << std::endl;
        //s.add(Set<u64>::Interval(0, 10));
        //std::cout << s.toString() << std::endl;

        //std::cout << "---" << std::endl;

        //s.remove(Set<u64>::Interval(10, 10));
        //std::cout << s.toString() << std::endl;
        //s.remove(Set<u64>::Interval(19, 2));
        //std::cout << s.toString() << std::endl;
        //s.remove(Set<u64>::Interval(9, 1));
        //std::cout << s.toString() << std::endl;
        //s.remove(Set<u64>::Interval(20, 11));
        //std::cout << s.toString() << std::endl;
        //s.remove(Set<u64>::Interval(0, 10));
        //std::cout << s.toString() << std::endl;

    }
    return 0;
}
