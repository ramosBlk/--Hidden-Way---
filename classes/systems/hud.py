import math

import pygame

from classes.systems.assets import carregar_imagem
from classes.ui import texto_pixel, desenhar_placa


class Hud:
    """Interface de jogo: ícone da chave e avisos temporários (feedback textual)."""

    # Centro do ícone da chave na tela (a chave coletada "voa" até aqui)
    POS_CHAVE = (700, 40)

    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.icone_chave = carregar_imagem("assets/sprites/itens/chave.png", (39, 21), (255, 214, 74))
        self.avisos = []          # [texto, tempo_restante, duracao, cor]
        self.pulso_chave = 0.0    # animação rápida quando o ícone "recebe" a chave

    def avisar(self, texto, duracao=2.2, cor=(255, 244, 170)):
        # evita empilhar o mesmo aviso repetido
        for a in self.avisos:
            if a[0] == texto:
                a[1] = a[2] = duracao
                return
        self.avisos.append([texto, duracao, duracao, cor])

    def chave_recebida(self):
        self.pulso_chave = 0.5

    def atualizar(self, dt):
        for a in self.avisos:
            a[1] -= dt
        self.avisos = [a for a in self.avisos if a[1] > 0]
        self.pulso_chave = max(0.0, self.pulso_chave - dt)

    def desenhar_contador(self, janela, atual, total):
        """Contador de chaves das fases genéricas: ícone + atual/total."""
        cx, cy = self.POS_CHAVE
        placa = pygame.Rect(0, 0, 190, 44)
        placa.center = (cx + 50, cy)
        completo = atual >= total
        desenhar_placa(janela, placa, (90, 190, 110) if completo else (160, 130, 50), (30, 28, 24))
        escala = 1 + 0.5 * math.sin(self.pulso_chave / 0.5 * math.pi) if self.pulso_chave > 0 else 1
        icone = pygame.transform.scale(self.icone_chave, (int(39 * escala), int(21 * escala)))
        janela.blit(icone, icone.get_rect(center=(cx - 25, cy)))
        cor = (170, 255, 190) if completo else (255, 230, 120)
        janela.blit(texto_pixel(f"{atual}/{total}", 9, cor, escala=2), (cx + 6, cy - 9))

    def desenhar(self, janela, mostrar_chave):
        if mostrar_chave:
            escala = 1 + 0.5 * math.sin(self.pulso_chave / 0.5 * math.pi) if self.pulso_chave > 0 else 1
            cx, cy = self.POS_CHAVE
            placa = pygame.Rect(0, 0, 170, 44)
            placa.center = (cx + 40, cy)
            desenhar_placa(janela, placa, (160, 130, 50), (30, 28, 24))
            icone = pygame.transform.scale(self.icone_chave, (int(39 * escala), int(21 * escala)))
            janela.blit(icone, icone.get_rect(center=(cx - 25, cy)))
            janela.blit(texto_pixel("CHAVE", 9, (255, 230, 120), escala=2), (cx + 6, cy - 9))

        y = 120
        for texto, restante, duracao, cor in self.avisos:
            alpha = int(255 * min(1.0, restante / 0.4, (duracao - restante) / 0.15 + 0.01))
            txt = texto_pixel(texto, 10, cor, escala=3).copy()
            txt.set_alpha(alpha)
            janela.blit(txt, txt.get_rect(center=(self.largura // 2, y)))
            y += 44
