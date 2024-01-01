// Utility functions and types used by many of the solutions.

#include <vector>
#include <iterator>
#include <map>
#include <set>
#include <iostream>
#include <fstream>
#include <algorithm>
#include <functional>
#include <stdint.h>
#include <assert.h>
#include <cmath>
#include <sstream>

using u8  = uint8_t;
using u16 = uint16_t;
using u32 = uint32_t;
using u64 = uint64_t;
using i8  = int8_t;
using i16 = int16_t;
using i32 = int32_t;
using i64 = int64_t;

namespace Util {

// Read the contents of a file and return its lines.
// @param fileName: Path to the file to read.
// @param skipEmptyLines: If true, the resulting vector does not contain the
// empty lines found in the file.
// @return: A vector containing all the lines of the file.
std::vector<std::string> readFile(std::string const& fileName,
                                  bool const skipEmptyLines=false) {
    std::ifstream file(fileName, std::ios::in);
    if (!file) {
        std::cerr << "Cannot open file " << fileName << std::endl;
        std::exit(1);
    }
    std::vector<std::string> lines;
    std::string line;
    while (std::getline(file, line)) {
        if (!skipEmptyLines || line.size()) {
            lines.push_back(line);
        }
    }
    return lines;
}

// Check if a character is a digit.
// @param ch: The character to test.
// @return: true if `ch` is a digit [0-9], false otherwise.
bool isDigit(char const ch) {
    return '0' <= ch && ch <= '9';
}

// Extract all numbers appearing in a string. Numbers can be separated by any
// character that is not a digit.
// @param line: The string to extract the numbers from.
// @return: A vector<u64> containing all numbers of the string, in the same
// order as they appear in the string.
std::vector<u64> extractNums(std::string_view const& line) {
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

// Split a string around a substring.
// @param line: The string to split.
// @param splitOn: The substring to split around.
// @return: A vector containing the result of the split. This vector does not
// contain empty strings, e.g. split("abaab", "a") returns {"b", "b"}.
std::vector<std::string> split(std::string_view const& line,
                               std::string_view const& splitOn) {
    std::vector<std::string> res;
    std::string_view::size_type pos(0);
    while (pos < line.size()) {
        std::string_view::size_type const findRes(line.find(splitOn, pos));
        std::string_view::size_type const nextOcc(findRes == std::string::npos ?
            line.size() : findRes);
        if (nextOcc != pos) {
            res.push_back(std::string(line.substr(pos, nextOcc - pos)));
        }
        pos = nextOcc + splitOn.size();
    }
    return res;
}

// Create a new string from a source string, replacing all occurences of `from`
// to `to`.
std::string replace(std::string_view const& line,
                    char const from,
                    char const to) {
    std::string res;
    for (u64 i(0); i < line.size(); ++i) {
        char const ch(line[i]);
        res += ch == from ? to : ch;
    }
    return res;
}

// Create a std::map mapping the values found in the range [first; last) with
// the number of times they appear in this range.
template<typename It>
std::map<typename std::iterator_traits<It>::value_type, u64>
occurences(It first, It last) {
    std::map<typename std::iterator_traits<It>::value_type, u64> occ;
    for (It it(first); it != last; ++it) {
        occ[*it] += 1;
    }
    return occ;
}

// Get the set of values contained in a std::map<K,V>.
template<typename K, typename V>
std::set<V> values(std::map<K, V> const& map) {
    std::set<V> res;
    std::for_each(map.cbegin(), map.cend(), [&](auto const& p) {
        res.insert(p.second);
    });
    return res;
}

template<typename T, typename U>
std::vector<U> map(std::vector<T> const& v, U (*f)(T const&)) {
    std::vector<U> res;
    std::for_each(v.begin(), v.end(), [&](T const& t) {
        res.push_back(f(t));
    });
    return res;
}

// A type for a position in 2D space.
class Pos2d {
public:
    using CoordType = i64;

    // Create a Pos2d with the given component.
    // @param x: The x component of the position.
    // @param y: The y component of the position.
    Pos2d(CoordType const x, CoordType const y) : x(x), y(y) {}

    // Compare two Pos2d. This is mostly used so that a std::set<Pos2d> can be
    // created.
    // @param other: The other Pos2d to compare against.
    // @return: true if this Pos2d is smaller than the other, false otherwise.
    bool operator<(Pos2d const& other) const {
        return y < other.y ? true : x < other.x;
    }

    bool operator==(Pos2d const& other) const = default;
    bool operator!=(Pos2d const& other) const = default;

    // Compute the euclidean distance between this Pos2d and another.
    // @param other: The other position to compute the distance from.
    // @return: The distance.
    double distance(Pos2d const& other) const {
        double const deltaX(x - other.x);
        double const deltaY(y - other.y);
        return std::sqrt(deltaX * deltaX + deltaY * deltaY);
    }

    // Compute the manhattan distance between this Pos2d and another.
    // @param other: The other position to compute the distance from.
    // @return: The distance.
    u64 manDistance(Pos2d const& other) const {
        i64 const deltaX(x - other.x);
        i64 const deltaY(y - other.y);
        return std::abs(deltaX) + std::abs(deltaY);
    }

    // Return the position above/under/left-of/right-of this position.
    Pos2d up() const { return Pos2d(x, y - 1); }
    Pos2d down() const { return Pos2d(x, y + 1); }
    Pos2d left() const { return Pos2d(x - 1, y); }
    Pos2d right() const { return Pos2d(x + 1, y); }

    // The component of the position that can be mutated freely.
    i64 x;
    i64 y;
};

// Operator to print a Pos2d into std::cout / std::cerr.
std::ostream& operator<<(std::ostream& stream, Pos2d const& pos) {
    stream << "(" << pos.x << ", " << pos.y << ")";
    return stream;
}

// A 2D grid of values of type T. A Grid<T> is always rectangular and holds the
// values of _all_ the cells/positions that falls within the Grid (ie. it is not
// a sparse collection).
template<typename T>
class Grid {
public:
    // Construct a grid.
    // @param width: The width of the grid.
    // @param height: The height of the grid.
    // @param defaultValue: The value to give to all cells/positions of the grid
    // upon init.
    Grid(u64 const width, u64 const height, T const& defaultValue = T()) :
        m_grid(height) {
        for (std::vector<T>& row : m_grid) {
            for (u64 i(0); i < width; ++i) {
                row.push_back(defaultValue);
            }
        }
    }

    // Construct a grid from an array of strings, that is, this constructor
    // treats each character of each string as a cell of the grid. All strings
    // in the vector must have the same length. The resulting grid as a height
    // equals to lines.size() and a width matching the length of all strings.
    // @param lines: The array of string to construct the grid from.
    // @praam charToT: A function pointer that converts a char to a T. This is
    // called on all char/cells of the array of string.
    Grid(std::vector<std::string> const& lines, T (*charToT)(char const)) :
        m_grid(lines.size()) {
        u64 rowIndex(0);
        for (std::string const& row : lines) {
            for (char const c : row) {
                m_grid[rowIndex].push_back(charToT(c));
            }
            if (rowIndex) {
                // Check that all lines have the same length.
                assert(m_grid[rowIndex].size() == m_grid[rowIndex-1].size());
            }
            rowIndex++;
        }
    }

    // Get the height and width of the grid.
    i64 height() const { return m_grid.size(); }
    i64 width() const { return m_grid[0].size(); }

    // Check if a position is within the bounds of the grid.
    // @return: true if the position is within the bounds, false otherwise.
    bool inBounds(Pos2d const& pos) const {
        return 0 <= pos.x && pos.x < width() && 0 <= pos.y && pos.y < height();
    }

    // Access a cell of the grid with its position.
    // @param pos: The position of the cell to access. If this position is
    // outside the grid's boundaries this raises an exception.
    // @return: A mutable reference to the value of the cell at the given
    // position.
    T& operator[](Pos2d const& pos) {
        assert(inBounds(pos));
        return m_grid[pos.y][pos.x];
    }

    // Access a cell of the grid with its position.
    // @param pos: The position of the cell to access. If this position is
    // outside the grid's boundaries this raises an exception.
    // @return: A non-mutable reference to the value of the cell at the given
    // position.
    T const& operator[](Pos2d const& pos) const {
        assert(inBounds(pos));
        return m_grid[pos.y][pos.x];
    }

    // Find the position of all the cells in the grid having the given value.
    // @param value: The value to look for in the grid.
    // @return: A set of Pos2d containing the position of all the cells that
    // matched the value.
    std::set<Pos2d> find(T const& value) const {
        std::set<Pos2d> res;
        for (i64 y(0); y < height(); ++y) {
            for (i64 x(0); x < width(); ++x) {
                if (m_grid[y][x] == value) {
                    res.emplace(x, y);
                }
            }
        }
        return res;
    }

    std::string toString() const {
        std::string const hBorder("+" + std::string(width(), '-') + "+");
        std::ostringstream oss;
        oss << hBorder << std::endl;
        for (std::vector<T> const& row : m_grid) {
            oss << "|";
            for (T const& v : row) {
                oss << v;
            }
            oss << "|" << std::endl;
        }
        oss << hBorder;
        return oss.str();
    }

private:
    std::vector<std::vector<T>> m_grid;
};
}
