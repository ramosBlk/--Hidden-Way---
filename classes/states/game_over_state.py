import pygame
from classes.states.game_state import GameState
from classes.game_over import GameOver  # Importa a sua classe de arte/desenho


class GameOverState(GameState):
    def __init__(self, gerenciador, largura, altura):
        super().__init__(gerenciador)
        self.gerenciador = gerenciador
        self.largura = largura
        self.altura = altura

        # Instancia a sua classe de visual de Game Over
        self.tela_game_over = GameOver(largura=self.largura, altura=self.altura)

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                # Pressionar R ou ENTER recomeça o jogo voltando para o Mapa 1
                if evento.key == pygame.K_r or evento.key == pygame.K_RETURN:
                    from classes.states.mapa1_state import Mapa1State
                    self.gerenciador.mudar_estado(Mapa1State(self.gerenciador, self.largura, self.altura))

    def atualizar(self):
        pass

    def desenhar(self, janela):
        # Primeiro desenha o fundo do Mapa 1 para que o painel apareça por cima congelando a cena
        # (Ou pode deixar apenas a sua tela de Game Over renderizada)
        self.tela_game_over.desenhar(janela, motivo="Queda")