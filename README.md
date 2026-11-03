## Répartition du travail (partie 2 : deadlocks, A* amélioré, interface)

| Personne | Fichier | Fonction ou tâche | Rôle |
|---|---|---|---|
| **P1** | `deadlock.py` (nouveau) | `findDeadCells(board)` | retourne `(corners, lines)` |
| | | `_findCornerCells(board)` | cases en coin, hors cibles |
| | | `_findLineCells(board, corners)` | cases sur une ligne morte entre deux coins |
| | | `isDeadlock(state, dead_cells)` | True si une caisse est sur une case morte |
| **P2** | `search.py` | `Search.aStar(..., dead_cells=None)` | ignore les états avec deadlock |
| | | `Search.pruned` | liste des états retirés |
| | | plateaux 6 et 7 | ajouter la Figure 7 et vérifier le coût avec BFS |
| | heuristiques | `h3` | enlever le `float('inf')` |
| | `comparison.py` | ligne "A* h3 + deadlock" | ajouter la ligne et la colonne des états retirés |
| | rapport | tableau et analyse | solution, itérations et comparaison avec BFS, h1, h2, h3 |
| **P3** | `gui.py` | `choose_board()` | écran de choix du plateau |
| | | `choose_algorithm()` | BFS ou A* (h1, h2, h3, avec ou sans deadlock) |
| | | `run_algorithm(name, board)` | retourne solution, coût et steps |
| | | `draw_deadlocks(...)` | cases mortes : rouge (coins), jaune (lignes) |
