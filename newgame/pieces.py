from functions import *
import pygame
import copy

def checkSelfCheck(board, movingpiece, square):
    ''' Checks if the current team will be moving into check, returns True if they are '''
    board.array[int(matrix(square)[0])][int(matrix(square)[1])] = movingpiece
    board.array[int(matrix(movingpiece.position)[0])][int(matrix(movingpiece.position)[1])] = None
    colour = movingpiece.colour
    if movingpiece.symbol == 'K':
        king = movingpiece

    for rank in board.array:
        for piece in rank:
            if piece is not None:
                if piece.symbol == 'K' and piece.colour == colour:
                    king = piece

    for rank in board.array:
        for piece in rank:
            if piece is not None:
                if piece.colour != colour:
                    if king.position in piece.legalMoves(board):
                        king.checkhistory = True
                        return True

    return False

def checkCheck(board, colour):
    for rank in board.array:
        for piece in rank:
            if piece is not None:
                if piece.symbol == 'K' and piece.colour == colour:
                    king = piece

    for rank in board.array:
        for piece in rank:
            if piece is not None:
                if piece.colour != colour:
                    if king.position in piece.legalMoves(board):
                        king.checkhistory = True
                        return True

    return False

class Piece(pygame.sprite.Sprite):
    def __init__(self, position, colour, symbol):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.poshistory = []
        self.colour = colour
        self.symbol = symbol
        self.coords = locate(self.position)
        self.rect = pygame.Rect(self.coords[0],self.coords[1],63,63)
    
    def update(self, position):
        self.poshistory.append(self.position)
        self.position = position
        self.coords = locate(self.position)
        self.rect = pygame.Rect(locate(self.position)[0],locate(self.position)[1],63,63)

    def removeMoves(self, board):
        '''A method which removes moves from the legal moves list for the piece. It will remove the current square of the piece'''
        self.movement = []
        for path in self.paths:
            for move in self.paths[path]:
                if move is not None:
                    if board.array[int(matrix(move)[0])][int(matrix(move)[1])] == None:
                        if move not in self.movement:
                            self.movement.append(move)
                    elif board.array[int(matrix(move)[0])][int(matrix(move)[1])].colour != self.colour:
                        if move not in self.movement:
                            self.movement.append(move)

        return self.movement


class King(Piece):
    def __init__(self, position, colour):
        Piece.__init__(self, position, colour, 'K')
        self.paths = {
            '1': []
        }
        self.checkhistory = False

    def legalMoves(self, board):
        ''' Finds all of the legal moves based on the board state '''
        self.paths = {
            '1': []
        }

        self.paths['1'].append(chess(int(matrix(self.position))+11))
        self.paths['1'].append(chess(int(matrix(self.position))+10))
        self.paths['1'].append(chess(int(matrix(self.position))+9))
        self.paths['1'].append(chess(int(matrix(self.position))+1))
        self.paths['1'].append(chess(int(matrix(self.position))-1))
        self.paths['1'].append(chess(int(matrix(self.position))-9))
        self.paths['1'].append(chess(int(matrix(self.position))-10))
        self.paths['1'].append(chess(int(matrix(self.position))-11))

        if len(self.poshistory) == 0 and self.checkhistory == False:
            if self.colour == 'w':
                if board.array[7][7].symbol == 'R':
                    rook = board.array[7][7]
                    if len(rook.poshistory) == 0:
                        if 'f1' in rook.legalMoves(board):
                            self.paths['1'].append(chess(int(matrix(self.position))+2))
                if board.array[7][0].symbol == 'R':
                    rook = board.array[7][0]
                    if len(rook.poshistory) == 0:
                        if 'd1' in rook.legalMoves(board):
                            self.paths['1'].append(chess(int(matrix(self.position))-2))
            elif self.colour == 'b':
                if board.array[0][7].symbol == 'R':
                    rook = board.array[0][7]
                    if len(rook.poshistory) == 0:
                        if 'f8' in rook.legalMoves(board):
                            self.paths['1'].append(chess(int(matrix(self.position))+2))
                if board.array[0][0].symbol == 'R':
                    rook = board.array[0][0]
                    if len(rook.poshistory) == 0:
                        if 'd8' in rook.legalMoves(board):
                            self.paths['1'].append(chess(int(matrix(self.position))-2))

        return self.removeMoves(board)


