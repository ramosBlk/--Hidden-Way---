import pytest
import pygame

from classes.systems.fases import criar_fase
from classes.systems.game_manager import GameManager


@pytest.mark.parametrize("indice", range(3))
def test_fase_inicializa_e_desenha(indice):
    fase = criar_fase(indice, GameManager(), 1400, 760)
    tela = pygame.display.get_surface()
    tela.fill((0, 0, 0))

    fase.desenhar(tela)
