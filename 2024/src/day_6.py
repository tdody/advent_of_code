"""
--- Day 6: Guard Gallivant ---
The Historians use their fancy device again, this time to whisk you all away to the North Pole prototype suit manufacturing lab... in the year 1518! It turns out that having direct access to history is very convenient for a group of historians.

You still have to be careful of time paradoxes, and so it will be important to avoid anyone from 1518 while The Historians search for the Chief. Unfortunately, a single guard is patrolling this part of the lab.

Maybe you can work out where the guard will go ahead of time so that The Historians can search safely?

You start by making a map (your puzzle input) of the situation. For example:

....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
The map shows the current position of the guard with ^ (to indicate the guard is currently facing up from the perspective of the map). Any obstructions - crates, desks, alchemical reactors, etc. - are shown as #.

Lab guards in 1518 follow a very strict patrol protocol which involves repeatedly following these steps:

If there is something directly in front of you, turn right 90 degrees.
Otherwise, take a step forward.
Following the above protocol, the guard moves up several times until she reaches an obstacle (in this case, a pile of failed suit prototypes):

....#.....
....^....#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...
Because there is now an obstacle in front of the guard, she turns right before continuing straight in her new facing direction:

....#.....
........>#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...
Reaching another obstacle (a spool of several very long polymers), she turns right again and continues downward:

....#.....
.........#
..........
..#.......
.......#..
..........
.#......v.
........#.
#.........
......#...
This process continues for a while, but the guard eventually leaves the mapped area (after walking past a tank of universal solvent):

....#.....
.........#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#v..
By predicting the guard's route, you can determine which specific positions in the lab will be in the patrol path. Including the guard's starting position, the positions visited by the guard before leaving the area are marked with an X:

....#.....
....XXXXX#
....X...X.
..#.X...X.
..XXXXX#X.
..X.X.X.X.
.#XXXXXXX.
.XXXXXXX#.
#XXXXXXX..
......#X..
In this example, the guard will visit 41 distinct positions on your map.

Predict the path of the guard. How many distinct positions will the guard visit before leaving the mapped area?

--- Part Two ---
While The Historians begin working around the guard's patrol route, you borrow their fancy device and step outside the lab. From the safety of a supply closet, you time travel through the last few months and record the nightly status of the lab's guard post on the walls of the closet.

Returning after what seems like only a few seconds to The Historians, they explain that the guard's patrol area is simply too large for them to safely search the lab without getting caught.

Fortunately, they are pretty sure that adding a single new obstruction won't cause a time paradox. They'd like to place the new obstruction in such a way that the guard will get stuck in a loop, making the rest of the lab safe to search.

To have the lowest chance of creating a time paradox, The Historians would like to know all of the possible positions for such an obstruction. The new obstruction can't be placed at the guard's starting position - the guard is there right now and would notice.

In the above example, there are only 6 different positions where a new obstruction would cause the guard to get stuck in a loop. The diagrams of these six situations use O to mark the new obstruction, | to show a position where the guard moves up/down, - to show a position where the guard moves left/right, and + to show a position where the guard moves both up/down and left/right.

Option one, put a printing press next to the guard's starting position:

....#.....
....+---+#
....|...|.
..#.|...|.
....|..#|.
....|...|.
.#.O^---+.
........#.
#.........
......#...
Option two, put a stack of failed suit prototypes in the bottom right quadrant of the mapped area:


....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
......O.#.
#.........
......#...
Option three, put a crate of chimney-squeeze prototype fabric next to the standing desk in the bottom right quadrant:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----+O#.
#+----+...
......#...
Option four, put an alchemical retroencabulator near the bottom left corner:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
..|...|.#.
#O+---+...
......#...
Option five, put the alchemical retroencabulator a bit to the right instead:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
....|.|.#.
#..O+-+...
......#...
Option six, put a tank of sovereign glue right next to the tank of universal solvent:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----++#.
#+----++..
......#O..
It doesn't really matter what you choose to use as an obstacle so long as you and The Historians can put it into position without the guard noticing. The important thing is having enough options that you can find one that minimizes time paradoxes, and in this example, there are 6 different positions you could choose.

You need to get the guard stuck in a loop by adding a single new obstruction. How many different positions could you choose for this obstruction?
"""

