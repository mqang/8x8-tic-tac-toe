from ai_strategy import Search_Strategy
from board import BOARD_CELLS, BOARD_SIZE, CENTER_MOVES, WIN_LENGTH, Problem
from game_session import GameSession
from textual_ui import (
    BoardWidget,
    CellClicked,
    CellWidget,
    InputModeSelected,
    ModeOptionWidget,
    TicTacToeApp,
)

__all__ = [
    "BOARD_CELLS",
    "BOARD_SIZE",
    "CENTER_MOVES",
    "WIN_LENGTH",
    "BoardWidget",
    "CellClicked",
    "CellWidget",
    "GameSession",
    "InputModeSelected",
    "ModeOptionWidget",
    "Problem",
    "Search_Strategy",
    "TicTacToeApp",
]


if __name__ == "__main__":
    TicTacToeApp().run()
