# Path: 2025/src/day_9.py
"""
--- Day 9: Movie Theater ---
You slide down the firepole in the corner of the playground and land in the North Pole base movie theater!

The movie theater has a big tile floor with an interesting pattern. Elves here are redecorating the theater by switching out some of the square tiles in the big grid they form. Some of the tiles are red; the Elves would like to find the largest rectangle that uses red tiles for two of its opposite corners. They even have a list of where the red tiles are located in the grid (your puzzle input).

For example:

7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
Showing red tiles as # and other tiles as ., the above arrangement of red tiles would look like this:

..............
.......#...#..
..............
..#....#......
..............
..#......#....
..............
.........#.#..
..............
You can choose any two red tiles as the opposite corners of your rectangle; your goal is to find the largest rectangle possible.

For example, you could make a rectangle (shown as O) with an area of 24 between 2,5 and 9,7:

..............
.......#...#..
..............
..#....#......
..............
..OOOOOOOO....
..OOOOOOOO....
..OOOOOOOO.#..
..............
Or, you could make a rectangle with area 35 between 7,1 and 11,7:

..............
.......OOOOO..
.......OOOOO..
..#....OOOOO..
.......OOOOO..
..#....OOOOO..
.......OOOOO..
.......OOOOO..
..............
You could even make a thin rectangle with an area of only 6 between 7,3 and 2,3:

..............
.......#...#..
..............
..OOOOOO......
..............
..#......#....
..............
.........#.#..
..............
Ultimately, the largest rectangle you can make in this example has area 50. One way to do this is between 2,5 and 11,1:

..............
..OOOOOOOOOO..
..OOOOOOOOOO..
..OOOOOOOOOO..
..OOOOOOOOOO..
..OOOOOOOOOO..
..............
.........#.#..
..............
Using two red tiles as opposite corners, what is the largest area of any rectangle you can make?


The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
The Elves just remembered: they can only switch out tiles that are red or green. So, your rectangle can only include red or green tiles.

In your list, every red tile is connected to the red tile before and after it by a straight line of green tiles. The list wraps, so the first red tile is also connected to the last red tile. Tiles that are adjacent in your list will always be on either the same row or the same column.

Using the same example as before, the tiles marked X would be green:

..............
.......#XXX#..
.......X...X..
..#XXXX#...X..
..X........X..
..#XXXXXX#.X..
.........X.X..
.........#X#..
..............
In addition, all of the tiles inside this loop of red and green tiles are also green. So, in this example, these are the green tiles:

..............
.......#XXX#..
.......XXXXX..
..#XXXX#XXXX..
..XXXXXXXXXX..
..#XXXXXX#XX..
.........XXX..
.........#X#..
..............
The remaining tiles are never red nor green.

The rectangle you choose still must have red tiles in opposite corners, but any other tiles it includes must now be red or green. This significantly limits your options.

For example, you could make a rectangle out of red and green tiles with an area of 15 between 7,3 and 11,1:

..............
.......OOOOO..
.......OOOOO..
..#XXXXOOOOO..
..XXXXXXXXXX..
..#XXXXXX#XX..
.........XXX..
.........#X#..
..............
Or, you could make a thin rectangle with an area of 3 between 9,7 and 9,5:

..............
.......#XXX#..
.......XXXXX..
..#XXXX#XXXX..
..XXXXXXXXXX..
..#XXXXXXOXX..
.........OXX..
.........OX#..
..............
The largest rectangle you can make in this example using only red and green tiles has area 24. One way to do this is between 9,5 and 2,3:

..............
.......#XXX#..
.......XXXXX..
..OOOOOOOOXX..
..OOOOOOOOXX..
..OOOOOOOOXX..
.........XXX..
.........#X#..
..............
Using two red tiles as opposite corners, what is the largest area of any rectangle you can make using only red and green tiles?
"""
# --- Part One ---

from loguru import logger
from tqdm import tqdm


class Point:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y


def rectangle_area(point_1: Point, point_2: Point) -> int:
    return (abs(point_2.x - point_1.x) + 1) * (abs(point_2.y - point_1.y) + 1)


