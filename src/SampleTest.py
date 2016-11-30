"""
sampleTest.py should be test cases where important functions/algorithms are to be tested against.
"""

import unittest
import Othello
import Algorithms


class OthelloTest(unittest.TestCase):

    # def setUp(self):
    # def tearDown(self):

    def testGameOver(self):
        self.game = Othello.Othello([
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, 0, 1, None, None, None],
            [None, None, None, 1, 0, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
        ])
        self.failUnless(not self.game.is_game_over())


# class AlgorithmsTest(unittest.TestCase):
#
#     # def setUp(self):
#     # def tearDown(self):


def main():
    unittest.main()

if __name__ == '__main__':
    main()
