"""
--- Day 8: Resonant Collinearity ---
You find yourselves on the roof of a top-secret Easter Bunny installation.

While The Historians do their thing, you take a look at the familiar huge antenna. Much to your surprise, it seems to have been reconfigured to emit a signal that makes people 0.1% more likely to buy Easter Bunny brand Imitation Mediocre Chocolate as a Christmas gift! Unthinkable!

Scanning across the city, you find that there are actually many such antennas. Each antenna is tuned to a specific frequency indicated by a single lowercase letter, uppercase letter, or digit. You create a map (your puzzle input) of these antennas. For example:

............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
The signal only applies its nefarious effect at specific antinodes based on the resonant frequencies of the antennas. In particular, an antinode occurs at any point that is perfectly in line with two antennas of the same frequency - but only when one of the antennas is twice as far away as the other. This means that for any pair of antennas with the same frequency, there are two antinodes, one on either side of them.

So, for these two antennas with frequency a, they create the two antinodes marked with #:

..........
...#......
..........
....a.....
..........
.....a....
..........
......#...
..........
..........
Adding a third antenna with the same frequency creates several more antinodes. It would ideally add four antinodes, but two are off the right side of the map, so instead it adds only two:

..........
...#......
#.........
....a.....
........a.
.....a....
..#.......
......#...
..........
..........
Antennas with different frequencies don't create antinodes; A and a count as different frequencies. However, antinodes can occur at locations that contain antennas. In this diagram, the lone antenna with frequency capital A creates no antinodes but has a lowercase-a-frequency antinode at its location:

..........
...#......
#.........
....a.....
........a.
.....a....
..#.......
......A...
..........
..........
The first example has antennas with two different frequencies, so the antinodes they create look like this, plus an antinode overlapping the topmost A-frequency antenna:

......#....#
...#....0...
....#0....#.
..#....0....
....0....#..
.#....A.....
...#........
#......#....
........A...
.........A..
..........#.
..........#.
Because the topmost A-frequency antenna overlaps with a 0-frequency antinode, there are 14 total unique locations that contain an antinode within the bounds of the map.

Calculate the impact of the signal. How many unique locations within the bounds of the map contain an antinode?

--- Part Two ---
Watching over your shoulder as you work, one of The Historians asks if you took the effects of resonant harmonics into your calculations.

Whoops!

After updating your model, it turns out that an antinode occurs at any grid position exactly in line with at least two antennas of the same frequency, regardless of distance. This means that some of the new antinodes will occur at the position of each antenna (unless that antenna is the only one of its frequency).

So, these three T-frequency antennas now create many antinodes:

T....#....
...T......
.T....#...
.........#
..#.......
..........
...#......
..........
....#.....
..........
In fact, the three T-frequency antennas are all exactly in line with two antennas, so they are all also antinodes! This brings the total number of antinodes in the above example to 9.

The original example now has 34 antinodes, including the antinodes that appear on every antenna:

##....#....#
.#.#....0...
..#.#0....#.
..##...0....
....0....#..
.#...#A....#
...#..#.....
#....#.#....
..#.....A...
....#....A..
.#........#.
...#......##
Calculate the impact of the signal using this updated model. How many unique locations within the bounds of the map contain an antinode?
"""

# Path: src/day_8.py
# --- Part One ---


class Position:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


class Antenna:
    frequency: str
    position: Position

    def __init__(self, frequency: str, position: Position):
        self.frequency = frequency
        self.position = position

    def is_out_of_bounds(
        self, dx: int, dy: int, grid: list[list[str]], factor: int = 1
    ) -> bool:
        return (
            self.position.x + dx * factor < 0
            or self.position.x + dx * factor >= len(grid[0])
            or self.position.y + dy * factor < 0
            or self.position.y + dy * factor >= len(grid)
        )


