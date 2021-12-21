import pygame


def render(self) -> None:
    """
    Render game changes
    :return:
    """
    self.background.render_stars(self.screen)
    self.fps_counter.render(self.screen)

    if self.game_state.game_running:
        for alien in self.aliens.sprites():
            alien.render(self.screen)
        for bullet in self.bullets.sprites():
            bullet.render(self.screen)

        self.ship.render(self.screen)
    self.game_state.render(self.screen)
    pygame.display.flip()
