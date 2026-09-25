import pygame


class GameOver:

    def __init__(self, largura=1400, altura=760):
        self.largura = largura
        self.altura = altura

        # Overlay sutil em tom vinho/escuro para harmonizar com o pôr do sol
        self.overlay = pygame.Surface((largura, altura), pygame.SRCALPHA)
        self.overlay.fill((25, 12, 28, 210))

        # Fontes do jogo
        self.fonte_titulo = pygame.font.SysFont("trebuchetms", 58, bold=True)
        self.fonte_motivo = pygame.font.SysFont("arial", 20)
        self.fonte_instrucao = pygame.font.SysFont("trebuchetms", 22, bold=True)

        # Cores temáticas (Pôr do sol / Terracota)
        self.cor_borda_ext = (180, 70, 50)
        self.cor_borda_int = (230, 160, 60)
        self.cor_titulo = (235, 65, 50)
        self.cor_texto = (235, 225, 220)
        self.cor_destaque = (255, 210, 80)

    def desenhar(
        self,
        janela,
        motivo="Você errou o código 3 vezes! Papa Figo perdeu a paciência e te derrotou.",
    ):
        """Desenha a tela de Game Over por cima do cenário atual."""
        # 1. Aplica a camada escura no fundo
        janela.blit(self.overlay, (0, 0))

        # 2. Configura o Painel Central
        largura_painel = min(900, self.largura - 100)
        altura_painel = 320
        x_painel = (self.largura - largura_painel) // 2
        y_painel = (self.altura - altura_painel) // 2

        # Fundo do Painel
        painel_fundo = pygame.Surface(
            (largura_painel, altura_painel), pygame.SRCALPHA
        )
        painel_fundo.fill((15, 10, 18, 235))
        janela.blit(painel_fundo, (x_painel, y_painel))

        # Moldura Estilizada
        pygame.draw.rect(
            janela,
            self.cor_borda_ext,
            (x_painel, y_painel, largura_painel, altura_painel),
            4,
        )
        pygame.draw.rect(
            janela,
            self.cor_borda_int,
            (
                x_painel + 6,
                y_painel + 6,
                largura_painel - 12,
                altura_painel - 12,
            ),
            2,
        )

        # 3. Título "GAME OVER"
        txt_titulo = self.fonte_titulo.render("GAME OVER", True, self.cor_titulo)
        rect_titulo = txt_titulo.get_rect(
            center=(self.largura // 2, y_painel + 70)
        )
        janela.blit(txt_titulo, rect_titulo)

        # Divisória
        pygame.draw.line(
            janela,
            self.cor_borda_int,
            (x_painel + 40, y_painel + 120),
            (x_painel + largura_painel - 40, y_painel + 120),
            2,
        )

        # 4. Mensagem de Motivo
        txt_motivo = self.fonte_motivo.render(motivo, True, self.cor_texto)
        rect_motivo = txt_motivo.get_rect(
            center=(self.largura // 2, y_painel + 165)
        )
        janela.blit(txt_motivo, rect_motivo)

        # 5. Instrução para reiniciar
        txt_instrucao = self.fonte_instrucao.render(
            "Pressione  [ R ]  para reiniciar a jornada",
            True,
            self.cor_destaque,
        )
        rect_instrucao = txt_instrucao.get_rect(
            center=(self.largura // 2, y_painel + 245)
        )
        janela.blit(txt_instrucao, rect_instrucao)