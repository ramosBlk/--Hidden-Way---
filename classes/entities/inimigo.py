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
    Recebe três acertos de pedra antes de morrer; encostar nele causa dano ao jogador.
    """
    TIPOS = {
        "slime": dict(tamanho=(42, 21), velocidade=70, cor=(92, 190, 80), sprite="slime"),
        "slime_vermelho": dict(tamanho=(42, 21), velocidade=70, cor=(220, 65, 65), sprite="slime"),
        "morcego": dict(tamanho=(48, 24), velocidade=105, cor=(110, 70, 160)),
    }
    TEMPO_MORRENDO = 0.35
    VIDA_MAXIMA = 3

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
        self.vida = self.VIDA_MAXIMA
        self.particulas = particulas
        sprite = cfg.get("sprite", tipo)
        self.frames = [carregar_imagem(f"assets/sprites/inimigos/{sprite}_{i}.png",
                                       cfg["tamanho"], cfg["cor"]) for i in range(2)]
        if tipo == "slime_vermelho":
            self.frames = [self._tingir_slime_vermelho(frame) for frame in self.frames]

    @staticmethod
    def _tingir_slime_vermelho(imagem):
        tingida = imagem.copy()
        pixels = pygame.PixelArray(tingida)
        for x in range(tingida.get_width()):
            for y in range(tingida.get_height()):
                cor = tingida.unmap_rgb(pixels[x, y])
                if cor.g > cor.r * 1.15 and cor.g > cor.b * 1.1:
                    pixels[x, y] = (min(255, int(cor.g * 0.95)),
                                    int(cor.g * 0.18),
                                    int(cor.g * 0.14),
                                    cor.a)
        del pixels
        return tingida

    @property
    def eh_slime(self):
        return self.tipo.startswith("slime")

    @property
    def vivo(self):
        return self.estado == EstadoInimigo.VIVO

    @property
    def hitbox(self):
        if self.eh_slime:
            r = pygame.Rect(0, 0, self.largura - 8, self.altura + 9)
            r.midbottom = (int(self.x), int(self.y))
        else:
            r = pygame.Rect(0, 0, self.largura - 10, self.altura - 6)
            r.center = (int(self.x), int(self.y))
        return r

    def receber_dano(self):
        if not self.vivo:
            return False
        self.vida = max(0, self.vida - 1)
        h = self.hitbox
        if self.vida == 0:
            self.estado = EstadoInimigo.MORRENDO
            self.tempo_morte = 0.0
            Audio.tocar("inimigo_morre")
            quantidade = 16
        else:
            Audio.tocar("pedra_impacto")
            quantidade = 8
        self.particulas.emitir(h.centerx, h.centery, quantidade,
                               [self.cor, (255, 255, 255), (40, 40, 40)],
                               velocidade=(50, 180), vida=(0.3, 0.7), tam=(2, 5), gravidade=220)
        return True

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
        if not self.eh_slime:
            self.y = self.y_base + 32 * math.sin(self.tempo * 3)

    def desenhar(self, janela):
        if self.estado == EstadoInimigo.MORTO:
            return
        img = self.frames[int(self.tempo * (4 if self.eh_slime else 10)) % 2]
        if self.direcao < 0:
            img = pygame.transform.flip(img, True, False)
        if self.estado == EstadoInimigo.MORRENDO:  # achata e some
            k = self.tempo_morte / self.TEMPO_MORRENDO
            img = pygame.transform.scale(img, (int(self.largura * (1 + 0.4 * k)), max(2, int(self.altura * (1 - k)))))
            img.set_alpha(int(255 * (1 - k)))
        if self.eh_slime:
            janela.blit(img, img.get_rect(midbottom=(int(self.x), int(self.y))))
        else:
            janela.blit(img, img.get_rect(center=(int(self.x), int(self.y))))
        if self.vivo:
            self._desenhar_barra_vida(janela)

    def _desenhar_barra_vida(self, janela):
        barra = pygame.Rect(0, 0, self.largura - 8, 7)
        topo = self.y - self.altura if self.eh_slime else self.y - self.altura / 2
        barra.midbottom = (round(self.x), round(topo - 4))
        pygame.draw.rect(janela, (24, 20, 24), barra)
        pygame.draw.rect(janela, (100, 35, 40), barra.inflate(-2, -2))
        preenchimento = barra.inflate(-2, -2)
        preenchimento.width = round(preenchimento.width * self.vida / self.VIDA_MAXIMA)
        if preenchimento.width:
            pygame.draw.rect(janela, (94, 220, 108), preenchimento)
        pygame.draw.rect(janela, (210, 220, 190), barra, 1)
