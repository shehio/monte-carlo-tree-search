from __future__ import annotations
import logging
import numpy as np

from drawplayer import SingletonDrawPlayer
from gamestate import GameState
from rolloutstrategyhelper import RolloutStrategyHelper


class MonteCarloTreeSearchNode:
    # This action in the params is the action that the player from the parent MCTS node, i.e. the prev game state, has
    # played. This information is critical for when we're calculating the win ratio (see below).
    def __init__(self, game_state: GameState, parent: MonteCarloTreeSearchNode, action=None):
        self.game_state = game_state
        self.parent = parent
        self.action = action
        self.children = np.array([], dtype=MonteCarloTreeSearchNode)
        self.untried_actions = game_state.get_valid_moves()
        self.wins = dict(map(lambda player: (player, 0), game_state.players))
        self.wins[SingletonDrawPlayer] = 0
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

    # The learning depends highly on the rollout strategy.
    def rollout(self):
        logging.debug(f'Rollout now for {self.__repr__()}')
        rollout_state = self.game_state
        while not rollout_state.is_game_over:
            move = MonteCarloTreeSearchNode.get_move_from_rollout_strategy(rollout_state)
            rollout_state = rollout_state.make_move(move)
        logging.debug(f'The winner of this rollout: {rollout_state.winner}')
        return rollout_state.winner

    def backpropagate(self, who_won):
        self.visits += 1
        self.wins[who_won] += 1
        if self.parent is not None:
            self.parent.backpropagate(who_won)

    # This ratio tries to maximize the winning. It doesn't try to minimize losing.
    def select_child_with_max_ucb(self, c) -> MonteCarloTreeSearchNode:
        ucb_values = list(map(lambda child: MonteCarloTreeSearchNode.get_ucb(child, c), self.children))
        return self.children[np.argmax(ucb_values)]

    @staticmethod
    def get_ucb(child: MonteCarloTreeSearchNode, c):
        return child.win_ratio + c * np.sqrt(np.log(child.parent.visits) / child.visits)

    @staticmethod
    def get_move_from_rollout_strategy(rollout_state: GameState) -> int:
        return RolloutStrategyHelper.get_heuristic_move(rollout_state)

    @property
    def win_ratio(self):
        if self.parent is None:  # In case it's the parent node.
            return 0
        # If the node hasn't been visited, then the win_ratio (part of ucb) is inf. This means it will be selected.
        if self.visits == 0:
            return np.inf
        return self.wins[self.parent.game_state.current_player] / self.visits

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
               f'children: {self.children}, turn: {self.game_state.turn}, game: \n{self.game_state}'
