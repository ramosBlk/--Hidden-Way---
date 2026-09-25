import pygame


class Colisao:
    def __init__(self, largura=1400, altura=760, caminho_mascara=None):
        self.largura = largura
        self.altura = altura

        if caminho_mascara:
            self.mascara_superficie = pygame.image.load(caminho_mascara).convert()
        else:
            self.mascara_superficie = pygame.Surface((self.largura, self.altura))

            # Fundo PRETO (Não caminhável / Grama / Árvores / Cerca)
            self.mascara_superficie.fill((0, 0, 0))

            # Faixa da estrada de terra na tela de 1400x760
            self.areas_caminhaveis = [
                [
                    (0, 625),  # Canto superior esquerdo da estrada
                    (1400, 625),  # Canto superior direito da estrada
                    (1400, 710),  # Canto inferior direito da estrada
                    (0, 710)  # Canto inferior esquerdo da estrada
                ]
            ]

            # Desenha a estrada de terra em BRANCO (Caminhável)
            for area in self.areas_caminhaveis:
                pygame.draw.polygon(self.mascara_superficie, (255, 255, 255), area)

    def pode_andar(self, x, y):
        """
        Verifica se a posição dos pés (x, y) está sobre a estrada (BRANCO).
        """
        px = int(x)
        py = int(y)

        if 0 <= px < self.largura and 0 <= py < self.altura:
            cor = self.mascara_superficie.get_at((px, py))
            return cor.r > 200 and cor.g > 200 and cor.b > 200

        return False

    def desenhar_debug(self, janela):
        """
        Desenha a máscara transparente para testar se a faixa branca coincide com a terra.
        """
        mascara_alpha = self.mascara_superficie.copy()
        mascara_alpha.set_alpha(120)
        janela.blit(mascara_alpha, (0, 0))