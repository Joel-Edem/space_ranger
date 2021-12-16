import pygame


def render(self) -> None:
    """
    Render game changes
    :return:
    """
    self.screen.fill((0, 0, 0))
    self.background.render_stars(self.screen)
    self.fps_counter.render(self.screen)
    pygame.display.flip()
