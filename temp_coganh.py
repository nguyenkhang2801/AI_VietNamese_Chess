import pygame
import math
from copy import deepcopy


# =================== Setting size of game ==============
WIDTH = 600
MARGIN = 50
ROWS = 5
COLS = 5
ROWWIDTH = WIDTH // (ROWS - 1)
RADIUS = 20
OUTLINE = 4
FPS = 60
CASEOF4 = [(0,1), (0,3), (1,0), (1,4), (3,0), (3,4), (4,1), (4,3), (1,2), (2,1), (2,3), (3,2)] # Positions which have maximun 4 moves



# ===== Set up display to visualize pathfinding =====
WIN = pygame.display.set_mode((WIDTH + MARGIN * 2, WIDTH + MARGIN * 2))
pygame.display.set_caption("Co ganh")



#  ================== Setting color  =====================
ORANGE = (255, 165, 0)          # 
TURQUOISE = (64, 224, 208)      # 
WHITE = (255, 255, 255)         # 
BLACK = (0, 0, 0)               # 
RED = (255, 0, 0)               # Red piece
PURPLE = (128, 0, 128)          #
GREEN = (0, 255, 0)             # 
GREY = (128, 128, 128)          # Gridline color
YELLOW = (255, 255, 0)          # Legal move
BLUE = (0, 255, 0)              # Blue piece



class Piece():
    def __init__(self, row, col, color):
        self.color = color
        self.row = row
        self.col = col
        self.x = 0
        self.y = 0
        self.calculatePosition()
        self.selected = False
    
    def calculatePosition(self):
        self.x = MARGIN + self.col * ROWWIDTH
        self.y = MARGIN + self.row * ROWWIDTH

    def draw(self):
        if self.selected:
            pygame.draw.circle(WIN, PURPLE, (self.x, self.y), RADIUS + OUTLINE)
        else:
            pygame.draw.circle(WIN, GREY, (self.x, self.y), RADIUS + OUTLINE)
        pygame.draw.circle(WIN, self.color, (self.x, self.y), RADIUS)  
    
    def changeColor(self):
        self.color = RED if self.color == BLUE else BLUE
        
    
    def move(self, row, col):
        self.row = row
        self.col = col
        self.calculatePosition()

    def __repr__(self):
        return str(self.color)



