import enum
import os.path
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS = os.path.join(BASE_DIR, "assets")


class Settings:
    screen_width = 800
    screen_height = 700

    bg_color = (0, 0, 0)
    color_light = (255, 255, 255)
    show_fps = False

    sound_level = 15

    def __init__(self):
        """Settings for space rangers game"""
        raise Exception("Do not instantiate")


class ShipSettings:
    speed_factor = 3


class BackgroundStarSettings:
    number_of_stars = 200
    speed_factor = 20
    speed = 10
    small = (1, 1)
    medium = (1, 2)
    large = (2, 3)
    color = (255, 255, 255)


class PlayerDirection(enum.Enum):
    left = enum.auto()
    right = enum.auto()
    up = enum.auto()
    down = enum.auto()


class AlienSettings:
    speed = 2
    drop_rate = 10
    direction = 1  # 1 for right -1 for left


class GameSettings:
    max_lives = 3
    max_bullets = 5
