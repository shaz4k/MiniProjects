import curses
from curses import wrapper
import queue
import time


maze = [
    ["#", "#", "#", "#", "#", "#", "O", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]


def find_path_bfs(maze, stdscr):
    start = 'O'
    end = 'X'
    start_position = find_start(maze, start)

    # Breadth-first search algorithm
    # Queue

    q = queue.Queue()
    q.put((start_position, [start_position]))

    visited = set()

    while not q.empty():
        current_position, path = q.get()
        row, col = current_position

        stdscr.clear()
        print_maze(maze, stdscr, path)
        time.sleep(0.2)
        stdscr.refresh()

        if maze[row][col] == end:
            return path, len(path)

        neighbours = find_neighbours(maze, row, col)
        for neighbour in neighbours:
            if neighbour in visited:
                continue

            r, c = neighbour
            if maze[r][c] == '#':
                continue

            new_path = path + [neighbour]
            q.put((neighbour, new_path))
            visited.add(neighbour)


def find_path_dfs(maze, stdscr):
    start = 'O'
    end = 'X'
    start_position = find_start(maze, start)

    # Use a stack instead of queue, where we append and pop elements from its end
    # DFS visits the most recently discovered node that hasn't been fully explored

    stack = []
    stack.append((start_position, [start_position]))

    visited = set()

    while stack:
        current_position, path = stack.pop()
        row, col = current_position

        stdscr.clear()
        print_maze(maze, stdscr, path)
        time.sleep(0.2)
        stdscr.refresh()

        if maze[row][col] == end:
            return path, len(path)

        neighbours = find_neighbours(maze, row, col)
        for neighbour in neighbours:
            if neighbour in visited:
                continue

            r, c = neighbour
            if maze[r][c] == '#':
                continue

            new_path = path + [neighbour]
            stack.append((neighbour, new_path))
            visited.add(neighbour)


def find_neighbours(maze, row, col):
    neighbours = []
    if row > 0:  # UP
        neighbours.append((row - 1, col))
    if row + 1 < len(maze):  # DOWN
        neighbours.append((row + 1, col))
    if col > 0:  # LEFT
        neighbours.append((row, col - 1))
    if col + 1 < len(maze[0]):  # RIGHT
        neighbours.append((row, col + 1))
    return neighbours


def find_start(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j
    return None


def print_maze(maze, stdscr, path=[]):
    GREEN = curses.color_pair(1)
    RED = curses.color_pair(2)

    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j*2, 'X', RED)
            else:
                stdscr.addstr(i, j*2, value, GREEN)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    while True:
        stdscr.addstr(0, 0, "Select an algorithm: \n")
        stdscr.addstr(1, 0, "1: Breadth-First Search\n")
        stdscr.addstr(2, 0, "2: Depth-First Search\n")
        stdscr.addstr(3, 0, "q: Quit\n")
        stdscr.refresh()
        stdscr.clrtobot()
        choice = stdscr.getkey()
        if choice == '1':
            start_time = time.time()
            path, path_length = find_path_bfs(maze, stdscr)
            end_time = time.time()
            stdscr.addstr(4, 0, f"BFS took {round(end_time - start_time, 3)} seconds\n")
            stdscr.addstr(5, 0, f"BFS took {path_length} steps\n")
        elif choice == '2':
            start_time = time.time()
            path, path_length = find_path_dfs(maze, stdscr)
            end_time = time.time()
            stdscr.addstr(4, 0, f"DFS took {round(end_time - start_time, 3)} seconds\n")
            stdscr.addstr(5, 0, f"BFS took {path_length} steps\n")
        elif choice.lower() == 'q':
            break
        else:
            stdscr.addstr("Invalid option. Please try again.\n")
        stdscr.addstr(6, 0, "Press any key to continue...\n")

        # stdscr.refresh()
        stdscr.getch()


wrapper(main)
