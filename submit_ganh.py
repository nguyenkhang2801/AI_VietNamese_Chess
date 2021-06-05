
import numpy as np

neighborDict = {}
adjacentDict = {}
neighborPosL = []
adjacentPosL = []

AI_TEAM = None

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

def my_move(board, from_pos, to_pos):
    board[to_pos[0],to_pos[1]] = board[from_pos[0], from_pos[1]]
    board[from_pos[0], from_pos[1]] = 0

def ganh(board, team):
    '''
    check enemy team is "ganh" or not 
    co the bi loi
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

def eveluate(board):
    if len(np.where(board==AI_TEAM)[0]) == 0:
        return -30

    if len(np.where(board==-AI_TEAM)[0]) == 0:
        return 30
    
    return len(np.where(board==AI_TEAM)[0])

def minimax(board, a, b, dept, myTurn):
    temp_board = None
    if dept == 0:
        return eveluate(board)
    stop = False
    
    if myTurn:
        team_pos = np.where(board == AI_TEAM)
        for pos in zip(team_pos[0], team_pos[1]):
            neighbors = adjacentDict[pos[0]*5 + pos[1]]
            for neighbor in neighbors:
                if board[neighbor[0],neighbor[1]] != 0:
                    continue
                temp_board = np.copy(board)
                my_move(temp_board, pos, neighbor)
                temp_board = postprocess_move(temp_board, pos, neighbor, AI_TEAM)
                temp = minimax(board, a, b, dept-1, False)
                a = max(a, temp)
                if a >= b:
                    stop = True
                    break
            if stop:
                break
        return a
    else:
        team_pos = np.where(board == -1 * AI_TEAM)
        for pos in zip(team_pos[0], team_pos[1]):
            neighbors = adjacentDict[pos[0]*5 + pos[1]]
            for neighbor in neighbors:
                if board[neighbor[0],neighbor[1]] != 0:
                    continue
                temp_board = np.copy(board)
                my_move(temp_board, pos, neighbor)
                temp_board = postprocess_move(temp_board, pos, neighbor, -1*AI_TEAM)
                temp = minimax(board, a, b, dept-1, True)
                b = min(a, temp)
                if a >= b:
                    stop = True
                    break
            if stop:
                break
        return b

def traverse_CHET(startPos, currColor, oppColor, state, q = []):
    
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


def postprocess_move(board, fromPos, toPos, team):
    '''
    fromPos: Vị trí cũ
    toPos: vị trí mới
    team: team vừa di chuyển
    '''
    neighbors = adjacentDict[toPos[0]*5+toPos[1]]
    board = np.copy(board)
    board = ganh(board, team)
    for neighbor in neighbors:
        if board[neighbor[0], neighbor[1]] == team*-1:
            traverse_CHET(neighbor, team, team*-1, board)
    
    return board

def get_next_move(board, player):
    global AI_TEAM
    AI_TEAM = player
    score = 0
    max_score=-40
    nextMove = None

    team_pos = np.where(board == AI_TEAM)
    for pos in zip(team_pos[0], team_pos[1]):
        neighbors = adjacentDict[pos[0]*5 + pos[1]]
        for neighbor in neighbors:
            if board[neighbor[0],neighbor[1]] != 0:
                continue
            temp_board = np.copy(board)
            my_move(temp_board, pos, neighbor)
            temp_board = postprocess_move(temp_board, pos, neighbor, AI_TEAM)
            score = minimax(board, -30, 30, 2, False)
            # print('+++++++++++++++++++++++++++++++++++++++++++++++!')
            # print('pos: ', pos)
            # print('score: ', score)
            # print('================================================/')
            if score >= max_score:
                
                nextMove = [pos, neighbor]
                max_score = score
    # print('next move: ', nextMove)
    return nextMove

