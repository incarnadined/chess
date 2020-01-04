import pygame
import chess
import math

def number(letter):
    swap = {
        'a': '0',
        'b': '1',
        'c': '2',
        'd': '3',
        'e': '4',
        'f': '5',
        'g': '6',
        'h': '7'
    }
    try:
        return swap[letter]
    except:
        pass

def letter(number):
    swap = {
        '-1': None,
        '0': 'a',
        '1': 'b',
        '2': 'c',
        '3': 'd',
        '4': 'e',
        '5': 'f',
        '6': 'g',
        '7': 'h',
        '8': None
    }
    return swap[str(number)]

def locate(square):
    if square[0] == 'a':
        x = 50
    elif square[0] == 'b':
        x = 50 + (62.5*1)
    elif square[0] == 'c':
        x = 50 + (62.5*2)
    elif square[0] == 'd':
        x = 50 + (62.5*3)
    elif square[0] == 'e':
        x = 50 + (62.5*4)
    elif square[0] == 'f':
        x = 50 + (62.5*5)
    elif square[0] == 'g':
        x = 50 + (62.5*6)
    elif square[0] == 'h':
        x = 50 + (62.5*7)

    if square[1] == '8':
        y = 50
    elif square[1] == '7':
        y = 50 + (62.5*1)
    elif square[1] == '6':
        y = 50 + (62.5*2)
    elif square[1] == '5':
        y = 50 + (62.5*3)
    elif square[1] == '4':
        y = 50 + (62.5*4)
    elif square[1] == '3':
        y = 50 + (62.5*5)
    elif square[1] == '2':
        y = 50 + (62.5*6)
    elif square[1] == '1':
        y = 50 + (62.5*7)
    #print(x,y)
    return (int(x),int(y))

def coordToSquare(coord):
    x = coord[0]
    y = coord[1]

    # Find the square
    column = math.floor((x - 50)/62.5)
    row = math.floor((y-50)/62.5)
    if column < 8 and column >= 0 and row < 8 and row >= 0:
        #print(letter(column)+str((row-8)*-1))
        return letter(column)+str((row-8)*-1)
    else:
        #print(column,row)
        return '00'
        pass

def chessToMatrix(chess):
    row = str((int(chess[1]) - 8)*-1)
    column = number(chess[0])
    #print(row)
    #print(column)
    return row+column

def matrixToChess(matrix):
    if len(str(matrix)) == 1:
        matrix = '0'+str(matrix)
    matrix = str(matrix)
    print(matrix)
    if matrix[1] == '8' or matrix[1] == '9'or int(matrix)< 0:
        return None
    row = str((int(matrix[0]) - 8)*-1)
    column = letter(matrix[1])
    if int(row) > 0 and int(row) < 9 and column is not None:
        return column+row

class Turn():
    def __init__(self):
        self.colour = 'w'

    def completeTurn(self):
        if self.colour == 'w':
            self.colour = 'b'
        else:
            self.colour = 'w'

    def visual(self,colour,font,blue,purple):
        if self.colour == 'w' and colour == 'w':
            return font.render('White', True, blue)
        elif self.colour == 'w' and colour == 'b':
            return font.render('Black', True, purple)
        if self.colour == 'b' and colour == 'w':
            return font.render('White', True, purple)
        elif self.colour == 'b' and colour == 'b':
            return font.render('Black', True, blue)

class Taken():
    def __init__(self):
        self.array = []
        self.sort()

    def add(self,piece):
        self.array.append(piece)
        self.sort()
        print(self.white)

    def sort(self):
        self.white = []
        self.black = []
        for piece in self.array:
            if piece.colour == 'w':
                self.white.append(piece)
            if piece.colour == 'b':
                self.black.append(piece)

        self.white.sort(key=lambda x: x.value, reverse=True)
        self.black.sort(key=lambda x: x.value, reverse=True)

