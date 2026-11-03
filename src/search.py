from collections import deque

from src.deadlock import isDeadlock
from src.node import Node

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

board6 = [
    "OOOOOOO",
    "OS O RO",
    "O  OB O",
    "OS  B O",
    "O  OB O",
    "OS O  O",
    "OOOOOOO",
]

board7 = [
    "OOOOOO  ",
    "OSSS OOO",
    "O S B  O",
    "O  BBB O",
    "OOOO  RO",
    "   OOOOO",
]


class Search:
    pruned = []

    @staticmethod
    def breadthFirst(initial_node):
        steps = 0
        if initial_node.state.isGoal():
            return initial_node, steps

        frontier = deque([initial_node])
        explored = set()

        while frontier:
            node = frontier.popleft()
            explored.add(node.state)
            steps += 1

            for action, new_state in node.state.successorFunction():
                if new_state not in explored:
                    child = Node(
                        state=new_state,
                        parent=node,
                        action=action,
                        g=node.g + 1,
                    )

                    if new_state.isGoal():
                        return child, steps

                    if (
                        child.state not in explored
                        and not any(n.state == child.state for n in frontier)
                    ):
                        frontier.append(child)
        return None, steps

    @staticmethod
    def _find(nodes, state):
        for node in nodes:
            if node.state == state:
                return node
        return None

    @staticmethod
    def aStar(initial_node, h, dead_cells=None):
        Search.pruned = []
        initial_node.setF(h)
        open_list = [initial_node]
        closed_list = []
        steps = 0

        while open_list:
            current = min(open_list, key=lambda node: node.f)
            open_list.remove(current)
            steps += 1
            if current.state.isGoal():
                return current, steps
            closed_list.append(current)

            for action, successor in current.state.successorFunction():
                if dead_cells and isDeadlock(successor, dead_cells):
                    Search.pruned.append(successor)
                    continue
                child = Node(successor, current, action, current.g + 1)
                child.setF(h)

                in_open = Search._find(open_list, successor)
                in_closed = Search._find(closed_list, successor)

                if in_open is None and in_closed is None:
                    open_list.append(child)
                elif in_open is not None and in_open.f > child.f:
                    open_list.remove(in_open)
                    open_list.append(child)
                elif in_closed is not None and in_closed.f > child.f:
                    closed_list.remove(in_closed)
                    open_list.append(child)

        return None, steps
