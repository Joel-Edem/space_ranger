import dataclasses
import os
from typing import Callable

import pygame.image
from pygame import Rect
from pygame.sprite import Sprite, Group

from src.componnets.bullet import Bullet
from src.load_assets import SpriteSheet, Location
from src.settings import ASSETS, Settings, AlienSettings


@dataclasses.dataclass
class Position:
    x: int
    y: int


class Alien(Sprite):
    sprite_image = None
    explosion_sprites = []
    explosion_sprite_sheet = SpriteSheet(os.path.join("images", "explosion_sprite_sheet.png"))

    @staticmethod
    def get_max_aliens_x(alien_width):
        available_space_x = Settings.screen_width - 2 * alien_width
        return int(available_space_x / (2 * alien_width))

    @staticmethod
    def get_max_aliens_y(alien_height, ship_height):
        available_y = Settings.screen_height - (5 * alien_height) - ship_height
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
        if not cls.explosion_sprite_sheet.loaded:
            cls.explosion_sprite_sheet.load()

            for row in range(6):
                for col in range(7):
                    if row == 5 and col > 4:
                        # print(len(cls.explosion_sprites))
                        break

                    location = Location(
                        x=col * 250,
                        y=row * 250,
                        width=250,
                        height=250
                    )
                    img = cls.explosion_sprite_sheet.get_image(at=location)
                    x, y = img.get_size()
                    new_x = round(x * .25)
                    new_y = round(y * .25)
                    cls.explosion_sprites.append(pygame.transform.scale(img, (new_x, new_y)))

    def __init__(self):
        super().__init__()
        self.load_image()
        self.image = self.sprite_image
        self.rect = self.image.get_rect()
        self.is_dying = False
        self.shrink = 0
        self.explosion_idx = 0
        self.explosion_rect: Rect = self.explosion_sprites[0].get_rect()
        self.explosion_rect.center = self.rect.center

    def check_edges(self):
        if self.rect.right >= Settings.screen_width:
            return True
        elif self.rect.left < 0:
            return True

    @classmethod
    def check_bottom(cls, aliens: Group, fn=None):
        """
        Check if ship has hit bottom edge
        :param aliens:
        :param fn: callback function
        :return:
        """
        for alien in aliens.sprites():
            if alien.rect.bottom >= Settings.screen_height:
                if fn:
                    fn()
                break

    def handle_bullet_hit(self):
        """
        trigger animation when hit by bullet or ship
        :return:
        """
        if not self.is_dying:
            self.is_dying = True
            self.shrink = 100

    @classmethod
    def check_fleet_edges(cls, aliens: Group):
        """check if aliens have reached screen edge
        :param aliens:
        """
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

    def animate(self):
        next_idx = self.explosion_idx + 1
        if int(next_idx) < len(self.explosion_sprites):
            self.explosion_idx = next_idx
            self.explosion_rect: Rect = self.explosion_sprites[int(self.explosion_idx)].get_rect()
            self.explosion_rect.center = self.rect.center
            self.shrink -= 1
            x, y = self.image.get_size()
            new_x = round(x * .95)
            new_y = round(y * .95)
            self.image = pygame.transform.scale(self.image, (new_x, new_y))
            self.rect = self.image.get_rect(center=self.rect.center)
        else:
            self.shrink = 0

    def update(self) -> None:
        self.rect.x += (AlienSettings.speed * AlienSettings.direction)
        if self.is_dying:
            if int(self.shrink):
                self.animate()
            else:
                self.kill()

    @classmethod
    def check_bullet_ship_collisions(cls, bullets, aliens, update_score: Callable[[int], None] = None, sound=None):
        """
        check if bullets collided with aliens and  remove
        :return:
        """
        collisions = pygame.sprite.groupcollide(bullets, aliens, False, False)

        aliens_hit: list[Alien]
        bullet: Bullet
        for bullet, aliens_hit in collisions.items():
            if not bullet.is_animating:
                for alien in aliens_hit:
                    if not alien.is_dying:
                        alien.handle_bullet_hit()
                        sound.play()
                        update_score(1)
                bullet.destroy()
        # if collisions:
        #
        #     alien: list[Alien,]
        #     bullet: Bullet
        #     for alien in collisions.values():
        #         # if not alien.is_dying:
        #         print(alien)
        #         alien[0].handle_bullet_hit()
        #
        #     for bullet in collisions.keys():
        #         bullet.destroy()
        #

    @classmethod
    def check_level_complete(cls, aliens, cb):
        """

        :param aliens:
        :param cb: callback
        :return:
        """
        if not len(aliens):
            cb()

    @classmethod
    def update_fleet(cls, aliens: Group, bullets: Group,
                     life_lost=None, level_complete=None, update_score: Callable[[int], None] = None, sound=None):
        cls.check_fleet_edges(aliens)
        cls.check_bottom(aliens, life_lost)
        cls.check_bullet_ship_collisions(bullets, aliens, update_score, sound)
        aliens.update()
        cls.check_level_complete(aliens, level_complete)

    def render(self, screen):
        screen.blit(self.image, self.rect)
        if self.is_dying:
            screen.blit(self.explosion_sprites[int(self.explosion_idx)], self.explosion_rect)

# time warp power up
