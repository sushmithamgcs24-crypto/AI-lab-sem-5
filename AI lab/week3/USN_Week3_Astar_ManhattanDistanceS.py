import heapq

# Manhattan Distance
def manhattan_distance(state, goal):
    distance = 0
    for tile in range(1, 9): 
        current_index = state.index(tile)
        goal_index = goal.index(tile)
        current_row = current_index // 3
        current_col = current_index % 3

        goal_row = goal_index // 3
        goal_col = goal_index % 3

        distance += abs(current_row - goal_row)
        distance += abs(current_col - goal_col)
    return distance

# Print the puzzle state in a 3x3 grid
def print_state(state):
    for i in range(0, 9, 3):
        print(" ".join(map(str, state[i:i + 3])))
    print()

# Generate all possible moves
def generate_successors(state):
    successors = []
    blank_index = state.index(0)
    row = blank_index // 3
    col = blank_index % 3

    # Up, Down, Left, Right
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in moves:
        new_row = row + dr
        new_col = col + dc

        # Check valid position
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_index = new_row * 3 + new_col
            new_state = list(state)

            # Swap blank with tile
            new_state[blank_index], new_state[new_index] = \
                new_state[new_index], new_state[blank_index]

            successors.append(tuple(new_state))
    return successors

# Reconstruct the solution path
def reconstruct_path(parent, state):
    path = []
    while state is not None:
        path.append(state)
        state = parent[state]
    path.reverse()
    return path

# A* Algorithm using Manhattan Distance
def a_star_manhattan(initial_state, goal_state):
    open_list = []
    closed = set()
    
    g = {}
    parent = {}
    g[initial_state] = 0
    parent[initial_state] = None
    h = manhattan_distance(initial_state, goal_state)
    f = g[initial_state] + h

    counter = 0
    # Insert initial state tuple into OPEN
    heapq.heappush(open_list, (f, counter, initial_state))

    while open_list:
        # Extract the state tuple from the popped min-heap element
        f_val, cnt, current = heapq.heappop(open_list)

        if current in closed:
            continue

        # Add current node state to CLOSED
        closed.add(current)

        # Check if goal is reached
        if current == goal_state:
            path = reconstruct_path(parent, current)
            print("\nSolution Found!")
            print("Number of moves:", len(path) - 1)
            print()
            for step, state in enumerate(path):
                print(f"Step {step}:")
                print_state(state)
            return path

        # Generate successors
        for successor in generate_successors(current):
            if successor in closed:
                continue

            new_g = g[current] + 1

            if successor not in g or new_g < g[successor]:
                g[successor] = new_g
                h = manhattan_distance(successor, goal_state)
                f = new_g + h
                parent[successor] = current
                counter += 1
                heapq.heappush(open_list, (f, counter, successor))

    print("No solution exists.")
    return None

def get_user_input(prompt):
    print(prompt)
    print("Enter 9 numbers (0-8) separated by spaces row by row (e.g., 1 2 3 4 0 6 7 5 8):")
    while True:
        try:
            user_input = input("> ").strip().split()
            if len(user_input) != 9:
                print("Error: Please enter exactly 9 numbers.")
                continue
            
            numbers = tuple(map(int, user_input))
            if sorted(numbers) != list(range(9)):
                print("Error: Input must contain all numbers from 0 to 8 exactly once.")
                continue
                
            return numbers
        except ValueError:
            print("Error: Invalid characters found. Please enter integers only.")

# --- Main execution execution flow ---
if __name__ == "__main__":
    print("--- 8-Puzzle Solver using A* and Manhattan Distance ---")
    initial_state = get_user_input("\n--- Define INITIAL State ---")
    goal_state = get_user_input("\n--- Define GOAL State ---")
    
    print("\nStarting search...")
    a_star_manhattan(initial_state, goal_state)
