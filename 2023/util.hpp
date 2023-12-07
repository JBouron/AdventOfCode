// Utility functions and types used by many of the solutions.

#include <vector>
#include <stdint.h>

using u8  = uint8_t;
using u16 = uint16_t;
using u32 = uint32_t;
using u64 = uint64_t;
using i8  = int8_t;
using i16 = int16_t;
using i32 = int32_t;
using i64 = int64_t;

namespace Util {

// Read the contents of a file and return its lines.
// @param fileName: Path to the file to read.
// @param skipEmptyLines: If true, the resulting vector does not contain the
// empty lines found in the file.
// @return: A vector containing all the lines of the file.
std::vector<std::string> readFile(std::string const& fileName,
                                  bool const skipEmptyLines=false) {
    std::ifstream file(fileName, std::ios::in);
    if (!file) {
        std::cerr << "Cannot open file " << fileName << std::endl;
        std::exit(1);
    }
    std::vector<std::string> lines;
    std::string line;
    while (std::getline(file, line)) {
        if (!skipEmptyLines || line.size()) {
            lines.push_back(line);
        }
    }
    return lines;
}

// Check if a character is a digit.
// @param ch: The character to test.
// @return: true if `ch` is a digit [0-9], false otherwise.
bool isDigit(char const ch) {
    return '0' <= ch && ch <= '9';
}

// Extract all numbers appearing in a string. Numbers can be separated by any
// character that is not a digit.
// @param line: The string to extract the numbers from.
// @return: A vector<u64> containing all numbers of the string, in the same
// order as they appear in the string.
std::vector<u64> extractNums(std::string_view const& line) {
    std::vector<u64> res;
    auto it(std::find_if(line.begin(), line.end(), isDigit));
    while (it != line.end()) {
        auto const endOfNum(std::find_if_not(it, line.end(), isDigit));
        u32 const len(endOfNum - it);
        // FIXME: std::stoll() does not support string_views, we need to copy the
        // view into a string before converting it to a u64.
        std::string const numStr(line.substr(it - line.begin(), len));
        res.push_back(std::stoll(numStr));
        it = std::find_if(endOfNum, line.end(), isDigit);
    }
    return res;
}

// Split a string around a substring.
// @param line: The string to split.
// @param splitOn: The substring to split around.
// @return: A vector containing the result of the split. This vector does not
// contain empty strings, e.g. split("abaab", "a") returns {"b", "b"}.
std::vector<std::string> split(std::string_view const& line,
                               std::string_view const& splitOn) {
    std::vector<std::string> res;
    std::string_view::size_type pos(0);
    while (pos < line.size()) {
        std::string_view::size_type const findRes(line.find(splitOn, pos));
        std::string_view::size_type const nextOcc(findRes == std::string::npos ?
            line.size() : findRes);
        if (nextOcc != pos) {
            res.push_back(std::string(line.substr(pos, nextOcc - pos)));
        }
        pos = nextOcc + splitOn.size();
    }
    return res;
}
}
