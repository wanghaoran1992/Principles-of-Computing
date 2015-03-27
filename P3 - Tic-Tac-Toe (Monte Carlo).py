"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 100    # Number of trials to run
MCMATCH = 1.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player
    
# Add your functions here.
def mc_trial(board, player):
    """
    Takes a board and the next player to move and plays
    the game picking random moves. Modifies the board
    and returns when the game is over
    """
    
    player_win = board.check_win()
    while player_win == None:
        empty = board.get_empty_squares()
        next_move = empty[random.randrange(len(empty))]
        board.move(next_move[0], next_move[1], player)
        player = provided.switch_player(player)
        player_win = board.check_win()
        
def mc_update_scores(scores, board, player):
    """
    Takes a grid of scores, a completed board, and which
    player is the machine player. Updates the scores board
    directly
    """
    winner = board.check_win()
    if winner == None or winner == provided.DRAW:
        return
    
    if winner == player:
        match_score = MCMATCH
        other_score = -1 * MCOTHER
    else:
        match_score = -1 * MCMATCH
        other_score = MCOTHER
    
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            status = board.square(row, col)
            if status == provided.EMPTY:
                pass
            elif status == player:
                scores[row][col] += match_score
            else:
                scores[row][col] += other_score
        
def get_best_move(board, scores):
    """
    Takes a current board and grid of scores and returns
    the square with the maximum score
    """
    empty = board.get_empty_squares()
    if len(empty) == 0:
        return
    
    vals = [scores[square[0]][square[1]] for square in empty]
    max_val = max(vals)
    moves = []
    
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if scores[row][col] == max_val and ((row, col) in empty):
                moves.append((row, col))
    
    ret_move = moves[random.randrange(len(moves))]
    return ret_move

def mc_move(board, player, trials):
    """
    Takes current board, which player is the machine player,
    and the number of trials to run. Returns a move for the
    machine player in the form of a (row, col) tuple
    """
    scores = [[0 for dummy_x in range(board.get_dim())] for dummy_y in range(board.get_dim())]
    for _ in range(trials):
        trial_board = board.clone()
        mc_trial(trial_board, player)
        mc_update_scores(scores, trial_board, player)
        
    return get_best_move(board, scores)


provided.play_game(mc_move, NTRIALS, False)
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)