import os
import pygame

from classes.colisao import Colisao


class Player:
    def __init__(self, x=50, y=570):  # Posição inicial na estrada de terra

        # Aumentado para 96x96 para ficar proporcional à resolução 1400x760
        self.largura = 96
        self.altura = 96

        self.direcao = "direita"

        # =======================
        # Imagens paradas (Idle)
        # =======================
        self.idle_right = pygame.image.load(
            os.path.join(
                "assets",
                "sprites",
                "personagem_principal",
                "rotations",
                "south-east.png"
            )
        ).convert_alpha()

        self.idle_right = pygame.transform.scale(
            self.idle_right, (self.largura, self.altura)
        )

        self.idle_left = pygame.image.load(
            os.path.join(
                "assets",
                "sprites",
                "personagem_principal",
                "rotations",
                "south-west.png"
            )
        ).convert_alpha()

        self.idle_left = pygame.transform.scale(
            self.idle_left, (self.largura, self.altura)
        )

        # Tentativa de carregar idle para cima e para baixo do diretório rotations
        try:
            self.idle_up = pygame.image.load(
                os.path.join(
                    "assets",
                    "sprites",
                    "personagem_principal",
                    "rotations",
                    "north.png"
                )
            ).convert_alpha()
            self.idle_up = pygame.transform.scale(
                self.idle_up, (self.largura, self.altura)
            )
        except pygame.error:
            self.idle_up = None

        try:
            self.idle_down = pygame.image.load(
                os.path.join(
                    "assets",
                    "sprites",
                    "personagem_principal",
                    "rotations",
                    "south.png"
                )
            ).convert_alpha()
            self.idle_down = pygame.transform.scale(
                self.idle_down, (self.largura, self.altura)
            )
        except pygame.error:
            self.idle_down = None

        # =======================
        # Animação Direita
        # =======================
        self.animacao_direita = []

        for i in range(1, 5):
            imagem = pygame.image.load(
                os.path.join(
                    "assets",
                    "sprites",
                    "personagem_principal",
                    "run_right",
                    f"{i}.png"
                )
            ).convert_alpha()

            imagem = pygame.transform.scale(
                imagem, (self.largura, self.altura)
            )

            self.animacao_direita.append(imagem)

        # =======================
        # Animação Esquerda
        # =======================
        self.animacao_esquerda = []

        for i in range(1, 5):
            imagem = pygame.image.load(
                os.path.join(
                    "assets",
                    "sprites",
                    "personagem_principal",
                    "run_left",
                    f"{i}.png"
                )
            ).convert_alpha()

            imagem = pygame.transform.scale(
                imagem, (self.largura, self.altura)
            )

            self.animacao_esquerda.append(imagem)

        # =======================
        # Animação Cima (run_up)
        # =======================
        self.animacao_cima = []

        for i in range(1, 5):
            imagem = pygame.image.load(
                os.path.join(
                    "assets",
                    "sprites",
                    "personagem_principal",
                    "run_up",
                    f"{i}.png"
                )
            ).convert_alpha()

            imagem = pygame.transform.scale(
                imagem, (self.largura, self.altura)
            )

            self.animacao_cima.append(imagem)

        # =======================
        # Animação Baixo (run_low)
        # =======================
        self.animacao_baixo = []

        for i in range(1, 5):
            imagem = pygame.image.load(
                os.path.join(
                    "assets",
                    "sprites",
                    "personagem_principal",
                    "run_low",
                    f"{i}.png"
                )
            ).convert_alpha()

            imagem = pygame.transform.scale(
                imagem, (self.largura, self.altura)
            )

            self.animacao_baixo.append(imagem)

        # Fallbacks caso as imagens idle específicas de cima/baixo não existam
        if self.idle_up is None:
            self.idle_up = self.animacao_cima[0]
        if self.idle_down is None:
            self.idle_down = self.animacao_baixo[0]

        self.imagem = self.idle_right

        self.frame = 0
        self.velocidade_animacao = 0.2

        # Posição
        self.x = float(x)
        self.y = float(y)

        # Velocidade ajustada para telas maiores
        self.velocidade = 5

        # Instância da colisão (1400x760)
        self.colisao = Colisao(largura=1400, altura=760)

    def desenhar(self, janela, debug=False):
        if debug:
            self.colisao.desenhar_debug(janela)

        janela.blit(self.imagem, (int(self.x), int(self.y)))

    def mover(self):
        teclas = pygame.key.get_pressed()
        andando = False

        dx = 0
        dy = 0

        # Movimento Horizontal
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            dx -= self.velocidade
            self.direcao = "esquerda"
            andando = True

        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            dx += self.velocidade
            self.direcao = "direita"
            andando = True

        # Movimento Vertical
        if teclas[pygame.K_w] or teclas[pygame.K_UP]:
            dy -= self.velocidade
            if dx == 0:
                self.direcao = "cima"
            andando = True

        if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            dy += self.velocidade
            if dx == 0:
                self.direcao = "baixo"
            andando = True

        # Testar e aplicar movimento em X
        if dx != 0:
            novo_x = self.x + dx
            pes_x = novo_x + (self.largura / 2)
            pes_y = self.y + self.altura
            if self.colisao.pode_andar(pes_x, pes_y):
                self.x = novo_x

        # Testar e aplicar movimento em Y
        if dy != 0:
            novo_y = self.y + dy
            pes_x = self.x + (self.largura / 2)
            pes_y = novo_y + self.altura
            if self.colisao.pode_andar(pes_x, pes_y):
                self.y = novo_y

        # Atualizar Animações
        if andando:
            self.frame += self.velocidade_animacao

            if self.direcao == "direita":
                if self.frame >= len(self.animacao_direita):
                    self.frame = 0
                self.imagem = self.animacao_direita[int(self.frame)]

            elif self.direcao == "esquerda":
                if self.frame >= len(self.animacao_esquerda):
                    self.frame = 0
                self.imagem = self.animacao_esquerda[int(self.frame)]

            elif self.direcao == "cima":
                if self.frame >= len(self.animacao_cima):
                    self.frame = 0
                self.imagem = self.animacao_cima[int(self.frame)]

            elif self.direcao == "baixo":
                if self.frame >= len(self.animacao_baixo):
                    self.frame = 0
                self.imagem = self.animacao_baixo[int(self.frame)]

        else:
            self.frame = 0
            if self.direcao == "direita":
                self.imagem = self.idle_right
            elif self.direcao == "esquerda":
                self.imagem = self.idle_left
            elif self.direcao == "cima":
                self.imagem = self.idle_up
            elif self.direcao == "baixo":
                self.imagem = self.idle_down