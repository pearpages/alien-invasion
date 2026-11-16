from dataclasses import dataclass


@dataclass
class GameStats:
    """Track statistics for Alien Invasion."""

    ships_left: int
    score: int = 0
    level: int = 1
    # High score should never be reset.
    high_score: int = 0

    def reset(self, ship_limit: int) -> None:
        """Start a new game, keeping the high score."""
        self.ships_left = ship_limit
        self.score = 0
        self.level = 1
