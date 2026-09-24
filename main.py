import os
import pygame

pygame.init()

# Definindo larguras e alturas em variáveis para facilitar a manutenção
LARGURA = 800
ALTURA = 600

# Tamanho da Janela
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Hidden Way")

# Caminho do cenário
caminho_imagem = os.path.join('assets', 'sprites', 'telas','Tela.png')
imagem_original = pygame.image.load(caminho_imagem)

# Caminho do personagem (corrigido o nome da pasta 'personagem_principal')
caminho_imagem_player = os.path.join('assets', 'sprites', 'personagem_principal', 'rotations' ,'south-east.png')
imagem_player = pygame.image.load(caminho_imagem_player)

# Redimensiona o cenário para o tamanho da janela
imagem_principal = pygame.transform.scale(imagem_original, (LARGURA, ALTURA))

# Posição inicial do personagem (X, Y)
pos_x = 50
pos_y = 520

loop = True
# Loop principal do jogo
while loop:
    for event in pygame.event.get():  # Evento de Fechar a Janela
        if event.type == pygame.QUIT:
            loop = False

    # 1. Desenha o fundo/cenário primeiro
    janela.blit(imagem_principal, (0, 0))

    # 2. Desenha o personagem por cima do fundo
    janela.blit(imagem_player, (pos_x, pos_y))

    # Atualiza a tela
    pygame.display.update()

pygame.quit()