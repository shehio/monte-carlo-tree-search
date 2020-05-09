from twoplayergame import GameState
from montecarlotreesearch import MonteCarloTreeSearch

import numpy as np
import random

if __name__ == '__main__':
    game = GameState()
    p1 = MonteCarloTreeSearch(game)

    while game.is_game_over() == np.inf:
        p1_move = p1.get_best_move(game)
        game = game.make_move('p1', p1_move)

        p2_move = game.make_move(random.choice(game.get_legal_actions()))
        game = game.mak_move('p2', p2_move)

    print(game)