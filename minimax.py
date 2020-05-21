import numpy as np
import logging

from drawplayer import SingletonDrawPlayer
from gamestate import GameState


class Minimax:

    @staticmethod  # No evaluation function; eq. no max depth. Go all the way down.
    def get_best_move(game_state: GameState):
        current_player = game_state.current_player
        _, move = Minimax.__minimax_helper(game_state, current_player, 0)
        return move

    @staticmethod
    def __minimax_helper(game_state: GameState, maximizing_player, depth):
        if game_state.is_game_over:
            if game_state.winner.name == maximizing_player.name:
                return 100, None
            elif game_state.winner is SingletonDrawPlayer:
                return 0, None
            elif game_state.is_game_over:
                return -100, None

        if game_state.current_player == maximizing_player:
            scores = np.array([])
            valid_moves = game_state.get_valid_moves()
            for move in valid_moves:
                new_game_state = game_state.copy().make_move(move)
                score = Minimax.__minimax_helper(new_game_state, maximizing_player, depth + 1)
                scores = np.append(scores, score[0])

            max_eval = max(scores)
            arg_max_move = valid_moves[np.argmax(scores)]
            if depth == 0:
                logging.info('============ MINIMAX ============')
                logging.info(f'Scores: {scores}')
                logging.info(f'Moves: {valid_moves}')
                logging.info(f'Max Eval: {max_eval}')
                logging.info(f'Arg Max Move: {arg_max_move}')
                logging.info('============ MINIMAX ============')

            return max_eval, arg_max_move

        else:
            valid_moves = game_state.get_valid_moves()
            scores = np.array([])
            for move in valid_moves:
                new_game_state = game_state.copy().make_move(move)
                score = Minimax.__minimax_helper(new_game_state, maximizing_player, depth + 1)
                scores = np.append(scores, score[0])
            min_eval = min(scores)
            arg_min_move = valid_moves[np.argmax(scores)]

            return min_eval, None
