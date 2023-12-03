// Compile with --std=c++20!.
#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include <assert.h>

std::vector<std::string> split(std::string const& str, char const ch) {
    std::vector<std::string> res;
    std::string::size_type pos(0);
    while (pos < std::string::npos) {
        auto const nextPos(str.find(ch, pos));
        if (nextPos != pos) {
            res.push_back(str.substr(pos, nextPos - pos));
        }
        pos = nextPos + !!(nextPos != std::string::npos);
    }
    return res;
}

std::string removeChar(std::string const& str, char const ch) {
    std::string res; 
    for (auto it(str.begin()); it != str.end(); ++it) {
        if (*it != ch) {
            res += *it;
        }
    }
    return res;
}

int main(int const argc, char ** const argv) {
    assert(argc == 2);
    std::ifstream file(argv[1], std::ios::in);
    std::string line;
    int part1(0);
    int part2(0);
    while (std::getline(file, line)) {
        line = removeChar(removeChar(line, ';'), ',');
        auto const parts(split(line, ' '));
        std::map<std::string, int> m({{"red", 0}, {"green", 0}, {"blue", 0}});
        for (int i(3); i < parts.size(); i += 2) {
            auto const& color(parts[i]);
            assert(m.contains(color));
            m[color] = std::max(m[color], std::stoi(parts[i-1]));
        }
        if (m["red"] <= 12 && m["green"] <= 13 && m["blue"] <= 14) {
            auto const id(std::stoi(removeChar(parts[1], ':')));
            part1 += id;
        }
        part2 += m["red"] * m["green"] * m["blue"];
    }
    std::cout << "Part 1: " << part1 << std::endl;
    std::cout << "Part 2: " << part2 << std::endl;
    return 0;
}
