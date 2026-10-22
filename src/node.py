class Node:
    def __init__(self, state, parent=None, action=None, g=0):
        self.state = state   
        self.parent = parent
        self.action = action      
        self.g = g
        
    
    def getPath(self): 
        path = []
        current = self
        while current is not None:
            path.append(current.state)
            current = current.parent
        path.reverse()
        return path

    def getSolution(self): 
        actions = []
        current = self
        while current is not None and current.action is not None:
            actions.append(current.action)
            current = current.parent
        actions.reverse()
        return actions



    # calculate f(n)=g(n)+h(n)    person 1
    def setF(heuristic) : ...


    def __repr__(self):  
        return f"Node(action={self.action}, g={self.g})"
