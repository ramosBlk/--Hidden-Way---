import unittest

import pygame

from classes.systems.colisao import Colisao
from classes.systems.fases import FASES


class JogadorTeste:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.largura = 57
        self.hitbox_offset_x = 14
        self.hitbox_largura = 28
        self.altura = 58
        self.vel_x = 0
        self.vel_y = 0
        self.no_chao = False


class TesteColisaoParedesFase2(unittest.TestCase):
    def setUp(self):
        self.colisao = Colisao()
        self.parede = pygame.Rect(*FASES[1].paredes[3])
        self.plataforma_canto = pygame.Rect(*FASES[1].plataformas[23])
        self.parede_canto = pygame.Rect(*FASES[1].paredes[-1])

    def test_parede_do_canto_comeca_abaixo_da_plataforma_da_chave(self):
        self.assertEqual(
            self.parede_canto,
            pygame.Rect(
                self.plataforma_canto.left,
                self.plataforma_canto.bottom,
                self.plataforma_canto.width,
                528 - self.plataforma_canto.bottom,
            ),
        )

    def test_parede_do_canto_sustenta_o_jogador_sob_a_plataforma(self):
        jogador = JogadorTeste(1220, self.plataforma_canto.top - 58)
        jogador.vel_y = 6

        self.colisao.tratar_colisao_plataforma(jogador, [self.parede_canto])

        self.assertEqual(jogador.y, self.parede_canto.top - jogador.altura)
        self.assertTrue(jogador.no_chao)

    def test_impede_movimento_que_aprofunda_sobreposicao_com_parede(self):
        jogador = JogadorTeste(1180, 230)
        jogador.vel_x = 1

        self.colisao.tratar_colisao_plataforma(jogador, [self.parede])

        direita_hitbox = jogador.x + jogador.hitbox_offset_x + jogador.hitbox_largura
        self.assertEqual(direita_hitbox, self.parede.left)

    def test_bloqueia_ao_se_aproximar_da_parede(self):
        jogador = JogadorTeste(1173, 230)
        jogador.vel_x = 1

        self.colisao.tratar_colisao_plataforma(jogador, [self.parede])

        self.assertEqual(jogador.x, 1173)

    def test_permita_sair_de_sobreposicao_inicial_com_a_parede(self):
        jogador = JogadorTeste(1180, 230)
        jogador.vel_x = -1

        self.colisao.tratar_colisao_plataforma(jogador, [self.parede])

        self.assertEqual(jogador.x, 1179)


if __name__ == "__main__":
    unittest.main()
