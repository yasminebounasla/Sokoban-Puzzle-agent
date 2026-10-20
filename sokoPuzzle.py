from copy import deepcopy

DIRECTIONS = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}


# Symbols: 'R' player, 'O' wall, ' ' empty, 'S' target, 'B' box, '.' player on target, '*' box on target

class SokoPuzzle:

    # create a state from a board (list of strings)
    def __init__(self, board):

        # Convert each row into a list of characters
        self.board = [list(row) for row in board]

        # Board dimensions
        self.rows = len(self.board)    
        self.cols = len(self.board[0]) 

        # Possible movements
        self.moves = list(DIRECTIONS.keys())

        # Find the robot's position
        self.robot_position = None

        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell in ('R', '.'):              # robot is on a target (.) or on a normal cell (R)
                    self.robot_position = (i, j)
                    break

            if self.robot_position is not None:
                break 

    # True if all boxes are on targets
    def isGoal(self): 
        # Count all boxes
        boxes = sum(
            cell in ('B', '*')
            for row in self.board
            for cell in row
        )

        # Count all targets
        targets = sum(
            cell in ('S', '.', '*')
            for row in self.board
            for cell in row
        )

        # Count boxes placed on targets
        boxes_on_targets = sum(
            cell == '*'
            for row in self.board
            for cell in row
        )

        # The puzzle is solved when every box is on a target
        return boxes == targets and boxes_on_targets == boxes


    # compare 2 states (robot + boxes), called by `in closed` in the BFS
    def __eq__(self, other): 
         # Check that the other object is a SokoPuzzle object
        if not isinstance(other, SokoPuzzle):
            return False

        # Compare the two boards
        return self.board == other.board


    # 
    def __hash__(self):
        return hash(tuple("".join(row) for row in self.board))


    # move to a direction (U, D, L, R) if possible, return new state or None
    def _move(self, action):
        di, dj = DIRECTIONS[action]               
        i, j = self.robot_position                 # position of the robot
        ni, nj = i + di, j + dj                    # next position of the robot
        next_cell = self.board[ni][nj]             # the content of the next cell in the board

        # 1. whole
        if next_cell == 'O':
            return None
        
        # 2. box in front
        if next_cell in ('B', '*'):
            bi, bj = ni + di, nj + dj            # position of the cell behind the box
            behind = self.board[bi][bj]
            if behind not in (' ', 'S'):         # verify if the box can be pushed
                return None

        new_state = deepcopy(self)                # create a new state to avoid modifying the current one

        # 2. box in front
        if next_cell in ('B', '*'):
            new_state.board[bi][bj] = 'B' if behind == ' ' else '*'      # box moves: R B ' ' -> ' ' R B  | R B S -> ' ' R *
            new_state.board[ni][nj] = 'R' if next_cell == 'B' else '.'   # robot takes box cell: R B -> R |   R * -> '.' (robot on target)
        else:
            new_state.board[ni][nj] = 'R' if next_cell == ' ' else '.'   # no box: R ' ' -> ' ' R   |   R S -> ' ' .
 
        new_state.board[i][j] = ' ' if self.board[i][j] == 'R' else 'S'  # exit cell: R -> ' '   |   '.' -> S   (target shows again)
        new_state.robot_position = (ni, nj)                              # update position on the new state
        return new_state


    # returns a list of (action, new_state) pairs for all valid moves from the current state
    def successorFunction(self):
        successors = []                             # empty list
        for action in self.moves:                   # "U", "D", "L", "R"
            new_state = self._move(action)          # new state or None
            if new_state is not None:               # None = invalid move, ignore it
                successors.append((action, new_state))  # e.g. ("D", state_D)
        return successors                           # 0 to 4 pairs

    def __str__(self):
        return "\n".join("".join(row) for row in self.board)