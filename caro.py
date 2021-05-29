import numpy as np
import copy

from numpy.core.fromnumeric import size
from numpy.core.numerictypes import maximum_sctype
from numpy.lib.function_base import bartlett

class Caro:
    def __init__(self, size=3):
        self.size = size
        self.value = 1
        self.enemy = 2
        self.win_line = -1 # 0: vertical, 1: horizontal, 2: cross

    def showBoard(self, board):
        print(board)
        print('\n')
        for i in range(self.size):
            for j in range(self.size):
                if board[i,j] == 0:
                    print('_\t', end="")
                elif board[i,j] == 1:
                    print('o\t',end="")
                else:
                    print('x\t', end="")
            print('\n', end="")
    
    def move(self, board, position, value):
        # position: (y,x)
        board = np.copy(board)
        if board[position[0], position[1]] != 0:
            print('++++++++++++++++++++++++++++++++++++++++')
            print('Position marked')
            print(position)
            self.showBoard(board)
            print('===========================================')
            return None
        board[position[0], position[1]] = value
        return board

    def check_strait(self, board, pos):
        if board[pos, 0] != 0 and len(np.nonzero(board[pos] - board[pos,0])[0]) == 0:
            self.win_line = 1
            return True
        if board[0, pos] != 0 and len(np.nonzero(board[:, pos] - board[0, pos])[0]) == 0:
            self.win_line = 0
            return True
        return False
    
    def check_cross(self, board):
        diagonal = np.diagonal(board)
        anti_diagonal = np.diagonal(np.fliplr(board))
        if diagonal[0] != 0 and len(np.nonzero(diagonal - diagonal[0])[0]) == 0:
            self.win_line = 2
            return True
        if anti_diagonal[0] != 0 and len(np.nonzero(anti_diagonal - anti_diagonal[0])[0]) == 0:
            self.win_line = 2
            return True
        return False
    def isEndGame(self, board):
        for i in range(self.size):
            if self.check_strait(board, i):
                return True
        if self.check_cross(board): return True
        if len(np.nonzero(board)[0]) == self.size**2: return True
        return False

    def get_result(self, board):
        if not self.isEndGame(board):
            return 0
        if self.win_line == -1:
            return 0
        if self.win_line == 2:
            return board[self.size//2, self.size//2]

        for i in range(self.size):
            if self.check_strait(board, i):
                if self.win_line == 0:
                    return board[0,i]
                return board[i,0]

    def eveluate(self, board):
        if self.get_result(board) == 1:
            return 10
        elif self.get_result(board) == 2:
            return -10

        score = 0
        for i in range(self.size):
            if len(np.where(board[i, :] == self.enemy)[0])==0 and len(np.where(board[i, :] == self.value)[0]) > 0:
                score += 1
            if len(np.where(board[:, i] == self.enemy)[0])==0 and len(np.where(board[:, i] == self.value)[0]) > 0:
                score += 1
        diagonal = np.diagonal(board)
        anti_diagonal = np.diagonal(np.fliplr(board))
        if len(np.where(diagonal == self.enemy)[0])==0 and len(np.where(diagonal == self.value)[0]) > 0:
                score += 1
        if len(np.where(anti_diagonal == self.enemy)[0])==0 and len(np.where(anti_diagonal == self.value)[0]) > 0:
                score += 1
        return score
    
    def alphabeta(self, board, a, b, dept, myTurn):
        if self.isEndGame(board) or dept == 0:
            return self.eveluate(board)
        
        movable = np.where(board == 0)
        if myTurn:
            for pos in zip(movable[0], movable[1]):
                if board[pos[0], pos[1]] != 0:
                    raise ValueError("Loi move")
                n_board = self.move(board, pos, self.value)
                temp = self.alphabeta(n_board, a, b, dept-1, False)
                a = max(a, temp)
                if a >= b:
                    break
            return a
        else:
            for pos in zip(movable[0], movable[1]):
                if board[pos[0], pos[1]] != 0:
                    raise ValueError("Loi move1")
                n_board = self.move(board, pos, self.enemy)
                b = min(b, self.alphabeta(n_board, a, b, dept-1, True))
                if a >= b:
                    break
            return b
        raise ValueError("Loi roi")    
    
    def process(self, board):
        max_score = -10
        movable = np.where(board == 0)
        next_move = (0,0)
        for i, pos in enumerate(zip(movable[0], movable[1])):
            if board[pos[0], pos[1]] != 0:
                raise ValueError("Loi move2")
            n_board = self.move(board, pos, self.value)
            score = self.alphabeta(n_board, -10, 10, 1, False)
            print('+++++++++++++++++++++++++++++++++++++++++++++++!')
            print('pos: ', pos)
            print('score: ', score)
            print('len: {0}/{1}'.format(i, len(movable[0])))
            print('================================================/')
            if  score > max_score:
                with open('ret.txt', 'a') as f:
                    f.write("better score: ")
                max_score = score
                next_move = pos
            with open('ret.txt', 'a') as f:
                f.write('score: {0}\n'.format(score))
                f.write(str(n_board) + "\n\n")

            
        return next_move
    
    def check_position(self, x, y):
        if 0 <= x < self.size:
            return True
        if 0 <= y < self.size:
            return True
        return False
        
    def play(self):
        board = np.zeros((self.size, self.size))

        while True:
            with open('ret.txt', 'a') as f:
                f.write('___________________________________________\n')
            print('____________________________________________________-')
            x = int(input('x: '))
            y = int(input('y: '))

            while not self.check_position(x,y):
                self.showBoard(board)
                print((x,y))
                x = int(input('x: '))
                y = int(input('y: '))
                

            if board[y, x] != 0:
                raise ValueError("Loi move3")
            board = self.move(board, (y,x), self.enemy)

            if self.isEndGame(board):
                self.showBoard(board)
                break
            
            com_pos = self.process(board)
            board = self.move(board, com_pos, self.value)

            self.showBoard(board)
            print(self.eveluate(board))
            if self.isEndGame(board):
                break

        print('Winner is: ', self.get_result(board))
    

            
            

    
    

caro = Caro(3)
caro.play()


# a = np.array([[1,2,3], [5,1,3], [3,2,6]])
# print(a)
# print(np.where(a == 3))