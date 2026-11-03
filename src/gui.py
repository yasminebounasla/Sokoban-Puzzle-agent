import pygame
from pathlib import Path

from src.deadlock import findDeadCells
from src.heuristics import heuristic
from src.node import Node
from src.search import Search, board1, board2, board3, board4, board5, board6, board7
from src.sokoPuzzle import SokoPuzzle

TILE = 64        # taille d'une case en pixels
HEADER_H = 50    # hauteur de la bande de titre au-dessus de la grille
INFO_H = 110     # hauteur de la bande d'info sous la grille
MIN_W = 560      # largeur minimale de la fenetre (les petits plateaux sont centres)
MENU_SIZE = (800, 600)

# colors of the window
BG = (26, 31, 40)          # background
PANEL = (36, 44, 56)       # title band and info band
ACCENT = (72, 112, 153)    # blue lines
WHITE = (245, 245, 245)
GRAY = (160, 168, 178)

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
        screen.fill(BG)
        heading = title_font.render(title, True, WHITE)
        screen.blit(heading, heading.get_rect(center=(MENU_SIZE[0] // 2, 55)))

        for index, (option, rect) in enumerate(zip(options, button_rects)):
            hovered = rect.collidepoint(mouse_pos)
            color = ACCENT if hovered else (48, 62, 78)
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


# draw the title band at the top: board name + algorithm
def show_header(screen, title):
    width = screen.get_width()
    pygame.draw.rect(screen, PANEL, (0, 0, width, HEADER_H))                    # band background
    pygame.draw.line(screen, ACCENT, (0, HEADER_H - 1), (width, HEADER_H - 1), 2)  # blue line under it
    font = pygame.font.SysFont("arial", 24, bold=True)
    text = font.render(title, True, WHITE)
    screen.blit(text, text.get_rect(center=(width // 2, HEADER_H // 2)))        # title centered


# display cost, steps and progress in the info band at the bottom of the window
def show_info(screen, cost, steps, move, total):
    top = screen.get_height() - INFO_H                                          # y where the info band starts
    pygame.draw.rect(screen, PANEL, (0, top, screen.get_width(), INFO_H))       # band background
    pygame.draw.line(screen, ACCENT, (0, top), (screen.get_width(), top), 2)    # blue line above it
    label_font = pygame.font.SysFont("arial", 15)
    value_font = pygame.font.SysFont("arial", 26, bold=True)
    items = (("COST", cost), ("STEPS", steps), ("MOVE", f"{move} / {total}"))   # 3 columns
    column = screen.get_width() // len(items)
    for k, (label, value) in enumerate(items):
        x = k * column + column // 2                                            # center of the column
        label_text = label_font.render(label, True, GRAY)
        value_text = value_font.render(str(value), True, WHITE)
        screen.blit(label_text, label_text.get_rect(center=(x, top + 18)))      # small gray label
        screen.blit(value_text, value_text.get_rect(center=(x, top + 44)))      # big white value


# small legend that explains the deadlock colors
def show_legend(screen):
    top = screen.get_height() - INFO_H
    font = pygame.font.SysFont("arial", 15)
    x = 12
    for color, name in (((230, 45, 45), "corner deadlock"), ((245, 205, 45), "line deadlock")):
        pygame.draw.rect(screen, color, (x, top + 68, 14, 14))                  # colored square
        screen.blit(font.render(name, True, GRAY), (x + 22, top + 67))          # its name
        x += 200


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
def animate_solution(path, cost, steps, deadlock_cells=None, title=""):
    pygame.init()                                                       # start pygame
    rows = len(path[0].board)                                           # number of rows in the board
    cols = len(path[0].board[0])                                        # number of columns in the board
    board_w, board_h = cols * TILE, rows * TILE                         # size of the grid in pixels
    win_w = max(board_w, MIN_W)                                         # small boards are centered in the window
    screen = pygame.display.set_mode((win_w, HEADER_H + board_h + INFO_H))  # title band + grid + info band
    pygame.display.set_caption("Sokoban")                               # window title
    images = load_images()                                              # load the images once
    corners, lines = deadlock_cells or (set(), set())
    board_surface = pygame.Surface((board_w, board_h))                  # the grid is drawn here, then centered
    board_pos = ((win_w - board_w) // 2, HEADER_H)                      # where the grid goes in the window

    for move, state in enumerate(path):                                 # state = one picture of the board
        for event in pygame.event.get():                                # events = everything the user did
            if event.type == pygame.QUIT:                               # if the user closed the window, stop the animation
                pygame.quit()
                return False
        screen.fill(BG)                                                 # background color
        show_header(screen, title)                                      # board name + algorithm
        draw_board(board_surface, state, images)                        # draw the current state on the grid surface
        draw_deadlocks(board_surface, corners, lines)                   # deadlock colors (empty if not used)
        screen.blit(board_surface, board_pos)                           # put the grid in the middle of the window
        pygame.draw.rect(screen, ACCENT, (*board_pos, board_w, board_h), 2)  # blue frame around the grid
        show_info(screen, cost, steps, move, len(path) - 1)             # cost, steps and move number
        if corners or lines:
            show_legend(screen)                                         # explain the colors
        pygame.display.flip()                                           # show what we just drew
        pygame.time.wait(400)                                           # pause between two states (ms)

    font = pygame.font.SysFont("arial", 16)
    prompt = font.render("Press R or Enter to choose another board, or Esc to quit.", True, (200, 205, 212))
    screen.blit(prompt, (12, screen.get_height() - 24))
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
        title = f"{board_name}  |  {algorithm}"
        if not animate_solution(solution, cost, steps, deadlock_cells, title):
            return