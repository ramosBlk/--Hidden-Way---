import os
import pygame

class Player:
    def __init__(self, x=50, y=520):
        caminho_imagem = os.path.join(
            "assets",
            "sprites",
            "personagem_principal",
            "rotations",
            "south-east.png"
        )
        self.imagem = pygame.image.load(caminho_imagem)
        self.imagem = pygame.transform.scale(self.imagem, (64, 64))

        self.x = x
        self.y = y
        self.velocidade = 0.2

    def desenhar(self, janela):
        janela.blit(self.imagem, (self.x, self.y))

    def mover(self):
        teclas = pygame.key.get_pressed()

        # Esquerda (A)
        if teclas[pygame.K_a]:
            self.x -= self.velocidade
        # Direita (D)
        if teclas[pygame.K_d]:
            self.x += self.velocidade
        # Cima (W)
        if teclas[pygame.K_w]:
            self.y -= self.velocidade
        # Baixo (S)
        if teclas[pygame.K_s]:
            self.y += self.velocidade