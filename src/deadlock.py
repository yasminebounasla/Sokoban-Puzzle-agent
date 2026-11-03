def _findCornerCells(board):
    """
    Returns the corner cells that are not target squares.
    A corner is formed by two adjacent walls (Up/Left, Up/Right, Down/Left, Down/Right).
    """
    corners = set()
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    for r in range(rows):
        for c in range(cols):
            cell = board[r][c]
            # Ignore walls and target cells ('S', '.', '*')
            if cell in ('O', 'S', '.', '*'):
                continue
            
            # Check for the presence of walls in the four directions
            wall_up = (r - 1 >= 0 and board[r - 1][c] == 'O')
            wall_down = (r + 1 < rows and board[r + 1][c] == 'O')
            wall_left = (c - 1 >= 0 and board[r][c - 1] == 'O')
            wall_right = (c + 1 < cols and board[r][c + 1] == 'O')
            
            # A corner is formed by two perpendicular walls
            if (wall_up and wall_left) or (wall_up and wall_right) or \
               (wall_down and wall_left) or (wall_down and wall_right):
                corners.add((r, c))
                
    return corners

def _findLineCells(board, corners):
    """
    Returns cells on a dead line connecting two corners.
    The line must have a continuous wall on at least one side and contain no targets.
    """
    lines = set()
    corners_list = list(corners)
    
    for i in range(len(corners_list)):
        for j in range(i + 1, len(corners_list)):
            r1, c1 = corners_list[i]
            r2, c2 = corners_list[j]
            
            # Check horizontal lines (same row)
            if r1 == r2:
                c_min, c_max = min(c1, c2), max(c1, c2)
                is_dead_line = True
                wall_above_continuous = True
                wall_below_continuous = True
                
                for c in range(c_min + 1, c_max):
                    cell = board[r1][c]
                    # If there is a wall or a target in the path, it's not a dead line
                    if cell in ('O', 'S', '.', '*'):
                        is_dead_line = False
                        break
                    
                    # Check wall continuity above and below the line
                    if board[r1 - 1][c] != 'O':
                        wall_above_continuous = False
                    if board[r1 + 1][c] != 'O':
                        wall_below_continuous = False
                        
                if is_dead_line and (wall_above_continuous or wall_below_continuous):
                    for c in range(c_min + 1, c_max):
                        lines.add((r1, c))
                        
            # Check vertical lines (same column)
            elif c1 == c2:
                r_min, r_max = min(r1, r2), max(r1, r2)
                is_dead_line = True
                wall_left_continuous = True
                wall_right_continuous = True
                
                for r in range(r_min + 1, r_max):
                    cell = board[r][c1]
                    # If there is a wall or a target in the path, it's not a dead line
                    if cell in ('O', 'S', '.', '*'):
                        is_dead_line = False
                        break
                    
                    # Check wall continuity to the left and right of the line
                    if board[r][c1 - 1] != 'O':
                        wall_left_continuous = False
                    if board[r][c1 + 1] != 'O':
                        wall_right_continuous = False
                        
                if is_dead_line and (wall_left_continuous or wall_right_continuous):
                    for r in range(r_min + 1, r_max):
                        lines.add((r, c1))
                        
    return lines

def findDeadCells(board):
    """
    Returns a tuple of (corners, lines) representing all dead cells on the board.
    """
    corners = _findCornerCells(board)
    lines = _findLineCells(board, corners)
    return corners, lines

def isDeadlock(state, dead_cells):
    """
    Returns True if any unplaced box is located on a dead cell (corner or line).
    """
    if dead_cells is None:
        return False
        
    corners, lines = dead_cells
    all_dead_cells = corners.union(lines)
    
    # Check if any standard box 'B' (not on a target '*') is on a dead cell
    for r in range(len(state.board)):
        for c in range(len(state.board[0])):
            if state.board[r][c] == 'B':
                if (r, c) in all_dead_cells:
                    return True
                    
    return False