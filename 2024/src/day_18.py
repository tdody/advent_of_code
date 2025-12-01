"""
--- Day 18: RAM Run ---
You and The Historians look a lot more pixelated than you remember. You're inside a computer at the North Pole!

Just as you're about to check out your surroundings, a program runs up to you. "This region of memory isn't safe! The User misunderstood what a pushdown automaton is and their algorithm is pushing whole bytes down on top of us! Run!"

The algorithm is fast - it's going to cause a byte to fall into your memory space once every nanosecond! Fortunately, you're faster, and by quickly scanning the algorithm, you create a list of which bytes will fall (your puzzle input) in the order they'll land in your memory space.

Your memory space is a two-dimensional grid with coordinates that range from 0 to 70 both horizontally and vertically. However, for the sake of example, suppose you're on a smaller grid with coordinates that range from 0 to 6 and the following list of incoming byte positions:

5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
Each byte position is given as an X,Y coordinate, where X is the distance from the left edge of your memory space and Y is the distance from the top edge of your memory space.

You and The Historians are currently in the top left corner of the memory space (at 0,0) and need to reach the exit in the bottom right corner (at 70,70 in your memory space, but at 6,6 in this example). You'll need to simulate the falling bytes to plan out where it will be safe to run; for now, simulate just the first few bytes falling into your memory space.

As bytes fall into your memory space, they make that coordinate corrupted. Corrupted memory coordinates cannot be entered by you or The Historians, so you'll need to plan your route carefully. You also cannot leave the boundaries of the memory space; your only hope is to reach the exit.

In the above example, if you were to draw the memory space after the first 12 bytes have fallen (using . for safe and # for corrupted), it would look like this:

...#...
..#..#.
....#..
...#..#
..#..#.
.#..#..
#.#....
You can take steps up, down, left, or right. After just 12 bytes have corrupted locations in your memory space, the shortest path from the top left corner to the exit would take 22 steps. Here (marked with O) is one such path:

OO.#OOO
.O#OO#O
.OOO#OO
...#OO#
..#OO#.
.#.O#..
#.#OOOO
Simulate the first kilobyte (1024 bytes) falling onto your memory space. Afterward, what is the minimum number of steps needed to reach the exit?

"""

# Path: src/day_18.py
# --- Part One ---

import os

from loguru import logger
from tqdm import tqdm


class Memory:
    size: int
    corrupted: list[tuple[int, int]]

    def __init__(self, size: int, corrupted: list[tuple[int, int]]):
        self.size = size
        self.corrupted = corrupted

    @classmethod
    def from_file(cls, file_path: str):
        corrupted = []
        with open(file_path, "r") as file:
            for line in file:
                x, y = line.strip().split(",")
                corrupted.append((int(x), int(y)))

        max_corrupted = max([max(x, y) for x, y in corrupted])

        if max_corrupted == 6:
            size = 7
        else:
            size = 71

        return cls(size, corrupted)

    def is_corrupted(self, x: int, y: int) -> bool:
        return (x, y) in self.corrupted

    def __str__(self) -> str:
        memory = ""
        for y in range(self.size):
            for x in range(self.size):
                if self.is_corrupted(x, y):
                    memory += "#"
                else:
                    memory += "."
            memory += "\n"
        return memory

    def plot_path(self, path: list[tuple[int, int]]) -> str:
        memory = ""
        for y in range(self.size):
            for x in range(self.size):
                if (x, y) in path:
                    memory += "O"
                elif self.is_corrupted(x, y):
                    memory += "#"
                else:
                    memory += "."
            memory += "\n"
        return memory

    def __repr__(self) -> str:
        return self.__str__()


def bfs(memory: Memory, start: tuple[int, int], end: tuple[int, int]) -> int:
    queue = [(start, 0)]
    visited = set([start])

    logger.debug(f"Start: {start}")
    logger.debug(f"End: {end}")

    while queue:
        current, steps = queue.pop(0)
        logger.debug(f"Current: {current}")

        if current == end:
            return steps

        x, y = current

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = x + dx, y + dy

            if new_x < 0 or new_x >= memory.size or new_y < 0 or new_y >= memory.size:
                logger.debug(f"Out of bounds: {new_x}, {new_y}")
                continue

            if (new_x, new_y) in visited:
                logger.debug(f"Visited: {new_x}, {new_y}")
                continue

            if memory.is_corrupted(new_x, new_y):
                logger.debug(f"Corrupted: {new_x}, {new_y}")
                continue

            visited.add((new_x, new_y))
            queue.append(((new_x, new_y), steps + 1))

    return -1


def djikstra_search(
    memory: Memory, start: tuple[int, int], end: tuple[int, int]
) -> tuple[int, list[tuple[int, int]]]:
    """
    Djikstra search algorithm to find the shortest path from start to end.
    Returns the number of steps and the path.
    """

    queue: list[tuple[tuple[int, int], int, list]] = [(start, 0, [])]
    visited = set([start])

    while queue:
        current, steps, path = queue.pop(0)

        if current == end:
            return steps, path

        x, y = current

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = x + dx, y + dy

            if new_x < 0 or new_x >= memory.size or new_y < 0 or new_y >= memory.size:
                continue

            if (new_x, new_y) in visited:
                continue

            if memory.is_corrupted(new_x, new_y):
                continue

            visited.add((new_x, new_y))
            queue.append(((new_x, new_y), steps + 1, path + [(new_x, new_y)]))

    return -1, []


def part_1(file_path: str) -> int:
    """
    Read the input file and return the solution.
    """

    memory = Memory.from_file(file_path)
    # limit the corrupted memory to 1024
    memory.corrupted = memory.corrupted[:1024]

    if os.environ.get("LOGURU_LEVEL") == "DEBUG":
        print(memory)
    step, _ = djikstra_search(memory, (0, 0), (memory.size - 1, memory.size - 1))
    return step


# --- Part Two ---


def part_2(file_path: str) -> int:
    """
    Read the input file and return the solution.
    """

    memory = Memory.from_file(file_path)

    full_corrupted = memory.corrupted.copy()

    # erase any corrupted memory that is on the path
    memory.corrupted = []

    _, starting_path = djikstra_search(
        memory, (0, 0), (memory.size - 1, memory.size - 1)
    )
    logger.debug(f"Starting path: {starting_path}")
    logger.debug(f"Found corrupted byte count: {full_corrupted}")

    if os.environ.get("LOGURU_LEVEL") == "DEBUG":
        print(memory.plot_path(starting_path))

    for i in tqdm(range(0, len(full_corrupted))):
        # if the corrupted byte falls on the path, we need to find a new path
        if full_corrupted[i] in starting_path:
            logger.debug(f"Corrupted byte found on path: {full_corrupted[i]}")

            # add the byte from 0 to i-th corrupted byte
            memory.corrupted = full_corrupted[: i + 1]

            if os.environ.get("LOGURU_LEVEL") == "DEBUG":
                print(memory.plot_path(starting_path))

            step, starting_path = djikstra_search(
                memory, (0, 0), (memory.size - 1, memory.size - 1)
            )

            if step == -1:
                return memory.corrupted[i]

    return -1
