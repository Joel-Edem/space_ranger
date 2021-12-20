from src.componnets.aliens import Alien


def update(self) -> None:
    """
    # Update game state
    :return:
    """
    self.fps_counter.update()
    self.background.update_stars()
    Alien.update_fleet(self.aliens)
    self.ship.update()
    self.bullets.update()

