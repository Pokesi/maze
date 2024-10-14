import os

from greg import gen_maze


def generate_mazes(n: int, m: int, num_mazes: int) -> list[list[list[str]]]:
    mazes = []
    for _ in range(num_mazes):
        mazes.append(gen_maze(n, m))
    save_mazes(mazes)
    return mazes


def load_mazes() -> list[list[list[str]]]:
    mazes = []
    for file in os.listdir("mazes"):
        if file.endswith(".txt"):
            mazes.append(load_maze(int(file.split(".")[0])))
    return mazes


def save_mazes(mazes: list[list[list[str]]]) -> None:
    if not os.path.exists("mazes"):
        os.makedirs("mazes")
    for i, maze in enumerate(mazes):
        with open(f"mazes/{i + 1}.txt", "w") as f:
            for row in maze:
                f.write("".join(row) + "\n")
    open("mazes.flag", "w").close()


def load_maze(i: int) -> list[list[str]]:
    with open(f"mazes/{i}.txt", "r") as f:
        return [list(line.strip()) for line in f]
