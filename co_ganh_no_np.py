import copy


AI_TEAM=1

neighborDict = {}
adjacentDict = {}
neighborPosL = []
adjacentPosL = []
for r in range(5):
    for c in range(5):
        neighborPosL = [(r, c - 1), (r, c + 1), (r - 1, c), (r + 1, c), (r - 1, c - 1), (r + 1, c + 1), (r - 1, c + 1), (r + 1, c - 1)]
        if (r % 2 == 0 and c % 2 != 0) or (r % 2 != 0 and c % 2 == 0):
            adjacentPosL = [(r - 1, c), (r, c - 1), (r, c + 1), (r + 1, c)]
            adjacentPosL = list( filter(lambda x: (0 <= x[0] < 5) and (0 <= x[1] < 5), adjacentPosL) )
            neighborPosL = list( filter(lambda x: (0 <= x[0] < 5) and (0 <= x[1] < 5), neighborPosL) )
            neighborDict[r*5 + c] = neighborPosL
            adjacentDict[r*5 + c] = adjacentPosL
        else:
            adjacentPosL = neighborPosL = list( filter(lambda x: (0 <= x[0] < 5) and (0 <= x[1] < 5), neighborPosL) )
            adjacentDict[r*5 + c] = neighborDict[r*5 + c] = neighborPosL
        
        adjacentPosL = neighborPosL = []
def traverse_CHET(startPos, currColor, oppColor, state, q = []):
    # startPos: starting position for traversing; (r, c)
    # currColor: current player's color
    # oppColor: opponent's color
    # state: board game
    # q: list saving opponents' positions of which colors were changed
    # return True if no way out, else False
    
    # index = startPos[0]*5 + startPos[1]
    # aL = adjacentDict[index]
    #state[ startPos[0] ][ startPos[1] ] = currColor
    
    ############################### DFS
    
    state[ startPos[0] ][ startPos[1] ] = currColor
    q.append(startPos)
    for x in adjacentDict[ startPos[0]*5 + startPos[1] ]:
        if (state[ x[0] ][ x[1] ] == 0) or ( state[ x[0] ][ x[1] ] == oppColor and ( not traverse_CHET(x, currColor, oppColor, state, q) ) ):
            while(q[-1] != startPos):
                state[ q[-1][0] ][ q[-1][1] ] = oppColor
                q.pop()
            state[ startPos[0] ][ startPos[1] ] = oppColor
            q.pop()
            return False
            
    return True

