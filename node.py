class Node:

    # Rôle : stocke l'état, le parent, l'action et le coût g
    def __init__(self, state, parent=None, action=None, g=0): ...

    # Rôle : liste des états du début jusqu'à ce nœud
    # cette fonction utilise : self.parent (remonte la chaîne)
    def getPath(self): ...

    # Rôle : liste des actions du début jusqu'à ce nœud
    # cette fonction utilise : self.parent, self.action
    def getSolution(self): ...