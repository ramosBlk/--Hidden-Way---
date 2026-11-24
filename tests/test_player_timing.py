import pygame
import pytest

from classes.entities.player import Player
from classes.systems.timing import accumulate_frame_time


class PressedKeys:
    def __init__(self, pressed):
        self.pressed = pressed

    def __getitem__(self, key):
        return key in self.pressed


@pytest.mark.parametrize("render_rate", (30, 60, 120))
def test_player_moves_the_same_distance_per_second_at_different_render_rates(
    monkeypatch, render_rate
):
    monkeypatch.setattr(
        pygame.key, "get_pressed", lambda: PressedKeys({pygame.K_d})
    )
    player = Player(x=100, y=570)
    player.no_chao = True
    accumulator = 0.0

    for _ in range(render_rate):
        steps, accumulator = accumulate_frame_time(1 / render_rate, accumulator)
        for _ in range(steps):
            player.atualizar_movimento(gravidade_ativada=False)

    assert player.x == pytest.approx(310.0)
