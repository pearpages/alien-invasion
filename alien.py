import pygame
from pygame.sprite import Sprite

from rules import at_screen_edge


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, image: pygame.Surface, x: int, y: int):
        """Place an alien with its top-left corner at (x, y)."""
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

    def check_edges(self, screen_width: int) -> bool:
        """Return True if alien is at edge of screen."""
        return at_screen_edge(self.rect.left, self.rect.right, screen_width)

    def update(self, dx: float):
        """Move the alien dx pixels; negative dx moves it left."""
        self.x += dx
        self.rect.x = self.x
