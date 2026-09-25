import pygame
from classes.cenario import Cenario
from classes.player import Player

pygame.init()

LARGURA = 1400
ALTURA = 760

janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Hidden Way")

cenario = Cenario("assets/sprites/telas/Tela_inicio.png", largura=LARGURA, altura=ALTURA, velocidade=3.5)
player = Player(x=100, y=570)

# Limites da câmera na tela
LIMITE_DIREITO_TELA = 900
LIMITE_ESQUERDO_TELA = 300

relogio = pygame.time.Clock()
rodando = True

while rodando:
    relogio.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()

    # 1. Movimentação do personagem no mundo
    player.mover()

    # 2. Rolagem da Câmera / Cenário
    # Avançando (Ir para a direita)
    if player.x >= LIMITE_DIREITO_TELA and (teclas[pygame.K_d] or teclas[pygame.K_RIGHT]):
        player.x = LIMITE_DIREITO_TELA
        cenario.mover_cenario(player.velocidade, para_frente=True)

    # Voltando (Ir para a esquerda)
    elif player.x <= LIMITE_ESQUERDO_TELA and (teclas[pygame.K_a] or teclas[pygame.K_LEFT]) and cenario.distancia_percorrida > 0:
        player.x = LIMITE_ESQUERDO_TELA
        cenario.mover_cenario(player.velocidade, para_frente=False)

    # 3. Limites físicos para o jogador não sair da janela
    if player.x < 0:
        player.x = 0
    elif player.x > LARGURA - player.largura:
        player.x = LARGURA - player.largura

    # 4. Renderização
    cenario.desenhar(janela)
    player.desenhar(janela)

    pygame.display.flip()

pygame.quit()