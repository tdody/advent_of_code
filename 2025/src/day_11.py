# Path: 2025/src/day_11.py

"""
--- Day 11: Reactor ---
You hear some loud beeping coming from a hatch in the floor of the factory, so you decide to check it out. Inside, you find several large electrical conduits and a ladder.

Climbing down the ladder, you discover the source of the beeping: a large, toroidal reactor which powers the factory above. Some Elves here are hurriedly running between the reactor and a nearby server rack, apparently trying to fix something.

One of the Elves notices you and rushes over. "It's a good thing you're here! We just installed a new server rack, but we aren't having any luck getting the reactor to communicate with it!" You glance around the room and see a tangle of cables and devices running from the server rack to the reactor. She rushes off, returning a moment later with a list of the devices and their outputs (your puzzle input).

For example:

aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
Each line gives the name of a device followed by a list of the devices to which its outputs are attached. So, bbb: ddd eee means that device bbb has two outputs, one leading to device ddd and the other leading to device eee.

The Elves are pretty sure that the issue isn't due to any specific device, but rather that the issue is triggered by data following some specific path through the devices. Data only ever flows from a device through its outputs; it can't flow backwards.

After dividing up the work, the Elves would like you to focus on the devices starting with the one next to you (an Elf hastily attaches a label which just says you) and ending with the main output to the reactor (which is the device with the label out).

To help the Elves figure out which path is causing the issue, they need you to find every path from you to out.

In this example, these are all of the paths from you to out:

Data could take the connection from you to bbb, then from bbb to ddd, then from ddd to ggg, then from ggg to out.
Data could take the connection to bbb, then to eee, then to out.
Data could go to ccc, then ddd, then ggg, then out.
Data could go to ccc, then eee, then out.
Data could go to ccc, then fff, then out.
In total, there are 5 different paths leading from you to out.

How many different paths lead from you to out?

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
Thanks in part to your analysis, the Elves have figured out a little bit about the issue. They now know that the problematic data path passes through both dac (a digital-to-analog converter) and fft (a device which performs a fast Fourier transform).

They're still not sure which specific path is the problem, and so they now need you to find every path from svr (the server rack) to out. However, the paths you find must all also visit both dac and fft (in any order).

For example:

svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
This new list of devices contains many paths from svr to out:

svr,aaa,fft,ccc,ddd,hub,fff,ggg,out
svr,aaa,fft,ccc,ddd,hub,fff,hhh,out
svr,aaa,fft,ccc,eee,dac,fff,ggg,out
svr,aaa,fft,ccc,eee,dac,fff,hhh,out
svr,bbb,tty,ccc,ddd,hub,fff,ggg,out
svr,bbb,tty,ccc,ddd,hub,fff,hhh,out
svr,bbb,tty,ccc,eee,dac,fff,ggg,out
svr,bbb,tty,ccc,eee,dac,fff,hhh,out
However, only 2 paths from svr to out visit both dac and fft.

Find all of the paths that lead from svr to out. How many of those paths visit both dac and fft?

"""

# --- Part One ---

import networkx as nx


def read_file(file_path: str) -> nx.DiGraph:
    """
    Read the input file and return the graph.
    """
    with open(file_path, "r") as f:
        data = f.read().splitlines()
        G = nx.DiGraph()
        for line in data:
            node, neighbors = line.split(":")
            neighbors = neighbors.split()
            for neighbor in neighbors:
                G.add_edge(node, neighbor)
    return G


def count_paths_dp(graph: nx.DiGraph, start: str, end: str) -> int:
    """
    Count simple paths from start to end using DFS with memoization.
    For a DAG, this is O(V + E). For graphs with cycles, we track visited nodes.
    """
    # Use adjacency list for faster lookups
    adj = {node: list(graph.successors(node)) for node in graph.nodes()}

    def dfs(node: str, visited: frozenset) -> int:
        if node == end:
            return 1
        total = 0
        new_visited = visited | {node}
        for neighbor in adj.get(node, []):
            if neighbor not in visited:
                total += dfs(neighbor, new_visited)
        return total

    return dfs(start, frozenset())


def part_1(file_path: str) -> int:
    """
    Read the input file and return the solution.
    """
    graph = read_file(file_path)
    return count_paths_dp(graph, "you", "out")


# --- Part Two ---

