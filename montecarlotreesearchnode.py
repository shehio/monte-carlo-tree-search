class MonteCarloTreeSearchNode:
    def __init__(self, game_state):
        self.game_state = game_state
        self.wins = 0
        self.number_of_simulations = 0

    def select(self):
        pass

    def expand(self):
        pass

    def rollout(self):
        pass

    def backpropagate(self):
        pass
