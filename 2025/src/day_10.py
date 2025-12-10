# Path: 2025/src/day_10.py

"""
--- Day 10: Factory ---
Just across the hall, you find a large factory. Fortunately, the Elves here have plenty of time to decorate. Unfortunately, it's because the factory machines are all offline, and none of the Elves can figure out the initialization procedure.

The Elves do have the manual for the machines, but the section detailing the initialization procedure was eaten by a Shiba Inu. All that remains of the manual are some indicator light diagrams, button wiring schematics, and joltage requirements for each machine.

For example:

[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
The manual describes one machine per line. Each line contains a single indicator light diagram in [square brackets], one or more button wiring schematics in (parentheses), and joltage requirements in {curly braces}.

To start a machine, its indicator lights must match those shown in the diagram, where . means off and # means on. The machine has the number of indicator lights shown, but its indicator lights are all initially off.

So, an indicator light diagram like [.##.] means that the machine has four indicator lights which are initially off and that the goal is to simultaneously configure the first light to be off, the second light to be on, the third to be on, and the fourth to be off.

You can toggle the state of indicator lights by pushing any of the listed buttons. Each button lists which indicator lights it toggles, where 0 means the first light, 1 means the second light, and so on. When you push a button, each listed indicator light either turns on (if it was off) or turns off (if it was on). You have to push each button an integer number of times; there's no such thing as "0.5 presses" (nor can you push a button a negative number of times).

So, a button wiring schematic like (0,3,4) means that each time you push that button, the first, fourth, and fifth indicator lights would all toggle between on and off. If the indicator lights were [#.....], pushing the button would change them to be [...##.] instead.

Because none of the machines are running, the joltage requirements are irrelevant and can be safely ignored.

You can push each button as many times as you like. However, to save on time, you will need to determine the fewest total presses required to correctly configure all indicator lights for all machines in your list.

There are a few ways to correctly configure the first machine:

[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
You could press the first three buttons once each, a total of 3 button presses.
You could press (1,3) once, (2,3) once, and (0,1) twice, a total of 4 button presses.
You could press all of the buttons except (1,3) once each, a total of 5 button presses.
However, the fewest button presses required is 2. One way to do this is by pressing the last two buttons ((0,2) and (0,1)) once each.

The second machine can be configured with as few as 3 button presses:

[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
One way to achieve this is by pressing the last three buttons ((0,4), (0,1,2), and (1,2,3,4)) once each.

The third machine has a total of six indicator lights that need to be configured correctly:

[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
The fewest presses required to correctly configure it is 2; one way to do this is by pressing buttons (0,3,4) and (0,1,2,4,5) once each.

So, the fewest button presses required to correctly configure the indicator lights on all of the machines is 2 + 3 + 2 = 7.

Analyze each machine's indicator light diagram and button wiring schematics. What is the fewest button presses required to correctly configure the indicator lights on all of the machines?

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
All of the machines are starting to come online! Now, it's time to worry about the joltage requirements.

Each machine needs to be configured to exactly the specified joltage levels to function properly. Below the buttons on each machine is a big lever that you can use to switch the buttons from configuring the indicator lights to increasing the joltage levels. (Ignore the indicator light diagrams.)

The machines each have a set of numeric counters tracking its joltage levels, one counter per joltage requirement. The counters are all initially set to zero.

So, joltage requirements like {3,5,4,7} mean that the machine has four counters which are initially 0 and that the goal is to simultaneously configure the first counter to be 3, the second counter to be 5, the third to be 4, and the fourth to be 7.

The button wiring schematics are still relevant: in this new joltage configuration mode, each button now indicates which counters it affects, where 0 means the first counter, 1 means the second counter, and so on. When you push a button, each listed counter is increased by 1.

So, a button wiring schematic like (1,3) means that each time you push that button, the second and fourth counters would each increase by 1. If the current joltage levels were {0,1,2,3}, pushing the button would change them to be {0,2,2,4}.

You can push each button as many times as you like. However, your finger is getting sore from all the button pushing, and so you will need to determine the fewest total presses required to correctly configure each machine's joltage level counters to match the specified joltage requirements.

Consider again the example from before:

[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
Configuring the first machine's counters requires a minimum of 10 button presses. One way to do this is by pressing (3) once, (1,3) three times, (2,3) three times, (0,2) once, and (0,1) twice.

Configuring the second machine's counters requires a minimum of 12 button presses. One way to do this is by pressing (0,2,3,4) twice, (2,3) five times, and (0,1,2) five times.

Configuring the third machine's counters requires a minimum of 11 button presses. One way to do this is by pressing (0,1,2,3,4) five times, (0,1,2,4,5) five times, and (1,2) once.

So, the fewest button presses required to correctly configure the joltage level counters on all of the machines is 10 + 12 + 11 = 33.

Analyze each machine's joltage requirements and button wiring schematics. What is the fewest button presses required to correctly configure the joltage level counters on all of the machines?
"""

