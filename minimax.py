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

        scores = np.array([])
        valid_moves = game_state.get_valid_moves()

        if game_state.current_player == maximizing_player:
            for move in valid_moves:
                new_game_state = game_state.copy().make_move(move)
                score = Minimax.__minimax_helper(new_game_state, maximizing_player, depth + 1)
                scores = np.append(scores, score[0])

            max_eval = max(scores)
            arg_max_move = valid_moves[np.argmax(scores)]
            Minimax.__print_debugging_info(depth, scores, valid_moves, max_eval, arg_max_move)

            return max_eval, arg_max_move

        else:
            for move in valid_moves:
                new_game_state = game_state.copy().make_move(move)
                score = Minimax.__minimax_helper(new_game_state, maximizing_player, depth + 1)
                scores = np.append(scores, score[0])

            return min(scores), None

    @classmethod
    def __print_debugging_info(cls, depth, scores, valid_moves, max_eval, arg_max_move):
        if depth == 0:
            logging.debug('============ MINIMAX ============')
            logging.debug(f'Scores: {scores}')
            logging.debug(f'Moves: {valid_moves}')
            logging.debug(f'Max Eval: {max_eval}')
            logging.debug(f'Arg Max Move: {arg_max_move}')
            logging.debug('============ MINIMAX ============')
