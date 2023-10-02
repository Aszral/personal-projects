from commands import Command, Op
from heap import Heap
import memory_block
import algorithms
import os


def read_data(path: str) -> tuple[int, list[str]]:
    with open(path, "r") as file:
        size: int = int(file.readline())
        cmds: list[str] = file.readlines()[0:]
        return size, cmds


def main():
    path: str = "instructions"
    algos: list[tuple[str, algorithms.Algorithm]] = [
        ("First Fit", algorithms.first_fit),
        ("Best Fit", algorithms.best_fit),
        ("Worst Fit", algorithms.worst_fit),
    ]

    size, data = read_data(path + ".in")
    cmds: list[Command] = [Command.from_str(line) for line in data]
    out: str = ""

    for algo_name, algo in algos:
        heap = Heap(algo, memory_block.Size(size))
        for cmd in cmds:
            if cmd.op == Op.Alloc:
                heap.allocate(cmd.get_id(), cmd.get_size())
            elif cmd.op == Op.Dealloc:
                heap.deallocate(cmd.get_id())
            elif cmd.op == Op.Compact:
                heap.compact()
            elif cmd.op == Op.Output:
                heap.output(path)
        out: str = str(heap)
        with open(path + ".out", "a") as file:
            file.write(out)


if __name__ == "__main__":
    main()