# --- Part One ---

from loguru import logger
import re
import z3


class Lights:
    target_lights: list[str]
    current_lights: list[str]
    regex_detection: re.Pattern = re.compile(r"\[([.#]+)\]")

    def __init__(self, target_lights: list[str]):
        self.target_lights = target_lights
        self.current_lights = ["."] * len(target_lights)

    @classmethod
    def from_string(cls, string: str) -> "Lights":
        match = cls.regex_detection.match(string)
        if match is None:
            raise ValueError(f"Invalid input string: {string}")

        return cls(match.group(1))

    def __str__(self) -> str:
        return "".join(self.current_lights)

    def __repr__(self) -> str:
        return f"Lights(current_lights={self.current_lights})"


class Button:
    wiring: list[int]
    regex_detection: re.Pattern = re.compile(r"\(([\d,]+)\)")

    def __init__(self, wiring: list[int]):
        self.wiring = wiring

    @classmethod
    def from_string(cls, string: str) -> list["Button"]:
        matches = cls.regex_detection.findall(string)
        if not matches:
            raise ValueError(f"Invalid input string: {string}")

        return [cls([int(x) for x in match.split(",")]) for match in matches]

    def __str__(self) -> str:
        return f"Button(wiring={self.wiring})"

    def __repr__(self) -> str:
        return f"Button(wiring={self.wiring})"


class Joltage:
    requirements: list[int]
    regex_detection: re.Pattern = re.compile(r"\{([\d,]+)\}")

    def __init__(self, requirements: list[int]):
        self.requirements = requirements

    @classmethod
    def from_string(cls, string: str) -> "Joltage":
        match = cls.regex_detection.search(string)

        if match is None:
            raise ValueError(f"Invalid input string: {string}")

        return cls([int(x) for x in match.group(1).split(",")])

    def __str__(self) -> str:
        return f"Joltage(requirements={self.requirements})"

    def __repr__(self) -> str:
        return f"Joltage(requirements={self.requirements})"