class Board:
    def __init__(self):
        self.board = []
        self.redLeft = 8
        self.blueLeft = 8
        self.ore = 0
        self.createBoard()

    def createBoard(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if row == 0:
                    self.board[row].append(Piece(row, col, RED))
                elif row == 1 and (col == 0 or col == COLS - 1):
                    self.board[row].append(Piece(row, col, RED))
                elif row == 2 and col == COLS - 1:
                    self.board[row].append(Piece(row, col, RED))
                elif row == 2 and col == 0:
                    self.board[row].append(Piece(row, col, BLUE))
                elif row == ROWS - 2 and (col == 0 or col == COLS - 1):
                    self.board[row].append(Piece(row, col, BLUE))
                elif row == ROWS - 1:
                    self.board[row].append(Piece(row, col, BLUE))
                else:
                    self.board[row].append(0)

    def draw(self):
        self.drawGridLine()
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw()
    
    def getPiece(self, row, col):
        return self.board[row][col]
    
    def move(self, piece, row, col):
        # swap data in self.board
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

    def getValidMoves(self, piece):
        moves = []
        row = piece.row
        col = piece.col

        # check 8 directions
        if row - 1 >= 0:
            if self.board[row - 1][col] == 0:
                moves.append((row - 1, col))
        if row + 1 < ROWS:
            if self.board[row + 1][col] == 0:
                moves.append((row + 1, col))
        if col - 1 >= 0:
            if self.board[row][col -1] == 0:
                moves.append((row, col - 1))
        if col + 1 < COLS:
            if self.board[row][col + 1] == 0:
                moves.append((row, col + 1))
        if (row, col) not in CASEOF4:
            if row - 1 >= 0 and col - 1 >= 0:
                if self.board[row - 1][col - 1] == 0:
                    moves.append((row - 1, col - 1))
            if row - 1 >= 0 and col + 1 < COLS:
                if self.board[row - 1][col + 1] == 0:
                    moves.append((row - 1, col + 1))
            if row + 1 < ROWS and col - 1 >= 0:
                if self.board[row + 1][col - 1] == 0:
                    moves.append((row + 1, col - 1))
            if row + 1 < ROWS and col + 1 < COLS:
                if self.board[row + 1][col + 1] == 0:
                    moves.append((row + 1, col + 1))

        return moves

    def evalation(self):
        return self.redLeft - self.blueLeft

    def getAllPieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces


    def drawGridLine(self):
        # draw vertical and horizontal line
        for i in range(ROWS):
            pygame.draw.line(WIN, GREY, (0 + MARGIN, i * ROWWIDTH + MARGIN), (WIDTH + MARGIN, i * ROWWIDTH + MARGIN))
        for i in range(ROWS):
            pygame.draw.line(WIN, GREY, (i * ROWWIDTH + MARGIN, 0 + MARGIN), (i * ROWWIDTH + MARGIN, WIDTH + MARGIN))    
        # draw diagonal 
        pygame.draw.line(WIN, GREY, (MARGIN, MARGIN), (MARGIN + ROWWIDTH * 2, MARGIN + ROWWIDTH * 2))    
        pygame.draw.line(WIN, GREY, (MARGIN + ROWWIDTH * 2, MARGIN), (MARGIN + ROWWIDTH * 4, MARGIN + ROWWIDTH * 2))    
        pygame.draw.line(WIN, GREY, (MARGIN, MARGIN + ROWWIDTH * 2), (MARGIN + ROWWIDTH * 2, MARGIN))    
        pygame.draw.line(WIN, GREY, (MARGIN + ROWWIDTH * 2, MARGIN + ROWWIDTH * 2), (MARGIN + ROWWIDTH * 4, MARGIN))    

        pygame.draw.line(WIN, GREY, (MARGIN, MARGIN + ROWWIDTH * 2), (MARGIN + ROWWIDTH * 2, MARGIN + ROWWIDTH * 4))    
        pygame.draw.line(WIN, GREY, (MARGIN + ROWWIDTH * 2, MARGIN + ROWWIDTH * 2), (MARGIN + ROWWIDTH * 4, MARGIN + ROWWIDTH * 4))    
        pygame.draw.line(WIN, GREY, (MARGIN, MARGIN + ROWWIDTH * 4), (MARGIN + ROWWIDTH * 2, MARGIN + ROWWIDTH * 2))    
        pygame.draw.line(WIN, GREY, (MARGIN + ROWWIDTH * 2, MARGIN + ROWWIDTH * 4), (MARGIN + ROWWIDTH * 4, MARGIN + ROWWIDTH * 2))    





class Game:
    def _init(self):
        self.board = Board()
        self.selected = None
        self.turn = BLUE
        self.validMoves = []
        self.winner = None

    def findWinner(self):
        if self.board.blueLeft <= 0:
            self.winner = RED
            return True
        elif self.board.redLeft <= 0:
            self.winner = BLUE
            return True
        else: 
            return False

    def __init__(self):
        self._init()

    def resetGame(self):
        self._init()

    def update(self):
        WIN.fill(WHITE)
        self.board.draw()
        self.drawValidMoves()
        pygame.display.update()

    def changeTurn(self):
        self.turn = RED if self.turn == BLUE else BLUE

    def drawValidMoves(self):
        if not self.validMoves:
            return
        for move in self.validMoves:
            row, col = move
            pygame.draw.circle(WIN, YELLOW, (MARGIN + col * ROWWIDTH, MARGIN + row * ROWWIDTH), 15)

    def select(self, row, col):
        piece = self.board.getPiece(row, col)
        inLstValidMoves = True if (row, col) in self.validMoves else False
        if self.selected:
            if piece == 0 and inLstValidMoves:
                # ============ MOVE ==================
                self.board.move(self.selected, row, col)
                self.selected.selected = False
                self.selected = None
                self.validMoves = []
                self.checkSkip(self.board, row, col)                
                self.changeTurn()
                return
            elif piece != 0:
                # =========== SELECT ONTHER PIECE ==========
                self.selected.selected = False
                self.selected = None
                self.select(row, col)
                return
        else:
            # ========= CHOOSE A PIECE =============
            if piece != 0:
                if piece.color == self.turn:
                    piece.selected = True
                    self.selected = piece
                    self.validMoves = self.board.getValidMoves(piece)
                else:
                    return
            else:
                return
            
    def checkSkip(self, board, row, col):
        opponent = RED if self.turn == BLUE else BLUE

        # ============== check horizontal skip ================
        if col - 1 >= 0 and col + 1 < COLS:
            leftPiece = board.getPiece(row, col - 1)
            rightPiece = board.getPiece(row, col + 1)
            # ====== Nuoc di ganh ===========
            if leftPiece != 0 and rightPiece != 0 and leftPiece.color == rightPiece.color == opponent:
                self.skip(board, leftPiece)
                self.skip(board, rightPiece)
            # ======== Nuoc di vay ===========


        # =============== check vertical skip ==================
        if row - 1 >= 0 and row + 1 < ROWS:
            topPiece = board.getPiece(row - 1, col)
            botPiece = board.getPiece(row + 1, col)
            # ====== Nuoc di ganh ===========
            if topPiece != 0 and botPiece != 0 and topPiece.color == botPiece.color == opponent:
                self.skip(board, topPiece)
                self.skip(board, botPiece)
            # ======== Nuoc di vay ===========

        if (row, col) not in CASEOF4:
            # ============== Check left diagonal skip =================
            if row - 1 >= 0 and col - 1 >= 0 and row + 1 < ROWS and col + 1 < COLS:
                topLeftPiece = board.getPiece(row - 1, col -1)
                botRightPiece = board.getPiece(row + 1, col + 1)
                # ====== Nuoc di ganh ===========
                if topLeftPiece != 0 and botRightPiece != 0 and topLeftPiece.color == botRightPiece.color == opponent:
                    self.skip(board, topLeftPiece)
                    self.skip(board, botRightPiece)
                # ======== Nuoc di vay ===========
   
            # ============== Check right diagonal skip =================
            if row - 1 >= 0 and col + 1 < COLS and row + 1 < ROWS and col - 1 >= 0:
                topRightPiece = board.getPiece(row - 1, col + 1)
                botLeftPiece = board.getPiece(row + 1, col - 1)
                # ====== Nuoc di ganh ===========
                if topRightPiece != 0 and botLeftPiece != 0 and topRightPiece.color == botLeftPiece.color == opponent:
                    self.skip(board, topRightPiece)
                    self.skip(board, botLeftPiece)
                # ======== Nuoc di vay ===========

                
    def skip(self, board, piece):
        if piece.color == RED:
            board.redLeft -= 1
        else:
            board.blueLeft -= 1
        piece.changeColor()

    def moveOfAI(self, board):
        self.board = board
        self.changeTurn()


        
        

def minimax(currentBoard, depth, maxPlayer, game):
    if depth == 0 or game.findWinner():
        return currentBoard.evalation(), currentBoard

    if maxPlayer:
        maxEval = float('-inf')
        bestMove = None
        for move in getAllMoveOfBoard(currentBoard, RED, game):
            evaluation = minimax(move, depth - 1, False, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                bestMove = move
        return maxEval, bestMove
    else:
        minEval = float('inf')
        bestMove = None        
        for move in getAllMoveOfBoard(currentBoard, BLUE, game):
            evaluation = minimax(move, depth - 1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                bestMove = move
        return minEval, bestMove


def getAllMoveOfBoard(board, color, game):
    moves = []

    for piece in board.getAllPieces(color):
        validMoves = board.getValidMoves(piece)
        for move in validMoves:
            tempBoard = deepcopy(board)
            tempPiece = tempBoard.getPiece(piece.row, piece.col)
            newBoard = simulateMove(tempPiece, move, tempBoard, game)
            moves.append(newBoard)

    return moves

def simulateMove(piece, move, board, game):
    board.move(piece, move[0], move[1])
    game.checkSkip(board, move[0], move[1])
    return board

def getRowColFromMouse(pos):
    x, y = pos
    row = (y - MARGIN // 2) // ROWWIDTH
    col = (x - MARGIN // 2) // ROWWIDTH 
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game()


    while run:
        clock.tick(FPS)



        if game.findWinner():
            run = False
        
        #============== AI turn ====================
        if game.turn == RED:
            evaluation, bestMove = minimax(game.board, 3, True, game)
            game.moveOfAI(bestMove)        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = getRowColFromMouse(pos)
                game.select(row, col)
            
        game.update()

    pygame.quit()

main()