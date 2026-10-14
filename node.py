class Node:
    
    def __init__(self, state, parent=None, action=None, g=0):
        self.state = state      # the game state (SokoPuzzle)
        self.parent = parent    # node we come from (None for the first node)
        self.action = action    # action that created this node ("U", "D", "L", "R")
        self.g = g              # path cost = number of actions so far

    # Rôle : liste des états du début jusqu'à ce nœud
    # cette fonction utilise : self.parent (remonte la chaîne)
    def getPath(self): ...

    # Rôle : liste des actions du début jusqu'à ce nœud
    # cette fonction utilise : self.parent, self.action
    def getSolution(self): ...