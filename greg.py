import random

random.seed(1)

move_x = [1, -1, 0, 0]
move_y = [0, 0, 1, -1]


def gen_maze(n: int, m: int, wall: str = "#") -> list[list[str]]:
    """
    n (int): The height of the maze.
    m (int): The width of the maze.
    wall (str): The character representing a wall in the maze.
    """
    if n % 2 == 0:
        n += 1
    if m % 2 == 0:
        m += 1

    maze = []
    i = 0
    while i < n:
        row = []
        j = 0
        while j < m:
            row.append(wall)
            j += 1
        maze.append(row)
        i += 1

    max_Y = n - 1
    max_X = m - 1

    q = []

    start_X = random.randrange(1, max_X, 2)
    start = (0, start_X)
    maze[start[0]][start[1]] = " "

    q.append((1, start_X))
    maze[1][start_X] = " "

    has_visited = set()
    has_visited.add((1, start_X))

    while len(q) > 0:
        curr = q.pop(len(q) - 1)
        Y = curr[0]
        X = curr[1]

        directions = []
        idx = 0
        while idx < len(move_x):
            directions.append((move_y[idx], move_x[idx]))
            idx += 1

        i = len(directions) - 1
        while i > 0:
            j = random.randint(0, i)
            temp = directions[i]
            directions[i] = directions[j]
            directions[j] = temp
            i -= 1

        dir_idx = 0
        while dir_idx < len(directions):
            dy = directions[dir_idx][0]
            dx = directions[dir_idx][1]
            newY = Y + dy * 2
            newX = X + dx * 2

            if newY > 0 and newY < max_Y and newX > 0 and newX < max_X:
                if (newY, newX) not in has_visited:
                    maze[Y + dy][X + dx] = " "
                    maze[newY][newX] = " "
                    has_visited.add((newY, newX))
                    q.append((newY, newX))
            dir_idx += 1

    exit_X = random.randrange(1, max_X, 2)
    maze[max_Y][exit_X] = " "

    i = 0
    while i < len(maze):
        line = ""
        j = 0
        while j < len(maze[i]):
            line += maze[i][j]
            j += 1
        i += 1
    return maze
