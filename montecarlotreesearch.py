from twoplayergame import GameState
from montecarlotreesearchnode import MonteCarloTreeSearchNode


class MonteCarloTreeSearch:
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.root = MonteCarloTreeSearchNode(game_state)

    # Note that there's no training / testing here.
    # Only get the best move to make according to simulation, regardless of how deep the actual game tree is.
    # Note that, at number_of_simulation = inf, MCTS --> Minimax.
    def get_best_move(self, number_of_simulation=100):
        pass