from loguru import logger


class Direction:
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"

    @classmethod
    def get_direction(cls, direction: str):
        if direction == cls.UP:
            return cls.UP
        elif direction == cls.DOWN:
            return cls.DOWN
        elif direction == cls.LEFT:
            return cls.LEFT
        elif direction == cls.RIGHT:
            return cls.RIGHT
        else:
            raise ValueError("Invalid direction.")


class Position:
    row: int
    col: int

    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    def __str__(self):
        return f"Position: {self.row}, {self.col}"

    def __eq__(self, other: object):
        if not isinstance(other, Position):
            return NotImplemented
        return self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self.row, self.col))


class Obstacle(Position):
    def __init__(self, row: int, col: int):
        super().__init__(row, col)


class Guard:
    position: Position
    direction: Direction
    turns: list[Position]

    def __init__(self, position: Position, direction: str):
        self.position = position
        self.direction = Direction.get_direction(direction)
        self.turns = []

    def rotate_right(self) -> None:
        self.turns.append(self.position)
        if self.direction == Direction.UP:
            self.direction = Direction.get_direction("RIGHT")
        elif self.direction == Direction.RIGHT:
            self.direction = Direction.get_direction("DOWN")
        elif self.direction == Direction.DOWN:
            self.direction = Direction.get_direction("LEFT")
        elif self.direction == Direction.LEFT:
            self.direction = Direction.get_direction("UP")

    def get_immediate_next_position(self) -> Position:
        if self.direction == Direction.UP:
            return Position(self.position.row - 1, self.position.col)
        elif self.direction == Direction.DOWN:
            return Position(self.position.row + 1, self.position.col)
        elif self.direction == Direction.LEFT:
            return Position(self.position.row, self.position.col - 1)
        elif self.direction == Direction.RIGHT:
            return Position(self.position.row, self.position.col + 1)
        else:
            raise ValueError("Invalid direction.")

    def get_next_position(self, grid: "Grid") -> Position:
        # determine if an obstacle is located on the path
        # else return the position on the edge of the grid

        if self.direction == Direction.UP:
            lower_bound = 0
            blocked = False
            for obstacle in grid.obstacles:
                if (
                    obstacle.row < self.position.row
                    and obstacle.col == self.position.col
                ):
                    if obstacle.row >= lower_bound:
                        lower_bound = obstacle.row
                        blocked = True

            if blocked:
                # Add the visited positions
                grid.visited_positions = grid.visited_positions.union(
                    set(
                        [
                            Position(c, self.position.col)
                            for c in range(lower_bound + 1, self.position.row)
                        ]
                    )
                )

                return Position(lower_bound + 1, self.position.col)
            else:
                # add the visited positions
                grid.visited_positions = grid.visited_positions.union(
                    set(
                        [
                            Position(c, self.position.col)
                            for c in range(self.position.row)
                        ]
                    )
                )

                return Position(0, self.position.col)

        elif self.direction == Direction.DOWN:
            upper_bound = grid.n_rows
            blocked = False
            for obstacle in grid.obstacles:
                if (
                    obstacle.row > self.position.row
                    and obstacle.col == self.position.col
                ):
                    if obstacle.row <= upper_bound:
                        upper_bound = obstacle.row
                        blocked = True
            if blocked:
                # Add the visited positions
                grid.visited_positions = grid.visited_positions.union(
                    set(
                        [
                            Position(c, self.position.col)
                            for c in range(self.position.row + 1, upper_bound)
                        ]
                    )
                )

                return Position(upper_bound - 1, self.position.col)

            # add the visited positions
            grid.visited_positions = grid.visited_positions.union(
                set(
                    [
                        Position(c, self.position.col)
                        for c in range(self.position.row + 1, grid.n_rows)
                    ]
                )
            )

            return Position(grid.n_rows - 1, self.position.col)

        elif self.direction == Direction.LEFT:
            lower_bound = 0
            blocked = False
            for obstacle in grid.obstacles:
                if (
                    obstacle.row == self.position.row
                    and obstacle.col < self.position.col
                ):
                    if obstacle.col >= lower_bound:
                        lower_bound = obstacle.col
                        blocked = True
            if blocked:
                # Add the visited positions
                grid.visited_positions = grid.visited_positions.union(
                    set(
                        [
                            Position(self.position.row, c)
                            for c in range(lower_bound + 1, self.position.col)
                        ]
                    )
                )

                return Position(self.position.row, lower_bound + 1)

            # add the visited positions
            grid.visited_positions = grid.visited_positions.union(
                set([Position(self.position.row, c) for c in range(self.position.col)])
            )

            return Position(self.position.row, 0)

        elif self.direction == Direction.RIGHT:
            upper_bound = grid.n_cols
            blocked = False
            for obstacle in grid.obstacles:
                if (
                    obstacle.row == self.position.row
                    and obstacle.col > self.position.col
                ):
                    if obstacle.col <= upper_bound:
                        upper_bound = obstacle.col
                        blocked = True
            if blocked:
                # Add the visited positions
                grid.visited_positions = grid.visited_positions.union(
                    set(
                        [
                            Position(self.position.row, c)
                            for c in range(self.position.col + 1, upper_bound)
                        ]
                    )
                )

                return Position(self.position.row, upper_bound - 1)

            # add the visited positions
            grid.visited_positions = grid.visited_positions.union(
                set(
                    [
                        Position(self.position.row, c)
                        for c in range(self.position.col + 1, grid.n_cols)
                    ]
                )
            )

            return Position(self.position.row, grid.n_cols - 1)

        else:
            raise ValueError("Invalid direction.")

    def is_out(self, grid: "Grid") -> bool:
        """
        Check if the guard is out of the grid.
        """
        next_position = self.get_immediate_next_position()
        return (
            next_position.row < 0
            or next_position.row >= grid.n_rows
            or next_position.col < 0
            or next_position.col >= grid.n_cols
        )

    def is_blocked(self, obstacles: list[Obstacle]) -> bool:
        """
        Check if the guard is blocked by an obstacle.
        We check if the next position is an obstacle.
        """
        next_position = self.get_immediate_next_position()

        for obstacle in obstacles:
            if next_position == obstacle:
                return True

        return False

    def has_loop(self):
        """
        Check that any sequence of 4 consecutive turns repeats itself.
        """
        if len(self.turns) < 5:
            return False

        for i in range(len(self.turns) - 4):
            for j in range(i + 1, len(self.turns) - 3):
                if (
                    self.turns[i] == self.turns[j]
                    and self.turns[i + 1] == self.turns[j + 1]
                    and self.turns[i + 2] == self.turns[j + 2]
                    and self.turns[i + 3] == self.turns[j + 3]
                ):
                    return True


