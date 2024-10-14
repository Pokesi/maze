from queue_interface import Queue as QueueInterface
from typing import Callable


def main(maze_input: list[str], Queue: Callable[[], QueueInterface]) -> None:
    moves: QueueInterface = Queue()
    WIDTH = len(maze_input[0])
    HEIGHT = len(maze_input)

    start_col = "".join(maze_input[0]).find(" ")

    maze: list[list[str]] = [list(row) for row in maze_input]

    parents: dict[tuple[int, int], tuple[int, int] | None] = {}

    moves.put((0, start_col))
    parents[(0, start_col)] = None

    exit_position = None
    while not moves.empty():
        n_r, n_c = moves.get()

        neighbors = {
            "u": (n_r - 1, n_c),
            "d": (n_r + 1, n_c),
            "r": (n_r, n_c + 1),
            "l": (n_r, n_c - 1),
        }

        for neighbor in neighbors.values():
            new_row, new_col = neighbor
            if 0 <= new_row < HEIGHT and 0 <= new_col < WIDTH:
                val = maze[new_row][new_col]

                if new_row == HEIGHT - 1 and val == " ":
                    exit_position = (new_row, new_col)
                    parents[(new_row, new_col)] = (n_r, n_c)

                    break
                if val == " " and (new_row, new_col) not in parents:
                    moves.put((new_row, new_col))
                    parents[(new_row, new_col)] = (n_r, n_c)

        if exit_position:
            break

    level = 0
    if exit_position:
        path_node: tuple[int, int] | None = exit_position
        while path_node is not None:
            r, c = path_node
            level += 1

            if maze[r][c] == " ":
                maze[r][c] = "."
                path_node = parents[path_node]
