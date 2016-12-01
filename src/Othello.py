"""
Othello.py is a class that represent the game Othello.

Othello contains a 8x8 board represented by a nested list.
The list is filled with 0, 1, None.
where 0 represents black pieces,
1 represents white pieces,
and None represent empty spaces.

Othello class is able to determine if the game has ended or not.

When playing Othello, by default the white player play first.
"""

import copy
class Othello:
    """
    The game board will be represented by a 8 by 8 grid. Using a nested list.
    Each blank is either 0 for black piece, 1 for white piece, or None for empty
    Example:
    the initial board of Othello would be
    [
    [None None, None, None, None ,None, None, None],
    [None None, None, None, None ,None, None, None],
    [None None, None, None, None ,None, None, None],
    [None None, None, 1   , 0    ,None, None, None],
    [None None, None, 0   , 1    ,None, None, None],
    [None None, None, None, None ,None, None, None],
    [None None, None, None, None ,None, None, None],
    [None None, None, None, None ,None, None, None],
    ]
    """

    def __init__(self, board=[[None]*8]*8, current_player=1):
        self.board = board
        self.current_player = current_player  # white player starts first
        
        # num of pieces need to be updated each time a player drop a move.
        self.num_white = self.count_disks(1)
        self.num_black = self.count_disks(0)
        
    def successors(self):
        """
        Generate all position actions that can be performed based on current board and current player.
        :return: return a list where each element in the list is a Othello instance representing possible next state.
        """
        successors = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if type(self.board[row][col]) != int:  # an empty spot
                    if self.valid_position((row, col)):

                        # Construct an instance of Othello and add to successors
                        new_board = copy.deepcopy(self.board)
                        new_board[row][col] = self.current_player
                        next_player = 1 - self.current_player
                        new_state = Othello(new_board, next_player)
                        successors.append(new_state)

        return successors

    def valid_position(self, pos):
        """
        Checks whether a position is valid at position pos to place a disk.
        :param pos: A tuple where pos[0] is row and pos[1] is col of the board.
        :return: True iff we can place current_player's piece at position pos.
        """
        opponent = 1 - self.current_player
        row = pos[0]
        col = pos[1]

        # check right side of the pos
        if col < 6:
            tmp_col = col + 1
            while tmp_col < 7:
                if self.board[row][tmp_col] == opponent:
                    tmp_col += 1
                else:
                    break
            if tmp_col < 8 and tmp_col != col + 1 and self.board[row][tmp_col] == self.current_player:
                return True

        # check left side of the pos
        if col > 1:
            tmp_col = col - 1
            while tmp_col > 0:
                if self.board[row][tmp_col] == opponent:
                    tmp_col -= 1
                else:
                    break
            if tmp_col > -1 and tmp_col != col - 1 and self.board[row][tmp_col] == self.current_player:
                return True

        # check top side of the pos
        if row > 1:
            tmp_row = row - 1
            while tmp_row > 0:
                if self.board[tmp_row][col] == opponent:
                    tmp_row -= 1
                else:
                    break
            if tmp_row > -1 and tmp_row != row - 1 and self.board[tmp_row][col] == self.current_player:
                return True

        # check bottom side of the pos
        if row < 6:
            tmp_row = row + 1
            while tmp_row < 7:
                if self.board[tmp_row][col] == opponent:
                    tmp_row += 1
                else:
                    break
            if tmp_row < 8 and tmp_row != row + 1 and self.board[tmp_row][col] == self.current_player:
                return True
        return False

    def is_game_over(self):
        """
        Check game ending conditions.
        Game is over when all the empty space has been filled.
        Or neither players can make a valid move.
        :return: True iff game is over.
        """

        if not self.successors():  # if list is empty.
            # pass turn to opponent to see if neither has possible move.
            self.current_player = 1 - self.current_player
            if not self.successors():
                return True   # Game ended with no more possible move
            self.current_player = 1 - self.current_player  # switch player back
        return False
    
    def get_winner(self):
        """
        :return:  The winner or "Tie Game" for tie.
        or None if game is not over yet.
        """

        if self.is_game_over():
            if self.num_white > self.num_black:
                return 1
            elif self.num_white < self.num_black:
                return 0
            return "Tie Game"  # Tie game
        return None  # no winner yet
            
    def count_disks(self, color):
        """
        :param color: The color in which to count for.
        :return: number of color pieces on current board.
        """

        count = 0
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == color:
                    count += 1
        return count
    
    def place_piece(self, position):
        """
        Place a piece of current player's color.
        This function will also update the board, update current_player,
        and check for gaming ending conditions.
        :param position: The position where to drop a piece, it's a tuple (row, col) to define the place in nested list.
        :return: Return the winner if game is ended. else None
        """
        if not self.valid_position(position):
            raise ValueError(str.format("The position trying to place was not acceptable row:{0} col:{1}", position[0], position[1]))

        self.board[position[0]][position[1]] = self.current_player  # place down the piece
        if self.is_game_over():
            return self.get_winner()
        else:
            self.current_player = 1 - self.current_player
        return None

    def print_board(self):
        """
        Print the String representation of the board.
        :return: Nothing
        """
        for row in range(len(self.board)):
            print("|", end="")
            for col in range(len(self.board[row])):
                char = " "
                if type(self.board[row][col]) == int:
                    char = self.board[row][col]
                print(char, end="|")
            print("")


