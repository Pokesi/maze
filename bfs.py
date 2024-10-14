# mypy: ignore-errors
from bfs_maze import main as bfs_maze
from team_A import Queue as QueueA
from team_B import Queue as QueueB


def A(maze: list[str], *args) -> list[str]:
    return bfs_maze(maze, QueueA)


def B(maze: list[str], *args) -> list[str]:
    return bfs_maze(maze, QueueB)
