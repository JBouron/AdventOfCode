#include "../util.hpp"

using namespace Util;

enum class Tile : char {
    NS = '|',
    EW = '-',
    NE = 'L',
    NW = 'J',
    SW = '7',
    SE = 'F',
    GRD = '.',
    START = 'S',
};

// Given the position of the starting tile, figure out its type by looking at
// its neighbors. This function assumes that there is a unique solution of the
// type of the starting tile.
static Tile findStartTileType(Grid<Tile> const& grid, Pos2d const& startPos) {
    Pos2d const nPosN(startPos.up());
    Pos2d const nPosS(startPos.down());
    Pos2d const nPosW(startPos.left());
    Pos2d const nPosE(startPos.right());

    Tile const nN(grid.inBounds(nPosN) ? grid[nPosN] : Tile::GRD);
    Tile const nS(grid.inBounds(nPosS) ? grid[nPosS] : Tile::GRD);
    Tile const nW(grid.inBounds(nPosW) ? grid[nPosW] : Tile::GRD);
    Tile const nE(grid.inBounds(nPosE) ? grid[nPosE] : Tile::GRD);

    bool const connN(nN == Tile::NS || nN == Tile::SW || nN == Tile::SE);
    bool const connS(nS == Tile::NS || nS == Tile::NE || nS == Tile::NW);
    bool const connW(nW == Tile::EW || nW == Tile::NE || nW == Tile::SE);
    bool const connE(nE == Tile::EW || nE == Tile::SW || nE == Tile::NW);

    if (connN) {
        if (connS) { return Tile::NS; }
        if (connW) { return Tile::NW; }
        if (connE) { return Tile::NE; }
    }
    if (connS) {
        if (connW) { return Tile::SW; }
        if (connE) { return Tile::SE; }
    }
    if (connW) {
        if (connE) { return Tile::EW; }
    }
    assert(!"Couldn't determine the type of the start tile");
}

// Compute the position of the two neighbors connected to a cell.
static std::pair<Pos2d, Pos2d> neighbors(Grid<Tile> const& grid,
                                         Pos2d const& pos) {
    switch (grid[pos]) {
        case Tile::NS: return std::make_pair(pos.up(), pos.down()); break;
        case Tile::EW: return std::make_pair(pos.left(), pos.right()); break;
        case Tile::NE: return std::make_pair(pos.up(), pos.right()); break;
        case Tile::NW: return std::make_pair(pos.up(), pos.left()); break;
        case Tile::SW: return std::make_pair(pos.down(), pos.left()); break;
        case Tile::SE: return std::make_pair(pos.down(), pos.right()); break;
        default: assert(!"Invalid tile"); break;
    }
}

static void run(std::vector<std::string> const& lines) {
    i64 part1(0);
    i64 part2(0);
    Grid<Tile> grid(lines, [](char const c) { return static_cast<Tile>(c); });
    Grid<int> perim(grid.width(), grid.height(), 0);

    // Find the position and the type of the starting tile.
    auto const res(grid.find(Tile::START));
    assert(res.size() == 1);
    Pos2d const startPos(*res.cbegin());
    Tile const sTile(findStartTileType(grid, startPos));
    grid[startPos] = sTile;

    // Part 1: Follow the perimeter of the loop.
    Pos2d prevPos(startPos);
    Pos2d currPos([&](){
        switch (sTile) {
            case Tile::NS: return startPos.down(); break;
            case Tile::EW: return startPos.right(); break;
            case Tile::NE: return startPos.right(); break;
            case Tile::NW: return startPos.left(); break;
            case Tile::SW: return startPos.down(); break;
            case Tile::SE: return startPos.down(); break;
            default: assert(!"Invalid start tile type");
    }}());

    perim[startPos] = 1;
    while (currPos != startPos) {
        perim[currPos] = 1;
        auto const& [n1, n2] = neighbors(grid, currPos);
        Pos2d const tmp(currPos);
        currPos = n1 != prevPos ? n1 : n2;
        prevPos = tmp;
        part1++;
    }
    part1 = (part1 + 1) / 2;

    // Part 2.
    for (i64 y(0); y < grid.height(); ++y) {
        bool inLoop(false);
        Tile lastCorner(Tile::GRD);
        for (i64 x(0); x < grid.width(); ++x) {
            Pos2d const pos(x, y);
            Tile const tile(grid[pos]);
            bool const flip(perim[pos] && (tile == Tile::NS
                || (tile == Tile::NW && lastCorner == Tile::SE)
                || (tile == Tile::SW && lastCorner == Tile::NE)));
            if (flip) {
                inLoop = !inLoop;
            }
            if (!perim[pos] && inLoop) {
                part2++;
            }
            if (tile == Tile::NE || tile == Tile::NW || tile == Tile::SE ||
                tile == Tile::SW) {
                lastCorner = tile;
            }
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
        std::vector<std::string> const lines(Util::readFile(argv[1], true));
        run(lines);
    }
    return 0;
}
