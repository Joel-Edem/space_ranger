import pygame.time
import pygame.font

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
        self.last_fps = 1000

    def update(self):
        """Update fps img"""
        if Settings.show_fps:
            cur_fps = int(self.clock.get_fps())
            # if self.last_fps - 15 <= cur_fps >= self.last_fps + 15:
            # print(cur_fps)
            self.fps_img = self.font.render(f"cur:{cur_fps} Min: {self.last_fps}", False, Settings.color_light,
                                            Settings.bg_color)
            self.fps_img.convert()
            self.fps_rect = self.fps_img.get_rect()
            self.fps_rect.top = 10
            self.fps_rect.left = 10
            if self.last_fps > cur_fps > 0:
                self.last_fps = cur_fps

    def render(self, screen):
        if self.fps_img and Settings.show_fps:
            screen.blit(self.fps_img, self.fps_rect)


class Button:
    def __init__(self, message: str, centerx: int, y: int, is_active=False, cb=None, **kwargs):
        # self.screen = screen
        # self.screen_rect = screen.get_rect()

        self.width = kwargs.get('width', 200)
        self.height = kwargs.get('height', 50)
        self.active_color = kwargs.get("active_color", (0, 123, 65))
        self.button_color = kwargs.get('button_color', (0, 255, 0))

        self.text_color = kwargs.get('text_color', (255, 255, 255))
        self.font = pygame.font.SysFont(['poppins'], kwargs.get('font_size', 48))

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = centerx
        self.rect.top = y
        self.msg_image_rect = None
        self.msg_img = None
        self.is_active = is_active
        self.message = message
        self.call_back = cb
        self.prep_message(message)

    def prep_message(self, message):
        self.msg_img = self.font.render(message, True, self.text_color,
                                        self.button_color if not self.is_active else self.active_color)
        self.msg_image_rect = self.msg_img.get_rect()
        self.msg_image_rect.center = self.rect.center

    def set_active(self, active):
        # if active != self.is_active:
        self.is_active = active
        self.prep_message(self.message)

    def handle_click(self):
        print("clicked")
        if self.call_back:
            self.call_back()

    def handle_event(self):
        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            if self.rect.collidepoint(x, y):
                self.handle_click()

    def update(self):
        # self.handle_mouse_enter()
        pass

    def render(self, screen):
        screen.fill(self.button_color if not self.is_active else self.active_color, self.rect)
        screen.blit(self.msg_img, self.msg_image_rect)
