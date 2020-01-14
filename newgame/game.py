from pygame.locals import *
from random import randint
from pieces import *
from minmax import *
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
    if game.colour == 'b' and game.computerlevel != 0:
        piece, move, pawnpromotion = airun(game.computerlevel, game.board)
        print(piece.position, piece.poshistory, piece.legalMoves(game.board))
        moved = game.board.move(piece, move, game)
        print(moved)
        if moved and piece.symbol == 'P' and matrix(move)[0] == '7':
            promote(game.board, piece, pawnpromotion)
        while moved == False: # The move would've done something bad to do with check
            piece, move, pawnpromotion = airun(game.computerlevel, game.board)
            print(piece, move)
            print(moved)
            moved = game.board.move(piece, move, game)
            if moved and piece.symbol == 'P' and matrix(move)[0] == 7:
                promote(game.board, piece, pawnpromotion)
            if checkMate(game.board, 'b') == True:
                print('AI in checkmate')
                break
        # Comment the next line for some fun
        game.turn()
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == MOUSEBUTTONDOWN and selected is False:
            for rank in game.board.array:
                for piece in rank:
                    if piece is not None:
                        if piece.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                            if piece.colour == game.colour:
                                if game.computerlevel != 0:
                                    if game.colour == 'w':
                                        selected = piece
                                        for place in selected.legalMoves(game.board):
                                            coords = locate(place)
                                            availablesquares.append(pygame.Rect(coords[0]+(62.5*3/8),coords[1]+(62.5*3/8),15.5125,15.5125))
                                else:
                                    selected = piece
                                    for place in selected.legalMoves(game.board):
                                        coords = locate(place)
                                        availablesquares.append(pygame.Rect(coords[0]+(62.5*3/8),coords[1]+(62.5*3/8),15.5125,15.5125))
            try:
                for piece in prom:
                    if prom[piece].collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
                        if piece == 'knight':
                            game.board.array[int(matrix(pawn.position)[0])][int(matrix(pawn.position)[1])] = Knight(pawn.position,pawn.colour)
                        elif piece == 'bish':
                            game.board.array[int(matrix(pawn.position)[0])][int(matrix(pawn.position)[1])] = Bishop(pawn.position,pawn.colour)
                        elif piece == 'rook':
                            game.board.array[int(matrix(pawn.position)[0])][int(matrix(pawn.position)[1])] = Rook(pawn.position,pawn.colour)
                        elif piece == 'queen':
                            game.board.array[int(matrix(pawn.position)[0])][int(matrix(pawn.position)[1])] = Queen(pawn.position,pawn.colour)
                        promotion = False
                        pawn = False
                        prom = {}
                        game.turn()
            except KeyError: #The list has been cleared
                pass
        elif event.type == MOUSEBUTTONDOWN:
            coords = pygame.mouse.get_pos()
            legal = game.board.move(selected, square(coords), game)
            if legal is False:
                # Snap piece back to it's square if it was an illegal move
                selected.coords = locate(selected.position)
            # Check if pawn has reached the back rank, if so create a surface for the promotion selection
            elif selected.symbol == 'P' and (selected.position[1] == '8' or selected.position[1] == '1'):
                promotion = pygame.Surface((400,100))
                pawn = selected
            elif promotion is not True:
                game.turn()
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

    # Draw the menu to select pieces
    if promotion:
        promotion.fill(colours['darkorange'])
        pygame.draw.rect(promotion, colours['deeppink'] , pygame.Rect(10,10,80,80))
        pygame.draw.rect(promotion, colours['deeppink'] , pygame.Rect(110,10,80,80))
        pygame.draw.rect(promotion, colours['deeppink'] , pygame.Rect(210,10,80,80))
        pygame.draw.rect(promotion, colours['deeppink'] , pygame.Rect(310,10,80,80))
        prom['knight'] = pygame.Rect(110,260,80,80)
        prom['bish'] = pygame.Rect(210,260,80,80)
        prom['rook'] = pygame.Rect(310,260,80,80)
        prom['queen'] = pygame.Rect(410,260,80,80)
        promotion.blit(pygame.transform.scale(pygame.image.load('../wikipedia/'+pawn.colour+'N.png'),(80,80)),(10,10))
        promotion.blit(pygame.transform.scale(pygame.image.load('../wikipedia/'+pawn.colour+'B.png'),(80,80)),(110,10))
        promotion.blit(pygame.transform.scale(pygame.image.load('../wikipedia/'+pawn.colour+'R.png'),(80,80)),(210,10))
        promotion.blit(pygame.transform.scale(pygame.image.load('../wikipedia/'+pawn.colour+'Q.png'),(80,80)),(310,10))
        screen.blit(promotion, (100,250))

    clock.tick(500)
    pygame.display.update()