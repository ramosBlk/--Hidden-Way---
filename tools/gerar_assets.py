"""
Gera (proceduralmente) os assets em pixel art da mecânica chave -> baú -> caverna.

Uso (na raiz do projeto):  python tools/gerar_assets.py

Os PNGs gerados ficam em assets/sprites/ e podem ser substituídos por arte feita à mão
(basta manter o mesmo nome e proporção). O jogo possui fallback caso algum falte.
"""
import os
import random

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
import pygame

pygame.init()
pygame.display.set_mode((1, 1))

ESCALA = 3  # cada "pixel de arte" vira 3x3 pixels na tela


def salvar(superficie, caminho, escala=ESCALA):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    if escala != 1:
        superficie = pygame.transform.scale(superficie, (superficie.get_width() * escala,
                                                         superficie.get_height() * escala))
    pygame.image.save(superficie, caminho)
    print("gerado:", caminho, superficie.get_size())


def nova(w, h):
    return pygame.Surface((w, h), pygame.SRCALPHA)


def contorno(surf, cor):
    """Adiciona 1px de contorno ao redor dos pixels opacos."""
    w, h = surf.get_size()
    saida = surf.copy()
    for y in range(h):
        for x in range(w):
            if surf.get_at((x, y)).a == 0:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and surf.get_at((nx, ny)).a > 0:
                        saida.set_at((x, y), cor)
                        break
    return saida


# ---------------------------------------------------------------- paleta (do Mapa_1)
OUT = (38, 22, 14)
MAD_ESC = (92, 54, 30)
MAD = (148, 92, 50)
MAD_CLA = (190, 128, 72)
METAL = (214, 214, 204)
METAL_ESC = (128, 128, 124)
OURO = (255, 214, 74)
OURO_CLA = (255, 244, 170)
OURO_ESC = (190, 128, 28)
INTERIOR = (30, 18, 16)
TRANSP = (0, 0, 0, 0)


# ---------------------------------------------------------------- baú (14x16 -> 42x48)
def _base_bau(s):
    pygame.draw.rect(s, OUT, (0, 10, 14, 6))
    pygame.draw.rect(s, MAD, (1, 11, 12, 4))
    pygame.draw.rect(s, MAD_ESC, (1, 14, 12, 1))
    pygame.draw.rect(s, MAD_CLA, (1, 11, 12, 1))
    for x in (2, 11):  # faixas de metal
        pygame.draw.rect(s, METAL, (x, 11, 1, 4))
        pygame.draw.rect(s, METAL_ESC, (x + (1 if x == 2 else -1), 11, 1, 4))


def _tampa_fechada(s, dy=0):
    pygame.draw.rect(s, OUT, (0, 6 + dy, 14, 5))
    s.set_at((0, 6 + dy), TRANSP)
    s.set_at((13, 6 + dy), TRANSP)
    pygame.draw.rect(s, MAD, (1, 7 + dy, 12, 3))
    pygame.draw.rect(s, MAD_CLA, (2, 7 + dy, 10, 1))
    pygame.draw.rect(s, MAD_ESC, (1, 9 + dy, 12, 1))
    for x in (2, 11):
        pygame.draw.rect(s, METAL, (x, 6 + dy, 1, 4))
        pygame.draw.rect(s, METAL_ESC, (x + (1 if x == 2 else -1), 7 + dy, 1, 3))


def _fechadura(s, aberta=False):
    pygame.draw.rect(s, OUT, (5, 9, 4, 4))
    pygame.draw.rect(s, OURO if not aberta else OURO_ESC, (6, 10, 2, 2))


