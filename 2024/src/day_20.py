"""
--- Day 20: Race Condition ---
The Historians are quite pixelated again. This time, a massive, black building looms over you - you're right outside the CPU!

While The Historians get to work, a nearby program sees that you're idle and challenges you to a race. Apparently, you've arrived just in time for the frequently-held race condition festival!

The race takes place on a particularly long and twisting code path; programs compete to see who can finish in the fewest picoseconds. The winner even gets their very own mutex!

They hand you a map of the racetrack (your puzzle input). For example:

###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
The map consists of track (.) - including the start (S) and end (E) positions (both of which also count as track) - and walls (#).

When a program runs through the racetrack, it starts at the start position. Then, it is allowed to move up, down, left, or right; each such move takes 1 picosecond. The goal is to reach the end position as quickly as possible. In this example racetrack, the fastest time is 84 picoseconds.

Because there is only a single path from the start to the end and the programs all go the same speed, the races used to be pretty boring. To make things more interesting, they introduced a new rule to the races: programs are allowed to cheat.

The rules for cheating are very strict. Exactly once during a race, a program may disable collision for up to 2 picoseconds. This allows the program to pass through walls as if they were regular track. At the end of the cheat, the program must be back on normal track again; otherwise, it will receive a segmentation fault and get disqualified.

So, a program could complete the course in 72 picoseconds (saving 12 picoseconds) by cheating for the two moves marked 1 and 2:

###############
#...#...12....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
Or, a program could complete the course in 64 picoseconds (saving 20 picoseconds) by cheating for the two moves marked 1 and 2:

###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...12..#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
This cheat saves 38 picoseconds:

###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.####1##.###
#...###.2.#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
This cheat saves 64 picoseconds and takes the program directly to the end:

###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..21...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
Each cheat has a distinct start position (the position where the cheat is activated, just before the first move that is allowed to go through walls) and end position; cheats are uniquely identified by their start position and end position.

In this example, the total number of cheats (grouped by the amount of time they save) are as follows:

There are 14 cheats that save 2 picoseconds.
There are 14 cheats that save 4 picoseconds.
There are 2 cheats that save 6 picoseconds.
There are 4 cheats that save 8 picoseconds.
There are 2 cheats that save 10 picoseconds.
There are 3 cheats that save 12 picoseconds.
There is one cheat that saves 20 picoseconds.
There is one cheat that saves 36 picoseconds.
There is one cheat that saves 38 picoseconds.
There is one cheat that saves 40 picoseconds.
There is one cheat that saves 64 picoseconds.
You aren't sure what the conditions of the racetrack will be like, so to give yourself as many options as possible, you'll need a list of the best cheats. How many cheats would save you at least 100 picoseconds?

--- Part Two ---
The programs seem perplexed by your list of cheats. Apparently, the two-picosecond cheating rule was deprecated several milliseconds ago! The latest version of the cheating rule permits a single cheat that instead lasts at most 20 picoseconds.

Now, in addition to all the cheats that were possible in just two picoseconds, many more cheats are possible. This six-picosecond cheat saves 76 picoseconds:

###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#1#####.#.#.###
#2#####.#.#...#
#3#####.#.###.#
#456.E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
Because this cheat has the same start and end positions as the one above, it's the same cheat, even though the path taken during the cheat is different:

###############
#...#...#.....#
#.#.#.#.#.###.#
#S12..#.#.#...#
###3###.#.#.###
###4###.#.#...#
###5###.#.###.#
###6.E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
Cheats don't need to use all 20 picoseconds; cheats can last any amount of time up to and including 20 picoseconds (but can still only end when the program is on normal track). Any cheat time not used is lost; it can't be saved for another cheat later.

You'll still need a list of the best cheats, but now there are even more to choose between. Here are the quantities of cheats in this example that save 50 picoseconds or more:

There are 32 cheats that save 50 picoseconds.
There are 31 cheats that save 52 picoseconds.
There are 29 cheats that save 54 picoseconds.
There are 39 cheats that save 56 picoseconds.
There are 25 cheats that save 58 picoseconds.
There are 23 cheats that save 60 picoseconds.
There are 20 cheats that save 62 picoseconds.
There are 19 cheats that save 64 picoseconds.
There are 12 cheats that save 66 picoseconds.
There are 14 cheats that save 68 picoseconds.
There are 12 cheats that save 70 picoseconds.
There are 22 cheats that save 72 picoseconds.
There are 4 cheats that save 74 picoseconds.
There are 3 cheats that save 76 picoseconds.
Find the best cheats using the updated cheating rules. How many cheats would save you at least 100 picoseconds?
"""

import os
from typing import Optional
from loguru import logger
import networkx as nx
from tqdm import tqdm

DIRECTIONS = [(-1, 0), (0, -1), (1, 0), (0, 1)]


