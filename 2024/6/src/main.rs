use std::env;
use std::fs;
use std::error::Error;

// NOTE: This is an incomplete solution.

// Represents a 2D position on a grid.
#[derive(Debug)]
struct Pos2d {
    x: u64,
    y: u64,
}

// Type of a cell in the grid.
#[derive(Debug)]
#[derive(Copy,Clone)]
enum CellType {
    Unknown,
    // Empty cell, i.e. the guard can walk through this cell.
    Empty,
    // Cell contains an obstacle, not walkable.
    Obstacle,
    // Cell is occupied by guard.
    Guard,
}

// Represents a rectangular grid of cells.
#[derive(Debug)]
struct Grid<T> {
    // Width of the grid in number of cells.
    width: usize,
    // Height of the grid in number of cells.
    height: usize,
    // The actual contents of the grid.
    cells: Vec<Vec<T>>,
}

impl<T: Copy> Grid<T> {
    // Construct a Grid from a file. Each character in the file is interpreted as being a cell.
    // Thie function expects that all lines in the file have the same length (i.e. same number of
    // cells in all rows).
    // @param filename: Path to the file.
    // @param parser: Function to cast a character to the proper value of type T. Called for each
    // character of each line to determine the value of each cell.
    // @return: A grid, or error if applicable.
    fn from_file(filename: &str, parser: &dyn Fn(char) -> T) -> Result<Grid<T>, Box<dyn Error>> {
        let input = std::fs::read_to_string(filename)?;
        let rows: Vec<Vec<T>> = input.split("\n")
            .filter(|line| line.len() > 0)
            .map(|line| line.chars().map(|c| parser(c)).collect::<Vec<_>>())
            .collect::<Vec<_>>();

        if rows.len() == 0 {
            // Don't accept empty grids.
            return Err("Empty grids not supported".into());
        }

        // Check that all rows have the same length.
        let expected_len = rows[0].len();
        for r in rows.iter().skip(1) {
            if expected_len != r.len() {
                return Err("Not all lines have the same length, invalid grid".into());
            }
        }

        Ok(Grid{width: expected_len, height: rows.len(), cells: rows})
    }

    // Get the string representation of this Grid.
    // @param cell_to_char: Function to cast a cell to a char. Called on every single cell to
    // generate the string representation of the whole grid.
    // @return: A multi-line string showing the grid, including a border.
    fn to_string(&self, cell_to_char: &dyn Fn(T) -> char) -> String {
        let bar = "+".to_owned() + &str::repeat("-", self.width) + "+";

        bar.clone() + "\n" + &self.cells.iter()
            .map(|row| row.iter().map(|cell| cell_to_char(*cell)).collect::<String>())
            .map(|row_str| String::from("|") + &row_str + "|\n")
            .collect::<String>()
            + &bar
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    let filename = std::env::args().nth(1).expect("Missing filename as argument");
    let grid = Grid::from_file(&filename, &|c| match c {
        '.' => CellType::Empty,
        '#' => CellType::Obstacle,
        '^' => CellType::Empty,
        _ => CellType::Unknown,
    })?;

    let cell_to_char = |c| match c {
        CellType::Empty => '.',
        CellType::Obstacle => '#',
        _ => 'U',
    };
    let grid_str = grid.to_string(&cell_to_char);
    println!("{}", grid_str);
    Ok(())
}
