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
        kingpos = square
    else: # This else statement is needed so that the kingpos isn't overwritten with the actual king pos but instead the new square(assuming the king is moving)
        for rank in board.array:
            for piece in rank:
                if piece is not None:
                    if piece.symbol == 'K' and piece.colour == colour:
                        king = piece
                        kingpos = piece.position

    for rank in board.array:
        for piece in rank:
            if piece is not None:
                if piece.colour != colour:
                    if kingpos in piece.legalMoves(board):
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
                        print(colour, 'is now in check')
                        return True

    return False

def checkMate(board, colour):
    ''' Does the same as checkCheck() except for checkMate not just check '''
    if checkCheck(board, colour) == False:
        return False

    movestemp = []
    for rank in board.array:
        for piece in rank:
            if piece is not None:
                if piece.symbol == 'K' and piece.colour == colour:
                    king = piece
    for rank in board.array:
        for piece in rank:
            if piece is not None:
                if king.position in piece.legalMoves(board):
                    threat = piece
                    for path in threat.paths:
                        if king.position in threat.paths[path]:
                            threatmoves = threat.paths[path]
    moves = king.legalMoves(board)

    # Checks if a piece form the kings team can capture the threat
    for rank in board.array:
        for piece in rank:
            if piece is not None:
                if piece.colour == king.colour:
                    if threat.position in piece.legalMoves(board):
                        if piece.symbol == 'K': # If the piece is the king, check that they won't expose themself to new check
                            if checkSelfCheck(copy.deepcopy(board), piece, threat.position) is not True:
                                print(piece,'can capture',threat, 'to stop check')
                                return False
                            else:
                                moves.pop(moves.index(threat.position))
                        else:
                            print(piece,'can capture',threat, 'to stop check')
                            return False

    # Checks if a piece form the kings team can get in the way
    for move in threatmoves:
        for rank in board.array:
            for piece in rank:
                if piece is not None:
                    if piece.colour == king.colour:
                        if move in piece.legalMoves(board):
                            if piece.symbol is not 'K':
                                print(piece,'can get in the way of check and save', king.colour,'from check')
                                return False

    # Checks if anywhere the king can go is check
    for move in king.legalMoves(board):
        for rank in board.array:
            for piece in rank:
                if piece is not None:
                    if piece.colour != colour:
                        if move in piece.legalMoves(board):
                            if len(moves) == 0:
                                break
                            try:
                                moves.pop(moves.index(move))
                            except ValueError:
                                print('WARNING: value for checkmate moving not in list') 
    if len(moves) == 0:
        print(colour,'is in checkmate')
        return True


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

    def __repr__(self):
        return self.symbol


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
                try:
                    if board.array[7][7].symbol == 'R':
                        rook = board.array[7][7]
                        if len(rook.poshistory) == 0:
                            if 'f1' in rook.legalMoves(board):
                                self.paths['1'].append(chess(int(matrix(self.position))+2))
                except AttributeError: # The rook location is actually None
                    pass
                try:
                    if board.array[7][0].symbol == 'R':
                        rook = board.array[7][0]
                        if len(rook.poshistory) == 0:
                            if 'd1' in rook.legalMoves(board):
                                self.paths['1'].append(chess(int(matrix(self.position))-2))
                except AttributeError: # The rook location is actually None
                    pass
            elif self.colour == 'b':
                try:
                    if board.array[0][7].symbol == 'R':
                        rook = board.array[0][7]
                        if len(rook.poshistory) == 0:
                            if 'f8' in rook.legalMoves(board):
                                self.paths['1'].append(chess(int(matrix(self.position))+2))
                except AttributeError: # The rook location is actually None
                    pass
                try:
                    if board.array[0][0].symbol == 'R':
                        rook = board.array[0][0]
                        if len(rook.poshistory) == 0:
                            if 'd8' in rook.legalMoves(board):
                                self.paths['1'].append(chess(int(matrix(self.position))-2))
                except AttributeError: # The rook location is actually None
                    pass

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
        self.matrix = matrix(self.position)
        if self.position[1] != '8' and self.position[1] != '1':
            if self.colour == 'w':
                if board.array[int(str(expand(int(matrix(self.position))-10))[0])][int(str(expand(int(matrix(self.position))-10))[1])] is None:
                    self.paths['n'].append(chess(expand(int(matrix(self.position))-10)))
                    if len(self.poshistory) == 0 and board.array[int(str(expand(int(matrix(self.position))-20))[0])][int(str(expand(int(matrix(self.position))-20))[1])] == None:
                        self.paths['n'].append(chess(expand(int(matrix(self.position))-20)))
                left = expand(str(int(self.matrix)-11))
                right = expand(str(int(self.matrix)-9))
                if left[1] == '8' or left[1] == '9':
                    pass
                elif board.array[int(left[0])][int(left[1])] != None:
                    self.paths['nw'].append(chess(left))
                if right[1] == '8' or right[1] == '9':
                    pass
                elif board.array[int(right[0])][int(right[1])] != None:
                    self.paths['ne'].append(chess(right))
            elif self.colour == 'b':
                if board.array[int(str(expand(int(matrix(self.position))+10))[0])][int(str(expand(int(matrix(self.position))+10))[1])] is None:
                    self.paths['n'].append(chess(expand(int(matrix(self.position))+10)))
                    if len(self.poshistory) == 0 and board.array[int(str(expand(int(matrix(self.position))+20))[0])][int(str(expand(int(matrix(self.position))+20))[1])] == None:
                        self.paths['n'].append(chess(expand(int(matrix(self.position))+20)))
                left = expand(str(int(self.matrix)+9))
                right = expand(str(int(self.matrix)+11))
                if left[1] == '8' or left[1] == '9':
                    pass
                elif board.array[int(left[0])][int(left[1])] != None:
                    self.paths['se'].append(chess(left))
                if right[1] == '8' or right[1] == '9':
                    pass
                elif board.array[int(right[0])][int(right[1])] != None:
                    self.paths['sw'].append(chess(right))

        return self.removeMoves(board)


class Board():
    def __init__(self):
        self.array = [
            [Rook('a8','b'),Knight('b8','b'),Bishop('c8','b'),Queen('d8','b'),King('e8','b'),Bishop('f8','b'),Knight('g8','b'),Rook('h8','b')],
            [Pawn('a7','b'),Pawn('b7','b'),Pawn('c7','b'),Pawn('d7','b'),Pawn('e7','b'),Pawn('f7','b'),Pawn('g7','b'),Pawn('h7','b')],
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

    def move(self, piece, square, captured, history, checkmate):
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

                if piece.colour == 'w':
                    if checkMate(self, 'b') == False:
                        checkmate = 'b'
                else:
                    if checkMate(self, 'w') == True:
                        checkmate = 'w'
                return True
        else:
            print('That move would put/leave your king in check')
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
        self.checkmate = ''

    def turn(self):
        if self.colour == 'w':
            self.colour = 'b'
        elif self.colour == 'b':
            self.colour = 'w'

#game = Game()
#print(game.board.array)
#game.board.move(game.board.array[4][3],'d2',[])
#print(game.board.array)