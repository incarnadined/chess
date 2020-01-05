from pygame.locals import *
from models import *
import pygame

pygame.init()

#Set universal variables
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
purple = (84, 100, 137)
lightpurple = (153, 165, 193) 
blue = (0,0,128)
available_squares = []

# Set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()

selected = False
nomove = False
check = (False, )

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
                #print('square: ',square)
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
                    #print(i,j)
                    if j != None:
                        if j.rect.collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
                            selected = j
                            posj = i.index(j)
                            posi = board.array.index(i)
                            #print(posj,posi)
        elif event.type == MOUSEBUTTONDOWN:
            board.updatefen(turn.colour)
            print(selected.position)
            check = checkCheck(board, selected, coordToSquare(pygame.mouse.get_pos()), turn.colour)
            print(check)
            nomove, board = selected.move(coordToSquare(pygame.mouse.get_pos()),board)
            matrixloc = chessToMatrix(selected.position)

            if not nomove:
                board.array[posi][posj] = None
                #print(posi,posj)
                #print(matrixloc)
                newsquare = board.array[int(matrixloc[0])][int(matrixloc[1])]
                if newsquare != None:
                    captured.add(newsquare)
                board.array[int(matrixloc[0])][int(matrixloc[1])] = selected
                available_squares = []

                #Finish turn
                #check = checkCheck(board.fen)
                turn.completeTurn()
                selected = False
                matrixloc = None

            if nomove:
                #Snap piece back to square
                selected.coords = locate(selected.position)
                selected = False
            #Remove available square indicator    
            available_squares = []            

            nomove = False

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

    if check[0] == True:
        if check[1] == 'w':
            loc = (75,225)
        elif check[1] == 'b':
            loc = (75,275)
        text = font.render('Check', True, purple)
        sideBar.blit(text, loc) 
    screen.blit(sideBar, (600,50))

    for square in available_squares:
        pygame.draw.ellipse(screen,(255,0,0),square)

    #screen.blit(grid, position)
    clock.tick(60)
    pygame.display.update()

    # Flip the display
    #pygame.display.flip()

# Done! Time to quit.
pygame.quit()