import random
import time

SIZE = 5
PLAYERA = 1         #
PLAYERB = -1        #
EMPTY = 0           #
TIMELIMIT = 0.05
INF = 9999999

# ======================== Class Player =======================================
class Player:
    # student do not allow to change two first functions

    def __init__(self, str_name):
        self.str = str_name
        self.preBoard = Board()     # mỗi player sẽ có 1 bàn cờ riêng
                                    # lưu trạng thái bàn cờ sau khi player vừa dùng next_move
                                    # mục đích:
                                    # để đối chiếu board trong "def move(board, player)" tìm ra nước đi của đối thủ -> thế cờ mở
        self.preBoard.createBoard([
                  [1, 1, 1, 1, 1], \
                  [1, 0, 0, 0, 1], \
                  [1, 0, 0, 0, -1], \
                  [-1, 0, 0, 0, -1], \
                  [-1, -1, -1, -1, -1], \
                ], self.str)

    def __int__(self):
        return self.str

    # Student MUST implement this function
    # The return value should be a move that is denoted by a list of tuples:
    # [(row1, col1), (row2, col2)] with:
        # (row1, col1): current position of selected piece
        # (row2, col2): new position of selected piece
    def next_move(self, state):
        ai = AI()
        board = Board()
        board.createBoard(state, self.str)
        dt = self.doiThu(board) # tim ra nuoc di cua doi thu
        player = 1 if self.str == PLAYERA else -1
        move = ai.alpha_beta_search(board, player, dt, self.preBoard)
        if move == None:
            return None
        result = ((int(move[0]/5), move[0] % 5), (int(move[1]/5), move[1]%5))
        self.preBoard = Board()
        self.preBoard.createBoard(state, self.str)
        self.preBoard.makeMove(move, player)        #làm mới lại bàn cờ qua nước đi vừa rồi
        return result

    # tim ra nuoc da di cua doi thu
    def doiThu(self, board):
        vi_tri_dau = -1
        vi_tri_sau = -1
        for i in range(SIZE*SIZE):
            if board.board[i] != self.preBoard.board[i]:
                if self.preBoard.board[i] != 0 and board.board[i] == 0:
                    vi_tri_dau = i
                if self.preBoard.board[i] == 0 and board.board[i] != 0:
                    vi_tri_sau = i
        return (vi_tri_dau, vi_tri_sau)

