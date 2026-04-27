import asyncio

from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Grid, Vertical
from textual.message import Message
from textual.widgets import Footer, Header, Static

from board import BOARD_CELLS
from game_session import GameSession


class CellClicked(Message):
    def __init__(self, position):
        self.position = position
        super().__init__()


class InputModeSelected(Message):
    def __init__(self, mode):
        self.mode = mode
        super().__init__()


class ModeOptionWidget(Static):
    def __init__(self, mode, label):
        self.mode = mode
        super().__init__(label, id=f"mode-{mode}", classes="mode-option")

    def on_click(self, event):
        event.stop()
        self.post_message(InputModeSelected(self.mode))


class CellWidget(Static):
    def __init__(self, position):
        self.position = position
        super().__init__(str(position), id=f"cell-{position - 1}", classes="cell empty")

    def on_click(self, event):
        event.stop()
        self.post_message(CellClicked(self.position))


class BoardWidget(Grid):
    def compose(self) -> ComposeResult:
        for position in range(1, BOARD_CELLS + 1):
            yield CellWidget(position)

    def update_from_session(self, session):
        board = session.problem.board_state_back_end
        winning_cells = set(session.winning_line or ())
        for index, value in enumerate(board):
            cell = self.query_one(f"#cell-{index}", Static)
            position = index + 1
            classes = ["cell"]
            if value == 'X':
                classes.append("player")
                text = "X"
            elif value == 'O':
                classes.append("ai")
                text = "O"
            else:
                classes.append("empty")
                text = str(position)

            if position == session.last_player_move:
                classes.append("last-player")
            if position == session.last_ai_move:
                classes.append("last-ai")
            if index == session.selected_index and session.input_mode == "keyboard":
                classes.append("selected")
            if index in winning_cells:
                classes.append("winning-cell")

            cell.set_classes(" ".join(classes))
            cell.update(text)