class King(pygame.sprite.Sprite):
    def __init__(self, colour, position):
        pygame.sprite.Sprite.__init__(self)
        self.value = 999
        self.colour = colour
        self.image = pygame.transform.scale(pygame.image.load('wikipedia/'+self.colour[0]+'K.png'),(63,63))
        self.position = position
        self.coords = locate(self.position)
        self.rect = pygame.Rect(self.coords[0],self.coords[1],63,63)
        self.symbol = 'K'
        self.poshistory = []

    def move(self,pos,board):
        if pos in self.legalMoves(board):
            self.poshistory.append(self.position)
            self.position = pos
            self.coords = locate(self.position)
            self.rect = pygame.Rect(self.coords[0],self.coords[1],63,63)
            if self.poshistory[-1] == self.position:
                return True
            else:
                return False
        else:
            return True
    
    def legalMoves(self,board):
        temp = []
        self.movement = []
        self.matrix = chessToMatrix(self.position)
        
        #Find all moves
        temp.append(matrixToChess(int(self.matrix)+11))
        temp.append(matrixToChess(int(self.matrix)+10))
        temp.append(matrixToChess(int(self.matrix)+9))
        temp.append(matrixToChess(int(self.matrix)+1))
        temp.append(matrixToChess(int(self.matrix)-1))
        temp.append(matrixToChess(int(self.matrix)-9))
        temp.append(matrixToChess(int(self.matrix)-10))
        temp.append(matrixToChess(int(self.matrix)-11))

        #Remove moves that go off the board
        for move in temp:
            #print(move,move)
            if move != None:
                self.movement.append(move)

        #Check if spaces are available
        self.spaces = {}
        for move in self.movement:
            piece = board.array[int(chessToMatrix(move)[0])][int(chessToMatrix(move)[1])]
            if piece is not None:
                self.spaces[move] = piece

        for i in list(self.spaces.keys()):
            piece = self.spaces[i]
            #print(self.spaces)
            #print(piece)
            if piece.colour == self.colour:
                j = self.movement.index(i)
                self.movement.pop(j)

        return self.movement

    def __repr__(self):
        if self.colour == 'w':
            return 'K'
        elif self.colour =='b':
            return 'k'

class Rook(pygame.sprite.Sprite):
    def __init__(self, colour, position):
        pygame.sprite.Sprite.__init__(self)
        self.value = 5
        self.colour = colour
        self.image = pygame.transform.scale(pygame.image.load('wikipedia/'+self.colour[0]+'R.png'),(63,63))
        self.position = position
        self.coords = locate(self.position)
        self.rect = pygame.Rect(self.coords[0],self.coords[1],63,63)
        self.symbol = 'R'
        self.poshistory = []

    def move(self,pos,board):
        if pos in self.legalMoves(board):
            self.poshistory.append(self.position)
            self.position = pos
            self.coords = locate(self.position)
            self.rect = pygame.Rect(self.coords[0],self.coords[1],63,63)
            if self.poshistory[-1] == self.position:
                return True
            else:
                return False
        else:
            return True

    def legalMoves(self,board):
        temp = []
        self.movement = []
        self.matrix = chessToMatrix(self.position)
        self.matrix = chessToMatrix(self.position)
        
        #Find all moves
        start = int(number(self.position[0]))
        #Find vertical possibilities
        for i in range(start,87,10):
            if i == start:
                temp.append(matrixToChess('0'+str(i)))
            else:
                temp.append(matrixToChess(i))
        #Find horizontal possibilities
        start = chessToMatrix(self.position)[0]
        #print('start: ',start)
        #print(int(start+'0'),' - ',int(start+'8'))
        for i in range(int(start+'0'),int(start+'8')):
            #print('i: ',i)
            if len(str(i)) == 2:
                temp.append(matrixToChess(i))
            else:
                temp.append(matrixToChess('0'+str(i)))

        #Remove moves that go off the board
        for move in temp:
            #print(move,move)
            if move != None:
                self.movement.append(move)

        #Remove yourself
        if self.position in self.movement:
            self.movement.pop(self.movement.index(self.position))

        #Check if spaces are available
        self.spaces = {}
        for move in self.movement:
            piece = board.array[int(chessToMatrix(move)[0])][int(chessToMatrix(move)[1])]
            if piece is not None:
                self.spaces[move] = piece

        for i in list(self.spaces.keys()):
            piece = self.spaces[i]
            #print(self.spaces)
            #print(piece)
            if piece.colour == self.colour:
                j = self.movement.index(i)
                self.movement.pop(j)

        return self.movement

    def __repr__(self):
        if self.colour == 'w':
            return 'R'
        elif self.colour =='b':
            return 'r'

