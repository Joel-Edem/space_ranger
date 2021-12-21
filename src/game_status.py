from src.componnets.aliens import Alien
from src.componnets.ship import Ship
from src.componnets.transitions import GenericTransition
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

    def start_level(self):
        self.reset_game()
        self.game.ship = Ship()
        Alien.create_fleet(self.game.aliens, self.game.ship.rect.height, level=self.current_level)
        self.remaining_lives = GameSettings.max_lives
        self.current_level = 1
        self.game_running = True

    def create_new_game(self):
        self.reset_game()
        self.game.ship = Ship()
        Alien.create_fleet(self.game.aliens, self.game.ship.rect.height, level=self.current_level)
        self.remaining_lives = GameSettings.max_lives
        self.current_level = 1
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

        def game_end():
            self.game_running = False

        self.transition = GenericTransition(
            message="Game Over",
            callback=game_end)

    def increase_level(self):
        self.current_level += 1
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

            self.transition = GenericTransition(
                message="Your ship was destroyed",
                callback=self.restart_level)
        else:
            self.game_over()

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
