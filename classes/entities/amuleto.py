import pygame

from classes.entities.chave import Chave


class Amuleto(Chave):
    """Fragmento pixelado que se encaixa no amuleto completo da HUD."""

    LARGURA_GRADE = 18
    ALTURA_GRADE = 12
    FAIXA_GRADE = 6
    TAMANHO_PIXEL = 3
    CONTORNO = (24, 31, 57)
    CORES = (
        ((58, 204, 221), (35, 143, 184), (164, 244, 246)),
        ((73, 147, 244), (43, 95, 190), (211, 240, 255)),
        ((79, 205, 176), (39, 139, 128), (185, 255, 221)),
    )

    def __init__(self, x, y, particulas, indice=0):
        super().__init__(x, y, particulas)
        self.indice = indice
        self.cores = [self.CORES[indice][0], self.CORES[indice][2], self.CORES[indice][1]]
        self.sprite = self.criar_sprite(indice)

    @staticmethod
    def criar_sprite(indice, tamanho_pixel=3):
        """Desenha uma das três peças complementares em baixa resolução."""
        if indice not in range(3):
            raise ValueError("O índice do fragmento deve ser 0, 1 ou 2.")

        linhas = (
            (7, 10), (6, 11), (5, 12), (4, 13), (3, 14), (2, 15),
            (1, 16), (0, 17), (0, 17), (1, 16), (2, 15), (4, 13),
        )
        inicio = indice * Amuleto.FAIXA_GRADE
        fim = inicio + Amuleto.FAIXA_GRADE
        largura = Amuleto.FAIXA_GRADE * tamanho_pixel
        altura = Amuleto.ALTURA_GRADE * tamanho_pixel
        imagem = pygame.Surface((largura, altura), pygame.SRCALPHA)
        base, sombra, brilho = Amuleto.CORES[indice]

        for y, (esquerda, direita) in enumerate(linhas):
            for x in range(esquerda, direita + 1):
                if not inicio <= x < fim:
                    continue
                retangulo = pygame.Rect((x - inicio) * tamanho_pixel, y * tamanho_pixel,
                                        tamanho_pixel, tamanho_pixel)
                cor = base if (x + y) % 3 else sombra
                if (x, y) in ((8, 4), (9, 4), (8, 5), (9, 5), (8, 6)):
                    cor = (255, 222, 113)
                elif (indice == 0 and x == 4 and y in (5, 6)) or (
                        indice == 2 and x == 13 and y in (5, 6)):
                    cor = brilho
                pygame.draw.rect(imagem, cor, retangulo)

                for dx, dy, lado in ((0, -1, "top"), (0, 1, "bottom"),
                                     (-1, 0, "left"), (1, 0, "right")):
                    nx, ny = x + dx, y + dy
                    vizinho_dentro = (0 <= ny < len(linhas)
                                      and linhas[ny][0] <= nx <= linhas[ny][1])
                    if vizinho_dentro:
                        continue
                    if lado == "top":
                        pygame.draw.line(imagem, Amuleto.CONTORNO, retangulo.topleft, retangulo.topright)
                    elif lado == "bottom":
                        pygame.draw.line(imagem, Amuleto.CONTORNO, retangulo.bottomleft, retangulo.bottomright)
                    elif lado == "left":
                        pygame.draw.line(imagem, Amuleto.CONTORNO, retangulo.topleft, retangulo.bottomleft)
                    else:
                        pygame.draw.line(imagem, Amuleto.CONTORNO, retangulo.topright, retangulo.bottomright)
        return imagem
