import imp
studentA = "1652192"
player_a = imp.load_source(studentA, studentA + ".py")


Test_Board = [
                  [0, -1, 0, -1, 0], \
                  [-1, 1, 0, -1, 0], \
                  [1, 0, 1, 1, 0], \
                  [1, 1, 1, 1, -1], \
                  [0, 0, 1, -1, -1], \
                ]


Pre_Board = [
                  [0, -1, -1, 0, 0], \
                  [-1, 1, 0, -1, 0], \
                  [1, 0, 1, 1, 0], \
                  [1, 1, 1, 1, -1], \
                  [0, 0, 1, -1, -1], \
                ]

def move(board, player): # khong sua ten ham nay
    A = player_a.Player(player)
    A.preBoard = player_a.Board()
    A.preBoard.createBoard(Pre_Board, 1)
    return A.next_move(board)

print(move(Test_Board, 1))