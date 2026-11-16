"""Shared test setup: pygame pieces that need no window."""

import pygame
import pytest


@pytest.fixture(scope="session", autouse=True)
def fonts():
    """Start pygame's font system, which Button and Scoreboard need."""
    pygame.font.init()
    yield
    pygame.font.quit()


@pytest.fixture
def ship_image():
    """A blank 60x48 picture standing in for the ship image."""
    return pygame.Surface((60, 48))


@pytest.fixture
def alien_image():
    """A blank 60x40 picture standing in for the alien image."""
    return pygame.Surface((60, 40))


@pytest.fixture
def bounds():
    """The rectangle of a 1200x800 screen."""
    return pygame.Rect(0, 0, 1200, 800)
