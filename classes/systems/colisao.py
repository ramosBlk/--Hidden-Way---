import math
import pygame

# Deslocamento máximo (em px) por sub-passo de movimento.
# Menor que a espessura das plataformas (5 px) para o player nunca "pular" por cima delas.
PASSO_MAXIMO = 4

class Colisao:
    def __init__(self, largura=1400, altura=760, caminho_mascara=None):
        self.largura = largura
        self.altura = altura

        if caminho_mascara:
            self.mascara_superficie = pygame.image.load(caminho_mascara).convert()
        else:
            self.mascara_superficie = pygame.Surface((self.largura, self.altura))
            self.mascara_superficie.fill((0, 0, 0))

            # Estrada de terra na tela inicial (Caminhável)
            self.areas_caminhaveis = [
                [
                    (0, 625),
                    (1400, 625),
                    (1400, 710),
                    (0, 710)
                ]
            ]

            for area in self.areas_caminhaveis:
                pygame.draw.polygon(self.mascara_superficie, (255, 255, 255), area)

    def pode_andar(self, x, y):
        """Verifica se a posição (x, y) está sobre a área livre na tela inicial."""
        px = int(x)
        py = int(y)

        if 0 <= px < self.largura and 0 <= py < self.altura:
            cor = self.mascara_superficie.get_at((px, py))
            return cor.r > 200 and cor.g > 200 and cor.b > 200

        return False

    def _sobrepoe(self, player, rect):
        """Testa a hitbox do player contra um retângulo usando float (sem arredondar a posição)."""
        esquerda = player.x + player.hitbox_offset_x
        return (esquerda < rect.right and esquerda + player.hitbox_largura > rect.left and
                player.y < rect.bottom and player.y + player.altura > rect.top)

    def tratar_colisao_plataforma(self, player, plataformas):
        """
        Move o player e resolve a colisão com plataformas e paredes do Mapa 1.
        Os eixos X e Y são tratados separadamente (permite deslizar pela parede) e o
        movimento é dividido em passos pequenos para não atravessar plataformas finas.
        """
        passos = max(1, math.ceil(max(abs(player.vel_x), abs(player.vel_y)) / PASSO_MAXIMO))
        passo_x = player.vel_x / passos
        passo_y = player.vel_y / passos

        player.no_chao = False
        for _ in range(passos):
            # --- Eixo X ---
            if passo_x != 0:
                # Retângulos em que o player já estava dentro são ignorados, para ele conseguir sair
                ja_dentro = [r for r in plataformas if self._sobrepoe(player, r)]
                player.x += passo_x

                for r in plataformas:
                    if r not in ja_dentro and self._sobrepoe(player, r):
                        if passo_x > 0:  # Bateu andando para a direita
                            player.x = r.left - player.hitbox_offset_x - player.hitbox_largura
                        else:  # Bateu andando para a esquerda
                            player.x = r.right - player.hitbox_offset_x
                        passo_x = 0
                        break

                # Limites laterais da tela do Mapa 1
                if player.x < 0:
                    player.x = 0
                elif player.x > self.largura - player.largura:
                    player.x = self.largura - player.largura

            # --- Eixo Y ---
            if passo_y != 0:
                ja_dentro = [r for r in plataformas if self._sobrepoe(player, r)]
                player.y += passo_y

                for r in plataformas:
                    if r not in ja_dentro and self._sobrepoe(player, r):
                        if passo_y > 0:  # Caindo em cima da plataforma
                            player.y = r.top - player.altura
                            player.no_chao = True
                        else:  # Batendo a cabeça por baixo
                            player.y = r.bottom
                        player.vel_y = 0
                        passo_y = 0
                        break

    def desenhar_debug(self, janela):
        mascara_alpha = self.mascara_superficie.copy()
        mascara_alpha.set_alpha(120)
        janela.blit(mascara_alpha, (0, 0))