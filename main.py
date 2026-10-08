import pygame
from classes.systems.game_manager import GameManager
from classes.states.inicio_state import InicioState

pygame.init()

LARGURA = 1400
ALTURA = 760
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Hidden Way")

# Inicializa o Gerenciador de Estados
gerenciador = GameManager()

# Define o estado inicial do jogo (Tela Inicial / Tutorial)
gerenciador.mudar_estado(InicioState(gerenciador, LARGURA, ALTURA))

relogio = pygame.time.Clock()
rodando = True
pygame.event.clear()

while rodando:
    dt = relogio.tick(60) / 1000.0  # segundos desde o último quadro

    # Coleta de eventos globais
    eventos = pygame.event.get()
    for evento in eventos:
        if evento.type == pygame.QUIT:
            rodando = False

    # Delega eventos, atualizações e renderizações para o estado atual ativo
    gerenciador.tratar_eventos(eventos)
    gerenciador.atualizar(dt)

    janela.fill((0, 0, 0))
    gerenciador.desenhar(janela)

    pygame.display.flip()

pygame.quit()