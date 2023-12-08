#include "../util.hpp"

struct Hand {
    std::string cards;
    u64 bid;
};

static std::map<char, u64> countCards(std::string_view const& cards) {
    return Util::occurences(cards.cbegin(), cards.cend());
}

enum class Type : u8 {
    HighCard,
    OnePair,
    TwoPair,
    ThreeOfAKind,
    FullHouse,
    FourOfAKind,
    FiveOfAKind,
};

// Set to true when running for part2. Modifies the behaviour of the comparison
// function so that 'J' acts as a joker.
static bool UseJokers = false;

// Apply the jokers in a hand so that it returns the strongest possible hand.
static std::string applyJokers(std::string_view const& cards) {
    if (cards.find("1") == std::string::npos) {
        // No jokers, nothing to replace.
        return std::string(cards);
    }
    std::map<char, u64> const c(countCards(cards));
    // Replace all 'J' with the card that appears the most in the hand. It does
    // not matter which card we pick in case we have a HighCard hand because 'J'
    // keep their value when comparing card-wise.
    auto const max(*std::max_element(c.cbegin(), c.cend(),
        [&](auto const& a, auto const& b) {
            if (a.first == '1') {
                return true;
            } else if (b.first == '1') {
                return false;
            } else {
                return a.second < b.second;
            }
    }));
    return Util::replace(cards, '1', max.first);
}

static Type getType(std::string_view const& cards) {
    std::string const tmp(UseJokers ? applyJokers(cards) : cards);
    std::map<char, u64> const c(countCards(tmp));
    if (c.size() == 1) {
        return Type::FiveOfAKind;
    } else if (c.size() == 2) {
        if (Util::values(c).contains(4)) {
            return Type::FourOfAKind;
        } else {
            return Type::FullHouse;
        }
    } else if (c.size() == 3) {
        if (Util::values(c).contains(3)) {
            return Type::ThreeOfAKind;
        } else {
            return Type::TwoPair;
        }
    } else if (c.size() == 4) {
        return Type::OnePair;
    } else {
        return Type::HighCard;
    }
}

static bool compareHands(Hand const& h1, Hand const& h2) {
    Type const t1(getType(h1.cards));
    Type const t2(getType(h2.cards));
    if (static_cast<u8>(t1) < static_cast<u8>(t2)) {
        return true;
    } else if (static_cast<u8>(t2) < static_cast<u8>(t1)) {
        return false;
    } else {
        // Compare the cards one-by-one. Because T, J, Q, K and A have been
        // replaced with ascii chars after '9' we can simply lexicographically
        // compare the strings.
        return h1.cards < h2.cards;
    }
}

static void run(std::vector<std::string> const& lines) {
    std::vector<Hand> hands;

    // Part 1:
    std::for_each(lines.begin(), lines.end(), [&](std::string const& l) {
        std::vector<std::string> const parts(Util::split(l, " "));
        assert(parts.size() == 2);
        u64 const bid(std::stoll(parts[1]));
        std::string cards(parts[0]);
        cards = Util::replace(cards, 'T', ':');
        cards = Util::replace(cards, 'J', ';');
        cards = Util::replace(cards, 'Q', '<');
        cards = Util::replace(cards, 'K', '=');
        cards = Util::replace(cards, 'A', '>');
        hands.emplace_back(cards, bid);
    });
    std::sort(hands.begin(), hands.end(), compareHands);
    u64 part1(0);
    for (u64 i(0); i < hands.size(); ++i) {
        part1 += (i+1) * hands[i].bid;
    }

    // Part 2:
    UseJokers = true;
    // Reprocess the input as the value of J changes.
    hands.clear();
    std::for_each(lines.begin(), lines.end(), [&](std::string const& l) {
        std::vector<std::string> const parts(Util::split(l, " "));
        assert(parts.size() == 2);
        u64 const bid(std::stoll(parts[1]));
        std::string cards(parts[0]);
        cards = Util::replace(cards, 'T', ':');
        cards = Util::replace(cards, 'J', '1');
        cards = Util::replace(cards, 'Q', '<');
        cards = Util::replace(cards, 'K', '=');
        cards = Util::replace(cards, 'A', '>');
        hands.emplace_back(cards, bid);
    });
    std::sort(hands.begin(), hands.end(), compareHands);
    u64 part2(0);
    for (u64 i(0); i < hands.size(); ++i) {
        part2 += (i+1) * hands[i].bid;
    }
    std::cout << "Part1: " << part1 << std::endl;
    std::cout << "Part2: " << part2 << std::endl;
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
