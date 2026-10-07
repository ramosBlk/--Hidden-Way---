from classes.systems.cenario import Cenario
from classes.entities.player import Player
from classes.states.game_state import GameState


class Mapa1State(GameState):
    def __init__(self, gerenciador, largura, altura):
        super().__init__(gerenciador)
        self.gerenciador = gerenciador
        self.largura = largura
        self.altura = altura

        # Player redimensionado e posicionado no início do Mapa 1
        self.player = Player(x=835, y=668, escala=0.6)

        # Cenário do Mapa 1 (plataformas)
        self.cenario = Cenario(
            caminho_imagem="assets/sprites/telas/Mapa_1.png",
            largura=self.largura,
            altura=self.altura,
            eh_plataforma=True
        )

    def tratar_eventos(self, eventos):
        # Aqui podemos tratar eventos específicos do Mapa 1 se necessário
        pass

    def atualizar(self):
        # Atualiza a movimentação com gravidade ativada e colisão com as plataformas
        self.player.atualizar_movimento(gravidade_ativada=True, plataformas=self.cenario.plataformas)

        # Se cair da tela, muda para o estado de Game Over
        if self.player.y > self.altura:
            from classes.states.game_over_state import GameOverState  # Vamos criar a seguir
            self.gerenciador.mudar_estado(GameOverState(self.gerenciador, self.largura, self.altura))

    def desenhar(self, janela):
        self.cenario.desenhar(janela)
        self.player.desenhar(janela)