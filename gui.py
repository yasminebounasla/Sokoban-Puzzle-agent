import pygame

TILE = 64        # taille d'une case en pixels
INFO_H = 60      # hauteur de la bande d'info sous la grille

FILES = {
    "wall": "wall.png",
    "space": "space.png",
    "target": "target.png",
    "box": "box.png",
    "box_on_target": "box_on_target.png",
    "player": "player.png",
}


# download the images and scale them to TILE x TILE
def load_images():
    images = {}
    for name, file in FILES.items():
        img = pygame.image.load(file)                              # load image from file
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


# animate the solution path on the screen, with a pause between each state
def animate_solution(path, cost, steps):
    pygame.init()                                                       # start pygame
    rows = len(path[0].board)                                           # number of rows in the board
    cols = len(path[0].board[0])                                        # number of columns in the board
    screen = pygame.display.set_mode((cols * TILE, rows * TILE + INFO_H))  # create the window (board + info band)
    pygame.display.set_caption("Sokoban")                               # window title
    images = load_images()                                              # load the images once

    for state in path:                                                  # state = one picture of the board
        for event in pygame.event.get():                                # events = everything the user did
            if event.type == pygame.QUIT:                               # if the user closed the window, stop the animation
                pygame.quit()
                return
        screen.fill((30, 30, 30))                                       # gray background for the info band
        draw_board(screen, state, images)                               # draw the current state
        show_info(screen, cost, steps)                                  # draw the cost and steps
        pygame.display.flip()                                           # show what we just drew
        pygame.time.wait(400)                                           # pause between two states (ms)

    running = True                                                      # keep the window open at the end
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                               # wait until the user closes the window
                running = False
    pygame.quit()                                                       # close pygame
