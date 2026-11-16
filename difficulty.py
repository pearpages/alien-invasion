from dataclasses import dataclass, replace
from typing import Self

from config import Config


@dataclass(frozen=True)
class Difficulty:
    """Speeds and alien points for the current level."""

    ship_speed: float
    bullet_speed: float
    alien_speed: float
    alien_points: int

    @classmethod
    def starting(cls, config: Config) -> Self:
        """Return the difficulty for level 1."""
        return cls(
            ship_speed=config.ship_speed,
            bullet_speed=config.bullet_speed,
            alien_speed=config.alien_speed,
            alien_points=config.alien_points,
        )

    def next_level(self, config: Config) -> Self:
        """Return a new, harder difficulty; this one is left unchanged."""
        return replace(
            self,
            ship_speed=self.ship_speed * config.speedup_scale,
            bullet_speed=self.bullet_speed * config.speedup_scale,
            alien_speed=self.alien_speed * config.speedup_scale,
            alien_points=int(self.alien_points * config.score_scale),
        )
