import random
from collections import deque
import heapq

# Maze dimensions
MAZE_WIDTH = 10
MAZE_HEIGHT = 10

# Define the maze and the player's starting position
maze = [[' ' for _ in range(MAZE_WIDTH)] for _ in range(MAZE_HEIGHT)]
start = (0, 0)
goal = (MAZE_WIDTH - 1, MAZE_HEIGHT - 1)

# Directions for movement (right, down, left, up)
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def generate_maze():
    # Randomly place walls in the maze
    for i in range(MAZE_HEIGHT):
        for j in range(MAZE_WIDTH):
            if random.random() < 0.2:
                maze[i][j] = '#'

    # Ensure the start and goal positions are empty
    maze[start[0]][start[1]] = 'S'
    maze[goal[0]][goal[1]] = 'G'

def print_maze():
    for row in maze:
        print(''.join(row))

def is_valid_move(x, y):
    return 0 <= x < MAZE_HEIGHT and 0 <= y < MAZE_WIDTH and maze[x][y] != '#'

def bfs():
    queue = deque([start])
    visited = set([start])
    parent = {start: None}

    while queue:
        current = queue.popleft()
        if current == goal:
            return reconstruct_path(parent)

        for direction in directions:
            next_move = (current[0] + direction[0], current[1] + direction[1])
            if is_valid_move(next_move[0], next_move[1]) and next_move not in visited:
                queue.append(next_move)
                visited.add(next_move)
                parent[next_move] = current

    return None

def dfs():
    stack = [start]
    visited = set([start])
    parent = {start: None}

    while stack:
        current = stack.pop()
        if current == goal:
            return reconstruct_path(parent)

        for direction in directions:
            next_move = (current[0] + direction[0], current[1] + direction[1])
            if is_valid_move(next_move[0], next_move[1]) and next_move not in visited:
                stack.append(next_move)
                visited.add(next_move)
                parent[next_move] = current

    return None

def a_star():
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {start: None}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from)

        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])

            if is_valid_move(neighbor[0], neighbor[1]):
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def greedy_best_first_search():
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), start))
    came_from = {start: None}
    visited = set([start])

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from)

        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])

            if is_valid_move(neighbor[0], neighbor[1]) and neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                heapq.heappush(open_set, (heuristic(neighbor, goal), neighbor))

    return None

def reconstruct_path(came_from):
    current = goal
    path = []
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

def main():
    generate_maze()
    print("Maze:")
    print_maze()

    search_methods = {
        "1": bfs,
        "2": dfs,
        "3": a_star,
        "4": greedy_best_first_search
    }

    print("\nSelect a search method:")
    print("1. Breadth-First Search (BFS)")
    print("2. Depth-First Search (DFS)")
    print("3. A* Search")
    print("4. Greedy Best-First Search")

    choice = input("Enter the number of your choice: ")

    if choice in search_methods:
        path = search_methods[choice]()
        if path:
            print("\nPath to the treasure:")
            for step in path:
                maze[step[0]][step[1]] = 'P'
            print_maze()
        else:
            print("\nNo path found to the treasure.")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
