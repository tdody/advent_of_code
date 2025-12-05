# Path: 2025/src/day_4.py

"""
--- Day 4: Printing Department ---
You ride the escalator down to the printing department. They're clearly getting ready for Christmas; they have lots of large rolls of paper everywhere, and there's even a massive printer in the corner (to handle the really big print jobs).

Decorating here will be easy: they can make their own decorations. What you really need is a way to get further into the North Pole base while the elevators are offline.

"Actually, maybe we can help with that," one of the Elves replies when you ask for help. "We're pretty sure there's a cafeteria on the other side of the back wall. If we could break through the wall, you'd be able to keep moving. It's too bad all of our forklifts are so busy moving those big rolls of paper around."

If you can optimize the work the forklifts are doing, maybe they would have time to spare to break through the wall.

The rolls of paper (@) are arranged on a large grid; the Elves even have a helpful diagram (your puzzle input) indicating where everything is located.

For example:

..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
The forklifts can only access a roll of paper if there are fewer than four rolls of paper in the eight adjacent positions. If you can figure out which rolls of paper the forklifts can access, they'll spend less time looking and more time breaking down the wall to the cafeteria.

In this example, there are 13 rolls of paper that can be accessed by a forklift (marked with x):

..xx.xx@x.
x@@.@.@.@@
@@@@@.x.@@
@.@@@@..@.
x@.@@@@.@x
.@@@@@@@.@
.@.@.@.@@@
x.@@@.@@@@
.@@@@@@@@.
x.x.@@@.x.
Consider your complete diagram of the paper roll locations. How many rolls of paper can be accessed by a forklift?

--- Part Two ---
Now, the Elves just need help accessing as much of the paper as they can.

Once a roll of paper can be accessed by a forklift, it can be removed. Once a roll of paper is removed, the forklifts might be able to access more rolls of paper, which they might also be able to remove. How many total rolls of paper could the Elves remove if they keep repeating this process?

Starting with the same example as above, here is one way you could remove as many rolls of paper as possible, using highlighted @ to indicate that a roll of paper is about to be removed, and using x to indicate that a roll of paper was just removed:

Initial state:
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.

Remove 13 rolls of paper:
..xx.xx@x.
x@@.@.@.@@
@@@@@.x.@@
@.@@@@..@.
x@.@@@@.@x
.@@@@@@@.@
.@.@.@.@@@
x.@@@.@@@@
.@@@@@@@@.
x.x.@@@.x.

Remove 12 rolls of paper:
.......x..
.@@.x.x.@x
x@@@@...@@
x.@@@@..x.
.@.@@@@.x.
.x@@@@@@.x
.x.@.@.@@@
..@@@.@@@@
.x@@@@@@@.
....@@@...

Remove 7 rolls of paper:
..........
.x@.....x.
.@@@@...xx
..@@@@....
.x.@@@@...
..@@@@@@..
...@.@.@@x
..@@@.@@@@
..x@@@@@@.
....@@@...

Remove 5 rolls of paper:
..........
..x.......
.x@@@.....
..@@@@....
...@@@@...
..x@@@@@..
...@.@.@@.
..x@@.@@@x
...@@@@@@.
....@@@...

Remove 2 rolls of paper:
..........
..........
..x@@.....
..@@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@x.
....@@@...

Remove 1 roll of paper:
..........
..........
...@@.....
..x@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...

Remove 1 roll of paper:
..........
..........
...x@.....
...@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...

Remove 1 roll of paper:
..........
..........
....x.....
...@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...

Remove 1 roll of paper:
..........
..........
..........
...x@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...
Stop once no more rolls of paper are accessible by a forklift. In this example, a total of 43 rolls of paper can be removed.

Start with your original diagram. How many rolls of paper in total can be removed by the Elves and their forklifts?
"""

from typing import Optional

PAPER = "@"


class PaperGrid:
    grid: list[list[str]]
    papers: list[tuple[int, int]]

    def __init__(self, grid: list[list[str]]):
        self.grid = grid
        self.papers = []
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if self.is_paper(row, col):
                    self.papers.append((row, col))

    def __str__(self) -> str:
        return "\n".join(["".join(row) for row in self.grid])

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def from_file(cls, file_path: str) -> "PaperGrid":
        with open(file_path, "r") as file:
            return cls([list(line.strip()) for line in file.readlines()])

    def get_cell(self, row: int, col: int) -> Optional[str]:
        if row < 0 or row >= len(self.grid) or col < 0 or col >= len(self.grid[0]):
            return None
        return self.grid[row][col]

    def is_paper(self, row: int, col: int) -> bool:
        return self.get_cell(row, col) == PAPER

    def get_adjacent_values(self, row: int, col: int) -> list[str]:
        adjacent_cells = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if self.get_cell(row + i, col + j) is not None:
                    adjacent_cells.append(self.get_cell(row + i, col + j))
        return adjacent_cells

    def is_accessible(self, row: int, col: int, threshold: int) -> bool:
        adjacent_papers = [
            value for value in self.get_adjacent_values(row, col) if value == PAPER
        ]
        return len(adjacent_papers) < threshold

    def remove_paper(self, row: int, col: int) -> None:
        self.grid[row][col] = "."
        self.papers.remove((row, col))


def read_input(file_path: str) -> PaperGrid:
    with open(file_path, "r") as file:
        return PaperGrid([list(line.strip()) for line in file.readlines()])


def part_1(file_path: str) -> int:
    """
    Read the input file and return the solution.
    """

    threshold = 4
    grid = read_input(file_path)
    accessible_cells = 0

    for paper in grid.papers:
        if grid.is_accessible(paper[0], paper[1], threshold):
            accessible_cells += 1
    return accessible_cells


# --- Part Two ---


def part_2(file_path: str) -> int:
    """
    Read the input file and return the solution.
    """
    threshold = 4
    grid: PaperGrid = read_input(file_path)
    removed_papers = 0

    while True:
        accessible_papers = []
        for paper in grid.papers:
            if grid.is_accessible(paper[0], paper[1], threshold):
                accessible_papers.append(paper)
                removed_papers += 1
        if len(accessible_papers) == 0:
            break
        for paper in accessible_papers:
            grid.remove_paper(paper[0], paper[1])
    return removed_papers
