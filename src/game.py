import sys
import pygame

from src.componnets.background_stars import BackgroundStars
from src.handle_event import handle_events
from src.render import render
from src.settings import Settings
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
        self.is_running = False

        self.create_background()

    def create_background(self):
        self.background.create_stars()

    def start(self):
        """
        Start game
        :return:
        """
        logger.debug("starting game")
        self.is_running = True
        try:

            while self.is_running:
                handle_events(self)  # handle events
                update(self)  # update state
                render(self)  # render updates
                self.clock.tick()

        except Exception as e:
            print(f"error ==>{e}")
            pass
        finally:
            self.stop()

    def stop(self, ):
        logger.info('closing ---------------------------')

        self.is_running = False
        pygame.quit()
        logger.info("stopped")
        sys.exit(0)


