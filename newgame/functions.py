import math

selected = False
availablesquares = []
images = {}
promotion = False
prom = {}


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

def matrix(chess):
    chess = str(chess)
    row = str((int(chess[1]) - 8)*-1)
    column = number(chess[0])
    return row+column

def chess(matrix):
    if len(str(matrix)) == 1:
        matrix = '0'+str(matrix)
    matrix = str(matrix)
    if matrix[1] == '8' or matrix[1] == '9'or int(matrix)< 0:
        return None
    row = str((int(matrix[0]) - 8)*-1)
    column = letter(matrix[1])
    if int(row) > 0 and int(row) < 9 and column is not None:
        return column+row 

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

def square(coord):
    x = coord[0]
    y = coord[1]

    # Find the square
    column = math.floor((x - 50)/62.5)
    row = math.floor((y-50)/62.5)
    if column < 8 and column >= 0 and row < 8 and row >= 0:
        return letter(column)+str((row-8)*-1)
    else:
        return '00'
        pass

def expand(square):
    if len(str(square)) == 1:
        square = '0'+str(square)
    return str(square)