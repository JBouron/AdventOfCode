#include <iostream>
#include <fstream>
#include <vector>
#include <map>
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

static bool isDigit(char const ch) {
    return '0' <= ch && ch <= '9';
}

static std::vector<u8> extractNums(std::string_view const line) {
    std::vector<u8> res;
    auto it(std::find_if(line.begin(), line.end(), isDigit));
    while (it != line.end()) {
        auto const endOfNum(std::find_if_not(it, line.end(), isDigit));
        u32 const len(endOfNum - it);
        std::string const numStr(line.substr(it - line.begin(), len));
        res.push_back(std::stoi(numStr));
        it = std::find_if(endOfNum, line.end(), isDigit);
    }
    return res;
}

static u64 getNumberOfMatches(std::string_view const line) {
    std::string::size_type const colPos(line.find(':'));
    assert(colPos != std::string::npos);
    std::string::size_type const sepPos(line.find('|'));
    assert(sepPos != std::string::npos);
    std::string::size_type const spcPos(line.find(' '));
    std::string const gameIdStr(line.substr(spcPos+1, colPos-(spcPos+1)));
    u64 const gameId(std::stoi(gameIdStr));
    std::string_view const winningLine(line.substr(colPos+1, sepPos-(colPos+1)));
    std::string_view const scratchedLine(line.substr(sepPos+1));
    std::vector<u8> winningNums(extractNums(winningLine));
    std::vector<u8> scratchedNums(extractNums(scratchedLine));
    std::sort(winningNums.begin(), winningNums.end());
    std::sort(scratchedNums.begin(), scratchedNums.end());

    u64 w(0), s(0), matching(0);
    while (w < winningNums.size() && s < scratchedNums.size()) {
        if (winningNums[w] == scratchedNums[s]) {
            w++;
            s++;
            matching++;
        } else if (winningNums[w] < scratchedNums[s]) {
            w++;
        } else {
            s++;
        }
    }
    return matching;
}

static void run(std::vector<std::string> const& lines) {
    u64 part1(0);
    std::map<u64,u64> numCopies;
    for (u64 i(0); i < lines.size(); ++i) {
        numCopies[i] = 1;
    }
    for (u64 i(0); i < lines.size(); ++i) {
        std::string_view const l(lines[i]);
        u64 const matching(getNumberOfMatches(l));
        part1 += !!matching ? (1 << (matching - 1)) : 0;
        for (u64 j(i+1); j < i + 1 + matching; ++j) {
            numCopies[j] += numCopies[i];
        }
    }
    u64 part2(0);
    std::for_each(numCopies.begin(), numCopies.end(), [&](auto const kv) {
        part2 += kv.second;
    });
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
