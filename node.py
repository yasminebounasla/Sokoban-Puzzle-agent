class Node:
    def __init__(self, state, parent=None, action=None, g=0):
     
        self.state = state
        self.parent = parent
        self.action = action
        self.g = g
        
    
    def getPath(self):  # list of states from the root to this node
        path = []
        current = self
        while current is not None:
            path.append(current.state)
            current = current.parent
        path.reverse()
        return path

    def getSolution(self): #  list of actions from the root to this node
      
        actions = []
        current = self
        while current is not None and current.action is not None:
            actions.append(current.action)
            current = current.parent
        actions.reverse()
        return actions

    def __repr__(self):
        return f"Node(action={self.action}, g={self.g})"
