import json
import os

import pygame

from src.game_status import GameStatus
from src.settings import BASE_DIR, Settings
from src.widgets import Button


class HighScoreScreen:

    def __init__(self, state):
        self.game_state: GameStatus = state
        self.score_labels = []
        self.score_rects = []
        self.high_scores = []
        self.font = pygame.font.SysFont('poppins', 48)
        self.title_font = pygame.font.SysFont('poppins', 78)
        self.font_color = (255, 255, 255)
        self.back_button = None
        self.title = None
        self.title_rect = None

        self.load_high_scores()
        self.create_title()
        self.create_high_score_labels()
        self.create_buttons()

    def load_high_scores(self):

        """
        load high scores on startup
        :return:
        """
        fp = os.path.join(BASE_DIR, 'data', 'scores.json')
        try:
            with open(fp, 'r') as file:
                self.high_scores = json.load(file)
        except FileNotFoundError as e:
            print(f"Could not find file {e.filename}"
                  )

    def create_high_score_labels(self):
        self.score_labels = []
        self.score_rects = []
        gold = (255, 226, 48)
        if len(self.high_scores):
            for idx, score in enumerate(self.high_scores):
                score_img = self.font.render(
                    f"{int(score):,}", True, gold if idx < 3 else self.font_color)
                score_rect = score_img.get_rect()
                score_rect.centerx = Settings.screen_width / 2
                score_rect.top = self.title_rect.bottom + 20 + (10 * idx) + (idx * score_rect.height)
                self.score_labels.append(score_img)
                self.score_rects.append(score_rect)
        else:
            score_img = self.font.render(f"No High Scores", True, self.font_color)
            score_rect = score_img.get_rect()
            score_rect.centerx = Settings.screen_width / 2
            score_rect.top = self.title_rect.bottom + 20
            self.score_labels.append(score_img)
            self.score_rects.append(score_rect)

    def create_title(self):
        self.title = self.title_font.render(
            f"High Scores", True, self.font_color)
        self.title_rect = self.title.get_rect()
        self.title_rect.centerx = Settings.screen_width / 2
        self.title_rect.top = 70

    def close_screen(self):
        from src.ui.home_screen import HomeScreen
        self.game_state.current_screen = HomeScreen(self.game_state)

    def create_buttons(self):
        y = (self.score_rects[-1].bottom if len(self.score_rects) else self.title_rect.bottom) + 20
        x = Settings.screen_width / 2
        self.back_button = Button("Back", x, y, False, self.close_screen)

    def handle_click(self):
        self.back_button.handle_event()

    def handle_button_press(self, event):
        if event.key == pygame.K_RETURN:
            self.back_button.handle_click()

    def update(self):
        pass

    def render(self, screen):
        screen.blit(self.title, self.title_rect)
        for idx, score in enumerate(self.score_labels):
            screen.blit(score, self.score_rects[idx])

        self.back_button.render(screen)
