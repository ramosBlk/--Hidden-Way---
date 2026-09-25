import pygame


class Cenario:
    def __init__(self, caminho_imagem, largura=1400, altura=760, velocidade=3.5):
        self.largura = largura
        self.altura = altura
        self.velocidade = velocidade

        # Carrega a imagem normal e a espelhada
        self.imagem_normal = pygame.image.load(caminho_imagem).convert()
        self.imagem_normal = pygame.transform.scale(self.imagem_normal, (self.largura, self.altura))
        self.imagem_espelhada = pygame.transform.flip(self.imagem_normal, True, False)

        # Posições X das duas imagens
        self.x1 = 0
        self.x2 = self.largura

        self.tipo1 = 'normal'
        self.tipo2 = 'espelhada'

        self.distancia_percorrida = 0
        self.parado = False

    def mover_cenario(self, velocidade=None, para_frente=True):
        """
        Move o cenário:
        - para_frente=True:  Avança o mapa (cenário vai para a esquerda)
        - para_frente=False: Volta o mapa (cenário vai para a direita)
        """
        if self.parado:
            return

        vel = velocidade if velocidade is not None else self.velocidade

        if para_frente:
            # Avançando no mapa
            self.x1 -= vel
            self.x2 -= vel
            self.distancia_percorrida += vel

            # Recicla imagens saindo pela esquerda
            if self.x1 <= -self.largura:
                self.x1 = self.x2 + self.largura
                self.tipo1 = 'normal' if self.tipo2 == 'espelhada' else 'espelhada'

            if self.x2 <= -self.largura:
                self.x2 = self.x1 + self.largura
                self.tipo2 = 'normal' if self.tipo1 == 'espelhada' else 'espelhada'
        else:
            # Voltando no mapa
            if self.distancia_percorrida > 0:
                self.x1 += vel
                self.x2 += vel
                self.distancia_percorrida -= vel

                # Impede que a distância percorrida fique negativa
                if self.distancia_percorrida < 0:
                    self.distancia_percorrida = 0

                # Recicla imagens saindo pela direita
                if self.x1 >= self.largura:
                    self.x1 = self.x2 - self.largura
                    self.tipo1 = 'normal' if self.tipo2 == 'espelhada' else 'espelhada'

                if self.x2 >= self.largura:
                    self.x2 = self.x1 - self.largura
                    self.tipo2 = 'normal' if self.tipo1 == 'espelhada' else 'espelhada'

    def desenhar(self, janela):
        img1 = self.imagem_normal if self.tipo1 == 'normal' else self.imagem_espelhada
        img2 = self.imagem_normal if self.tipo2 == 'normal' else self.imagem_espelhada

        janela.blit(img1, (int(self.x1), 0))
        janela.blit(img2, (int(self.x2), 0))