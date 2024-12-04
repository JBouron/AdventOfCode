use std::env;
use std::fs;

fn str_find(haystack: &str,
            needle: &str,
            start_pos: usize,
            end_pos: usize) -> Option<usize> {
    match haystack[start_pos..end_pos].find(needle) {
        Some(p) => Some(start_pos + p),
        None => None,
    }
}

fn solve(input: &str, part2: bool) -> u32 {
    let mut sol = 0;
    let mut pos = 0;
	let mut mul_enabled = true;
    while pos < input.len() {
        let mul_pos = str_find(input, "mul(", pos, input.len());
        if let None = mul_pos {
            // There are no more mul instructions, we can stop now.
            break;
        }
        let mul_pos = mul_pos.unwrap();

		if part2 {
            // Check if there was a "do()" or "don't()" between pos and the
            // current mul instruction.
            let do_pos = str_find(input, "do()", pos, mul_pos);
            let dont_pos = str_find(input, "don't()", pos, mul_pos);
            match (do_pos, dont_pos) {
                (Some(p1), Some(p2)) => mul_enabled = p2 < p1,
                (Some(_), None)      => mul_enabled = true,
                (None, Some(_))      => mul_enabled = false,
                _                    => (),
            };
		}

        let comma_pos = str_find(input, ",", mul_pos, input.len());
        if let None = comma_pos {
            // If there are no commas to the right of the current position then
            // there is no way there is a valid mul instruction and thus we can
            // stop here.
            break;
        }
        let comma_pos = comma_pos.unwrap();

        let paren_pos = str_find(input, ")", comma_pos, input.len());
        if let None = paren_pos {
            // If there are no parenthesis to the right of the current position
            // then there is no way there is a valid mul instruction and thus we
            // can stop here.
            break;
        }
        let paren_pos = paren_pos.unwrap();


        let left = input[mul_pos + 4 .. comma_pos].parse::<u32>();
        let right = input[comma_pos + 1 .. paren_pos].parse::<u32>();
        match (left, right) {
            (Ok(l), Ok(r)) => {
                if !part2 || mul_enabled {
                    sol += l * r;
                }
                pos = paren_pos + 1;
            },
            _ => {
                // If we fail to parse the current mul instruction, only skip
                // over the "mul(". This is because there could be another mul
                // instruction such as "mul(mul(3,4))".
                pos = pos + 4;
            },
        };
    }
	sol
}

fn main() {
    let file_name = &env::args().collect::<Vec<_>>()[1];
    let contents: &str = &fs::read_to_string(file_name)
        .expect("Failed to read input");

	let part1 = solve(contents, false);
	let part2 = solve(contents, true);
    println!("Part 1: {part1}");
    println!("Part 2: {part2}");
}
