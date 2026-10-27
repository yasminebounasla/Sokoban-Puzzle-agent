from collections import deque
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

class Search:
    # (BFS) algorithm
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
                        return child, steps

                    if (    # to make sure we don't explore the same state again, we check both explored and frontier
                        child.state not in explored
                        and not any(n.state == child.state for n in frontier)
                    ):
                        frontier.append(child)
        return None, steps


    # verify if a state exist in open/closed list
    @staticmethod
    def _find(nodes, state):
        for n in nodes:
            if n.state == state:
                return n
        return None

    
    # A* algorithm 
    @staticmethod
    def aStar(initial_node, h):                         # h1, h2 or h3
        initial_node.setF(h)                            # calculate first f(n)
        open_list = [initial_node]                      
        closed_list = []                                
        steps = 0

        while open_list:                                # while not empty
            current = min(open_list, key=lambda n: n.f) # node with the lowest f(n)
            open_list.remove(current)                   # remove it form open list
            steps += 1
            if current.state.isGoal():                  # if isGoal(current.state) return current
                return current, steps
            closed_list.append(current)                 # add this node to closed list

            for action, successor in current.state.successorFunction():
                child = Node(successor, current, action, current.g + 1)   # child.g <- current.g + 1
                child.setF(h)                                             # child.f <- g + h

                # decide where to put the child 
                in_open = Search._find(open_list, successor)              
                in_closed = Search._find(closed_list, successor)          

                if in_open is None and in_closed is None:        # add child to Open list
                    open_list.append(child)
                elif in_open is not None and in_open.f > child.f:     # add it to  Open list with a higher f
                    open_list.remove(in_open)
                    open_list.append(child)
                elif in_closed is not None and in_closed.f > child.f:  # in Closed with a higher f
                    closed_list.remove(in_closed)
                    open_list.append(child)

        return None, steps  


