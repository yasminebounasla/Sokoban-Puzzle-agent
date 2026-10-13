from queue import Queue
import time
from node import Node
from sokoPuzzle import SokoPuzzle


class Search:

    # Rôle : BFS, retourne (goalNode, num_steps)  
    # cette fonction utilise : state.isGoal(), state.successorFunction(), Node(...), `in closed` (-> __eq__)
    @staticmethod
    def breadthFirst(initial_node): ...     


# ---- Configurations initiales  ----
board1 = []
board2 = []
board3 = []
board4 = []
board5 = []


# ---- Main  ----
# cette fonction utilise : SokoPuzzle(board=level), Node(...), Search.breadthFirst, getSolution(), getPath()
if __name__ == "__main__":
    level = board1
    # TODO : initial_node = Node(SokoPuzzle(board=level)) puis lancer le BFS et afficher le résultat
    # GUI : from gui import animate_solution (optionnel)