class Knight(pygame.sprite.Sprite):
    def __init__(self, colour, position):
        pygame.sprite.Sprite.__init__(self)
        self.value = 3
        self.colour = colour
        self.image = pygame.transform.scale(pygame.image.load('wikipedia/'+self.colour[0]+'N.png'),(63,63))
        self.position = position
        self.coords = locate(self.position)
        self.rect = pygame.Rect(self.coords[0],self.coords[1],63,63)
        self.symbol = 'N'
        self.poshistory = []

    def move(self,pos,board):
        if pos in self.legalMoves(board):
            self.poshistory.append(self.position)
            self.position = pos
            self.coords = locate(self.position)
            self.rect = pygame.Rect(self.coords[0],self.coords[1],63,63)
            if self.poshistory[-1] == self.position:
                return True
            else:
                return False
        else:
            return True

    def legalMoves(self,board):
        temp = []
        self.movement = []
        self.matrix = chessToMatrix(self.position)
        self.matrix = chessToMatrix(self.position)
        
        #Find all moves
        print(self.matrix)
        temp.append(matrixToChess(int(self.matrix)+11))
        temp.append(matrixToChess(int(self.matrix)+10))
        temp.append(matrixToChess(int(self.matrix)+9))
        if len(str(int(self.matrix)+1)) == 1:
            temp.append(matrixToChess('0'+str(int(self.matrix)+1)))
        if len(str(int(self.matrix)-1)) == 1:
            temp.append(matrixToChess('0'+str(int(self.matrix)-1)))
        if len(str(int(self.matrix)-9)) == 1:
            temp.append(matrixToChess('0'+str(int(self.matrix)-9)))
        if len(str(int(self.matrix)-10)) == 1:
            temp.append(matrixToChess('0'+str(int(self.matrix)-10)))
        if len(str(int(self.matrix)-11)) == 1:
            temp.append(matrixToChess('0'+str(int(self.matrix)-11)))

        #Remove moves that go off the board
        for move in temp:
            #print(move,move)
            if move != None:
                self.movement.append(move)

        #Check if spaces are available
        self.spaces = {}
        for move in self.movement:
            piece = board.array[int(chessToMatrix(move)[0])][int(chessToMatrix(move)[1])]
            if piece is not None:
                self.spaces[move] = piece

        for i in list(self.spaces.keys()):
            piece = self.spaces[i]
            #print(self.spaces)
            #print(piece)
            if piece.colour == self.colour:
                j = self.movement.index(i)
                self.movement.pop(j)

        return self.movement
    
    def __repr__(self):
        if self.colour == 'w':
            return 'N'
        elif self.colour =='b':
            return 'n'

