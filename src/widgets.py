from typing import Optional

import pygame
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
        if active != self.is_active:
            self.is_active = active
            self.prep_message(self.message)

    def handle_click(self):
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


class Slider(pygame.Surface):

    def __init__(self, on_change=None, width: int = 400, level: int = 100, show_handle=True, show_label=True, label="slider"):
        """
        Volume slider component with slider and handle.
        users can use the arrow keys to move the slider if it is active.
        users can click and drag the handle to set its position.
        users can click on on the slider to set the position.
        current volume is displayed on the right
        **will accept callback to handle events
        :param width: Position of slider
        :param level: Initial position of slider. set to 100  by default
        """
        if width < 10:
            raise ValueError("With must be greater than 10 ")
        self.handle_change = on_change
        # slider level
        self._width = width
        self.font_color = (255, 255, 255)
        self.font = self.font = pygame.font.SysFont('poppins', 48)

        # create labels
        self.show_label = show_label
        self.title_text = label
        self.title_img = None
        self.title_rect: Optional[pygame.Rect] = None
        self.create_title()

        self.level = level
        self.level_img = None
        self.level_rect: Optional[pygame.Rect] = None
        self.create_level_label()
        self._height = self.level_rect.height + (self.title_rect.height + 5 if self.show_label else 0)
        super().__init__((self._width, self._height))
        self.rect = self.get_rect()

        # slider

        self.slider_rect: Optional[pygame.Rect] = None
        self.slider_rect_abs: Optional[pygame.Rect] = None
        self.bg_rect = None
        self.create_slider_rect()
        self.position_elements()

        # handle
        self.show_handle = show_handle
        self.handle_img = None
        self.handle_rect = None

        self.clicked = False
        self.set_initial_width()
        # Text labels

    def set_initial_width(self):
        """
        sets initial width on load
        :return:
        """
        self.slider_rect.width = self.bg_rect.width * (Settings.sound_level/100)
        self.set_new_level()



    def position_elements(self):
        if self.show_label:
            self.title_rect.centerx = self.rect.centerx
            self.title_rect.top = self.rect.top

        self.level_rect.right = self.rect.right - 10
        self.level_rect.top = self.rect.top if not self.show_label else self.title_rect.bottom

    def create_title(self):
        if self.show_label and self.title_text:
            self.title_img = self.font.render(self.title_text, True, self.font_color)
            self.title_rect = self.title_img.get_rect()

    def create_level_label(self):
        """
        Shows current level of slider
        :return:
        """
        # create Title
        self.level_img = self.font.render(f"{int(self.level)}", True, self.font_color)
        self.level_rect = self.level_img.get_rect()

    def create_slider_rect(self):
        """draw rect under title and before label"""
        self.slider_rect = pygame.Rect(
            10,
            (self.level_rect.height / 2) - (5 if not self.show_label else - self.title_rect.height + 5),
            self._width - 55 - 30, 10)  # 55==> self.level_rect.width when width is 100
        self.bg_rect = self.slider_rect.copy()

    def render(self, screen):
        self.blit(self.level_img, self.level_rect)
        if self.show_label:
            self.blit(self.title_img, self.title_rect)

        pygame.draw.rect(self, (86, 86, 86), self.bg_rect)
        pygame.draw.rect(self, (227, 227, 227), self.slider_rect)
        screen.blit(self, self.rect)

    def update(self):
        if self.clicked:
            self.update_slider_width()
            self.set_new_level()

    def set_new_level(self):
        _new_level = int(self.slider_rect.width / self.bg_rect.width * 100)
        if _new_level != self.level:
            self.level = _new_level
            pygame.draw.rect(self, (0, 0, 0), self.level_rect)
            self.level_img = self.font.render(f"{int(self.level)}", True, self.font_color)

            # callback
            if self.handle_change:
                self.handle_change(_new_level)

    def get_abs_pos_of_slider(self):
        return pygame.Rect(
            self.rect.x + self.bg_rect.x,
            self.rect.y + self.bg_rect.y,
            self.bg_rect.width, self.bg_rect.height)

    def handle_click(self):
        x, y = pygame.mouse.get_pos()
        self.slider_rect_abs = self.get_abs_pos_of_slider()
        if self.slider_rect_abs.collidepoint(x, y):
            self.clicked = True

    def update_slider_width(self):
        x, _ = pygame.mouse.get_pos()
        if x < self.slider_rect_abs.left:  # set to slider width to 0 zero
            self.slider_rect.width = 0
        elif x > self.bg_rect.width + self.slider_rect_abs.left:  # greater than 100 set to 100
            self.slider_rect.width = self.bg_rect.width
        else:  # between 0 and 100 set to new width
            self.slider_rect.width = x-self.slider_rect_abs.left

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.clicked:
                self.handle_click()
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.clicked:
                self.clicked = False
        elif event.type == pygame.KEYDOWN:
            pass