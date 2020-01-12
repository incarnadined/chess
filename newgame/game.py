from pygame.locals import *
from random import randint
from pieces import *
import pygame

pygame.init()
game = Game()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()
colours = pygame.color.THECOLORS

all_sprites = pygame.sprite.Group()
for rank in game.board.array:
    for piece in rank:
        if piece != None:
            all_sprites.add(piece)

running = True
while running:
    if selected:
        selected.coords = pygame.mouse.get_pos()[0]-63//2, pygame.mouse.get_pos()[1]-63//2
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == MOUSEBUTTONDOWN and selected is False:
            for rank in game.board.array:
                for piece in rank:
                    if piece is not None:
                        if piece.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                            selected = piece
                            for place in selected.legalMoves(game.board):
                                coords = locate(place)
                                availablesquares.append(pygame.Rect(coords[0]+(62.5*3/8),coords[1]+(62.5*3/8),15.5125,15.5125))
        elif event.type == MOUSEBUTTONDOWN:
            coords = pygame.mouse.get_pos()
            legal = game.board.move(selected,square(coords),game.captured)
            if legal is False:
                # Snap piece back to it's square if it was an illegal move
                selected.coords = locate(selected.position)
            selected = False
            availablesquares = []

    # Draw the board
    screen.fill(colours['aquamarine'])
    cellsize = (SCREEN_HEIGHT-(SCREEN_HEIGHT/6))/8
    grid = pygame.Surface((cellsize*8, cellsize*8))
    grid.fill((110,48,35))
    for x in range(1, 36, 2):
        for y in range(1, 36, 2):
            rect = pygame.Rect(x*cellsize, y*cellsize, cellsize, cellsize)
            pygame.draw.rect(grid, (229,207,170), rect)
    for x in range(0, 36, 2):
        for y in range(0, 36, 2):
            rect = pygame.Rect(x*cellsize, y*cellsize, cellsize, cellsize)
            pygame.draw.rect(grid, (229,207,170), rect)
    screen.blit(grid, (50,50))

    # Draw the pieces
    for rank in game.board.array:
        for piece in rank:
            if piece is not None and piece is not selected:
                # If first time running, then define the images only once to speed it up
                if len(images) < 16:
                    images[piece.colour+piece.symbol] = pygame.transform.scale(pygame.image.load('../wikipedia/'+piece.colour+piece.symbol+'.png'), (63,63))
                screen.blit(images[piece.colour+piece.symbol], piece.coords)

    # Draw a little dot on each of the squares that the piece can move to
    for place in availablesquares:
        pygame.draw.ellipse(screen,colours['darksalmon'],place)

    # Show the pieces that have been taken on the side
    for piece in game.captured:
        screen.blit(images[piece.colour+piece.symbol], (randint(600,800), randint(50,500)))

    # Draw the selceted piece last so it shows above everything else
    if selected:
        screen.blit(images[selected.colour+selected.symbol], selected.coords)

    clock.tick(60)
    pygame.display.update()