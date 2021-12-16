import random

import pygame
from pygame.sprite import Sprite, Group

from src.settings import BackgroundStarSettings as BG_Settings, Settings, StarDirection


class BackgroundStars(Sprite):
    stars = Group()
    star_direction: StarDirection = None

    @staticmethod
    def get_star_size() -> (int, int):
        """
        :return a random size for star
        """
        return random.choice(
            (BG_Settings.small, BG_Settings.large, BG_Settings.medium)
        )

    @staticmethod
    def get_star_speed() -> int:
        """
        :return a random size for star
        """
        # return random.choice(
        #     (BG_Settings.medium_speed,
        #      BG_Settings.slow_speed,
        #      )
        # )
        return random.randint(0, BG_Settings.speed)

    @staticmethod
    def get_starting_location_x():
        """
        return location for x coord
        """
        return random.randrange(0, Settings.screen_width)

    @staticmethod
    def get_starting_location_y() -> int:
        """
        return location for y coord
        """
        return random.randrange(0, Settings.screen_height)

    def __init__(self):
        super().__init__(self.stars)  # add all stars to background
        self.size: (int, int) = self.get_star_size()
        self.x = self.get_starting_location_x()  # x position
        self.y = self.get_starting_location_y()  # y position
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[-1])
        self.speed = (self.get_star_speed() * random.choice([1, -1])) / BG_Settings.speed_factor
        self.color = BG_Settings.color

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self):
        """
        Update stars position based on generated settings
        :return:
        """
        x_out_of_bounds = Settings.screen_width < self.x or self.x < 0
        y_out_of_bounds = Settings.screen_height < self.y or self.y < 0

        if x_out_of_bounds or y_out_of_bounds:
            self.x = 0 if self.star_direction == StarDirection.left else \
                Settings.screen_width if self.star_direction == StarDirection.right else \
                    self.get_starting_location_x()
            self.y = self.get_starting_location_y()
        else:
            self.x += self.speed
            self.y += self.speed
        if self.star_direction == StarDirection.right:
            self.x -= 2
        elif self.star_direction == StarDirection.left:
            self.x += 2

        self.rect.x = self.x
        self.rect.y = self.y

    @classmethod
    def create_stars(cls):
        for i in range(BG_Settings.number_of_stars):
            cls()

    @classmethod
    def render_stars(cls, screen):
        star: BackgroundStars
        for star in cls.stars:
            star.render(screen)