class TicTacToeApp(App):
    TITLE = "Tic-Tac-Toe 8x8"
    SUB_TITLE = "4 in a row"
    BINDINGS = [
        Binding("up", "cursor_up", "Up", show=False),
        Binding("down", "cursor_down", "Down", show=False),
        Binding("left", "cursor_left", "Left", show=False),
        Binding("right", "cursor_right", "Right", show=False),
        Binding("enter", "play", "Move", show=False),
        Binding("space", "play", "Move", show=False),
        Binding("k", "select_keyboard", "Keyboard", show=False),
        Binding("m", "select_mouse", "Mouse", show=False),
        Binding("r", "restart", "Restart"),
        Binding("q", "quit", "Quit"),
    ]
    CSS = """
    Screen {
        background: #0f1419;
        color: #d7dde5;
    }

    #shell {
        width: 100%;
        height: 100%;
        align: center middle;
        padding: 0 1;
    }

    #game {
        width: 64;
        height: auto;
        align: center top;
    }

    #title {
        height: 1;
        content-align: center middle;
        text-style: bold;
        color: #f2f5f8;
    }

    #meta {
        height: 1;
        content-align: center middle;
        color: #8ea0b4;
    }

    #mode-picker {
        layout: grid;
        grid-size: 2 1;
        grid-columns: 1fr 1fr;
        height: 3;
        margin: 1 0;
    }

    .mode-option {
        height: 3;
        margin: 0 1;
        border: solid #253241;
        content-align: center middle;
        text-style: bold;
        color: #d7dde5;
    }

    .mode-option:hover {
        border: solid #7cc7ff;
        color: #f8fbff;
    }

    .hidden {
        display: none;
    }

    BoardWidget {
        layout: grid;
        grid-size: 8 8;
        grid-columns: 7;
        grid-rows: 3;
        width: 58;
        height: 24;
        align: center middle;
    }

    .cell {
        width: 7;
        height: 3;
        border: solid #253241;
        content-align: center middle;
        text-style: bold;
    }

    .empty {
        color: #6f8499;
        text-style: none;
    }

    .player {
        color: #ff6b7a;
    }

    .ai {
        color: #ffd166;
    }

    .selected {
        border: double #7cc7ff;
        color: #f8fbff;
    }

    .last-player {
        border: solid #ff8fa0;
    }

    .last-ai {
        border: solid #ffe08a;
    }

    .winning-cell {
        background: #203328;
        border: heavy #7df5a4;
        color: #ffffff;
        text-style: bold;
    }

    .player.winning-cell {
        background: #3a1f28;
        border: heavy #ff8fa0;
    }

    .ai.winning-cell {
        background: #332d18;
        border: heavy #ffe08a;
    }

    #status {
        height: 2;
        margin-top: 1;
        content-align: center middle;
    }

    #help {
        height: 1;
        content-align: center middle;
        color: #7b8da0;
    }
    """

    def __init__(self):
        super().__init__()
        self.session = GameSession()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(id="shell"):
            with Vertical(id="game"):
                yield Static("Tic-Tac-Toe 8x8", id="title")
                yield Static(id="meta")
                with Grid(id="mode-picker"):
                    yield ModeOptionWidget("keyboard", "Keyboard (K)")
                    yield ModeOptionWidget("mouse", "Mouse (M)")
                yield BoardWidget(id="board")
                yield Static(id="status")
                yield Static(id="help")
        yield Footer()

    def on_mount(self):
        self.refresh_view()

    def action_cursor_up(self):
        if not self.can_use_keyboard():
            return
        self.session.move_selection(-1, 0)
        self.refresh_view()

    def action_cursor_down(self):
        if not self.can_use_keyboard():
            return
        self.session.move_selection(1, 0)
        self.refresh_view()

    def action_cursor_left(self):
        if not self.can_use_keyboard():
            return
        self.session.move_selection(0, -1)
        self.refresh_view()

    def action_cursor_right(self):
        if not self.can_use_keyboard():
            return
        self.session.move_selection(0, 1)
        self.refresh_view()

    async def action_play(self):
        if not self.can_use_keyboard():
            return
        await self.play_position(self.session.selected_position)

    def action_select_keyboard(self):
        self.session.choose_input_mode("keyboard")
        self.refresh_view()

    def action_select_mouse(self):
        self.session.choose_input_mode("mouse")
        self.refresh_view()

    def on_input_mode_selected(self, message):
        self.session.choose_input_mode(message.mode)
        self.refresh_view()

    async def on_cell_clicked(self, message):
        if not self.can_use_mouse():
            return
        await self.play_position(message.position)

    async def play_position(self, position):
        if self.session.ai_thinking:
            return

        self.session.select_position(position)
        moved = self.session.play_player_position(position)
        self.refresh_view()
        if not moved or self.session.game_over:
            return

        self.session.ai_thinking = True
        self.refresh_view()
        try:
            await asyncio.to_thread(self.session.play_ai_turn)
        finally:
            self.session.ai_thinking = False
        self.refresh_view()

    def action_restart(self):
        if self.session.ai_thinking:
            self.session.status_message = "AI is thinking. Restart after this turn."
            self.refresh_view()
            return
        self.session.restart()
        self.refresh_view()

    def can_use_keyboard(self):
        if self.session.input_mode == "keyboard":
            return True
        if self.session.input_mode == "mouse":
            self.session.status_message = "Mouse mode is active. Keyboard input is disabled."
        else:
            self.session.status_message = "Choose Keyboard or Mouse before playing."
        self.refresh_view()
        return False

    def can_use_mouse(self):
        if self.session.input_mode == "mouse":
            return True
        if self.session.input_mode == "keyboard":
            self.session.status_message = "Keyboard mode is active. Mouse input is disabled."
        else:
            self.session.status_message = "Choose Keyboard or Mouse before playing."
        self.refresh_view()
        return False

    def refresh_view(self):
        self.query_one("#mode-picker", Grid).set_class(self.session.input_mode is not None, "hidden")
        self.query_one("#board", BoardWidget).update_from_session(self.session)
        self.query_one("#meta", Static).update(self.render_meta())
        self.query_one("#status", Static).update(self.render_status())
        self.query_one("#help", Static).update(self.render_help())

    def render_meta(self):
        mode = self.session.input_mode.title() if self.session.input_mode else "Choose"
        turn = "You" if self.session.current_player == 'X' else "AI"
        if self.session.game_over:
            turn = "Game over"
        return f"Mode: {mode}   Turn: {turn}   Moves: {self.session.move_count}/64   Selected: {self.session.selected_position}"

    def render_help(self):
        if self.session.input_mode == "keyboard":
            return "Arrow keys: select   Enter: move   R: restart   Q: quit"
        if self.session.input_mode == "mouse":
            return "Click a cell: move   R: restart   Q: quit"
        return "Choose input first: K for keyboard, M for mouse"

    def render_status(self):
        line = Text(self.session.status_message, style="bold")
        if self.session.last_player_move:
            line.append(f"   Your last: {self.session.last_player_move}", style="red")
        if self.session.last_ai_move:
            line.append(f"   AI: {self.session.last_ai_move}", style="yellow")
        return line
