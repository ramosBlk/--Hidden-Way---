from types import SimpleNamespace

import pygame

from classes.entities.chave import Chave, EstadoChave
from classes.entities.inimigo import EstadoInimigo, Inimigo
from classes.systems.audio import Audio
from classes.systems.colisao import Colisao
from classes.systems.fases import proxima_fase
from classes.systems.game_manager import GameManager


def test_player_lands_on_thin_platform_without_tunneling():
    player = SimpleNamespace(
        x=20.0,
        y=0.0,
        altura=10,
        hitbox_offset_x=0,
        hitbox_largura=10,
        vel_x=0,
        vel_y=80,
        no_chao=False,
    )

    Colisao(100, 100).tratar_colisao_plataforma(
        player, [pygame.Rect(0, 50, 100, 2)]
    )

    assert player.y == 40
    assert player.vel_y == 0
    assert player.no_chao


def test_enemy_takes_three_hits_then_dies(monkeypatch):
    monkeypatch.setattr(Audio, "tocar", lambda _name: None)
    particulas = SimpleNamespace(emitir=lambda *args, **kwargs: None)
    inimigo = Inimigo("slime", 0, 100, 100, particulas)

    assert [inimigo.receber_dano() for _ in range(3)] == [True, True, True]
    assert inimigo.vida == 0
    assert inimigo.estado == EstadoInimigo.MORRENDO

    inimigo.atualizar(inimigo.TEMPO_MORRENDO)
    assert inimigo.estado == EstadoInimigo.MORTO


def test_key_collection_transitions_once_to_hud():
    particulas = SimpleNamespace(emitir=lambda *args, **kwargs: None)
    chave = Chave(20, 30, particulas)

    assert chave.coletar((100, 40))
    assert not chave.coletar((100, 40))
    chave.atualizar(chave.TEMPO_SUBIDA)

    assert chave.atualizar(chave.TEMPO_VOO)
    assert chave.estado == EstadoChave.COLETADA
    assert not chave.atualizar(1.0)


def test_phase_progression_preserves_lives_and_finishes_after_last_phase():
    gerenciador = GameManager()
    transicao = proxima_fase(1, gerenciador, 1400, 760, vidas=2)
    proxima = transicao["proxima_fase"]()

    assert proxima.indice == 2
    assert proxima.player.vidas == 2
    assert proxima_fase(2, gerenciador, 1400, 760)["proxima_fase"] is None
