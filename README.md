# Alien Invasion

The Alien Invasion game from *Python Crash Course*, 3rd edition (chapters 12–14), in its finished form.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pygame
```

## Run

Run from this folder, because the game loads `images/` with relative paths:

```bash
python alien_invasion.py
```

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
| `images/` | `ship.bmp` and `alien.bmp` (simple stand-ins; swap in the book's images if you like) |
