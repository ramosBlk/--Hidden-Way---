from types import SimpleNamespace

import pytest
import pygame

from classes.entities.pedra import Pedra
from classes.systems.combate import SistemaCombate


@pytest.mark.parametrize(
    "frame_delta, enemy_x",
    ((0.2, 50), (2.0, 500)),
)
def test_projectile_hits_enemy_crossed_during_long_frame(frame_delta, enemy_x):
    atingido = []
    inimigo = SimpleNamespace(
        vivo=True,
        hitbox=pygame.Rect(enemy_x, 2, 20, 16),
        receber_dano=lambda: atingido.append(True),
    )
    particulas = SimpleNamespace(emitir=lambda *args, **kwargs: None)
    combate = SistemaCombate(SimpleNamespace(), [inimigo], particulas)
    combate.projeteis.append(Pedra(10, 10, "direita"))

    combate.atualizar(frame_delta)

    assert atingido == [True]
    assert combate.projeteis == []
