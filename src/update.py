from src.componnets.aliens import Alien


def update(self) -> None:
    """
    # Update game state
    :return:
    """
    self.fps_counter.update()
    self.background.update_stars()

    if self.game_state.game_running and not self.game_state.transition:
        self.ship.update()
        self.bullets.update()
        Alien.update_fleet(self.aliens, self.bullets,
                           self.game_state.lost_life, self.game_state.level_complete,
                           self.score_board.update_score)
    self.game_state.update()
    self.score_board.update()
