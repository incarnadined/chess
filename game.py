from pygame.locals import *
from models import *
import pygame
from random import randint as rand

pygame.init()

#Set universal variables
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
purple = (84, 100, 137)
lightpurple = (153, 165, 193) 
blue = (0,0,128)
truepurple = (106,13,173)
turquoise = (53,153,255)
available_squares = []

# Set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()

selected = False
nomove = False
check = {'w':False,'b':False,'wt':False,'bt':False}
checkmate = False
loc = False
info = False
promotion = False
inforect = False
movespeed = 10
start = 0
randavailable = False
# Pawn promotion selection
prom = {}
#random = pygame.Rect(75,125,50,33)

board = Board()
all_sprites = pygame.sprite.Group()
for i in board.array:
    for j in i:
        if j != None:
            all_sprites.add(j)
font = pygame.font.Font('freesansbold.ttf', 32)
turn = Turn()
captured = Taken()

# Run until the user asks to quit
running = True
while running:
    if selected:
        #Check it is the turn of the moved piece
        if selected.colour == turn.colour:
            selected.coords = (pygame.mouse.get_pos()[0]-31.25,pygame.mouse.get_pos()[1]-31.25)
            for square in selected.legalMoves(board):
                coords = locate(square)
                available_squares.append(pygame.Rect(coords[0]+(62.5*3/8),coords[1]+(62.5*3/8),15.5125,15.5125))
        else:
            selected = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == MOUSEBUTTONUP:
            pass
        if event.type == MOUSEBUTTONDOWN and selected == False:
            for i in board.array:
                for j in i:
                    if j != None:
                        if j.rect.collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
                            selected = j
                            posj = i.index(j)
                            posi = board.array.index(i)
                            #print(posj,posi)
            for piece in prom:
                if prom[piece].collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
                    if piece == 'queen':
                        board.array[int(chessToMatrix(pawn.position)[0])][int(chessToMatrix(pawn.position)[1])] = Queen(pawn.colour, pawn.position)
                    if piece == 'rook':
                        board.array[int(chessToMatrix(pawn.position)[0])][int(chessToMatrix(pawn.position)[1])] = Rook(pawn.colour, pawn.position)
                    if piece == 'bish':
                        board.array[int(chessToMatrix(pawn.position)[0])][int(chessToMatrix(pawn.position)[1])] = Bishop(pawn.colour, pawn.position)
                    if piece == 'knight':
                        board.array[int(chessToMatrix(pawn.position)[0])][int(chessToMatrix(pawn.position)[1])] = Knight(pawn.colour, pawn.position)
                    promotion = False
                    pawn = False
            if inforect.collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
                if info == True:
                    info = False
                else:
                    info = True
                    start = 0
            if randomslider.collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
                if info is True:
                    if randavailable == True:
                        randavailable = False
                    else:
                        randavailable = True
        elif event.type == MOUSEBUTTONDOWN:
            board.updatefen(turn.colour)
            origpos = selected.position
            nomove, board = selected.move(coordToSquare(pygame.mouse.get_pos()),board)
            matrixloc = chessToMatrix(selected.position)                    

            if not nomove:
                board.array[posi][posj] = None
                #print(posi,posj)
                newsquare = board.array[int(matrixloc[0])][int(matrixloc[1])]
                if newsquare != None:
                    capture = True
                    captured.add(newsquare)
                board.array[int(matrixloc[0])][int(matrixloc[1])] = selected
                available_squares = []

                #Finish turn
                #check = checkCheck(board.fen)
                check = checkCheck(board, selected, coordToSquare(pygame.mouse.get_pos()), check)
                if check['w'] == True:
                    print(board.wk,board.bk)
                    king = board.array[int(chessToMatrix(board.wk)[0])][int(chessToMatrix(board.wk)[1])]
                    checkmate = checkMate(board, king, check)
                    checkmatecolour = 'w'
                elif check['b'] == True:
                    king = board.array[int(chessToMatrix(board.bk)[0])][int(chessToMatrix(board.bk)[1])]
                    checkmate = checkMate(board, king, check)
                    checkmatecolour = 'b'

                if check[turn.colour] == True:
                    if capture == True:
                        board.array[int(matrixloc[0])][int(matrixloc[1])] = captured.array[-1]
                        captured.remove()
                    else:
                        board.array[int(matrixloc[0])][int(matrixloc[1])] = None
                    board.array[posi][posj] = selected
                    selected.position = origpos
                    selected.coords = locate(selected.position)
                    selected.rect = pygame.Rect(selected.coords[0],selected.coords[1],63,63)
                    selected.poshistory.pop(-1)
                    if selected.symbol == 'K':
                        if selected.colour == 'w':
                            print(selected.position)
                            board.wk = selected.position
                        elif selected.colour == 'b':
                            board.bk = selected.position
                    check[turn.colour] = False
                else:
                    # Pawn promotion
                    if selected.symbol == 'P':
                        if chessToMatrix(selected.position)[0] == '0' or chessToMatrix(selected.position)[0] == '7':
                            selected.matrix = chessToMatrix(selected.position)
                            board.array[int(selected.matrix[0])][int(selected.matrix[1])] 
                            promotion = pygame.Surface((400,100))
                            promotion.fill(truepurple)
                            pygame.draw.rect(promotion, lightpurple, pygame.Rect(10,10,80,80))
                            pygame.draw.rect(promotion, lightpurple, pygame.Rect(110,10,80,80))
                            pygame.draw.rect(promotion, lightpurple, pygame.Rect(210,10,80,80))
                            pygame.draw.rect(promotion, lightpurple, pygame.Rect(310,10,80,80))
                            prom['knight'] = pygame.Rect(110,260,80,80)
                            prom['bish'] = pygame.Rect(210,260,80,80)
                            prom['rook'] = pygame.Rect(310,260,80,80)
                            prom['queen'] = pygame.Rect(410,260,80,80)
                            promotion.blit(pygame.transform.scale(pygame.image.load('wikipedia/'+selected.colour+'N.png'),(80,80)),(10,10))
                            promotion.blit(pygame.transform.scale(pygame.image.load('wikipedia/'+selected.colour+'B.png'),(80,80)),(110,10))
                            promotion.blit(pygame.transform.scale(pygame.image.load('wikipedia/'+selected.colour+'R.png'),(80,80)),(210,10))
                            promotion.blit(pygame.transform.scale(pygame.image.load('wikipedia/'+selected.colour+'Q.png'),(80,80)),(310,10))
                            pawn = selected

                    turn.completeTurn()
                    matrixloc = None
                    capture = False
                    selected = False

            if nomove:
                #Snap piece back to square
                selected.coords = locate(selected.position)
                selected = False
            #Remove available square indicator    
            available_squares = []            

            nomove = False
            selected = False

            #Reset for new piece selection
            
        
    
    # Fill the background with purple
    screen.fill(purple)

    # Draw the board
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
    
    screen.blit(grid,(50,50), grid.get_rect())

    #Initialise pieces
    for i in board.array:
        for j in i:
            if j != None:
                screen.blit(j.image,j.coords)

    #Display sidebar info
    sideBar = pygame.Surface((250,500))
    sideBar.fill(lightpurple)

    text = turn.visual('w',font,blue,purple)
    sideBar.blit(text, (75,25)) 
    text = turn.visual('b',font,blue,purple)
    sideBar.blit(text, (75,450)) 

    x = 10
    y = 400
    for piece in captured.black:
        x+=25
        if x > 185:
            x = 35
            y-= 30
        sideBar.blit(pygame.transform.scale(pygame.image.load('wikipedia/'+piece.colour+piece.symbol+'.png'),(30,30)),(x,y))
    x = 10
    y = 75
    for piece in captured.white:
        x+=25
        if x > 185:
            x = 35
            y+= 30
        sideBar.blit(pygame.transform.scale(pygame.image.load('wikipedia/'+piece.colour+piece.symbol+'.png'),(30,30)),(x,y))

    pygame.draw.line(sideBar, purple, (0,250), (250,250),3)

    if checkmate == True:
        if checkmatecolour == 'w':
            loc = (30,220)
            text = font.render('Checkmate!', True, truepurple)
        if checkmatecolour == 'b':
            loc = (30,275)
            text = font.render('Checkmate!', True, truepurple)
    elif check['w'] == True:
        loc = (75,220)
        text = font.render('Check', True, truepurple)
    elif check['b'] == True:
        loc = (75,275)
        text = font.render('Check', True, truepurple)
    
    if loc != False:
        sideBar.blit(text, loc) 
        loc = False
    screen.blit(sideBar, (600,50))

    for square in available_squares:
        if randavailable:
            pygame.draw.ellipse(screen,(rand(0,255),rand(0,255),rand(0,255)),square)
        else:
            pygame.draw.ellipse(screen,(255,0,0),square)
    
    if promotion:
        screen.blit(promotion,(100,250))


    infobar = pygame.Surface((875,550))
    infobar.fill(turquoise)
    random = pygame.draw.rect(infobar,(128,128,128),pygame.Rect(50,100,50,33))
    if randavailable == True:
        randomslider = pygame.draw.rect(infobar,(220,220,220),pygame.Rect(50,95,25,43))
        randomslider = pygame.Rect(75,125,25,43)
        text = font.render(' ON', True, (255,255,255), (0,255,0))
        infobar.blit(text, (75,100))
    if randavailable == False:
        randomslider = pygame.draw.rect(infobar,(220,220,220),pygame.Rect(115,95,25,43))
        randomslider = pygame.Rect(140,125,25,43)
        text = font.render('OFF', True, (255,255,255), (0,0,255))
        infobar.blit(text, (50,100))

    if info == False:
        infoarrow = pygame.Surface((25,50))
        infoarrow.fill(purple)
        pygame.draw.ellipse(infoarrow,turquoise,pygame.Rect(0,0,50,50))
        pygame.draw.polygon(infoarrow,(255,255,255), ((5,25),(20,50//3),(20,(50//3)*2)))
        screen.blit(infoarrow,(875,100))
        inforect = pygame.Rect(875,100,25,50)
    elif info == True:
        if 900-start >= 25:
            start+=movespeed
            screen.blit(infobar, (900-start,25))
        else:
            screen.blit(infobar, (25,25))        


    #screen.blit(grid, position)
    clock.tick(60)
    pygame.display.update()

    # Flip the display
    #pygame.display.flip()

# Done! Time to quit.
pygame.quit()