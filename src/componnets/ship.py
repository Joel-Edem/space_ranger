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
    flames = []
    sprite_sheet = SpriteSheet("images/space_ranger_sprite_sheet.png")
    flame_sprite_sheet = SpriteSheet("images/flame_sprite_sheet.png")
    ANIMATION_RATE = .4
    IDLE_RATE = .2
    _initialized = False

    @classmethod
    def initialize(cls):
        from assets.images.ship_frames import ship_frames
        from assets.images.flame_frames import flame_frames

        if not cls.sprite_sheet.loaded:
            cls.sprite_sheet.load()
            cls.flame_sprite_sheet.load()
        if not cls._initialized:
            for idx, frame in flame_frames['flame']["frames"].items():
                location = Location(
                    x=frame["x"],
                    y=frame["y"],
                    width=flame_frames["frame_width"],
                    height=flame_frames["frame_height"]
                )
                img = cls.flame_sprite_sheet.get_image(at=location)
                cls.flames.append(img)

            for idx, frame in ship_frames['ship']["frames"].items():
                location = Location(
                    x=frame["x"],
                    y=frame["y"],
                    width=ship_frames["frame_width"],
                    height=ship_frames["frame_height"]
                )
                img = cls.sprite_sheet.get_image(at=location)
                cls.images.append(img)
            cls._initialized = True

    def __init__(self):
        super().__init__()
        Ship.initialize()

        self.direction: PlayerDirection = PlayerDirection.up
        self.current_frame = 0
        self.flame_idx = 0
        self.image = self.images[self.actions[self.direction][self.current_frame]]
        self.rect = self.image.get_rect()
        self.rect.centerx = Settings.screen_width / 2
        self.rect.bottom = Settings.screen_height - 35
        self.is_animating = False
        self.flame_rect = self.flames[self.flame_idx].get_rect()
        self.flame_rect.centerx = self.rect.centerx
        self.flame_rect.top = self.rect.bottom-20

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
        screen.blit(self.flames[int(self.flame_idx)], self.flame_rect)
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

    def animate_flame(self):
        self.flame_idx = (.25 + self.flame_idx) % len(self.flames)
        self.flame_rect.centerx = self.rect.centerx


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
        self.animate_flame()
