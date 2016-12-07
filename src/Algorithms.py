"""
algorithms.py should contain the search algorithms and strategies we'll implement to achieve 2 AI playing Othello.

These algorithms will determine the next move of current player based on current board.
"""
import Othello
import random


def random(game):
    """
    Randomly make a possible move. No strategy is used.
    :param game: A Othello instance which represent the current game. (board, player, etc.)
    :return: Return a game that represents the next move of current player randomly.
    """
    if type(game) != Othello.Othello:
        raise TypeError("parameter game is not an Othello instance")
    successors = game.successors()
    return successors[random.randint(0, len(successors)-1)]


def most_eliminate(game):
    """
    Make a move that will eliminate most opponent's piece at current situation.
    :param game: A Othello instance
    :return: Return an Othello instance with move made to eliminate most opponent's piece
    """
    if type(game) != Othello.Othello:
        raise TypeError("parameter game is not an Othello instance")
    successors = game.successors()
    least_opponent_piece = game.count_disks(game.switch_turn())
    most_elimination = successors[0]
    for successor in successors:
        new_oppo_piece = successor.count_disks(successor.switch_turn())
        if new_oppo_piece < least_opponent_piece:
            least_opponent_piece = new_oppo_piece
            most_elimination = successor
    return most_elimination

def minmax_move(game, depth, max_player):
    """
    Make a  best move that maximizes the max_player chances to win.
    :param game: A Othello instance.
    :param deth: number of turns till the end of the game taken into account.
    :param max_player: if the player is white piece or not (boolean value) -> we assume that active player is white piece and opponent is black.
    :return: return the best move to make player win the game.
    """
    d = depth
    successors = game.successors()
    best_move = successors[0]
    best_value = minmax(game.clone(best_move), d, False)
    for successor in successors:
        value = minmax(game.clone(best_move), d, False)
        if((max_player and (value > best_value)) or (not max_player and (value < best_value))):
            best_move = successor
            best_value =value
    return best_move
##### helper function to perform minmax algorithm ########
def minmax(game, depth, max_player):
    """
    Returns the most number pieces on the board if the player makes a certain move.
    """
    if type(game) != Othello.Othello:
        raise TypeError("parameter game is not an Othello instance")
    if(depth <= 0 or game.is_game_over()):
        return game.get_winner()
    successors = game.successors()
    if max_player:
        #maximizing
        best_value = game.count_disks(1) #because max_player is white.
        for successor in successors:
            value = minmax(successor, depth -1, False) #false because next turn would be for black which is a min player.
            best_value = max(best_value, value)
        return best_value
