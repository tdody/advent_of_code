# Path: 2025/src/day_5.py

"""
--- Day 5: Cafeteria ---
As the forklifts break through the wall, the Elves are delighted to discover that there was a cafeteria on the other side after all.

You can hear a commotion coming from the kitchen. "At this rate, we won't have any time left to put the wreaths up in the dining hall!" Resolute in your quest, you investigate.

"If only we hadn't switched to the new inventory management system right before Christmas!" another Elf exclaims. You ask what's going on.

The Elves in the kitchen explain the situation: because of their complicated new inventory management system, they can't figure out which of their ingredients are fresh and which are spoiled. When you ask how it works, they give you a copy of their database (your puzzle input).

The database operates on ingredient IDs. It consists of a list of fresh ingredient ID ranges, a blank line, and a list of available ingredient IDs. For example:

3-5
10-14
16-20
12-18

1
5
8
11
17
32
The fresh ID ranges are inclusive: the range 3-5 means that ingredient IDs 3, 4, and 5 are all fresh. The ranges can also overlap; an ingredient ID is fresh if it is in any range.

The Elves are trying to determine which of the available ingredient IDs are fresh. In this example, this is done as follows:

Ingredient ID 1 is spoiled because it does not fall into any range.
Ingredient ID 5 is fresh because it falls into range 3-5.
Ingredient ID 8 is spoiled.
Ingredient ID 11 is fresh because it falls into range 10-14.
Ingredient ID 17 is fresh because it falls into range 16-20 as well as range 12-18.
Ingredient ID 32 is spoiled.
So, in this example, 3 of the available ingredient IDs are fresh.

Process the database file from the new inventory management system. How many of the available ingredient IDs are fresh?

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
The Elves start bringing their spoiled inventory to the trash chute at the back of the kitchen.

So that they can stop bugging you when they get new inventory, the Elves would like to know all of the IDs that the fresh ingredient ID ranges consider to be fresh. An ingredient ID is still considered fresh if it is in any range.

Now, the second section of the database (the available ingredient IDs) is irrelevant. Here are the fresh ingredient ID ranges from the above example:

3-5
10-14
16-20
12-18
The ingredient IDs that these ranges consider to be fresh are 3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, and 20. So, in this example, the fresh ingredient ID ranges consider a total of 14 ingredient IDs to be fresh.

Process the database file again. How many ingredient IDs are considered to be fresh according to the fresh ingredient ID ranges?
"""


class Range:
    min: int
    max: int

    def __init__(self, min: int, max: int) -> None:
        self.min = min
        self.max = max

    def __repr__(self) -> str:
        return f"{self.min}-{self.max}"

    @classmethod
    def from_string(cls, string: str) -> "Range":
        min, max = string.split("-")
        return cls(int(min), int(max))

    def contains_ingredient(self, ingredient: int) -> bool:
        return self.min <= ingredient <= self.max

    def __len__(self) -> int:
        return self.max - self.min + 1

    def __eq__(self, other: "Range") -> bool:
        return self.min == other.min and self.max == other.max

    def __lt__(self, other: "Range") -> bool:
        return self.min < other.min


def read_input(file_path: str) -> tuple[list[Range], list[int]]:
    with open(file_path, "r") as file:
        lines = file.readlines()

    ranges = []
    ingredients = []
    for line in lines:
        if "-" in line:
            ranges.append(Range.from_string(line.strip()))
        elif line.strip().isdigit():
            ingredients.append(int(line.strip()))

    return ranges, ingredients


def part_1(file_path: str) -> int:
    """
    Read the input file and return the solution.
    """

    ranges, ingredients = read_input(file_path)
    fresh_ingredients_count = 0
    for ingredient in ingredients:
        for range in ranges:
            if range.contains_ingredient(ingredient):
                fresh_ingredients_count += 1
                break

    return fresh_ingredients_count


# --- Part Two ---


def part_2(file_path: str) -> int:
    """
    Read the input file and return the solution.
    """

    ranges, _ = read_input(file_path)

    ranges.sort()
    max_seen_index = 0

    total_range_length = 0

    for r in ranges:
        # Option 1: The considered range doesn't overlap with previous ranges
        if r.min > max_seen_index:
            total_range_length += len(r)
            max_seen_index = r.max
        # Option 2: range.min == max_seen_index
        elif r.min == max_seen_index:
            total_range_length += len(r) - 1
            max_seen_index = r.max
        # Option 3: range.min<max_seen_index<range.max
        elif r.min < max_seen_index < r.max:
            total_range_length += len(Range(max_seen_index + 1, r.max))
            max_seen_index = r.max
        # Option 4: range.max == max_seen_index
        elif r.max == max_seen_index:
            continue
        # Option 5: range.max < max_seen_index
        elif r.max < max_seen_index:
            continue

    return total_range_length
