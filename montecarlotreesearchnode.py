from __future__ import annotations
import logging
import numpy as np

from twoplayergame import GameState


class MonteCarloTreeSearchNode:
    def __init__(self, game_state: GameState, parent: MonteCarloTreeSearchNode, action=None):
        self.game_state = game_state
        self.parent = parent
        self.action = action
        self.children = np.array([], dtype=MonteCarloTreeSearchNode)
        self.untried_actions = game_state.get_valid_moves()
        self.wins = dict(map(lambda player: (player, 0), game_state.players))
        self.wins['Draw'] = 0
        self.visits = 0

    def select(self, c) -> MonteCarloTreeSearchNode:
        leaf_node = self

        while not leaf_node.is_terminal:
            if not leaf_node.is_fully_expanded:
                return leaf_node.expand()
            else:
                leaf_node = leaf_node.select_child_with_max_ucb(c)

        return leaf_node

    def expand(self) -> MonteCarloTreeSearchNode:
        logging.debug(f'Expanding for {self.__repr__()}')
        action = self.untried_actions.pop()
        new_game_state = self.game_state.make_move(action)
        child_node = MonteCarloTreeSearchNode(new_game_state, self, action)
        self.children = np.append(self.children, child_node)
        logging.debug(f'Created {child_node.__repr__()}')
        return child_node

    def rollout(self) -> float:
        logging.debug(f'Rollout now for {self.__repr__()}')
        rollout_state = self.game_state
        while rollout_state.is_game_over is None:
            possible_moves = rollout_state.get_valid_moves()
            move = possible_moves[np.random.randint(len(possible_moves))]
            rollout_state = rollout_state.make_move(move)
        logging.debug(f'The winner of this rollout: {rollout_state.winner}')
        return rollout_state.winner

    def backpropagate(self, who_won):
        self.visits += 1
        self.wins[who_won] += 1
        if self.parent is not None:
            self.parent.backpropagate(who_won)

    def select_child_with_max_ucb(self, c) -> MonteCarloTreeSearchNode:
        ucb_values = list(map(lambda child: MonteCarloTreeSearchNode.get_ucb(child, c), self.children))
        return self.children[np.argmax(ucb_values)]

    @staticmethod
    def get_ucb(child: MonteCarloTreeSearchNode, c):
        return child.win_ratio + c * np.sqrt(np.log(child.parent.visits) / child.visits)

    @property
    def win_ratio(self):
        # If the node hasn't been visited, then the win_ratio (part of ucb) is inf. This means it will be selected.
        if self.visits == 0:
            return np.inf
        return self.wins[self.game_state.current_player] / self.visits

    @property
    def is_fully_expanded(self):
        return len(self.children) == len(self.game_state.get_valid_moves())

    @property
    def is_terminal(self):
        return self.game_state.winner is not None

    def __repr__(self):
        return f'TreeNode: {id(self)}'

    def __str__(self):
        return f'TreeNode: {id(self)}, action: {self.action}, number of visits: {self.visits}, ' \
               f'win ratio: {self.win_ratio}, fully expanded: {self.is_fully_expanded}, ' \
               f'children: {self.children}'
