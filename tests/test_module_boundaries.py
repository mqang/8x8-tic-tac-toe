import unittest

import ai_strategy
import board
import game_session
import main
import textual_ui


class ModuleBoundaryTests(unittest.TestCase):
    def test_domain_modules_expose_current_public_api(self):
        self.assertIs(board.Problem, main.Problem)
        self.assertIs(ai_strategy.Search_Strategy, main.Search_Strategy)
        self.assertIs(game_session.GameSession, main.GameSession)
        self.assertIs(textual_ui.TicTacToeApp, main.TicTacToeApp)

    def test_shared_board_constants_are_importable(self):
        self.assertEqual(board.BOARD_SIZE, 8)
        self.assertEqual(board.WIN_LENGTH, 4)
        self.assertEqual(board.BOARD_CELLS, 64)
        self.assertEqual(board.CENTER_MOVES, {27, 28, 35, 36})


if __name__ == "__main__":
    unittest.main()
