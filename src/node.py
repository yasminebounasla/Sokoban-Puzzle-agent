class Node:
    def __init__(self, state, parent=None, action=None, g=0):
        self.state = state   
        self.parent = parent
        self.action = action      
        self.g = g
        self.h = 0                          
        self.f = 0 
        
    
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



    # calculate f(n)=g(n)+h(n)  
    def setF(self, heuristic):
        self.h = heuristic(self.state)       # h(n)
        self.f = self.g + self.h 


    def __repr__(self):  
        return f"Node(action={self.action}, g={self.g})"
