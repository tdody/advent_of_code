"""
--- Day 13: Claw Contraption ---
Next up: the lobby of a resort on a tropical island. The Historians take a moment to admire the hexagonal floor tiles before spreading out.

Fortunately, it looks like the resort has a new arcade! Maybe you can win some prizes from the claw machines?

The claw machines here are a little unusual. Instead of a joystick or directional buttons to control the claw, these machines have two buttons labeled A and B. Worse, you can't just put in a token and play; it costs 3 tokens to push the A button and 1 token to push the B button.

With a little experimentation, you figure out that each machine's buttons are configured to move the claw a specific amount to the right (along the X axis) and a specific amount forward (along the Y axis) each time that button is pressed.

Each machine contains one prize; to win the prize, the claw must be positioned exactly above the prize on both the X and Y axes.

You wonder: what is the smallest number of tokens you would have to spend to win as many prizes as possible? You assemble a list of every machine's button behavior and prize location (your puzzle input). For example:

Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
This list describes the button configuration and prize location of four different claw machines.

For now, consider just the first claw machine in the list:

Pushing the machine's A button would move the claw 94 units along the X axis and 34 units along the Y axis.
Pushing the B button would move the claw 22 units along the X axis and 67 units along the Y axis.
The prize is located at X=8400, Y=5400; this means that from the claw's initial position, it would need to move exactly 8400 units along the X axis and exactly 5400 units along the Y axis to be perfectly aligned with the prize in this machine.
The cheapest way to win the prize is by pushing the A button 80 times and the B button 40 times. This would line up the claw along the X axis (because 80*94 + 40*22 = 8400) and along the Y axis (because 80*34 + 40*67 = 5400). Doing this would cost 80*3 tokens for the A presses and 40*1 for the B presses, a total of 280 tokens.

For the second and fourth claw machines, there is no combination of A and B presses that will ever win a prize.

For the third claw machine, the cheapest way to win the prize is by pushing the A button 38 times and the B button 86 times. Doing this would cost a total of 200 tokens.

So, the most prizes you could possibly win is two; the minimum tokens you would have to spend to win all (two) prizes is 480.

You estimate that each button would need to be pressed no more than 100 times to win a prize. How else would someone be expected to play?

Figure out how to win as many prizes as possible. What is the fewest tokens you would have to spend to win all possible prizes?

--- Part Two ---
As you go to win the first prize, you discover that the claw is nowhere near where you expected it would be. Due to a unit conversion error in your measurements, the position of every prize is actually 10000000000000 higher on both the X and Y axis!

Add 10000000000000 to the X and Y position of every prize. After making this change, the example above would now look like this:

Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=10000000008400, Y=10000000005400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=10000000012748, Y=10000000012176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=10000000007870, Y=10000000006450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=10000000018641, Y=10000000010279
Now, it is only possible to win a prize on the second and fourth claw machines. Unfortunately, it will take many more than 100 presses to do so.

Using the corrected prize coordinates, figure out how to win as many prizes as possible. What is the fewest tokens you would have to spend to win all possible prizes?


"""

import re
from typing import Optional

import numpy as np
from loguru import logger

# Path: src/day_13.py
# --- Part One ---


def parse_line(line: str) -> tuple[int, int]:
    """
    Parse a line of the input file.

    >>> parse_line("Button A: X+49, Y+95")
    (49, 95)

    >>> parse_line("Prize: X=3738, Y=5486")
    (3738, 5486)
    """
    # use re.findall to get the numbers
    x, y = map(int, re.findall(r"\d+", line))
    return x, y


class Clamp:
    movements: np.ndarray
    prize: np.ndarray

    def __init__(self, movements: np.ndarray, prize: np.ndarray):
        self.movements = movements
        self.prize = prize

    @classmethod
    def from_string(cls, strings: list[str]):
        """
        Input:
        Button A: X+49, Y+95
        Button B: X+28, Y+16
        Prize: X=3738, Y=5486

        Becomes:
        movements = np.ndarray([49, 28, 95, 16])
        prize = np.ndarray([3738, 5486])
        """
        button_a_x, button_a_y = parse_line(strings[0])
        button_b_x, button_b_y = parse_line(strings[1])
        prize_x, prize_y = parse_line(strings[2])

        movements = np.array([[button_a_x, button_b_x], [button_a_y, button_b_y]])
        prize = np.array([prize_x, prize_y]).reshape(-1, 1)

        logger.debug(f"movements:\n{movements}")
        logger.debug(f"prize:\n{prize}")

        return cls(movements, prize)

    def get_to_prize(self) -> Optional[tuple[int, int]]:
        """
        Problem: A.X = B
        Solution: X =A^-1 * B where A^-1 is the inverse of A
        """

        # Get the movements
        ax, bx = self.movements[0]
        ay, by = self.movements[1]

        # Get the prize
        px, py = self.prize

        # Calculate A presses via elimination
        a_presses, remainder = divmod(px * by - py * bx, ax * by - ay * bx)
        # If A presses isn't an integer, there is no integer solution
        if remainder:
            return None

        # Calculate B presses with X equation
        b_presses, remainder = divmod(px - ax * a_presses, bx)
        # If B presses isn't an integer, there is no integer solution
        if remainder:
            return None

        # Sanity check
        assert ax * a_presses + bx * b_presses == px
        assert ay * a_presses + by * b_presses == py
        # We've found an integer solution
        return (a_presses, b_presses)

    def get_cost(self) -> int:
        """
        Get the cost of the prize
        """

        n_moves = self.get_to_prize()

        if n_moves is None:
            logger.debug("No solution")
            return 0

        cost = 3 * n_moves[0] + n_moves[1]
        logger.debug(f"cost: {cost}")

        return cost


def part_1(file_path: str) -> int:
    """
    Read the input file and return the solution.
    """

    with open(file_path) as file:
        lines = file.read().splitlines()

    # Parse the input file
    clamps = [Clamp.from_string(lines[i : i + 3]) for i in range(0, len(lines), 4)]

    # Get the cost of each prize
    costs = [clamp.get_cost() for clamp in clamps]

    return sum(costs)


# --- Part Two ---


def part_2(file_path: str) -> int:
    """
    Read the input file and return the solution.
    """

    EXTRA = 10000000000000

    with open(file_path) as file:
        lines = file.read().splitlines()

    # Parse the input file
    clamps = [Clamp.from_string(lines[i : i + 3]) for i in range(0, len(lines), 4)]

    # Add the extra to the prize
    for clamp in clamps:
        clamp.prize += EXTRA

    # Get the cost of each prize
    costs = [clamp.get_cost() for clamp in clamps]

    return sum(costs)
