import numpy as np

from gamestate import GameState


class RolloutStrategyHelper:

    @staticmethod
    def get_heuristic_move(game_state: GameState) -> int:
        winning_number_minus_one = game_state.turn * (game_state.board_size - 1)

        row_sum = game_state.game_board.sum(1)
        for i in range(0, len(row_sum)):
            if row_sum[i] == winning_number_minus_one:
                for j in range(0, game_state.board_size):
                    if game_state.game_board[i][j] == 0:
                        return game_state.reverse_move_map[(i, j)]

        col_sum = game_state.game_board.sum(0)
        for j in range(0, len(col_sum)):
            if col_sum[j] == winning_number_minus_one:
                for i in range(0, game_state.board_size):
                    if game_state.game_board[i][j] == 0:
                        return game_state.reverse_move_map[(i, j)]

        diagonal = [game_state.game_board.trace()]
        if diagonal == winning_number_minus_one:
            for i in range(0, game_state.board_size):
                if game_state.game_board[i][i] == 0:
                    return game_state.reverse_move_map[(i, i)]

        inv_diagonal = [game_state.game_board[::-1].trace()]
        if inv_diagonal == winning_number_minus_one:
            for i in range(0, game_state.board_size):
                if game_state.game_board[i][(game_state.board_size - 1) - i] == 0:
                    return game_state.reverse_move_map[(i, (game_state.board_size - 1) - i)]

        return RolloutStrategyHelper.get_defensive_move(game_state)

    @staticmethod
    def get_defensive_move(game_state: GameState) -> int:
        winning_number_minus_one = -1 * game_state.turn * (game_state.board_size - 1)

        row_sum = game_state.game_board.sum(1)
        for i in range(0, len(row_sum)):
            if row_sum[i] == winning_number_minus_one:
                for j in range(0, game_state.board_size):
                    if game_state.game_board[i][j] == 0:
                        return game_state.reverse_move_map[(i, j)]

        col_sum = game_state.game_board.sum(0)
        for j in range(0, len(col_sum)):
            if col_sum[j] == winning_number_minus_one:
                for i in range(0, game_state.board_size):
                    if game_state.game_board[i][j] == 0:
                        return game_state.reverse_move_map[(i, j)]

        diagonal = [game_state.game_board.trace()]
        if diagonal == winning_number_minus_one:
            for i in range(0, game_state.board_size):
                if game_state.game_board[i][i] == 0:
                    return game_state.reverse_move_map[(i, i)]

        inv_diagonal = [game_state.game_board[::-1].trace()]
        if inv_diagonal == winning_number_minus_one:
            for i in range(0, game_state.board_size):
                if game_state.game_board[i][(game_state.board_size - 1) - i] == 0:
                    return game_state.reverse_move_map[(i, (game_state.board_size - 1) - i)]

        valid_moves = game_state.get_valid_moves()
        return valid_moves[np.random.randint(len(valid_moves))]
