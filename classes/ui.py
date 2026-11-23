import pygame
from classes.systems.audio import Audio

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
                if b.rect.collidepoint(evento.pos) and self.indice != i:
                    self.indice = i
                    Audio.tocar("selecao")
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for i, b in enumerate(self.botoes):
                if b.rect.collidepoint(evento.pos):
                    self.indice = i
                    return i
        elif evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_UP, pygame.K_w):
                self.indice = (self.indice - 1) % len(self.botoes)
                Audio.tocar("selecao")
            elif evento.key in (pygame.K_DOWN, pygame.K_s):
                self.indice = (self.indice + 1) % len(self.botoes)
                Audio.tocar("selecao")
            elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                return self.indice
        return None

    def desenhar(self, janela, alpha=255):
        for i, b in enumerate(self.botoes):
            b.desenhar(janela, selecionado=(i == self.indice), alpha=alpha)


class Slider:
    """Controle deslizante pixelado, ajustável por mouse ou teclado."""

    def __init__(self, rotulo, centro, valor, minimo=0, maximo=100, passo=5, largura=420):
        self.rotulo = rotulo
        self.minimo = minimo
        self.maximo = maximo
        self.passo = passo
        self.largura = largura
        self.valor = max(minimo, min(maximo, int(valor)))
        self.arrastando = False
        self.trilho_rect = pygame.Rect(0, 0, largura, 10)
        self.trilho_rect.center = centro
        self.rect = pygame.Rect(0, 0, largura + 360, 56)
        self.rect.center = centro

    def _definir_valor(self, valor):
        valor = max(self.minimo, min(self.maximo, int(valor)))
        if valor == self.valor:
            return False
        self.valor = valor
        return True

    def _definir_posicao(self, x):
        proporcao = max(0.0, min(1.0, (x - self.trilho_rect.left) / self.trilho_rect.width))
        valor = round(self.minimo + proporcao * (self.maximo - self.minimo))
        valor = round((valor - self.minimo) / self.passo) * self.passo + self.minimo
        return self._definir_valor(valor)

    def tratar_evento(self, evento, selecionado=False):
        if evento.type == pygame.KEYDOWN and selecionado:
            if evento.key in (pygame.K_LEFT, pygame.K_a):
                return self._definir_valor(self.valor - self.passo)
            if evento.key in (pygame.K_RIGHT, pygame.K_d):
                return self._definir_valor(self.valor + self.passo)
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.trilho_rect.inflate(0, 32).collidepoint(evento.pos):
                self.arrastando = True
                return self._definir_posicao(evento.pos[0])
        elif evento.type == pygame.MOUSEMOTION and self.arrastando:
            return self._definir_posicao(evento.pos[0])
        elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            self.arrastando = False
        return False

    def desenhar(self, janela, selecionado=False):
        percentual = ((self.valor - self.minimo) / (self.maximo - self.minimo)
                      if self.maximo > self.minimo else 0)
        preenchido = pygame.Rect(self.trilho_rect)
        preenchido.width = int(self.trilho_rect.width * percentual)
        pygame.draw.rect(janela, (65, 68, 75), self.trilho_rect)
        if preenchido.width:
            pygame.draw.rect(janela, (255, 214, 74), preenchido)
        pygame.draw.rect(janela, (180, 185, 195), self.trilho_rect, 2)

        marcador = pygame.Rect(0, 0, 20, 20)
        marcador.center = (self.trilho_rect.left + int(self.trilho_rect.width * percentual),
                           self.trilho_rect.centery)
        pygame.draw.rect(janela, (255, 226, 115), marcador)
        pygame.draw.rect(janela, (65, 56, 35), marcador, 2)

        cor = (255, 214, 74) if selecionado else (225, 225, 230)
        rotulo = texto_pixel(self.rotulo, 9, cor, escala=2)
        janela.blit(rotulo, rotulo.get_rect(midright=(self.trilho_rect.left - 24,
                                                      self.trilho_rect.centery)))
        texto_valor = texto_pixel(f"{self.valor}%", 9, cor, escala=2)
        janela.blit(texto_valor, texto_valor.get_rect(midleft=(self.trilho_rect.right + 24,
                                                               self.trilho_rect.centery)))


class SeletorOpcoes:
    """Seletor horizontal de valores textuais para as opções gráficas."""

    def __init__(self, opcoes, centro, valor, largura=420, rotulo="QUALIDADE DO GRÁFICO"):
        self.opcoes = tuple(opcoes)
        self.rotulo = rotulo
        self.largura = largura
        self.rect = pygame.Rect(0, 0, largura + 360, 56)
        self.rect.center = centro
        self.retos_opcoes = []
        largura_opcao = largura // len(self.opcoes)
        for indice in range(len(self.opcoes)):
            ret = pygame.Rect(centro[0] - largura // 2 + indice * largura_opcao,
                              centro[1] - 25, largura_opcao, 50)
            self.retos_opcoes.append(ret)
        normalizadas = [opcao.lower().replace("é", "e") for opcao in self.opcoes]
        self.indice = next((i for i, opcao in enumerate(normalizadas)
                            if opcao == valor.lower().replace("é", "e")), 0)

    @property
    def valor(self):
        return self.opcoes[self.indice].lower().replace("é", "e")

    def _selecionar(self, indice):
        indice = max(0, min(len(self.opcoes) - 1, indice))
        if indice == self.indice:
            return False
        self.indice = indice
        return True

    def tratar_evento(self, evento, selecionado=False):
        if evento.type == pygame.KEYDOWN and selecionado:
            if evento.key in (pygame.K_LEFT, pygame.K_a):
                return self._selecionar(self.indice - 1)
            if evento.key in (pygame.K_RIGHT, pygame.K_d):
                return self._selecionar(self.indice + 1)
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for indice, ret in enumerate(self.retos_opcoes):
                if ret.collidepoint(evento.pos):
                    return self._selecionar(indice)
        return False

    def desenhar(self, janela, selecionado=False):
        cor_rotulo = (255, 214, 74) if selecionado else (225, 225, 230)
        rotulo = texto_pixel(self.rotulo, 9, cor_rotulo, escala=2)
        janela.blit(rotulo, rotulo.get_rect(midright=(self.retos_opcoes[0].left - 24,
                                                      self.retos_opcoes[0].centery)))
        for indice, (opcao, ret) in enumerate(zip(self.opcoes, self.retos_opcoes)):
            ativo = indice == self.indice
            cor = (255, 214, 74) if ativo else (225, 225, 230)
            texto = texto_pixel(opcao.upper(), 9, cor, escala=2)
            janela.blit(texto, texto.get_rect(center=ret.center))
            if indice < len(self.opcoes) - 1:
                divisor = texto_pixel("|", 9, (155, 160, 170), escala=2)
                janela.blit(divisor, divisor.get_rect(center=(ret.right, ret.centery)))
