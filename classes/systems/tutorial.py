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

MECANICAS = [
    "FASE 1: ache a CHAVE, abra o BAÚ",
    "com [E] e entre na CAVERNA.",
    "FASES 2 A 5: pegue TODAS as chaves",
    "para destrancar a PORTA de saída.",
    "Pule EM CIMA dos inimigos para",
    "derrotá-los. Tocar neles = Game Over.",
    "Cuidado com ESPINHOS e BURACOS!",
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
        painel = pygame.Surface((960, 330), pygame.SRCALPHA)
        painel.fill((0, 0, 0, 0))
        base = pygame.Surface(painel.get_size(), pygame.SRCALPHA)
        desenhar_placa(base, pygame.Rect(0, 0, 944, 314), (160, 130, 50), (24, 26, 34))
        base.set_alpha(225)
        painel.blit(base, (0, 0))

        titulo = texto_pixel("COMO JOGAR", 14, (255, 214, 74), escala=3, sombra=(70, 40, 10))
        painel.blit(titulo, titulo.get_rect(midtop=(472, 18)))

        # coluna esquerda: controles
        painel.blit(texto_pixel("CONTROLES", 9, (170, 220, 255), escala=2), (36, 76))
        for i, (tecla, desc) in enumerate(CONTROLES):
            y = 112 + i * 34
            cap = texto_pixel(tecla, 9, (255, 255, 255), escala=2)
            caixa = pygame.Rect(36, y - 3, 150, 26)
            pygame.draw.rect(painel, (50, 56, 70), caixa)
            pygame.draw.rect(painel, (150, 160, 180), caixa, 2)
            painel.blit(cap, cap.get_rect(center=caixa.center))
            painel.blit(texto_pixel(desc, 9, (225, 225, 230), escala=2), (200, y))

        # coluna direita: mecânicas
        painel.blit(texto_pixel("COMO FUNCIONA", 9, (170, 255, 190), escala=2), (500, 76))
        for i, linha in enumerate(MECANICAS):
            painel.blit(texto_pixel(linha, 9, (235, 235, 225), escala=2), (500, 112 + i * 24))

        rodape = texto_pixel("Chegue até a ÁRVORE GIGANTE à direita e pressione [E] para começar!",
                             9, (255, 244, 170), escala=2)
        painel.blit(rodape, rodape.get_rect(midbottom=(472, 300)))
        return painel

    def desenhar(self, janela):
        if self._painel is None:
            self._painel = self._montar_painel()
        janela.blit(self._painel, self._painel.get_rect(midtop=(self.largura // 2, 12)))
