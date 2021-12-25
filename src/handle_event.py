import pygame

from src.componnets.bullet import Bullet


def handle_events(game):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.stop()
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_q, pygame.K_ESCAPE]:
                if not game.game_state.game_running:
                    game.stop()
            elif event.key == pygame.K_SPACE:
                if game.game_state.game_running:
                    if not game.game_state.transition:
                        fire_bullet(game)
        game.game_state.handle_events(event)


def fire_bullet(game):
    # todo check if game has started
    # create bullet and add to bullet group
    Bullet(game.bullets, 'laser', game.ship.rect.centerx, game.ship.rect.top)
    game.sound_effects['laser'].play()
