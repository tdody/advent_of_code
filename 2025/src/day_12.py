# Path: 2025/src/day_12.py

"""
--- Day 12: Christmas Tree Farm ---
You're almost out of time, but there can't be much left to decorate. Although there are no stairs, elevators, escalators, tunnels, chutes, teleporters, firepoles, or conduits here that would take you deeper into the North Pole base, there is a ventilation duct. You jump in.

After bumping around for a few minutes, you emerge into a large, well-lit cavern full of Christmas trees!

There are a few Elves here frantically decorating before the deadline. They think they'll be able to finish most of the work, but the one thing they're worried about is the presents for all the young Elves that live here at the North Pole. It's an ancient tradition to put the presents under the trees, but the Elves are worried they won't fit.

The presents come in a few standard but very weird shapes. The shapes and the regions into which they need to fit are all measured in standard units. To be aesthetically pleasing, the presents need to be placed into the regions in a way that follows a standardized two-dimensional unit grid; you also can't stack presents.

As always, the Elves have a summary of the situation (your puzzle input) for you. First, it contains a list of the presents' shapes. Second, it contains the size of the region under each tree and a list of the number of presents of each shape that need to fit into that region. For example:

0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
The first section lists the standard present shapes. For convenience, each shape starts with its index and a colon; then, the shape is displayed visually, where # is part of the shape and . is not.

The second section lists the regions under the trees. Each line starts with the width and length of the region; 12x5 means the region is 12 units wide and 5 units long. The rest of the line describes the presents that need to fit into that region by listing the quantity of each shape of present; 1 0 1 0 3 2 means you need to fit one present with shape index 0, no presents with shape index 1, one present with shape index 2, no presents with shape index 3, three presents with shape index 4, and two presents with shape index 5.

Presents can be rotated and flipped as necessary to make them fit in the available space, but they have to always be placed perfectly on the grid. Shapes can't overlap (that is, the # part from two different presents can't go in the same place on the grid), but they can fit together (that is, the . part in a present's shape's diagram does not block another present from occupying that space on the grid).

The Elves need to know how many of the regions can fit the presents listed. In the above example, there are six unique present shapes and three regions that need checking.

The first region is 4x4:

....
....
....
....
In it, you need to determine whether you could fit two presents that have shape index 4:

###
#..
###
After some experimentation, it turns out that you can fit both presents in this region. Here is one way to do it, using A to represent one present and B to represent the other:

AAA.
ABAB
ABAB
.BBB
The second region, 12x5: 1 0 1 0 2 2, is 12 units wide and 5 units long. In that region, you need to try to fit one present with shape index 0, one present with shape index 2, two presents with shape index 4, and two presents with shape index 5.

It turns out that these presents can all fit in this region. Here is one way to do it, again using different capital letters to represent all the required presents:

....AAAFFE.E
.BBBAAFFFEEE
DDDBAAFFCECE
DBBB....CCC.
DDD.....C.C.
The third region, 12x5: 1 0 1 0 3 2, is the same size as the previous region; the only difference is that this region needs to fit one additional present with shape index 4. Unfortunately, no matter how hard you try, there is no way to fit all of the presents into this region.

So, in this example, 2 regions can fit all of their listed presents.

Consider the regions beneath each tree and the presents the Elves would like to fit into each of them. How many of the regions can fit all of the presents listed?


The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
The Elves thank you profusely for the help and start rearranging the oddly-shaped presents. As you look up, you notice that a lot more Elves have arrived here at the Christmas tree farm.

In fact, many of these new arrivals look familiar: they're the Elves you helped while decorating the North Pole base. Right on schedule, each group seems to have brought a star to put atop one of the Christmas trees!

Before any of them can find a ladder, a particularly large Christmas tree suddenly flashes brightly when a large star magically appears above it! As your eyes readjust, you think you notice a portly man with a white beard disappear into the crowd.

You go look for a ladder; only 23 stars to go.
"""

import re

from loguru import logger


class Present:
    index: int
    shape: list[list[str]]
    width: int
    height: int

    def __init__(self, index: int, shape: list[list[str]], width: int, height: int):
        self.index = index
        self.shape = shape
        self.width = width
        self.height = height

    def __str__(self) -> str:
        return f"Box(index={self.index}, shape={self.shape}, width={self.width}, height={self.height})"

    def __repr__(self) -> str:
        return f"Box(index={self.index}, shape={self.shape}, width={self.width}, height={self.height})"

    def __eq__(self, other: "Present") -> bool:
        return self.index == other.index

    def __hash__(self) -> int:
        return hash((self.index, self.width, self.height))

    def n_pound_signs(self) -> int:
        return sum(row.count("#") for row in self.shape)

    @classmethod
    def from_strings(cls, strings: list[str]) -> list["Present"]:
        index_string = strings[0]
        index = int(index_string.split(":")[0])

        shape_strings = strings[1:]
        shape = [list(string) for string in shape_strings]
        width = len(shape[0])
        height = len(shape)
        return cls(index, shape, width, height)


class Region:
    shape: tuple[int, int]
    present_map: list[int]

    def __init__(self, shape: tuple[int, int], present_map: list[int]):
        self.shape = shape
        self.present_map = present_map

    @classmethod
    def from_string(cls, string: str) -> "Region":
        shape_str, present_str = string.split(": ")
        shape = tuple(map(int, shape_str.split("x")))
        present_map = [int(char) for char in present_str.split(" ")]
        return cls(shape, present_map)

    def __str__(self) -> str:
        return f"Region(shape={self.shape}, present_map={self.present_map})"

    def __repr__(self) -> str:
        return f"Region(shape={self.shape}, present_map={self.present_map})"

    def __eq__(self, other: "Region") -> bool:
        return self.shape == other.shape and self.present_map == other.present_map

    def __hash__(self) -> int:
        return hash((self.shape, tuple(self.present_map)))

    def is_solvable(self, presents: list[Present]) -> bool:
        box_area = self.shape[0] * self.shape[1]
        present_area = 0
        for i in range(len(self.present_map)):
            present = presents[i]
            present_area += present.width * present.height * self.present_map[i]
        if box_area < present_area:
            return False

        n_pound_signs = 0
        for i in range(len(self.present_map)):
            present = presents[i]
            n_pound_signs += present.n_pound_signs() * self.present_map[i]
        return n_pound_signs <= box_area


# --- Part One ---


def part_1(file_path: str) -> int:
    """
    Read the input file and return the solution.
    """

    current_line_batch: list[str] = []
    presents: list[Present] = []
    regions: list[Region] = []
    with open(file_path, "r") as file:
        for line in file:
            if line.strip() == "":
                presents.append(Present.from_strings(current_line_batch))
                current_line_batch = []
            elif re.match(r"^\d+x\d+", line.strip()):
                regions.append(Region.from_string(line.strip()))
            else:
                current_line_batch.append(line.strip())

    logger.info(f"Presents: {presents}")
    logger.info(f"Regions: {regions}")

    solvable_boxes = 0
    for region in regions:
        if region.is_solvable(presents):
            solvable_boxes += 1

    return solvable_boxes


# --- Part Two ---


def part_2(file_path: str) -> int:
    """
    Read the input file and return the solution.
    """

    return 0
