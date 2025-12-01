"""
Setup the day by creating the input file and the module file.

Example:
python setup_day.py --year 2024 --day 1
"""

import argparse
import os


def setup_day(year: int, day: int) -> None:
    """
    Setup the day by creating the input file and the module file.
    """
    year_str = str(year)
    day_str = str(day)
    module_file = f"{year_str}/src/day_{day_str}.py"
    input_file = f"{year_str}/inputs/day_{day_str}_input.txt"
    test_file = f"{year_str}/inputs/day_{day_str}_input_test.txt"

    if os.path.exists(module_file):
        print(f"Year {year}, day {day} already exists.")
        return

    # create the files
    with open(module_file, "w") as file:
        file.write(f"# Path: {year_str}/src/day_{day_str}.py\n")
        file.write("# --- Part One ---\n\n")
        file.write("def part_1(file_path: str) -> int:\n")
        file.write('    """\n')
        file.write("    Read the input file and return the solution.\n")
        file.write('    """\n\n')
        file.write("    return 0\n\n")
        file.write("# --- Part Two ---\n\n")
        file.write("def part_2(file_path: str) -> int:\n")
        file.write('    """\n')
        file.write("    Read the input file and return the solution.\n")
        file.write('    """\n\n')
        file.write("    return 0\n")

    with open(input_file, "w") as file:
        file.write("")

    with open(test_file, "w") as file:
        file.write("")

    print(f"Year {year}, day {day} created.")


if __name__ == "__main__":
    argsparse = argparse.ArgumentParser()
    argsparse.add_argument(
        "--year", type=int, help="The year of the challenge to setup.", required=True
    )
    argsparse.add_argument(
        "--day", type=int, help="The day of the challenge to setup.", required=True
    )
    year = argsparse.parse_args().year
    day = argsparse.parse_args().day
    setup_day(year, day)