class Bishop(pygame.sprite.Sprite):
    def __init__(self, colour, position):
        pygame.sprite.Sprite.__init__(self)
        self.value = 4
        self.colour = colour
        self.image = pygame.transform.scale(pygame.image.load('wikipedia/'+self.colour[0]+'B.png'),(63,63))
        self.position = position
        self.coords = locate(self.position)
        self.rect = pygame.Rect(self.coords[0],self.coords[1],63,63)
        self.symbol = 'B'
        self.poshistory = []

    def move(self,pos,board):
        if pos in self.legalMoves(board):
            self.poshistory.append(self.position)
            self.position = pos
            self.coords = locate(self.position)
            self.rect = pygame.Rect(self.coords[0],self.coords[1],63,63)
            if self.poshistory[-1] == self.position:
                return True
            else:
                return False
        else:
            return True

    def legalMoves(self,board):
        temp = []
        self.movement = []
        self.matrix = chessToMatrix(self.position)
        self.matrix = chessToMatrix(self.position)
        
        #Find all moves
        for i in range(-11,-99,-11):
            #if len(str(i)) == 0:
            print(str(i))
            temp.append(matrixToChess(int(self.matrix)+i))
        temp.append(matrixToChess(int(self.matrix)+11))
        temp.append(matrixToChess(int(self.matrix)+10))
        temp.append(matrixToChess(int(self.matrix)+9))
        temp.append(matrixToChess(int(self.matrix)+1))
        temp.append(matrixToChess(int(self.matrix)-1))
        temp.append(matrixToChess(int(self.matrix)-9))
        temp.append(matrixToChess(int(self.matrix)-10))
        temp.append(matrixToChess(int(self.matrix)-11))

        #Remove moves that go off the board
        for move in temp:
            #print(move,move)
            if move != None:
                self.movement.append(move)

        #Check if spaces are available
        self.spaces = {}
        for move in self.movement:
            piece = board.array[int(chessToMatrix(move)[0])][int(chessToMatrix(move)[1])]
            if piece is not None:
                self.spaces[move] = piece

        for i in list(self.spaces.keys()):
            piece = self.spaces[i]
            #print(self.spaces)
            #print(piece)
            if piece.colour == self.colour:
                j = self.movement.index(i)
                self.movement.pop(j)

        return self.movement
    
    def __repr__(self):
        if self.colour == 'w':
            return 'B'
        elif self.colour =='b':
            return 'b'

class Queen(pygame.sprite.Sprite):
    def __init__(self, colour, position):
        pygame.sprite.Sprite.__init__(self)
        self.value = 9
        self.colour = colour
        self.image = pygame.transform.scale(pygame.image.load('wikipedia/'+self.colour[0]+'Q.png'),(63,63))
        self.position = position
        self.coords = locate(self.position)
        self.rect = pygame.Rect(self.coords[0],self.coords[1],63,63)
        self.symbol = 'Q'
        self.poshistory = []

    def move(self,pos,board):
        if pos in self.legalMoves(board):
            self.poshistory.append(self.position)
            self.position = pos
            self.coords = locate(self.position)
            self.rect = pygame.Rect(self.coords[0],self.coords[1],63,63)
            if self.poshistory[-1] == self.position:
                return True
            else:
                return False
        else:
            return True

    def legalMoves(self,board):
        temp = []
        self.movement = []
        self.matrix = chessToMatrix(self.position)
        self.matrix = chessToMatrix(self.position)
        
        #Find all moves
        temp.append(matrixToChess(int(self.matrix)+11))
        temp.append(matrixToChess(int(self.matrix)+10))
        temp.append(matrixToChess(int(self.matrix)+9))
        temp.append(matrixToChess(int(self.matrix)+1))
        temp.append(matrixToChess(int(self.matrix)-1))
        temp.append(matrixToChess(int(self.matrix)-9))
        temp.append(matrixToChess(int(self.matrix)-10))
        temp.append(matrixToChess(int(self.matrix)-11))

        #Remove moves that go off the board
        for move in temp:
            #print(move,move)
            if move != None:
                self.movement.append(move)

        #Check if spaces are available
        self.spaces = {}
        for move in self.movement:
            piece = board.array[int(chessToMatrix(move)[0])][int(chessToMatrix(move)[1])]
            if piece is not None:
                self.spaces[move] = piece

        for i in list(self.spaces.keys()):
            piece = self.spaces[i]
            #print(self.spaces)
            #print(piece)
            if piece.colour == self.colour:
                j = self.movement.index(i)
                self.movement.pop(j)

        return self.movement
    
    def __repr__(self):
        if self.colour == 'w':
            return 'Q'
        elif self.colour =='b':
            return 'q'

