import pygame


class Fade:
    """Fade de tela. modo "saida": tela -> cor (escurece); modo "entrada": cor -> tela (clareia)."""

    def __init__(self, largura, altura, duracao=0.8, modo="saida", cor=(0, 0, 0), alpha_max=255):
        self.duracao = max(0.001, duracao)
        self.modo = modo
        self.alpha_max = alpha_max
        self.tempo = 0.0
        self.superficie = pygame.Surface((largura, altura))
        self.superficie.fill(cor)

    @property
    def progresso(self):
        return min(1.0, self.tempo / self.duracao)

    @property
    def concluido(self):
        return self.tempo >= self.duracao

    @property
    def alpha(self):
        p = self.progresso
        return int(self.alpha_max * (p if self.modo == "saida" else 1 - p))

    def atualizar(self, dt):
        self.tempo += dt

    def desenhar(self, janela):
        a = self.alpha
        if a > 0:
            self.superficie.set_alpha(a)
            janela.blit(self.superficie, (0, 0))
