import math
from enum import Enum

import pygame

from classes.systems.assets import carregar_imagem


class EstadoChave(Enum):
    NO_MAPA = "no_mapa"
    VOANDO = "voando"      # animação de coleta: sobe e voa até o ícone da HUD
    COLETADA = "coletada"


class Chave:
    """Item coletável. Só pode ser coletado uma vez (o estado deixa de ser NO_MAPA)."""
    TEMPO_SUBIDA = 0.25
    TEMPO_VOO = 0.55

    def __init__(self, x, y, particulas):
        self.centro = pygame.Vector2(x, y)
        self.hitbox = pygame.Rect(0, 0, 36, 36)
        self.hitbox.center = (x, y)
        self.estado = EstadoChave.NO_MAPA
        self.particulas = particulas
        self.tempo = 0.0
        self.tempo_coleta = 0.0
        self.destino = pygame.Vector2(0, 0)
        self.pos_voo = pygame.Vector2(x, y)
        self.sprite = carregar_imagem("assets/sprites/itens/chave.png", (39, 21), (255, 214, 74))
        self.brilho = carregar_imagem("assets/sprites/efeitos/brilho.png", (48, 48), (255, 230, 140))

    @property
    def voando(self):
        return self.estado == EstadoChave.VOANDO

    def coletar(self, destino_hud):
        """Inicia a coleta. Retorna False se a chave já foi coletada."""
        if self.estado != EstadoChave.NO_MAPA:
            return False
        self.estado = EstadoChave.VOANDO
        self.destino = pygame.Vector2(destino_hud)
        self.tempo_coleta = 0.0
        self.particulas.emitir(self.centro.x, self.centro.y, 26,
                               [(255, 230, 120), (255, 255, 200), (255, 190, 60)],
                               velocidade=(60, 190), vida=(0.4, 0.9), tam=(2, 5), gravidade=120)
        return True

    def atualizar(self, dt):
        """Retorna True no instante em que a chave chega ao ícone da HUD."""
        self.tempo += dt
        if self.estado != EstadoChave.VOANDO:
            return False
        self.tempo_coleta += dt
        t = self.tempo_coleta
        if t < self.TEMPO_SUBIDA:  # pequena elevação
            k = t / self.TEMPO_SUBIDA
            self.pos_voo = self.centro + pygame.Vector2(0, -28 * math.sin(k * math.pi / 2))
        else:  # voa (ease-in) até o ícone da HUD, deixando um rastro de brilho
            k = min(1.0, (t - self.TEMPO_SUBIDA) / self.TEMPO_VOO)
            origem = self.centro + pygame.Vector2(0, -28)
            self.pos_voo = origem.lerp(self.destino, k * k)
            self.particulas.emitir(self.pos_voo.x, self.pos_voo.y, 2, [(255, 230, 120), (255, 255, 210)],
                                   velocidade=(10, 40), vida=(0.2, 0.4), tam=(2, 3))
            if k >= 1.0:
                self.estado = EstadoChave.COLETADA
                return True
        return False

    def desenhar(self, janela):
        if self.estado == EstadoChave.COLETADA:
            return
        if self.estado == EstadoChave.NO_MAPA:
            pos = (self.centro.x, self.centro.y + 4 * math.sin(self.tempo * 3))
            escala_halo = 1.0 + 0.15 * math.sin(self.tempo * 5)
        else:
            pos = self.pos_voo
            escala_halo = 1.4
        tam_halo = int(48 * escala_halo * 1.3)
        halo = pygame.transform.scale(self.brilho, (tam_halo, tam_halo))
        janela.blit(halo, halo.get_rect(center=(int(pos[0]), int(pos[1]))))
        janela.blit(self.sprite, self.sprite.get_rect(center=(int(pos[0]), int(pos[1]))))