def frame_bau(n):
    s = nova(14, 16)
    if n == 0:  # fechado
        _base_bau(s)
        _tampa_fechada(s)
        _fechadura(s)
    elif n == 1:  # tampa destravando: sobe 1px e deixa escapar uma linha de luz
        _base_bau(s)
        pygame.draw.rect(s, OURO_CLA, (1, 10, 12, 1))
        _tampa_fechada(s, dy=-1)
        _fechadura(s, aberta=True)
    elif n == 2:  # tampa meio aberta
        _base_bau(s)
        pygame.draw.rect(s, OUT, (0, 7, 14, 4))
        pygame.draw.rect(s, OURO_CLA, (1, 8, 12, 2))
        pygame.draw.rect(s, OURO, (1, 10, 12, 1))
        pygame.draw.rect(s, OUT, (1, 2, 12, 5))  # tampa inclinada para trás (face interna)
        pygame.draw.rect(s, MAD_ESC, (2, 3, 10, 3))
        pygame.draw.rect(s, MAD, (2, 3, 10, 1))
        for x in (3, 10):
            pygame.draw.rect(s, METAL_ESC, (x, 2, 1, 5))
    else:  # totalmente aberto
        _base_bau(s)
        pygame.draw.rect(s, OUT, (0, 6, 14, 5))
        pygame.draw.rect(s, INTERIOR, (1, 7, 12, 3))
        pygame.draw.rect(s, OURO_ESC, (2, 8, 10, 2))   # tesouro
        pygame.draw.rect(s, OURO, (3, 7, 3, 2))
        pygame.draw.rect(s, OURO_CLA, (4, 7, 1, 1))
        pygame.draw.rect(s, OURO, (8, 7, 3, 2))
        pygame.draw.rect(s, OURO_CLA, (9, 7, 1, 1))
        pygame.draw.rect(s, OUT, (1, 0, 12, 6))        # tampa totalmente atrás
        pygame.draw.rect(s, MAD, (2, 1, 10, 4))
        pygame.draw.rect(s, MAD_CLA, (2, 1, 10, 1))
        pygame.draw.rect(s, MAD_ESC, (2, 4, 10, 1))
        for x in (3, 10):
            pygame.draw.rect(s, METAL, (x, 1, 1, 4))
    return s


# ---------------------------------------------------------------- chave (13x7 -> 39x21)
def gerar_chave():
    s = nova(13, 7)
    pygame.draw.circle(s, OURO, (3, 3), 3)
    s.set_at((3, 3), TRANSP)
    s.set_at((2, 1), OURO_CLA)
    s.set_at((3, 1), OURO_CLA)
    pygame.draw.rect(s, OURO, (6, 3, 7, 1))
    pygame.draw.rect(s, OURO_ESC, (6, 4, 7, 1))
    pygame.draw.rect(s, OURO, (10, 5, 1, 2))
    pygame.draw.rect(s, OURO, (12, 5, 1, 2))
    return contorno(s, OUT)


# ---------------------------------------------------------------- brilhos
def gerar_brilho(tamanho=16, cor=(255, 230, 140), degraus=5):
    """Brilho radial 'em degraus' (estilo pixel art), com alpha decrescente."""
    s = nova(tamanho, tamanho)
    c = (tamanho - 1) / 2
    for y in range(tamanho):
        for x in range(tamanho):
            d = ((x - c) ** 2 + (y - c) ** 2) ** 0.5 / (tamanho / 2)
            if d < 1:
                nivel = int((1 - d) * degraus) / degraus
                if nivel > 0:
                    s.set_at((x, y), (*cor, int(190 * nivel)))
    return s


def gerar_luz_caverna():
    """Luz que sai da entrada da caverna (elipse vertical em degraus)."""
    w, h = 33, 36
    s = nova(w, h)
    for y in range(h):
        for x in range(w):
            dx = (x - (w - 1) / 2) / (w / 2)
            dy = (y - (h - 1) / 2) / (h / 2)
            d = (dx * dx + dy * dy) ** 0.5
            if d < 1:
                nivel = int((1 - d) ** 0.8 * 8) / 8
                if nivel > 0:
                    cor = (255, 252, 225) if nivel > 0.6 else (255, 232, 150)
                    s.set_at((x, y), (*cor, min(255, int(300 * nivel))))
    return s


