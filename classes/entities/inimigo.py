import math
from enum import Enum

import pygame

from classes.systems.assets import carregar_imagem
from classes.systems.audio import Audio


class EstadoInimigo(Enum):
    VIVO = "vivo"
    MORRENDO = "morrendo"   # achatado, some em instantes
    MORTO = "morto"


class Inimigo:
    """
    Inimigo que patrulha entre x_min e x_max.
      - "slime": anda no chão (y = y do chão).
      - "morcego": voa ondulando em torno de y (y = altura base do voo).
    O player o derrota pulando em cima (pisão); qualquer outro contato mata o player.
    """
    TIPOS = {
        "slime": dict(tamanho=(42, 21), velocidade=70, cor=(92, 190, 80)),
        "morcego": dict(tamanho=(48, 24), velocidade=105, cor=(110, 70, 160)),
    }
    TEMPO_MORRENDO = 0.35

    def __init__(self, tipo, x_min, x_max, y, particulas):
        cfg = self.TIPOS[tipo]
        self.tipo = tipo
        self.x_min, self.x_max = x_min, x_max
        self.largura, self.altura = cfg["tamanho"]
        self.velocidade = cfg["velocidade"]
        self.cor = cfg["cor"]
        self.x = float(x_min)          # centro
        self.y_base = float(y)         # slime: chão | morcego: centro do voo
        self.y = self.y_base
        self.direcao = 1
        self.tempo = 0.0
        self.estado = EstadoInimigo.VIVO
        self.tempo_morte = 0.0
        self.particulas = particulas
        self.frames = [carregar_imagem(f"assets/sprites/inimigos/{tipo}_{i}.png", cfg["tamanho"], self.cor)
                       for i in range(2)]

    @property
    def vivo(self):
        return self.estado == EstadoInimigo.VIVO

    @property
    def hitbox(self):
        """Hitbox um pouco menor que o sprite (mais justo para o jogador)."""
        r = pygame.Rect(0, 0, self.largura - 10, self.altura - 6)
        if self.tipo == "slime":
            r.midbottom = (int(self.x), int(self.y))
        else:
            r.center = (int(self.x), int(self.y))
        return r

    def pisado_por(self, hitbox_player, vel_y_player):
        """True se o player está caindo sobre a parte de cima do inimigo."""
        return vel_y_player > 0 and hitbox_player.bottom - self.hitbox.top <= 22

    def derrotar(self):
        self.estado = EstadoInimigo.MORRENDO
        self.tempo_morte = 0.0
        Audio.tocar("pisao")
        h = self.hitbox
        self.particulas.emitir(h.centerx, h.centery, 16, [self.cor, (255, 255, 255), (40, 40, 40)],
                               velocidade=(50, 180), vida=(0.3, 0.7), tam=(2, 5), gravidade=300)

    def atualizar(self, dt):
        self.tempo += dt
        if self.estado == EstadoInimigo.MORRENDO:
            self.tempo_morte += dt
            if self.tempo_morte >= self.TEMPO_MORRENDO:
                self.estado = EstadoInimigo.MORTO
            return
        if self.estado == EstadoInimigo.MORTO:
            return
        self.x += self.direcao * self.velocidade * dt
        if self.x >= self.x_max:
            self.x, self.direcao = self.x_max, -1
        elif self.x <= self.x_min:
            self.x, self.direcao = self.x_min, 1
        if self.tipo == "morcego":
            self.y = self.y_base + 32 * math.sin(self.tempo * 3)

    def desenhar(self, janela):
        if self.estado == EstadoInimigo.MORTO:
            return
        img = self.frames[int(self.tempo * (10 if self.tipo == "morcego" else 4)) % 2]
        if self.direcao < 0:
            img = pygame.transform.flip(img, True, False)
        if self.estado == EstadoInimigo.MORRENDO:  # achata e some
            k = self.tempo_morte / self.TEMPO_MORRENDO
            img = pygame.transform.scale(img, (int(self.largura * (1 + 0.4 * k)), max(2, int(self.altura * (1 - k)))))
            img.set_alpha(int(255 * (1 - k)))
        if self.tipo == "slime":
            janela.blit(img, img.get_rect(midbottom=(int(self.x), int(self.y))))
        else:
            janela.blit(img, img.get_rect(center=(int(self.x), int(self.y))))
