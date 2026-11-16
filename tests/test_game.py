"""The whole game, built on an off-screen surface instead of a window."""

import pygame
import pytest

from assets import Assets
from config import Config
from game import Game


@pytest.fixture
def game():
    config = Config()
    screen = pygame.Surface((config.screen_width, config.screen_height))
    return Game(config, screen, Assets.load())


def test_new_game_waits_for_play_with_a_full_fleet(game):
    assert not game.game_active
    assert len(game.aliens) == 72
    assert game.ship.rect.midbottom == (600, 800)


def test_clearing_the_fleet_goes_up_a_level(game):
    game.aliens.empty()

    game._check_bullet_alien_collisions()

    assert game.stats.level == 2
    assert len(game.aliens) == 72
    assert game.difficulty.alien_points == 75


def test_a_frame_draws_without_a_window(game):
    game.screen.fill((0, 0, 0))

    game.aliens.draw(game.screen)
    game.ship.draw(game.screen)
    game.sb.draw(game.screen)

    assert game.screen.get_at(game.ship.rect.center) != (0, 0, 0)