class Grid:
    red_tiles: set[Point]
    red_tiles_ordered: list[Point]
    # For optimization: store x-ranges per row that are inside the polygon
    # Each row y maps to a list of (x_start, x_end) inclusive ranges
    row_ranges: dict[int, list[tuple[int, int]]]

    def __init__(
        self, red_tiles: set[Point], red_tiles_ordered: list[Point] | None = None
    ):
        self.red_tiles = red_tiles
        self.red_tiles_ordered = (
            red_tiles_ordered if red_tiles_ordered is not None else list(red_tiles)
        )
        self.row_ranges = {}

    @classmethod
    def from_file(cls, file_path: str):
        with open(file_path, "r") as file:
            red_tiles_list = [
                Point(int(x), int(y))
                for x, y in [line.strip().split(",") for line in file.readlines()]
            ]
            return cls(set(red_tiles_list), red_tiles_list)

    def __str__(self):
        if not self.row_ranges:
            return f"Grid with {len(self.red_tiles)} red tiles (polygon not built)"
        min_x = min(self.red_tiles, key=lambda p: p.x).x
        max_x = max(self.red_tiles, key=lambda p: p.x).x
        min_y = min(self.row_ranges.keys())
        max_y = max(self.row_ranges.keys())

        def is_inside(x: int, y: int) -> bool:
            if y not in self.row_ranges:
                return False
            return any(x_start <= x <= x_end for x_start, x_end in self.row_ranges[y])

        return "Grid:\n" + "\n".join(
            [
                "".join(
                    [
                        "#"
                        if Point(x, y) in self.red_tiles
                        else "X"
                        if is_inside(x, y)
                        else "."
                        for x in range(min_x, max_x + 1)
                    ]
                )
                for y in range(min_y, max_y + 1)
            ]
        )

    def __repr__(self):
        return self.__str__()

    def build_polygon_ranges(self):
        """
        Build row_ranges: for each y, store the x-ranges that are inside the polygon.

        Uses sweep line algorithm for efficiency:
        - O(v_segments × log) for events instead of O(rows × v_segments)
        - Maintains active vertical edges incrementally
        """
        if not self.red_tiles_ordered:
            return

        import bisect
        from collections import defaultdict

        # Step 1: Extract horizontal and vertical segments from polygon
        h_segments: dict[int, list[tuple[int, int]]] = defaultdict(list)
        v_segments: list[tuple[int, int, int]] = []

        n = len(self.red_tiles_ordered)
        for i in range(n):
            p1 = self.red_tiles_ordered[i]
            p2 = self.red_tiles_ordered[(i + 1) % n]

            if p1.x == p2.x:
                v_segments.append((p1.x, min(p1.y, p2.y), max(p1.y, p2.y)))
            else:
                h_segments[p1.y].append((min(p1.x, p2.x), max(p1.x, p2.x)))

        # Get bounding box
        all_y = [p.y for p in self.red_tiles_ordered]
        min_y, max_y = min(all_y), max(all_y)

        # Step 2: Create sweep line events
        # Event: (y, type, x) where type: 0=start (add edge), 1=end (remove edge)
        events: list[tuple[int, int, int]] = []
        for x, y_min, y_max in v_segments:
            events.append((y_min, 0, x))  # start: add edge at y_min
            events.append((y_max, 1, x))  # end: remove edge at y_max
        events.sort()

        # Step 3: Sweep line - process events and build row_ranges
        self.row_ranges = {}
        active: list[int] = []  # sorted list of active vertical edge x-coordinates
        event_idx = 0

        for y in range(min_y, max_y + 1):
            # Process all events at this y (starts before ends due to sort order)
            while event_idx < len(events) and events[event_idx][0] == y:
                _, etype, x = events[event_idx]
                if etype == 0:  # start
                    bisect.insort(active, x)
                else:  # end
                    active.remove(x)
                event_idx += 1

            # Build ranges from active edges (already sorted!)
            ranges: list[tuple[int, int]] = []
            for j in range(0, len(active) - 1, 2):
                ranges.append((active[j], active[j + 1]))

            # Add horizontal segments at this row
            for x_min, x_max in h_segments.get(y, []):
                ranges.append((x_min, x_max))

            # Merge overlapping/adjacent ranges
            if ranges:
                ranges.sort()
                merged = [ranges[0]]
                for start, end in ranges[1:]:
                    if start <= merged[-1][1] + 1:
                        merged[-1] = (merged[-1][0], max(merged[-1][1], end))
                    else:
                        merged.append((start, end))
                self.row_ranges[y] = merged

        logger.info(f"Built polygon ranges for {len(self.row_ranges)} rows")

    def _row_segment_covered(self, y: int, x_min: int, x_max: int) -> bool:
        """
        Check if the segment [x_min, x_max] in row y is fully inside the polygon.
        A segment is covered if it's entirely within one of the row's x-ranges.
        """
        if y not in self.row_ranges:
            return False

        # Check if [x_min, x_max] is fully contained in any range
        for range_start, range_end in self.row_ranges[y]:
            if range_start <= x_min and x_max <= range_end:
                return True
        return False

    def rectangle_inside_polygon(self, point_1: Point, point_2: Point) -> bool:
        """
        Check if the rectangle defined by two opposite corners is fully inside
        the polygon. Uses row_ranges for O(height * num_ranges) checks.
        """
        min_x = min(point_1.x, point_2.x)
        max_x = max(point_1.x, point_2.x)
        min_y = min(point_1.y, point_2.y)
        max_y = max(point_1.y, point_2.y)

        # Check each row in the rectangle
        for y in range(min_y, max_y + 1):
            if not self._row_segment_covered(y, min_x, max_x):
                return False
        return True

    def find_max_rectangle_area(self, only_inside_polygon: bool = False) -> int:
        max_area = 0
        red_list = list(self.red_tiles)

        # Sort by potential area (descending) to check larger rectangles first
        # This allows early termination in some cases
        if only_inside_polygon:
            # Pre-compute areas and sort
            pairs_with_area = [
                (point_1, point_2, rectangle_area(point_1, point_2))
                for i, point_1 in enumerate(red_list)
                for point_2 in red_list[i + 1 :]
            ]
            pairs_with_area.sort(key=lambda x: x[2], reverse=True)

            for point_1, point_2, area in tqdm(
                pairs_with_area, desc="Checking rectangles"
            ):
                if area <= max_area:
                    break  # Can't find larger area
                if self.rectangle_inside_polygon(point_1, point_2):
                    max_area = area
        else:
            for i, point_1 in enumerate(red_list):
                for point_2 in red_list[i + 1 :]:
                    area = rectangle_area(point_1, point_2)
                    if area > max_area:
                        max_area = area
        return max_area


def part_1(file_path: str) -> int:
    """
    Read the input file and return the solution.
    """

    grid = Grid.from_file(file_path)
    logger.debug(grid)
    return grid.find_max_rectangle_area()


# --- Part Two ---


def part_2(file_path: str) -> int:
    """
    Read the input file and return the solution.
    """

    grid = Grid.from_file(file_path)
    grid.build_polygon_ranges()
    logger.debug(grid)
    return grid.find_max_rectangle_area(only_inside_polygon=True)
