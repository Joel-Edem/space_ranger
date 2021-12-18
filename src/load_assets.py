import os
from dataclasses import dataclass
from typing import Optional

import pygame
from pygame.surface import Surface

from src.settings import ASSETS
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@dataclass
class Location:
    """rectangle of sprite position"""
    x: int  # x
    y: int
    width: int
    height: int

    def area(self):
        return self.x, self.y, self.width, self.height


class SpriteSheet:

    def __init__(self, file_name: str):
        """
        load and stores sprite sheets
        """
        self.sprite_sheet: Optional[Surface] = None
        self.file_name = file_name
        self.loaded = False

    def load(self):
        """load sprite sheets"""
        file = os.path.join(ASSETS, self.file_name)
        try:
            self.sprite_sheet = pygame.image.load(file).convert_alpha()
            self.loaded = True
        except pygame.error as e:
            logger.error(f"failed to load asset {file}")
            logger.error(e)

    def get_image(self, at: Location) -> Surface:
        """return image at given location or none"""
        rect = pygame.Rect(at.area())
        image = pygame.Surface(rect.size).convert_alpha()
        image.blit(self.sprite_sheet, (0, 0), rect)
        return image
