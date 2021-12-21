import pygame

from src.settings import Settings


class Transition:

    def __init__(self, callback=None):
        self.in_transition = True
        self.transition_count = 100
        self.callback = callback

    def update(self):
        # self.in_transition = False
        self.transition_count -= 1
        if int(self.transition_count) <= 0:
            self.in_transition = False
            if self.callback:
                self.callback()

    def render(self, *args, **kwargs) -> None:
        raise NotImplementedError


class GenericTransition(Transition):

    def __init__(self,message, callback=None, text_color=(255, 255, 255), ):
        super().__init__(callback)
        self.message=message
        self.font_color = text_color
        self.max_font_size = 68
        self.current_font_size = 20
        self.font = pygame.font.SysFont(['poppins'], self.current_font_size)
        self.font_img = self.font.render(self.message,
                                         True, self.font_color, (0, 0, 0))

        # self.rect = pygame.Rect(0, 0, int(Settings.screen_width / 5), int(Settings.screen_height / 9))
        # self.rect.centerx = Settings.screen_width / 2
        # self.rect.centery = Settings.screen_height / 2

        self.font_rect = self.font_img.get_rect()
        self.font_rect.centerx = Settings.screen_width / 2
        self.font_rect.centery = Settings.screen_height / 2

    def update(self):
        self.transition_count -= .7
        if int(self.transition_count) <= 0:
            self.in_transition = False
            if self.callback:
                self.callback()
        else:
            self.animate()
        # if int(self.transition_count) > 0:
        #     self.font_img, self.font_rect = self.animate(self.font_img, self.font_rect.center)
        # self.transition_count -= 10

    def animate(self):
        if self.current_font_size < self.max_font_size:
            self.font = pygame.font.SysFont(['poppins'], self.current_font_size)
            self.font_img = self.font.render(self.message,
                                             True, self.font_color, (0, 0, 0))
            self.current_font_size += 1
            self.font_rect = self.font_img.get_rect()
            self.font_rect.centerx = Settings.screen_width / 2
            self.font_rect.centery = Settings.screen_height/2


        # x, y = self.font_img.get_size()
        # new_x = round(x * 1.004)
        # new_y = round(y * 1.004)
        # self.font_img = pygame.transform.scale(self.font_img, (new_x, new_y))
        # self.font_rect = self.font_img.get_rect(center=self.font_rect.center)
        # if not int(x) or not int(y):
        #     self.transition_count = 0

    def render(self, screen):
        # screen.fill((0, 255, 0), self.rect)

        screen.blit(self.font_img, self.font_rect)
        # self.rect.set_alpha(50)
        # screen.blit(self.surface, self.font_rect)
