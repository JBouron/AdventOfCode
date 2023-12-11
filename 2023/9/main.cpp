#include "../util.hpp"

using Sequence = std::vector<i64>;

static Sequence getDiff(Sequence const& seq) {
    assert(seq.size() >= 2);
    Sequence res;
    for (u64 i(1); i < seq.size(); ++i) {
        res.push_back(seq[i] - seq[i-1]);
    }
    return res;
}

static bool allZeroes(Sequence const& seq) {
    for (i64 const& e : seq) {
        if (!!e) {
            return false;
        }
    }
    return true;
}

static i64 extrapolate(Sequence const& seq, bool const part2) {
    if (allZeroes(seq)) {
        return 0;
    } else {
        Sequence const diff(getDiff(seq));
        assert(diff.size() == seq.size() - 1);
        i64 const diffExtra(extrapolate(diff, part2));
        if (part2) {
            return seq[0] - diffExtra;
        } else {
            return seq[seq.size()-1] + diffExtra;
        }
    }
}

static void run(std::vector<std::string> const& lines) {
    std::vector<Sequence> sequences;
    std::for_each(lines.begin(), lines.end(), [&](std::string const& l) {
        Sequence seq;
        // A bit nasty because Util::extractNums only support unsigned ints.
        std::vector<std::string> const parts(Util::split(l, " "));
        std::for_each(parts.begin(), parts.end(), [&](std::string const& str) {
            seq.push_back(std::stoll(str));
        });
        sequences.push_back(seq);
    });

    // Part 1 & 2
    i64 part1(0);
    i64 part2(0);
    for (Sequence const& s : sequences) {
        part1 += extrapolate(s, false);
        part2 += extrapolate(s, true);
    }
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
