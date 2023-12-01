#include <iostream>
#include <fstream>
#include <algorithm>

static const std::string NUMBERS[] = {
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
};

// Check if a char is a digit.
// @param c: The char to test.
// @return: true if the char is a digit, false otherwise.
static bool isDigit(char const c) {
    return '0' <= c && c <= '9';
};

// Get the first digit or first spelled digit from a string.
// @param str: The string to extract the first digit/number from.
// @param incSpelled: If true, include spelled out numbers (part 2 only)
// otherwise only look at digits.
// @return: The first digit in the string.
static int firstDigitFromString(std::string const str, bool const incSpelled) {
    auto const firstDigit(std::find_if(str.cbegin(), str.cend(), isDigit));
    if (!incSpelled) {
        return *firstDigit - '0';
    } else {
        std::string::const_iterator firstNum(str.cend());
        int firstNumIdx(-1);
        for (int i(0); i < 9; ++i) {
            auto const num(NUMBERS[i]);
            auto const p(std::search(str.cbegin(), str.cend(),
                                     num.cbegin(), num.cend()));
            if (p < firstNum) {
                firstNum = p;
                firstNumIdx = i;
            }
        }
        if (firstDigit < firstNum) {
            return *firstDigit - '0';
        } else {
            return firstNumIdx + 1;
        }
    }
}

// Get the last digit or last spelled digit from a string.
// @param str: The string to extract the last digit/number from.
// @param incSpelled: If true, include spelled out numbers (part 2 only)
// otherwise only look at digits.
// @return: The last digit in the string.
static int lastDigitFromString(std::string const str, bool const incSpelled) {
    auto const lastDigit(std::find_if(str.crbegin(), str.crend(), isDigit));
    if (!incSpelled) {
        return *lastDigit - '0';
    } else {
        std::string::const_reverse_iterator lastNum(str.crend());
        int lastNumIdx(-1);
        for (int i(0); i < 9; ++i) {
            auto const num(NUMBERS[i]);
            auto const p(std::search(str.crbegin(), str.crend(),
                                     num.crbegin(), num.crend()));
            if (p < lastNum) {
                lastNum = p;
                lastNumIdx = i;
            }
        }
        if (lastDigit < lastNum) {
            return *lastDigit - '0';
        } else {
            return lastNumIdx + 1;
        }
    }
}

int main(int const argc, char const * const * const argv) {
    std::ifstream input(argv[1], std::ios::in);
    std::string line;
    int part1(0);
    int part2(0);
    while (std::getline(input, line)) {
        part1 += firstDigitFromString(line, false) * 10
                 + lastDigitFromString(line, false);
        part2 += firstDigitFromString(line, true) * 10
                 + lastDigitFromString(line, true);
    }
    std::cout << "Part 1: " << part1 << std::endl;
    std::cout << "Part 2: " << part2 << std::endl;
    return 0;
}
