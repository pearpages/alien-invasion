"""Start Alien Invasion: uv run main.py"""

import pygame

from assets import Assets
from config import Config
from game import Game


def main():
    """Build everything the game needs, connect it, and run the game.

    This is the only place that creates the window and loads files; every
    class receives what it needs from here.
    """
    pygame.init()
    config = Config()
    screen = pygame.display.set_mode(
        (config.screen_width, config.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")
    assets = Assets.load()

    Game(config, assets).run(screen)
    pygame.quit()


if __name__ == "__main__":
    main()