class Grid:
    grid: list[list[str]]
    guard: Guard
    obstacles: list[Obstacle]
    visited_positions: set[Position]
    turns: list[Position]

    def __init__(
        self,
        grid: list[list[str]],
        guard: Guard,
        obstacles: list[Obstacle],
        visited_positions: set[Position],
        turns: list[Position] = [],
    ):
        self.grid = grid
        self.guard = guard
        self.obstacles = obstacles
        self.visited_positions = visited_positions
        self.turns = turns

    @property
    def n_rows(self) -> int:
        return len(self.grid)

    @property
    def n_cols(self) -> int:
        return len(self.grid[0])

    @property
    def n_visited_positions(self) -> int:
        return len(self.visited_positions)

    @classmethod
    def from_str(cls, str_grid: list[list[str]]):
        guard = None
        obstacles = []

        for row, line in enumerate(str_grid):
            for col, char in enumerate(line):
                if char in [
                    Direction.UP,
                    Direction.DOWN,
                    Direction.LEFT,
                    Direction.RIGHT,
                ]:
                    guard = Guard(Position(row, col), char)
                elif char == "#":
                    obstacles.append(Obstacle(row, col))

        assert guard is not None, "Guard not found."
        assert len(obstacles) > 0, "No obstacles found."

        return cls(str_grid, guard, obstacles, visited_positions={guard.position})

    def plot_map(self, with_added_obstacle: bool = False):
        updated_grid = [["." for _ in range(self.n_cols)] for _ in range(self.n_rows)]

        # Add visited positions
        for position in self.visited_positions:
            updated_grid[position.row][position.col] = "X"

        # Add guard position
        updated_grid[self.guard.position.row][self.guard.position.col] = str(
            self.guard.direction
        )  # Convert Direction to string

        # Add obstacles
        for obstacle in self.obstacles:
            updated_grid[obstacle.row][obstacle.col] = "#"

        if with_added_obstacle:
            updated_grid[self.obstacles[-1].row][self.obstacles[-1].col] = "O"

        for line in updated_grid:
            print("".join(line))
        print()

    def move_guard(self, verbose: bool = False, with_added_obstacle: bool = False):
        row, col = self.guard.position.row, self.guard.position.col

        # Add the guard's starting position
        self.guard.position = Position(row, col)
        self.visited_positions.add(self.guard.position)

        # Move the guard until it is out of the grid or stuck in a loop
        while not self.guard.is_out(self) and not self.guard.has_loop():
            # Check if the guard is blocked by an obstacle
            if self.guard.is_blocked(self.obstacles):
                self.turns.append(self.guard.position)
                self.guard.rotate_right()

            # Move the guard to the next position
            self.guard.position = self.guard.get_next_position(grid=self)

            if verbose:
                self.plot_map(with_added_obstacle=with_added_obstacle)

        if self.guard.has_loop():
            print("Guard is stuck in a loop.")
        elif self.guard.is_out(self):
            print("Guard is out of the grid.")

        print(self.n_visited_positions)


