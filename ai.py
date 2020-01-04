from chess import Board
import random

board = Board()
values = {
    'q': 9,
    'b': 3,
    'n': 3,
    'k': 99,
    'p': 1,
    'r': 5,
    'Q': -9,
    'B': -3,
    'N': -3,
    'K': -99,
    'P': -1,
    'R': -5
}

def evaluate(board):
    global value
    turn = board.fen().split(' ')[1]
    if turn == 'w':
        for i in values:
            values[i] = -values[i]
    
    pieces = board.fen().split(' ')[0]
    value = 0
    for piece in pieces:
        try:
            value+=values[piece]
        except KeyError:
            pass
        #print(piece,value)
    
    return value

def hello(board,boardvalue):
    boardvalue = sorted(boardvalue, key=lambda x: x[1], reverse=True)
    #print(boardvalue)
    for x in range (len(boardvalue)-1):
        #print('hello:',x)
        #print(len(boardvalue))
        boardvaluepop = []
        if boardvalue[x][2] != 0:
            boardvaluepop.append(x)
    for i in boardvaluepop:
        boardvalue.pop(i)
    #print(board.fen())
    temp = []
    for i in boardvalue:
        if i[1] in temp:
            move = random.choice(boardvalue)[0]
        elif len(temp) == 0:
            temp.append(i[1])
        else:
            move = boardvalue[0][0]
    board.push(move)
    print(board.fen())
    #print('HEESLKGLHNEAOIESBLIJGNLKDSJGLDSI')

def test(board, boardvalue, deepness, depth=2):
    #print(depth)        
    #print('else')
    depth-=1
    #print(depth)
    
    for move in board.legal_moves:
        #print('hi')
        board.push(move)
            
        #print('hello')
        boardvalue.append((move,evaluate(board),deepness))
        deepness+=1
        if depth > 0:
            test(board,boardvalue,depth,False)
        board.pop()

        if board.is_game_over():
            print('end')
    #print(depth)

    return boardvalue
    
    
def name(board):
    originalboard = board
    boardvalue = test(board,[],0,2)
    #print(boardvalue)
    hello(originalboard, boardvalue)

name(board)
print(board)
name(board)
print(board)
name(board)
print(board)
name(board)
print(board)
name(board)
print(board)
name(board)
print(board)
name(board)
print(board)
'''name(board)
name(board)
name(board)
name(board)
name(board)
name(board)
name(board)
name(board)
name(board)
name(board)
name(board)
name(board)
name(board)
name(board)
name(board)
name(board)
name(board)
name(board)
name(board)
name(board)
name(board)
name(board)
name(board)
name(board)
name(board)
name(board)
name(board)
name(board)
name(board)
name(board)
name(board)
name(board)
name(board)'''