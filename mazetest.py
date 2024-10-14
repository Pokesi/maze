import cProfile
import os
import pstats
import time
import unittest
from typing import Callable

from memory_profiler import profile  # type: ignore

import periphery
from bfs import A, B

NANOSECOND_DIVISOR = 1000000000


class TestMazeGeneration(unittest.TestCase):
    impl: Callable[[list[str]], list[str]] = A

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.mazes = periphery.load_mazes()
        self.impl = A if globals()["a_or_b"] == "A" else B

    def test_duration(self):
        mazes = self.mazes
        start = time.monotonic_ns()
        for maze in mazes:
            self.impl(maze)
        end = time.monotonic_ns()
        print(f"Time taken: {(end - start) / NANOSECOND_DIVISOR} seconds")
        print(f"Average time per maze: {(end - start) / NANOSECOND_DIVISOR / len(mazes)} seconds")

    def test_cprofile(self):
        mazes = self.mazes

        def test_func():
            for maze in mazes:
                self.impl(maze)

        cProfile.runctx(
            "test_func()",
            globals(),
            locals(),
            filename=f"{self.impl.__name__}_cprofile.prof",
        )
        stats = pstats.Stats(f"{self.impl.__name__}_cprofile.prof")
        total_calls = sum(stat[0] for stat in stats.stats.values() if stat[0] is not None)
        print(f"Total number of function calls: {total_calls}")

    @profile(stream=open(f"{time.time()}_mem.prof", "w+"))
    def test_memory(self):
        mazes = self.mazes
        for maze in mazes:
            self.impl(maze)

    def test_time_per_maze(self):
        mazes = self.mazes
        times = []
        for maze in mazes:
            start = time.monotonic_ns()
            self.impl(maze)
            end = time.monotonic_ns()
            times.append(end - start)

        with open(f"{self.impl.__name__}_times.csv", "w") as f:
            f.write("Maze,Time\n")
            for i, t in enumerate(times):
                f.write(f"{i+1},{t / NANOSECOND_DIVISOR:.6f}\n")

        print(f"Time data saved to '{self.impl.__name__}_times.csv'")


def main():
    with open("args.txt", "r") as f:
        n, m, num_mazes = f.read().split()

    input_impl = input("Enter the implementation to test (A or B): ")

    # Generate mazes if they don't exist
    if not os.path.exists("mazes.flag"):
        periphery.generate_mazes(int(n), int(m), int(num_mazes))
    global a_or_b
    a_or_b = input_impl.upper()
    unittest.main()


def both():
    with open("args.txt", "r") as f:
        n, m, num_mazes = f.read().split()

    global a_or_b
    a_or_b = "A"
    unittest.main()
    a_or_b = "B"
    unittest.main()


if __name__ == "__main__":
    main()
