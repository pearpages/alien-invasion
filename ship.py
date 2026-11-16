import pygame
from pygame.sprite import Sprite

from rules import ship_step


class Ship(Sprite):
    """A class to manage the ship."""

    def __init__(self, image: pygame.Surface, bounds: pygame.Rect):
        """Place the ship at the bottom center of bounds.

        image is the ship's picture; bounds is the area it may move in,
        normally the whole screen.
        """
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.bounds = bounds

        # Start each new ship at the bottom center of the screen.
        self.center_ship()

        # Movement flags; start with a ship that's not moving.
        self.moving_right = False
        self.moving_left = False

    def update(self, speed: float):
        """Move the ship speed pixels, following the movement flags."""
        # Update the ship's x value, not the rect.
        self.x += ship_step(
            left=self.rect.left,
            right=self.rect.right,
            screen_width=self.bounds.width,
            speed=speed,
            moving_left=self.moving_left,
            moving_right=self.moving_right,
        )

        # Update rect object from self.x.
        self.rect.x = self.x

    def draw(self, screen: pygame.Surface):
        """Draw the ship at its current location."""
        screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship at the bottom of its bounds."""
        self.rect.midbottom = self.bounds.midbottom
        # Store a float for the ship's exact horizontal position.
        self.x = float(self.rect.x)
