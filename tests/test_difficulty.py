import pytest

from config import Config
from difficulty import Difficulty


def test_starting_difficulty_comes_from_config():
    config = Config(ship_speed=2.0, alien_points=10)

    difficulty = Difficulty.starting(config)

    assert difficulty.ship_speed == 2.0
    assert difficulty.alien_points == 10


def test_next_level_scales_speeds_and_points():
    config = Config()
    level_1 = Difficulty.starting(config)

    level_2 = level_1.next_level(config)

    assert level_2.ship_speed == pytest.approx(1.5 * 1.1)
    assert level_2.bullet_speed == pytest.approx(2.5 * 1.1)
    assert level_2.alien_speed == pytest.approx(1.0 * 1.1)
    assert level_2.alien_points == 75


def test_next_level_leaves_the_current_difficulty_unchanged():
    config = Config()
    level_1 = Difficulty.starting(config)

    level_1.next_level(config)

    assert level_1 == Difficulty.starting(config)
