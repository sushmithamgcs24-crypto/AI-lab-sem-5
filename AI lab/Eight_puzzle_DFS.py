# 8-Puzzle using Depth First Search (DFS)

def get_moves(state):
    """Generate all possible states by moving the blank tile."""
    moves = []

    # Find position of blank (0)
    zero = state.index(0)
    row = zero // 3
    col = zero % 3

    # Possible movements: Up, Down, Left, Right
    directions = [
        (-1, 0), # Up
        (1, 0), # Down
        (0, -1), # Left
        (0, 1) # Right
    ]

    for dr, dc in directions:
        new_row = row + dr
        new_col = col + dc

        # Check if move is valid
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_zero = new_row * 3 + new_col

            # Create new state
            new_state = list(state)

            # Swap blank with adjacent tile
            new_state[zero], new_state[new_zero] = \
                new_state[new_zero], new_state[zero]

            moves.append(tuple(new_state))

    return moves


def print_state(state):
    """Display the puzzle state."""
    for i in range(0, 9, 3):
        print(state[i], state[i + 1], state[i + 2])
    print()


def dfs(initial, goal, max_depth=15):
    """
    Perform Depth-First Search with a maximum depth limit 
    to prevent infinite deep paths and memory exhaustion.
    """
    # Stack contains (current_state, path, current_depth)
    stack = [(initial, [initial], 0)]

    # Store visited states to avoid cycles
    visited = set()

    while stack:
        # Remove the top element (LIFO)
        current, path, depth = stack.pop()

        # Check if goal is reached
        if current == goal:
            return path

        # Skip if already visited
        if current in visited:
            continue

        visited.add(current)

        # Only expand nodes if we haven't crossed the depth threshold
        if depth < max_depth:
            # We reverse the moves to search them in a natural order (Up -> Down -> Left -> Right)
            # because a stack is Last-In, First-Out (LIFO).
            for new_state in reversed(get_moves(current)):
                if new_state not in visited:
                    stack.append(
                        (new_state, path + [new_state], depth + 1)
                    )

    return None


# -------------------------------
# Main Program
# -------------------------------

print("8-PUZZLE USING DFS (DEPTH-LIMITED)")
print()

print("Enter Initial State:")
initial = []
for i in range(3):
    row = list(map(int, input(f"Enter row {i + 1}: ").split()))
    initial.extend(row)

print("\nEnter Goal State:")
goal = []
for i in range(3):
    row = list(map(int, input(f"Enter row {i + 1}: ").split()))
    goal.extend(row)

# Convert lists to tuples
initial = tuple(initial)
goal = tuple(goal)

# Perform DFS with a maximum path length restriction (e.g., 15)
# Note: For highly randomized grids, pure DFS is not recommended. 
# Use A* with Manhattan distance if your initial state is very far from the goal.
solution = dfs(initial, goal, max_depth=15)

# Display result
if solution:
    print("\nGoal Reached!")
    print("\nSolution Path:")
    print("Number of moves:", len(solution) - 1)
    print()

    for step, state in enumerate(solution):
        print("Step", step)
        print_state(state)
else:
    print("\nNo solution found within the maximum depth threshold.")
