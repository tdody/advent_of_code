"""
--- Day 9: Disk Fragmenter ---
Another push of the button leaves you in the familiar hallways of some friendly amphipods! Good thing you each somehow got your own personal mini submarine. The Historians jet away in search of the Chief, mostly by driving directly into walls.

While The Historians quickly figure out how to pilot these things, you notice an amphipod in the corner struggling with his computer. He's trying to make more contiguous free space by compacting all of the files, but his program isn't working; you offer to help.

He shows you the disk map (your puzzle input) he's already generated. For example:

2333133121414131402
The disk map uses a dense format to represent the layout of files and free space on the disk. The digits alternate between indicating the length of a file and the length of free space.

So, a disk map like 12345 would represent a one-block file, two blocks of free space, a three-block file, four blocks of free space, and then a five-block file. A disk map like 90909 would represent three nine-block files in a row (with no free space between them).

Each file on disk also has an ID number based on the order of the files as they appear before they are rearranged, starting with ID 0. So, the disk map 12345 has three files: a one-block file with ID 0, a three-block file with ID 1, and a five-block file with ID 2. Using one character for each block where digits are the file ID and . is free space, the disk map 12345 represents these individual blocks:

0..111....22222
The first example above, 2333133121414131402, represents these individual blocks:

00...111...2...333.44.5555.6666.777.888899
The amphipod would like to move file blocks one at a time from the end of the disk to the leftmost free space block (until there are no gaps remaining between file blocks). For the disk map 12345, the process looks like this:

0..111....22222
02.111....2222.
022111....222..
0221112...22...
02211122..2....
022111222......
The first example requires a few more steps:

00...111...2...333.44.5555.6666.777.888899
009..111...2...333.44.5555.6666.777.88889.
0099.111...2...333.44.5555.6666.777.8888..
00998111...2...333.44.5555.6666.777.888...
009981118..2...333.44.5555.6666.777.88....
0099811188.2...333.44.5555.6666.777.8.....
009981118882...333.44.5555.6666.777.......
0099811188827..333.44.5555.6666.77........
00998111888277.333.44.5555.6666.7.........
009981118882777333.44.5555.6666...........
009981118882777333644.5555.666............
00998111888277733364465555.66.............
0099811188827773336446555566..............
The final step of this file-compacting process is to update the filesystem checksum. To calculate the checksum, add up the result of multiplying each of these blocks' position with the file ID number it contains. The leftmost block is in position 0. If a block contains free space, skip it instead.

Continuing the first example, the first few blocks' position multiplied by its file ID number are 0 * 0 = 0, 1 * 0 = 0, 2 * 9 = 18, 3 * 9 = 27, 4 * 8 = 32, and so on. In this example, the checksum is the sum of these, 1928.

Compact the amphipod's hard drive using the process he requested. What is the resulting filesystem checksum? (Be careful copy/pasting the input for this puzzle; it is a single, very long line.)
"""

# Path: src/day_9.py
# --- Part One ---


def load_disk_map(document_path: str) -> str:
    """
    Read the document and return the content as a string.
    """
    return open(document_path).read().strip()


class FreeSpaceQueue:
    def __init__(self):
        self.stack_dict = {k: [] for k in range(1, 10)}
        self.stack_priority = list(range(1, 10))

    def update_priority(self):
        self.stack_priority = sorted(
            [k for k in self.stack_dict if len(self.stack_dict[k]) > 0],
            key=lambda k: self.stack_dict[k][0][0],
        )

    def push(self, index_block: list[int], sort=False):
        if len(index_block) > 0:
            self.stack_dict[len(index_block)].append(index_block)
            if sort:
                self.stack_dict[len(index_block)].sort(key=lambda b: b[0])
            self.update_priority()

    def pop(self, file_index_block: list[int]) -> list[int] | None:
        index_block = None
        for k in self.stack_priority:
            if (
                k >= len(file_index_block)
                and self.stack_dict[k][0][0] < file_index_block[0]
            ):
                index_block = self.stack_dict[k].pop(0)
                break
        if index_block is not None:
            if len(index_block) > len(file_index_block):
                new_block = index_block[len(file_index_block) :]
                self.push(new_block, sort=True)
            else:
                self.update_priority()
        return index_block


def parse_disk(disk_map: str) -> tuple[list[int], FreeSpaceQueue, list[str]]:
    free_space_locs, free_space_queue, file = [], FreeSpaceQueue(), []  # type:ignore
    for k, char in enumerate(disk_map):
        start_ix = len(file)
        if k % 2 == 0:
            file.extend([f"{k // 2}"] * int(char))
        else:
            file.extend(["."] * int(char))
            free_space_locs.extend(range(start_ix, len(file)))
            free_space_queue.push(list(range(start_ix, len(file))))
    return free_space_locs, free_space_queue, file


def rearrange_file(free_space_locs: list[int], file: list[str]) -> list[str]:
    """
    Rearrange the file by moving the file blocks to the leftmost free space block.
    """
    for k in range(len(file) - 1, 0, -1):
        if (k > free_space_locs[0]) and file[k] != ".":
            new_mem_ix = free_space_locs.pop(0)
            file[k], file[new_mem_ix] = file[new_mem_ix], file[k]
            free_space_locs.append(k)
    return file


def rearrange_file_by_blocks(
    free_space_queue: FreeSpaceQueue, file: list[str]
) -> list[str]:
    file_blocks, index_blocks = [], []
    cur_block, curr_ix_block = [file[0]], [0]
    for k in range(1, len(file)):
        if file[k] == cur_block[-1]:
            cur_block.append(file[k])
            curr_ix_block.append(k)
        else:
            file_blocks.append(cur_block)
            index_blocks.append(curr_ix_block)
            cur_block, curr_ix_block = [file[k]], [k]
    if cur_block[0] != file_blocks[0][0]:
        file_blocks.append(cur_block)
        index_blocks.append(curr_ix_block)
    for file_bk, ix_bk in zip(file_blocks[::-1], index_blocks[::-1]):
        if file_bk[0] != ".":
            free_bk = free_space_queue.pop(ix_bk)
            if free_bk:
                ix1, ix2, ix3, ix4 = (
                    free_bk[0],
                    free_bk[0] + len(ix_bk),
                    ix_bk[0],
                    ix_bk[-1] + 1,
                )
                file[ix1:ix2], file[ix3:ix4] = (
                    file[ix3:ix4],
                    file[ix1:ix2],
                )
    return file


def file_system_checksum(file: list[str]) -> int:
    return sum(k * int(chr) for k, chr in enumerate(file) if chr.isdigit())


def part_1(file_path: str) -> int:
    """
    Fragment the disk and break blocks.
    """

    disk_map = load_disk_map(file_path)
    free_space_locs, _, file = parse_disk(disk_map)
    ordered_file = rearrange_file(free_space_locs, list(file))
    return file_system_checksum(ordered_file)


# --- Part Two ---


def part_2(file_path: str) -> int:
    """
    Fragment the disk and optimize for blocks.
    """

    disk_map = load_disk_map(file_path)
    _, free_blocks, file = parse_disk(disk_map)
    ordered_file_by_blocks = rearrange_file_by_blocks(free_blocks, file)
    return file_system_checksum(ordered_file_by_blocks)
