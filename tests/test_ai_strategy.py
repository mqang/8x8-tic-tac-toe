import unittest

from ai_strategy import Search_Strategy
from board import Problem


def make_board(pieces):
    board = [' ' for _ in range(64)]
    for position, symbol in pieces.items():
        board[position - 1] = symbol
    return board


class AIStrategyTests(unittest.TestCase):
    def best_move(self, pieces, first_move=False):
        strategy = Search_Strategy(Problem())
        strategy.first_move = first_move
        move = strategy.find_best_move(make_board(pieces))
        return None if move is None else move + 1

    def test_first_response_to_corner_takes_central_square(self):
        self.assertIn(
            self.best_move({1: 'X'}, first_move=True),
            {28, 29, 36, 37},
        )

    def test_extends_two_in_a_row_into_direct_threat(self):
        self.assertIn(
            self.best_move({25: 'O', 27: 'O', 1: 'X', 64: 'X'}),
            {26, 28},
        )

    def test_blocks_opponent_two_in_a_row_before_it_becomes_a_threat(self):
        self.assertIn(
            self.best_move({25: 'X', 27: 'X', 5: 'O', 60: 'O'}),
            {26, 28},
        )

    def test_immediate_win_still_takes_priority(self):
        self.assertEqual(
            self.best_move({1: 'O', 2: 'O', 3: 'O', 10: 'X', 11: 'X'}),
            4,
        )

    def test_immediate_block_still_takes_priority(self):
        self.assertEqual(
            self.best_move({1: 'X', 2: 'X', 3: 'X', 10: 'O', 11: 'O'}),
            4,
        )


if __name__ == "__main__":
    unittest.main()
