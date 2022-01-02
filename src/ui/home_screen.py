import pygame

from src.settings import Settings
from src.widgets import Button


class HomeScreen:

    def __init__(self, state):
        """Home screen for game
        will have buttons to start game,
        view high scores,
        pick difficulty,
        adjust settings and quit"""

        self.current_selection = "start"
        self.last_active = 'start'
        self.widgets = {}
        self.game_state = state
        self.buttons = {
            "start": {
                "msg": "Start",
                "height": 50,
                "cb": self.game_state.create_new_game
            },
            "high_scores": {
                "msg": "High Scores",
                "height": 50,
                "cb": self.show_high_score_screen
            },

            "settings": {
                "msg": "Settings",
                "height": 50,
                "cb": None
            },

            "exit": {
                "msg": "Exit",
                "height": 50,
                "cb": self.game_state.game.stop
            }
        }
        self.create_widgets()

    def show_high_score_screen(self):
        from src.ui.high_score_screen import HighScoreScreen

        self.game_state.current_screen = HighScoreScreen(self.game_state)

    def create_widgets(self):
        """
        create buttons and ui elements
        :return:
        """
        for idx, w_name in enumerate(self.buttons.keys()):
            y = ((Settings.screen_height / 2) - (
                    self.buttons[w_name]["height"] * (len(self.buttons) / 2))
                 ) + 10 * idx + idx * self.buttons[w_name]["height"]

            self.widgets[w_name] = Button(self.buttons[w_name]['msg'],
                                          Settings.screen_width / 2, y,
                                          is_active=self.current_selection == w_name,
                                          cb=self.buttons[w_name]['cb'])

    def render(self, screen):
        for btn in self.widgets.values():
            btn.render(screen)

    def switch_active_button(self, up: bool):

        keys = list(self.buttons.keys())
        cur_idx = keys.index(self.current_selection)
        next_idx = (cur_idx - 1) if up else (cur_idx + 1) % len(keys)
        self.last_active = keys[next_idx]
        self.widgets[keys[cur_idx]].set_active(False)
        self.widgets[keys[next_idx]].set_active(True)
        self.current_selection = keys[next_idx]

    def handle_button_press(self, event):
        if event.key == pygame.K_DOWN:
            self.switch_active_button(False)
        elif event.key == pygame.K_UP:
            self.switch_active_button(True)
        elif event.key == pygame.K_RETURN:
            self.widgets[self.current_selection].handle_click()

    def handle_click(self):
        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            for btn_name, btn in self.widgets.items():
                if btn.rect.collidepoint(x, y):
                    btn.handle_click()
                    self.current_selection = btn_name
                    break

    def update(self):
        x, y = pygame.mouse.get_pos()
        hits = False
        for k, btn in self.widgets.items():
            if btn.rect.collidepoint(x, y):
                hits = True
                self.last_active = k
                btn.set_active(True)
            else:
                btn.set_active(False)
        if not hits:
            self.widgets[self.last_active].set_active(True)