def read_map(file_path: str) -> list[list[str]]:
    with open(file_path, "r") as file:
        return [[c for c in line.strip()] for line in file]


def part_1(file_path: str):
    """
    We need to predict the path of the guard and determine how many distinct positions
    the guard will visit before leaving the mapped area.
    """

    grid = Grid.from_str(read_map(file_path))
    grid.plot_map()
    grid.move_guard(verbose=True)


def part_2(file_path: str):
    """
    We need to find all the possible positions where we can place an obstacle
    such that the guard gets stuck in a loop.
    """

    # Load the grid
    grid = Grid.from_str(read_map(file_path))

    # We need to keep track of the guard's starting position and direction
    guard_start = grid.guard.position
    guard_start_direction = grid.guard.direction

    # First, move the guard to find all the possible positions where we can place an obstacle
    grid.move_guard(verbose=False)
    possible_positions: list[Position] = [
        p for p in grid.visited_positions if p != guard_start
    ]

    # Reset the grid
    grid.visited_positions.clear()
    grid.guard.position = guard_start
    grid.guard.direction = guard_start_direction
    grid.guard.turns.clear()

    # Count the number of looping obstacles
    looping_obstacles = 0
    logger.info(f"Possible positions: {len(possible_positions)}")

    # Iterate over all the possible positions and add an obstacle
    for i, position in enumerate(possible_positions):
        logger.info(
            f"Guard start: {guard_start}, direction: {guard_start_direction}, obstacle: {position}"
        )
        logger.info(f"Adding obstacle at position {position}.")
        grid.obstacles.append(Obstacle(position.row, position.col))

        grid.move_guard(verbose=False, with_added_obstacle=False)

        if grid.guard.has_loop():
            looping_obstacles += 1

        # remove the last obstacle from the grid
        grid.obstacles.pop()
        grid.visited_positions.clear()

        grid.guard.position = guard_start
        grid.guard.direction = guard_start_direction
        grid.guard.turns.clear()

        logger.info(f"Done with position {i+1}/{len(possible_positions)}.")

    print(f"Found {looping_obstacles} looping obstacles.")
