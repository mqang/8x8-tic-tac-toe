import unittest

from game_session import GameSession


class GameSessionTests(unittest.TestCase):
    def test_initial_state_starts_on_player_turn(self):
        session = GameSession()

        self.assertEqual(session.current_player, "X")
        self.assertEqual(session.selected_position, 1)
        self.assertFalse(session.game_over)
        self.assertIsNone(session.winner)
        self.assertIsNone(session.last_player_move)
        self.assertIsNone(session.last_ai_move)

    def test_player_move_updates_board_and_ai_replies(self):
        session = GameSession()

        moved = session.play_position(1)

        self.assertTrue(moved)
        self.assertEqual(session.problem.board_state_back_end[0], "X")
        self.assertEqual(session.last_player_move, 1)
        self.assertIn(session.last_ai_move, {28, 29, 36, 37})
        self.assertEqual(session.current_player, "X")
        self.assertFalse(session.game_over)

    def test_rejects_occupied_cell_without_triggering_ai(self):
        session = GameSession()
        session.play_position(1)
        original_ai_move = session.last_ai_move

        moved = session.play_position(1)

        self.assertFalse(moved)
        self.assertEqual(session.last_player_move, 1)
        self.assertEqual(session.last_ai_move, original_ai_move)
        self.assertIn("already", session.status_message)

    def test_player_win_ends_game_before_ai_moves(self):
        session = GameSession()
        session.problem.update_board(1, "X")
        session.problem.update_board(2, "X")
        session.problem.update_board(3, "X")

        moved = session.play_position(4)

        self.assertTrue(moved)
        self.assertTrue(session.game_over)
        self.assertEqual(session.winner, "X")
        self.assertIsNone(session.last_ai_move)

        moved_after_game_over = session.play_position(5)
        self.assertFalse(moved_after_game_over)
        self.assertEqual(session.problem.board_state_back_end[4], " ")

    def test_player_win_records_winning_line(self):
        session = GameSession()
        session.problem.update_board(1, "X")
        session.problem.update_board(2, "X")
        session.problem.update_board(3, "X")

        session.play_position(4)

        self.assertEqual(session.winning_line, (0, 1, 2, 3))


if __name__ == "__main__":
    unittest.main()
