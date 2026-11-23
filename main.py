import pygame
from classes.systems.game_manager import GameManager
from classes.states.menu_state import MenuState
from classes.systems.configuracoes import Configuracoes

pygame.init()
Configuracoes.carregar()

LARGURA = 1400
ALTURA = 760
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Hidden Way")
sobreposicao_brilho = pygame.Surface((LARGURA, ALTURA))
sobreposicao_brilho.fill((0, 0, 0))
brilho_aplicado = None

# Inicializa o Gerenciador de Estados
gerenciador = GameManager()

# Define o estado inicial do jogo (menu principal)
gerenciador.mudar_estado(MenuState(gerenciador, LARGURA, ALTURA))

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

    if brilho_aplicado != Configuracoes.brilho:
        brilho_aplicado = Configuracoes.brilho
        alpha_brilho = round((100 - brilho_aplicado) / 100 * 220)
        sobreposicao_brilho.set_alpha(alpha_brilho)
    if brilho_aplicado < 100:
        janela.blit(sobreposicao_brilho, (0, 0))

    pygame.display.flip()

pygame.quit()