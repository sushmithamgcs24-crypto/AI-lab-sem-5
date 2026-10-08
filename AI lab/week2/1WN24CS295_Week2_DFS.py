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
    """Display the puzzle state as a 3x3 grid."""
    for i in range(0, 9, 3):
        print(state[i], state[i + 1], state[i + 2])
    print()


def dfs(initial, goal):
    """
    Perform Depth-First Search without depth limits.
    Uses a parent map to completely eliminate slow path-copying overhead.
    """
    # Stack contains only the state
    stack = [initial]

    # Store visited states
    visited = set()

    # parent_map[child_state] = parent_state
    parent_map = {initial: None}

    while stack:
        # Remove the top element (LIFO)
        current = stack.pop()

        # Check if goal is reached
        if current == goal:
            # Reconstruct the sequence of board states from goal back to initial state
            states_path = []
            curr = goal
            while curr is not None:
                states_path.append(curr)
                curr = parent_map[curr]
            states_path.reverse()
            return states_path

        # Skip if already visited
        if current in visited:
            continue

        visited.add(current)

        # Generate possible moves
        # Reversed so they are pushed onto stack in a natural priority order
        for new_state in reversed(get_moves(current)):
            if new_state not in visited and new_state not in parent_map:
                parent_map[new_state] = current
                stack.append(new_state)

    return None


# -------------------------------
# Main Program
# -------------------------------

print("8-PUZZLE USING DFS (GRID VISUALIZATION)")
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

# Perform DFS
solution_states = dfs(initial, goal)

# Display result
if solution_states is not None:
    print("\nGoal Reached!")
    print("\nSolution Path (Board States):")
    print(f"Total steps: {len(solution_states) - 1}\n")

    for step, state in enumerate(solution_states):
        print(f"--- Step {step} ---")
        print_state(state)
else:
    print("\nNo solution found.")
