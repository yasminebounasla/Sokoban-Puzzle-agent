## Répartition du travail

| Personne | Fichier(s) | À faire |
|---|---|---|
| **P1 : détection de deadlock** | `deadlock.py` (nouveau) | `findDeadCells(board)` : retourne `(corners, lines)`, deux ensembles de cases `(i, j)`<br>`_findCornerCells(board)` : cases en coin, hors cibles<br>`_findLineCells(board, corners)` : cases sur une ligne morte entre deux coins<br>`isDeadlock(state, dead_cells)` : `True` si une caisse est sur une case morte |
| **P2 : A\* amélioré** | `search.py`, fichier des heuristiques, `comparison.py` | `Search.aStar(initial_node, h, dead_cells=None)` : ignorer les états avec deadlock et les enregistrer dans `Search.pruned`<br>`h3` : enlever le `float('inf')` (h3 = h2 + terme robot-caisse)<br>`comparison.py` : ajouter la ligne « A\* h3 + deadlock », la colonne des états retirés, et lancer sur les 7 plateaux |
| **P3 : interface Pygame** | `gui.py`, `search.py` (main) | `choose_board()` : écran de choix du plateau<br>`choose_algorithm()` : choix BFS ou A\* (h1, h2, h3, avec ou sans deadlock)<br>`run_algorithm(name, board)` : lance l'algorithme, retourne solution, coût et steps<br>`draw_deadlocks(...)` et son bouton : cases mortes en rouge (coins) et jaune (lignes)<br>Dans le `main` : ajouter les plateaux 6 et 7 de la Figure 7 et vérifier leur coût avec BFS |

**À décider ensemble avant de coder :** `findDeadCells(board)` retourne `(corners, lines)`. P1 livre d'abord une version « coins seulement » pour que P2 et P3 puissent avancer.