class Grid:
    antennas: list[Antenna]
    grid: list[list[str]]

    def __init__(self, antennas: list[Antenna], grid: list[list[str]]):
        self.antennas = antennas
        self.grid = grid

    def __plot(self, antinodes: set[Position]):
        plot_grid = [list(row) for row in self.grid]

        for antinode in antinodes:
            plot_grid[antinode.y][antinode.x] = "#"

        for antenna in self.antennas:
            plot_grid[antenna.position.y][antenna.position.x] = antenna.frequency

        for row in plot_grid:
            print("".join(row))

    def get_antinodes(self) -> set[Position]:
        antinodes = set()

        for i in range(len(self.antennas)):
            for j in range(i + 1, len(self.antennas)):
                antinodes.update(
                    self.get_antinodes_between(self.antennas[i], self.antennas[j])
                )

        self.__plot(antinodes)
        return antinodes

    def get_antinodes_with_resonant_harmonics(self) -> set[Position]:
        antinodes = set()

        for i in range(len(self.antennas)):
            for j in range(i + 1, len(self.antennas)):
                antinodes.update(
                    self.get_antinodes_between_with_resonant_harmonics(
                        self.antennas[i], self.antennas[j]
                    )
                )

        self.__plot(antinodes)
        return antinodes

    def get_antinodes_between_with_resonant_harmonics(
        self, antenna_1: Antenna, antenna_2: Antenna
    ) -> set[Position]:
        antinodes: set[Position] = set()

        if antenna_1.frequency == antenna_2.frequency:
            x1 = antenna_1.position.x
            y1 = antenna_1.position.y
            x2 = antenna_2.position.x
            y2 = antenna_2.position.y

            antinodes.add(antenna_1.position)
            antinodes.add(antenna_2.position)

            # compute the difference between the x and y coordinates
            # the diff is the delta from antenna_1 to antenna_2
            x_diff = x2 - x1
            y_diff = y2 - y1

            # for each antenna decide if the delta needs to be added or subtracted
            factor: int = 1
            stop: bool = False

            while not stop:
                stop_1 = antenna_1.is_out_of_bounds(
                    x_diff, y_diff, self.grid, factor=factor
                )
                stop_2 = antenna_1.is_out_of_bounds(
                    x_diff, y_diff, self.grid, factor=-factor
                )

                if stop_1 and stop_2:
                    stop = True
                    break

                # check if the new position is within the grid
                if not antenna_1.is_out_of_bounds(
                    x_diff, y_diff, self.grid, factor=factor
                ):
                    antinodes.add(Position(x1 + x_diff * factor, y1 + y_diff * factor))
                if not antenna_1.is_out_of_bounds(
                    x_diff, y_diff, self.grid, factor=-factor
                ):
                    antinodes.add(Position(x1 - x_diff * factor, y1 - y_diff * factor))

                factor += 1

        return antinodes

    def get_antinodes_between(
        self,
        antenna_1: Antenna,
        antenna_2: Antenna,
    ) -> set[Position]:
        antinodes: set[Position] = set()

        if antenna_1.frequency == antenna_2.frequency:
            x1 = antenna_1.position.x
            y1 = antenna_1.position.y
            x2 = antenna_2.position.x
            y2 = antenna_2.position.y

            # compute the difference between the x and y coordinates
            # the diff is the delta from antenna_1 to antenna_2
            x_diff = x2 - x1
            y_diff = y2 - y1

            # for each antenna decide if the delta needs to be added or subtracted
            for i in [-1, 2]:
                # check if the new position is within the grid
                if not antenna_1.is_out_of_bounds(x_diff, y_diff, self.grid, factor=i):
                    antinodes.add(Position(x1 + x_diff * i, y1 + y_diff * i))

        return antinodes

    @classmethod
    def from_file(cls, file_path: str):
        antennas = []
        with open(file_path, "r") as file:
            grid = [[char for char in line.strip()] for line in file]
            for y in range(len(grid)):
                for x in range(len(grid[y])):
                    char = grid[y][x]
                    if char != ".":
                        antennas.append(Antenna(char, Position(x, y)))

        return cls(antennas, grid)


def part_1(file_path: str) -> int:
    """
    Read the input file and return the solution.
    """

    grid = Grid.from_file(file_path)
    antinodes = grid.get_antinodes()

    return len(antinodes)


# --- Part Two ---


def part_2(file_path: str) -> int:
    """
    Read the input file and return the solution.
    """

    grid = Grid.from_file(file_path)
    antinodes = grid.get_antinodes_with_resonant_harmonics()

    return len(antinodes)
