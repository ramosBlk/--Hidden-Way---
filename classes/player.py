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

        if teclas[pygame.K_a]:
            dx -= self.velocidade
            self.direcao = "esquerda"
            andando = True

        if teclas[pygame.K_d]:
            dx += self.velocidade
            self.direcao = "direita"
            andando = True

        if teclas[pygame.K_w]:
            dy -= self.velocidade
            andando = True

        if teclas[pygame.K_s]:
            dy += self.velocidade
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
            else:
                if self.frame >= len(self.animacao_esquerda):
                    self.frame = 0
                self.imagem = self.animacao_esquerda[int(self.frame)]
        else:
            self.frame = 0
            if self.direcao == "direita":
                self.imagem = self.idle_right
            else:
                self.imagem = self.idle_left