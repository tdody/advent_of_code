# Path: 2025/src/day_6.py

"""
--- Day 6: Trash Compactor ---
After helping the Elves in the kitchen, you were taking a break and helping them re-enact a movie scene when you over-enthusiastically jumped into the garbage chute!

A brief fall later, you find yourself in a garbage smasher. Unfortunately, the door's been magnetically sealed.

As you try to find a way out, you are approached by a family of cephalopods! They're pretty sure they can get the door open, but it will take some time. While you wait, they're curious if you can help the youngest cephalopod with her math homework.

Cephalopod math doesn't look that different from normal math. The math worksheet (your puzzle input) consists of a list of problems; each problem has a group of numbers that need to be either added (+) or multiplied (*) together.

However, the problems are arranged a little strangely; they seem to be presented next to each other in a very long horizontal list. For example:

123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +
Each problem's numbers are arranged vertically; at the bottom of the problem is the symbol for the operation that needs to be performed. Problems are separated by a full column of only spaces. The left/right alignment of numbers within each problem can be ignored.

So, this worksheet contains four problems:

123 * 45 * 6 = 33210
328 + 64 + 98 = 490
51 * 387 * 215 = 4243455
64 + 23 + 314 = 401
To check their work, cephalopod students are given the grand total of adding together all of the answers to the individual problems. In this worksheet, the grand total is 33210 + 490 + 4243455 + 401 = 4277556.

Of course, the actual worksheet is much wider. You'll need to make sure to unroll it completely so that you can read the problems clearly.

Solve the problems on the math worksheet. What is the grand total found by adding together all of the answers to the individual problems?

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
The big cephalopods come back to check on how things are going. When they see that your grand total doesn't match the one expected by the worksheet, they realize they forgot to explain how to read cephalopod math.

Cephalopod math is written right-to-left in columns. Each number is given in its own column, with the most significant digit at the top and the least significant digit at the bottom. (Problems are still separated with a column consisting only of spaces, and the symbol at the bottom of the problem is still the operator to use.)

Here's the example worksheet again:

123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +
Reading the problems right-to-left one column at a time, the problems are now quite different:

The rightmost problem is 4 + 431 + 623 = 1058
The second problem from the right is 175 * 581 * 32 = 3253600
The third problem from the right is 8 + 248 + 369 = 625
Finally, the leftmost problem is 356 * 24 * 1 = 8544
Now, the grand total is 1058 + 3253600 + 625 + 8544 = 3263827.

Solve the problems on the math worksheet again. What is the grand total found by adding together all of the answers to the individual problems?

"""

from math import prod

from loguru import logger
import re


class MathGrid:
    grid: list[list[str]]
    operators: list[str]

    def __init__(self, grid: list[list[str]], operators: list[str]):
        self.grid = grid
        self.operators = operators

    @staticmethod
    def _get_spacings_from_operator_line(operator_line: str) -> list[int]:
        matches = re.findall(r"(\s+)", operator_line)
        lengths = [len(m) for m in matches]
        lengths[-1] += 1
        return lengths

    @classmethod
    def default_from_file(cls, file_path: str) -> "MathGrid":
        with open(file_path, "r") as file:
            lines = file.readlines()
            number_lines = lines[0:-1]
            operator_line = lines[-1]

            grid = []
            for line in number_lines:
                grid.append(line.strip().split())

            logger.debug(f"Grid: {grid}")
            return cls(
                grid,
                operator_line.strip().split(),
            )

    @classmethod
    def advanced_from_file(cls, file_path: str) -> "MathGrid":
        with open(file_path, "r") as file:
            lines = file.readlines()
            number_lines = lines[0:-1]
            operator_line = lines[-1]
            spacings = cls._get_spacings_from_operator_line(operator_line)
            logger.debug(f"Spacings: {spacings}")

            grid = []
            # read each chunk of n_characters (from spacings) and append to grid
            for line in number_lines:
                index = 0
                deciphered_line = []
                for spacing in spacings:
                    deciphered_line.append(line[index : index + spacing])
                    index += spacing + 1
                grid.append(deciphered_line)
            logger.debug(f"Grid: {grid}")
            return cls(grid, operator_line.strip().split())

    def solve_problem(self, n: int) -> int:
        """
        Solve the problem for the given number of operators.
        """
        operator = self.operators[n]
        numbers = [int(self.grid[i][n]) for i in range(len(self.grid))]
        if operator == "+":
            return sum(numbers)
        elif operator == "*":
            return prod(numbers)
        else:
            raise ValueError(f"Invalid operator: {operator}")

    def rearrange_problem(self, n: int) -> int:
        starting_numbers = [self.grid[i][n] for i in range(len(self.grid))]
        logger.debug(f"Starting numbers: {starting_numbers}")

        numbers = [number[::-1] for number in starting_numbers]

        max_number_len = max(len(number) for number in numbers)

        new_numbers = []
        for i in range(max_number_len):
            new_numbers.append(int("".join([number[i] for number in numbers])))

        return new_numbers

    def solve_advanced_problem(self, n: int) -> int:
        """
        Solve the advanced problem for the given number of operators.
        """
        numbers = self.rearrange_problem(n)
        operator = self.operators[n]
        logger.debug(
            f"Solving advanced problem for {n} with numbers {numbers} and operator {operator}"
        )
        if operator == "+":
            return sum(numbers)
        elif operator == "*":
            return prod(numbers)
        else:
            raise ValueError(f"Invalid operator: {operator}")

    def solve_grid(self) -> int:
        """
        Solve the grid.
        """
        return sum(self.solve_problem(i) for i in range(len(self.operators)))

    def solve_advanced_grid(self) -> int:
        """
        Solve the advanced grid.
        """
        return sum(self.solve_advanced_problem(i) for i in range(len(self.operators)))


# --- Part One ---


def part_1(file_path: str) -> int:
    """
    Read the input file and return the solution.
    """

    math_grid = MathGrid.default_from_file(file_path)
    return math_grid.solve_grid()


# --- Part Two ---


def part_2(file_path: str) -> int:
    """
    Read the input file and return the solution.
    """

    math_grid = MathGrid.advanced_from_file(file_path)
    return math_grid.solve_advanced_grid()
