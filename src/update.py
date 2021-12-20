def update(self) -> None:
    """
    # Update game state
    :return:
    """
    self.fps_counter.update()
    self.background.update_stars()

    self.ship.update()
    self.bullets.update()