class Machine:
    lights: Lights
    buttons: list[Button]
    joltage: Joltage

    def __init__(self, lights: Lights, buttons: list[Button], joltage: Joltage):
        self.lights = lights
        self.buttons = buttons
        self.joltage = joltage

    @classmethod
    def from_string(cls, string: str) -> "Machine":
        lights = Lights.from_string(string)
        buttons = Button.from_string(string)
        joltage = Joltage.from_string(string)
        return cls(lights, buttons, joltage)

    def __str__(self) -> str:
        return f"Machine(lights={self.lights}, buttons={self.buttons}, joltage={self.joltage})"

    def __repr__(self) -> str:
        return f"Machine(lights={self.lights}, buttons={self.buttons}, joltage={self.joltage})"

    def solve_part_1(self) -> int:
        num_buttons = len(self.buttons)
        num_lights = len(self.lights.current_lights)
        ButtonVars = [z3.Bool(f"button_{i}") for i in range(num_buttons)]

        # Construct a z3 solver
        solver = z3.Optimize()

        # For each light, ensure that after pressing a subset of buttons, the light matches the target
        for idx in range(num_lights):
            # Find which buttons affect this light (buttons that toggle this light)
            affected_buttons = [
                j for j, btn in enumerate(self.buttons) if idx in btn.wiring
            ]

            # Count how many affected buttons are pressed (parity)
            # We need to convert Bool to Int for the sum
            parity_sum = z3.Sum([z3.If(ButtonVars[j], 1, 0) for j in affected_buttons])

            # Determine target state for this light
            target_on = self.lights.target_lights[idx] == "#"

            # Since we start with all lights OFF (current_lights initialized to ".")
            # To get a light ON: need odd number of toggles (parity % 2 == 1)
            # To keep a light OFF: need even number of toggles (parity % 2 == 0)
            if target_on:
                # Need odd parity to turn light ON
                solver.add(parity_sum % 2 == 1)
            else:
                # Need even parity to keep light OFF
                solver.add(parity_sum % 2 == 0)

        # Minimize number of button presses
        total_presses = z3.Sum([z3.If(b, 1, 0) for b in ButtonVars])
        solver.minimize(total_presses)

        if solver.check() == z3.sat:
            model = solver.model()
            presses = sum(bool(model[var]) for var in ButtonVars)
            logger.debug(f"Solved: {presses} presses")
            return presses
        else:
            logger.debug("No solution found using z3 for machine: {}".format(self))
            raise ValueError(f"No solution found for Machine: {self}")

    def solve_part_2(self) -> int:
        num_buttons = len(self.buttons)
        num_counters = len(self.joltage.requirements)

        # Use integer variables for how many times each button is pressed
        ButtonVars = [z3.Int(f"button_{i}") for i in range(num_buttons)]

        # Construct a z3 solver
        solver = z3.Optimize()

        # Each button can be pressed 0 or more times (non-negative)
        for btn_var in ButtonVars:
            solver.add(btn_var >= 0)

        # For each joltage counter, ensure that the sum of button presses equals the requirement
        for i in range(num_counters):
            # Find which buttons affect this counter
            affected_buttons = [
                j for j, btn in enumerate(self.buttons) if i in btn.wiring
            ]
            # Sum up how many times each affected button was pressed
            joltage_sum = z3.Sum([ButtonVars[j] for j in affected_buttons])
            # This sum must equal the joltage requirement
            solver.add(joltage_sum == self.joltage.requirements[i])

        # Minimize total number of button presses
        total_presses = z3.Sum(ButtonVars)
        solver.minimize(total_presses)

        if solver.check() == z3.sat:
            model = solver.model()
            presses = sum(model[var].as_long() for var in ButtonVars)
            logger.debug(f"Solved: {presses} presses")
            return presses
        else:
            logger.debug("No solution found using z3 for machine: {}".format(self))
            raise ValueError(f"No solution found for Machine: {self}")


def part_1(file_path: str) -> int:
    """
    Read the input file and return the solution.
    """

    with open(file_path, "r") as file:
        lines = file.readlines()

    total_presses = 0
    for line in lines:
        logger.debug("--------------------------------")
        logger.debug(line)
        machine = Machine.from_string(line)
        logger.debug(machine)
        total_presses += machine.solve_part_1()
    return total_presses


# --- Part Two ---


def part_2(file_path: str) -> int:
    """
    Read the input file and return the solution.
    """

    with open(file_path, "r") as file:
        lines = file.readlines()

    total_presses = 0
    for line in lines:
        logger.debug("--------------------------------")
        logger.debug(line)
        machine = Machine.from_string(line)
        logger.debug(machine)
        total_presses += machine.solve_part_2()
    return total_presses
