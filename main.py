from twoplayergame import GameState
from montecarlotreesearch import MonteCarloTreeSearch
from player import Player

from functools import partial
import numpy as np
import random

if __name__ == '__main__':
    game = GameState()

    mcts_strategy = partial(MonteCarloTreeSearch.get_best_move, number_of_simulation=100)
    p1 = Player('p1', mcts_strategy)

    p2 = Player('p2', lambda game_state: random.choice(game_state.get_legal_actions()))

    while game.is_game_over() == np.inf:
        game = game.make_move(p1.make_move(game))
        game = game.make_move(p2.make_move(game))
        print(game)
