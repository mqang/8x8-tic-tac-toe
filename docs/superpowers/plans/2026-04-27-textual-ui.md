# Textual UI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the prompt-loop UI with a Textual full-screen terminal app while preserving game logic.

**Architecture:** Keep `Problem` and `Search_Strategy` intact for rules and AI. Add a lightweight `GameSession` controller that Textual can call, then render that session through `TicTacToeApp` and `BoardWidget`.

**Tech Stack:** Python 3.12, Rich, Textual, unittest.

---

### Task 1: Session Boundary

**Files:**
- Modify: `main.py`
- Test: `tests/test_game_session.py`

- [ ] Add tests for `GameSession` initial state, player move, invalid move, and game-over blocking.
- [ ] Implement `GameSession` with selected index, current player, last player move, last AI move, status message, and winner/draw state.
- [ ] Run `uv run python -m unittest tests.test_game_session`.

### Task 2: Textual App

**Files:**
- Modify: `main.py`
- Modify: `pyproject.toml`

- [ ] Add `textual` dependency.
- [ ] Add `BoardWidget` and `TicTacToeApp`.
- [ ] Wire keyboard actions for arrow movement, `Enter`, `Space`, `q`, and optional `r` restart.
- [ ] Keep empty cells labeled `1-64`, highlight selection and last moves.

### Task 3: Verification

**Files:**
- Modify: `README.md`

- [ ] Update README run instructions if needed.
- [ ] Run `uv run python -m unittest discover -s tests`.
- [ ] Run a non-interactive import check for `TicTacToeApp`.
