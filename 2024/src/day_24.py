"""
--- Day 24: Crossed Wires ---
You and The Historians arrive at the edge of a large grove somewhere in the jungle. After the last incident, the Elves installed a small device that monitors the fruit. While The Historians search the grove, one of them asks if you can take a look at the monitoring device; apparently, it's been malfunctioning recently.

The device seems to be trying to produce a number through some boolean logic gates. Each gate has two inputs and one output. The gates all operate on values that are either true (1) or false (0).

AND gates output 1 if both inputs are 1; if either input is 0, these gates output 0.
OR gates output 1 if one or both inputs is 1; if both inputs are 0, these gates output 0.
XOR gates output 1 if the inputs are different; if the inputs are the same, these gates output 0.
Gates wait until both inputs are received before producing output; wires can carry 0, 1 or no value at all. There are no loops; once a gate has determined its output, the output will not change until the whole system is reset. Each wire is connected to at most one gate output, but can be connected to many gate inputs.

Rather than risk getting shocked while tinkering with the live system, you write down all of the gate connections and initial wire values (your puzzle input) so you can consider them in relative safety. For example:

x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02
Because gates wait for input, some wires need to start with a value (as inputs to the entire system). The first section specifies these values. For example, x00: 1 means that the wire named x00 starts with the value 1 (as if a gate is already outputting that value onto that wire).

The second section lists all of the gates and the wires connected to them. For example, x00 AND y00 -> z00 describes an instance of an AND gate which has wires x00 and y00 connected to its inputs and which will write its output to wire z00.

In this example, simulating these gates eventually causes 0 to appear on wire z00, 0 to appear on wire z01, and 1 to appear on wire z02.

Ultimately, the system is trying to produce a number by combining the bits on all wires starting with z. z00 is the least significant bit, then z01, then z02, and so on.

In this example, the three output bits form the binary number 100 which is equal to the decimal number 4.

Here's a larger example:

x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
After waiting for values on all wires starting with z, the wires in this system have the following values:

bfw: 1
bqk: 1
djm: 1
ffh: 0
fgs: 1
frj: 1
fst: 1
gnj: 1
hwm: 1
kjc: 0
kpj: 1
kwq: 0
mjb: 1
nrd: 1
ntg: 0
pbm: 1
psh: 1
qhw: 1
rvg: 0
tgd: 0
tnw: 1
vdt: 1
wpb: 0
z00: 0
z01: 0
z02: 0
z03: 1
z04: 0
z05: 1
z06: 1
z07: 1
z08: 1
z09: 1
z10: 1
z11: 0
z12: 0
Combining the bits from all wires starting with z produces the binary number 0011111101000. Converting this number to decimal produces 2024.

Simulate the system of gates and wires. What decimal number does it output on the wires starting with z?

--- Part Two ---
After inspecting the monitoring device more closely, you determine that the system you're simulating is trying to add two binary numbers.

Specifically, it is treating the bits on wires starting with x as one binary number, treating the bits on wires starting with y as a second binary number, and then attempting to add those two numbers together. The output of this operation is produced as a binary number on the wires starting with z. (In all three cases, wire 00 is the least significant bit, then 01, then 02, and so on.)

The initial values for the wires in your puzzle input represent just one instance of a pair of numbers that sum to the wrong value. Ultimately, any two binary numbers provided as input should be handled correctly. That is, for any combination of bits on wires starting with x and wires starting with y, the sum of the two numbers those bits represent should be produced as a binary number on the wires starting with z.

For example, if you have an addition system with four x wires, four y wires, and five z wires, you should be able to supply any four-bit number on the x wires, any four-bit number on the y numbers, and eventually find the sum of those two numbers as a five-bit number on the z wires. One of the many ways you could provide numbers to such a system would be to pass 11 on the x wires (1011 in binary) and 13 on the y wires (1101 in binary):

x00: 1
x01: 1
x02: 0
x03: 1
y00: 1
y01: 0
y02: 1
y03: 1
If the system were working correctly, then after all gates are finished processing, you should find 24 (11+13) on the z wires as the five-bit binary number 11000:

z00: 0
z01: 0
z02: 0
z03: 1
z04: 1
Unfortunately, your actual system needs to add numbers with many more bits and therefore has many more wires.

Based on forensic analysis of scuff marks and scratches on the device, you can tell that there are exactly four pairs of gates whose output wires have been swapped. (A gate can only be in at most one such pair; no gate's output was swapped multiple times.)

For example, the system below is supposed to find the bitwise AND of the six-bit number on x00 through x05 and the six-bit number on y00 through y05 and then write the result as a six-bit number on z00 through z05:

x00: 0
x01: 1
x02: 0
x03: 1
x04: 0
x05: 1
y00: 0
y01: 0
y02: 1
y03: 1
y04: 0
y05: 1

x00 AND y00 -> z05
x01 AND y01 -> z02
x02 AND y02 -> z01
x03 AND y03 -> z03
x04 AND y04 -> z04
x05 AND y05 -> z00
However, in this example, two pairs of gates have had their output wires swapped, causing the system to produce wrong answers. The first pair of gates with swapped outputs is x00 AND y00 -> z05 and x05 AND y05 -> z00; the second pair of gates is x01 AND y01 -> z02 and x02 AND y02 -> z01. Correcting these two swaps results in this system that works as intended for any set of initial values on wires that start with x or y:

x00 AND y00 -> z00
x01 AND y01 -> z01
x02 AND y02 -> z02
x03 AND y03 -> z03
x04 AND y04 -> z04
x05 AND y05 -> z05
In this example, two pairs of gates have outputs that are involved in a swap. By sorting their output wires' names and joining them with commas, the list of wires involved in swaps is z00,z01,z02,z05.

Of course, your actual system is much more complex than this, and the gates that need their outputs swapped could be anywhere, not just attached to a wire starting with z. If you were to determine that you need to swap output wires aaa with eee, ooo with z99, bbb with ccc, and aoc with z24, your answer would be aaa,aoc,bbb,ccc,eee,ooo,z24,z99.

Your system of gates and wires has four pairs of gates which need their output wires swapped - eight wires in total. Determine which four pairs of gates need their outputs swapped so that your system correctly performs addition; what do you get if you sort the names of the eight wires involved in a swap and then join those names with commas?
"""

