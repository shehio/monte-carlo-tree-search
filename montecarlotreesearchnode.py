from __future__ import annotations
import numpy as np

from twoplayergame import GameState


class MonteCarloTreeSearchNode:
    def __init__(self, game_state: GameState, parent: MonteCarloTreeSearchNode, player):
        self.game_state = game_state
        self.parent = parent
        self.player = player
        self.children = np.array([], dtype=MonteCarloTreeSearchNode)
        self.wins = 0
        self.visits = 0

    def select(self, c) -> MonteCarloTreeSearchNode:
        leaf_node = self

        while not leaf_node.terminal:
            if not self.is_fully_expanded:
                return self.expand()
            else:
                leaf_node = self.select_child_with_max_ucb(c)

        return leaf_node

    def expand(self) -> MonteCarloTreeSearchNode:
        pass

    def rollout(self) -> float:
        pass

    def backpropagate(self, win):
        self.visits += 1
        self.wins += win
        if self.parent is not None:
            self.parent.backpropagate(win)

    def select_child_with_max_ucb(self, c):
        ucb_values = list(map(lambda child: MonteCarloTreeSearchNode.get_ucb(child, c), self.children))
        return self.children(np.argmax(ucb_values))

    @staticmethod
    def get_ucb(child: MonteCarloTreeSearchNode, c):
        child.win_ratio + c * np.sqrt(np.log(child.parent.visits) / child.visits)

    @property
    def win_ratio(self):
        # If the node hasn't been visited, then the win_ratio (part of ucb) is inf. This means it will be selected.
        if self.visits == 0:
            return np.inf
        return self.wins / self.visits

    @property
    def is_fully_expanded(self):
        return len(self.children) == len(self.game_state.get_legal_actions(self.player))

    @property
    def is_terminal(self):
        return self.game_state.is_game_over()