class Queen(Piece):
    def __init__(self, position, colour):
        Piece.__init__(self, position, colour, 'Q')
        self.paths = {
            'n': [],
            'ne': [],
            'e': [],
            'se': [],
            's': [],
            'sw': [],
            'w': [],
            'nw': []
        }

    def legalMoves(self, board):
        self.paths = {
            'n': [],
            'ne': [],
            'e': [],
            'se': [],
            's': [],
            'sw': [],
            'w': [],
            'nw': []
        }

        ''' Finds all of the legal moves based on the board state '''
        for square in range(int(matrix(self.position)),-1,-10):
            square = expand(square)
            self.paths['n'].append(chess(square))
            if board.array[int(square[0])][int(square[1])] != None and chess(square) != self.position:
                break
        for square in range(int(matrix(self.position)),78,10):
            square = expand(square)
            self.paths['s'].append(chess(square))
            if board.array[int(square[0])][int(square[1])] != None and chess(square) != self.position:
                break
        for square in range(int(matrix(self.position)),int(matrix(self.position)[0]+'8'),1):
            square = expand(square)
            self.paths['e'].append(chess(square))
            if board.array[int(square[0])][int(square[1])] != None and chess(square) != self.position:
                break
        for square in range(int(matrix(self.position)),-1,-1):
            square = expand(square)
            if square[1] == '9':
                break
            self.paths['w'].append(chess(square))
            if board.array[int(square[0])][int(square[1])] != None and chess(square) != self.position:
                break
        for square in range(int(matrix(self.position)),-1,-11):
            square = expand(square)
            if square[1] == '9':
                break
            self.paths['nw'].append(chess(square))
            if board.array[int(square[0])][int(square[1])] != None and chess(square) != self.position:
                break
        for square in range(int(matrix(self.position)),-1,-9):
            square = expand(square)
            if square[1] == '8':
                break
            self.paths['ne'].append(chess(square))
            if board.array[int(square[0])][int(square[1])] != None and chess(square) != self.position:
                break
        for square in range(int(matrix(self.position)),78,11):
            square = expand(square)
            if square[1] == '8':
                break
            self.paths['se'].append(chess(square))
            if board.array[int(square[0])][int(square[1])] != None and chess(square) != self.position:
                break
        for square in range(int(matrix(self.position)),79,9):
            square = expand(square)
            if square[1] == '9':
                break
            self.paths['sw'].append(chess(square))
            if board.array[int(square[0])][int(square[1])] != None and chess(square) != self.position:
                break

        return self.removeMoves(board)


class Rook(Piece):
    def __init__(self, position, colour):
        Piece.__init__(self, position, colour, 'R')
        self.paths = {
            'n': [],
            'e': [],
            's': [],
            'w': []
        }

    def legalMoves(self, board):
        ''' Finds all of the legal moves based on the board state '''
        self.paths = {
            'n': [],
            'e': [],
            's': [],
            'w': []
        }
        for square in range(int(matrix(self.position)),-1,-10):
            square = expand(square)
            self.paths['n'].append(chess(square))
            if board.array[int(square[0])][int(square[1])] != None and chess(square) != self.position:
                break
        for square in range(int(matrix(self.position)),78,10):
            square = expand(square)
            self.paths['s'].append(chess(square))
            if board.array[int(square[0])][int(square[1])] != None and chess(square) != self.position:
                break
        for square in range(int(matrix(self.position)),int(matrix(self.position)[0]+'8'),1):
            square = expand(square)
            self.paths['e'].append(chess(square))
            if board.array[int(square[0])][int(square[1])] != None and chess(square) != self.position:
                break
        for square in range(int(matrix(self.position)),-1,-1):
            square = expand(square)
            if square[1] == '9':
                break
            self.paths['w'].append(chess(square))
            if board.array[int(square[0])][int(square[1])] != None and chess(square) != self.position:
                break

        return self.removeMoves(board)


