"""
--- Day 5: Print Queue ---
Satisfied with their search on Ceres, the squadron of scholars suggests subsequently scanning the stationery stacks of sub-basement 17.

The North Pole printing department is busier than ever this close to Christmas, and while The Historians continue their search of this historically significant facility, an Elf operating a very familiar printer beckons you over.

The Elf must recognize you, because they waste no time explaining that the new sleigh launch safety manual updates won't print correctly. Failure to update the safety manuals would be dire indeed, so you offer your services.

Safety protocols clearly indicate that new pages for the safety manuals must be printed in a very specific order. The notation X|Y means that if both page number X and page number Y are to be produced as part of an update, page number X must be printed at some point before page number Y.

The Elf has for you both the page ordering rules and the pages to produce in each update (your puzzle input), but can't figure out whether each update has the pages in the right order.

For example:

47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
The first section specifies the page ordering rules, one per line. The first rule, 47|53, means that if an update includes both page number 47 and page number 53, then page number 47 must be printed at some point before page number 53. (47 doesn't necessarily need to be immediately before 53; other pages are allowed to be between them.)

The second section specifies the page numbers of each update. Because most safety manuals are different, the pages needed in the updates are different too. The first update, 75,47,61,53,29, means that the update consists of page numbers 75, 47, 61, 53, and 29.

To get the printers going as soon as possible, start by identifying which updates are already in the right order.

In the above example, the first update (75,47,61,53,29) is in the right order:

75 is correctly first because there are rules that put each other page after it: 75|47, 75|61, 75|53, and 75|29.
47 is correctly second because 75 must be before it (75|47) and every other page must be after it according to 47|61, 47|53, and 47|29.
61 is correctly in the middle because 75 and 47 are before it (75|61 and 47|61) and 53 and 29 are after it (61|53 and 61|29).
53 is correctly fourth because it is before page number 29 (53|29).
29 is the only page left and so is correctly last.
Because the first update does not include some page numbers, the ordering rules involving those missing page numbers are ignored.

The second and third updates are also in the correct order according to the rules. Like the first update, they also do not include every page number, and so only some of the ordering rules apply - within each update, the ordering rules that involve missing page numbers are not used.

The fourth update, 75,97,47,61,53, is not in the correct order: it would print 75 before 97, which violates the rule 97|75.

The fifth update, 61,13,29, is also not in the correct order, since it breaks the rule 29|13.

The last update, 97,13,75,29,47, is not in the correct order due to breaking several rules.

For some reason, the Elves also need to know the middle page number of each update being printed. Because you are currently only printing the correctly-ordered updates, you will need to find the middle page number of each correctly-ordered update. In the above example, the correctly-ordered updates are:

75,47,61,53,29
97,61,53,29,13
75,29,13
These have middle page numbers of 61, 53, and 29 respectively. Adding these page numbers together gives 143.

Of course, you'll need to be careful: the actual list of page ordering rules is bigger and more complicated than the above example.

Determine which updates are already in the correct order. What do you get if you add up the middle page number from those correctly-ordered updates?

--- Part Two ---
While the Elves get to work printing the correctly-ordered updates, you have a little time to fix the rest of them.

For each of the incorrectly-ordered updates, use the page ordering rules to put the page numbers in the right order. For the above example, here are the three incorrectly-ordered updates and their correct orderings:

75,97,47,61,53 becomes 97,75,47,61,53.
61,13,29 becomes 61,29,13.
97,13,75,29,47 becomes 97,75,47,29,13.
After taking only the incorrectly-ordered updates and ordering them correctly, their middle page numbers are 47, 29, and 47. Adding these together produces 123.

Find the updates which are not in the correct order. What do you get if you add up the middle page numbers after correctly ordering just those updates?
"""

from loguru import logger


