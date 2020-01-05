import pygame
import chess
import math
import copy


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
    #print('\n')
    #print(chess)
    row = str((int(chess[1]) - 8)*-1)
    column = number(chess[0])
    #print(row)
    #print(column)
    return row+column


def matrixToChess(matrix):
    if len(str(matrix)) == 1:
        matrix = '0'+str(matrix)
    matrix = str(matrix)
    #print(matrix)
    if matrix[1] == '8' or matrix[1] == '9'or int(matrix)< 0:
        return None
    row = str((int(matrix[0]) - 8)*-1)
    column = letter(matrix[1])
    if int(row) > 0 and int(row) < 9 and column is not None:
        return column+row #c7


def checkCheck(board, piece, mov, colour):
    captured = []
    matrix = chessToMatrix(piece.position)
    newmat = chessToMatrix(mov)
    piece.move(mov,board)

    board.array[int(matrix[0])][int(matrix[1])] = None
    newsquare = board.array[int(newmat[0])][int(newmat[0])]
    if newsquare != None:
        captured.append(newsquare)
    board.array[int(newmat[0])][int(newmat[1])] = piece

    if colour == 'w':
        kingloc = board.wk
    elif colour == 'b':
        kingloc = board.bk

    for item in board.array:
        for ite in item:
            if ite is not None:
                if kingloc in ite.legalMoves(board):
                    piece.position = piece.poshistory[-1]
                    piece.poshistory.pop(-1)
                    piece.coords = locate(piece.position)
                    piece.rect = pygame.Rect(piece.coords[0],piece.coords[1],63,63)

                    board.array[int(matrix[0])][int(matrix[1])] = piece
                    newsquare = board.array[int(newmat[0])][int(newmat[0])]
                    if len(captured) != 0:
                        board.array[int(newmat[0])][int(newmat[1])] = captured[0]
                    else:
                        board.array[int(newmat[0])][int(newmat[1])] = None
                    return (True,colour)

    piece.position = piece.poshistory[-1]
    piece.poshistory.pop(-1)
    piece.coords = locate(piece.position)
    piece.rect = pygame.Rect(piece.coords[0],piece.coords[1],63,63)
    
    board.array[int(matrix[0])][int(matrix[1])] = piece
    newsquare = board.array[int(newmat[0])][int(newmat[0])]
    if len(captured) != 0:
        board.array[int(newmat[0])][int(newmat[1])] = captured[0]
    else:
        board.array[int(newmat[0])][int(newmat[1])] = None
    return (False,colour)


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
        self.matrix = chessToMatrix(self.position)

    def move(self,pos,board):
        if pos in self.legalMoves(board):
            self.poshistory.append(self.position)
            self.position = pos
            self.coords = locate(self.position)
            self.rect = pygame.Rect(self.coords[0],self.coords[1],63,63)
            if self.colour == 'w':
                board.wk = self.position
            elif self.colour == 'b':
                board.bk = self.position
            if self.poshistory[-1] == self.position:
                return True, board
            else:
                return False, board
        else:
            return True, board
    
    def legalMoves(self,board):
        self.temp = []
        self.movement = []
        self.matrix = chessToMatrix(self.position)
        
        #Find all moves
        self.temp.append(matrixToChess(int(self.matrix)+11))
        self.temp.append(matrixToChess(int(self.matrix)+10))
        self.temp.append(matrixToChess(int(self.matrix)+9))
        self.temp.append(matrixToChess(int(self.matrix)+1))
        self.temp.append(matrixToChess(int(self.matrix)-1))
        self.temp.append(matrixToChess(int(self.matrix)-9))
        self.temp.append(matrixToChess(int(self.matrix)-10))
        self.temp.append(matrixToChess(int(self.matrix)-11))

        #Remove moves that go off the board
        for move in self.temp:
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
        self.matrix = chessToMatrix(self.position)

    def move(self,pos,board):
        if pos in self.legalMoves(board):
            self.poshistory.append(self.position)
            self.position = pos
            self.coords = locate(self.position)
            self.rect = pygame.Rect(self.coords[0],self.coords[1],63,63)
            if self.poshistory[-1] == self.position:
                return True, board
            else:
                return False, board
        else:
            return True, board

    def legalMoves(self,board):
        self.temp = []
        self.movement = []
        self.matrix = chessToMatrix(self.position)
        

        #Find all moves
        start = int(chessToMatrix(self.position)[1])
        start1 = int(chessToMatrix(self.position)[0])
        #Find vertical-up possibilities
        for i in range(start1,-1,-1):
            self.temp.append(matrixToChess(str(i)+str(start)))
            if matrixToChess(str(i)+str(start)) == self.position:
                pass
            elif board.array[i][start] != None:
                break
        # Find veritcal-down possibilities
        for i in range(start1+1,8,1):
            self.temp.append(matrixToChess(str(i)+str(start)))
            if matrixToChess(str(i)+str(start)) == self.position:
                pass
            elif board.array[i][start] != None:
                break

        #Find horizontal-left possibilities
        start = int(chessToMatrix(self.position)[0])
        start1 = int(chessToMatrix(self.position)[1])
        for i in range(start1,-1,-1):
            self.temp.append(matrixToChess(str(start)+str(i)))
            if matrixToChess(str(start)+str(i)) == self.position:
                pass
            elif board.array[start][i] != None:
                break
        # Find horizontal-right possibilities
        for i in range(start1,8,1):
            self.temp.append(matrixToChess(str(start)+str(i)))
            if matrixToChess(str(start)+str(i)) == self.position:
                pass
            elif board.array[start][i] != None:
                break

        #Remove moves that go off the board
        for move in self.temp:
            if move is not None:
                self.movement.append(move)          

        #Remove yourself
        #print(self.movement)
        #print(self.position)
        while self.position in self.movement:
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
        self.matrix = chessToMatrix(self.position)

    def move(self,pos,board):
        if pos in self.legalMoves(board):
            self.poshistory.append(self.position)
            self.position = pos
            self.coords = locate(self.position)
            self.rect = pygame.Rect(self.coords[0],self.coords[1],63,63)
            if self.poshistory[-1] == self.position:
                return True, board
            else:
                return False, board
        else:
            return True, board

    def legalMoves(self,board):
        self.temp = []
        self.movement = []
        self.matrix = chessToMatrix(self.position)
        self.matrix = chessToMatrix(self.position)
        
        #Find all moves
        self.temp.append(matrixToChess(int(self.matrix)+21))
        self.temp.append(matrixToChess(int(self.matrix)+19))
        self.temp.append(matrixToChess(int(self.matrix)+12))
        self.temp.append(matrixToChess(int(self.matrix)+8))
        self.temp.append(matrixToChess(int(self.matrix)-8))
        self.temp.append(matrixToChess(int(self.matrix)-12))
        self.temp.append(matrixToChess(int(self.matrix)-21))
        self.temp.append(matrixToChess(int(self.matrix)-19))

        #Remove moves that go off the board
        for move in self.temp:
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
        self.image = pygame.transform.scale(
            pygame.image.load('wikipedia/'+self.colour[0]+'B.png'), (63, 63))
        self.position = position
        self.coords = locate(self.position)
        self.rect = pygame.Rect(self.coords[0], self.coords[1], 63, 63)
        self.symbol = 'B'
        self.poshistory = []
        self.matrix = chessToMatrix(self.position)

    def move(self, pos, board):
        if pos in self.legalMoves(board):
            self.poshistory.append(self.position)
            self.position = pos
            self.coords = locate(self.position)
            self.rect = pygame.Rect(self.coords[0], self.coords[1], 63, 63)
            if self.poshistory[-1] == self.position:
                return True, board
            else:
                return False, board
        else:
            return True, board

    def legalMoves(self, board):
        self.temp = []
        self.movement = []
        self.matrix = chessToMatrix(self.position)
        self.matrix = chessToMatrix(self.position)
        
        # Find all moves
        for i in range(-11, -99, -11):
            try:
                if int(str(i+int(self.matrix))[1]) == 9:
                    break
            except IndexError:
                pass
            self.temp.append(matrixToChess(int(self.matrix)+i))
            mat = str(int(self.matrix)+i)
            if len(mat) == 1:
                mat = '0'+mat
            if matrixToChess(int(self.matrix)+i) == None:
                pass
            elif board.array[int(mat[0])][int(mat[1])] != None:
                break
        for i in range(11, 99, 11):
            if len(str(i+int(self.matrix))) > 2:
                pass
            elif int(str(i+int(self.matrix))[1]) > 7:
                #print(int(str(i+int(self.matrix))[1]))
                break
            else:
                self.temp.append(matrixToChess(int(self.matrix)+i))
                #print(matrixToChess(int(self.matrix)+i))
            mat = str(int(self.matrix)+i)
            if len(mat) == 1:
                mat = '0'+mat
            if matrixToChess(int(self.matrix)+i) == None:
                pass
            elif board.array[int(mat[0])][int(mat[1])] != None:
                break
        for i in range(9, 99, 9):
            if len(str(i+int(self.matrix))) > 2:
                pass
            elif int(str(i+int(self.matrix))[1]) == 9:
                break
            else:
                self.temp.append(matrixToChess(int(self.matrix)+i))
            mat = str(int(self.matrix)+i)
            if len(mat) == 1:
                mat = '0'+mat
            if matrixToChess(int(self.matrix)+i) == None:
                pass
            elif board.array[int(mat[0])][int(mat[1])] != None:
                break
        for i in range(-9, -99, -9):
            try:
                if int(str(i+int(self.matrix))[1]) == 8:
                    break
                else:
                    self.temp.append(matrixToChess(int(self.matrix)+i))
                mat = str(int(self.matrix)+i)
                if len(mat) == 1:
                    mat = '0'+mat
                if matrixToChess(int(self.matrix)+i) == None:
                    pass
                elif board.array[int(mat[0])][int(mat[1])] != None:
                    break
            except:
                self.temp.append(matrixToChess(int(self.matrix)+i))
                mat = str(int(self.matrix)+i)
                if len(mat) == 1:
                    mat = '0'+mat
                if matrixToChess(int(self.matrix)+i) == None:
                    pass
                elif board.array[int(mat[0])][int(mat[1])] != None:
                    break

        # Remove moves that go off the board
        for move in self.temp:
            # print(move,move)
            if move is not None:
                self.movement.append(move)

        # Check if spaces are available
        self.spaces = {}
        for move in self.movement:
            loc = chessToMatrix(move)
            piece = board.array[int(loc[0])][int(loc[1])]
            if piece is not None:
                self.spaces[move] = piece
        for i in list(self.spaces.keys()):
            piece = self.spaces[i]
            # print(self.spaces)
            # print(piece)
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
        self.matrix = chessToMatrix(self.position)

    def move(self,pos,board):
        if pos in self.legalMoves(board):
            self.poshistory.append(self.position)
            self.position = pos
            self.coords = locate(self.position)
            self.rect = pygame.Rect(self.coords[0],self.coords[1],63,63)
            if self.poshistory[-1] == self.position:
                return True, board
            else:
                return False, board
        else:
            return True, board

    def legalMoves(self,board):
        self.temp = []
        self.movement = []
        self.matrix = chessToMatrix(self.position)
        self.matrix = chessToMatrix(self.position)
        
        #Find diagonals
        for i in range(-11, -99, -11):
            try:
                if int(str(i+int(self.matrix))[1]) == 9:
                    break
            except IndexError:
                pass
            self.temp.append(matrixToChess(int(self.matrix)+i))
            mat = str(int(self.matrix)+i)
            if len(mat) == 1:
                mat = '0'+mat
            if matrixToChess(int(self.matrix)+i) == None:
                pass
            elif board.array[int(mat[0])][int(mat[1])] != None:
                break
        for i in range(11, 99, 11):
            if len(str(i+int(self.matrix))) > 2:
                pass
            elif int(str(i+int(self.matrix))[1]) > 7:
                break
            else:
                self.temp.append(matrixToChess(int(self.matrix)+i))
            mat = str(int(self.matrix)+i)
            if len(mat) == 1:
                mat = '0'+mat
            if matrixToChess(int(self.matrix)+i) == None:
                pass
            elif board.array[int(mat[0])][int(mat[1])] != None:
                break
        for i in range(9, 99, 9):
            if len(str(i+int(self.matrix))) > 2:
                pass
            elif int(str(i+int(self.matrix))[1]) == 9:
                break
            else:
                self.temp.append(matrixToChess(int(self.matrix)+i))
            mat = str(int(self.matrix)+i)
            if len(mat) == 1:
                mat = '0'+mat
            if matrixToChess(int(self.matrix)+i) == None:
                pass
            elif board.array[int(mat[0])][int(mat[1])] != None:
                break
        for i in range(-9, -99, -9):
            try:
                if int(str(i+int(self.matrix))[1]) == 8:
                    break
                else:
                    self.temp.append(matrixToChess(int(self.matrix)+i))
                mat = str(int(self.matrix)+i)
                if len(mat) == 1:
                    mat = '0'+mat
                if matrixToChess(int(self.matrix)+i) == None:
                    pass
                elif board.array[int(mat[0])][int(mat[1])] != None:
                    break
            except:
                self.temp.append(matrixToChess(int(self.matrix)+i))
                mat = str(int(self.matrix)+i)
                if len(mat) == 1:
                    mat = '0'+mat
                if matrixToChess(int(self.matrix)+i) == None:
                    pass
                elif board.array[int(mat[0])][int(mat[1])] != None:
                    break

        #Find vertical-up possibilities
        start = int(chessToMatrix(self.position)[1])
        start1 = int(chessToMatrix(self.position)[0])
        for i in range(start1,-1,-1):
            self.temp.append(matrixToChess(str(i)+str(start)))
            if matrixToChess(str(i)+str(start)) == self.position:
                pass
            elif board.array[i][start] != None:
                break
        # Find veritcal-down possibilities
        for i in range(start1+1,8,1):
            self.temp.append(matrixToChess(str(i)+str(start)))
            if matrixToChess(str(i)+str(start)) == self.position:
                pass
            elif board.array[i][start] != None:
                break

        #Find horizontal-left possibilities
        start = int(chessToMatrix(self.position)[0])
        start1 = int(chessToMatrix(self.position)[1])
        for i in range(start1,-1,-1):
            self.temp.append(matrixToChess(str(start)+str(i)))
            if matrixToChess(str(start)+str(i)) == self.position:
                pass
            elif board.array[start][i] != None:
                break
        # Find horizontal-right possibilities
        for i in range(start1,8,1):
            self.temp.append(matrixToChess(str(start)+str(i)))
            if matrixToChess(str(start)+str(i)) == self.position:
                pass
            elif board.array[start][i] != None:
                break

        #Remove moves that go off the board
        for move in self.temp:
            #print(move,move)
            if move != None:
                self.movement.append(move)

        #Remove yourself
        while self.position in self.movement:
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
        self.matrix = chessToMatrix(self.position)

    def move(self,pos,board):
        print(board)
        #print('pos',pos)
        #print(self.legalMoves(board))
        if pos in self.legalMoves(board):
            self.poshistory.append(self.position)
            self.position = pos
            self.coords = locate(self.position)
            self.rect = pygame.Rect(self.coords[0],self.coords[1],63,63)
            if self.poshistory[-1] == self.position:
                return True, board
            else:
                return False, board
        else:
            return True, board

    def legalMoves(self,board):
        self.temp = []
        self.movement = []
        self.matrix = chessToMatrix(self.position)
        
        #Find all moves
        if self.colour == 'w':
            #print(self.temp)
            self.temp.append(matrixToChess(int(self.matrix)-10))
            #print(self.temp)
            # Move 2 squares from start
            # Check there isn't a piece in the way
            one_forward = str(int(self.matrix)-10)
            if len(self.poshistory) == 0 and board.array[int(one_forward[0])][int(one_forward[1])] == None:
                self.temp.append(matrixToChess(int(self.matrix)-20))
            #print(self.temp)
        if self.colour == 'b':
            self.temp.append(matrixToChess(int(self.matrix)+10))
            # Move 2 squares from start
            # Check there isn't a piece in the way
            one_forward = str(int(self.matrix)+10)
            if len(self.poshistory) == 0 and board.array[int(one_forward[0])][int(one_forward[1])] == None:
                self.temp.append(matrixToChess(int(self.matrix)+20))

        for move in self.temp:
            self.tempmatrix = chessToMatrix(move)
            if board.array[int(self.tempmatrix[0])][int(self.tempmatrix[1])] != None:
                self.temp.pop(self.temp.index(move))

        #Attacking moves
        if self.colour == 'w':
            left = str(int(self.matrix)-11)
            right = str(int(self.matrix)-9)
            
            if left[1] == '8' or left[1] == '9':
                pass
            elif board.array[int(left[0])][int(left[1])] != None:
                self.temp.append(matrixToChess(left))
            if right[1] == '8' or right[1] == '9':
                pass
            elif board.array[int(right[0])][int(right[1])] != None:
                self.temp.append(matrixToChess(right))
        else:
            left = str(int(self.matrix)+11)
            if len(left) == 1:
                left = '0'+left
            right = str(int(self.matrix)+9)
            if len(right) == 1:
                right = '0'+right
            #print('left: ',left)

            if left[1] == '8' or left[1] == '9':
                pass
            elif board.array[int(left[0])][int(left[1])] != None:
                self.temp.append(matrixToChess(left))
            if right[1] == '8' or right[1] == '9':
                pass
            elif board.array[int(right[0])][int(right[1])] != None:
                self.temp.append(matrixToChess(right))

        #Remove moves that go off the board
        for move in self.temp:
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

        #print(self.poshistory)
        return self.movement
    
    def __repr__(self):
        if self.colour == 'w':
            return 'P'
        elif self.colour =='b':
            return 'p'


