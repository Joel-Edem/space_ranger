import pygame

from src.settings import Settings
from src.widgets import Button


class Transition:

    def __init__(self, callback=None):
        """

        :param callback: Called when transition is complete
        """
        self.in_transition = True
        self.transition_count = 100
        self.callback = callback

    def update(self):
        raise NotImplementedError

    def render(self, *args, **kwargs) -> None:
        raise NotImplementedError

    def handle_event(self):
        pass


class PauseGame(Transition):

    def render(self, screen):
        screen.blit(self.font_img, self.font_rect)
        self.resume_btn.render(screen)
        self.quit_btn.render(screen)

    # noinspection DuplicatedCode
    def update(self):
        x, y = pygame.mouse.get_pos()
        for btn in [self.resume_btn, self.quit_btn]:
            btn.set_active(not not btn.rect.collidepoint(x, y))

    def handle_resume(self):
        """
        Callback for resume button
        :return:
        """
        self.in_transition = False

    def handle_quit(self):
        """
        callback for quit button
        :return:
        """
        self.callback()

    def handle_event(self):
        self.resume_btn.handle_event()
        self.quit_btn.handle_event()

    def __init__(self, callback=None):
        super().__init__(callback)
        self.font = pygame.font.SysFont(['poppins'], 68)

        self.font_img = self.font.render("Game Paused",
                                         True, (255, 255, 255), (0, 0, 0))

        self.font_rect = self.font_img.get_rect()
        self.font_rect.centerx = Settings.screen_width / 2
        self.font_rect.centery = Settings.screen_height / 2
        self.resume_btn = Button("Resume", self.font_rect.centerx, self.font_rect.bottom + 10,
                                 cb=self.handle_resume)
        self.quit_btn = Button("Quit", self.font_rect.centerx, self.resume_btn.rect.bottom + 10,
                               button_color=(255, 0, 0), active_color=(200, 0, 0), cb=self.handle_quit)


class GenericTransition(Transition):

    def __init__(self, message, callback=None, text_color=(255, 255, 255), ):
        super().__init__(callback)
        self.message = message
        self.font_color = text_color
        self.max_font_size = 68
        self.current_font_size = 20
        self.font = pygame.font.SysFont(['poppins'], self.current_font_size)
        self.font_img = self.font.render(self.message,
                                         True, self.font_color, (0, 0, 0))
        self.font_rect = self.font_img.get_rect()
        self.font_rect.centerx = Settings.screen_width / 2
        self.font_rect.centery = Settings.screen_height / 2

    def update(self):
        self.transition_count -= 1
        if int(self.transition_count) <= 0:
            self.in_transition = False
            if self.callback:
                self.callback()
        else:
            self.animate()

    def animate(self):
        if self.current_font_size < self.max_font_size:
            self.font = pygame.font.SysFont(['poppins'], self.current_font_size)
            self.font_img = self.font.render(self.message,
                                             True, self.font_color, (0, 0, 0))
            self.current_font_size += 2
            self.font_rect = self.font_img.get_rect()
            self.font_rect.centerx = Settings.screen_width / 2
            self.font_rect.centery = Settings.screen_height / 2

    def render(self, screen):
        screen.blit(self.font_img, self.font_rect)
