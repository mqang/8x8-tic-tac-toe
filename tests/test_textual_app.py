import unittest

from textual_ui import TicTacToeApp


class TicTacToeAppTests(unittest.IsolatedAsyncioTestCase):
    async def test_inputs_are_blocked_until_mode_is_selected(self):
        app = TicTacToeApp()

        async with app.run_test() as pilot:
            await pilot.press("right")
            await pilot.press("enter")
            await pilot.click("#cell-9", offset=(1, 1))
            await pilot.pause()

            self.assertIsNone(app.session.input_mode)
            self.assertEqual(app.session.selected_position, 1)
            self.assertIsNone(app.session.last_player_move)
            self.assertIn("Choose", app.session.status_message)

    async def test_keyboard_navigation_and_move_update_session(self):
        app = TicTacToeApp()

        async with app.run_test() as pilot:
            await pilot.press("k")
            await pilot.press("right")
            self.assertEqual(app.session.selected_position, 2)

            await pilot.press("enter")

            self.assertEqual(app.session.last_player_move, 2)
            self.assertIsNotNone(app.session.last_ai_move)
            self.assertEqual(app.session.current_player, "X")

    async def test_mouse_click_plays_clicked_cell(self):
        app = TicTacToeApp()

        async with app.run_test() as pilot:
            await pilot.click("#mode-mouse", offset=(1, 1))
            await pilot.click("#cell-9", offset=(1, 1))
            await pilot.pause()

            self.assertEqual(app.session.last_player_move, 10)
            self.assertIsNotNone(app.session.last_ai_move)
            self.assertEqual(app.session.current_player, "X")

    async def test_keyboard_mode_ignores_mouse_clicks(self):
        app = TicTacToeApp()

        async with app.run_test() as pilot:
            await pilot.press("k")
            await pilot.click("#cell-9", offset=(1, 1))
            await pilot.pause()

            self.assertEqual(app.session.input_mode, "keyboard")
            self.assertIsNone(app.session.last_player_move)
            self.assertIn("Keyboard mode", app.session.status_message)

    async def test_mouse_mode_ignores_keyboard_moves(self):
        app = TicTacToeApp()

        async with app.run_test() as pilot:
            await pilot.press("m")
            await pilot.press("right")
            await pilot.press("enter")
            await pilot.pause()

            self.assertEqual(app.session.input_mode, "mouse")
            self.assertEqual(app.session.selected_position, 1)
            self.assertIsNone(app.session.last_player_move)
            self.assertIn("Mouse mode", app.session.status_message)

    async def test_board_cells_use_square_terminal_ratio(self):
        app = TicTacToeApp()

        async with app.run_test():
            cell = app.query_one("#cell-0")
            board = app.query_one("#board")

            self.assertEqual(cell.styles.width.value, 7)
            self.assertEqual(cell.styles.height.value, 3)
            self.assertEqual(board.styles.width.value, 58)

    async def test_game_layout_centers_board_under_meta(self):
        app = TicTacToeApp()

        async with app.run_test():
            game = app.query_one("#game")

            self.assertEqual(game.styles.align_horizontal, "center")

    async def test_keyboard_selection_uses_outline_without_fill(self):
        app = TicTacToeApp()

        async with app.run_test() as pilot:
            await pilot.press("k")
            await pilot.press("right")
            cell = app.query_one("#cell-1")

            self.assertEqual(cell.styles.background.a, 0)

    async def test_restart_is_blocked_while_ai_is_thinking(self):
        app = TicTacToeApp()

        async with app.run_test() as pilot:
            await pilot.press("k")
            app.session.ai_thinking = True
            await pilot.press("right")
            await pilot.press("r")

            self.assertEqual(app.session.selected_position, 2)
            self.assertIn("AI is thinking", app.session.status_message)

    async def test_winning_cells_are_highlighted_after_game_over(self):
        app = TicTacToeApp()

        async with app.run_test():
            app.session.problem.update_board(1, "X")
            app.session.problem.update_board(2, "X")
            app.session.problem.update_board(3, "X")
            app.session.play_player_position(4)
            app.refresh_view()

            winning_classes = [
                app.query_one(f"#cell-{index}").classes
                for index in range(4)
            ]

            self.assertTrue(all("winning-cell" in classes for classes in winning_classes))
            self.assertIn("YOU WIN", app.render_status().plain)


if __name__ == "__main__":
    unittest.main()
