import numpy as np
import os

def move(board, from_pos, to_pos):
    board[to_pos[0],to_pos[1]] = board[from_pos[0], from_pos[1]]
    board[from_pos[0], from_pos[1]] = 0

def show_board(board):
    for i in range(5):
        for j in range(5):
            if board[i,j] == 1:
                print('X\t', end='')
            elif board[i,j] == -1:
                print('O\t', end='')
            else:
                print('_\t', end='')
        print('\n', end='')

def move(board, fromPos, toPos):
    board = np.copy(board)
    if board[fromPos[0], fromPos[1]] == 0 or board[toPos[0], toPos[1]] != 0:
        # raise ValueError("Move error")
        print("Move error")
        return None
    board[toPos[0], toPos[1]] = board[fromPos[0], fromPos[1]]
    board[fromPos[0], fromPos[1]] = 0
    return board

def ganh(board, team):
    '''
    check enemy team is "ganh" or not 
    '''
    board = np.copy(board)
    def process(board, team):
        board = np.copy(board).reshape(-1)
        team_pos = np.where(board == team)[0]
        for pos in team_pos:
            if pos % 2 == 0:
                if 1 <= pos // 5 <= 3 and 1 <= pos % 5 <= 3:
                    if board[pos] * -2 == board[pos-6] + board[pos+6]:
                        board[pos-6] = board[pos]
                        board[pos+6] = board[pos]
                    if board[pos] * -2 == board[pos-4] + board[pos+4]:
                        board[pos-4] = board[pos]
                        board[pos+4] = board[pos]
            if pos-1 >= 0 and pos + 1 <= 24 and (pos-1) % 5 < (pos+1) % 5:
                if board[pos] * -2 == board[pos-1] + board[pos+1]:
                    board[pos-1] = board[pos]
                    board[pos+1] = board[pos]
            if pos-5 >= 0 and pos + 5 <= 24 and (pos-5) // 5 < (pos+5) // 5:
                if board[pos] * -2 == board[pos-5] + board[pos+5]:
                    board[pos-5] = board[pos]
                    board[pos+5] = board[pos]
        return board.reshape(5,5)

    new_board = process(board, team)
    while (new_board != board).any():
        board = new_board
        new_board = process(board, team)
    
    return board

def vay(board, team):
    '''
    call after team played to check enemy is "vay" or not
    '''
    board = np.copy(board)
    


board = np.array([
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, -1, 1, 0, -1],
    [-1, 0, 0, 0, -1],
    [-1, -1, -1, -1, -1]
])
board = np.array([
    [1, 1, 1, 1, 0],
    [0, -1, 1, 1, 0],
    [1, 1, 1, 0, -1],
    [0, -1, 0, 0, 0],
    [-1, -1, 0, -1, -1]
])
show_board(board)

print("\n _________________________________________________________\n")

board = ganh(board, -1)
show_board(board)