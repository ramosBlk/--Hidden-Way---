import pygame

from classes.entities.amuleto import Amuleto
from classes.systems.assets import carregar_imagem
from classes.ui import texto_pixel, desenhar_placa


class Hud:
    """Interface de jogo: objetivos, chave e avisos temporários."""

    POS_AMULETOS = ((509, 41), (521, 41), (533, 41))
    POS_CHAVE = (750, 40)

    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.icone_chave = carregar_imagem("assets/sprites/itens/chave.png", (39, 21), (255, 214, 74))
        self.icones_chave = [
            pygame.transform.scale(self.icone_chave, (largura, altura))
            for largura, altura in ((39, 21), (43, 23), (47, 25))
        ]
        self.icones_chave_apagados = [icone.copy() for icone in self.icones_chave]
        for icone in self.icones_chave_apagados:
            icone.set_alpha(90)
        self.icones_amuleto = [Amuleto.criar_sprite(indice, 2) for indice in range(3)]
        self.icones_amuleto_apagados = [icone.copy() for icone in self.icones_amuleto]
        for icone in self.icones_amuleto_apagados:
            icone.fill((105, 110, 125, 150), special_flags=pygame.BLEND_RGBA_MULT)
        self.avisos = []          # [texto, tempo_restante, duracao, cor]
        self.aviso_central = None
        self.pulso_chave = 0.0    # animação rápida quando o ícone "recebe" a chave
        self.retrato_jogador = None
        self.coracao_cheio = self._criar_coracao((235, 65, 75))
        self.coracao_vazio = self._criar_coracao((90, 92, 102))

    def configurar_jogador(self, jogador):
        sprite = jogador.sprites.idle_de("baixo")
        largura = min(36, sprite.get_width())
        altura = min(36, sprite.get_height())
        recorte = sprite.subsurface(pygame.Rect(
            (sprite.get_width() - largura) // 2, 0, largura, altura)).copy()
        self.retrato_jogador = pygame.transform.scale(recorte, (36, 36))

    @staticmethod
    def _criar_coracao(cor):
        linhas = (
            "..XX...XX..",
            ".XXXX.XXXX.",
            "XXXXXXXXXXX",
            "XXXXXXXXXXX",
            ".XXXXXXXXX.",
            "..XXXXXXX..",
            "...XXXXX...",
            "....XXX....",
            ".....X.....",
        )
        imagem = pygame.Surface((11, 9), pygame.SRCALPHA)
        contorno = (45, 28, 38)
        for y, linha in enumerate(linhas):
            for x, pixel in enumerate(linha):
                if pixel != "X":
                    continue
                pygame.draw.rect(imagem, contorno, (x, y, 1, 1))
                for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                    nx, ny = x + dx, y + dy
                    if (ny < 0 or ny >= len(linhas) or nx < 0 or nx >= len(linha)
                            or linhas[ny][nx] != "X"):
                        continue
                    pygame.draw.rect(imagem, cor, (x, y, 1, 1))
        return pygame.transform.scale(imagem, (33, 27))

    def avisar(self, texto, duracao=2.2, cor=(255, 244, 170)):
        # evita empilhar o mesmo aviso repetido
        for a in self.avisos:
            if a[0] == texto:
                a[1] = a[2] = duracao
                return
        self.avisos.append([texto, duracao, duracao, cor])

    def chave_recebida(self):
        self.pulso_chave = 0.5

    def avisar_central(self, texto, duracao=2.2, cor=(255, 244, 170)):
        self.aviso_central = [texto, duracao, duracao, cor]

    def atualizar(self, dt):
        for a in self.avisos:
            a[1] -= dt
        self.avisos = [a for a in self.avisos if a[1] > 0]
        if self.aviso_central:
            self.aviso_central[1] -= dt
            if self.aviso_central[1] <= 0:
                self.aviso_central = None
        self.pulso_chave = max(0.0, self.pulso_chave - dt)

    def desenhar_objetivos(self, janela, amuletos_recolhidos, tem_chave):
        placa = pygame.Rect(0, 0, 420, 58)
        placa.center = (self.largura // 2, 39)
        desenhar_placa(janela, placa, (160, 130, 50), (30, 28, 24))

        coletados = sum(amuletos_recolhidos)
        total_amuletos = len(amuletos_recolhidos)
        for indice, posicao in enumerate(self.POS_AMULETOS):
            icone = (self.icones_amuleto[indice] if amuletos_recolhidos[indice]
                     else self.icones_amuleto_apagados[indice])
            janela.blit(icone, icone.get_rect(center=posicao))

        titulo = texto_pixel("AMULETOS", 7, (225, 225, 230), escala=2)
        janela.blit(titulo, titulo.get_rect(center=(625, 28)))
        contador = texto_pixel(f"{coletados}/{total_amuletos}", 8,
                               (255, 230, 120), escala=2)
        janela.blit(contador, contador.get_rect(center=(625, 47)))
        pygame.draw.line(janela, (110, 105, 95), (715, 18), (715, 59), 2)

        if self.pulso_chave > 0:
            indice_icone = 2 if self.pulso_chave > 0.3 else 1
        else:
            indice_icone = 0
        icone_chave = (self.icones_chave[indice_icone] if tem_chave
                       else self.icones_chave_apagados[indice_icone])
        janela.blit(icone_chave, icone_chave.get_rect(center=self.POS_CHAVE))
        texto_chave = texto_pixel("CHAVE", 7, (255, 230, 120) if tem_chave else (145, 145, 145), escala=2)
        janela.blit(texto_chave, texto_chave.get_rect(midleft=(777, 40)))

    def desenhar_vidas(self, janela, jogador):
        painel = pygame.Rect(10, 10, 224, 56)
        pygame.draw.rect(janela, (24, 27, 35), painel)
        pygame.draw.rect(janela, (160, 130, 50), painel, 3)
        pygame.draw.rect(janela, (65, 61, 52), painel.inflate(-8, -8), 1)
        moldura = pygame.Rect(17, 16, 44, 44)
        pygame.draw.rect(janela, (8, 11, 16), moldura)
        pygame.draw.rect(janela, (130, 140, 155), moldura, 2)
        if self.retrato_jogador:
            janela.blit(self.retrato_jogador, self.retrato_jogador.get_rect(center=moldura.center))
        for indice in range(3):
            coracao = self.coracao_cheio if indice < jogador.vidas else self.coracao_vazio
            janela.blit(coracao, (72 + indice * 49, 25))

    def desenhar_contador(self, janela, atual, total):
        """Desenha a quantidade de amuletos coletados."""
        self.desenhar_objetivos(janela, [indice < atual for indice in range(total)], False)

    def desenhar(self, janela, mostrar_chave):
        if mostrar_chave:
            self.desenhar_objetivos(janela, [False, False, False], True)

        y = 120
        for texto, restante, duracao, cor in self.avisos:
            alpha = int(255 * min(1.0, restante / 0.4, (duracao - restante) / 0.15 + 0.01))
            txt = texto_pixel(texto, 10, cor, escala=3).copy()
            txt.set_alpha(alpha)
            janela.blit(txt, txt.get_rect(center=(self.largura // 2, y)))
            y += 44

        if self.aviso_central:
            texto, restante, duracao, cor = self.aviso_central
            alpha = int(255 * min(1.0, restante / 0.35, (duracao - restante) / 0.15 + 0.01))
            imagem = texto_pixel(texto, 14, cor, escala=3, sombra=(35, 25, 10)).copy()
            imagem.set_alpha(alpha)
            janela.blit(imagem, imagem.get_rect(center=(self.largura // 2, self.altura // 2)))
