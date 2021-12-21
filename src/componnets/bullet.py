import os

import pygame.image
from pygame.sprite import Sprite, Group

from src.settings import ASSETS


class Bullet(Sprite):
    images = {
        "bullet": [],
        'laser': [],
    }

    @classmethod
    def load_images(cls, b_type):
        if not cls.images[b_type]:
            cls.images[b_type] = []
            for i in range(3, -1, -1):
                fn = os.path.join(ASSETS, 'images', b_type, f"{i}.png")
                cls.images[b_type].append(
                    pygame.image.load(fn).convert_alpha()
                )

    def __init__(self, group: Group, bullet_type: str, ship_x: float, ship_height: float, ):
        super().__init__(group)
        if not self.images[bullet_type]:
            self.load_images(bullet_type)
        self.current_idx = 0
        self.image = self.images[bullet_type][self.current_idx]
        self.rect = self.image.get_rect()
        self.rect.top = ship_height
        self.rect.centerx = ship_x
        self.speed_factor = 2
        self.is_animating = False
        self.bullet_type = bullet_type

    def check_bounds(self):
        if self.rect.bottom <= 0:
            self.kill()
            self.is_animating = False
            return False
        return True

    def update(self):
        if self.check_bounds():
            self.rect.y = float(self.rect.y) - self.speed_factor
            if self.is_animating:
                self.current_idx += .35
                if self.current_idx >= len(self.images[self.bullet_type]) - 1:
                    self.is_animating = False
                    self.kill()
                self.image = self.images[self.bullet_type][int(self.current_idx)]

    def destroy(self):
        """
        Animate bullet destruction
        :return:
        """
        self.is_animating = True


    def render(self, screen):
        screen.blit(self.image, self.rect)
