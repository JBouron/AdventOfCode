#include "../util.hpp"
#include <numeric>

static void run(std::vector<std::string> const& lines) {
    assert(lines.size() > 2);
    std::string const steps(lines[0]);
    std::map<std::string, std::pair<std::string, std::string>> nodes;
    std::for_each(lines.begin() + 1, lines.end(), [&](std::string const l) {
        // We assume all node mappings are of the form: AAA = (BBB, CCC).
        assert(l.size() == 16);
        std::string const nodeName(l.substr(0, 3));
        std::string const left(l.substr(7, 3));
        std::string const right(l.substr(12, 3));
        nodes[nodeName] = std::make_pair(left, right);
    });

    // Part 1:
    u64 stepNumber(0);
    u64 const mod(steps.size());
    std::string currNode("AAA");
    while (currNode != "ZZZ") {
        char const nextStep(steps[stepNumber % mod]);
        if (nextStep == 'L') {
            currNode = nodes[currNode].first;
        } else {
            currNode = nodes[currNode].second;
        }
        stepNumber++;
    }
    u64 const part1(stepNumber);

    // Part 2: TODO
    u64 part2(0);

    std::cout << "Part 1: " << part1 << std::endl;
    std::cout << "Part 2: " << part2 << std::endl;
}

int main(int const argc, char ** const argv) {
    if (argc < 2) {
        std::cerr << "Expected filename as argument" << std::endl;
        std::exit(1);
    } else {
        std::vector<std::string> const lines(Util::readFile(argv[1], true));
        run(lines);
    }
    return 0;
}
