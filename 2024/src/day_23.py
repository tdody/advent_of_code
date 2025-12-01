"""
--- Day 23: LAN Party ---
As The Historians wander around a secure area at Easter Bunny HQ, you come across posters for a LAN party scheduled for today! Maybe you can find it; you connect to a nearby datalink port and download a map of the local network (your puzzle input).

The network map provides a list of every connection between two computers. For example:

kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
Each line of text in the network map represents a single connection; the line kh-tc represents a connection between the computer named kh and the computer named tc. Connections aren't directional; tc-kh would mean exactly the same thing.

LAN parties typically involve multiplayer games, so maybe you can locate it by finding groups of connected computers. Start by looking for sets of three computers where each computer in the set is connected to the other two computers.

In this example, there are 12 such sets of three inter-connected computers:

aq,cg,yn
aq,vc,wq
co,de,ka
co,de,ta
co,ka,ta
de,ka,ta
kh,qp,ub
qp,td,wh
tb,vc,wq
tc,td,wh
td,wh,yn
ub,vc,wq
If the Chief Historian is here, and he's at the LAN party, it would be best to know that right away. You're pretty sure his computer's name starts with t, so consider only sets of three computers where at least one computer's name starts with t. That narrows the list down to 7 sets of three inter-connected computers:

co,de,ta
co,ka,ta
de,ka,ta
qp,td,wh
tb,vc,wq
tc,td,wh
td,wh,yn
Find all the sets of three inter-connected computers. How many contain at least one computer with a name that starts with t?

--- Part Two ---
There are still way too many results to go through them all. You'll have to find the LAN party another way and go there yourself.

Since it doesn't seem like any employees are around, you figure they must all be at the LAN party. If that's true, the LAN party will be the largest set of computers that are all connected to each other. That is, for each computer at the LAN party, that computer will have a connection to every other computer at the LAN party.

In the above example, the largest set of computers that are all connected to each other is made up of co, de, ka, and ta. Each computer in this set has a connection to every other computer in the set:

ka-co
ta-co
de-co
ta-ka
de-ta
ka-de
The LAN party posters say that the password to get into the LAN party is the name of every computer at the LAN party, sorted alphabetically, then joined together with commas. (The people running the LAN party are clearly a bunch of nerds.) In this example, the password would be co,de,ka,ta.

What is the password to get into the LAN party?
"""

import itertools
import os
from loguru import logger
import networkx as nx
import matplotlib.pyplot as plt


# Path: src/day_23.py
# --- Part One ---


def read_file(file_path: str) -> nx.Graph:
    """
    Read the input file and return the graph.
    """

    graph = nx.Graph()

    with open(file_path, "r") as file:
        for line in file:
            node1, node2 = line.strip().split("-")
            graph.add_edge(node1, node2)

    logger.debug(f"Read {len(graph)} nodes from the file.")

    return graph


def find_groups_of_three_with_t(graph: nx.Graph) -> int:
    """
    Find all the sets of three inter-connected computers.
    """

    combos = set()
    for clique in nx.find_cliques(graph):
        for combo in itertools.combinations(clique, 3):
            if len(list(filter(lambda x: x[0] == "t", combo))):
                combos.add(tuple(sorted(combo)))
    return len(combos)


def find_largest_clique(graph: nx.Graph) -> str:
    """
    Find the largest set of computers that are all connected to each other.
    """

    max_clique = max(nx.find_cliques(graph), key=len)

    return ",".join(sorted(max_clique))


def part_1(file_path: str) -> int:
    """
    Read the input file and return the solution.
    """

    graph = read_file(file_path)

    if os.environ.get("LOGURU_LEVEL") == "DEBUG":
        nx.draw(graph, with_labels=True)
        plt.show()

    return find_groups_of_three_with_t(graph)


# --- Part Two ---


def part_2(file_path: str) -> str:
    """
    Read the input file and return the solution.
    """

    graph = read_file(file_path)

    return find_largest_clique(graph)