class Board:
    def __init__(self):
        self.board = list() # bàn cờ lúc này chuyển từ 2 chiều sang 1 chiều
        self.num1 = 0  # So luong quan ta
        self.num2 = 0  # So luong quan dich
        # đếm số lượng quân địch và quân ta, hỗ trợ phép thử thế mở (quân địch đi mà không gánh, không vây)
        self.win = 0   # hỗ trợ hàm vây
    # Tao mot board tu state mac dinh
    def createBoard(self, state, str_name):
        for i in range(SIZE):
            for j in range(SIZE):
                cur_player = state[i][j]
                if cur_player == PLAYERA:
                    self.board.append(1)
                elif cur_player == PLAYERB:
                    self.board.append(-1)
                else:
                    self.board.append(0)

                if cur_player == str_name:
                    self.num1 += 1
                elif cur_player != EMPTY:
                    self.num2 += 1


    def staticEval(self, player):
        if player == 1:
            if self.num1 == 0:
                return -INF
            if self.num2 == 0:
                return INF
            return self.num1 - self.num2
        elif player == -1:
            if self.num1 == 0:
                return INF
            if self.num2 == 0:
                return -INF
            return self.num2 - self.num1
        else:
            return None

    # Tim nuoc de Vay doi thu
    def recus_Vay(self, startPos, currColor, oppColor, state, q = []):
        state[startPos] = currColor
        self.win += 1
        q.append(startPos)
        lst = list()
        if startPos%2 == 0:
            lst = [startPos-6, startPos-5, startPos-4, startPos-1, startPos+1, startPos+4, startPos+5, startPos+6]
        else:
            lst = [startPos-5, startPos-1, startPos+1, startPos+5]
        for x in lst:
            if x <= 0 or x >= 24 or not x % 5 - startPos % 5 in [-1, 0, 1]:
                continue
            # state 0 = '.'
            if (state[x] == 0) or (state[x] == oppColor and ( not self.recus_Vay(x, currColor, oppColor, state, q) ) ):
                while(q[-1] != startPos):
                    state[q[-1]] = oppColor
                    q.pop()
                    self.win -= 1
                state[startPos] = oppColor
                q.pop()
                self.win -= 1
                return False
        return True 

    # Tim tat ca cac nuoc di co the cua ban co
    # board: trang thai ban co
    # dt: nuoc di cua doi thu
    # return: list() tat cac cac nuoc di co the
    #def (nuoc di cua doi thu, player hien tai, ban co truoc khi doi thu ra quan)
    def getAvailableMoves(self, dt, player, preBoard):
        #ưu tiên thứ tự thế cờ mở, vây (>= 2 quân địch bị vây), gánh, vây (< 2 quân địch bị vây)
        if dt[0] != dt[1]: #and preBoard.num1 == self.num1 and preBoard.num2 == self.num2:
            availableMove = list()          #list tất cả các nước đi có thể
            listGanhAvailable = list()      #list gánh
            listBayAvailable = list()       #list mở
            listVayAvailable = list()       #list vây (< 2)
            listVayCung = list()            #list vây (> 2)
            isBay = False
            isGanh = False
            isVay = False
            for i in range(SIZE*SIZE):
                if self.board[i] == player:
                    lst = list()    #những điểm kề i trên bàn cờ
                    if i%2 == 0:
                        lst = [i-6, i-5, i-4, i-1, i+1, i+4, i+5, i+6]
                    else:
                        lst = [i-5, i-1, i+1, i+5]
                    bay1 = False
                    ganh1= False
                    vay1 = False
                    for x in lst:
                        if self.dKienMove(i, x):
                            ##### gánh + mở
                            lst1 = list()   #những điểm tạo thành đường thẳng với điểm x
                            if x % 2 == 0:
                                lst1 = [(x - 6, x + 6), (x - 5, x + 5), (x - 4, x + 4), (x - 1, x + 1)]
                            else:
                                lst1 = [(x - 5, x + 5), (x - 1, x + 1)]
                            for x1 in lst1:
                                if x1[0] >= 0 and x1[0] <= 24 and x1[0] % 5 - x % 5 in [-1, 0, 1] and x1[1] >= 0 and x1[1] <= 24 and x1[1] % 5 - x % 5 in [-1, 0, 1]:
                                    
                                    # Gánh, nếu 2 điểm bên cạnh đều là quân địch, mình sẽ đi vào để gánh
                                    if self.board[x1[0]] == otherPlayer(player) and self.board[x1[1]] == otherPlayer(player):
                                        # thế MỞ, nếu nước đi của quân địch tạo ra ô trống để quân ta vào gánh
                                        if preBoard.num1 == self.num1 and preBoard.num2 == self.num2:   # quân địch không ăn, không vây
                                            if x == dt[0]: # kiểm tra x có phải là ô trống do quân địch tạo ra hay không
                                                bay1 = True
                                                listBayAvailable.append((i, x))
                                                break
                                        # thế gánh bình thường
                                        else:
                                            ganh1 = True
                                            listGanhAvailable.append((i, x))
                                            break
                            ######### thế Vây
                            lst2 = list()   # những điểm lân cận của x
                            if x%2 == 0:
                                lst2 = [x-6, x-5, x-4, x-1, x+1, x+4, x+5, x+6]
                            else:
                                lst2 = [x-5, x-1, x+1, x+5]
                            
                            self.win = 0     #số quân cờ địch có thể sẽ bị vây nếu thực hiện nước đi từ i sang x
                            state = list()
                            for k in range(SIZE * SIZE):
                                state.append(self.board[k])     #copy bàn cờ
                            state[i] = 0
                            state[x] = player

                            for j in lst2:
                                if j >= 0 and j <= 24 and j % 5 - x % 5 in [-1, 0, 1]:
                                    if state[j] == otherPlayer(player):
                                        if(self.recus_Vay(j, player, otherPlayer(player), state)):
                                            vay1 = True
                                            listVayAvailable.append((i, x))
                                            if self.win >= 2:
                                                listVayCung.append((i, x))
                            #########
                            # them i, x vao danh sach nhung nuoc co the di
                            availableMove.append((i, x))
                    if bay1 is True:
                        isBay = True
                    if ganh1 is True:
                        isGanh = True
                    if vay1 is True:
                        isVay = True


            #### thứ tự ưu tiên: thế mở, thế vây (>2), thế gánh, thế vây (<2), tất cả mọi nước đi có thể           
            if isBay:
                return listBayAvailable
            if len(listVayCung) != 0:
                return listVayCung
            if isGanh:
                return listGanhAvailable
            if isVay:
                return listVayAvailable
            
            return availableMove
        else:
            availableMove = list()
            for i in range(SIZE*SIZE):
                if self.board[i] == player:
                    lst = list()
                    if i%2 == 0:
                        lst = [i-6, i-5, i-4, i-1, i+1, i+4, i+5, i+6]
                    else:
                        lst = [i-5, i-1, i+1, i+5]
                    for x in lst:
                        if self.dKienMove(i, x):
                            availableMove.append((i, x))
            return availableMove

    #Hàm hỗ trợ hàm Makemove,  vây quân địch
    def traverse_CHET(self, startPos, currColor, oppColor, q = []):
        self.board[startPos] = currColor
        self.num1+=1
        self.num2-=1
        q.append(startPos)
        lst = list()
        if startPos%2 == 0:
            lst = [startPos-6, startPos-5, startPos-4, startPos-1, startPos+1, startPos+4, startPos+5, startPos+6]
        else:
            lst = [startPos-5, startPos-1, startPos+1, startPos+5]
        for x in lst:
            if x <= 0 or x >= 24 or not x % 5 - startPos % 5 in [-1, 0, 1]:
                continue
            # state 0 = '.'
            if (self.board[x] == 0) or ( self.board[x] == oppColor and ( not self.traverse_CHET(x, currColor, oppColor, q) ) ):
                while(q[-1] != startPos):
                    self.board[q[-1]] = oppColor
                    self.num1-=1
                    self.num2+=1
                    q.pop()
                
                self.board[startPos] = oppColor
                self.num1-=1
                self.num2+=1
                q.pop()
                return False
        return True    

    # Thuc hien buoc chuyen move tren trang thai board
    def makeMove(self, move, player):
        if self.board[move[0]] == 0:
            return False
        if self.board[move[1]] != 0:
            return False
        ## Chuyen trang thai ban co
        self.board[move[1]] = self.board[move[0]]
        self.board[move[0]] = 0
        
        ## Ganh
        lst = list()
        if move[1] % 2 == 0:
            lst = [(move[1] - 6, move[1] + 6), (move[1] - 5, move[1] + 5), (move[1] - 4, move[1] + 4), (move[1] - 1, move[1] + 1)]
        else:
            lst = [(move[1] - 5, move[1] + 5), (move[1] - 1, move[1] + 1)]
        for x in lst:
            if x[0] >= 0 and x[0] <= 24 and x[0] % 5 - move[1] % 5 in [-1, 0, 1] and x[1] >= 0 and x[1] <= 24 and x[1] % 5 - move[1] % 5 in [-1, 0, 1] :
                if not self.board[x[0]] in [self.board[move[1]], 0] and not self.board[x[1]] in [self.board[move[1]], 0]:
                    self.board[x[0]] = self.board[move[1]]
                    self.board[x[1]] = self.board[move[1]]
                    if self.board[move[1]] == player:
                        self.num1 += 2
                        self.num2 -= 2
                    else:
                        self.num1 -= 2
                        self.num2 += 2
        # vây
        for i in range(SIZE * SIZE):
            if self.board[i] == otherPlayer(player):
                self.traverse_CHET(i, player, otherPlayer(player))

        return True

    # Tra ve mot board moi co gia tri y het ban do hien tai
    def copyBoard(self):
        new_board = Board()
        new_board.board = self.board.copy()
        new_board.num1 = self.num1
        new_board.num2 = self.num2
        return new_board
    # điều kiện để tạo move
    def dKienMove(self, vi_tri_dau, vi_tri_sau):
        if vi_tri_sau <= 0 or vi_tri_sau >= 24 or not vi_tri_sau % 5 - vi_tri_dau % 5 in [-1, 0, 1]:
            return False
        if self.board[vi_tri_sau] != 0:
            return False
        return True

