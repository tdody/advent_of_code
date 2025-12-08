# Path: 2025/src/day_8.py

"""
--- Day 8: Playground ---
Equipped with a new understanding of teleporter maintenance, you confidently step onto the repaired teleporter pad.

You rematerialize on an unfamiliar teleporter pad and find yourself in a vast underground space which contains a giant playground!

Across the playground, a group of Elves are working on setting up an ambitious Christmas decoration project. Through careful rigging, they have suspended a large number of small electrical junction boxes.

Their plan is to connect the junction boxes with long strings of lights. Most of the junction boxes don't provide electricity; however, when two junction boxes are connected by a string of lights, electricity can pass between those two junction boxes.

The Elves are trying to figure out which junction boxes to connect so that electricity can reach every junction box. They even have a list of all of the junction boxes' positions in 3D space (your puzzle input).

For example:

162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
This list describes the position of 20 junction boxes, one per line. Each position is given as X,Y,Z coordinates. So, the first junction box in the list is at X=162, Y=817, Z=812.

To save on string lights, the Elves would like to focus on connecting pairs of junction boxes that are as close together as possible according to straight-line distance. In this example, the two junction boxes which are closest together are 162,817,812 and 425,690,689.

By connecting these two junction boxes together, because electricity can flow between them, they become part of the same circuit. After connecting them, there is a single circuit which contains two junction boxes, and the remaining 18 junction boxes remain in their own individual circuits.

Now, the two junction boxes which are closest together but aren't already directly connected are 162,817,812 and 431,825,988. After connecting them, since 162,817,812 is already connected to another junction box, there is now a single circuit which contains three junction boxes and an additional 17 circuits which contain one junction box each.

The next two junction boxes to connect are 906,360,560 and 805,96,715. After connecting them, there is a circuit containing 3 junction boxes, a circuit containing 2 junction boxes, and 15 circuits which contain one junction box each.

The next two junction boxes are 431,825,988 and 425,690,689. Because these two junction boxes were already in the same circuit, nothing happens!

This process continues for a while, and the Elves are concerned that they don't have enough extension cables for all these circuits. They would like to know how big the circuits will be.

After making the ten shortest connections, there are 11 circuits: one circuit which contains 5 junction boxes, one circuit which contains 4 junction boxes, two circuits which contain 2 junction boxes each, and seven circuits which each contain a single junction box. Multiplying together the sizes of the three largest circuits (5, 4, and one of the circuits of size 2) produces 40.

Your list contains many junction boxes; connect together the 1000 pairs of junction boxes which are closest together. Afterward, what do you get if you multiply together the sizes of the three largest circuits?


--- Part Two ---
The Elves were right; they definitely don't have enough extension cables. You'll need to keep connecting junction boxes together until they're all in one large circuit.

Continuing the above example, the first connection which causes all of the junction boxes to form a single circuit is between the junction boxes at 216,146,977 and 117,168,530. The Elves need to know how far those junction boxes are from the wall so they can pick the right extension cable; multiplying the X coordinates of those two junction boxes (216 and 117) produces 25272.

Continue connecting the closest unconnected pairs of junction boxes together until they're all in the same circuit. What do you get if you multiply together the X coordinates of the last two junction boxes you need to connect?
"""

# --- Part One ---

from loguru import logger
from typing import Literal
from typing import Optional
import math
import networkx as nx
import numpy as np
from scipy.spatial.distance import cdist


class JunctionBox:
    id: int
    x: int
    y: int
    z: int

    def __init__(self, id: int, x: int, y: int, z: int):
        self.id = id
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_file(cls, file_path: str) -> list["JunctionBox"]:
        with open(file_path, "r") as file:
            return [cls.from_string(line.strip(), id) for id, line in enumerate(file)]

    @classmethod
    def from_string(cls, string: str, id: int) -> "JunctionBox":
        x, y, z = string.split(",")
        return cls(id, int(x), int(y), int(z))

    def __str__(self) -> str:
        return f"{self.x},{self.y},{self.z}"

    def __repr__(self) -> str:
        return f"JunctionBox(id={self.id}, x={self.x}, y={self.y}, z={self.z})"

    def __eq__(self, other: "JunctionBox") -> bool:
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)