def cmp_board(board1, board2):
    for i in range(25):
        if board1[i//5][i%5] != board2[i//5][i%5]:
            return False
    return True
    
def show_board(board):
    for i in range(5):
        for j in range(5):
            if board[i][j] == 1:
                print('X\t', end='')
            elif board[i][j] == -1:
                print('O\t', end='')
            else:
                print('_\t', end='')
        print('\n', end='')

def move(board, fromPos, toPos):
    board = copy.deepcopy(board)
    if board[ fromPos[0] ][ fromPos[1] ] == 0 or board[ toPos[0] ][ toPos[1] ] != 0:
        # raise ValueError("Move error")
        print("Move error")
        return None
    board[ toPos[0] ][ toPos[1] ] = board[ fromPos[0] ][ fromPos[1] ]
    board[ fromPos[0] ][ fromPos[1] ] = 0
    return board

def ganh(board, team):
    '''
    check enemy team is "ganh" or not 
    co the bi loi
    '''
    board = copy.deepcopy(board)
    def process(board, team):
        temp_board = copy.deepcopy(board)
        board = []
        for i in range(5):
            for j in range(5):
                board.append(temp_board[i][j])
        team_pos = []
        for i in range(25):
            if board[i] == team:
                team_pos.append(i)
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
        for i in range(5):
            for j in range(5):
                temp_board[i][j] = board[i*5+j]
        return temp_board

    new_board = process(board, team)
    # while (collections.Counter(new_board) != collections.Counter(board)):
    while not cmp_board(new_board, board):
        board = new_board
        new_board = process(board, team)
    
    return board



def eveluate(board):
    count = 0
    for i in range(5):
        for j in range(5):
            if board[i][j] == AI_TEAM:
                count += 1
    if count == 0:
        print('Player won')
        return -30

    if count == 16:
        print('AI won')
        return 30
    
    return count

def minimax(board, a, b, dept, myTurn):
    temp_board = None
    if dept == 0:
        return eveluate(board)
    stop = False
    
    if myTurn:
        team_pos = []
        for i in range(5):
            for j in range(5):
                if board[i][j] == AI_TEAM:
                    team_pos.append((i,j))
        # team_pos = np.where(board == AI_TEAM)
        for pos in team_pos:
            neighbors = adjacentDict[pos[0]*5 + pos[1]]
            for neighbor in neighbors:
                if board[ neighbor[0] ][ neighbor[1] ] != 0:
                    continue
                temp_board = copy.deepcopy(board)
                temp_board = move(temp_board, pos, neighbor)
                temp_board = postprocess_move(temp_board, pos, neighbor, AI_TEAM)
                temp = minimax(temp_board, a, b, dept-1, False)
                a = max(a, temp)
                if a >= b:
                    stop = True
                    break
            if stop:
                break
        return a
    else:
        team_pos = []
        for i in range(5):
            for j in range(5):
                if board[i][j] == -1 * AI_TEAM:
                    team_pos.append((i,j))
        # team_pos = np.where(board == -1 * AI_TEAM)
        for pos in team_pos:
            neighbors = adjacentDict[pos[0]*5 + pos[1]]
            for neighbor in neighbors:
                if board[ neighbor[0] ][ neighbor[1] ] != 0:
                    continue
                temp_board = copy.deepcopy(board)
                temp_board = move(temp_board, pos, neighbor)
                temp_board = postprocess_move(temp_board, pos, neighbor, -1*AI_TEAM)
                temp = minimax(temp_board, a, b, dept-1, True)
                b = min(b, temp)
                if a >= b:
                    stop = True
                    break
            if stop:
                break
        return b
                    

def postprocess_move(board, fromPos, toPos, team):
    '''
    fromPos: Vị trí cũ
    toPos: vị trí mới
    team: team vừa di chuyển
    '''
    neighbors = adjacentDict[toPos[0]*5+toPos[1]]
    # print('neighbors: ', neighbors)
    board = copy.deepcopy(board)
    board = ganh(board, team)
    for neighbor in neighbors:
        if board[ neighbor[0] ][ neighbor[1] ] == team*-1:
            temp_board = copy.deepcopy(board)
            traverse_CHET(neighbor, team, team*-1, board)
            # if collections.Counter(temp_board) != collections.Counter(board):
            if not cmp_board(temp_board, board):
                with open('ret.txt', 'a') as f:
                    print('vay: ', neighbor)
                    # f.write('temp_board: \n{0}\n'.format(temp_board))
                    # f.write('board: {0}\n'.format(board))
    
    return board
def get_next_move(board):
    score = 0
    max_score=-40
    nextMove = None

    team_pos = []
    for i in range(5):
        for j in range(5):
            if board[i][j] == AI_TEAM:
                team_pos.append((i,j))
    # team_pos = np.where(board == AI_TEAM)
    for pos in team_pos:
        neighbors = adjacentDict[pos[0]*5 + pos[1]]
        for neighbor in neighbors:
            if board[ neighbor[0] ][ neighbor[1] ] != 0:
                continue
            temp_board = copy.deepcopy(board)
            temp_board = move(temp_board, pos, neighbor)
            temp_board = postprocess_move(temp_board, pos, neighbor, AI_TEAM)
            score = minimax(temp_board, -30, 30, 1, False)
            # print('+++++++++++++++++++++++++++++++++++++++++++++++!')
            # print('pos: ', pos)
            # print('score: ', score)
            # print('================================================/')
            if score >= max_score:
                
                nextMove = [pos, neighbor]
                max_score = score
    print(nextMove)
    return nextMove

def playgame(board):

    while True:
        print('==================================================')
        print('From pos')
        y1 = int(input("y: "))
        x1 = int(input("x: "))
        
        
        print('To pos')
        y2 = int(input("y: "))
        x2 = int(input("x: "))
        
        board = move(board, (y1,x1), (y2,x2))
        board = postprocess_move(board, (y1,x1), (y2,x2), -1 * AI_TEAM)

        show_board(board)
        print('_____________________________________________')


        next_move = get_next_move(board)
        board = move(board, next_move[0], next_move[1])
        board = postprocess_move(board, next_move[0], next_move[1], AI_TEAM)

        show_board(board)


board =[
        [   1,  1,  1,  1,  1],
        [   1,  0,  0,  0,  1],
        [   1,  0,  0,  0,  -1],
        [   -1, 0,  0,  0,  -1],
        [   -1, -1, -1, -1, -1]
]

show_board(board)
playgame(board)

