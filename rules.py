"""The game's rules as plain functions: numbers in, answers out.

Nothing here imports pygame, so every rule can be tested on its own.
"""

from collections.abc import Iterable


def fleet_positions(
    screen_width: int, screen_height: int, alien_width: int, alien_height: int
) -> list[tuple[int, int]]:
    """Return the top-left (x, y) of every alien in a new fleet.

    Aliens are one alien width apart and one alien height apart. The
    fleet leaves a margin of one alien on the left, and keeps clear of
    the right edge and of the bottom of the screen, where the ship is.
    """
    return [
        (x, y)
        for y in range(
            alien_height, screen_height - 3 * alien_height, 2 * alien_height
        )
        for x in range(
            alien_width, screen_width - 2 * alien_width, 2 * alien_width
        )
    ]


def at_screen_edge(left: int, right: int, screen_width: int) -> bool:
    """Return True if something spanning left..right touches a side."""
    return right >= screen_width or left <= 0


def reached_bottom(bottoms: Iterable[int], screen_height: int) -> bool:
    """Return True if any of the bottom edges has reached the screen's."""
    return any(bottom >= screen_height for bottom in bottoms)


def points_for_hits(hits_per_bullet: Iterable[int], alien_points: int) -> int:
    """Return the points for a volley, given how many aliens each bullet hit.

    A bullet can hit more than one alien at once; each alien counts.
    """
    return alien_points * sum(hits_per_bullet)


def can_fire(bullets_on_screen: int, bullets_allowed: int) -> bool:
    """Return True if the player may fire another bullet."""
    return bullets_on_screen < bullets_allowed


def ship_step(
    *,
    left: int,
    right: int,
    screen_width: int,
    speed: float,
    moving_left: bool,
    moving_right: bool,
) -> float:
    """Return how far the ship moves this frame; negative is left.

    The ship stops at the screen's sides. Holding both keys cancels out.
    """
    step = 0.0
    if moving_right and right < screen_width:
        step += speed
    if moving_left and left > 0:
        step -= speed
    return step


def reserve_ships(ships_left: int) -> int:
    """Return how many ships wait in reserve, not counting the one in play."""
    return max(ships_left - 1, 0)


def format_score(score: int) -> str:
    """Round a score to the nearest ten and add thousands separators."""
    return f"{round(score, -1):,}"
