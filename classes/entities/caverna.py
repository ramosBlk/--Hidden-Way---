import math
import random
from enum import Enum

import pygame

from classes.systems.assets import carregar_imagem
from classes.systems.audio import Audio


class EstadoCaverna(Enum):
    BLOQUEADA = "bloqueada"
    LIBERANDO = "liberando"   # as pedras se desfazem
    LIBERADA = "liberada"


class Caverna:
    """
    Entrada da caverna (canto superior direito). Enquanto não estiver LIBERADA, uma pilha de
    pedras cobre a entrada e uma parede invisível impede a passagem. Depois do baú aberto, as
    pedras se desfazem e surge uma luz na entrada.
    """
    TEMPO_LIBERANDO = 1.0
    CENTRO = (1342, 197)

    def __init__(self, particulas):
        self.particulas = particulas
        self.entrada = pygame.Rect(1318, 168, 48, 62)   # área que dispara a mudança de fase
        self.parede = pygame.Rect(1306, 150, 14, 83)     # bloqueio sólido enquanto trancada
        self.estado = EstadoCaverna.BLOQUEADA
        self.tempo = 0.0
        self.brilho_extra = 0.0                           # 0..1: a luz cresce quando o player entra
        self.pedras = carregar_imagem("assets/sprites/itens/caverna_bloqueada.png", (66, 69), (110, 112, 118))
        self.luz = carregar_imagem("assets/sprites/itens/caverna_liberada.png", (66, 72), (255, 236, 170))

    @property
    def liberada(self):
        return self.estado == EstadoCaverna.LIBERADA

    def solidos(self):
        """Retângulos sólidos que dependem do estado (somados às paredes do cenário)."""
        return [] if self.liberada else [self.parede]

    def liberar(self):
        if self.estado != EstadoCaverna.BLOQUEADA:
            return
        self.estado = EstadoCaverna.LIBERANDO
        self.tempo = 0.0
        Audio.tocar("pedras")
        self.particulas.emitir(*self.CENTRO, 36, [(112, 114, 120), (88, 90, 98), (140, 142, 148)],
                               velocidade=(30, 130), vida=(0.5, 1.1), tam=(3, 6), gravidade=300,
                               area=(26, 28))

    def atualizar(self, dt):
        self.tempo += dt
        if self.estado == EstadoCaverna.LIBERANDO:
            if random.random() < 0.5:
                self.particulas.emitir(self.CENTRO[0], 190, 1, [(120, 122, 128), (90, 92, 100)],
                                       velocidade=(20, 70), vida=(0.4, 0.8), tam=(2, 4), gravidade=260,
                                       area=(24, 26))
            if self.tempo >= self.TEMPO_LIBERANDO:
                self.estado = EstadoCaverna.LIBERADA
        elif self.liberada and random.random() < 0.12:  # luzes saindo da entrada
            self.particulas.emitir(self.CENTRO[0], 215, 1, [(255, 244, 190), (255, 224, 140)],
                                   velocidade=(15, 45), vida=(0.8, 1.5), tam=(2, 3), angulo=(60, 120),
                                   area=(18, 6))

    def _desenhar_luz(self, janela, intensidade):
        pulso = 1 + 0.06 * math.sin(self.tempo * 4)
        escala = (1.0 + 2.2 * self.brilho_extra) * pulso * intensidade
        w, h = int(66 * 1.25 * escala), int(72 * 1.25 * escala)
        if w < 2 or h < 2:
            return
        luz = pygame.transform.scale(self.luz, (w, h))
        luz.set_alpha(int(255 * min(1.0, intensidade)))
        janela.blit(luz, luz.get_rect(center=self.CENTRO))

    def desenhar(self, janela):
        if self.estado == EstadoCaverna.BLOQUEADA:
            janela.blit(self.pedras, (1310, 155))
        elif self.estado == EstadoCaverna.LIBERANDO:
            k = self.tempo / self.TEMPO_LIBERANDO
            self._desenhar_luz(janela, k)
            # as pedras tremem, afundam e somem enquanto a luz cresce
            pedras = self.pedras.copy()
            pedras.set_alpha(int(255 * (1 - k)))
            janela.blit(pedras, (1310 + random.randint(-2, 2), 155 + int(26 * k * k)))
        else:
            self._desenhar_luz(janela, 1.0)
