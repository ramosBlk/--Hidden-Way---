import pygame
from classes.states.game_state import GameState
from classes.game_over import GameOver
from classes.systems.audio import Audio


class GameOverState(GameState):
    """
    Estado de Game Over.
    - fundo: último quadro do jogo (surface) para aparecer escurecido ao fundo.
    - reiniciar: função sem argumentos que devolve o estado da fase a reiniciar.
      Se não for informada, reinicia o Mapa 1.
    """

    def __init__(self, gerenciador, largura, altura, fundo=None, reiniciar=None, motivo="Você caiu no buraco!"):
        super().__init__(gerenciador)
        self.gerenciador = gerenciador
        self.largura = largura
        self.altura = altura
        self.fundo = fundo
        self.motivo = motivo
        self.reiniciar = reiniciar or self._reiniciar_mapa1
        self.tela_game_over = GameOver(largura=self.largura, altura=self.altura)
        Audio.tocar("game_over")

    def _reiniciar_mapa1(self):
        from classes.states.mapa1_state import Mapa1State
        return Mapa1State(self.gerenciador, self.largura, self.altura)

    def tratar_eventos(self, eventos):
        for evento in eventos:
            acao = self.tela_game_over.tratar_evento(evento)
            if acao == "tentar":
                Audio.tocar("clique")
                self.gerenciador.mudar_estado(self.reiniciar())
            elif acao == "menu":
                Audio.tocar("clique")
                from classes.states.inicio_state import InicioState
                self.gerenciador.mudar_estado(InicioState(self.gerenciador, self.largura, self.altura))

    def atualizar(self, dt=1 / 60):
        self.tela_game_over.atualizar(dt)

    def desenhar(self, janela):
        self.tela_game_over.desenhar(janela, fundo=self.fundo, subtitulo=self.motivo)