import sys
from collections import defaultdict

sys.setrecursionlimit(10000)


def part_2(file_path: str) -> int:
    """
    Read the input file and return the solution.
    Find all paths from svr to out that visit both dac and fft (in any order).

    Key insight: The graph is a DAG with narrow "waists" - layers where only
    a few nodes exist. ALL paths must pass through one of the nodes in each
    narrow layer.

    Strategy:
    1. For each segment between consecutive waists, count paths indexed by
       whether they include the mandatory nodes (fft at layer 10, dac at layer 28)
    2. Use DP to propagate counts through waists, tracking mandatory node inclusion
    3. Final answer = paths that include both fft and dac
    """
    graph = read_file(file_path)
    adj = {node: tuple(graph.successors(node)) for node in graph.nodes()}

    # Get topological generations to identify layers
    topo_gens = list(nx.topological_generations(graph))

    # Find relevant nodes (on paths from svr to out)
    svr_desc = nx.descendants(graph, 'svr') | {'svr'}
    out_anc = nx.ancestors(graph, 'out') | {'out'}
    relevant = svr_desc & out_anc

    # Define waist layers and their nodes
    waist_layers = [0, 7, 13, 19, 25, 31, 38]
    waists = []
    for layer in waist_layers:
        nodes = [n for n in topo_gens[layer] if n in relevant]
        waists.append((layer, nodes))

    mandatory_nodes = {'fft', 'dac'}

    def get_nodes_between_layers(start_layer: int, end_layer: int) -> set:
        """Get all relevant nodes between two layers (exclusive of start, inclusive of end)."""
        nodes = set()
        for layer in range(start_layer + 1, end_layer + 1):
            nodes.update(n for n in topo_gens[layer] if n in relevant)
        return nodes

    def count_paths_segment(
        start_node: str,
        end_node: str,
        allowed: set,
        segment_mandatory: set,
        adj: dict
    ) -> dict:
        """
        Count paths from start_node to end_node within allowed nodes,
        tracking which mandatory nodes are visited.
        Returns: {frozenset(mandatory_visited): count}
        """
        # Build subgraph adjacency
        sub_adj = {}
        for n in allowed:
            sub_adj[n] = [neighbor for neighbor in adj.get(n, ()) if neighbor in allowed]

        memo = {}

        def dp(node: str, visited_mand: frozenset) -> dict:
            key = (node, visited_mand)
            if key in memo:
                return memo[key]

            if node == end_node:
                return {visited_mand: 1}

            result = defaultdict(int)
            for neighbor in sub_adj.get(node, []):
                new_mand = visited_mand
                if neighbor in segment_mandatory:
                    new_mand = visited_mand | {neighbor}

                sub_result = dp(neighbor, new_mand)
                for m_set, cnt in sub_result.items():
                    result[m_set] += cnt

            memo[key] = dict(result) if result else {}
            return memo[key]

        init_mand = frozenset({start_node} & segment_mandatory)
        return dp(start_node, init_mand)

    # Initialize: start at svr with no mandatory visited
    current_state = defaultdict(int)
    current_state[('svr', frozenset())] = 1

    # Process each segment
    for i in range(len(waists) - 1):
        start_layer, start_nodes = waists[i]
        end_layer, end_nodes = waists[i + 1]

        # Get nodes in this segment
        segment_nodes = get_nodes_between_layers(start_layer, end_layer)
        allowed = segment_nodes | set(start_nodes)

        # Mandatory nodes in this segment
        segment_mandatory = mandatory_nodes & segment_nodes

        next_state = defaultdict(int)

        # For each current state, compute transitions
        for (start_node, mand_visited), incoming_count in current_state.items():
            if incoming_count == 0:
                continue

            # Count paths to each end node
            for end_node in end_nodes:
                path_results = count_paths_segment(
                    start_node, end_node, allowed, segment_mandatory, adj
                )

                for segment_mand, path_count in path_results.items():
                    total_mand = mand_visited | segment_mand
                    next_state[(end_node, total_mand)] += incoming_count * path_count

        current_state = next_state

    # Final answer: sum of counts where both fft and dac are visited
    total = 0
    for (node, mand_visited), count in current_state.items():
        if node == 'out' and 'fft' in mand_visited and 'dac' in mand_visited:
            total += count

    return total
