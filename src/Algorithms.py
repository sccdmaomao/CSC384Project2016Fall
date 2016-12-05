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
    opponent_piece = game.count_disks(game.switch_turn())
    most_elimination = successors[0]
    for successor in successors:
        new_oppo_piece = successor.count_disks(successor.switch_turn())
        if new_oppo_piece < opponent_piece:
            most_elimination = successor
    return most_elimination