import pygame

from src.componnets.bullet import Bullet


def handle_events(game):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.stop()
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_q, pygame.K_ESCAPE]:
                game.stop()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    fire_bullet(game)
        elif event.type == pygame.KEYUP:
            pass


def fire_bullet(game):

    # todo check if game has started
    # create bullet and add to bullet group
    Bullet(game.bullets, 'laser', game.ship.rect.centerx, game.ship.rect.top)

#
#
# def handle_key_up(self, e):
#     if e.key == pygame.K_RIGHT:
#         self.background.star_direction = None
#     elif e.key == pygame.K_LEFT:
#         self.background.star_direction = None
#     elif e.key == pygame.K_SPACE:
#         pass
#     if e.key == pygame.K_q:
#         self.stop()
#
#
# def handle_key_down(self, e):
#     if e.key == pygame.K_RIGHT:
#         self.background.star_direction = PlayerDirection.right
#     elif e.key == pygame.K_LEFT:
#         self.background.star_direction = PlayerDirection.left
#     elif e.key == pygame.K_SPACE:
#         pass
#     if e.key == pygame.K_q:
#         self.stop()
