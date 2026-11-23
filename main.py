import asyncio

import pygame
from classes.systems.game_manager import GameManager
from classes.states.inicio_state import InicioState

pygame.init()

LARGURA = 1400
ALTURA = 760
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Hidden Way")


async def main():
    gerenciador = GameManager()
    gerenciador.mudar_estado(InicioState(gerenciador, LARGURA, ALTURA))

    relogio = pygame.time.Clock()
    rodando = True
    pygame.event.clear()

    while rodando:
        dt = relogio.tick(60) / 1000.0

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


if __name__ == "__main__":
    asyncio.run(main())