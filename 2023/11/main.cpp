#include "../util.hpp"

using namespace Util;

enum class Tile : char {
    EMPTY = '.',
    GAL = '#',
};

static std::vector<i64> emptyRows(Grid<Tile> const& grid) {
    std::vector<i64> res;
    for (i64 y(0); y < grid.height(); ++y) {
        i64 x(0);
        while (x < grid.width() && grid[Pos2d(x, y)] == Tile::EMPTY) { ++x; }
        if (x == grid.width()) {
            res.push_back(y);
        }
    }
    return res;
}

static std::vector<i64> emptyCols(Grid<Tile> const& grid) {
    std::vector<i64> res;
    for (i64 x(0); x < grid.width(); ++x) {
        i64 y(0);
        while (y < grid.height() && grid[Pos2d(x, y)] == Tile::EMPTY) { ++y; }
        if (y == grid.height()) {
            res.push_back(x);
        }
    }
    return res;
}

static void run(std::vector<std::string> const& lines) {
    Grid<Tile> grid(lines, [](char const c) { return static_cast<Tile>(c); });
    std::vector<i64> const emptyRowsIdx(emptyRows(grid));
    std::vector<i64> const emptyColsIdx(emptyCols(grid));

    std::set<Pos2d> const tmp(grid.find(Tile::GAL));
    std::vector<Pos2d> const galaxies(tmp.begin(), tmp.end());

    auto const runPart([&](bool const isPart2) {
        i64 res(0);
        i64 const scale(isPart2 ? 1000000 : 2);
        for (u64 i(0); i < galaxies.size(); ++i) {
            for (u64 j(i); j < galaxies.size(); ++j) {
                Pos2d const& g1(galaxies[i]);
                Pos2d const& g2(galaxies[j]);

                i64 const numCrossingsR(std::count_if(
                    emptyRowsIdx.begin(), emptyRowsIdx.end(), [&](i64 const e) {
                    assert(e != g1.y && e != g2.y);
                    return std::min(g1.y, g2.y) < e && e < std::max(g1.y, g2.y);
                }));
                i64 const numCrossingsC(std::count_if(
                    emptyColsIdx.begin(), emptyColsIdx.end(), [&](i64 const e) {
                    assert(e != g1.x && e != g2.x);
                    return std::min(g1.x, g2.x) < e && e < std::max(g1.x, g2.x);
                }));
                i64 const numCrossings(numCrossingsR + numCrossingsC);

                res += g1.manDistance(g2) + (scale - 1) * numCrossings;
            }
        }
        return res;
    });
    i64 part1(runPart(false));
    i64 part2(runPart(true));

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
