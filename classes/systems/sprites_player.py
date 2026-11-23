import os
import pygame

BASE = os.path.join("assets", "sprites", "personagem_principal")
REF = 64  # tamanho original (px) dos PNGs do personagem


class SpritesPlayer:
    """Carrega e entrega os sprites do jogador por direção."""

    # direção -> nome do arquivo/pasta
    IDLE = {"direita": "south-east", "esquerda": "south-west", "cima": "north", "baixo": "south"}
    CORRIDA = {"direita": "run_right", "esquerda": "run_left", "cima": "run_up", "baixo": "run_low"}
    PULO = {"direita": "east", "esquerda": "west", "cima": "north", "baixo": "south"}
    DISPARO = "shoot"

    # Pastas exportadas com canvas maior que 64x64: (x, y) da janela 64x64 recortada
    RECORTES = {"south": (10, 8)}  # jumping/south é 84x84

    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.idle = {d: self._imagem(os.path.join("rotations", f"{n}.png")) for d, n in self.IDLE.items()}
        self.corrida = {d: [self._imagem(os.path.join(p, f"{i}.png")) for i in range(1, 5)]
                        for d, p in self.CORRIDA.items()}
        self.pulo = {d: self._pasta(os.path.join("jumping", p), self.RECORTES.get(p))
                     for d, p in self.PULO.items()}
        self.disparo = self._pasta(self.DISPARO, normalizar_altura=True)
        self.disparo_esquerda = [pygame.transform.flip(frame, True, False)
                                 for frame in self.disparo]

    def _imagem(self, caminho, recorte=None, normalizar_altura=False):
        try:
            img = pygame.image.load(os.path.join(BASE, caminho)).convert_alpha()
            if recorte:
                img = img.subsurface((*recorte, REF, REF)).copy()
            if normalizar_altura:
                limites = img.get_bounding_rect()
                if limites.height:
                    escala = self.tamanho[1] * (60 / REF) / limites.height
                    ampliada = pygame.transform.scale(
                        img,
                        (round(img.get_width() * escala), round(img.get_height() * escala)),
                    )
                    normalizada = pygame.Surface(self.tamanho, pygame.SRCALPHA)
                    destino_x = self.tamanho[0] / 2 - limites.centerx * escala
                    destino_y = self.tamanho[1] * (62 / REF) - limites.bottom * escala
                    normalizada.blit(ampliada, (round(destino_x), round(destino_y)))
                    return normalizada
            return pygame.transform.scale(img, self.tamanho)
        except (pygame.error, FileNotFoundError, ValueError):
            return pygame.Surface(self.tamanho)

    def _pasta(self, caminho, recorte=None, normalizar_altura=False):
        """Carrega todos os PNGs de uma pasta em ordem numérica (frame_000, frame_001...)."""
        pasta = os.path.join(BASE, caminho)
        if not os.path.isdir(pasta):
            return []
        arquivos = sorted(
            (f for f in os.listdir(pasta) if f.lower().endswith(".png")),
            key=lambda nome: int("".join(c for c in nome if c.isdigit()) or 0),
        )
        return [
            self._imagem(os.path.join(caminho, f), recorte, normalizar_altura)
            for f in arquivos
        ]

    def idle_de(self, direcao):
        return self.idle.get(direcao, self.idle["direita"])

    def corrida_de(self, direcao):
        return self.corrida.get(direcao, self.corrida["direita"])

    def pulo_de(self, direcao):
        """Frames do pulo; usa 'direita' como reserva se a pasta estiver vazia."""
        return self.pulo.get(direcao) or self.pulo["direita"]