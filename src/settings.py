import enum
import json
import os.path
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS = os.path.join(BASE_DIR, "assets")



class Settings:
    is_initialized = False
    settings_file = "settings.json"
    screen_width = 800
    screen_height = 700

    bg_color = (0, 0, 0)
    color_light = (255, 255, 255)
    show_fps = False

    sound_level = 50

    def __init__(self):
        """Settings for space rangers game"""
        # self.load()
        # Settings.is_initialized = True
        # if Settings.is_initialized:
        raise Exception("Do not re-instantiate")

    @classmethod
    def save(cls):
        fp = os.path.join(BASE_DIR, cls.settings_file)
        with open(fp, "w") as file:
            try:
                json.dump(cls.sound_level, file)

            except FileNotFoundError as e:
                print(f"Could not find file {e.filename}"
                      )

    @classmethod
    def load(cls):
        fp = os.path.join(BASE_DIR, cls.settings_file)
        try:
            with open(fp, "rb") as file:
                cls.sound_level = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Could not find file {cls.settings_file}")


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
