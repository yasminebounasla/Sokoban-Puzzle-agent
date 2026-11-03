import pygame
from pathlib import Path

from src.deadlock import findDeadCells
from src.heuristics import heuristic
from src.node import Node
from src.search import Search, board1, board2, board3, board4, board5, board6, board7
from src.sokoPuzzle import SokoPuzzle

TILE = 64        # taille d'une case en pixels
INFO_H = 60      # hauteur de la bande d'info sous la grille
MENU_SIZE = (800, 600)

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"

FILES = {
    "wall": ASSETS_DIR / "wall.png",
    "space": ASSETS_DIR / "space.png",
    "target": ASSETS_DIR / "target.png",
    "box": ASSETS_DIR / "box.png",
    "box_on_target": ASSETS_DIR / "box_on_target.png",
    "player": ASSETS_DIR / "player.png",
}


BOARDS = (
    ("Board 1", board1),
    ("Board 2", board2),
    ("Board 3", board3),
    ("Board 4", board4),
    ("Board 5", board5),
    ("Board 6", board6),
    ("Board 7", board7),
)

ALGORITHMS = (
    "BFS",
    "A* (h1)",
    "A* (h2)",
    "A* (h3)",
    "A* (h1 + deadlock)",
    "A* (h2 + deadlock)",
    "A* (h3 + deadlock)",
)


