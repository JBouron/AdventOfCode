#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include <cmath>
#include <algorithm>
#include <stdint.h>
#include <assert.h>

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

// Merge all the numbers appearing in a line and return its value in u64, ie. "1
// sbf 4 sdlfkj 98" returns 1498.
// @param line: The string to extract the number from.
// @return: The U64 representation of the number.
static u64 mergeNums(std::string_view const& line) {
    std::string acc;
    std::for_each(line.cbegin(), line.cend(), [&](char const ch) {
        if (isDigit(ch)) {
            acc += ch;
        }
    });
    return std::stoll(acc);
}

// For a given race time and the record distance, compute the number of possible
// ways to beat the record.
// @param time: Race time.
// @param distance: Distance to beat.
static u64 numberOfWaysToBeat(u64 const time, u64 const distance) {
    // Distance traveled in T ms after holding the button for H ms is:
    //  D = H*T - H**2.
    // We need to beat the record of R mm, hence we need to choose H such
    // that:
    //  D > R
    //  H*T - H**2 > R
    //  H**2 - H*T + R < 0
    // We compute the roots of the polynomial, the needed H are all integers
    // between those two roots.
    double const& T(time);
    double const& R(distance);
    double const root1((T - std::sqrt(T*T - 4*R)) / 2.f);
    double const root2((T + std::sqrt(T*T - 4*R)) / 2.f);
    // This function does not support the case where there is exactly one root,
    // although I do not think the problem allows this.
    assert(root1 != root2);
    double const root1Ceil(std::ceil(root1));
    double const root2Floor(std::floor(root2));
    assert(root1Ceil != root2Floor);
    // Because we want to beat the record we need to be careful of the edge
    // case where a root is an integer as this would lead to a tie.
    u64 const minH(root1 == root1Ceil ? (root1Ceil + 1) : root1Ceil);
    u64 const maxH(root2 == root2Floor ? (root2Floor - 1) : root2Floor);
    assert(minH<maxH);
    return (maxH - minH + 1);
}

static void run(std::vector<std::string> const& lines) {
    assert(lines.size() == 2);
    std::vector<u64> const times(extractNums(lines[0]));
    std::vector<u64> const distances(extractNums(lines[1]));
    assert(times.size() == distances.size());

    // Part 1:
    u64 part1(1);
    for (u64 i(0); i < times.size(); ++i) {
        part1 *= numberOfWaysToBeat(times[i], distances[i]);
    }

    // Part 2:
    u64 const part2Time(mergeNums(lines[0]));
    u64 const part2Dist(mergeNums(lines[1]));
    u64 const part2(numberOfWaysToBeat(part2Time, part2Dist));

    std::cout << "Part 1: " << part1 << std::endl;
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
    }
    return 0;
}
