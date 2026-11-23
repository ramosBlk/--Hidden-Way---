import pygame


class Pedra:
    """Projétil de pedra pixelado, lançado horizontalmente pelo jogador."""

    VELOCIDADE = 390
    ALCANCE = 480

    def __init__(self, x, y, direcao):
        self.direcao = 1 if direcao == "direita" else -1
        self.distancia = 0.0
        self.rect = pygame.Rect(0, 0, 20, 16)
        self.rect.center = (round(x), round(y))
        self.sprites = self._criar_sprites()

    @staticmethod
    def _criar_sprites():
        imagem = pygame.Surface((18, 15), pygame.SRCALPHA)
        pixels = (
            ".....DDDDD........",
            "...DDGGGGGDD......",
            "..DGGGGGGGGGDD....",
            ".DGGGWWWGGGGGGD...",
            "DGGGWWWWGGGGGGGD..",
            "DGGGGGGGGGGGGGGD..",
            ".DGGGGGGGGGGGGD...",
            "..DDGGGGGGGGDD....",
            "....DDDDD........",
            "..................",
        )
        cores = {
            "D": (35, 40, 50),
            "G": (115, 124, 137),
            "W": (190, 201, 211),
        }
        for y, linha in enumerate(pixels):
            for x, pixel in enumerate(linha):
                if pixel in cores:
                    pygame.draw.rect(imagem, cores[pixel], (x, y + 2, 1, 1))
        sprite = pygame.transform.scale(imagem, (24, 20))
        return sprite, pygame.transform.flip(sprite, True, False)

    def atualizar(self, dt):
        deslocamento = self.VELOCIDADE * dt
        self.rect.x += round(self.direcao * deslocamento)
        self.distancia += deslocamento
        return self.distancia < self.ALCANCE and self.rect.right >= 0 and self.rect.left <= 1400

    def desenhar(self, janela):
        sprite = self.sprites[0] if self.direcao > 0 else self.sprites[1]
        janela.blit(sprite, sprite.get_rect(center=self.rect.center))
