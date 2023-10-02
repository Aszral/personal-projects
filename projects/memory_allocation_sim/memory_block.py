from dataclasses import dataclass
from typing import NewType

Id = NewType("Id", int)
Free = Id(-1)
Used = NewType("UsedId", Id)
Address = NewType("Address", int)
Size = NewType("Size", int)


@dataclass
class MemoryBlock:
    id: Id
    size: Size
    start_address: Address
    end_address: Address

    # Handles new free blocks.
    @staticmethod
    def new_free(size: Size, start_address: Address) -> "MemoryBlock":
        return MemoryBlock(Free, size, start_address, Address(start_address + size - 1))

    # Handles new but used blocks.
    @staticmethod
    def new_used(id: Id, size: Size, start_address: Address) -> "MemoryBlock":
        return MemoryBlock(id, size, start_address, Address(start_address + size - 1))

    def is_free(self) -> bool:
        return self.id == Free

    def is_used(self) -> bool:
        return not self.is_free()

    def as_free(self) -> "MemoryBlock":
        return MemoryBlock.new_free(self.size, self.start_address)

    def can_merge(self, other: "MemoryBlock") -> bool:
        return (
            self.is_free()
            and other.is_free()
            and (
                self.start_address == other.end_address + 1
                or other.start_address == self.end_address + 1
            )
        )

    def merge(self, other: "MemoryBlock") -> "MemoryBlock":
        if not self.can_merge(other):
            raise ValueError("Cannot merge blocks")
        start_address: int = min(self.start_address, other.start_address)
        end_address: int = max(self.end_address, other.end_address)
        return MemoryBlock.new_free(
            Size(end_address - start_address + 1), start_address
        )
