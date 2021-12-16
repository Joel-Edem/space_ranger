import pygame.time

from src.settings import Settings


class FpsCounter:

    def __init__(self, clock: pygame.time.Clock, **kwargs):
        """
        displays current game frame rate
        :param clock:
        """
        self.clock = clock
        self.font = pygame.font.SysFont(['poppins'], kwargs.get('font_size', 48))
        self.fps_img = None
        self.fps_rect = None
        self.last_fps = 0

    def update(self):
        """Update fps img"""
        cur_fps = int(self.clock.get_fps())
        # if self.last_fps - 15 <= cur_fps >= self.last_fps + 15:
            # print(cur_fps)
        self.fps_img = self.font.render(f"cur:{cur_fps} max: {self.last_fps}", False, Settings.color_light, Settings.bg_color)
        self.fps_img.convert()
        self.fps_rect = self.fps_img.get_rect()
        self.fps_rect.top = 10
        self.fps_rect.left = 10
        if cur_fps > self.last_fps:
            self.last_fps = cur_fps

    def render(self, screen):
        if self.fps_img:
            screen.blit(self.fps_img, self.fps_rect)
