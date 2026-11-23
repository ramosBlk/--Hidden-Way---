import asyncio

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


# Define o estado inicial do jogo (menu principal)
gerenciador.mudar_estado(MenuState(gerenciador, LARGURA, ALTURA))

        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                rodando = False

        gerenciador.tratar_eventos(eventos)
        gerenciador.atualizar(dt)

        janela.fill((0, 0, 0))
        gerenciador.desenhar(janela)

        pygame.display.flip()
        await asyncio.sleep(0)

    pygame.quit()

    if brilho_aplicado != Configuracoes.brilho:
        brilho_aplicado = Configuracoes.brilho
        alpha_brilho = round((100 - brilho_aplicado) / 100 * 220)
        sobreposicao_brilho.set_alpha(alpha_brilho)
    if brilho_aplicado < 100:
        janela.blit(sobreposicao_brilho, (0, 0))

    pygame.display.flip()

if __name__ == "__main__":
    asyncio.run(main())