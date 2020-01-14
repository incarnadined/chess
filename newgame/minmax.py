import random
from functions import matrix
from pieces import Game
import copy

game = Game()

def evaluate(board, currentvalue):
    piecesonboard = []
    for rank in board.array:
        for piece in rank:
            if piece is not None:
                piecesonboard.append(piece)
    for piece in piecesonboard:
        currentvalue+=piece.value
    return currentvalue

def minMax(board, depth, maxing=False):
    global game
    if depth == 0:
        return evaluate(board)
    pieces = []
    for rank in board.array:
        for piece in rank:
            if piece is not None:
                if piece.legalMoves(board) != []:
                    pieces.append(piece)
    print(depth)
    if maxing:
        bestMove = -9999
        for piece in pieces:
            if piece.colour == 'w':
                originalmove = piece.position
                for move in piece.legalMoves(board):
                    #print(piece,move)
                    board.move(piece, move, game)
                    #print(board.array)
                    bestMove = evaluate(board)
                    bestMove = max(bestMove,minMax(copy.deepcopy(board), depth - 1, not maxing))
                    #print(bestMove)
                    board.move(piece, originalmove, game)
        return bestMove
    else:
        bestMove = 9999
        for piece in pieces:
            if piece.colour == 'b':
                originalmove = piece.position
                for move in piece.legalMoves(board):
                    #print(piece,move)
                    board.move(piece, move, game)
                    #print(board.array)
                    bestMove = evaluate(board)
                    bestMove = max(bestMove,minMax(copy.deepcopy(board), depth - 1, not maxing))
                    #print(bestMove)
                    board.move(piece, originalmove, game)
        return bestMove


def airun(level, board):
    board = copy.deepcopy(board)
    global game
    move = False

    if level == 1:
        possiblemoves = []
        for i in board.array:
            for piece in i:
                if piece is not None and piece.colour == 'b':
                    moves = piece.legalMoves(board)
                    if moves != []:
                        possiblemoves.append((piece,moves))
            
        piece = random.choice(possiblemoves)
        move = random.choice(piece[1])
        piece = piece[0]

        if piece.symbol == 'P' and matrix(move)[0] == '7': # If it is a pawn moving to the back rank
            promotion = random.choice(['knight','bish','rook','queen'])
        else:
            promotion = ''

        return piece, move, promotion

    elif level == 2:
        moves = {}
        pieces = []
        value = 0
        finalmoves = []
        for rank in board.array:
            for piece in rank:
                if piece is not None:
                    if piece.colour == 'b':
                        pieces.append(piece)
        for piece in pieces:
            originalmove = piece.position
            for move in piece.legalMoves(board):
                board.array[int(matrix(originalmove)[0])][int(matrix(originalmove)[1])] = None
                board.array[int(matrix(move)[0])][int(matrix(move)[1])] = piece
                value = evaluate(copy.deepcopy(board), value)
                board.array[int(matrix(move)[0])][int(matrix(move)[1])] = None
                board.array[int(matrix(originalmove)[0])][int(matrix(originalmove)[1])] = piece
                moves[move] = (value, piece)

        moves = sorted(moves.items(), key=lambda x: x[0])
        if moves[0][1][0] == moves[1][1][0]:
            for i in moves:
                if i[1][0] == moves[0][1][0]:
                    finalmoves.append(i)
        print(moves)
        if finalmoves:
            print(finalmoves)
            finalmove = random.choice(finalmoves)
        else:
            finalmove = moves[0]

        print(finalmove[1][1], finalmove[0], 'queen')
        return finalmove[1][1], finalmove[0], 'queen'

    elif level == 3:
        # Uses minmax to a depth of 3?
        pass
    elif level == 4:
        # Uses minmax to a depth of 5?
        pass
