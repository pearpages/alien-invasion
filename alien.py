import pygame
from pygame.sprite import Sprite

from rules import at_screen_edge


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_width = self.screen.get_rect().width
        return at_screen_edge(self.rect.left, self.rect.right, screen_width)

    def update(self, dx: float):
        """Move the alien dx pixels; negative dx moves it left."""
        self.x += dx
        self.rect.x = self.x
