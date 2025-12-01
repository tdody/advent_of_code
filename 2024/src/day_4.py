"""
--- Day 4: Ceres Search ---
"Looks like the Chief's not here. Next!" One of The Historians pulls out a device and pushes the only button on it. After a brief flash, you recognize the interior of the Ceres monitoring station!

As the search for the Chief continues, a small Elf who lives on the station tugs on your shirt; she'd like to know if you could help her with her word search (your puzzle input). She only has to find one word: XMAS.

This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to find all of them. Here are a few ways XMAS might appear, where irrelevant characters have been replaced with .:


..X...
.SAMX.
.A..A.
XMAS.S
.X....
The actual word search will be full of letters instead. For example:

MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
In this word search, XMAS occurs a total of 18 times; here's the same word search again, but where letters not involved in any XMAS have been replaced with .:

....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX
Take a look at the little Elf's word search. How many times does XMAS appear?

--- Part Two ---
The Elf looks quizzically at you. Did you misunderstand the assignment?

Looking for the instructions, you flip over the word search to find that this isn't actually an XMAS puzzle; it's an X-MAS puzzle in which you're supposed to find two MAS in the shape of an X. One way to achieve that is like this:

M.S
.A.
M.S
Irrelevant characters have again been replaced with . in the above diagram. Within the X, each MAS can be written forwards or backwards.

Here's the same example from before, but this time all of the X-MASes have been kept instead:

.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........
In this example, an X-MAS appears 9 times.

Flip the word search from the instructions back over to the word search side and try again. How many times does an X-MAS appear?
"""


class LetterGrid:
    grid: list[list[str]]

    def __init__(self, grid: list[list[str]]):
        self.grid = grid

    @property
    def n_rows(self) -> int:
        return len(self.grid)

    @property
    def n_cols(self) -> int:
        return len(self.grid[0])

    def get_row(self, col: int) -> list[str]:
        return self.grid[col]

    def get_col(self, row: int) -> list[str]:
        return [self.grid[i][row] for i in range(self.n_rows)]

    def get_diagonal(self, row: int, col: int, right: bool) -> list[str]:
        if row >= self.n_rows or col >= self.n_cols:
            return []

        diagonal = []
        while row < self.n_rows and col < self.n_cols and row >= 0 and col >= 0:
            diagonal.append(self.grid[row][col])
            row += 1
            col += 1 if right else -1

        return diagonal

    def __str__(self) -> str:
        return "\n".join(["".join(row) for row in self.grid])

    def get_3_x_3(self, row: int, col: int) -> list[str]:
        if row + 2 >= self.n_rows or col + 2 >= self.n_cols:
            return []
        return [
            self.grid[row][col],
            self.grid[row][col + 2],
            self.grid[row + 1][col + 1],
            self.grid[row + 2][col],
            self.grid[row + 2][col + 2],
        ]

    @classmethod
    def from_str(cls, s: str) -> "LetterGrid":
        return cls([list(row.strip()) for row in s.strip().split("\n")])


def read_input(file_path: str) -> LetterGrid:
    with open(file_path, "r") as file:
        return LetterGrid([line.strip().split() for line in file.readlines()])


def find_xmas(grid: LetterGrid) -> int:
    xmas_count = 0

    # Find XMAS in rows
    for i in range(grid.n_rows):
        # left to right
        xmas_count += "".join(grid.get_row(i)).count("XMAS")
        # right to left
        xmas_count += "".join(grid.get_row(i)[::-1]).count("XMAS")

    # Find XMAS in columns
    for i in range(grid.n_cols):
        # top to bottom
        xmas_count += "".join(grid.get_col(i)).count("XMAS")
        # bottom to top
        xmas_count += "".join(grid.get_col(i)[::-1]).count("XMAS")

    # Find XMAS in diagonals

    # From lef to right
    for i in range(grid.n_rows):
        diagonal = grid.get_diagonal(i, 0, right=True)
        # top to bottom
        xmas_count += "".join(diagonal).count("XMAS")
        # bottom to top
        xmas_count += "".join(diagonal[::-1]).count("XMAS")

    # From top
    for i in range(1, grid.n_cols):
        diagonal = grid.get_diagonal(0, i, right=True)
        # left to right
        xmas_count += "".join(diagonal).count("XMAS")
        # right to left
        xmas_count += "".join(diagonal[::-1]).count("XMAS")

        # From right to left
        diagonal = grid.get_diagonal(0, i, right=False)
        # left to right
        xmas_count += "".join(diagonal).count("XMAS")
        # right to left
        xmas_count += "".join(diagonal[::-1]).count("XMAS")

    # From the right
    for i in range(1, grid.n_rows):
        diagonal = grid.get_diagonal(i, grid.n_cols - 1, right=False)
        # top to bottom
        xmas_count += "".join(diagonal).count("XMAS")
        # bottom to top
        xmas_count += "".join(diagonal[::-1]).count("XMAS")

    return xmas_count


def validate_3_x_3(grid: LetterGrid, row: int, col: int) -> bool:
    """
    0 . 1
    . 2 .
    3 . 4

    The grid is valid if the following conditions are met:
    - the ends of the diagonal aren't the same
    - 2 is "A"
    - 2 "M" and 2 "S"

    """
    if row + 2 >= grid.n_rows or col + 2 >= grid.n_cols:
        return False

    square = grid.get_3_x_3(row, col)

    if square[0] == square[4]:
        return False
    if square[2] != "A":
        return False
    if square[3] == square[1]:
        return False
    if square.count("M") != 2 or square.count("S") != 2:
        return False

    return True


def find_x_mas(grid: LetterGrid) -> int:
    x_mas_count = 0

    for i in range(grid.n_rows - 2):
        for j in range(grid.n_cols - 2):
            if validate_3_x_3(grid, i, j):
                x_mas_count += 1

    return x_mas_count


def part_1(file_path: str) -> int:
    grid = read_input(file_path)
    return find_xmas(grid)


def part_2(file_path: str) -> int:
    grid = read_input(file_path)
    return find_x_mas(grid)
