from src.node import Node
from src.sokoPuzzle import SokoPuzzle
from src.search import Search
from src.gui import animate_solution
from src.search import Search, board1, board2, board3, board4, board5

USE_GUI = True


def main():
    board = board4

    initial_state = SokoPuzzle(board)
    root = Node(
        state=initial_state,
        parent=None,
        action=None,
        g=0
    )

    print("=" * 50)
    print("Initial state:")
    print(initial_state)
    print("=" * 50)
    print("\nRunning BFS ...\n")

    goal_node = Search.breadthFirst(root)

    if goal_node is None:
        print("No solution found.")
        return

    print("Solution found!")
    print(f"Path cost (g): {goal_node.g}")
    print(f"Solution actions: {goal_node.getSolution()}")
    print(f"Number of states in path: {len(goal_node.getPath())}")

    print("\nFinal state:")
    print(goal_node.state)

    if USE_GUI:
        animate_solution(
            goal_node.getPath(),
            goal_node.g,
            len(goal_node.getSolution())
        )


if __name__ == "__main__":
    main()