class AI:
    def __init__(self):
        self.timeStart = time.time()
        self.timeExceeded = False

    def alpha_beta_search(self, board:Board, playerId:int, dt, preBoard):
        best_value = -INF
        beta = INF
        moves = board.getAvailableMoves(dt, playerId, preBoard)
        if len(moves) == 0:
            return None
        if len(moves) == 1:
            return moves[0]
        best_move = list()
        depth = 1
        while not self.timeOut():
            for i in range(len(moves)):
                new_board = board.copyBoard()
                new_board.makeMove(moves[i], playerId)
                value = self.min_value(new_board, otherPlayer(playerId), best_value, beta , moves[i], depth - 1, board)
                if value >= best_value:
                    best_value = value
                    best_move.append((moves[i], best_value))
                if self.timeOut():
                    break
            depth += 1
        lst = list()
        for x in best_move:
            if x[1] == best_value:
                lst.append(x[0])
        if len(lst) == 1:
            return lst[0]
        else:
            return lst[random.randint(0, len(lst) - 1)]

    def min_value(self, board, playerId, alpha, beta, dt, depth, preBoard):
        if depth == 0 or self.timeOut():
            return board.staticEval(otherPlayer(playerId))
        value = INF
        moves = board.getAvailableMoves(dt, playerId, preBoard)
        for i in range(len(moves)):
            new_board = board.copyBoard()
            new_board.makeMove(moves[i], playerId)
            value = min(value, self.max_value(new_board, otherPlayer(playerId), alpha, beta , moves[i], depth - 1, board))
            if value <= alpha:
                return value
            beta = min(beta, value)
            if self.timeOut():
                break
        return value

    def max_value(self, board, playerId, alpha, beta, dt, depth, preBoard):
        if depth == 0 or self.timeOut():
            return board.staticEval(otherPlayer(playerId))
        value = -INF
        moves = board.getAvailableMoves(dt, playerId, preBoard)
        for i in range(len(moves)):
            new_board = board.copyBoard()
            new_board.makeMove(moves[i], playerId)
            value = max(value, self.min_value(new_board, otherPlayer(playerId), alpha, beta , moves[i], depth - 1, board))
            if value >= beta:
                return value
            beta = max(beta, value)
            if self.timeOut():
                break
        return value

    def timeOut(self):
        if time.time() - self.timeStart >= TIMELIMIT:
            self.timeExceeded = True
            return True
        return False

    def getTime(self):
        return time.time() - self.timeStart


def otherPlayer(player):
    return -1 if player == 1 else 1