class Connection:
    junction_box_1: JunctionBox
    junction_box_2: JunctionBox

    def __init__(self, junction_box_1: JunctionBox, junction_box_2: JunctionBox):
        self.junction_box_1 = junction_box_1
        self.junction_box_2 = junction_box_2

    def __str__(self) -> str:
        return f"{self.junction_box_1} -> {self.junction_box_2}"

    def __repr__(self) -> str:
        return f"Connection(junction_box_1={self.junction_box_1}, junction_box_2={self.junction_box_2})"

    @property
    def length(self) -> int:
        return math.sqrt(
            (self.junction_box_1.x - self.junction_box_2.x) ** 2
            + (self.junction_box_1.y - self.junction_box_2.y) ** 2
            + (self.junction_box_1.z - self.junction_box_2.z) ** 2
        )

    def __eq__(self, other: "Connection") -> bool:
        return set([self.junction_box_1, self.junction_box_2]) == set(
            [other.junction_box_1, other.junction_box_2]
        )


class Grid:
    connections: list[Connection]
    junction_boxes: list[JunctionBox]
    __distance_matrix: Optional[np.array]

    def __init__(
        self, connections: list[Connection], junction_boxes: list[JunctionBox]
    ):
        self.connections = connections
        self.junction_boxes = junction_boxes
        self.__distance_matrix = None

    @classmethod
    def from_file(cls, file_path: str) -> "Grid":
        junction_boxes = JunctionBox.from_file(file_path)
        connections = []
        return cls(connections, junction_boxes)

    def __str__(self) -> str:
        n_nodes = len(self.junction_boxes)
        n_connections = len(self.connections)
        return f"Grid(n_nodes={n_nodes}, n_connections={n_connections})"

    def __repr__(self) -> str:
        return self.__str__()

    def __compute_distance_matrix(self) -> np.array:
        coordinates = np.array(
            [
                [junction_box.x, junction_box.y, junction_box.z]
                for junction_box in self.junction_boxes
            ]
        )
        logger.debug(f"Coordinates shape: {coordinates.shape}")
        distance_matrix = cdist(coordinates, coordinates, metric="euclidean")
        np.fill_diagonal(distance_matrix, np.inf)

        self.__distance_matrix = distance_matrix
        logger.debug(f"Distance matrix shape: {self.__distance_matrix.shape}")

    def find_shortest_cable(self) -> Optional[Connection]:
        if self.__distance_matrix is None:
            self.__compute_distance_matrix()
        shortest_cable: Optional[tuple[JunctionBox, JunctionBox]] = None

        # Single shortest distance overall (i, j pair)
        flat_idx = np.argmin(self.__distance_matrix)
        i, j = np.unravel_index(flat_idx, self.__distance_matrix.shape)

        shortest_cable = Connection(self.junction_boxes[i], self.junction_boxes[j])

        self.__distance_matrix[i, j] = np.inf
        self.__distance_matrix[j, i] = np.inf

        return shortest_cable

    def find_connected_circuits(
        self, top_n: Optional[int] = None
    ) -> list[list[JunctionBox]]:
        # using nx find the connected components
        graph = nx.Graph()
        for junction_box in self.junction_boxes:
            graph.add_node(junction_box.id)
        for connection in self.connections:
            graph.add_edge(connection.junction_box_1.id, connection.junction_box_2.id)

        # sort by size
        connected_components = list(nx.connected_components(graph))
        connected_components.sort(key=len, reverse=True)
        if top_n is not None:
            return connected_components[:top_n]
        return connected_components

    def is_fully_connected(self) -> bool:
        return len(self.find_connected_circuits()) == 1


def part_1(file_path: str) -> int:
    """
    Read the input file and return the solution.
    """

    grid: Grid = Grid.from_file(file_path)
    n_cables: Literal[10, 1000] = 10 if "test" in file_path else 1000

    logger.debug(f"Grid: {grid}")

    for _ in range(n_cables):
        new_connection = grid.find_shortest_cable()
        logger.debug(f"New connection: {new_connection}")
        grid.connections.append(new_connection)

    circuits = grid.find_connected_circuits(top_n=3)

    for circuit in circuits:
        logger.debug(f"Circuit: {circuit}")

    # multiply the size of the circuits
    return math.prod(len(circuit) for circuit in circuits)


# --- Part Two ---


def part_2(file_path: str) -> int:
    """
    Read the input file and return the solution.
    """

    grid: Grid = Grid.from_file(file_path)
    last_connection: Optional[Connection] = None

    while not grid.is_fully_connected():
        last_connection = grid.find_shortest_cable()
        logger.debug(f"New connection: {last_connection}")
        grid.connections.append(last_connection)

    return last_connection.junction_box_1.x * last_connection.junction_box_2.x
