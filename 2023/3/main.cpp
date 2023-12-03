#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <functional>
#include <map>
#include <assert.h>

static bool isDigit(char const ch) {
    return '0' <= ch && ch <= '9';
}

static bool isSym(char const ch) {
    return !isDigit(ch) && ch != '.';
}

static std::vector<std::vector<int>> findSyms(
    std::vector<std::string> const& lines) {
    std::vector<std::vector<int>> res(lines.size());
    for (int i(0); i < lines.size(); ++i) {
        std::string const& l(lines[i]);
        auto it(std::find_if(l.begin(), l.end(), isSym));
        while (it != l.end()) {
            res[i].push_back(it - l.begin());            
            it = std::find_if(it + 1, l.end(), isSym);
        }
    }
    return res;
}

static bool contains(std::vector<int> const& v, std::function<bool(int)> pred) {
    return std::find_if(v.begin(), v.end(), pred) != v.end();
}

static void run(std::vector<std::string> const& lines) {
    int part1(0);
    int part2(0);
    std::vector<std::vector<int>> syms(findSyms(lines));
    std::map<std::pair<int, int>, std::vector<int>> adj;
    for (int i(0); i < lines.size(); ++i) {
        std::string const& l(lines[i]);
        auto numStart(std::find_if(l.begin(), l.end(), isDigit));
        auto numEnd(std::find_if_not(numStart + 1, l.end(), isDigit));
        while (numStart != l.end()) {
            // We have a number between numStart and numEnd excluded. Check the
            // above, curr and below line for adjacent symbols.
            int const idxStart(std::max(0L, numStart - l.begin() - 1));
            int const idxEnd(numEnd - l.begin());

            // Part 1:
            auto const pred([&](int const idx) {
                return idxStart <= idx && idx <= idxEnd;
            });
            bool const isPartNum(
                (i > 0 && contains(syms[i-1], pred)) ||
                (contains(syms[i], pred)) ||
                (i < lines.size()-1 && contains(syms[i+1], pred))
            );
            int const startIdx(numStart - l.begin());
            int const len(numEnd - numStart);
            int const num(std::stoi(l.substr(startIdx, len)));
            if (isPartNum) {
                part1 += num;
            }

            // Part 2:
            auto const lamb([&](int const i) {
                std::vector<int> const& s(syms[i]);
                auto it(std::find_if(s.begin(), s.end(), pred));
                while (it != s.end()) {
                    auto const key(std::make_pair(i, *it));
                    adj[key].push_back(num);
                    it = std::find_if(it + 1, s.end(), pred);
                }
            });
            if (i > 0) {
                lamb(i-1);
            }
            lamb(i);
            if (i < lines.size()-1) {
                lamb(i+1);
            }

            numStart = std::find_if(numEnd, l.end(), isDigit);
            numEnd = std::find_if_not(numStart + 1, l.end(), isDigit);
        }
    }
    for (const auto& [key, value] : adj) {
        if (value.size() == 2) {
            part2 += value[0] * value[1];
        }
    }
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
