"""The whole game, driven only through its public methods.

Events are made up with pygame.event.Event, so no keyboard, mouse or
window is needed.
"""

import pygame
import pytest

from assets import Assets
from config import Config
from game import Game


@pytest.fixture
def game():
    return Game(Config(), Assets.load())


@pytest.fixture
def screen():
    return pygame.Surface((1200, 800))


def press(game, key):
    game.handle(pygame.event.Event(pygame.KEYDOWN, key=key))


def release(game, key):
    game.handle(pygame.event.Event(pygame.KEYUP, key=key))


def click(game, pos):
    game.handle(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=pos, button=1))


def alien_positions(game):
    return sorted(alien.rect.topleft for alien in game.aliens)


# --- starting ----------------------------------------------------------------


def test_new_game_waits_for_play_with_a_full_fleet(game):
    assert not game.game_active
    assert game.running
    assert len(game.aliens) == 72
    assert game.ship.rect.midbottom == (600, 800)


def test_clicking_play_starts_the_game(game):
    click(game, game.play_button.rect.center)

    assert game.game_active


def test_clicking_elsewhere_does_not_start_the_game(game):
    click(game, (10, 10))

    assert not game.game_active


def test_nothing_moves_before_the_game_starts(game):
    before = alien_positions(game)

    for _ in range(10):
        game.step()

    assert alien_positions(game) == before


# --- the ship and its bullets ------------------------------------------------


def test_holding_right_moves_the_ship_and_releasing_stops_it(game):
    game.start()
    x = game.ship.rect.x

    press(game, pygame.K_RIGHT)
    for _ in range(10):
        game.step()
    moved_to = game.ship.rect.x
    release(game, pygame.K_RIGHT)
    game.step()

    assert moved_to == x + 15  # 10 steps at speed 1.5
    assert game.ship.rect.x == moved_to


def test_space_fires_a_bullet_that_flies_up(game):
    game.start()

    press(game, pygame.K_SPACE)
    game.step()
    y = game.bullets.sprites()[0].rect.y
    for _ in range(10):
        game.step()

    assert len(game.bullets) == 1
    assert game.bullets.sprites()[0].rect.y < y


def test_only_three_bullets_at_a_time(game):
    game.start()

    for _ in range(5):
        press(game, pygame.K_SPACE)

    assert len(game.bullets) == 3


def test_shooting_an_alien_scores_its_points(game):
    game.start()
    press(game, pygame.K_SPACE)

    for _ in range(300):
        game.step()
        if game.stats.score:
            break

    assert game.stats.score == 50
    assert len(game.aliens) == 71


# --- the fleet ---------------------------------------------------------------


def test_the_fleet_moves_right_then_drops_and_turns_at_the_edge(game):
    game.start()
    top = min(alien.rect.top for alien in game.aliens)

    for _ in range(200):
        game.step()

    assert game.fleet_direction == -1
    assert min(alien.rect.top for alien in game.aliens) == top + 10


def test_clearing_the_fleet_goes_up_a_level(game):
    game.start()
    game.aliens.empty()

    game.step()

    assert game.stats.level == 2
    assert len(game.aliens) == 72
    assert game.difficulty.alien_points == 75


# --- losing ships ------------------------------------------------------------


@pytest.fixture
def no_pause(monkeypatch):
    """Skip the real half-second pause after a hit, to keep tests fast."""
    monkeypatch.setattr("game.sleep", lambda seconds: None)


def crash_an_alien_into_the_ship(game):
    """Put an alien on top of the ship, then play one frame."""
    alien = game.aliens.sprites()[0]
    alien.rect.center = game.ship.rect.center
    alien.x = float(alien.rect.x)
    game.step()


def test_a_crash_costs_one_ship_and_brings_a_new_fleet(game, no_pause):
    game.start()

    crash_an_alien_into_the_ship(game)

    assert game.stats.ships_left == 2
    assert len(game.aliens) == 72
    assert game.game_active


def test_the_game_ends_after_three_crashes(game, no_pause):
    game.start()

    for _ in range(3):
        crash_an_alien_into_the_ship(game)

    assert not game.game_active


def test_no_reserve_icons_while_flying_the_last_ship(game, no_pause):
    game.start()

    for _ in range(2):
        crash_an_alien_into_the_ship(game)

    assert game.game_active
    assert game.stats.ships_left == 1
    assert len(game.sb.ships) == 0


# --- quitting ----------------------------------------------------------------


def test_q_stops_the_game_loop(game):
    press(game, pygame.K_q)

    assert not game.running


def test_closing_the_window_stops_the_game_loop(game):
    game.handle(pygame.event.Event(pygame.QUIT))

    assert not game.running


# --- drawing -----------------------------------------------------------------


def test_draw_paints_the_ship_on_any_surface(game, screen):
    game.draw(screen)

    assert screen.get_at(game.ship.rect.center) != (230, 230, 230)


def test_draw_shows_play_only_while_the_game_is_waiting(game, screen):
    button_green = (0, 135, 0, 255)
    corner = game.play_button.rect.topleft

    game.draw(screen)
    shown_before_start = screen.get_at(corner)
    game.start()
    game.draw(screen)

    assert shown_before_start == button_green
    assert screen.get_at(corner) != button_green


def test_draw_does_not_change_the_game(game, screen):
    game.start()
    before = alien_positions(game)

    game.draw(screen)

    assert alien_positions(game) == before
