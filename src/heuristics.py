#person 2 

import math

class heuristic:
    @staticmethod
    def h1(state):

        grid = state.board if hasattr(state, 'board') else state
        count = 0
        for row in grid:
            for cell in row:
                if cell == 'B':
                    count += 1
        return count

    @staticmethod
    def h2(state):
 
        grid = state.board if hasattr(state, 'board') else state
        nb_left = heuristic.h1(state)
        if nb_left == 0:
            return 0

        boxes_left = []
        targets = []

        # Extract coordinates of unplaced boxes ('B') and target positions ('S', '.', '*')
        for r in range(len(grid)):
            for c in range(len(grid[r])):
                cell = grid[r][c]
                if cell == 'B':
                    boxes_left.append((r, c))
                if cell in ('S', '.', '*'):
                    targets.append((r, c))

        manhattan_sum = 0
        for bx, by in boxes_left:
            # Find minimum Manhattan distance to the nearest target
            min_dist = min(abs(bx - tx) + abs(by - ty) for tx, ty in targets)
            manhattan_sum += min_dist

        return 2 * nb_left + manhattan_sum

    @staticmethod
    def h3(state):

        grid = state.board if hasattr(state, 'board') else state
        nb_left = heuristic.h1(state)
        if nb_left == 0:
            return 0

        boxes_left = []
        targets = []
        player_pos = None

        for r in range(len(grid)):
            for c in range(len(grid[r])):
                cell = grid[r][c]
                if cell == 'B':
                    boxes_left.append((r, c))
                elif cell in ('R', '.'):
                    player_pos = (r, c)
                
                if cell in ('S', '.', '*'):
                    targets.append((r, c))

        # 1. Corner Deadlock Detection:
        # If an unplaced box is trapped in a corner formed by walls, the state is unsolvable
        for bx, by in boxes_left:
            if (bx, by) not in targets:
                wall_up = grid[bx - 1][by] == 'O'
                wall_down = grid[bx + 1][by] == 'O'
                wall_left = grid[bx][by - 1] == 'O'
                wall_right = grid[bx][by + 1] == 'O'

                if (wall_up and wall_left) or (wall_up and wall_right) or \
                   (wall_down and wall_left) or (wall_down and wall_right):
                    return float('inf')  # Prune this branch completely

        # 2. Base h2 value calculation
        h2_val = heuristic.h2(state)

        # 3. Add distance from player to the nearest unplaced box
        if player_pos and boxes_left:
            px, py = player_pos
            min_player_to_box = min(abs(px - bx) + abs(py - by) for bx, by in boxes_left)
            player_cost = max(0, min_player_to_box - 1)
        else:
            player_cost = 0

        return h2_val + player_cost

    
    @staticmethod
    def getHeuristic(name):
      
        heuristics = {
            'h1': heuristic.h1,
            'h2': heuristic.h2,
            'h3': heuristic.h3
        }
        return heuristics.get(name, heuristic.h1)
