# Attributs communs : robot_block, wall_space_obstacle (matrices 2D), robot_position (i, j), moves
# Symboles : R robot | O mur | ' ' vide | S cible | B caisse | . robot sur cible | * caisse sur cible
from copy import deepcopy

DIRECTIONS = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}


class SokoPuzzle:

    # Rôle : construit l'état à partir de la matrice board (P1)
    def __init__(self, board): ...

    # Rôle : True si toutes les caisses sont sur des cibles (P1)
    def isGoal(self): ...

    # Rôle : compare 2 états (robot + caisses), appelée par `in closed` dans le BFS (P1)
    def __eq__(self, other): ...




    # Rôle : applique une action U/D/L/R (avance ou pousse une caisse), None si invalide (P2)
    # cette fonction utilise : deepcopy, DIRECTIONS
    def _move(self, action): ...

    # Rôle : retourne [(action, nouvel_état), ...] pour les mouvements valides (P2)
    # cette fonction utilise : self._move
    def successorFunction(self): ...

    # Rôle : affiche la grille en texte, pour tester dans le terminal (P2, optionnelle)
    def __str__(self): ...