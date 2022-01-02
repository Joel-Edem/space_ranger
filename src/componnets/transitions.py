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

    def handle_event(self, event=None):
        pass


class PauseGame(Transition):

    def render(self, screen):
        screen.blit(self.font_img, self.font_rect)
        self.resume_btn.render(screen)
        self.quit_btn.render(screen)

    # noinspection DuplicatedCode
    def update(self):
        x, y = pygame.mouse.get_pos()
        hits = False
        for idx, btn in enumerate([self.resume_btn, self.quit_btn]):
            if btn.rect.collidepoint(x, y):
                hits = True
                btn.set_active(True)
                self.curr_selection = "resume" if idx == 0 else "quit"

            else:
                btn.set_active(False)
        if not hits:

            if self.curr_selection == 'resume':
                self.resume_btn.set_active(True)
                self.quit_btn.set_active(False)
            else:
                self.resume_btn.set_active(False)
                self.quit_btn.set_active(True)

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

    def switch_active_button(self):
        if self.curr_selection == "resume":
            self.curr_selection = "quit"
            self.resume_btn.set_active(False)
            self.quit_btn.set_active(True)
        else:
            self.curr_selection = "resume"
            self.resume_btn.set_active(True)
            self.quit_btn.set_active(False)

    def handle_event(self, event=None):

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.resume_btn.handle_event()
            self.quit_btn.handle_event()
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_DOWN, pygame.K_UP]:
                self.switch_active_button()
            elif event.key == pygame.K_RETURN:
                if self.curr_selection == 'resume':
                    self.resume_btn.handle_click()
                elif self.curr_selection == 'quit':
                    self.quit_btn.handle_click()

    def __init__(self, callback=None):
        super().__init__(callback)
        self.font = pygame.font.SysFont(['poppins'], 68)

        self.font_img = self.font.render("Game Paused",
                                         True, (255, 255, 255), (0, 0, 0))

        self.font_rect = self.font_img.get_rect()
        self.font_rect.centerx = Settings.screen_width / 2
        self.font_rect.centery = Settings.screen_height / 2
        self.resume_btn = Button("Resume", self.font_rect.centerx, self.font_rect.bottom + 10,
                                 cb=self.handle_resume,
                                 button_color=(0, 150, 0), active_color=(0, 240, 0))
        self.quit_btn = Button("Quit", self.font_rect.centerx, self.resume_btn.rect.bottom + 10,
                               button_color=(150, 0, 0), active_color=(245, 0, 0), cb=self.handle_quit)
        self.curr_selection = "resume"


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
