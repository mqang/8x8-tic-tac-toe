# Textual UI Refactor Design

## Goal

Move the terminal interface from Rich prompt rendering to a Textual full-screen app while preserving the existing 8x8 tic-tac-toe rules, board state, win detection, and AI move selection.

## Scope

- Keep `Problem` and `Search_Strategy` as the source of game rules and AI behavior.
- Add a small game session/controller layer for turn state, selected cell, last moves, and result messages.
- Add a Textual app that renders an 8x8 board, status area, and keyboard controls.
- Support arrow-key navigation and `Enter`/`Space` to place the player's move.
- Keep the familiar `1-64` cell labels visible on empty cells.
- Highlight the selected cell, the last player move, and the last AI move.
- Show a terminal result state for player win, AI win, or draw.

## Non-Goals

- No changes to AI scoring, minimax depth, candidate ordering, or win logic.
- No mouse support, settings menu, difficulty selection, undo, animation, or theme switcher in this first pass.
- No restart flow unless it is trivial and isolated.

## Verification

- Existing AI strategy tests must continue to pass.
- New session tests must prove player moves, invalid moves, AI response, and game-over blocking remain deterministic at the UI boundary.
- The Textual app must import and initialize without starting the game loop during tests.
