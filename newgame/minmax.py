import random



def airun(level, board):
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
        return piece[0], move
    elif level == 2:
        # Still pretty much random except it will take if it can
        pass
    elif level == 3:
        # Uses minmax to a depth of 3?
        pass
    elif level == 4:
        # Uses minmax to a depth of 5?
        pass