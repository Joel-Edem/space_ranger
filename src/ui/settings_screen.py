from collections import OrderedDict

import pygame

from src.settings import Settings
from src.widgets import Button, Slider


class SettingsScreen:

    def __init__(self, game_state):
        self.game_state = game_state
        self.font = pygame.font.SysFont('poppins', 48)
        self.title_font = pygame.font.SysFont('poppins', 78)
        self.font_color = (255, 255, 255)
        self.back_button = None
        self.title = None
        self.title_rect = None

        self.widgets = OrderedDict()
        self.create_title()
        self.create_widgets()
        self.create_buttons()

    def create_title(self):
        self.title = self.title_font.render(
            f"Settings", True, self.font_color)
        self.title_rect = self.title.get_rect()
        self.title_rect.centerx = Settings.screen_width / 2
        self.title_rect.top = 70

    def close_screen(self):
        from src.ui.home_screen import HomeScreen
        self.game_state.current_screen = HomeScreen(self.game_state)

    def create_buttons(self):
        y = (list(self.widgets.values())[-1].rect.bottom if len(self.widgets) else self.title_rect.bottom) + 40
        x = Settings.screen_width / 2
        self.back_button = Button("Back", x, y, False, self.close_screen)

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_click()
        elif event.type == pygame.KEYDOWN:
            self.handle_button_press(event)
        self.widgets["volume_slider"].handle_event(event)

    def handle_click(self):
        self.back_button.handle_event()

    def handle_button_press(self, event):
        if event.key == pygame.K_RETURN:
            self.back_button.handle_click()

    def create_widgets(self):
        self.create_volume_slider()

    def create_volume_slider(self):
        self.widgets["volume_slider"] = Slider(label="sound", on_change=self.update_volume, level=Settings.sound_level)
        self.widgets["volume_slider"].rect.top = self.title_rect.bottom + 10
        self.widgets["volume_slider"].rect.centerx = self.title_rect.centerx

    def update_volume(self, volume):
        Settings.sound_level = volume
        for sound_name in self.game_state.game.sound_effects.keys():
            self.game_state.game.set_volume(sound_name)
        Settings.save()

    def update(self):
        self.widgets['volume_slider'].update()

    def render(self, screen):
        screen.blit(self.title, self.title_rect)
        self.back_button.render(screen)
        for w in self.widgets.values():
            w.render(screen)

# todo fix convert call on some surfaces: You did not assign the new surface to the pointer
