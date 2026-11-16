import pygame
import pygame.font
from pygame.sprite import Group

from config import Color
from game_stats import GameStats
from rules import format_score, reserve_ships
from ship import Ship


def score_label(score: int) -> str:
    """Return the text shown for the current score."""
    return f"Score: {format_score(score)}"


def high_score_label(high_score: int) -> str:
    """Return the text shown for the high score."""
    return f"High score: {format_score(high_score)}"


def level_label(level: int) -> str:
    """Return the text shown for the current level."""
    return f"Level: {level}"


class Scoreboard:
    """A class to report scoring information."""

    def __init__(
        self,
        stats: GameStats,
        bg_color: Color,
        ship_image: pygame.Surface,
        bounds: pygame.Rect,
    ):
        """Show stats on a bg_color background, laid out within bounds.

        ship_image is used for the row of ships left.
        """
        self.stats = stats
        self.bg_color = bg_color
        self.ship_image = ship_image
        self.bounds = bounds

        # Font settings for scoring information.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score images.
        self.prep_images()

    def prep_images(self):
        """Prepare the score, high score, level and ships images."""
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image."""
        self.score_image = self.font.render(
            score_label(self.stats.score), True, self.text_color, self.bg_color
        )

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.bounds.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        self.high_score_image = self.font.render(
            high_score_label(self.stats.high_score),
            True,
            self.text_color,
            self.bg_color,
        )

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.bounds.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Turn the level into a rendered image."""
        self.level_image = self.font.render(
            level_label(self.stats.level), True, self.text_color, self.bg_color
        )

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Show the ships waiting in reserve; the one in play is not shown."""
        self.ships = Group()
        for ship_number in range(reserve_ships(self.stats.ships_left)):
            ship = Ship(self.ship_image, self.bounds)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    @property
    def bottom(self) -> int:
        """Return the y just below everything the scoreboard draws."""
        rects = [
            self.score_rect,
            self.high_score_rect,
            self.level_rect,
            *(ship.rect for ship in self.ships),
        ]
        return max(rect.bottom for rect in rects)

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def draw(self, screen: pygame.Surface):
        """Draw scores, level, and ships to the screen."""
        screen.blit(self.score_image, self.score_rect)
        screen.blit(self.high_score_image, self.high_score_rect)
        screen.blit(self.level_image, self.level_rect)
        self.ships.draw(screen)
