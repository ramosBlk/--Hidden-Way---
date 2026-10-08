import math
import random

import pygame

from classes.ui import Botao, NavegadorBotoes, desenhar_placa, texto_pixel


class GameOver:
    """
    Tela de Game Over (visual): cenário congelado escurecendo, placa de pedra que desce,
    título que "bate" na tela, subtítulo e botões que aparecem em sequência.

    tratar_evento() devolve "tentar" ou "menu" quando um botão é acionado.
    """
    T_PLACA = 0.5      # a placa termina de descer
    T_TITULO = 0.9     # título aparece
    T_BOTOES = 1.5     # botões aparecem e ficam clicáveis

    def __init__(self, largura=1400, altura=760):
        self.largura = largura
        self.altura = altura
        self.tempo = 0.0
        self.painel = pygame.Rect(0, 0, 700, 360)
        self.painel.center = (largura // 2, altura // 2 + 10)
        cx = largura // 2
        self.botoes = NavegadorBotoes([
            Botao("TENTAR NOVAMENTE", (cx, self.painel.bottom - 130)),
            Botao("VOLTAR AO MENU", (cx, self.painel.bottom - 60)),
        ])
        self._acoes = ("tentar", "menu")

    def atualizar(self, dt):
        self.tempo += dt

    def tratar_evento(self, evento):
        if self.tempo < self.T_BOTOES:
            return None
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:  # atalho já existente
            return "tentar"
        i = self.botoes.tratar_evento(evento)
        return self._acoes[i] if i is not None else None

    def _desenhar_caveira(self, janela, cx, topo):
        osso, osso_esc, vazio = (160, 165, 175), (130, 135, 145), (20, 15, 20)
        pygame.draw.ellipse(janela, osso_esc, (cx - 100, topo - 35, 65, 50))
        pygame.draw.ellipse(janela, osso_esc, (cx + 35, topo - 35, 65, 50))
        pygame.draw.rect(janela, vazio, (cx - 80, topo - 18, 12, 15))
        pygame.draw.rect(janela, vazio, (cx + 68, topo - 18, 12, 15))
        pygame.draw.ellipse(janela, osso, (cx - 55, topo - 50, 110, 75))
        pygame.draw.rect(janela, osso, (cx - 40, topo, 80, 30))
        pygame.draw.rect(janela, vazio, (cx - 30, topo - 25, 20, 25))
        pygame.draw.rect(janela, vazio, (cx + 10, topo - 25, 20, 25))
        pygame.draw.polygon(janela, vazio, [(cx, topo - 5), (cx - 6, topo + 8), (cx + 6, topo + 8)])
        for dx in (-24, -8, 8, 24):  # dentes
            pygame.draw.rect(janela, vazio, (cx + dx - 1, topo + 14, 2, 14))

    def desenhar(self, janela, fundo=None, subtitulo="Você caiu no buraco!"):
        t = self.tempo
        if fundo is not None:
            janela.blit(fundo, (0, 0))
        # escurece o cenário suavemente
        escuro = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        escuro.fill((10, 5, 8, int(175 + 55 * min(1.0, t / 0.5))))
        janela.blit(escuro, (0, 0))

        # placa desce com "quique" no final
        k = min(1.0, t / self.T_PLACA)
        desloc = -(self.painel.bottom + 80) * (1 - k) ** 2
        if k >= 1.0:
            desloc = 0
        painel = self.painel.move(0, int(desloc))
        cx = painel.centerx

        desenhar_placa(janela, painel)
        self._desenhar_caveira(janela, cx, painel.top)

        # título
        if t >= self.T_TITULO - 0.25:
            kt = min(1.0, (t - (self.T_TITULO - 0.25)) / 0.25)
            titulo = texto_pixel("GAME OVER", 22, (190, 40, 40), escala=4, sombra=(40, 10, 12))
            largura = int(titulo.get_width() * (1.6 - 0.6 * kt))
            altura = int(titulo.get_height() * (1.6 - 0.6 * kt))
            titulo = pygame.transform.scale(titulo, (largura, altura)).copy()
            titulo.set_alpha(int(255 * kt))
            tremor = (random.randint(-3, 3), random.randint(-3, 3)) if kt < 1.0 else (0, 0)
            janela.blit(titulo, titulo.get_rect(center=(cx + tremor[0], painel.top + 85 + tremor[1])))

        # subtítulo
        if t >= self.T_TITULO + 0.2:
            ks = min(1.0, (t - self.T_TITULO - 0.2) / 0.3)
            sub = texto_pixel(subtitulo, 10, (225, 215, 200), escala=2).copy()
            sub.set_alpha(int(255 * ks))
            janela.blit(sub, sub.get_rect(center=(cx, painel.top + 150)))

        # botões
        if t >= self.T_BOTOES - 0.3:
            alpha = int(255 * min(1.0, (t - (self.T_BOTOES - 0.3)) / 0.3))
            self.botoes.desenhar(janela, alpha)