class Rule:
    first: int
    second: int

    @classmethod
    def from_str(cls, s: str) -> "Rule":
        values = s.split("|")
        return cls(int(values[0]), int(values[1]))

    def __init__(self, first: int, second: int):
        self.first = first
        self.second = second

    def check_order(self, update: "Update") -> bool:
        if self.first in update.pages and self.second in update.pages:
            if update.pages.index(self.first) < update.pages.index(self.second):
                return True
            else:
                return False
        else:
            return True

    def __str__(self) -> str:
        return f"{self.first}|{self.second}"


class Update:
    pages: list[int]

    @classmethod
    def from_str(cls, s: str) -> "Update":
        return cls([int(page) for page in s.split(",")])

    def __init__(self, pages: list[int]):
        self.pages = pages

    def __str__(self) -> str:
        return ",".join([str(page) for page in self.pages])

    def validate_order(self, rules: list[Rule]) -> bool:
        for rule in rules:
            if not rule.check_order(self):
                return False
        return True

    def remove(self, value: int) -> int:
        """
        Remove the first instance of a value from the list.
        """
        self.pages.remove(value)
        return value

    def re_order(self, rules: list[Rule]) -> "Update":
        if self.validate_order(rules):
            return self
        # starting length of the update
        length = len(self.pages)

        # isolate appropriate rules
        update_rules = filter_rules(rules, self)

        # find value to extract
        lower_bound = find_rule_lower_bound(update_rules)
        # re-order the update
        ordered_list = [self.remove(lower_bound)]

        while not len(ordered_list) == length:
            update_rules = filter_rules(rules, self)
            lower_bound = find_rule_lower_bound(update_rules)
            ordered_list.append(self.remove(lower_bound))

            if len(self.pages) == 1:
                ordered_list.append(self.pages[0])
                break

        ordered_update = Update(ordered_list)

        assert ordered_update.validate_order(rules)

        return ordered_update


def read_input(file_path: str) -> tuple[list[Rule], list[Update]]:
    """
    Reads the input file and returns the rules and updates.
    """
    rules = []
    updates = []
    with open(file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            if "|" in line:
                rules.append(Rule.from_str(line.strip()))
            elif "," in line:
                updates.append(Update.from_str(line.strip()))

    logger.debug(f"Read {len(rules)} rules and {len(updates)} updates.")
    return rules, updates


def part_1(file_path: str) -> int:
    """
    Determine which updates are already in the correct order.
    Returns the sum of the middle page number from those correctly-ordered updates.
    """
    rules, updates = read_input(file_path)

    correct_updates = []
    for update in updates:
        correct = update.validate_order(rules)
        if correct:
            correct_updates.append(update)

    logger.debug(f"Found {len(correct_updates)} correct updates.")

    middle_pages = []
    for update in correct_updates:
        middle_pages.append(update.pages[len(update.pages) // 2])

    return sum(middle_pages)


def filter_rules(rules: list[Rule], update: Update) -> list[Rule]:
    """
    Filter the rules that apply to the update.
    """
    return [
        rule
        for rule in rules
        if rule.first in update.pages and rule.second in update.pages
    ]


def find_rule_lower_bound(rules: list[Rule]) -> int:
    """
    Find the number that only appears as the first number in the rules.
    """
    first_numbers = {rule.first for rule in rules}
    second_numbers = {rule.second for rule in rules}

    for number in first_numbers:
        if number not in second_numbers:
            return number

    raise ValueError("No lower bound found.")


def part_2(file_path: str) -> int:
    """
    Find the updates which are not in the correct order.
    Returns the sum of the middle page numbers after correctly ordering just those updates.
    """

    rules, updates = read_input(file_path)

    middle_pages = []

    for update in updates:
        # check if the update is in the correct order
        if update.validate_order(rules):
            continue

        # re-order the update
        re_ordered_update = update.re_order(rules)

        middle_pages.append(re_ordered_update.pages[len(re_ordered_update.pages) // 2])

    return sum(middle_pages)
