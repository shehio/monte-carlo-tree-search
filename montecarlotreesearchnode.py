from __future__ import annotations

import numpy as np


class MonteCarloTreeSearchNode:
    def __init__(self, game_state, parent):
        self.game_state = game_state
        self.parent = parent
        self.children = np.array([], dtype=MonteCarloTreeSearchNode)
        self.wins = 0
        self.number_of_visits = 0

    def select(self) -> MonteCarloTreeSearchNode:
        pass

    def expand(self) -> MonteCarloTreeSearchNode:
        pass

    def rollout(self) -> float:
        pass

    def backpropagate(self):
        pass

    def select_child_with_max_ucb(c):
        pass

    @property
    def win_ratio(self):
        # If the node hasn't been visited, then the win_ratio (part of ucb) is inf. This means it will be selected.
        if self.number_of_visits == 0:
            return np.inf
        return self.wins / self.number_of_visits

    @staticmethod
    def get_ucb(child: MonteCarloTreeSearchNode, c):
        child.win_ratio + c * np.sqrt(np.log(child.parent.number_of_visits) / child.number_of_visits)


