import bisect
from dataclasses import dataclass
from typing import Optional, Dict
from memory_block import Address, Id, Size, MemoryBlock
from algorithms import Algorithm, first_fit, best_fit, worst_fit


@dataclass
class OperationResult:
    operation: Optional[str]
    instruction_count: Optional[int]
    data: Optional[str]

    @staticmethod
    def ok():
        return OperationResult(None, None, None)

    @staticmethod
    def allocation_error(count: int, max_free_block_size: int):
        return OperationResult("A", count, str(max_free_block_size))

    @staticmethod
    def deallocation_error(count: int, reason: str):
        return OperationResult("D", count, reason)

    def __str__(self):
        match self.operation, self.instruction_count, self.data:
            case op, count, data:
                return f"{op};{count};{data}"
            case _:
                return ""


@dataclass
class Heap:
    size: Size
    blocks: list[MemoryBlock]
    instruction_count: int
    errors: list[str]
    algo: Algorithm
    output_cnt: int
    allocation_attempts: Dict[Id, bool]

    def __init__(self, algo: Algorithm, size: Size):
        self.size = size
        self.instruction_count = 1
        self.output_cnt = 0
        self.errors = []
        self.blocks = [MemoryBlock.new_free(size, Address(0))]
        self.algo = algo
        self.allocation_attempts = {}

    def free_block(self, block: MemoryBlock) -> None:
        for i, b in list(enumerate(self.blocks)):
            if block.can_merge(b):
                new_block = block.merge(self.blocks.pop(i))
                self.blocks.append(new_block)

    def __max_free_block_size(self) -> int:
        return max([b.size if b.is_free() else 0 for b in self.blocks])

    def allocate(self, id: Id, size: Size) -> None:
        self.instruction_count += 1
        block_idx: Optional[int] = self.algo(size, self.blocks)

        if block_idx is None:
            res = OperationResult.allocation_error(
                self.instruction_count - 1, self.__max_free_block_size()
            )
            self.errors.append(str(res))
            self.allocation_attempts[id] = False  # set to false when alloc fails
            return

        block = self.blocks.pop(block_idx)

        if block.size > size:
            self.blocks.append(
                MemoryBlock.new_free(
                    Size(block.size - size), Address(block.start_address + size)
                )
            )
            self.blocks.append(
                MemoryBlock.new_used(id, Size(size), Address(block.start_address))
            )
        elif block.size == size:
            self.blocks.append(
                MemoryBlock.new_used(id, Size(size), Address(block.start_address))
            )

        self.allocation_attempts[id] = True  # set to true when alloc succeeds

    def deallocate(self, id: Id) -> None:
        self.instruction_count += 1
        for i, block in enumerate(self.blocks):
            if block.id == id:
                self.blocks.remove(block)
                new_block = MemoryBlock.new_free(block.size, block.start_address)

                adjacent_blocks = [b for b in self.blocks if b.can_merge(new_block)]

                for adjacent_block in adjacent_blocks:
                    self.blocks.remove(adjacent_block)
                    new_block = new_block.merge(adjacent_block)
                self.blocks.append(new_block)

                return

        reason = "1" if self.allocation_attempts.get(id) == False else "0"
        res = OperationResult.deallocation_error(self.instruction_count - 1, reason)
        self.errors.append(str(res))
        self.blocks.sort(key=lambda b: b.start_address)

    def compact(self) -> None:
        self.instruction_count += 1
        self.blocks.sort(key=lambda x: x.start_address)

        free_memory = sum([b.size for b in self.blocks if b.is_free()])
        used_blocks = [b for b in self.blocks if b.is_used()]

        compacted_blocks = []
        offset: int = 0
        for block in used_blocks:
            new_block = MemoryBlock.new_used(block.id, block.size, Address(offset))
            compacted_blocks.append(new_block)
            offset += block.size

        compacted_blocks.append(
            MemoryBlock.new_free(Size(free_memory), Address(offset))
        )

        self.blocks = compacted_blocks

    def output(self, path: str) -> None:
        self.instruction_count += 1
        self.output_cnt += 1
        output = str(self)

        with open(f"{path}.out{self.output_cnt}", "a") as f:
            f.write(output)

    def __str__(self) -> str:
        out: str = ""
        if self.algo == first_fit:
            out += "First fit:"
        elif self.algo == best_fit:
            out += "Best fit:"
        elif self.algo == worst_fit:
            out += "Worst fit:"

        allocated_blocks: list[MemoryBlock] = [b for b in self.blocks if b.is_used()]
        # allocated_blocks.sort(key=lambda x: x.start_address)
        allocated_blocks.sort(key=lambda x: x.id)

        free_blocks: list[MemoryBlock] = [b for b in self.blocks if b.is_free()]
        free_blocks.sort(key=lambda x: x.start_address)

        free_memory: int = sum([b.size for b in self.blocks if b.is_free()])

        fragmentation: float = 1 - (
            max(b.size for b in self.blocks if b.is_free()) / free_memory
        )

        errors = "\n".join(self.errors)

        out += "\nAllocated Blocks:\n"
        out += "\n".join(
            f"{b.id};{b.start_address};{b.end_address}" for b in allocated_blocks
        )
        out += "\nFree Blocks:\n"
        out += "\n".join(f"{b.start_address};{b.end_address}" for b in free_blocks)
        out += f"\nFragmentation:\n{format(fragmentation, '.6f')}\n"

        if self.errors:
            errors = "\n".join(self.errors)
            out += f"Errors:\n{errors}\n"
        else:
            out += "Errors:\nNone\n"

        out += "\n"

        return out