def _choose_option(title, options):
    pygame.init()
    screen = pygame.display.set_mode(MENU_SIZE)
    pygame.display.set_caption("Sokoban - " + title)
    title_font = pygame.font.SysFont("arial", 34, bold=True)
    option_font = pygame.font.SysFont("arial", 23)
    small_font = pygame.font.SysFont("arial", 17)
    button_height = 48
    gap = 12
    total_height = len(options) * button_height + (len(options) - 1) * gap
    start_y = (MENU_SIZE[1] - total_height) // 2 + 20
    button_rects = [
        pygame.Rect(160, start_y + index * (button_height + gap), 480, button_height)
        for index in range(len(options))
    ]
    clock = pygame.time.Clock()

    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill((26, 31, 40))
        heading = title_font.render(title, True, (245, 245, 245))
        screen.blit(heading, heading.get_rect(center=(MENU_SIZE[0] // 2, 55)))

        for index, (option, rect) in enumerate(zip(options, button_rects)):
            hovered = rect.collidepoint(mouse_pos)
            color = (72, 112, 153) if hovered else (48, 62, 78)
            pygame.draw.rect(screen, color, rect, border_radius=8)
            pygame.draw.rect(screen, (112, 132, 154), rect, 1, border_radius=8)
            label = option_font.render(f"{index + 1}.  {option}", True, (255, 255, 255))
            screen.blit(label, label.get_rect(midleft=(rect.x + 18, rect.centery)))

        hint = small_font.render("Click an option or press its number. Esc to quit.", True, (185, 190, 198))
        screen.blit(hint, hint.get_rect(center=(MENU_SIZE[0] // 2, MENU_SIZE[1] - 25)))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                if pygame.K_1 <= event.key <= pygame.K_9:
                    index = event.key - pygame.K_1
                    if index < len(options):
                        return index
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for index, rect in enumerate(button_rects):
                    if rect.collidepoint(event.pos):
                        return index

        clock.tick(30)


def choose_board():
    """Show the board picker and return the selected (name, board), or None."""
    selection = _choose_option("Choose a board", [name for name, _ in BOARDS])
    return BOARDS[selection] if selection is not None else None


def choose_algorithm():
    """Show the algorithm picker and return its label, or None."""
    selection = _choose_option("Choose a search algorithm", ALGORITHMS)
    return ALGORITHMS[selection] if selection is not None else None


def run_algorithm(name, board):
    """Return (solution states, path cost, expanded nodes) for the selected search."""
    root = Node(SokoPuzzle(board))
    if name == "BFS":
        goal_node, steps = Search.breadthFirst(root)
    else:
        algorithms = {
            "A* (h1)": ("h1", False),
            "A* (h2)": ("h2", False),
            "A* (h3)": ("h3", False),
            "A* (h1 + deadlock)": ("h1", True),
            "A* (h2 + deadlock)": ("h2", True),
            "A* (h3 + deadlock)": ("h3", True),
        }
        try:
            heuristic_name, use_deadlocks = algorithms[name]
        except KeyError:
            raise ValueError(f"Unknown search algorithm: {name}") from None

        dead_cells = None
        if use_deadlocks:
            corners, lines = findDeadCells(SokoPuzzle(board).board)
            dead_cells = corners | lines
        estimate = heuristic.getHeuristic(heuristic_name)
        goal_node, steps = Search.aStar(root, estimate, dead_cells)

    if goal_node is None:
        return None, None, steps
    return goal_node.getPath(), goal_node.g, steps


# download the images and scale them to TILE x TILE
def load_images():
    images = {}
    for name, file in FILES.items():
        img = pygame.image.load(str(file))                             # load image from file
        images[name] = pygame.transform.scale(img, (TILE, TILE))   # resize all images to TILE x TILE
    return images


# draw the board on the screen, using the images dictionary
def draw_board(screen, state, images):
    for i, row in enumerate(state.board):
        for j, cell in enumerate(row):
            pos = (j * TILE, i * TILE)              # colonne j -> x, ligne i -> y
            if cell == 'O':
                screen.blit(images["wall"], pos)              # O -> wall
            elif cell == 'B':
                screen.blit(images["box"], pos)               # B -> box
            elif cell == '*':
                screen.blit(images["box_on_target"], pos)     # * -> box on target
            elif cell == 'S':
                screen.blit(images["target"], pos)            # S -> target
            elif cell == 'R':
                screen.blit(images["space"], pos)             # R -> space + robot par-dessus
                screen.blit(images["player"], pos)
            elif cell == '.':
                screen.blit(images["target"], pos)            # . -> target + robot par-dessus
                screen.blit(images["player"], pos)
            else:
                screen.blit(images["space"], pos)             # ' ' -> space


# display the cost and number of steps in the info band at the bottom of the window
def show_info(screen, cost, steps):
    font = pygame.font.SysFont("arial", 22)                                     # create a font object
    text = font.render(f"Cost: {cost}   Steps: {steps}", True, (255, 255, 255)) # create a text surface with white color
    y = screen.get_height() - INFO_H + 15                                       # position of the text (15 pixels from the top of the info band)
    screen.blit(text, (10, y))                     # draw the text on the screen at (10, y) with 10 pixels from the left


def draw_deadlocks(screen, corners, lines):
    """Overlay deadlock squares: red for corners, yellow for other dead squares."""
    for cells, color in (
        (corners, (230, 45, 45, 105)),
        (lines, (245, 205, 45, 105)),
    ):
        for row, col in cells:
            rect = pygame.Rect(col * TILE, row * TILE, TILE, TILE)
            overlay = pygame.Surface((TILE, TILE), pygame.SRCALPHA)
            overlay.fill(color)
            screen.blit(overlay, rect.topleft)
            pygame.draw.rect(screen, color[:3], rect, 2)


# animate the solution path on the screen, with a pause between each state
def animate_solution(path, cost, steps, deadlock_cells=None):
    pygame.init()                                                       # start pygame
    rows = len(path[0].board)                                           # number of rows in the board
    cols = len(path[0].board[0])                                        # number of columns in the board
    screen = pygame.display.set_mode((cols * TILE, rows * TILE + INFO_H))  # create the window (board + info band)
    pygame.display.set_caption("Sokoban")                               # window title
    images = load_images()                                              # load the images once
    corners, lines = deadlock_cells or (set(), set())

    for state in path:                                                  # state = one picture of the board
        for event in pygame.event.get():                                # events = everything the user did
            if event.type == pygame.QUIT:                               # if the user closed the window, stop the animation
                pygame.quit()
                return False
        screen.fill((30, 30, 30))                                       # gray background for the info band
        draw_board(screen, state, images)                               # draw the current state
        draw_deadlocks(screen, corners, lines)
        show_info(screen, cost, steps)                                  # draw the cost and steps
        pygame.display.flip()                                           # show what we just drew
        pygame.time.wait(400)                                           # pause between two states (ms)

    font = pygame.font.SysFont("arial", 16)
    prompt = font.render("Press R or Enter to choose another board, or Esc to quit.", True, (200, 205, 212))
    screen.blit(prompt, (10, screen.get_height() - 23))
    pygame.display.flip()

    choose_another = False
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_r, pygame.K_RETURN, pygame.K_KP_ENTER):
                    choose_another = True
                    break
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False
        if choose_another:
            break
        clock.tick(30)
    pygame.quit()
    return True


def run_gui():
    """Run the board/algorithm selection, solve the puzzle, and animate its solution."""
    while True:
        board_choice = choose_board()
        if board_choice is None:
            pygame.quit()
            return
        board_name, board = board_choice

        algorithm = choose_algorithm()
        if algorithm is None:
            pygame.quit()
            return

        solution, cost, steps = run_algorithm(algorithm, board)
        print(f"{board_name} | {algorithm} | expanded: {steps}")
        if solution is None:
            print("No solution found.")
            continue

        print(f"Solution cost: {cost}")
        deadlock_cells = None
        if "deadlock" in algorithm:
            deadlock_cells = findDeadCells(SokoPuzzle(board).board)
        if not animate_solution(solution, cost, steps, deadlock_cells):
            return
