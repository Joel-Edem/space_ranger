import pygame

from src.componnets.aliens import Alien
from src.componnets.ship import Ship
from src.componnets.transitions import GenericTransition, PauseGame
from src.settings import GameSettings
from src.ui.home_screen import HomeScreen


class GameStatus:

    def __init__(self, game):
        """
        Manages game state.
        provides functionality to start, stop and reset game,
        track scores and high score as well as current level
        """
        self.game = game
        self.game_running = False  # set to true when gema starts
        self.remaining_lives = 0
        self.current_level = 1
        self.current_screen = HomeScreen(self)
        self.transition = None

    # def start_level(self):
    #     self.reset_game()
    #     self.game.ship = Ship()
    #     Alien.create_fleet(self.game.aliens, self.game.ship.rect.height, level=self.current_level)
    #     self.remaining_lives = GameSettings.max_lives
    #     self.current_level = 1
    #     self.game_running = True

    def create_new_game(self):
        self.reset_game()
        self.game.ship = Ship()
        Alien.create_fleet(self.game.aliens, self.game.ship.rect.height, level=self.current_level)
        self.remaining_lives = GameSettings.max_lives
        self.current_level = 1
        self.game.score_board.new_game()
        self.game_running = True
        self.transition = GenericTransition(
            message="Defeat the invaders")

    def restart_level(self):
        """
        reset current level
        :return:
        """
        self.game.aliens.empty()
        self.game.bullets.empty()
        self.game.ship = None
        self.game.ship = Ship()
        Alien.create_fleet(self.game.aliens, self.game.ship.rect.height, )

    def game_over(self):
        """
        called when all  lives are lost
        :return:
        """

        def _game_end_cb():
            self.game_running = False

        self.game.score_board.handle_game_over()
        self.transition = GenericTransition(
            message="Game Over",
            callback=_game_end_cb)

    def increase_level(self):
        self.current_level += 1
        self.game.score_board.update_level()
        self.game.aliens.empty()
        self.game.bullets.empty()
        self.game.ship = Ship()
        self.restart_level()

    def level_complete(self):
        """
        called on completion

        :return:
        """
        self.transition = GenericTransition(
            message=f"Level {self.current_level} complete!",
            callback=self.increase_level)

    def lost_life(self):
        """
        removes life. if extra life restart level else show game over
        :return:
        """

        if self.remaining_lives:
            self.remaining_lives -= 1
            self.game.score_board.handle_life_lost()
            self.transition = GenericTransition(
                message="Your ship was destroyed",
                callback=self.restart_level)
        else:
            self.game_over()

    def pause_game(self):
        """
        pause game
        :return:
        """
        assert self.game_running, True
        self.transition = PauseGame(callback=self.reset_game)

    def handle_events(self, event):
        if self.game_running:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE]:
                    if not self.transition:
                        self.pause_game()
                    else:
                        self.transition = None  # unpause
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.transition:
                    self.transition.handle_event()

        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.current_screen.handle_click()

    def update(self):
        """
        update transitions if any
        :return:
        """
        if self.game_running:
            if self.transition:
                if self.transition.in_transition:
                    self.transition.update()
                else:
                    self.transition = None
        else:
            self.current_screen.update()

    def render(self, screen):
        if self.game_running:
            if self.transition:
                self.transition.render(screen)
        else:
            self.current_screen.render(screen)

    def reset_game(self):
        self.game.aliens.empty()
        self.game.bullets.empty()
        self.game.ship = None
        self.remaining_lives = 0
        self.current_level = 1
        self.game_running = False

# todo if in game, handle escape,
# todo handle arrow keys if not in game
# todo sound
# todo high score screen
# todo laser cool down
# todo explosions
# todo  settings screen: adjust volume