# Path: src/day_24.py
# --- Part One ---

from typing import Optional
from loguru import logger
from networkx import DiGraph
from networkx import draw

OPERATORS = ["AND", "OR", "XOR", "SELF"]


class OperatorGraph(DiGraph):
    def __init__(self):
        super().__init__()

    def add_node(self, name: str, value: Optional[int], operator: str):
        super().add_node(name, operator=operator, value=value)

    def add_edge(self, node1: str, node2: str):
        super().add_edge(node1, node2)

    def compute_node(self, node: str) -> None:
        """
        Compute the value of the node.
        """

        if self.nodes[node]["value"] is not None:
            logger.debug(f"Node {node} already computed.")
            return

        predecessors = list(self.predecessors(node))

        logger.debug(
            f"Computing node: {node}, with {predecessors} using {self.nodes[node]['operator']} operator."
        )

        if self.nodes[list(self.predecessors(node))[0]]["value"] is None:
            logger.debug(f"   Predecessor {predecessors[0]} not computed.")
            return
        if self.nodes[list(self.predecessors(node))[1]]["value"] is None:
            logger.debug(f"   Predecessor {predecessors[1]} not computed.")
            return

        operator = self.nodes[node]["operator"]
        if operator == "SELF":
            self.nodes[node]["value"] = self.nodes[node]["value"]
        elif operator == "AND":
            self.nodes[node]["value"] = (
                self.nodes[list(self.predecessors(node))[0]]["value"]
                & self.nodes[list(self.predecessors(node))[1]]["value"]
            )
        elif operator == "OR":
            self.nodes[node]["value"] = (
                self.nodes[list(self.predecessors(node))[0]]["value"]
                | self.nodes[list(self.predecessors(node))[1]]["value"]
            )
        elif operator == "XOR":
            self.nodes[node]["value"] = (
                self.nodes[list(self.predecessors(node))[0]]["value"]
                ^ self.nodes[list(self.predecessors(node))[1]]["value"]
            )

        assert self.nodes[node]["value"] is not None

        return

    def is_fully_computed(self) -> bool:
        """
        Check if all the nodes have been computed.
        """

        for node in self.nodes:
            if self.nodes[node]["value"] is None:
                return False

        return True

    def compute_all_nodes(self) -> None:
        """
        Compute all the nodes.
        """

        while not self.is_fully_computed():
            for node in self.nodes:
                self.compute_node(node)

    def plot_graph(self):
        """
        Plot the graph.
        """

        import matplotlib.pyplot as plt

        draw(self, with_labels=True)
        plt.show()