class Board():
    def __init__(self):
        # Board for testing purposes
        self.arrays = [
            [None for x in range(8)],
            [None for x in range(8)],
            [None for x in range(8)],
            [None,None,None,None,None,None,None,None],
            [None for x in range(8)],
            [None,None,None,Rook('w','d3'),None,None,None,None],
            [None for x in range(8)],
            [None for x in range(8)],
        ]
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
        self.wk = 'e1'
        self.bk = 'e8'

        self.updatefen('w')
        
    def updatefen(self, turn):
        self.fen = ''
        nonecount = 0
        for rank in self.array:
            for piece in rank:
                #print(piece)
                if piece is not None:
                    if nonecount != 0:
                        self.fen+=str(nonecount)
                    nonecount = 0
                    self.fen+=piece.symbol
                elif piece is None:
                    nonecount+=1
            if nonecount != 0:
                self.fen+=str(nonecount)
            self.fen+='/'
            nonecount = 0

        # Remove trailing /
        self.fen = self.fen[:-1]

        # Add turn
        self.fen+= ' '+turn

        # Castling not implemented so add rights
        self.fen+= ' KQkq'

        # En passant not implemented so state not available
        self.fen+= ' -'

        # Halfmove counter for 50-turn rule not implemented so state it as 0
        self.fen+= ' 0'

        # No fullmove counter so set to 1
        self.fen+= ' 1'
    
    def __repr__(self):
        msg = ''
        for i in self.array:
            for j in i:
                if j is not None:
                    msg+=j.symbol+' '
                else:
                    msg+='. '
            msg+='\n'
        return msg