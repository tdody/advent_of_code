# Path: 2015/src/day_1.py
"""
--- Day 1: Not Quite Lisp ---
Santa was hoping for a white Christmas, but his weather machine's "snow" function is powered by stars, and he's fresh out! To save Christmas, he needs you to collect fifty stars by December 25th.

Collect stars by helping Santa solve puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

Here's an easy puzzle to warm you up.

Santa is trying to deliver presents in a large apartment building, but he can't find the right floor - the directions he got are a little confusing. He starts on the ground floor (floor 0) and then follows the instructions one character at a time.

An opening parenthesis, (, means he should go up one floor, and a closing parenthesis, ), means he should go down one floor.

The apartment building is very tall, and the basement is very deep; he will never find the top or bottom floors.

For example:

(()) and ()() both result in floor 0.
((( and (()(()( both result in floor 3.
))((((( also results in floor 3.
()) and ))( both result in floor -1 (the first basement level).
))) and )())()) both result in floor -3.
To what floor do the instructions take Santa?


--- Part Two ---
Now, given the same instructions, find the position of the first character that causes him to enter the basement (floor -1). The first character in the instructions has position 1, the second character has position 2, and so on.

For example:

) causes him to enter the basement at character position 1.
()()) causes him to enter the basement at character position 5.
What is the position of the character that causes Santa to first enter the basement?


"""

# --- Part One ---


class Sequence:
    str_sequence: str

    def __init__(self, str_sequence: str):
        self.str_sequence = str_sequence

    @classmethod
    def from_file(cls, file_path: str) -> "Sequence":
        with open(file_path, "r") as file:
            return cls(file.read().strip())

    def count_characters(self) -> int:
        plusses = self.str_sequence.count("(")
        minuses = self.str_sequence.count(")")
        return plusses - minuses

    def find_basement_index(self) -> int:
        current_position = 0
        for index, character in enumerate(self.str_sequence):
            if character == "(":
                current_position += 1
            elif character == ")":
                current_position -= 1
            if current_position == -1:
                return index + 1
        return -1


def part_1(file_path: str) -> int:
    """
    Read the input file and return the solution.
    """

    sequence = Sequence.from_file(file_path)
    return sequence.count_characters()


# --- Part Two ---


def part_2(file_path: str) -> int:
    """
    Read the input file and return the solution.
    """

    sequence = Sequence.from_file(file_path)
    return sequence.find_basement_index()