class Pawn(pygame.sprite.Sprite):
    def __init__(self, colour, position):
        pygame.sprite.Sprite.__init__(self)
        self.value = 1
        self.colour = colour
        self.image = pygame.transform.scale(pygame.image.load('wikipedia/'+self.colour[0]+'P.png'),(63,63))
        self.position = position
        self.coords = locate(self.position)
        self.rect = pygame.Rect(self.coords[0],self.coords[1],63,63)
        self.symbol = 'P'
        self.poshistory = []

    def move(self,pos,board):
        if pos in self.legalMoves(board):
            self.poshistory.append(self.position)
            self.position = pos
            self.coords = locate(self.position)
            self.rect = pygame.Rect(self.coords[0],self.coords[1],63,63)
            if self.poshistory[-1] == self.position:
                return True
            else:
                return False
        else:
            return True

    def legalMoves(self,board):
        temp = []
        self.movement = []
        self.matrix = chessToMatrix(self.position)
        #print(self.matrix)
        
        #Find all moves
        if self.colour == 'w':
            temp.append(matrixToChess(int(self.matrix)-10))
            #Move 2 squares from start
            if len(self.poshistory) == 0:
                temp.append(matrixToChess(int(self.matrix)-20))
        if self.colour == 'b':
            temp.append(matrixToChess(int(self.matrix)+10))
            #Move 2 squares from start
            if len(self.poshistory) == 0:
                temp.append(matrixToChess(int(self.matrix)+20))

        #Attacking moves
        if self.colour == 'w':
            left = str(int(self.matrix)-11)
            right = str(int(self.matrix)-9)
            
            if left[1] == '8' or left[1] == '9':
                pass
            elif board.array[int(left[0])][int(left[1])] != None:
                temp.append(matrixToChess(left))
            if right[1] == '8' or right[1] == '9':
                pass
            elif board.array[int(right[0])][int(right[1])] != None:
                temp.append(matrixToChess(right))
        else:
            left = str(int(self.matrix)+11)
            if len(left) == 1:
                left = '0'+left
            right = str(int(self.matrix)+9)
            if len(right) == 1:
                right = '0'+right
            print('left: ',left)

            if left[1] == '8' or left[1] == '9':
                pass
            elif board.array[int(left[0])][int(left[1])] != None:
                temp.append(matrixToChess(left))
            if right[1] == '8' or right[1] == '9':
                pass
            elif board.array[int(right[0])][int(right[1])] != None:
                temp.append(matrixToChess(right))

        #Remove moves that go off the board
        for move in temp:
            #print(move,move)
            if move != None:
                self.movement.append(move)

        #Check if spaces are available
        self.spaces = {}
        for move in self.movement:
            piece = board.array[int(chessToMatrix(move)[0])][int(chessToMatrix(move)[1])]
            if piece is not None:
                self.spaces[move] = piece

        for i in list(self.spaces.keys()):
            piece = self.spaces[i]
            #print(self.spaces)
            #print(piece)
            if piece.colour == self.colour:
                j = self.movement.index(i)
                self.movement.pop(j)

        #print(self.movement)
        #print(self.poshistory)
        return self.movement
    
    def __repr__(self):
        if self.colour == 'w':
            return 'P'
        elif self.colour =='b':
            return 'p'


class Board():
    def __init__(self):
        self.array = [
            [Rook('b', 'a8'),Knight('b','b8'),Bishop('b','c8'),Queen('b','d8'),King('b','e8'),Bishop('b','f8'),Knight('b','g8'),Rook('b','h8')],
            [Pawn('b', 'a7'),Pawn('b','b7'),Pawn('b','c7'),Pawn('b','d7'),Pawn('b','e7'),Pawn('b','f7'),Pawn('b','g7'),Pawn('b','h7')],
            [None for x in range(8)],
            [None for x in range(8)],
            [None for x in range(8)],
            [None for x in range(8)],
            [Pawn('w','a2'),Pawn('w','b2'),Pawn('w','c2'),Pawn('w','d2'),Pawn('w','e2'),Pawn('w','f2'),Pawn('w','g2'),Pawn('w','h2')],
            [Rook('w','a1'),Knight('w','b1'),Bishop('w','c1'),Queen('w','d1'),King('w','e1'),Bishop('w','f1'),Knight('w','g1'),Rook('w','h1')]
        ]

#class Bishop():
#a = King('w')
#a.legalMoves()