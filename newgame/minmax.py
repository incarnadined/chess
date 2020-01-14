import random
from functions import matrix
from pieces import Game
import copy

game = Game()

def evaluate(board):
    currentvalue = 0
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
        finalmoves = []
        equalmoves = []
        i = 0
        captured = False
        for rank in board.array:
            for piece in rank:
                if piece is not None:
                    if piece.colour == 'b':
                        pieces.append(piece)
        for piece in pieces:
            originalmove = piece.position
            for move in piece.legalMoves(board):
                if board.array[int(matrix(move)[0])][int(matrix(move)[1])] is not None:
                    captured = board.array[int(matrix(move)[0])][int(matrix(move)[1])]
                board.array[int(matrix(originalmove)[0])][int(matrix(originalmove)[1])] = None
                board.array[int(matrix(move)[0])][int(matrix(move)[1])] = piece
                value = evaluate(copy.deepcopy(board))
                if captured:
                    board.array[int(matrix(move)[0])][int(matrix(move)[1])] = captured
                    captured = False
                else:
                    board.array[int(matrix(move)[0])][int(matrix(move)[1])] = None
                board.array[int(matrix(originalmove)[0])][int(matrix(originalmove)[1])] = piece
                moves[str(i)] = (value, piece, move)
                i+=1

        moves = sorted(moves.items(), key=lambda x: x[1][0], reverse=True)

        for i in range(len(moves)): 
            if moves[i][1][0] == moves[0][1][0]:
                equalmoves.append(moves[i])

        finalvalues = random.choice(equalmoves)

        piece = finalvalues[1][1]
        move = finalvalues[1][2]

        print(piece, move, 'queen')
        return piece, move, 'queen'

    elif level == 3:
        # Uses minmax to a depth of 3?
        pass
    elif level == 4:
        # Uses minmax to a depth of 5?
        pass
