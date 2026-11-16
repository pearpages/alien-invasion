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

## Checks

```bash
uv run pytest              # tests in tests/
uv run ruff check .        # lint: PEP 8, import order, likely bugs
uv run ruff format .       # format the code
```

ruff and pytest are dev dependencies, configured in `pyproject.toml`.

## Files

| File | Role |
|---|---|
| `alien_invasion.py` | Main game class and loop |
| `config.py` | `Config`: frozen dataclass of settings that never change |
| `difficulty.py` | `Difficulty`: speeds and alien points for the current level; each level-up makes a new one |
| `ship.py`, `alien.py`, `bullet.py` | The sprites |
| `game_stats.py` | `GameStats`: dataclass for score, level, ships left, high score |
| `scoreboard.py` | Draws score, high score, level, remaining ships |
| `button.py` | The Play button |
| `pyproject.toml` | Project info and dependencies (like `package.json`) |
| `.python-version` | Python version uv uses for this project |
| `images/` | `ship.bmp` and `alien.bmp` (simple stand-ins; swap in the book's images if you like) |
