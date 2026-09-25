import os
import pygame

from classes.player import Player

pygame.init()

LARGURA = 1400
ALTURA = 760

janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Hidden Way")

player = Player()

caminho_imagem = os.path.join(
    "assets", "sprites", "telas", "Tela_inicio.png"
)
imagem_original = pygame.image.load(caminho_imagem)
imagem_principal = pygame.transform.scale(imagem_original, (LARGURA, ALTURA))

loop = True

while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False

    janela.blit(imagem_principal, (0, 0))

    # Agora quem desenha o personagem é a própria classe Player
    player.desenhar(janela)
    player.mover()
    pygame.display.update()

pygame.quit()