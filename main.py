import asyncio

import pygame

from classes.systems.game_manager import GameManager
from classes.states.menu_state import MenuState
from classes.systems.configuracoes import Configuracoes
from classes.systems.timing import FIXED_TIMESTEP, accumulate_frame_time

LARGURA = 1400
ALTURA = 760


async def main():
    pygame.init()
    Configuracoes.carregar()

    janela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Hidden Way")
    sobreposicao_brilho = pygame.Surface((LARGURA, ALTURA))
    sobreposicao_brilho.fill((0, 0, 0))
    brilho_aplicado = None
    gerenciador = GameManager()
    gerenciador.mudar_estado(MenuState(gerenciador, LARGURA, ALTURA))

    relogio = pygame.time.Clock()
    rodando = True
    acumulador = 0.0
    pygame.event.clear()

    while rodando:
        frame_delta = relogio.tick(60) / 1000.0
        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                rodando = False

        gerenciador.tratar_eventos(eventos)
        passos, acumulador = accumulate_frame_time(frame_delta, acumulador)
        for _ in range(passos):
            gerenciador.atualizar(FIXED_TIMESTEP)

        janela.fill((0, 0, 0))
        gerenciador.desenhar(janela)

        if brilho_aplicado != Configuracoes.brilho:
            brilho_aplicado = Configuracoes.brilho
            alpha_brilho = round((100 - brilho_aplicado) / 100 * 220)
            sobreposicao_brilho.set_alpha(alpha_brilho)
        if brilho_aplicado < 100:
            janela.blit(sobreposicao_brilho, (0, 0))

        pygame.display.flip()
        await asyncio.sleep(0)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())