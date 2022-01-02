import os.path
import sys
from typing import Optional

import pygame
from pygame.mixer import Sound
from pygame.sprite import Group

from src.componnets.background_stars import BackgroundStars
from src.componnets.scores import ScoreBoard
from src.componnets.ship import Ship
from src.game_status import GameStatus
from src.handle_event import handle_events
from src.render import render
from src.settings import Settings, ASSETS
import logging

from src.update import update
from src.widgets import FpsCounter

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Game:
    def __init__(self):
        """
        Entry point for space ranger game
        """
        logger.debug("initializing game")
        pygame.init()
        self.screen = pygame.display.set_mode(
            (Settings.screen_width, Settings.screen_height))
        logger.debug(f"display initialized to  {self.screen.get_size()}")
        self.clock = pygame.time.Clock()
        self.fps_counter = FpsCounter(self.clock)
        self.background = BackgroundStars
        self.create_background()
        self.ship: Optional[Ship] = None
        self.bullets: Group = Group()
        self.aliens: Group = Group()
        self.game_state = GameStatus(self)
        self.score_board = ScoreBoard(self.game_state)
        self.sound_effects: dict[str, Sound] = {}

        self.load_sounds()

    def load_sounds(self):

        for n in ["laser", "explosion"]:
            fp = os.path.join(ASSETS, 'sound', f'{n}.wav')
            sound = pygame.mixer.Sound(fp)
            if n == "explosion":
                sound.set_volume((Settings.sound_level / 100)/2)
            else:
                sound.set_volume(Settings.sound_level/100)
            self.sound_effects[n] = sound

    def create_background(self):
        self.background.create_stars()

    def run(self):
        """
        Start game loop
        :return:
        """
        logger.debug("starting game loop")
        # try:
        while True:
            handle_events(self)
            update(self)  # update state
            render(self)  # render updates
            self.clock.tick()

    def stop(self, ):
        logger.info('closing ---------------------------')

        self.game_state.reset_game()
        pygame.quit()
        logger.info("stopped")
        sys.exit(0)
