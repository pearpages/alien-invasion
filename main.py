"""Start Alien Invasion: uv run main.py"""

from pathlib import Path

import pygame

from assets import Assets
from config import Config
from game import Game
from high_score import HIGH_SCORE_FILE, load_high_score, save_high_score


def main(high_score_path: Path = HIGH_SCORE_FILE):
    """Build everything the game needs, connect it, and run the game.

    This is the only place that creates the window and touches files;
    every class receives what it needs from here. The high score is
    loaded before the game and saved when the player quits.
    """
    pygame.init()
    config = Config()
    screen = pygame.display.set_mode(
        (config.screen_width, config.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")
    assets = Assets.load()
    saved_high_score = load_high_score(high_score_path)

    game = Game(config, assets, high_score=saved_high_score)
    game.run(screen)

    if game.stats.high_score > saved_high_score:
        save_high_score(high_score_path, game.stats.high_score)
    pygame.quit()


if __name__ == "__main__":
    main()
