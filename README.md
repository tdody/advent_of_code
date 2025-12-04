# Advent of Code Solutions

![Advent of Code](https://github.com/tdody/advent_of_code_2024/blob/master/images/Banner.pnd?raw=true)

This repository contains my solutions to [Advent of Code](https://adventofcode.com/) challenges, organized by year.

## Project Structure

```
advent_of_code/
├── 2024/          # Solutions for Advent of Code 2024
│   ├── src/       # Solution files (day_1.py, day_2.py, ...)
│   └── inputs/    # Input files for each day
├── 2025/          # Solutions for Advent of Code 2025
│   ├── src/       # Solution files
│   └── inputs/    # Input files
├── aoc.py         # Main CLI script to run solutions
├── setup_day.py   # Script to scaffold a new day
└── pyproject.toml # Project dependencies and configuration
```

## Setup

This project uses [PDM](https://pdm-project.org/) for dependency management.

1. Install PDM (if not already installed):
   ```bash
   pip install pdm
   ```

2. Install project dependencies:
   ```bash
   pdm install
   ```

## Usage

### Running a Solution

Use the `aoc` command to run solutions:

```bash
pdm run aoc --year <YEAR> --day <DAY> --part <PART> [--test] [--debug]
```

**Arguments:**

- `--year`: The year of the challenge (e.g., 2024, 2025)
- `--day`: The day number (1-25)
- `--part`: The part number (1 or 2)
- `--test`: (Optional) Run with test input instead of the full input
- `--debug`: (Optional) Enable debug logging

**Examples:**

```bash
# Run part 1 of day 1 for 2025
pdm run aoc --year 2025 --day 1 --part 1

# Run part 2 with test input
pdm run aoc --year 2025 --day 1 --part 2 --test

# Run with debug logging
pdm run aoc --year 2025 --day 1 --part 1 --debug
```

### Setting Up a New Day

Use the `setup_day.py` script to scaffold a new day:

```bash
pdm run python setup_day.py --year <YEAR> --day <DAY>
```

This will create:

- A solution template file at `<YEAR>/src/day_<DAY>.py`
- An empty input file at `<YEAR>/inputs/day_<DAY>_input.txt`
- An empty test input file at `<YEAR>/inputs/day_<DAY>_input_test.txt`

**Example:**

```bash
pdm run python setup_day.py --year 2025 --day 4
```

## License

MIT
