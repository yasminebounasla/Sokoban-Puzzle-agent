# Attributs communs : board (matrice 2D avec les 7 symboles), robot_position (i, j), rows, cols, moves
# Symboles : R robot | O mur | ' ' vide | S cible | B caisse | . robot sur cible | * caisse sur cible
from copy import deepcopy

DIRECTIONS = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}


class SokoPuzzle:

    # Rôle : construit l'état à partir de la matrice board 
    def __init__(self, board): ...

    # Rôle : True si toutes les caisses sont sur des cibles 
    def isGoal(self): ...

    # Rôle : compare 2 états (robot + caisses), appelée par `in closed` dans le BFS 
    def __eq__(self, other): ...




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


    # Rôle : retourne [(action, nouvel_état), ...] pour les mouvements valides 
    def successorFunction(self): ...
