#include "../util.hpp"

enum class State : char {
    OP = '.',
    DAM = '#',
    UNK = '?'
};

struct Row {
    std::vector<State> springs;
    std::vector<u64> groups;

    bool isValid() const {
        assert(std::find(springs.begin(), springs.end(), State::UNK) == springs.end());
        std::vector<u64> actGroups;
        auto pos(std::find(springs.begin(), springs.end(), State::DAM));
        while (pos != springs.end()) {
            auto const end(std::find(pos, springs.end(), State::OP));
            actGroups.push_back(std::distance(pos, end));
            pos = std::find(end, springs.end(), State::DAM);
        }
        return actGroups == groups;
    }
};

static Row parseLine(std::string const& line) {
    std::vector<std::string> const parts(Util::split(line, " "));
    assert(parts.size() == 2);

    std::vector<State> spr;
    for (char const c : parts[0]) {
        spr.push_back(static_cast<State>(c)); 
    }

    std::vector<u64> const nums(Util::extractNums(parts[1]));
    return Row(spr, nums);
}

static u64 countArrangements(Row const& row) {
    u64 arr(0);

    std::function<void(Row&, u64)> inner;
    inner = [&](Row& row, u64 const i) {
        if (i == row.springs.size()) {
            if (row.isValid()) {
                arr++;
            }
        } else if (row.springs[i] == State::UNK) {
            Row n(row);
            n.springs[i] = State::OP;
            inner(n, i + 1);

            n = row;
            n.springs[i] = State::DAM;
            inner(n, i + 1);
        } else {
            inner(row, i + 1);
        }
    };

    Row r(row);
    inner(r, 0);
    return arr;
}

static void run(std::vector<std::string> const& lines) {
    u64 part1(0);
    std::vector<Row> const rows(Util::map(lines, parseLine));
    u64 i(0);
    for (Row const& r : rows) {
        part1 += countArrangements(r);
        std::cerr << "\rProcessed row " << i;
        ++i;
    }
    std::cerr << std::endl;

    std::cout << "Part 1: " << part1 << std::endl;
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
