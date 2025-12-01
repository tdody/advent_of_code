"""
--- Day 14: Restroom Redoubt ---
One of The Historians needs to use the bathroom; fortunately, you know there's a bathroom near an unvisited location on their list, and so you're all quickly teleported directly to the lobby of Easter Bunny Headquarters.

Unfortunately, EBHQ seems to have "improved" bathroom security again after your last visit. The area outside the bathroom is swarming with robots!

To get The Historian safely to the bathroom, you'll need a way to predict where the robots will be in the future. Fortunately, they all seem to be moving on the tile floor in predictable straight lines.

You make a list (your puzzle input) of all of the robots' current positions (p) and velocities (v), one robot per line. For example:

p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
Each robot's position is given as p=x,y where x represents the number of tiles the robot is from the left wall and y represents the number of tiles from the top wall (when viewed from above). So, a position of p=0,0 means the robot is all the way in the top-left corner.

Each robot's velocity is given as v=x,y where x and y are given in tiles per second. Positive x means the robot is moving to the right, and positive y means the robot is moving down. So, a velocity of v=1,-2 means that each second, the robot moves 1 tile to the right and 2 tiles up.

The robots outside the actual bathroom are in a space which is 101 tiles wide and 103 tiles tall (when viewed from above). However, in this example, the robots are in a space which is only 11 tiles wide and 7 tiles tall.

The robots are good at navigating over/under each other (due to a combination of springs, extendable legs, and quadcopters), so they can share the same tile and don't interact with each other. Visually, the number of robots on each tile in this example looks like this:

1.12.......
...........
...........
......11.11
1.1........
.........1.
.......1...
These robots have a unique feature for maximum bathroom security: they can teleport. When a robot would run into an edge of the space they're in, they instead teleport to the other side, effectively wrapping around the edges. Here is what robot p=2,4 v=2,-3 does for the first few seconds:

Initial state:
...........
...........
...........
...........
..1........
...........
...........

After 1 second:
...........
....1......
...........
...........
...........
...........
...........

After 2 seconds:
...........
...........
...........
...........
...........
......1....
...........

After 3 seconds:
...........
...........
........1..
...........
...........
...........
...........

After 4 seconds:
...........
...........
...........
...........
...........
...........
..........1

After 5 seconds:
...........
...........
...........
.1.........
...........
...........
...........
The Historian can't wait much longer, so you don't have to simulate the robots for very long. Where will the robots be after 100 seconds?

In the above example, the number of robots on each tile after 100 seconds has elapsed looks like this:

......2..1.
...........
1..........
.11........
.....1.....
...12......
.1....1....
To determine the safest area, count the number of robots in each quadrant after 100 seconds. Robots that are exactly in the middle (horizontally or vertically) don't count as being in any quadrant, so the only relevant robots are:

..... 2..1.
..... .....
1.... .....

..... .....
...12 .....
.1... 1....
In this example, the quadrants contain 1, 3, 4, and 1 robot. Multiplying these together gives a total safety factor of 12.

Predict the motion of the robots in your list within a space which is 101 tiles wide and 103 tiles tall. What will the safety factor be after exactly 100 seconds have elapsed?

--- Part Two ---
During the bathroom break, someone notices that these robots seem awfully similar to ones built and used at the North Pole. If they're the same type of robots, they should have a hard-coded Easter egg: very rarely, most of the robots should arrange themselves into a picture of a Christmas tree.

What is the fewest number of seconds that must elapse for the robots to display the Easter egg?
"""

# Path: src/day_14.py
# --- Part One ---

import re

import matplotlib.pyplot as plt
from loguru import logger


