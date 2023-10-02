from enum import Enum
from typing import Optional
from dataclasses import dataclass

from memory_block import Id, Size


class Op(Enum):
    Alloc = "A"
    Dealloc = "D"
    Compact = "C"
    Output = "O"


@dataclass
class Command:
    op: Op
    id: Optional[int]
    size: Optional[int]

    def __init__(
        self, op: Op, id: Optional[int] = None, size: Optional[int] = None
    ) -> None:
        self.op = op
        self.id = id
        self.size = size

    @staticmethod
    def from_str(line: str) -> "Command":
        parts: list[str] = [line[0]]

        if ";" in line:
            parts = line.split(";")
        match parts[0]:
            case "A":
                return Command(Op.Alloc, int(parts[1]), int(parts[2]))
            case "D":
                return Command(Op.Dealloc, int(parts[1]))
            case "C":
                return Command(Op.Compact)
            case "O":
                return Command(Op.Output)
            case _:
                raise ValueError("ERROR: Invalid Command")

    def get_id(self) -> Id:
        if self.id is None:
            raise ValueError("ERROR: Invalid Command")
        return Id(self.id)

    def get_size(self) -> Size:
        if self.size is None:
            raise ValueError("ERROR: Invalid Command")
        return Size(self.size)
