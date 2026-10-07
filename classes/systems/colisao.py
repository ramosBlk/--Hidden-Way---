import pygame


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

    def tratar_colisao_plataforma(self, player, plataformas):
        """
        Gerencia a física de colisão vertical e horizontal do player com as plataformas do Mapa 1.
        """
        player_rect = pygame.Rect(player.x, player.y, player.largura, player.altura)

        # Movimento horizontal livre nas plataformas
        player.x += player.vel_x if hasattr(player, 'vel_x') else 0

        # Limites laterais da tela do Mapa 1
        if player.x < 0:
            player.x = 0
        elif player.x > self.largura - player.largura:
            player.x = self.largura - player.largura

        # Atualiza o rect após movimento horizontal
        player_rect.x = player.x

        # Colisão Vertical (Gravidade e Pulo)
        player.no_chao = False
        for plat in plataformas:
            if player_rect.colliderect(plat):
                if player.vel_y > 0:  # Caindo em cima da plataforma
                    player.y = plat.top - player.altura
                    player.vel_y = 0
                    player.no_chao = True
                    player_rect.y = player.y
                elif player.vel_y < 0:  # Batendo a cabeça por baixo
                    player.y = plat.bottom
                    player.vel_y = 0
                    player_rect.y = player.y

    def desenhar_debug(self, janela):
        mascara_alpha = self.mascara_superficie.copy()
        mascara_alpha.set_alpha(120)
        janela.blit(mascara_alpha, (0, 0))