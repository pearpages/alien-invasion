from dataclasses import dataclass

type Color = tuple[int, int, int]


@dataclass(frozen=True)
class Config:
    """Settings that never change while the game runs."""

    # Screen
    screen_width: int = 1200
    screen_height: int = 800
    bg_color: Color = (230, 230, 230)

    # Ship
    ship_limit: int = 3
    ship_speed: float = 1.5

    # Bullets
    bullet_width: int = 3
    bullet_height: int = 15
    bullet_color: Color = (60, 60, 60)
    bullets_allowed: int = 3
    bullet_speed: float = 2.5

    # Aliens
    alien_speed: float = 1.0
    alien_points: int = 50
    fleet_drop_speed: int = 10

    # How much faster, and how much more each alien is worth, per level
    speedup_scale: float = 1.1
    score_scale: float = 1.5
