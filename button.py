import pygame
import pygame.font


class Button:
    """A class to build buttons for the game."""

    def __init__(self, msg: str, center: tuple[int, int]):
        """Make a button showing msg, centered on center."""
        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = center

        # The button message needs to be prepped only once.
        self._prep_msg(msg)

    def _prep_msg(self, msg: str):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(
            msg, True, self.text_color, self.button_color
        )
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw(self, screen: pygame.Surface):
        """Draw blank button and then draw message."""
        screen.fill(self.button_color, self.rect)
        screen.blit(self.msg_image, self.msg_image_rect)
