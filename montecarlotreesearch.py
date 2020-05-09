import numpy as np

from twoplayergame import GameState
from montecarlotreesearchnode import MonteCarloTreeSearchNode


class MonteCarloTreeSearch:
    # Note that there's no training / testing here.
    # Only get the best move to make according to simulation, regardless of how deep the actual game tree is.
    # Note that, at number_of_simulation = inf, MCTS --> Minimax.
    @staticmethod
    def get_best_move(game_state: GameState, number_of_simulation=100):
        root = MonteCarloTreeSearchNode(game_state)
        for i in range(number_of_simulation):
            print(f'Iteration number: {i + 1}')
            leaf_node = root.select(c=np.sqrt(2))
            reward = leaf_node.rollout()
            leaf_node.backpropagate(reward)

        MonteCarloTreeSearch.__print_tree(root)

        # When finally choosing an action, we shouldn't be exploring.
        return root.select_child_with_max_ucb(c=0)

    @staticmethod
    def __print_tree(root: MonteCarloTreeSearchNode):
        print('\nPrinting the current tree:')
        queue = [root]
        while queue:
            popped_node = queue.pop()
            print(popped_node)
            for child_node in popped_node.children:
                queue.append(child_node)
