import numpy as np

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
        for i in range(number_of_simulation):
            print(f'Iteration number: {i + 1}')
            leaf_node = self.root.select(c=np.sqrt(2))
            reward = leaf_node.rollout()
            leaf_node.backpropagate(reward)

        self.__print_tree(self.root)

        # When finally choosing an action, we shouldn't be exploring.
        return self.root.select_child_with_max_ucb(c=0)

    @staticmethod
    def __print_tree(root: MonteCarloTreeSearchNode):
        print('\nPrinting the current tree:')
        queue = [root]
        while queue:
            popped_node = queue.pop()
            print(popped_node)
            for child_node in popped_node.children:
                queue.append(child_node)
