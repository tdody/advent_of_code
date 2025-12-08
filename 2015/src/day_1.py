# Path: 2015/src/day_1.py
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
