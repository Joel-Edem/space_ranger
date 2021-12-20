import pygame
from pygame.sprite import Sprite

from src.load_assets import SpriteSheet, Location
from src.settings import PlayerDirection, Settings, ShipSettings


class Ship(Sprite):
    actions = {
        PlayerDirection.up: (0,),
        PlayerDirection.left: (4, 5, 6, 7, 7, 3, 3, 2, 1, 0, 7,),  # 360 rotation
        PlayerDirection.right: (0, 1, 2, 3, 3, 7, 7, 6, 5, 4, 3)
    }
    images = []
    sprite_sheet = SpriteSheet("images/space_ranger_sprite_sheet.png")
    ANIMATION_RATE = .25
    IDLE_RATE = .2

    @classmethod
    def initialize(cls):
        from assets.images.ship_frames import ship_frames

        if not cls.sprite_sheet.loaded:
            cls.sprite_sheet.load()

        for idx, frame in ship_frames['ship']["frames"].items():
            location = Location(
                x=frame["x"],
                y=frame["y"],
                width=ship_frames["frame_width"],
                height=ship_frames["frame_height"]
            )
            img = cls.sprite_sheet.get_image(at=location)
            cls.images.append(img)

    def __init__(self):
        super().__init__()
        Ship.initialize()

        self.direction: PlayerDirection = PlayerDirection.up
        self.current_frame = 0
        self.image = self.images[self.actions[self.direction][self.current_frame]]
        self.rect = self.image.get_rect()
        self.rect.centerx = Settings.screen_width / 2
        self.rect.bottom = Settings.screen_height - 10
        self.is_animating = False

    def handle_events(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] and self.direction != PlayerDirection.right:
            self.direction = PlayerDirection.right
            self.current_frame = 0
            self.is_animating = True
            # self.move_ship(PlayerDirection.right)
        elif keys[pygame.K_LEFT] and self.direction != PlayerDirection.left:
            self.direction = PlayerDirection.left
            self.current_frame = 0
            self.is_animating = True
            # self.move_ship(PlayerDirection.left)
        elif not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.is_animating = False

    def render(self, screen):
        screen.blit(self.image, self.rect)

    def move_ship(self):
        if self.direction == PlayerDirection.right and self.rect.right < Settings.screen_width:
            self.rect.x += ShipSettings.speed_factor
        elif self.direction == PlayerDirection.left and self.rect.left > 0:
            self.rect.x -= ShipSettings.speed_factor

    def reset_animation(self):
        self.current_frame -= self.ANIMATION_RATE
        if self.current_frame <= 0:
            self.current_frame = 0
            self.direction = PlayerDirection.up

    def update(self):
        self.handle_events()
        if not self.is_animating and self.direction != PlayerDirection.up and self.current_frame > 0:
            self.reset_animation()
        else:
            self.move_ship()
            self.current_frame += self.ANIMATION_RATE if self.is_animating else self.IDLE_RATE
            if self.current_frame >= len(self.actions[self.direction]):  # return to first image
                self.current_frame = 0 if not self.is_animating else self.current_frame - self.ANIMATION_RATE

        self.image = self.images[self.actions[self.direction][int(self.current_frame)]]
