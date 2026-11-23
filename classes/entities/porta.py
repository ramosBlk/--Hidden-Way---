import math
import random
from enum import Enum

import pygame

from classes.systems.assets import carregar_imagem
from classes.systems.audio import Audio
from classes.systems.configuracoes import Configuracoes


class EstadoPorta(Enum):
    FECHADA = "fechada"
    ABRINDO = "abrindo"
    ABERTA = "aberta"


class Porta:
    """Porta de saída da fase: abre quando o jogador usa a chave do baú."""
    TEMPO_ABRINDO = 0.9

    def __init__(
        self,
        x,
        y_chao,
        particulas,
        mostrar_textura=True,
        intensidade_brilho=1.0,
        halo_anel=False,
    ):
        self.rect = pygame.Rect(0, 0, 60, 84)
        self.rect.midbottom = (x, y_chao)
        self.entrada = self.rect.inflate(-24, 0)
        self.mostrar_textura = mostrar_textura
        self.intensidade_brilho = intensidade_brilho
        self.halo_anel = halo_anel
        self.particulas = particulas
        self.estado = EstadoPorta.FECHADA
        self.tempo = 0.0
        self.brilho_extra = 0.0
        self.fechada = carregar_imagem("assets/sprites/itens/porta_0.png", (60, 84), (80, 70, 60))
        self.aberta = carregar_imagem("assets/sprites/itens/porta_1.png", (60, 84), (255, 240, 170))
        self.brilho = carregar_imagem("assets/sprites/efeitos/brilho.png", (48, 48), (255, 230, 140))
        self.superficie_halo_anel = self._criar_halo_anel() if halo_anel else None

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
        if not Configuracoes.brilhos_ativos():
            if not self.mostrar_textura:
                sprite = self.aberta if self.estado == EstadoPorta.ABERTA else self.fechada
                janela.blit(sprite, self.rect)
            return
        if self.halo_anel:
            self._desenhar_halo_anel(janela, intensidade)
            return

        pulsacao = 1 + (0.05 + 0.05 * (self.intensidade_brilho - 1)) * math.sin(self.tempo * 4)
        tam = int(
            (90 + 160 * self.brilho_extra)
            * intensidade
            * self.intensidade_brilho
            * pulsacao
        )
        if tam < 2:
            return
        halo = pygame.transform.scale(self.brilho, (tam, tam))
        destino = halo.get_rect(center=self.rect.center)
        for _ in range(max(1, math.ceil(self.intensidade_brilho))):
            janela.blit(halo, destino)

    @staticmethod
    def _criar_halo_anel():
        halo = pygame.Surface((180, 220), pygame.SRCALPHA)
        camadas = (
            ((255, 190, 75, 24), 0, 0, 28),
            ((255, 210, 95, 38), 12, 14, 20),
            ((255, 235, 150, 58), 24, 28, 10),
        )
        for cor, margem_x, margem_y, espessura in camadas:
            retangulo = pygame.Rect(
                margem_x,
                margem_y,
                halo.get_width() - 2 * margem_x,
                halo.get_height() - 2 * margem_y,
            )
            pygame.draw.ellipse(halo, cor, retangulo, width=espessura)
        return halo

    def _desenhar_halo_anel(self, janela, intensidade):
        if self.superficie_halo_anel is None:
            raise RuntimeError("A superfície do brilho em anel não foi inicializada.")

        pulsacao = 1 + 0.05 * math.sin(self.tempo * 4)
        escala = (1 + 0.18 * (self.intensidade_brilho - 1) + 0.12 * self.brilho_extra) * pulsacao
        tamanho = (
            int(self.superficie_halo_anel.get_width() * escala),
            int(self.superficie_halo_anel.get_height() * escala),
        )
        halo = pygame.transform.smoothscale(self.superficie_halo_anel, tamanho)
        halo.set_alpha(min(255, int((125 * intensidade + 40 * self.brilho_extra) * self.intensidade_brilho)))
        centro = (self.rect.centerx, self.rect.centery - 34)
        janela.blit(halo, halo.get_rect(center=centro))

    def desenhar(self, janela):
        if self.estado == EstadoPorta.FECHADA:
            if self.mostrar_textura:
                janela.blit(self.fechada, self.rect)
            else:
                self._halo(janela, 0.85)
        elif self.estado == EstadoPorta.ABRINDO:
            k = self.tempo / self.TEMPO_ABRINDO
            intensidade = k if self.mostrar_textura else 0.85 + 0.15 * k
            self._halo(janela, intensidade)
            if self.mostrar_textura:
                janela.blit(self.fechada, self.rect.move(random.randint(-2, 2), 0))
                aberta = self.aberta.copy()
                aberta.set_alpha(int(255 * k))
                janela.blit(aberta, self.rect)
        else:
            self._halo(janela, 1.0)
            if self.mostrar_textura:
                janela.blit(self.aberta, self.rect)