class Style:
    RED = "\033[31m"  # Red
    GREEN = "\033[32m"  # Green
    YELLOW = "\033[33m"  # Yellow
    BLUE = "\033[34m"  # Blue
    PURPLE = "\033[35m"  # Purple
    CYAN = "\033[36m"  # Cyan
    WHITE = "\033[37m"  # White

    RESET = "\033[0m"

    @classmethod
    def get_style(cls, char: str) -> str:
        if char == "#":
            return cls.WHITE
        if char == ".":
            return cls.BLUE
        if char == "S" or char == "E":
            return cls.YELLOW
        if char == "O":
            return cls.GREEN
        if char == "X":
            return cls.PURPLE
        return cls.RESET


class Grid:
    graph: nx.DiGraph
    start: tuple[int, int]
    end: tuple[int, int]
    width: int
    height: int
    possible_cheats: list[list[tuple[int, int]]]

    def __init__(
        self,
        graph: nx.DiGraph,
        start: tuple[int, int],
        end: tuple[int, int],
        width: int,
        height: int,
        possible_cheats: list[list[tuple[int, int]]],
    ) -> None:
        self.graph = graph
        self.start = start
        self.end = end
        self.width = width
        self.height = height
        self.possible_cheats = possible_cheats

    @classmethod
    def from_file(cls, file_path: str) -> "Grid":
        with open(file_path, "r") as f:
            data = f.read().splitlines()
            G = nx.DiGraph()

            start = None
            end = None
            width = len(data[0])
            height = len(data)
            possible_cheats: list[list[tuple[int, int]]] = []

            for i, row in enumerate(data):
                for j, col in enumerate(row):
                    if col == "#":
                        continue

                    if col == "S":
                        start = (i, j)
                    elif col == "E":
                        end = (i, j)

                    for dx1, dy1 in DIRECTIONS:
                        x1, y1 = i + dx1, j + dy1

                        if (
                            0 <= x1 < len(data)
                            and 0 <= y1 < len(row)
                            and data[x1][y1] != "#"
                        ):
                            G.add_edge((i, j), (x1, y1), weight=1)

                        elif data[x1][y1] == "#":
                            x2, y2 = x1 + dx1, y1 + dy1

                            if (
                                0 <= x2 < len(data)
                                and 0 <= y2 < len(row)
                                and data[x2][y2] != "#"
                            ):
                                possible_cheats.append([(i, j), (x2, y2)])

            # possible_cheats can contains duplicates that are inverse of each other
            # for example, [(1, 2), (3, 4)] and [(3, 4), (1, 2)]
            # so we need to remove the duplicates
            possible_cheats = list(
                [
                    list(cheat)
                    for cheat in set(tuple(sorted(cheat)) for cheat in possible_cheats)
                ]
            )
            logger.debug(f"Start: {start}")
            logger.debug(f"End: {end}")
            logger.debug(f"Width: {width}")
            logger.debug(f"Height: {height}")
            logger.debug(f"Possible cheat count: {len(possible_cheats)}")

            assert start is not None
            assert end is not None
            return cls(G, start, end, width, height, possible_cheats)

    def shortest_path(self) -> list | dict:
        return nx.shortest_path(self.graph, self.start, self.end)

    def shortest_path_length(self) -> int:
        return nx.shortest_path_length(self.graph, self.start, self.end)

    def plot(
        self,
        path: Optional[list[tuple[int, int]]] = None,
        cheat: Optional[list[tuple[int, int]]] = None,
    ) -> None:
        path_to_plot = path or []
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) in path_to_plot and (i, j) not in [self.start, self.end]:
                    color = Style.get_style("O")
                    print(color + "O" + Style.RESET, end="")
                elif (i, j) == self.start:
                    color = Style.get_style("S")
                    print(color + "S" + Style.RESET, end="")
                elif (i, j) == self.end:
                    color = Style.get_style("E")
                    print(color + "E" + Style.RESET, end="")
                elif (i, j) in self.graph.nodes:
                    color = Style.get_style(".")
                    print(color + "." + Style.RESET, end="")
                elif cheat and (i, j) in cheat:
                    color = Style.get_style("X")
                    print(color + "X" + Style.RESET, end="")
                else:
                    color = Style.get_style("#")
                    print(color + "#" + Style.RESET, end="")

            print()
        print()

    def solve_with_cheats(self, allowed_cheat_duration: int) -> int:
        shortest_path = self.shortest_path()
        path = {loc: dist for dist, loc in enumerate(shortest_path)}

        save_over_100 = 0

        for dx in range(-20, 21):
            for dy in range(-20, 21):
                cheat = abs(dx) + abs(dy)
                if cheat < 2 or cheat > allowed_cheat_duration:
                    continue
                for sx, sy in path:
                    if (sx + dx, sy + dy) in path:
                        if path[sx + dx, sy + dy] - path[sx, sy] - cheat >= 100:
                            save_over_100 += 1

        return save_over_100


# Path: src/day_20.py
# --- Part One ---


def part_1(file_path: str) -> int:
    """
    Read the input file and return the solution.
    """

    grid = Grid.from_file(file_path)

    return grid.solve_with_cheats(allowed_cheat_duration=2)


# --- Part Two ---


def part_2(file_path: str) -> int:
    """
    Read the input file and return the solution.
    """

    grid = Grid.from_file(file_path)

    return grid.solve_with_cheats(allowed_cheat_duration=20)
