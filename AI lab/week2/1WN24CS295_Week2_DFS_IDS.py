# 8-Puzzle using Iterative Deepening Search (IDS)

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


def depth_limited_search(state, goal, limit, visited):
    """Perform a depth-limited DFS search to find the target state sequence."""
    if state == goal:
        return [state]
    if limit <= 0:
        return "cutoff"
        
    visited.add(state)
    cutoff_occurred = False
    
    for neighbor in get_moves(state):
        if neighbor not in visited:
            result = depth_limited_search(neighbor, goal, limit - 1, visited)
            
            if result == "cutoff":
                cutoff_occurred = True
            elif result != "failure":
                # Return the successful structural path list
                return [state] + result
                
    visited.remove(state)  # Backtrack from visited set
    
    return "cutoff" if cutoff_occurred else "failure"


def ids(initial, goal):
    """Iterate through increasing depths to find the optimal move path."""
    depth = 0
    while True:
        visited = set()
        result = depth_limited_search(initial, goal, depth, visited)
        if result != "cutoff" and result != "failure":
            return result
        depth += 1


# -------------------------------
# Main Program
# -------------------------------

print("8-PUZZLE USING IDS (GRID VISUALIZATION)")
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

# Perform IDS
solution_states = ids(initial, goal)

# Display result
if solution_states:
    print("\nGoal Reached!")
    print("\nSolution Path (Board States):")
    print(f"Total steps taken: {len(solution_states) - 1}\n")

    for step, state in enumerate(solution_states):
        print(f"--- Step {step} ---")
        print_state(state)
else:
    print("\nNo solution found.")