def read_file(file_path: str) -> tuple[OperatorGraph, list[str]]:
    """
    Read the input file and return the graph.
    """

    graph = OperatorGraph()
    output_nodes: set[str] = set()

    with open(file_path, "r") as file:
        for line in file:
            if ":" in line:
                node_name, value = line.strip().split(":")
                graph.add_node(node_name, value=int(value), operator="SELF")
            elif "->" in line:
                values = line.strip().split(" ")
                node_1 = values[0]
                operator = values[1]
                node_2 = values[2]

                assert operator in OPERATORS

                if node_1 not in graph:
                    graph.add_node(name=node_1, value=None, operator="")
                if node_2 not in graph:
                    graph.add_node(name=node_2, value=None, operator="")
                node_3 = values[4]
                if node_3 not in graph:
                    graph.add_node(name=node_3, value=None, operator=operator)
                else:
                    graph.nodes[node_3]["operator"] = operator

                graph.add_edge(node_1, node_3)
                graph.add_edge(node_2, node_3)

                output_nodes.add(node_3)

    logger.debug(f"Read {len(graph)} nodes from the file.")

    sorted_output_nodes = sorted(list(output_nodes))

    return graph, sorted_output_nodes


def get_output_values(graph: OperatorGraph, output_nodes: list[str]) -> int:
    """
    Get the values of the output nodes.
    """

    output_value = 0
    output_nodes = [node for node in output_nodes if node.startswith("z")]

    for node in output_nodes:
        power = int(node[1:])
        output_value += 2**power * graph.nodes[node]["value"]

    return output_value


def part_1(file_path: str) -> int:
    """
    Read the input file and return the solution.
    """

    graph, output_nodes = read_file(file_path)

    # graph.plot_graph()
    graph.compute_all_nodes()

    return get_output_values(graph, output_nodes)


# --- Part Two ---


def part_2(file_path: str) -> str:
    """
    Read the input file and return the solution.
    """

    wires = {}
    operations = []
    highest_z = "z00"

    # Read the input file
    data = open(file_path).read().split("\n")
    for line in data:
        if ":" in line:
            wire, value = line.split(": ")
            wires[wire] = int(value)
        elif "->" in line:
            op1, op, op2, _, res = line.split(" ")
            operations.append((op1, op, op2, res))
            if res[0] == "z" and int(res[1:]) > int(highest_z[1:]):
                highest_z = res

    # Detect  wrong results
    wrong = set()
    for op1, op, op2, res in operations:
        if res[0] == "z" and op != "XOR" and res != highest_z:
            wrong.add(res)
        if (
            op == "XOR"
            and res[0] not in ["x", "y", "z"]
            and op1[0] not in ["x", "y", "z"]
            and op2[0] not in ["x", "y", "z"]
        ):
            wrong.add(res)
        if op == "AND" and "x00" not in [op1, op2]:
            for subop1, subop, subop2, _ in operations:
                if (res == subop1 or res == subop2) and subop != "OR":
                    wrong.add(res)
        if op == "XOR":
            for subop1, subop, subop2, _ in operations:
                if (res == subop1 or res == subop2) and subop == "OR":
                    wrong.add(res)

    return ",".join(sorted(wrong))
