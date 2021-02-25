"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if board == initial_state():
        return X

    numX = 0
    numO = 0
    for row in board:
        numX += row.count(X)
        numO += row.count(O)
    
    if (numX == 0 and numO == 0) or (numO > numX):
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()

    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                moves.add((row, col))
    
    return moves



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if (action[0] < 0) or (action[0] > 2) or action[1] < 0 or action[1] > 2 or board[action[0]][action[1]] is not EMPTY:
        raise Exception("Invalid Move!!!")

    newBoard = copy.deepcopy(board)
    newBoard[action[0]][action[1]] = player(board)

    return newBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for symbol in [X,O]:
        for i in range(0,3):
            if all(board[i][j] == symbol for j in range(0,3)):
                return symbol

            if all(board[j][i] == symbol for j in range(0,3)):
                return symbol
            
        diag = [[(0,0), (1,1), (2,2)], [(0,2), (1,1), (2,0)]] 
        for options in diag:
            if all(board[i][j] == symbol for (i,j) in options):
                return symbol
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """    
    if winner(board) is not None:
        return True
     
    cellsArr = [cells for row in board for cells in row]
    if not any(cell == EMPTY for cell in cellsArr):
        return True
    
    return False
            


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    numX = 0
    numO = 0
    for row in board:
        numX += row.count(X)
        numO += row.count(O)
    
    if(numX > numO):
        return 1
    elif(numO > numX):
        return -1
    else:
        return 0



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    acceptableMoves = actions(board)
    if player(board) == X:
        maxValue = -math.inf
        for moves in acceptableMoves:
          value = min_Value(result(board. moves))
          if value > maxValue:
              maxValue = value
              desiredMove = moves

    else:
        minValue = math.inf
        for moves in acceptableMoves:
            value = max_value(result(board, moves))
            if value < minValue:
                minValue = value
                desiredMove = moves

    return desiredMove

def min_Value(board):
    v = math.inf

    if terminal(board):
        return utility(board)

    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    return v

def max_value(board):
    v = -math.inf

    if terminal(board):
        return utility(board)

    for action in actions(board):
        v = max(v, min_Value(result(board, action)))

    return v  


