"""
--- Day 17: Chronospatial Computer ---
The Historians push the button on their strange device, but this time, you all just feel like you're falling.

"Situation critical", the device announces in a familiar voice. "Bootstrapping process failed. Initializing debugger...."

The small handheld device suddenly unfolds into an entire computer! The Historians look around nervously before one of them tosses it to you.

This seems to be a 3-bit computer: its program is a list of 3-bit numbers (0 through 7), like 0,1,2,3. The computer also has three registers named A, B, and C, but these registers aren't limited to 3 bits and can instead hold any integer.

The computer knows eight instructions, each identified by a 3-bit number (called the instruction's opcode). Each instruction also reads the 3-bit number after it as an input; this is called its operand.

A number called the instruction pointer identifies the position in the program from which the next opcode will be read; it starts at 0, pointing at the first 3-bit number in the program. Except for jump instructions, the instruction pointer increases by 2 after each instruction is processed (to move past the instruction's opcode and its operand). If the computer tries to read an opcode past the end of the program, it instead halts.

So, the program 0,1,2,3 would run the instruction whose opcode is 0 and pass it the operand 1, then run the instruction having opcode 2 and pass it the operand 3, then halt.

There are two types of operands; each instruction specifies the type of its operand. The value of a literal operand is the operand itself. For example, the value of the literal operand 7 is the number 7. The value of a combo operand can be found as follows:

Combo operands 0 through 3 represent literal values 0 through 3.
Combo operand 4 represents the value of register A.
Combo operand 5 represents the value of register B.
Combo operand 6 represents the value of register C.
Combo operand 7 is reserved and will not appear in valid programs.
The eight instructions are as follows:

The adv instruction (opcode 0) performs division. The numerator is the value in the A register. The denominator is found by raising 2 to the power of the instruction's combo operand. (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.) The result of the division operation is truncated to an integer and then written to the A register.

The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand, then stores the result in register B.

The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3 bits), then writes that value to the B register.

The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero, it jumps by setting the instruction pointer to the value of its literal operand; if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.

The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)

The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value. (If a program outputs multiple values, they are separated by commas.)

The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored in the B register. (The numerator is still read from the A register.)

The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in the C register. (The numerator is still read from the A register.)

Here are some examples of instruction operation:

If register C contains 9, the program 2,6 would set register B to 1.
If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
If register B contains 29, the program 1,7 would set register B to 26.
If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354.
The Historians' strange device has finished initializing its debugger and is displaying some information about the program it is trying to run (your puzzle input). For example:

Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
Your first task is to determine what the program is trying to output. To do this, initialize the registers to the given values, then run the given program, collecting any output produced by out instructions. (Always join the values produced by out instructions with commas.) After the above program halts, its final output will be 4,6,3,5,6,3,5,2,1,0.

Using the information provided by the debugger, initialize the registers to the given values, then run the program. Once it halts, what do you get if you use commas to join the values it output into a single string?


--- Part Two ---
Digging deeper in the device's manual, you discover the problem: this program is supposed to output another copy of the program! Unfortunately, the value in register A seems to have been corrupted. You'll need to find a new value to which you can initialize register A so that the program's output instructions produce an exact copy of the program itself.

For example:

Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
This program outputs a copy of itself if register A is instead initialized to 117440. (The original initial value of register A, 2024, is ignored.)

What is the lowest positive initial value for register A that causes the program to output a copy of itself?


"""

# Path: src/day_17.py
# --- Part One ---

from abc import abstractmethod

from loguru import logger
from tqdm import tqdm


def oct_to_dec(oct: str) -> int:
    return int(oct, 8)


def dec_to_oct(dec: int) -> str:
    return format(dec, "o")


class Register:
    value: int

    def __init__(self, value: int) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f"Register({self.value})"

    def __str__(self) -> str:
        return f"{self.value}"


class Program:
    instructions: list[int]

    def __init__(self, instructions: list[int]) -> None:
        self.instructions = instructions

    def __repr__(self) -> str:
        return f"Program({self.instructions})"

    @classmethod
    def from_str(cls, instructions: str) -> "Program":
        instructions = instructions.replace("Program: ", "")
        return cls([int(i) for i in instructions.split(",")])


