def findDeadCells(board):
    """Return static dead squares as (corner_squares, other_dead_squares)."""
    floors = {
        (row, col)
        for row, cells in enumerate(board)
        for col, cell in enumerate(cells)
        if cell != "O"
    }
    goals = {
        (row, col)
        for row, cells in enumerate(board)
        for col, cell in enumerate(cells)
        if cell in ("S", ".", "*")
    }

    reachable = set(goals)
    frontier = list(goals)
    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))

    while frontier:
        row, col = frontier.pop()
        for dr, dc in directions:
            previous_box = (row - dr, col - dc)
            player_support = (row - 2 * dr, col - 2 * dc)
            if (
                previous_box in floors
                and player_support in floors
                and previous_box not in reachable
            ):
                reachable.add(previous_box)
                frontier.append(previous_box)

    dead_squares = floors - reachable
    corners = set()
    for row, col in dead_squares:
        vertical_wall = (
            (row - 1, col) not in floors or (row + 1, col) not in floors
        )
        horizontal_wall = (
            (row, col - 1) not in floors or (row, col + 1) not in floors
        )
        if vertical_wall and horizontal_wall:
            corners.add((row, col))

    return corners, dead_squares - corners


def isDeadlock(state, dead_cells):
    return any(
        cell == "B" and (row, col) in dead_cells
        for row, cells in enumerate(state.board)
        for col, cell in enumerate(cells)
    )