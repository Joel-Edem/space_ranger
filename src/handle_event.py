import pygame

from src.settings import PlayerDirection


def handle_events(self):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self.stop()
        elif event.type == pygame.KEYDOWN:
            pass
        elif event.type == pygame.KEYUP:
            pass


def handle_key_up(self, e):
    if e.key == pygame.K_RIGHT:
        self.background.star_direction = None
    elif e.key == pygame.K_LEFT:
        self.background.star_direction = None
    elif e.key == pygame.K_SPACE:
        pass
    if e.key == pygame.K_q:
        self.stop()


def handle_key_down(self, e):
    if e.key == pygame.K_RIGHT:
        self.background.star_direction = PlayerDirection.right
    elif e.key == pygame.K_LEFT:
        self.background.star_direction = PlayerDirection.left
    elif e.key == pygame.K_SPACE:
        pass
    if e.key == pygame.K_q:
        self.stop()