class Combo:
    value: int

    def __init__(self, value: int) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f"Combo({self.value})"

    def get_value(self, registers: dict[str, Register]) -> int:
        if self.value <= 3:
            return self.value
        elif self.value == 4:
            return registers["A"].value
        elif self.value == 5:
            return registers["B"].value
        elif self.value == 6:
            return registers["C"].value
        else:
            raise ValueError(f"Invalid combo value: {self.value}")


class Instruction:
    name: str

    def __init__(
        self,
    ):
        pass

    @abstractmethod
    def compute(
        self, registers: dict[str, Register], combo: int, output: list[str]
    ) -> tuple[int, list[str]]:
        raise NotImplementedError


class ADV(Instruction):
    name = "adv"

    def compute(
        self, registers: dict[str, Register], combo: int, output: list[str]
    ) -> tuple[int, list[str]]:
        a_value = registers["A"].value
        combo_value = Combo(combo).get_value(registers)

        registers["A"].value = int(a_value // (2**combo_value))
        logger.debug(
            f"ADV: {a_value} // (2**{combo_value}) = {registers['A'].value} -> A"
        )
        return 2, output


class BXL(Instruction):
    name = "bxl"

    def compute(
        self, registers: dict[str, Register], combo: int, output: list[str]
    ) -> tuple[int, list[str]]:
        b_value = registers["B"].value
        registers["B"].value = b_value ^ combo
        logger.debug(f"BXL: {b_value} ^ {combo} = {registers['B'].value} -> B")
        return 2, output


class BST(Instruction):
    name = "bst"

    def compute(
        self, registers: dict[str, Register], combo: int, output: list[str]
    ) -> tuple[int, list[str]]:
        start_value = Combo(combo).get_value(registers)
        new_value = Combo(combo).get_value(registers) % 8
        registers["B"].value = new_value
        logger.debug(f"BST: {start_value} % 8 =  {new_value} -> B")
        return 2, output


class JNZ(Instruction):
    name = "jnz"

    def compute(
        self, registers: dict[str, Register], combo: int, output: list[str]
    ) -> tuple[int, list[str]]:
        logger.debug(f"JNZ: {registers['A'].value}")
        if registers["A"].value != 0:
            return combo, output
        return 2, output


class BXC(Instruction):
    name = "bxc"

    def compute(
        self, registers: dict[str, Register], combo: int, output: list[str]
    ) -> tuple[int, list[str]]:
        b_value = registers["B"].value
        c_value = registers["C"].value
        registers["B"].value = b_value ^ c_value
        logger.debug(f"BXC: {b_value} ^ {c_value} = {registers['B'].value} -> B")
        return 2, output


class OUT(Instruction):
    name = "out"

    def compute(
        self, registers: dict[str, Register], combo: int, output: list[str]
    ) -> tuple[int, list[str]]:
        start_value = Combo(combo).get_value(registers)
        new_value = start_value % 8
        output.append(str(new_value))
        logger.debug(f"OUT: {start_value} % 8 = {new_value}")
        return 2, output


class BDV(Instruction):
    name = "bdv"

    def compute(
        self, registers: dict[str, Register], combo: int, output: list[str]
    ) -> tuple[int, list[str]]:
        a_value = registers["A"].value
        combo_value = Combo(combo).get_value(registers)
        registers["B"].value = int(a_value // (2**combo_value))
        logger.debug(
            f"BDV: {a_value} // (2**{combo_value}) = {registers['B'].value} -> B"
        )
        return 2, output


class CDV(Instruction):
    name = "cdv"

    def compute(
        self, registers: dict[str, Register], combo: int, output: list[str]
    ) -> tuple[int, list[str]]:
        a_value = registers["A"].value
        combo_value = Combo(combo).get_value(registers)
        registers["C"].value = int(a_value // (2**combo_value))
        logger.debug(
            f"CDV: {a_value} // (2**{combo_value}) = {registers['C'].value} -> C"
        )
        return 2, output


def read_input(file_path: str) -> tuple[dict[str, Register], Program]:
    with open(file_path, "r") as file:
        lines = file.readlines()

    registers = {
        "A": Register(int(lines[0].split(": ")[1])),
        "B": Register(int(lines[1].split(": ")[1])),
        "C": Register(int(lines[2].split(": ")[1])),
    }

    program = Program.from_str(lines[4])

    return registers, program


def run_instructions(registers: dict[str, Register], program: Program) -> list[str]:
    output: list[str] = []
    instructions: dict[int, Instruction] = {
        0: ADV(),
        1: BXL(),
        2: BST(),
        3: JNZ(),
        4: BXC(),
        5: OUT(),
        6: BDV(),
        7: CDV(),
    }

    instruction_pointer = 0
    while instruction_pointer < len(program.instructions):
        opcode = program.instructions[instruction_pointer]
        combo = program.instructions[instruction_pointer + 1]
        instruction = instructions[opcode]
        logger.debug(f"Instruction: {instruction.name} {combo}")
        jump, output = instruction.compute(registers, combo, output)
        logger.debug(f"\tRegisters: {registers}")
        logger.debug(f"\tJump: {jump}")

        if jump == 2:
            instruction_pointer += 2
        else:
            instruction_pointer = jump

    return output


def test_suite():
    """
    If register C contains 9, the program 2,6 would set register B to 1.
    If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
    If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
    If register B contains 29, the program 1,7 would set register B to 26.
    If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354.
    """

    registers = {
        "A": Register(0),
        "B": Register(0),
        "C": Register(9),
    }
    program = Program([2, 6])
    output = run_instructions(registers, program)
    assert registers["B"].value == 1

    registers = {
        "A": Register(10),
        "B": Register(0),
        "C": Register(0),
    }
    program = Program([5, 0, 5, 1, 5, 4])
    output = run_instructions(registers, program)
    logger.debug(output)
    assert output == [0, 1, 2]

    registers = {
        "A": Register(2024),
        "B": Register(0),
        "C": Register(0),
    }
    program = Program([0, 1, 5, 4, 3, 0])
    output = run_instructions(registers, program)
    assert output == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]
    assert registers["A"].value == 0

    registers = {
        "A": Register(0),
        "B": Register(29),
        "C": Register(0),
    }
    program = Program([1, 7])
    output = run_instructions(registers, program)
    assert registers["B"].value == 26

    registers = {
        "A": Register(0),
        "B": Register(2024),
        "C": Register(43690),
    }
    program = Program([4, 0])
    output = run_instructions(registers, program)
    assert registers["B"].value == 44354


def part_1(file_path: str) -> int:
    """
    Read the input file and return the solution.
    """

    registers, program = read_input(file_path)
    output = run_instructions(registers, program)
    print(",".join([str(i) for i in output]))
    return int("".join([str(i) for i in output]))


# --- Part Two ---


def part_2(file_path: str) -> int:
    """
    Read the input file and return the solution.
    """

    # Read the input file
    registers, program = read_input(file_path)
    # Store the program instructions as the desired output
    output = program.instructions

    # Find the lowest positive initial value for register A that causes the program to output a copy of itself
    # We will start from the end of the output and find the value of A that produces the output
    lower_bound = 0
    # We will iterate over the output in reverse order
    for i in tqdm(range(len(output) - 1, -1, -1)):
        # We will iterate over the possible values of A
        for a in tqdm(
            range(lower_bound, lower_bound + (8 ** (len(output) - i))), leave=False
        ):
            # Set the value of A
            registers["A"].value = a
            # Run the program
            new_output = run_instructions(registers, program)
            # If the output is the same as the current output
            if new_output == output[i:]:
                if len(new_output) == len(output):
                    # If the output is the same as the original output
                    return a

                a_base_8 = dec_to_oct(a)
                lower_bound = oct_to_dec(a_base_8 + "0")
                break

    return -1


if __name__ == "__main__":
    test_suite()
