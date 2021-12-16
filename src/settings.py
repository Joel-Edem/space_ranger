import enum


class Settings:
    screen_width = 800
    screen_height = 900

    bg_color = (0, 0, 0)
    color_light = (255, 255, 255)

    def __init__(self):
        """Settings for space rangers game"""
        pass
        raise Exception("Do not instantiate")


class BackgroundStarSettings:
    number_of_stars = 500
    speed_factor = 20
    speed = 10
    small = (1, 1)
    medium = (1, 2)
    large = (2, 3)
    color = (255, 255, 255)


class StarDirection(enum.Enum):

    left = enum.auto()
    right = enum.auto()
    up = enum.auto()
    down = enum.auto()