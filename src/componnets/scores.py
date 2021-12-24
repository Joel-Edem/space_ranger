import json
import os
import pygame
from assets.images.ship_frames import ship_frames
from src.componnets.ship import Ship
from src.load_assets import Location
from src.settings import Settings, BASE_DIR


class ScoreBoard:

    def __init__(self, game_state):
        self.score = 0
        self.high_scores: list = []
        self.load_high_scores()
        self.game_state = game_state

        self.level = self.game_state.current_level
        self.font = pygame.font.SysFont('poppins', 48)
        self.font_color = (255, 255, 255)

        self.score_image = None
        self.score_rect = None

        self.high_score_image = None
        self.high_score_rect = None

        self.level_image = None
        self.level_image_rect = None
        self.last_score = None
        self.cur_high_score = self.high_scores[0] if len(self.high_scores) else 0
        self.last_high_score = None
        self.ships_left_image = None
        self.ships_left_rect = None

    def update_score_image(self):
        if self.score != self.last_score:
            self.score_image = self.font.render(
                f"{self.score}", True, self.font_color)
            self.score_rect = self.score_image.get_rect()
            self.score_rect.right = Settings.screen_width - 20
            self.score_rect.top = 10
            self.last_score = self.score

    def update_high_score_image(self):
        """
        :return:
        """
        if self.cur_high_score != self.last_high_score:
            self.high_score_image = self.font.render(
                f"High Score: {self.cur_high_score}", True, self.font_color)
            self.high_score_rect = self.high_score_image.get_rect()
            self.high_score_rect.centerx = Settings.screen_width / 2
            self.high_score_rect.top = 10
            self.last_high_score = self.cur_high_score
            self.high_score_image.convert_alpha()

    def update(self):
        self.update_high_score_image()
        if self.game_state.game_running:
            self.update_score_image()

    def render(self, screen):
        screen.blit(self.high_score_image, self.high_score_rect)
        if self.game_state.game_running:
            screen.blit(self.score_image, self.score_rect)
            screen.blit(self.ships_left_image, self.ships_left_rect)
            screen.blit(self.level_image, self.level_image_rect)

    def update_ships_remaining(self):
        """
        display and update number of ships remaining with sprite
        :return:
        """
        if not Ship.sprite_sheet.loaded:
            Ship.sprite_sheet.load()
        remaining_lives = self.game_state.remaining_lives
        if remaining_lives:
            width = round(ship_frames["frame_width"] * .4) * remaining_lives
            height = round(ship_frames["frame_height"] * .4)

            self.ships_left_image = pygame.Surface((width, height))
            frame = ship_frames['ship']["frames"][0]
            sprite_location = Location(
                x=frame["x"],
                y=frame["y"],
                width=ship_frames["frame_width"],
                height=ship_frames["frame_height"]
            )
            sprite_rect = pygame.Rect(sprite_location.area())
            image: pygame.Surface = Ship.sprite_sheet.get_image(at=sprite_location)
            # scale image
            x, y = image.get_size()
            image = pygame.transform.scale(image, (round(x * .4), round(y * .4)))

            for i in range(remaining_lives):
                self.ships_left_image.blit(image.copy(), (i * image.get_width(), 0),
                                           sprite_rect)

            self.ships_left_rect = self.ships_left_image.get_rect()
            self.ships_left_rect.top += 5
            self.ships_left_rect.left += 5

    def update_level(self):
        """
        Shows players current level
        :return:
        """

        self.level_image = self.font.render(f"lv {self.game_state.current_level}", True, self.font_color)
        self.level_image_rect = self.level_image.get_rect()
        self.level_image_rect.right = self.score_rect.right
        self.level_image_rect.top = self.score_rect.bottom + 10

    def update_score(self, num_aliens):
        """
        update score when alien is destroyed
        :return:
        """
        points = 50
        self.score = self.score + (points * num_aliens)
        if self.score > self.cur_high_score:
            self.cur_high_score = self.score

    def handle_life_lost(self):
        """
        reduce ship count on life lost event
        :return:
        """
        self.update_ships_remaining()

    def handle_game_over(self):
        """
        reset scores, and level,
         save high scores  and update high scores
        :return:
        """
        # check if score is high score
        # if high score add to high score list
        for (i) in range(len(self.high_scores)):
            if self.cur_high_score >= self.high_scores[i]:
                self.high_scores.insert(i, self.score)
                break
        if len(self.high_scores) > 10:  # onlu store 10 high scores
            self.high_scores.pop()
        # save high scores
        if self.score > 0:
            self.save_high_scores()

    def new_game(self):
        """
        starts a new game
        :return:
        """
        self.score = 0
        self.last_score = None
        self.last_high_score = None
        self.update_ships_remaining()
        self.update_score_image()
        self.update_level()

        self.cur_high_score = self.high_scores[0] if len(self.high_scores) else 0

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
            print(f"Could not find file {e.filename}")

    def save_high_scores(self):
        """
        save high scores to database on game over or shutdown
        :return:
        """
        fp = os.path.join(BASE_DIR, 'data', 'scores.json')
        self.high_scores.sort(reverse=True)
        with open(fp, 'w') as file:
            json.dump(self.high_scores, file)
