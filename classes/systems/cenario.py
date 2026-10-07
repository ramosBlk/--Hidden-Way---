import pygame


class Cenario:
    def __init__(self, caminho_imagem, caminho_segunda_imagem=None, largura=1400, altura=760, velocidade=3.5, eh_plataforma=False):
        self.largura = largura
        self.altura = altura
        self.velocidade = velocidade
        self.eh_plataforma = eh_plataforma

        img_original = pygame.image.load(caminho_imagem).convert()
        self.imagem_1_esquerda = pygame.transform.scale(img_original, (self.largura, self.altura))
        self.imagem_1_direita = pygame.transform.flip(self.imagem_1_esquerda, True, False)

        if caminho_segunda_imagem:
            self.imagem_2 = pygame.image.load(caminho_segunda_imagem).convert()
            self.imagem_2 = pygame.transform.scale(self.imagem_2, (self.largura, self.altura))
        else:
            self.imagem_2 = self.imagem_1_esquerda

        self.x1 = 0
        self.x2 = self.largura

        self.distancia_percorrida = 0
        self.parado = False
        self.limite_maximo_distancia = largura

        # Lista de plataformas do Mapa 1 (caso eh_plataforma seja True)
        self.plataformas = [
            pygame.Rect(126, 725, 848, 5),
            pygame.Rect(-8, 620, 162, 5),
            pygame.Rect(400, 448, 267, 9),
            pygame.Rect(261, 537, 138, 5),
            pygame.Rect(234, 347, 36, 5),
            pygame.Rect(-31, 179, 256, 5),
            pygame.Rect(-41, 449, 258, 5),
            pygame.Rect(335, 313, 57, 5),
            pygame.Rect(680, 329, 50, 5),
            pygame.Rect(508, 248, 44, 5),
            pygame.Rect(799, 362, 42, 5),
            pygame.Rect(642, 180, 257, 5),
            pygame.Rect(587, 213, 26, 5),
            pygame.Rect(924, 160, 170, 5),
            pygame.Rect(1208, 233, 218, 5),
            pygame.Rect(1089, 332, 62, 7),
            pygame.Rect(912, 381, 29, 5),
            pygame.Rect(1061, 633, 52, 5),
            pygame.Rect(1184, 560, 308, 5),
            pygame.Rect(1258, 435, 172, 5),
        ]

    def mover(self, direcao_frente, player, tutorial):
        """Gerencia o movimento horizontal do player e rolagem do cenário na tela inicial."""
        if direcao_frente:  # Andando para a direita (D)
            if tutorial.passo_atual < 4:
                if player.x >= 900:
                    player.x = 900
                else:
                    player.x += player.velocidade
            else:
                if self.distancia_percorrida >= self.limite_maximo_distancia:
                    if player.x < self.largura - player.largura - 50:
                        player.x += player.velocidade
                else:
                    if player.x >= 900:
                        self.mover_cenario_lateral(velocidade=player.velocidade, para_frente=True)
                        player.x = 900
                    else:
                        player.x += player.velocidade
        else:  # Andando para a esquerda (A)
            if player.x <= 300 and self.distancia_percorrida > 0:
                self.mover_cenario_lateral(velocidade=player.velocidade, para_frente=False)
                player.x = 300
            else:
                player.x -= player.velocidade

    def mover_cenario_lateral(self, velocidade, para_frente=True):
        vel = velocidade if velocidade is not None else self.velocidade
        if para_frente:
            if self.distancia_percorrida < self.limite_maximo_distancia:
                self.x1 -= vel
                self.x2 -= vel
                self.distancia_percorrida += vel
        else:
            if self.distancia_percorrida > 0:
                self.x1 += vel
                self.x2 += vel
                self.distancia_percorrida -= vel

    def desenhar(self, janela):
        if self.eh_plataforma:
            janela.blit(self.imagem_1_esquerda, (0, 0))
        else:
            janela.blit(self.imagem_1_direita, (int(self.x1), 0))
            janela.blit(self.imagem_2, (int(self.x2), 0))