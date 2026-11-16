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

```bash
uv run main.py
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

## Design

Every class receives what it needs through its constructor instead of reaching into the whole game. `main()` in `main.py` is the one place that creates the window, loads the images and connects everything. No class keeps the screen: anything that draws gets it as an argument, `draw(screen)`. So every piece, including the whole game on an off-screen surface, can be tested without a window.

## Files

| File | Role |
|---|---|
| `main.py` | Entry point: `main()` starts pygame, opens the window, loads assets and connects everything |
| `game.py` | `Game`: the main loop, input, collisions and levels |
| `assets.py` | `Assets`: loads each image once, from `images/` next to the code |
| `rules.py` | The game's rules as plain functions with no pygame: fleet layout, edges, scoring, firing, ship movement |
| `config.py` | `Config`: frozen dataclass of settings that never change |
| `difficulty.py` | `Difficulty`: speeds and alien points for the current level; each level-up makes a new one |
| `ship.py`, `alien.py`, `bullet.py` | The sprites |
| `game_stats.py` | `GameStats`: dataclass for score, level, ships left, high score |
| `scoreboard.py` | Draws score, high score, level, remaining ships |
| `button.py` | The Play button |
| `pyproject.toml` | Project info and dependencies (like `package.json`) |
| `.python-version` | Python version uv uses for this project |
| `images/` | `ship.bmp` and `alien.bmp` (simple stand-ins; swap in the book's images if you like) |
