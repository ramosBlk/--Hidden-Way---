import math
import random
from enum import Enum

import pygame

from classes.systems.assets import carregar_imagem
from classes.systems.audio import Audio


class EstadoBau(Enum):
    FECHADO = "fechado"
    ABRINDO = "abrindo"
    ABERTO = "aberto"


class Bau:
    """
    Baú com 3 estados (FECHADO -> ABRINDO -> ABERTO). A animação de abertura usa 4 sprites
    (fechado, destravando, meio aberto, aberto) seguidos de um brilho/raios de recompensa.
    """
    # instante (s) em que cada frame de sprite começa durante a abertura
    INICIO_FRAMES = (0.0, 0.30, 0.60, 0.90)
    DURACAO_TOTAL = 1.6   # frames + brilho final
    # o sprite cobre o baú que já vem desenhado no Mapa_1.png
    TOPLEFT_SPRITE = (113, 127)

    def __init__(self, particulas):
        self.rect = pygame.Rect(113, 145, 42, 30)
        self.estado = EstadoBau.FECHADO
        self.particulas = particulas
        self.tempo = 0.0
        self.tremor = 0.0
        self._frame_anterior = 0
        self.frames = [carregar_imagem(f"assets/sprites/itens/bau_{i}.png", (42, 48), (148, 92, 50))
                       for i in range(4)]
        self.brilho = carregar_imagem("assets/sprites/efeitos/brilho.png", (48, 48), (255, 230, 140))

    def perto(self, hitbox_player):
        return self.rect.inflate(70, 40).colliderect(hitbox_player)

    def tentar_abrir(self, tem_chave):
        """Retorna "aberto_antes", "sem_chave" ou "abrindo"."""
        if self.estado != EstadoBau.FECHADO:
            return "aberto_antes"
        if not tem_chave:
            self.tremor = 0.35
            return "sem_chave"
        self.estado = EstadoBau.ABRINDO
        self.tempo = 0.0
        self._frame_anterior = 0
        return "abrindo"

    def _frame_atual(self):
        if self.estado == EstadoBau.FECHADO:
            return 0
        if self.estado == EstadoBau.ABERTO:
            return 3
        return max(i for i, ini in enumerate(self.INICIO_FRAMES) if self.tempo >= ini)

    def atualizar(self, dt):
        """Retorna True no instante em que a abertura termina."""
        self.tremor = max(0.0, self.tremor - dt)
        if self.estado != EstadoBau.ABRINDO:
            return False
        self.tempo += dt
        frame = self._frame_atual()
        if frame != self._frame_anterior:
            self._frame_anterior = frame
            Audio.tocar({1: "bau_rangido", 2: "bau_rangido", 3: "brilho"}[frame])
            self.particulas.emitir(self.rect.centerx, self.rect.top + 6, 10 if frame < 3 else 40,
                                   [(255, 230, 120), (255, 255, 200), (255, 190, 60)],
                                   velocidade=(50, 200), vida=(0.4, 1.0), tam=(2, 5), gravidade=140,
                                   angulo=(30, 150))
        if self.tempo >= self.DURACAO_TOTAL:
            self.estado = EstadoBau.ABERTO
            return True
        return False

    def desenhar(self, janela):
        deslocamento = int(3 * math.sin(self.tremor * 60)) if self.tremor > 0 else 0
        x, y = self.TOPLEFT_SPRITE
        janela.blit(self.frames[self._frame_atual()], (x + deslocamento, y))

        if self.estado == EstadoBau.ABRINDO and self.tempo > self.INICIO_FRAMES[3]:
            # halo + raios de luz subindo do baú durante o brilho final
            k = (self.tempo - self.INICIO_FRAMES[3]) / (self.DURACAO_TOTAL - self.INICIO_FRAMES[3])
            intensidade = math.sin(k * math.pi)
            centro = (self.rect.centerx, self.rect.top + 8)
            tam = int(48 + 130 * intensidade)
            halo = pygame.transform.scale(self.brilho, (tam, tam))
            janela.blit(halo, halo.get_rect(center=centro))
            raios = pygame.Surface((120, 120), pygame.SRCALPHA)
            for i in range(7):
                ang = math.radians(200 + i * 23 + self.tempo * 30)
                fim = (60 + math.cos(ang) * 58 * intensidade, 60 + math.sin(ang) * 58 * intensidade)
                pygame.draw.line(raios, (255, 240, 170, int(200 * intensidade)), (60, 60), fim, 3)
            janela.blit(raios, raios.get_rect(center=centro))
        elif self.estado == EstadoBau.ABERTO and random.random() < 0.04:
            # faíscas ocasionais: o baú permanece visualmente "vivo", mas aberto
            self.particulas.emitir(self.rect.centerx, self.rect.top + 4, 1, [(255, 230, 140)],
                                   velocidade=(10, 30), vida=(0.6, 1.0), tam=(2, 3), angulo=(70, 110),
                                   area=(12, 0))
