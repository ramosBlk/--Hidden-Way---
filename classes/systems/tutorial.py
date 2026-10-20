import pygame

from classes.ui import desenhar_placa, texto_pixel

# (tecla, descrição)
CONTROLES = [
    ("A / D  ou  < >", "Andar para os lados"),
    ("W / S  ou  ^ v", "Subir / descer (só no menu)"),
    ("ESPAÇO", "Pular"),
    ("E", "Interagir (baú, árvore)"),
    ("R", "Tentar de novo (Game Over)"),
]

class Tutorial:
    """
    Tutorial ESTÁTICO exibido na tela inicial: controles e explicação das mecânicas.
    Não depende mais do progresso do jogador (sem instruções passo a passo).
    """

    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.concluido = True      # a árvore já pode ser usada desde o início
        self._painel = None

    def atualizar(self, player, cenario):
        pass  # estático

    def _montar_painel(self):
        painel = pygame.Surface((600, 300), pygame.SRCALPHA)
        painel.fill((0, 0, 0, 0))
        base = pygame.Surface(painel.get_size(), pygame.SRCALPHA)
        desenhar_placa(base, pygame.Rect(0, 40, 600, 310), (0, 220, 255), (32, 36, 44))
        base.set_alpha(125)
        painel.blit(base, (0, 0))

        # coluna esquerda: controles
        painel.blit(texto_pixel("CONTROLES", 14, (170, 220, 255), escala=2), (30, 56))
        for i, (tecla, desc) in enumerate(CONTROLES):
            y = 112 + i * 34
            cap = texto_pixel(tecla, 9, (255, 255, 255), escala=2)
            caixa = pygame.Rect(36, y - 3, 150, 28)
            pygame.draw.rect(painel, (50, 56, 70), caixa)
            pygame.draw.rect(painel, (150, 160, 180), caixa, 2)
            painel.blit(cap, cap.get_rect(center=caixa.center))
            painel.blit(texto_pixel(desc, 9, (225, 225, 230), escala=2), (200, y))


        return painel

    def desenhar(self, janela):
        if self._painel is None:
            self._painel = self._montar_painel()
        janela.blit(self._painel, self._painel.get_rect(midtop=(self.largura // 2, 9)))
