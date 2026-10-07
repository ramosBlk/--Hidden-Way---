class GameManager:
    def __init__(self):
        self.estado_atual = None

    def mudar_estado(self, novo_estado):
        """Altera o estado atual do jogo."""
        self.estado_atual = novo_estado

    def tratar_eventos(self, eventos):
        if self.estado_atual:
            self.estado_atual.tratar_eventos(eventos)

    def atualizar(self):
        if self.estado_atual:
            self.estado_atual.atualizar()

    def desenhar(self, janela):
        if self.estado_atual:
            self.estado_atual.desenhar(janela)