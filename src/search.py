from collections import deque
from src.node import Node
from src.sokoPuzzle import SokoPuzzle
from src.gui import animate_solution

# Symbols: 'R' player, 'O' wall, ' ' empty, 'S' target, 'B' box, '.' player on target, '*' box on target

board1 = [
    "OOOOOO",
    "OS B O",
    "O OR O",
    "O    O",
    "O    O",
    "OOOOOO",
]

board2 = [
    "OOOOOOOOO",
    "O       O",
    "O       O",
    "O  OOO  O",
    "O    O. O",
    "O     O O",
    "O  B  O O",
    "O     O O",
    "OOOOOOOOO",
]

board3 = [
    "OOOOOOOO",
    "O   O  O",
    "O  BR  O",
    "O   OB O",
    "OOOOO SO",
    "    O SO",
    "    OOOO",
]

board4 = [
    " OOOO  ",
    " O  O  ",
    " O  OOO",
    " O *  O",
    "OOBOB O",
    "O SRS O",
    "O    OO",
    "OOO  O ",
    "  OOOO ",
]

board5 = [
    "  OOOOOO ",
    "OOOSO  O ",
    "O    B OO",
    "O B R  SO",
    "OOO O OOO",
    "  OBO O  ",
    "  O  SO  ",
    "  OOOOO  ",
]

class Search:
    # (BFS) algorithm
    def breadthFirst(initial_node):
        if initial_node.state.isGoal():
            return initial_node

        frontier = deque([initial_node])
        explored = set()

        while frontier:
            
            node = frontier.popleft()
            explored.add(node.state)  


            # Expand the node: generate children via successorFunction()
            for action, new_state in node.state.successorFunction():
                if new_state not in explored:
                    child = Node(
                        state=new_state,
                        parent=node,
                        action=action,
                        g=node.g + 1
                    )

                    if new_state.isGoal():
                        return child

                    if (    # to make sure we don't explore the same state again, we check both explored and frontier
                        child.state not in explored
                        and not any(n.state == child.state for n in frontier)
                    ):
                        frontier.append(child)
        return None



    # A* algorithm ( person 1 )
    def aStarSearch(initial_node, heuristic) : ...



