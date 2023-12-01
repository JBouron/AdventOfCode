#include <iostream>
#include <fstream>
#include <algorithm>

int main(int const argc, char const * const * const argv) {
    std::ifstream input(argv[1], std::ios::in);
    std::string line;
    int part1(0);
    int part2(0);
    std::string const numbers[] = {
        "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    };
    while (std::getline(input, line)) {
        auto const isDigit([](char const c) {
            return '0' <= c && c <= '9';
        });

        // Part 1.
        // Find the first and last digit. All lines have at least one digit.
        auto const firstDigit(std::find_if(line.cbegin(),
                                           line.cend(),
                                           isDigit));
        auto const lastDigit(std::find_if(line.crbegin(),
                                          line.crend(),
                                          isDigit));
        part1 += int(*firstDigit - '0') * 10;
        part1 += int(*lastDigit - '0');

        // Part 2.
        // Find the first and last number. A number is either a digit or a
        // spelled out number in the string. All lines have at least one number.
        // Re-use firstDigit and lastDigit from part1.
        std::string::const_iterator firstSpelled(line.cend());
        int firstSpelledIdx(-1);
        std::string::const_reverse_iterator lastSpelled(line.crend());
        int lastSpelledIdx(-1);
        for (int i(0); i < 9; ++i) {
            auto const num(numbers[i]);
            auto const f(std::search(line.cbegin(),
                                     line.cend(),
                                     num.cbegin(),
                                     num.cend()));
            if (f < firstSpelled) {
                firstSpelled = f;
                firstSpelledIdx = i;
            }
            auto const l(std::search(line.crbegin(),
                                     line.crend(),
                                     num.crbegin(),
                                     num.crend()));
            if (l != line.crend() && l < lastSpelled) {
                lastSpelled = l;
                lastSpelledIdx = i;
            }
        }

        auto const f(std::min(firstDigit, firstSpelled));
        if (firstSpelledIdx == -1 || isDigit(*f)) {
            // First digit is before the first spelled out number.
            part2 += int(*firstDigit - '0') * 10;
        } else {
            // First spelled out number is before the first digit.
            part2 += (firstSpelledIdx + 1) * 10;
        }

        auto const l(std::min(lastDigit, lastSpelled));
        if (lastSpelledIdx == -1 || isDigit(*l)) {
            part2 += int(*lastDigit - '0');
        } else {
            part2 += (lastSpelledIdx + 1);
        }
    }
    std::cout << "Part 1: " << part1 << std::endl;
    std::cout << "Part 2: " << part2 << std::endl;
    return 0;
}
