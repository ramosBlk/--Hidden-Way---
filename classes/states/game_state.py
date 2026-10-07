class GameState:
    def __init__(self, gerenciador):
        self.gerenciador = gerenciador

    def tratar_eventos(self, eventos):
        """Processa eventos de teclado/mouse específicos deste estado."""
        pass

    def atualizar(self):
        """Atualiza a lógica e a física deste estado."""
        pass

    def desenhar(self, janela):
        """Renderiza os elementos gráficos deste estado."""
        pass