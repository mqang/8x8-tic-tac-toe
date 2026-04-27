from ai_strategy import Search_Strategy
from board import BOARD_CELLS, BOARD_SIZE, Problem


class GameSession:
    def __init__(self):
        self.problem = Problem()
        self.search_strategy = Search_Strategy(self.problem)
        self.input_mode = None
        self.current_player = 'X'
        self.selected_index = 0
        self.last_player_move = None
        self.last_ai_move = None
        self.winner = None
        self.winning_line = None
        self.draw = False
        self.ai_thinking = False
        self.status_message = "Choose Keyboard or Mouse before playing."

    @property
    def selected_position(self):
        return self.selected_index + 1

    @property
    def game_over(self):
        return self.winner is not None or self.draw

    @property
    def move_count(self):
        return sum(value != ' ' for value in self.problem.board_state_back_end)

    def restart(self):
        self.__init__()

    def select_position(self, position):
        if 1 <= position <= BOARD_CELLS:
            self.selected_index = position - 1

    def choose_input_mode(self, mode):
        if self.input_mode is not None:
            self.status_message = f"{self.input_mode.title()} mode is already active."
            return False
        if mode not in {"keyboard", "mouse"}:
            return False

        self.input_mode = mode
        if mode == "keyboard":
            self.status_message = "Keyboard mode. Use arrow keys, then Enter."
        else:
            self.status_message = "Mouse mode. Click a cell to move."
        return True

    def move_selection(self, row_delta, col_delta):
        row, col = divmod(self.selected_index, BOARD_SIZE)
        next_row = min(max(row + row_delta, 0), BOARD_SIZE - 1)
        next_col = min(max(col + col_delta, 0), BOARD_SIZE - 1)
        self.selected_index = next_row * BOARD_SIZE + next_col

    def play_position(self, position):
        moved = self.play_player_position(position)
        if moved and self.current_player == 'O' and not self.game_over:
            self.play_ai_turn()
        return moved

    def play_player_position(self, position):
        if self.game_over:
            self.status_message = "Game over. Press R to restart or Q to quit."
            return False
        if self.ai_thinking or self.current_player != 'X':
            self.status_message = "AI is thinking. Wait for your turn."
            return False
        if not 1 <= position <= BOARD_CELLS:
            self.status_message = "Move must be between 1 and 64."
            return False

        index = position - 1
        if self.problem.board_state_back_end[index] in {'X', 'O'}:
            self.status_message = f"Cell {position} is already occupied."
            return False

        self.problem.update_board(position, 'X')
        self.last_player_move = position
        self.selected_index = index

        if self._finish_turn_if_game_over():
            return True

        self.current_player = 'O'
        self.status_message = "AI is thinking..."
        return True

    def play_ai_turn(self):
        if self.game_over or self.current_player != 'O':
            return

        best_move = self.search_strategy.find_best_move(self.problem.board_state_back_end)
        if best_move is None:
            self.draw = True
            self.status_message = "It's a draw."
            return

        self.problem.update_board(best_move + 1, 'O')
        self.last_ai_move = best_move + 1
        self.selected_index = best_move

        if self._finish_turn_if_game_over():
            return

        self.current_player = 'X'
        self.status_message = f"AI moved to {self.last_ai_move}. Your turn."

    def _finish_turn_if_game_over(self):
        self.winning_line = self.problem.find_winning_line(self.problem.board_state_back_end)
        self.winner = None if self.winning_line is None else self.problem.board_state_back_end[self.winning_line[0]]
        if self.winner:
            if self.winner == 'X':
                self.status_message = "YOU WIN! Four in a row."
            else:
                self.status_message = "AI WINS! Four in a row."
            return True

        if ' ' not in self.problem.board_state_back_end:
            self.draw = True
            self.status_message = "It's a draw."
            return True

        return False
