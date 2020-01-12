from random import randint as rand
from pygame.locals import *
from models import *
from minmax import *
import pygame

pygame.init()

#Set universal variables
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
purple = (84, 100, 137)
lightpurple = (153, 165, 193) 
blue = (0,0,128)
truepurple = (106,13,173)
turquoise = (53,153,255)
pink = (204, 0, 204)
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
randavailable = False
aislider = False
aisliderx = 20
holding = False
computerlevel = 0
restart = False
pawn = 0
capture = False
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
fontinfo = pygame.font.Font('freesansbold.ttf', 20)
turn = Turn()
captured = Taken()

# Run until the user asks to quit
running = True
while running:
    if selected:
        #Check it is the turn of the moved piece
        # Check an AI is not playing
        if computerlevel == 0:
            if selected.colour == turn.colour:
                selected.coords = (pygame.mouse.get_pos()[0]-31.25,pygame.mouse.get_pos()[1]-31.25)
                for square in selected.legalMoves(board):
                    coords = locate(square)
                    available_squares.append(pygame.Rect(coords[0]+(62.5*3/8),coords[1]+(62.5*3/8),15.5125,15.5125))
            else:
                selected = False
        elif selected.colour == turn.colour and turn.colour == 'w':
            selected.coords = (pygame.mouse.get_pos()[0]-31.25,pygame.mouse.get_pos()[1]-31.25)
            for square in selected.legalMoves(board):
                coords = locate(square)
                available_squares.append(pygame.Rect(coords[0]+(62.5*3/8),coords[1]+(62.5*3/8),15.5125,15.5125))
        else:
            selected = False
    '''if computerlevel != 0 and turn.colour == 'b':
        print(computerlevel)
        selected, aimove = airun(computerlevel, board)  
        print(selected[0],aimove)
        selected[0].move(aimove, board, check, captured, turn, capture)
        if board.array[int(chessToMatrix(aimove)[0])][int(chessToMatrix(aimove)[1])] != selected:
            selected, move = airun(computerlevel, board)
            selected[0].move(aimove, board, check, captured, turn, capture)
        selected = False'''

    # Slider
    if holding == True:
        if pygame.mouse.get_pos()[0]-709 <= 170 and pygame.mouse.get_pos()[0]-709 >= 20:
            aisliderx = pygame.mouse.get_pos()[0]-709
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == MOUSEBUTTONUP:
            if holding == True:
                holding = False
        if event.type == MOUSEBUTTONDOWN and selected == False:
            for i in board.array:
                for j in i:
                    if j != None:
                        if j.rect.collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
                            selected = j
                            posj = i.index(j)
                            posi = board.array.index(i)
                            #print(posj,posi)
            if pawn:
                for piece in prom:
                    if prom[piece].collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
                        if piece == 'queen':
                            board.array[int(chessToMatrix(pawn.position)[0])][int(chessToMatrix(pawn.position)[1])] = Queen(pawn.colour, pawn.position)
                            check = checkCheck(board, pawn, 'uneeded param', check)
                            if check['w'] == True:
                                king = board.array[int(chessToMatrix(board.wk)[0])][int(chessToMatrix(board.wk)[1])]
                                checkmate = checkMate(board, king, check)
                                checkmatecolour = 'w'
                            elif check['b'] == True:
                                king = board.array[int(chessToMatrix(board.bk)[0])][int(chessToMatrix(board.bk)[1])]
                                checkmate = checkMate(board, king, check)
                                checkmatecolour = 'b'
                            promotion = False
                            pawn = False
                        if piece == 'rook':
                            board.array[int(chessToMatrix(pawn.position)[0])][int(chessToMatrix(pawn.position)[1])] = Rook(pawn.colour, pawn.position)
                            check = checkCheck(board, pawn, 'uneeded param', check)
                            if check['w'] == True:
                                king = board.array[int(chessToMatrix(board.wk)[0])][int(chessToMatrix(board.wk)[1])]
                                checkmate = checkMate(board, king, check)
                                checkmatecolour = 'w'
                            elif check['b'] == True:
                                king = board.array[int(chessToMatrix(board.bk)[0])][int(chessToMatrix(board.bk)[1])]
                                checkmate = checkMate(board, king, check)
                                checkmatecolour = 'b'
                            promotion = False
                            pawn = False
                        if piece == 'bish':
                            board.array[int(chessToMatrix(pawn.position)[0])][int(chessToMatrix(pawn.position)[1])] = Bishop(pawn.colour, pawn.position)
                            if check['w'] == True:
                                king = board.array[int(chessToMatrix(board.wk)[0])][int(chessToMatrix(board.wk)[1])]
                                checkmate = checkMate(board, king, check)
                                checkmatecolour = 'w'
                            elif check['b'] == True:
                                king = board.array[int(chessToMatrix(board.bk)[0])][int(chessToMatrix(board.bk)[1])]
                                checkmate = checkMate(board, king, check)
                                checkmatecolour = 'b'
                            check = checkCheck(board, pawn, 'uneeded param', check)
                            promotion = False
                            pawn = False
                        if piece == 'knight':
                            board.array[int(chessToMatrix(pawn.position)[0])][int(chessToMatrix(pawn.position)[1])] = Knight(pawn.colour, pawn.position)
                            if check['w'] == True:
                                king = board.array[int(chessToMatrix(board.wk)[0])][int(chessToMatrix(board.wk)[1])]
                                checkmate = checkMate(board, king, check)
                                checkmatecolour = 'w'
                            elif check['b'] == True:
                                king = board.array[int(chessToMatrix(board.bk)[0])][int(chessToMatrix(board.bk)[1])]
                                checkmate = checkMate(board, king, check)
                                checkmatecolour = 'b'
                            check = checkCheck(board, pawn, 'uneeded param', check)
                            promotion = False
                            pawn = False
            if inforect.collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
                if info == True:
                    info = False
                elif info == False:
                    info = True
            if aislider:
                if aislider.collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):    
                    holding = True
            if restart:
                if restart.collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
                    board.restart(turn, captured)
        elif event.type == MOUSEBUTTONDOWN:
            nomove = selected.move(coordToSquare(pygame.mouse.get_pos()),board, check, captured, turn, capture)
            
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

    text = turn.visual('b',font,blue,purple)
    sideBar.blit(text, (75,25)) 
    text = turn.visual('w',font,blue,purple)
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
        if checkmatecolour == 'b':
            loc = (30,220)
            text = font.render('Checkmate!', True, truepurple)
        if checkmatecolour == 'w':
            loc = (30,275)
            text = font.render('Checkmate!', True, truepurple)
    elif check['b'] == True:
        loc = (75,220)
        text = font.render('Check', True, truepurple)
    elif check['w'] == True:
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

    # Create options menu on the right side
    if info == False:
        aislider = False
        restart = False

        infoarrow = pygame.Surface((25,50))
        infoarrow.fill(purple)
        pygame.draw.ellipse(infoarrow,truepurple,pygame.Rect(0,0,50,50))
        pygame.draw.polygon(infoarrow,(255,255,255), ((5,25),(20,50//3),(20,(50//3)*2)))
        screen.blit(infoarrow,(875,100))
        inforect = pygame.Rect(875,100,25,50)
    if info == True:
        infobar = pygame.Surface((200,600))
        infobar.fill(truepurple)

        cross = pygame.transform.scale(pygame.image.load('x.png'), (40,40))
        inforect = pygame.Rect(850,10,40,40)
        infobar.blit(cross, (150, 10))

        # Draw the slider to alter AI level, aisliderx has a range of 20-170 meaning a division of 40 gives us the values 0-4 inclusive (0 is off)
        pygame.draw.rect(infobar, purple, pygame.Rect(20,85,160,3))
        pygame.draw.ellipse(infobar, pink, pygame.Rect(aisliderx, 77, 19,19))
        aislider = pygame.Rect(aisliderx+700,77,19,19)
        
        computerlevel = aisliderx//40
        ai = fontinfo.render('Computer Level: '+str(computerlevel), True, purple)
        infobar.blit(ai, (10,55))

        pygame.draw.rect(infobar, pink, pygame.Rect(20, 540, 160, 40), 5)
        restart = pygame.Rect(720, 540, 160, 40)
        restartext = font.render('Restart', True, pink)
        infobar.blit(restartext, (40,545))

        screen.blit(infobar,(700,0))


    #screen.blit(grid, position)
    clock.tick(60)
    pygame.display.update()

    # Flip the display
    #pygame.display.flip()

# Done! Time to quit.
pygame.quit()