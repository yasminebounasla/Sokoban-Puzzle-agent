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




    # Rôle : applique une action U/D/L/R (avance ou pousse une caisse), None si invalide 
    # cette fonction utilise : deepcopy, DIRECTIONS
    def _move(self, action):  
        ...


    # Rôle : retourne [(action, nouvel_état), ...] pour les mouvements valides 
    # cette fonction utilise : self._move
    def successorFunction(self): ...
