"""
Engine.py is an search engine that allow different configuration of the search to be
created and completed by 'AI'
"""


class SearchEngine:

    def __init__(self, strategy='random'):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def get_strategy(self):
        return self.strategy

    def search(self, init_state, goal_function, heuristic_function):
        """
        :param init_state: The initial state
        :param goal_function: The function to determine whether we achieved at goal or not. Return the winner at given state.
        :param strategy:
        :return: Return the goal, or False if search was not able to find such goal.
        """
        if goal_function(init_state) == init_state.current_player:  # if goal_function returns the winner
            return init_state