# ---------------------------------------------------------------- caverna bloqueada (22x23 -> 66x69)
def gerar_caverna_bloqueada():
    rnd = random.Random(7)
    w, h = 22, 23
    s = nova(w, h)
    mascara = nova(w, h)
    for y in range(h):
        # arco: nas primeiras linhas a pedra é mais estreita
        recuo = {0: 7, 1: 5, 2: 3, 3: 2, 4: 1}.get(y, 0)
        pygame.draw.line(mascara, (255, 255, 255, 255), (recuo, y), (w - 1 - recuo, y))

    cinzas = [(112, 114, 120), (98, 100, 108), (126, 128, 132), (88, 90, 98)]
    y = 0
    while y < h:
        altura = rnd.choice((5, 6, 6))
        x = -rnd.randint(0, 3)
        while x < w:
            largura = rnd.randint(4, 8)
            base = rnd.choice(cinzas)
            for yy in range(y, min(y + altura, h)):
                for xx in range(max(x, 0), min(x + largura, w)):
                    if mascara.get_at((xx, yy)).a == 0:
                        continue
                    cor = base
                    if yy == y:
                        cor = tuple(min(255, c + 28) for c in base)
                    elif yy == y + altura - 1 or xx == x + largura - 1:
                        cor = tuple(max(0, c - 34) for c in base)
                    elif xx == max(x, 0):
                        cor = tuple(max(0, c - 18) for c in base)
                    s.set_at((xx, yy), cor)
            x += largura
        y += altura
    # musgo sobre as pedras
    for _ in range(22):
        xx, yy = rnd.randint(2, w - 3), rnd.randint(1, h - 2)
        if s.get_at((xx, yy)).a:
            s.set_at((xx, yy), rnd.choice(((74, 120, 52), (96, 148, 62))))
    # cadeado dourado no centro (indica "trancado")
    cx, cy = 11, 11
    pygame.draw.rect(s, OUT, (cx - 2, cy - 4, 5, 4))
    pygame.draw.rect(s, TRANSP, (cx - 1, cy - 3, 3, 3))
    pygame.draw.rect(s, METAL, (cx - 2, cy - 3, 1, 3))
    pygame.draw.rect(s, METAL, (cx + 2, cy - 3, 1, 3))
    pygame.draw.rect(s, OUT, (cx - 3, cy - 1, 7, 6))
    pygame.draw.rect(s, OURO, (cx - 2, cy, 5, 4))
    pygame.draw.rect(s, OURO_ESC, (cx - 2, cy + 3, 5, 1))
    s.set_at((cx, cy + 1), OUT)
    s.set_at((cx, cy + 2), OUT)
    return contorno(s, (34, 34, 42))


# ---------------------------------------------------------------- fundo da fase 2 (350x190 -> 1400x760)
def gerar_fundo_caverna():
    rnd = random.Random(11)
    w, h = 350, 190
    s = pygame.Surface((w, h))
    for y in range(h):
        t = y / h
        pygame.draw.line(s, (int(18 + 14 * t), int(14 + 10 * t), int(38 + 22 * t)), (0, y), (w, y))

    def silhueta(cor, base, amp, passo):
        pts = [(0, h)]
        for x in range(0, w + passo, passo):
            pts.append((x, base - rnd.randint(0, amp)))
        pts.append((w, h))
        pygame.draw.polygon(s, cor, pts)

    silhueta((30, 26, 56), 140, 40, 9)
    silhueta((22, 19, 42), 160, 28, 7)
    for x in range(0, w, 7):  # estalactites
        comp = rnd.randint(6, 34)
        pygame.draw.polygon(s, (12, 10, 26), [(x, 0), (x + 7, 0), (x + 3 + rnd.randint(-1, 1), comp)])
    for _ in range(14):  # cristais brilhantes
        cx, cy = rnd.randint(8, w - 8), rnd.randint(120, 175)
        for i in range(rnd.randint(2, 4)):
            altura = rnd.randint(6, 14)
            xx = cx + i * 3
            pygame.draw.polygon(s, (70, 200, 230), [(xx, cy), (xx + 2, cy), (xx + 1, cy - altura)])
            s.set_at((xx + 1, cy - altura + 2), (210, 250, 255))
    for _ in range(60):  # poeira
        s.set_at((rnd.randint(0, w - 1), rnd.randint(0, h - 1)), rnd.choice(((90, 80, 140), (60, 160, 190))))
    return s


def main():
    base = os.path.join("assets", "sprites")
    for n in range(4):
        salvar(frame_bau(n), os.path.join(base, "itens", f"bau_{n}.png"))
    salvar(gerar_chave(), os.path.join(base, "itens", "chave.png"))
    salvar(gerar_caverna_bloqueada(), os.path.join(base, "itens", "caverna_bloqueada.png"))
    salvar(gerar_luz_caverna(), os.path.join(base, "itens", "caverna_liberada.png"), escala=2)
    salvar(gerar_brilho(16), os.path.join(base, "efeitos", "brilho.png"))
    salvar(gerar_fundo_caverna(), os.path.join(base, "telas", "Mapa_2.png"), escala=4)


if __name__ == "__main__":
    main()
