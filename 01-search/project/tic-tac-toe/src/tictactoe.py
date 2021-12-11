"""
Tic Tac Toe Player
"""

import copy

X = "X"
O = "O"
EMPTY = None
INFINITY = 1e3


class InvalidAction(Exception):
    "Raised when the action is not available"
    pass


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

    X starts the game.
    """
    # initialize counters
    x_counter, o_counter = 0, 0

    for each_row in board: 
        # row-wise count of each X and O's
        x_counter += each_row.count(X)
        o_counter += each_row.count(O)
    
    # O plays if and only if it has less turns on board
    if o_counter < x_counter:
        return O
    
    return X    


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    
    An available in this game refers to a position on board where no X nor O is 
    chosen yet.
    """
    action_set = set()
    for row_index, row in enumerate(board):
        for col_index, value in enumerate(row):
            if value not in (X, O):
                action_set.add((row_index, col_index))

    return action_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.

    Cannot overwrite values.
    """
    # check if action is a valid action
    if action not in actions(board):
        raise InvalidAction("You have performed an invalid action.")

    # whose turn it is now? result will be either X or O
    current_player = player(board)

    # create a deep copy so as not to substitute values
    new_board = copy.deepcopy(board)
    
    row_index, col_index = action 
    new_board[row_index][col_index] = current_player

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check for consecutive positioning
    # assume square board
    BOARD_SIZE = len(board)

    # row-wise
    for each_row in board: 
        if each_row.count(X) == BOARD_SIZE:
            return X
        if each_row.count(O) == BOARD_SIZE:
            return O
    
    # column-wise
    for col_index in range(BOARD_SIZE):
        column = [row[col_index] for row in board]
        if column.count(X) == BOARD_SIZE:
            return X
        if column.count(O) == BOARD_SIZE:
            return O

    # diagonal-wise
    # main diagonal i = j
    main_diagonal = [board[i][i] for i in range(BOARD_SIZE)]
    # anti diagonal i = len(matrix) -1 -j
    anti_diagonal = [board[BOARD_SIZE-1-i][i] for i in range(BOARD_SIZE)]
    if main_diagonal.count(X) == BOARD_SIZE \
        or anti_diagonal.count(X) == BOARD_SIZE:
        return X
    if main_diagonal.count(O) == BOARD_SIZE \
        or anti_diagonal.count(O) == BOARD_SIZE:
        return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # the game is over when X or O is the winner
    if winner(board) in (X, O):
        return True

    # or if the board is full (i.e., there are no EMPTY anymore)
    if not any(map(lambda x : EMPTY in x, board)):
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    VICTORY = 1
    DEFEAT = -1
    DRAW = 0

    if winner(board) == X:
        return VICTORY
    elif winner(board) == O:
        return DEFEAT

    return DRAW


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    
    If I'm the maximizing player, I want to choose from my actions, the one that will 
    lead to the MAXIMUM possible outcome, from the outcomes my opponent has offered me. 
    And, of course, my opponent has tried to minimize the outcome to offer me.

    On the contrary, if it's the the minimizing player's turn, now I'm in the shoes of my opponent.
    In this case, as per my point of view, he/she is trying to minimize my outcome. Then I need to 
    choose from his/her actions, the one that will lead to the MINIMUM possible outcome 
    which is what he/she would do. 

    Of course, this supposes that your opponent is playing optimally.
    """
    if terminal(board):
        return None
    
    current_player = player(board)

    if current_player == X:
        # i'm the maximizing player, my opponent is the minimizing player
        candidate_outcome = -INFINITY 
        for action in actions(board):
            possible_board = result(board, action)
            # opponent is trying to minimize this action of mine
            opponents_utility = min_value(possible_board)
            # store info (action and utility) from the maximum 
            # value my opponent has given to me
            if opponents_utility > candidate_outcome:
                candidate_outcome = opponents_utility
                candidate_action = action
    elif current_player == O:
        # i'm the minimizing player, my opponent is the maximizing player
        candidate_outcome = INFINITY
        for action in actions(board):
            possible_board = result(board, action)
            # I am trying to maximize this action of my opponent
            opponents_utility = max_value(possible_board)
            # store info (action and utility) from the minimum 
            # value my opponent has given to me
            if opponents_utility < candidate_outcome:
                # store this result
                candidate_outcome = opponents_utility
                candidate_action = action

    return candidate_action


def max_value(board):
    """
    The maximizing player picks action a in set of actions that 
    produces the highest value of min_value(result(state, action)).
    """
    v = -INFINITY
    if terminal(board):
        return utility(board)

    for action in actions(board):
        # get the resulting board for a given action
        resulting_board = result(board, action)
        # check the best option for the next player
        v = max(v, min_value(resulting_board))
    
    return v


def min_value(board):
    """
    The minimizing player picks action a in set of actions that 
    produces the lowest value of max_value(result(state, actions)).
    """
    v = INFINITY
    if terminal(board):
        return utility(board)

    for action in actions(board):
        # get the resulting board for a given action
        resulting_board = result(board, action)
        # check the best option for the next player
        v = min(v, max_value(resulting_board))
    
    return v
