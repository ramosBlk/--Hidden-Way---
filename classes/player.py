import os
import pygame


class Player:
    def __init__(self, x=50, y=520):

        # Direção inicial
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

        self.idle_right = pygame.transform.scale(self.idle_right, (64, 64))

        self.idle_left = pygame.image.load(
            os.path.join(
                "assets",
                "sprites",
                "personagem_principal",
                "rotations",
                "south-west.png"
            )
        ).convert_alpha()

        self.idle_left = pygame.transform.scale(self.idle_left, (64, 64))

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

            imagem = pygame.transform.scale(imagem, (64, 64))
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

            imagem = pygame.transform.scale(imagem, (64, 64))
            self.animacao_esquerda.append(imagem)

        # Imagem inicial
        self.imagem = self.idle_right

        # Controle da animação
        self.frame = 0
        self.velocidade_animacao = 0.2

        # Posição
        self.x = x
        self.y = y

        # Velocidade do personagem
        self.velocidade = 0.2

    def desenhar(self, janela):
        janela.blit(self.imagem, (self.x, self.y))

    def mover(self):
        teclas = pygame.key.get_pressed()

        andando = False

        # ESQUERDA
        if teclas[pygame.K_a]:
            self.x -= self.velocidade
            self.direcao = "esquerda"

            self.frame += self.velocidade_animacao

            if self.frame >= len(self.animacao_esquerda):
                self.frame = 0

            self.imagem = self.animacao_esquerda[int(self.frame)]
            andando = True

        # DIREITA
        elif teclas[pygame.K_d]:
            self.x += self.velocidade
            self.direcao = "direita"

            self.frame += self.velocidade_animacao

            if self.frame >= len(self.animacao_direita):
                self.frame = 0

            self.imagem = self.animacao_direita[int(self.frame)]
            andando = True

        # CIMA
        if teclas[pygame.K_w]:
            self.y -= self.velocidade

        # BAIXO
        if teclas[pygame.K_s]:
            self.y += self.velocidade

        # Quando parar de andar
        if not andando:
            self.frame = 0

            if self.direcao == "direita":
                self.imagem = self.idle_right
            else:
                self.imagem = self.idle_left