class Bishop(Piece):
    def __init__(self, position, colour):
        Piece.__init__(self, position, colour, 'B')
        self.paths = {
            'ne': [],
            'se': [],
            'sw': [],
            'nw': []
        }

    def legalMoves(self, board):
        ''' Finds all of the legal moves based on the board state '''
        self.paths = {
            'ne': [],
            'se': [],
            'sw': [],
            'nw': []
        }
        for square in range(int(matrix(self.position)),-1,-11):
            square = expand(square)
            if square[1] == '9':
                break
            self.paths['nw'].append(chess(square))
            if board.array[int(square[0])][int(square[1])] != None and chess(square) != self.position:
                break
        for square in range(int(matrix(self.position)),-1,-9):
            square = expand(square)
            if square[1] == '8':
                break
            self.paths['ne'].append(chess(square))
            if board.array[int(square[0])][int(square[1])] != None and chess(square) != self.position:
                break
        for square in range(int(matrix(self.position)),78,11):
            square = expand(square)
            if square[1] == '8':
                break
            self.paths['se'].append(chess(square))
            if board.array[int(square[0])][int(square[1])] != None and chess(square) != self.position:
                break
        for square in range(int(matrix(self.position)),79,9):
            square = expand(square)
            if square[1] == '9':
                break
            self.paths['sw'].append(chess(square))
            if board.array[int(square[0])][int(square[1])] != None and chess(square) != self.position:
                break

        return self.removeMoves(board)


class Knight(Piece):
    def __init__(self, position, colour):
        Piece.__init__(self, position, colour, 'N')
        self.paths = {
            '1': []
        }

    def legalMoves(self, board):
        ''' Finds all of the legal moves based on the board state '''
        self.paths = {
            '1': []
        }

        self.paths['1'].append(chess(int(matrix(self.position))+21))
        self.paths['1'].append(chess(int(matrix(self.position))+19))
        self.paths['1'].append(chess(int(matrix(self.position))+12))
        self.paths['1'].append(chess(int(matrix(self.position))+8))
        self.paths['1'].append(chess(int(matrix(self.position))-8))
        self.paths['1'].append(chess(int(matrix(self.position))-12))
        self.paths['1'].append(chess(int(matrix(self.position))-21))
        self.paths['1'].append(chess(int(matrix(self.position))-19))

        return self.removeMoves(board)


class Pawn(Piece):
    def __init__(self, position, colour):
        Piece.__init__(self, position, colour, 'P')
        self.paths = {
            '1': []
        }

    def legalMoves(self, board):
        ''' Finds all of the legal moves based on the board state '''
        self.paths = {
            'n': [],
            'nw': [],
            'ne': [],
            's': [],
            'sw': [],
            'se': [],
        }
        if self.position[1] != '8' and self.position[1] != '1':
            if self.colour == 'w':
                try:
                    if board.array[int(str(expand(int(matrix(self.position))-10))[0])][int(str(expand(int(matrix(self.position))-10))[1])] is None:
                        self.paths['n'].append(chess(expand(int(matrix(self.position))-10)))
                except IndexError:
                        pass
                try:
                    if len(self.poshistory) == 0:
                        self.paths['n'].append(chess(expand(int(matrix(self.position))-20)))
                except IndexError:
                        pass
                try:
                    if board.array[int(str(expand(int(matrix(self.position))-11))[0])][int(str(expand(int(matrix(self.position))-11))[1])] is not None:
                        self.paths['nw'].append(chess(expand(int(matrix(self.position))-11)))
                except IndexError:
                        pass
                try:
                    if board.array[int(str(expand(int(matrix(self.position))-9))[0])][int(str(expand(int(matrix(self.position))-9))[1])] is not None:
                        self.paths['nw'].append(chess(expand(int(matrix(self.position))-9)))
                except IndexError:
                        pass
            elif self.colour == 'b':
                try:
                    if board.array[int(str(expand(int(matrix(self.position))+10))[0])][int(str(expand(int(matrix(self.position))+10))[1])] is None:
                        self.paths['s'].append(chess(int(matrix(self.position))+10))
                except IndexError:
                        pass
                try:
                    if len(self.poshistory) == 0:
                        self.paths['s'].append(chess(int(matrix(self.position))+20))
                except IndexError:
                        pass
                try:
                    if board.array[int(str(int(matrix(self.position))+11)[0])][int(str(int(matrix(self.position))+11)[1])] is not None:
                        self.paths['se'].append(chess(int(matrix(self.position))-11))
                except IndexError:
                        pass
                try:
                    if board.array[int(str(int(matrix(self.position))+9)[0])][int(str(int(matrix(self.position))+9)[1])] is not None:
                        self.paths['sw'].append(chess(int(matrix(self.position))+9))
                except IndexError:
                        pass

        return self.removeMoves(board)


