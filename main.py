from twoplayergame import GameState
from montecarlotreesearch import MonteCarloTreeSearch
from player import Player

from functools import partial
import numpy as np
import random


def partial_mcts(number_of_simulation, game_state):
    return MonteCarloTreeSearch.get_best_move(game_state, number_of_simulation)


if __name__ == '__main__':
    simulation_count = 100

    p1 = Player('p1', partial(partial_mcts, simulation_count))
    p2 = Player('p2', lambda game_state: random.choice(game_state.get_valid_moves()))

    game = GameState(np.array([p1, p2]), turn=1)
    print(game)

    while game.is_game_over is None:
        valid_moves = game.get_valid_moves()
        m1 = p1.get_move(game)
        game = game.make_move(m1)
        game = game.make_move(p2.get_move(game))
        print(game)
