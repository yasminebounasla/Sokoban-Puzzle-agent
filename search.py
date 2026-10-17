from collections import deque
from node import Node
from soko_puzzle import SokoPuzzle

# ---------------------------------------------------------
# Test levels (board1 ... board5)
# Symbols: 'R' player, 'O' wall, ' ' empty, 'S' target, 'B' box
# ---------------------------------------------------------
board1 = [
    "OOOOOOOOO",
    "O       O",
    "O R B S O",
    "O       O",
    "OOOOOOOOO",
]

board2 = [
    "OOOOOOOO",
    "O      O",
    "O R B  O",
    "O     SO",
    "O      O",
    "OOOOOOOO",
]

board3 = [
    "OOOOOOOOO",
    "O       O",
    "O R B S O",
    "O       O",
    "O B S   O",
    "O       O",
    "OOOOOOOOO",
]

board4 = [
    "  OOOOO  ",
    "  O   O  ",
    "  O B O  ",
    "  O S O  ",
    "  O   O  ",
    "OOOO OOOO",
    "O        O",
    "O  R  B  O",
    "O       SO",
    "OOOOOOOOOO",
]

board5 = [
    "OOOOOOOOOO",
    "O        O",
    "O  R  B  O",
    "O      S O",
    "O  B     O",
    "O     S  O",
    "O        O",
    "OOOOOOOOOO",
]


# ---------------------------------------------------------
# (BFS) algorithm
# ---------------------------------------------------------
def breadthFirst(initial_node):
    # Quick check: the root itself may already be a goal
    if initial_node.state.isGoal():
        return initial_node

    # FIFO queue: first-in, first-out
    frontier = deque([initial_node])

    # Set of visited states (to avoid revisiting)
    explored = set()
    explored.add(initial_node.state)

    while frontier:
        # Pop the first node from the queue
        node = frontier.popleft()

        # Expand the node: generate children via successorFunction()
        for action, new_state in node.state.successorFunction():
            # Only consider newly discovered states
            if new_state not in explored:
                child = Node(
                    state=new_state,
                    parent=node,
                    action=action,
                    g=node.g + 1
                )

                # Goal test before enqueueing (early exit optimization)
                if new_state.isGoal():
                    return child

                frontier.append(child)
                explored.add(new_state)

    # No solution found
    return None

# ---------------------------------------------------------
# main : launch BFS on a chosen board
# ---------------------------------------------------------
def main():
    # Select the board (feel free to switch to board2, board3, ...)
    board = board1

    # 1) Build the initial state from the chosen board
    initial_state = SokoPuzzle(board)

    # 2) Build the root node
    root = Node(state=initial_state, parent=None, action=None, g=0)

    print("=" * 50)
    print("Initial state:")
    print(initial_state)
    print("=" * 50)
    print("\nRunning BFS ...\n")

    # 3) Run BFS
    goal_node = breadthFirst(root)

    # 4) Display the results
    if goal_node is None:
        print("No solution found.")
        return

    print("Solution found!")
    print(f"  Path cost (g)   : {goal_node.g}")
    print(f"  Solution actions: {goal_node.getSolution()}")
    print(f"  Number of states in path: {len(goal_node.getPath())}")

    print("\nFinal state:")
    print(goal_node.state)
    print("=" * 50)


if __name__ == "__main__":
    main()
