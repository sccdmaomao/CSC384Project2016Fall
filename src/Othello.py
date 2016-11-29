'''
othello.py should contain everything the game needs to be play, 
i.e. the 8x8 board, the rules of placing down pieces, the winning condition check. etc.
'''

class Othello:
    '''
    The game board will be represented by a 8 by 8 grid. Using a nested list.
    Each blank is either 0 for black piece, 1 for white piece, or None for empty
    Example:
    the initial board of Othello would be
    [
    [None None, None, None, None ,None, None, None],
    [None None, None, None, None ,None, None, None],
    [None None, None, None, None ,None, None, None],
    [None None, None, 0, 1 ,None, None, None],
    [None None, None, 1, 0 ,None, None, None],
    [None None, None, None, None ,None, None, None],
    [None None, None, None, None ,None, None, None],
    [None None, None, None, None ,None, None, None],
    ]
    '''
    def __init__(self, board = [[None]*8]*8):
        self.board = board
        
        # num of pieces need to be updated each time a player drop a move.
        self.numOfWhite = countPiece(1)
        self.numOfBlack = countPiece(0)
        
    def is_gameOver(self):
        '''
        Game is over when all the empty space has been filled.
        '''
        for row in self.board:
            for col in self.board:
                if self.board[row][col] == None:
                    return False
        return True
    
    def winner(self):
        '''
        Return winning color if game is over.
        '''
        if is_gameOver():
            if self.numOfWhite > self.numOfBlack:
                return 1
            return 0
        return None # no winner yet
            
            
    def countPiece(self, color):
        '''
        Return the number of piecies on current board.
        0 = black
        1 = white
        '''
        count = 0
        for row in self.board:
            for col in self.board:
                if self.board[row][col] == color:
                    count += 1
        return count
    
    def placePiece(self, color, position):
        '''
        Place a piece of color color, update the board and recalculate the numbers of pieces.
        Also check game condition at the end.
        '''