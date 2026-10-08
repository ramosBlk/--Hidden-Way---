from classes.states.game_state import GameState
from classes.fase_completa import FaseCompleta
from classes.systems.audio import Audio


class FaseCompletaState(GameState):
    """
    Tela "FASE COMPLETA!". Ao clicar em CONTINUAR carrega o estado devolvido por `proxima_fase`
    (função sem argumentos). Se ela for None, volta ao menu inicial (fim da demonstração).
    """

    def __init__(self, gerenciador, largura, altura, fundo=None, proxima_fase=None,
                 titulo="FASE COMPLETA!", subtitulo="Você desbloqueou a próxima fase!"):
        super().__init__(gerenciador)
        self.largura = largura
        self.altura = altura
        self.fundo = fundo
        self.proxima_fase = proxima_fase
        self.titulo = titulo
        self.subtitulo = subtitulo
        self.tela = FaseCompleta(largura, altura)
        Audio.tocar("vitoria")

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if self.tela.tratar_evento(evento):
                Audio.tocar("clique")
                if self.proxima_fase:
                    self.gerenciador.mudar_estado(self.proxima_fase())
                else:
                    from classes.states.inicio_state import InicioState
                    self.gerenciador.mudar_estado(InicioState(self.gerenciador, self.largura, self.altura))
                return

    def atualizar(self, dt=1 / 60):
        self.tela.atualizar(dt)

    def desenhar(self, janela):
        self.tela.desenhar(janela, self.fundo, self.titulo, self.subtitulo)
