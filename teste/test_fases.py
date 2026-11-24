from pathlib import Path
import os
import sys

import pygame


RAIZ_PROJETO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ_PROJETO))
os.chdir(RAIZ_PROJETO)

from classes.systems.fases import FASES, criar_fase
from classes.systems.game_manager import GameManager
from classes.systems.timing import FIXED_TIMESTEP, accumulate_frame_time


LARGURA = 1400
ALTURA = 760


class TesteFases:
    def __init__(self):
        pygame.init()
        self.janela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Teste direto de fases - Hidden Way")
        self.relogio = pygame.time.Clock()
        self.gerenciador = GameManager()
        self.fase_atual = None
        self.rodando = True
        self.acumulador = 0.0
        self.fonte_titulo = pygame.font.SysFont("consolas", 42, bold=True)
        self.fonte_opcao = pygame.font.SysFont("consolas", 27)
        self.fonte_ajuda = pygame.font.SysFont("consolas", 18)
        self.opcoes = [
            "1 - FASE 1 - MAPA 1",
            f"2 - {FASES[1].nome}",
            f"3 - {FASES[2].nome}",
        ]

    def _abrir_fase(self, indice):
        self.fase_atual = indice
        self.gerenciador.mudar_estado(
            criar_fase(indice, self.gerenciador, LARGURA, ALTURA)
        )

    def _voltar_seletor(self):
        self.fase_atual = None
        self.acumulador = 0.0
        self.gerenciador.mudar_estado(None)

    def _tratar_eventos(self, eventos):
        if self.fase_atual is None:
            for evento in eventos:
                if evento.type == pygame.QUIT:
                    self.rodando = False
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        self.rodando = False
                    elif evento.key in (pygame.K_1, pygame.K_KP1):
                        self._abrir_fase(0)
                    elif evento.key in (pygame.K_2, pygame.K_KP2):
                        self._abrir_fase(1)
                    elif evento.key in (pygame.K_3, pygame.K_KP3):
                        self._abrir_fase(2)
            return

        eventos_fase = []
        for evento in eventos:
            if evento.type == pygame.QUIT:
                self.rodando = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                self._voltar_seletor()
                return
            else:
                eventos_fase.append(evento)

        if self.fase_atual is not None:
            self.gerenciador.tratar_eventos(eventos_fase)

    def _desenhar_seletor(self):
        self.janela.fill((18, 24, 42))
        titulo = self.fonte_titulo.render("TESTAR FASE", True, (245, 230, 160))
        self.janela.blit(titulo, titulo.get_rect(center=(LARGURA // 2, 190)))

        for i, opcao in enumerate(self.opcoes):
            texto = self.fonte_opcao.render(opcao, True, (235, 240, 250))
            self.janela.blit(texto, texto.get_rect(center=(LARGURA // 2, 310 + i * 58)))

        ajuda = self.fonte_ajuda.render(
            "Pressione 1, 2 ou 3 para iniciar uma fase | ESC para sair",
            True,
            (180, 195, 215),
        )
        self.janela.blit(ajuda, ajuda.get_rect(center=(LARGURA // 2, 550)))

    def executar(self):
        while self.rodando:
            dt = self.relogio.tick(60) / 1000.0
            self._tratar_eventos(pygame.event.get())

            if self.fase_atual is None:
                self.acumulador = 0.0
                self._desenhar_seletor()
            else:
                passos, self.acumulador = accumulate_frame_time(dt, self.acumulador)
                for _ in range(passos):
                    self.gerenciador.atualizar(FIXED_TIMESTEP)
                self.gerenciador.desenhar(self.janela)

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    TesteFases().executar()
