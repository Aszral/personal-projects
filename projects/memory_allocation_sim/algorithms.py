from typing import Callable, Optional
import memory_block
from memory_block import Size

Algorithm = Callable[[memory_block.Size, list[memory_block.MemoryBlock]], Optional[int]]
"""
Algorithm is a function that takes in:

- Size   : The size of the memory block to be allocated
- Blocks : A list of memory blocks in the heap

Returns the index of the memory block to be allocated or None if no suitable block is found.
"""


def first_fit(size: Size, blocks: list[memory_block.MemoryBlock]) -> Optional[int]:
    """
    Iterate through the list of blocks and return the index of:
        - First block that is large enough to fit the given size.
    """
    blocks.sort(key=lambda x: x.start_address)
    for i, block in enumerate(blocks):
        if block.is_free() and block.size >= size:
            return i
    return None


def best_fit(size: Size, blocks: list[memory_block.MemoryBlock]) -> Optional[int]:
    """
    Iterate through the list of blocks and return the index of:
        - The smallest block that is large enough to fit the given size.
    """
    blocks.sort(key=lambda x: x.start_address)
    best_idx: Optional[int] = None
    for i, block in enumerate(blocks):
        if block.is_free() and block.size >= size:
            if best_idx is None or block.size < blocks[best_idx].size:
                best_idx = i
    return best_idx


def worst_fit(size: Size, blocks: list[memory_block.MemoryBlock]) -> Optional[int]:
    """
    Iterate through the list of blocks and return the index of:
        - The largest block that is large enough to fit the given size.
    """
    blocks.sort(key=lambda x: x.start_address)
    worst_address: Optional[int] = None
    for i, block in enumerate(blocks):
        if block.is_free() and block.size >= size:
            if worst_address is None or block.size > blocks[worst_address].size:
                worst_address = i
    return worst_address
