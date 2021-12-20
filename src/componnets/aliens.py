import dataclasses
import os

import pygame.image
from pygame.sprite import Sprite, Group

from src.settings import ASSETS, Settings, AlienSettings


@dataclasses.dataclass
class Position:
    x: int
    y: int


class Alien(Sprite):
    sprite_image = None

    @staticmethod
    def get_max_aliens_x(alien_width):
        available_space_x = Settings.screen_width - 2 * alien_width
        return int(available_space_x / (2 * alien_width))

    @staticmethod
    def get_max_aliens_y(alien_height, ship_height):
        available_y = Settings.screen_height - (3 * alien_height) - ship_height
        return int(available_y / (2 * alien_height))

    @classmethod
    def create_alien(cls, position: Position):
        alien = cls()
        alien.x = alien.rect.width + 2 * alien.rect.width * position.x
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * position.y
        return alien

    @classmethod
    def create_fleet(cls, group: Group, ship_height: int, level=1):
        """
        :param group:
        :param ship_height:
        :param level:
        :return:
        """

        _ = cls()
        number_of_aliens_x = cls.get_max_aliens_x(_.rect.width)
        number_of_aliens_y = cls.get_max_aliens_y(_.rect.height, ship_height)
        for y in range(number_of_aliens_y):
            for x in range(number_of_aliens_x):
                group.add(cls.create_alien(Position(x, y)))

    @classmethod
    def load_image(cls):
        if not cls.sprite_image:
            fn = os.path.join(ASSETS, 'images', f"ufo.png")
            cls.sprite_image = pygame.image.load(fn).convert_alpha()

    def __init__(self):
        super().__init__()
        if not self.sprite_image:
            self.load_image()
        self.image = self.sprite_image
        self.rect = self.image.get_rect()

    def check_edges(self):
        if self.rect.right >= Settings.screen_width:
            return True
        elif self.rect.left < 0:
            return True

    @classmethod
    def check_fleet_edges(cls, aliens: Group):
        "check if aliens have reached screen edge"
        for alien in aliens.sprites():
            alien: Alien
            if alien.check_edges():
                cls.change_fleet_direction(aliens)
                break

    @classmethod
    def change_fleet_direction(cls, aliens: Group):
        for alien in aliens.sprites():
            alien.rect.y += AlienSettings.drop_rate
        AlienSettings.direction *= -1

    def update(self, group: Group) -> None:
        self.rect.x += (AlienSettings.speed * AlienSettings.direction)

    @classmethod
    def update_fleet(cls, aliens: Group):
        cls.check_fleet_edges(aliens)
        aliens.update(aliens)

    def render(self, screen):
        screen.blit(self.image, self.rect)

# time warp power up
