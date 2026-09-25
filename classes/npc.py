import os
import pygame


class NPC:
    def __init__(self, x_mundo, y_mundo, caminho_imagem=None, fala_puzzle=""):
        """
        x_mundo, y_mundo: Posição fixa do NPC no mapa/mundo.
        """
        self.x_mundo = x_mundo
        self.y_mundo = y_mundo
        self.largura = 96
        self.altura = 96

        # Se não for passado um caminho específico, usa por defeito o south.png do personagem_secundario
        if caminho_imagem is None:
            caminho_imagem = os.path.join(
                "assets",
                "sprites",
                "personagem_secundario",
                "rotations",
                "south-west.png"
            )

        self.imagem = pygame.image.load(caminho_imagem).convert_alpha()
        self.imagem = pygame.transform.scale(
            self.imagem, (self.largura, self.altura)
        )

        self.fala_puzzle = fala_puzzle
        self.raio_interacao = 110  # Distância máxima para interagir
        self.proximo = False

    def atualizar(self, player_x, player_y, cenario_distancia):
        """Calcula a posição na tela e verifica a proximidade com o jogador."""
        x_tela = self.x_mundo - cenario_distancia
        y_tela = self.y_mundo

        centro_player_x = player_x + (self.largura / 2)
        centro_player_y = player_y + (self.altura / 2)

        centro_npc_x = x_tela + (self.largura / 2)
        centro_npc_y = y_tela + (self.altura / 2)

        distancia = (
            (centro_player_x - centro_npc_x) ** 2
            + (centro_player_y - centro_npc_y) ** 2
        ) ** 0.5

        self.proximo = distancia <= self.raio_interacao

    def desenhar(self, janela, cenario_distancia):
        x_tela = self.x_mundo - cenario_distancia
        y_tela = self.y_mundo

        # Desenha apenas se estiver visível no ecrã
        if -self.largura <= x_tela <= janela.get_width():
            janela.blit(self.imagem, (int(x_tela), int(y_tela)))

            # Indicador visual para interagir
            if self.proximo:
                fonte = pygame.font.SysFont("arial", 18, bold=True)
                indicador = fonte.render("[E] Falar", True, (255, 255, 255))
                janela.blit(indicador, (int(x_tela + 10), int(y_tela - 25)))