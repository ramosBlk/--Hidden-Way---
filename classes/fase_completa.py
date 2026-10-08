import math
import random

import pygame

from classes.systems.particulas import SistemaParticulas
from classes.ui import Botao, NavegadorBotoes, desenhar_placa, texto_pixel

CORES_CONFETE = [(255, 214, 74), (255, 120, 90), (110, 200, 255), (130, 230, 130), (240, 240, 255)]


class FaseCompleta:
    """Tela de conclusão: fundo escurece, placa dourada, texto, confetes e botão CONTINUAR."""
    T_PLACA = 0.6
    T_TEXTO = 1.0
    T_BOTAO = 1.8

    def __init__(self, largura=1400, altura=760):
        self.largura = largura
        self.altura = altura
        self.tempo = 0.0
        self.confete = SistemaParticulas()
        self.painel = pygame.Rect(0, 0, 700, 320)
        self.painel.center = (largura // 2, altura // 2)
        self.botoes = NavegadorBotoes([Botao("CONTINUAR", (largura // 2, self.painel.bottom - 60))])
        self._confete_emitido = False

    def atualizar(self, dt):
        self.tempo += dt
        if self.tempo >= self.T_TEXTO:
            if not self._confete_emitido:  # explosão inicial de confetes
                self._confete_emitido = True
                for x in (self.painel.left, self.painel.right):
                    self.confete.emitir(x, self.painel.top, 40, CORES_CONFETE, velocidade=(150, 420),
                                        vida=(1.2, 2.4), tam=(4, 7), gravidade=380, angulo=(50, 130))
            if random.random() < 0.6:  # chuva contínua
                self.confete.emitir(random.uniform(0, self.largura), -10, 1, CORES_CONFETE,
                                    velocidade=(20, 60), vida=(2.5, 4.0), tam=(4, 6), gravidade=120,
                                    angulo=(250, 290))
        self.confete.atualizar(dt)

    def tratar_evento(self, evento):
        """Retorna True quando o jogador aciona CONTINUAR."""
        if self.tempo < self.T_BOTAO:
            return False
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_e:
            return True
        return self.botoes.tratar_evento(evento) is not None

    def desenhar(self, janela, fundo=None, titulo="FASE COMPLETA!", subtitulo="Você desbloqueou a próxima fase!"):
        t = self.tempo
        janela.fill((0, 0, 0))
        if fundo is not None:
            janela.blit(fundo, (0, 0))
        escuro = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        escuro.fill((6, 8, 18, int(215 * min(1.0, t / 0.5))))
        janela.blit(escuro, (0, 0))

        k = min(1.0, t / self.T_PLACA)
        k = 1 - (1 - k) ** 3   # ease-out
        painel = self.painel.copy()
        painel.height = max(8, int(self.painel.height * k))
        painel.centery = self.painel.centery
        desenhar_placa(janela, painel, (190, 150, 50), (34, 32, 40))

        if t >= self.T_TEXTO - 0.3:
            kt = min(1.0, (t - (self.T_TEXTO - 0.3)) / 0.3)
            txt = texto_pixel(titulo, 22, (255, 214, 74), escala=4, sombra=(70, 40, 10)).copy()
            pulso = 1 + 0.03 * math.sin(t * 5)
            txt = pygame.transform.scale(txt, (int(txt.get_width() * pulso), int(txt.get_height() * pulso)))
            txt.set_alpha(int(255 * kt))
            janela.blit(txt, txt.get_rect(center=(self.painel.centerx, self.painel.top + 95)))
        if t >= self.T_TEXTO + 0.3:
            ks = min(1.0, (t - self.T_TEXTO - 0.3) / 0.3)
            sub = texto_pixel(subtitulo, 10, (230, 230, 240), escala=2).copy()
            sub.set_alpha(int(255 * ks))
            janela.blit(sub, sub.get_rect(center=(self.painel.centerx, self.painel.top + 165)))

        self.confete.desenhar(janela)

        if t >= self.T_BOTAO - 0.3:
            self.botoes.desenhar(janela, int(255 * min(1.0, (t - (self.T_BOTAO - 0.3)) / 0.3)))
