"""
Tic Tac Toe Player
"""
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    if x_count > o_count:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:
                moves.add((i, j))
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if not (0 <= i < 3 and 0 <= j < 3):
        raise Exception("Invalid Action: Index out of range")
    if board[i][j] is not EMPTY:
        raise Exception("Invalid Action: Cell already taken")
    new_board = copy.deepcopy(board)
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows and columns
    for i in range(3):
        if board[i][0] and board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]
        if board[0][i] and board[0][i] == board[1][i] == board[2][i]:
            return board[0][i]

    # Check diagonals
    if board[0][0] and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    for row in board:
        if EMPTY in row:
            return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    current = player(board)
    best_action = None

    if current == X:
        best_score = float('-inf')
        for action in actions(board):
            score = minimax_score(result(board, action))
            if score > best_score:
                best_score = score
                best_action = action
    else:
        best_score = float('inf')
        for action in actions(board):
            score = minimax_score(result(board, action))
            if score < best_score:
                best_score = score
                best_action = action

    return best_action


def minimax_score(board):
    if terminal(board):
        return utility(board)

    current = player(board)

    if current == X:
        best = float('-inf')
        for action in actions(board):
            score = minimax_score(result(board, action))
            best = max(best, score)
        return best
    else:
        best = float('inf')
        for action in actions(board):
            score = minimax_score(result(board, action))
            best = min(best, score)
        return best
