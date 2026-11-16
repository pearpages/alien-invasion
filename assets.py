from dataclasses import dataclass
from pathlib import Path
from typing import Self

import pygame

# The images folder next to this file, wherever the game is started from.
IMAGES = Path(__file__).parent / "images"


@dataclass(frozen=True)
class Assets:
    """Images the game needs, each loaded from disk once."""

    ship: pygame.Surface
    alien: pygame.Surface

    @classmethod
    def load(cls, folder: Path = IMAGES) -> Self:
        """Load every image from folder."""
        return cls(
            ship=pygame.image.load(folder / "ship.bmp"),
            alien=pygame.image.load(folder / "alien.bmp"),
        )
