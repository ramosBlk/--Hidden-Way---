import math

import pygame

from classes.entities.player import Player
from classes.states.game_state import GameState
from classes.systems.cenario import Cenario
from classes.systems.hud import Hud
from classes.systems.particulas import SistemaParticulas
from classes.systems.queda import QuedaNoBuraco, caiu_no_buraco
from classes.systems.transicao import Fade


class Mapa2State(GameState):
    """
    Fase 2 (interior da caverna): primeira versão jogável, com chão com buracos e um cristal
    de saída. Serve de "próxima fase" da mecânica chave -> baú -> caverna.
    """
    PLATAFORMAS = [
        pygame.Rect(0, 660, 480, 12),
        pygame.Rect(600, 660, 300, 12),
        pygame.Rect(1020, 660, 380, 12),
        pygame.Rect(240, 540, 150, 10),
        pygame.Rect(690, 520, 180, 10),
        pygame.Rect(1010, 520, 150, 10),
    ]
    CRISTAL = pygame.Rect(1290, 590, 40, 70)

    def __init__(self, gerenciador, largura, altura):
        super().__init__(gerenciador)
        self.largura = largura
        self.altura = altura
        self.player = Player(x=60, y=590, escala=0.6)
        self.cenario = Cenario("assets/sprites/telas/Mapa_2.png", largura=largura, altura=altura,
                               eh_plataforma=True, plataformas=self.PLATAFORMAS, paredes=[])
        self.particulas = SistemaParticulas()
        self.hud = Hud(largura, altura)
        self.queda = QuedaNoBuraco(largura, altura)
        self.fade_entrada = Fade(largura, altura, 1.0, "entrada")
        self.fade_saida = None
        self.tempo = 0.0
        self.morrendo = False
        self.hud.avisar("FASE 2 - A CAVERNA", duracao=3.0)

    def atualizar(self, dt=1 / 60):
        self.tempo += dt
        self.particulas.atualizar(dt)
        self.hud.atualizar(dt)
        self.fade_entrada.atualizar(dt)

        if self.morrendo:
            if self.queda.atualizar(dt):
                from classes.states.game_over_state import GameOverState
                self.gerenciador.mudar_estado(GameOverState(
                    self.gerenciador, self.largura, self.altura, fundo=self.queda.quadro,
                    reiniciar=lambda: Mapa2State(self.gerenciador, self.largura, self.altura)))
            return

        if self.fade_saida:
            self.fade_saida.atualizar(dt)
            if self.fade_saida.concluido:
                from classes.states.fase_completa_state import FaseCompletaState
                self.gerenciador.mudar_estado(FaseCompletaState(
                    self.gerenciador, self.largura, self.altura, proxima_fase=None,
                    titulo="FIM DA DEMO", subtitulo="Novas fases em breve!"))
            return

        self.player.atualizar_movimento(gravidade_ativada=True, plataformas=self.cenario.plataformas, paredes=[])
        if self.player.hitbox().colliderect(self.CRISTAL):
            self.fade_saida = Fade(self.largura, self.altura, 0.8, "saida")
        elif caiu_no_buraco(self.player, self.altura):
            self.queda.iniciar(self.player, self.particulas)
            self.morrendo = True

    def desenhar(self, janela):
        self.cenario.desenhar(janela)
        for p in self.PLATAFORMAS:  # plataformas de pedra
            pygame.draw.rect(janela, (74, 70, 98), (p.x, p.y, p.w, 36))
            pygame.draw.rect(janela, (120, 116, 150), (p.x, p.y, p.w, 6))
            pygame.draw.rect(janela, (30, 28, 44), (p.x, p.y, p.w, 36), 3)
        # cristal de saída pulsando
        pulso = 0.5 + 0.5 * math.sin(self.tempo * 4)
        c = self.CRISTAL
        pygame.draw.polygon(janela, (70, 200, 230), [(c.centerx, c.top), (c.right, c.bottom - 14),
                                                      (c.centerx, c.bottom), (c.left, c.bottom - 14)])
        pygame.draw.polygon(janela, (210 + int(40 * pulso), 250, 255), [(c.centerx, c.top + 10),
                                                                        (c.centerx + 8, c.bottom - 20),
                                                                        (c.centerx - 4, c.bottom - 20)])

        if self.morrendo:
            self.queda.desenhar_player(janela, self.player)
        else:
            self.player.desenhar(janela)
        self.particulas.desenhar(janela)
        self.hud.desenhar(janela, mostrar_chave=False)
        if self.morrendo:
            self.queda.desenhar_fade(janela)
        if self.fade_saida:
            self.fade_saida.desenhar(janela)
        self.fade_entrada.desenhar(janela)
