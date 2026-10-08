import math
import random
from enum import Enum

import pygame

from classes.systems.assets import carregar_imagem
from classes.systems.audio import Audio


class EstadoPorta(Enum):
    FECHADA = "fechada"
    ABRINDO = "abrindo"
    ABERTA = "aberta"


class Porta:
    """Porta de saída da fase: trancada até todas as chaves serem coletadas."""
    TEMPO_ABRINDO = 0.9

    def __init__(self, x, y_chao, particulas):
        self.rect = pygame.Rect(0, 0, 60, 84)
        self.rect.midbottom = (x, y_chao)
        self.entrada = self.rect.inflate(-24, 0)
        self.particulas = particulas
        self.estado = EstadoPorta.FECHADA
        self.tempo = 0.0
        self.brilho_extra = 0.0
        self.fechada = carregar_imagem("assets/sprites/itens/porta_0.png", (60, 84), (80, 70, 60))
        self.aberta = carregar_imagem("assets/sprites/itens/porta_1.png", (60, 84), (255, 240, 170))
        self.brilho = carregar_imagem("assets/sprites/efeitos/brilho.png", (48, 48), (255, 230, 140))

    @property
    def liberada(self):
        return self.estado == EstadoPorta.ABERTA

    def liberar(self):
        if self.estado != EstadoPorta.FECHADA:
            return
        self.estado = EstadoPorta.ABRINDO
        self.tempo = 0.0
        Audio.tocar("porta")
        self.particulas.emitir(self.rect.centerx, self.rect.centery, 30,
                               [(255, 244, 190), (255, 224, 140), (180, 182, 190)],
                               velocidade=(30, 150), vida=(0.5, 1.1), tam=(2, 5), gravidade=100, area=(24, 36))

    def atualizar(self, dt):
        self.tempo += dt
        if self.estado == EstadoPorta.ABRINDO and self.tempo >= self.TEMPO_ABRINDO:
            self.estado = EstadoPorta.ABERTA
        elif self.liberada and random.random() < 0.1:
            self.particulas.emitir(self.rect.centerx, self.rect.bottom - 10, 1, [(255, 244, 190)],
                                   velocidade=(15, 40), vida=(0.8, 1.4), tam=(2, 3), angulo=(60, 120), area=(14, 4))

    def _halo(self, janela, intensidade):
        tam = int((90 + 160 * self.brilho_extra) * intensidade * (1 + 0.05 * math.sin(self.tempo * 4)))
        if tam < 2:
            return
        halo = pygame.transform.scale(self.brilho, (tam, tam))
        janela.blit(halo, halo.get_rect(center=self.rect.center))

    def desenhar(self, janela):
        if self.estado == EstadoPorta.FECHADA:
            janela.blit(self.fechada, self.rect)
        elif self.estado == EstadoPorta.ABRINDO:
            k = self.tempo / self.TEMPO_ABRINDO
            self._halo(janela, k)
            janela.blit(self.fechada, self.rect.move(random.randint(-2, 2), 0))
            aberta = self.aberta.copy()
            aberta.set_alpha(int(255 * k))
            janela.blit(aberta, self.rect)
        else:
            self._halo(janela, 1.0)
            janela.blit(self.aberta, self.rect)