class Board():
    def __init__(self):
        self.array = [
            [Rook('a8','b'),Knight('b8','b'),Bishop('c8','b'),Queen('d8','b'),King('e8','b'),Bishop('f8','b'),Knight('g8','b'),Rook('h8','b')],
            [None for x in range(8)],
            [None for x in range(8)],
            [None for x in range(8)],
            [None for x in range(8)],
            [None for x in range(8)],
            [Pawn('a2','w'),Pawn('b2','w'),Pawn('c2','w'),Pawn('d2','w'),Pawn('e2','w'),Pawn('f2','w'),Pawn('g2','w'),Pawn('h2','w')],
            [Rook('a1','w'),Knight('b1','w'),Bishop('c1','w'),Queen('d1','w'),King('e1','w'),Bishop('f1','w'),Knight('g1','w'),Rook('h1','w')]
        ]
        self.arrays = [
            [None for x in range(8)],
            [None,None,None,Queen('d7','b'),None,None,None,None],
            [None for x in range(8)],
            [None for x in range(8)],
            [None,None,None,None,Bishop('e4','w'),None,None,None],
            [None for x in range(8)],
            [None for x in range(8)],
            [None for x in range(8)]
        ]

    def move(self, piece, square, captured, history):
        '''Moves a piece to a square'''
        if checkSelfCheck(copy.deepcopy(self), piece, square) is not True:
            if square in piece.legalMoves(self):
                if piece.symbol != 'P':
                    algebraicmove = piece.symbol
                else:
                    algebraicmove = ''

                newsquare = self.array[int(matrix(square)[0])][int(matrix(square)[1])]
                if newsquare is not None:
                    algebraicmove+='x'
                    captured.append(newsquare)
                self.array[int(matrix(square)[0])][int(matrix(square)[1])] = piece
                self.array[int(matrix(piece.position)[0])][int(matrix(piece.position)[1])] = None
                algebraicmove+=square

                if piece.symbol == 'K':
                    if len(piece.poshistory) == 0:
                        if square == 'g1':
                            rook = self.array[7][7]
                            self.array[7][7] = None
                            self.array[7][5] = rook
                            rook.update('f1')
                            algebraicmove = '0-0'
                        elif square == 'c1':
                            rook = self.array[7][0]
                            self.array[7][0] = None
                            self.array[7][4] = rook
                            rook.update('d1')
                            algebraicmove = '0-0-0'
                        elif square == 'g8':
                            rook = self.array[0][7]
                            self.array[0][7] = None
                            self.array[0][5] = rook
                            rook.update('f8')
                            algebraicmove = '0-0'
                        elif square == 'c8':
                            rook = self.array[0][0]
                            self.array[0][0] = None
                            self.array[0][4] = rook
                            rook.update('d8')
                            algebraicmove = '0-0-0'

                piece.update(square)
                history.append(algebraicmove)
                return True
        return False



class Game():
    def __init__(self):
        self.board = Board()
        self.colour = 'w'
        self.castling = 'KQkq'
        self.enpassant = ''
        self.halfmoves = 0
        self.fullmoves = 0
        self.captured = []
        self.history = []


#game = Game()
#print(game.board.array)
#game.board.move(game.board.array[4][3],'d2',[])
#print(game.board.array)