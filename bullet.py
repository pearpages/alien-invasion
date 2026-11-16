import pygame
from pygame.sprite import Sprite

from config import Color


class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(
        self, midtop: tuple[int, int], size: tuple[int, int], color: Color
    ):
        """Create a bullet whose top middle point is at midtop."""
        super().__init__()
        self.color = color
        self.rect = pygame.Rect((0, 0), size)
        self.rect.midtop = midtop

        # Store the bullet's position as a float.
        self.y = float(self.rect.y)

    def update(self, speed: float):
        """Move the bullet up the screen by speed pixels."""
        # Update the exact position of the bullet.
        self.y -= speed
        # Update the rect position.
        self.rect.y = self.y

    def draw(self, screen: pygame.Surface):
        """Draw the bullet to the screen."""
        pygame.draw.rect(screen, self.color, self.rect)
