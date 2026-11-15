# Alien Invasion

The Alien Invasion game from *Python Crash Course*, 3rd edition (chapters 12–14), in its finished form.

## Setup

This project uses [uv](https://docs.astral.sh/uv/) to manage Python, the virtual environment and dependencies.

```bash
brew install uv
uv sync
```

`uv sync` reads `pyproject.toml`, downloads the Python version in `.python-version` if needed, creates `.venv/` and installs pygame. It also writes `uv.lock`, which pins exact versions; commit that file.

## Run

Run from this folder, because the game loads `images/` with relative paths:

```bash
uv run alien_invasion.py
```

`uv run` uses `.venv` automatically, so there's no need to activate it.

Controls: click **Play**, use ← → to move, Space to fire, Q to quit.

## Files

| File | Role |
|---|---|
| `alien_invasion.py` | Main game class and loop |
| `settings.py` | All settings, including the speed-up per level |
| `ship.py`, `alien.py`, `bullet.py` | The sprites |
| `game_stats.py` | Score, level, ships left |
| `scoreboard.py` | Draws score, high score, level, remaining ships |
| `button.py` | The Play button |
| `pyproject.toml` | Project info and dependencies (like `package.json`) |
| `.python-version` | Python version uv uses for this project |
| `images/` | `ship.bmp` and `alien.bmp` (simple stand-ins; swap in the book's images if you like) |
