"""
Main module for Advent of Code
"""

import argparse
import importlib
import os
import sys
from typing import Callable

from loguru import logger


def run_day(year_index: int, day_index: int, part: int) -> Callable:
    """'
    Programmatically run the challenge for the given year, day and part.
    """

    # check that the module exists
    if not os.path.exists(f"{year_index}/src/day_{day_index}.py"):
        raise ValueError(f"Year {year_index}, day {day_index} module not found.")

    module = importlib.import_module(f"{year_index}.src.day_{day_index}")
    if part == 1:
        return module.part_1
    elif part == 2:
        return module.part_2
    else:
        raise ValueError("Invalid part selected.")


def main():
    """Main entry point for the aoc script."""
    argsparse = argparse.ArgumentParser()
    argsparse.add_argument(
        "--year", type=int, help="The year of the challenge to run.", required=True
    )
    argsparse.add_argument(
        "--day", type=int, help="The day of the challenge to run.", required=True
    )
    argsparse.add_argument(
        "--test",
        help="Run the test cases for the challenge.",
        action="store_true",
    )
    argsparse.add_argument(
        "--part", type=int, help="The part of the challenge to run.", required=True
    )
    argsparse.add_argument(
        "--debug",
        help="Enable debug logging with loguru.",
        action="store_true",
    )

    args = argsparse.parse_args()
    year = args.year
    day = args.day
    part = args.part
    test = args.test
    debug = args.debug

    # Configure loguru logger based on debug flag
    logger.remove()  # Remove default handler
    if debug:
        logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level="DEBUG",
            colorize=True,
        )
        logger.debug(f"Debug mode enabled. Running year {year}, day {day}, part {part}")
    # When debug is False, no handler is added, so logs are suppressed

    file_path = f"{year}/inputs/day_{day}_input" + ("_test" if test else "") + ".txt"

    if not os.path.exists(file_path):
        raise ValueError(f"File not found: {file_path}")

    logger.debug(f"Input file: {file_path}")
    result = run_day(year, day, part)(file_path)
    logger.debug(f"Result: {result}")
    print(result)


if __name__ == "__main__":
    main()