class Robot:
    def __init__(
        self, x: int, y: int, dx: int, dy: int, grid_width: int, grid_height: int
    ):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.grid_width = grid_width
        self.grid_height = grid_height

    def move(self):
        self.x += self.dx
        self.y += self.dy

        if self.x < 0:
            self.x += self.grid_width
        elif self.x >= self.grid_width:
            self.x -= self.grid_width

        if self.y < 0:
            self.y += self.grid_height
        elif self.y >= self.grid_height:
            self.y -= self.grid_height

    def __repr__(self):
        return f"Robot({self.x}, {self.y}, {self.dx}, {self.dy})"

    @classmethod
    def from_line(cls, line: str, grid_width: int, grid_height: int):
        x, y, dx, dy = map(int, re.findall(r"-?\d+", line))
        return cls(x, y, dx, dy, grid_width, grid_height)


def count_robots(robots: list[Robot], grid_width: int, grid_height: int):
    # create the 4 quadrants of the grid
    q1 = (0, grid_width // 2), (0, grid_height // 2)
    q2 = (grid_width - grid_width // 2, grid_width), (0, grid_height // 2)
    q3 = (
        (grid_width - grid_width // 2, grid_width),
        (grid_height - grid_height // 2, grid_height),
    )
    q4 = (0, grid_width // 2), (grid_height - grid_height // 2, grid_height)

    quadrants = [q1, q2, q3, q4]

    # count the robots in each quadrant
    counts = [0, 0, 0, 0]
    for robot in robots:
        for i, (x_range, y_range) in enumerate(quadrants):
            if (
                x_range[0] <= robot.x < x_range[1]
                and y_range[0] <= robot.y < y_range[1]
            ):
                counts[i] += 1

    total_score = 1
    for count in counts:
        total_score *= count

    return total_score


def plot_robots(robots: list[Robot], grid_width: int, grid_height: int):
    grid = [["." for _ in range(grid_width)] for _ in range(grid_height)]

    for robot in robots:
        if grid[robot.y][robot.x] == ".":
            grid[robot.y][robot.x] = "1"
        else:
            grid_val = int(grid[robot.y][robot.x]) + 1
            grid[robot.y][robot.x] = str(grid_val)

    for row in grid:
        print("".join(row))
    print()


def get_robots_standard_deviation(robots: list[Robot]) -> float:
    """
    Get the standard deviation of the robots' positions.
    """

    x_positions = [robot.x for robot in robots]
    y_positions = [robot.y for robot in robots]

    x_mean = sum(x_positions) / len(x_positions)
    y_mean = sum(y_positions) / len(y_positions)

    x_variance = sum((x - x_mean) ** 2 for x in x_positions) / len(x_positions)
    y_variance = sum((y - y_mean) ** 2 for y in y_positions) / len(y_positions)

    x_std = x_variance**0.5
    y_std = y_variance**0.5

    return x_std + y_std


def part_1(file_path: str) -> int:
    """
    Read the input file and return the solution.
    """

    with open(file_path) as file:
        lines = file.readlines()

    grid_width, grid_height = 101, 103

    if "test" in file_path:
        grid_width, grid_height = 11, 7

    robots = [Robot.from_line(line, grid_width, grid_height) for line in lines]

    plot_robots(robots, grid_width, grid_height)

    for _ in range(100):
        for robot in robots:
            robot.move()

    plot_robots(robots, grid_width, grid_height)

    return count_robots(robots, grid_width, grid_height)


# --- Part Two ---


def part_2(file_path: str) -> None:
    """
    Read the input file and return the solution.
    """

    with open(file_path) as file:
        lines = file.readlines()

    grid_width, grid_height = 101, 103

    if "test" in file_path:
        grid_width, grid_height = 11, 7

    robots = [Robot.from_line(line, grid_width, grid_height) for line in lines]

    data_points = []

    for i in range(10000):
        for robot in robots:
            robot.move()

        stddev = get_robots_standard_deviation(robots)
        data_points.append(stddev)

        if stddev < 45:
            logger.info(f"Found the solution at time {i+1}")
            break

    # plot the standard deviation
    plot_robots(robots, grid_width, grid_height)

    fig, ax = plt.subplots()
    ax.set_xlim(0, len(data_points) * 1.05)
    ax.set_ylim(0, max(data_points) * 1.05)
    plt.plot(data_points)
    plt.show()

    return None
