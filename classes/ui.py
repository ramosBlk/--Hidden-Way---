import pygame

_cache_fontes = {}
_cache_textos = {}


def _fonte(base):
    if base not in _cache_fontes:
        _cache_fontes[base] = pygame.font.SysFont("consolas,couriernew,arial", base, bold=True)
    return _cache_fontes[base]


def texto_pixel(texto, base=10, cor=(255, 255, 255), escala=3, sombra=(0, 0, 0)):
    """
    Texto com aparência pixelada: renderiza sem antialias numa fonte pequena e amplia por
    um fator inteiro (sem suavização). Retorna uma Surface (com sombra, se pedida).
    """
    chave = (texto, base, cor, escala, sombra)
    if chave not in _cache_textos:
        img = _fonte(base).render(texto, False, cor)
        img = pygame.transform.scale(img, (img.get_width() * escala, img.get_height() * escala))
        if sombra:
            sb = _fonte(base).render(texto, False, sombra)
            sb = pygame.transform.scale(sb, img.get_size())
            saida = pygame.Surface((img.get_width() + escala, img.get_height() + escala), pygame.SRCALPHA)
            saida.blit(sb, (escala, escala))
            saida.blit(img, (0, 0))
            img = saida
        _cache_textos[chave] = img
    return _cache_textos[chave]


def desenhar_placa(janela, rect, cor_borda=(95, 105, 115), cor_fundo=(35, 42, 48)):
    """Placa de pedra com borda dupla (mesmo visual do antigo painel de Game Over)."""
    rect = pygame.Rect(rect)
    sombra = pygame.Surface(rect.size, pygame.SRCALPHA)
    sombra.fill((0, 0, 0, 150))
    janela.blit(sombra, (rect.x + 8, rect.y + 8))
    pygame.draw.rect(janela, cor_fundo, rect)
    pygame.draw.rect(janela, cor_borda, rect, 6)
    pygame.draw.rect(janela, (20, 25, 30), rect.inflate(-12, -12), 4)


class Botao:
    """Botão em estilo moldura de pedra, com estados normal/selecionado (hover ou teclado)."""

    def __init__(self, texto, centro, tamanho=(320, 52)):
        self.texto = texto
        self.rect = pygame.Rect(0, 0, *tamanho)
        self.rect.center = centro

    def desenhar(self, janela, selecionado=False, alpha=255):
        rect = self.rect.inflate(8, 4) if selecionado else self.rect
        surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        fundo = (70, 62, 40) if selecionado else (40, 45, 55)
        borda = (255, 214, 74) if selecionado else (110, 120, 135)
        pygame.draw.rect(surf, fundo, surf.get_rect())
        pygame.draw.rect(surf, borda, surf.get_rect(), 3)
        pygame.draw.rect(surf, (20, 22, 28), surf.get_rect().inflate(-6, -6), 1)
        txt = texto_pixel(self.texto, 9, (255, 244, 200) if selecionado else (225, 225, 230), escala=2)
        surf.blit(txt, txt.get_rect(center=surf.get_rect().center))
        surf.set_alpha(alpha)
        janela.blit(surf, rect)


class NavegadorBotoes:
    """Seleção de botões por teclado (setas/W/S + Enter) e mouse (hover + clique)."""

    def __init__(self, botoes):
        self.botoes = botoes
        self.indice = 0

    def tratar_evento(self, evento):
        """Retorna o índice do botão acionado, ou None."""
        if evento.type == pygame.MOUSEMOTION:
            for i, b in enumerate(self.botoes):
                if b.rect.collidepoint(evento.pos):
                    self.indice = i
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for i, b in enumerate(self.botoes):
                if b.rect.collidepoint(evento.pos):
                    self.indice = i
                    return i
        elif evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_UP, pygame.K_w):
                self.indice = (self.indice - 1) % len(self.botoes)
            elif evento.key in (pygame.K_DOWN, pygame.K_s):
                self.indice = (self.indice + 1) % len(self.botoes)
            elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                return self.indice
        return None

    def desenhar(self, janela, alpha=255):
        for i, b in enumerate(self.botoes):
            b.desenhar(janela, selecionado=(i == self.indice), alpha=alpha)
