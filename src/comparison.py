# perosn 3 
from time import perf_counter

from src.node import Node
from src.search import Search, board1, board2, board3, board4, board5
from src.sokoPuzzle import SokoPuzzle
from src.heuristics import heuristic


class Comparison:

    @staticmethod
    def measureSearch(algorithm, board, h=None):
        # Create a new initial state for each execution
        initial_state = SokoPuzzle(board)
        root = Node(
            state=initial_state,
            parent=None,
            action=None,
            g=0
        )

        # Measure execution time
        start = perf_counter()

        if algorithm == "BFS":
            goal_node, steps = Search.breadthFirst(root)
            

        else:
            goal_node, steps = Search.aStar(root, h)

        end = perf_counter()

        # Extract results
        if goal_node is None:
            cost = None
        else:
            cost = goal_node.g

        return {
            "time": end - start,
            "cost": cost,
            "expanded": steps,
        }

    @staticmethod
    def runComparison(puzzles):
        results = []

        for puzzle_name, board in puzzles:

            # Run BFS
            bfs_result = Comparison.measureSearch(
                "BFS", board
            )

            results.append({
                "puzzle": puzzle_name,
                "algorithm": "BFS",
                **bfs_result
            })

            # Run A* with each heuristic
            for h_name in ("h1", "h2", "h3"):
                h = heuristic.getHeuristic(h_name)

                astar_result = Comparison.measureSearch(
                    "A*", board, h
                )

                results.append({
                    "puzzle": puzzle_name,
                    "algorithm": f"A* ({h_name})",
                    **astar_result
                })

        Comparison.printResults(results)
        return results

    @staticmethod
    def printResults(results):
        print(
            f"{'Puzzle':<10}"
            f"{'Algorithm':<12}"
            f"{'Time (s)':<15}"
            f"{'Cost':<10}"
            f"{'Expanded':<10}"
        )

        print("-" * 57)

        for result in results:
            time_value = result["time"]
            cost = result["cost"]
            expanded = result["expanded"]

            cost_text = str(cost) if cost is not None else "No solution"
            expanded_text = (
                str(expanded) if expanded is not None else "N/A"
            )

            print(
                f"{result['puzzle']:<10}"
                f"{result['algorithm']:<12}"
                f"{time_value:<15.6f}"
                f"{cost_text:<10}"
                f"{expanded_text:<10}"
            )


if __name__ == "__main__":
    puzzles = [
        ("board1", board1),
        ("board2", board2),
        ("board3", board3),
        ("board4", board4),
        ("board5", board5),
    ]

    Comparison.runComparison(puzzles)