import os
import pygame
from classes.systems.colisao import Colisao


class Player:
    def __init__(self, x=50, y=570, escala=1.0):
        self.escala = escala
        self.largura = int(96 * escala)
        self.altura = int(96 * escala)
        self.direcao = "direita"

        self.x = float(x)
        self.y = float(y)
        self.velocidade = 5
        self.colisao = Colisao(largura=1400, altura=760)

        # Física, Pulo e Gravidade
        self.vel_x = 0
        self.vel_y = 0
        self.gravidade = 0.6
        self.forca_pulo = -11
        self.no_chao = False

        # Sistema de Animação
        self.frame = 0
        self.velocidade_animacao = 0.2
        self._carregar_sprites()
        self.imagem = self.idle_right

    def _carregar_sprites(self):
        """Carrega e redimensiona todos os sprites do jogador."""

        def carregar_imagem(caminho):
            try:
                img = pygame.image.load(caminho).convert_alpha()
                return pygame.transform.scale(img, (self.largura, self.altura))
            except (pygame.error, FileNotFoundError):
                return pygame.Surface((self.largura, self.altura))

        base_path = os.path.join("assets", "sprites", "personagem_principal")

        # Idles
        self.idle_right = carregar_imagem(os.path.join(base_path, "rotations", "south-east.png"))
        self.idle_left = carregar_imagem(os.path.join(base_path, "rotations", "south-west.png"))
        self.idle_up = carregar_imagem(os.path.join(base_path, "rotations", "north.png"))
        self.idle_down = carregar_imagem(os.path.join(base_path, "rotations", "south.png"))

        # Animações de movimento
        self.animacao_direita = [carregar_imagem(os.path.join(base_path, "run_right", f"{i}.png")) for i in range(1, 5)]
        self.animacao_esquerda = [carregar_imagem(os.path.join(base_path, "run_left", f"{i}.png")) for i in range(1, 5)]
        self.animacao_cima = [carregar_imagem(os.path.join(base_path, "run_up", f"{i}.png")) for i in range(1, 5)]
        self.animacao_baixo = [carregar_imagem(os.path.join(base_path, "run_low", f"{i}.png")) for i in range(1, 5)]

    def atualizar_movimento(self, gravidade_ativada=False, plataformas=None):
        """Processa entradas do teclado, física e colisão de forma modular."""
        teclas = pygame.key.get_pressed()
        andando = False
        dx = 0
        dy = 0

        # Movimento Horizontal (A e D / Setas)
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            dx -= self.velocidade
            self.direcao = "esquerda"
            andando = True
        elif teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            dx += self.velocidade
            self.direcao = "direita"
            andando = True

        if not gravidade_ativada:
            # --- MODO TELA INICIAL (Top-down livre) ---
            if teclas[pygame.K_w] or teclas[pygame.K_UP]:
                dy -= self.velocidade
                if dx == 0:
                    self.direcao = "cima"
                andando = True
            elif teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
                dy += self.velocidade
                if dx == 0:
                    self.direcao = "baixo"
                andando = True

            # Aplica movimento X com verificação de área livre
            if dx != 0:
                novo_x = self.x + dx
                if self.colisao.pode_andar(novo_x + (self.largura / 2), self.y + self.altura):
                    self.x = novo_x

            # Aplica movimento Y com verificação de área livre
            if dy != 0 and not teclas[pygame.K_SPACE]:
                novo_y = self.y + dy
                if self.colisao.pode_andar(self.x + (self.largura / 2), novo_y + self.altura):
                    self.y = novo_y

            # Pulo simples na tela inicial
            if teclas[pygame.K_SPACE] and self.no_chao:
                self.vel_y = self.forca_pulo
                self.no_chao = False

            if not self.no_chao or self.vel_y != 0:
                self.vel_y += self.gravidade
                self.y += self.vel_y
                if self.y >= 570:
                    self.y = 570
                    self.vel_y = 0
                    self.no_chao = True

        else:
            # --- MODO PLATAFORMA (Mapa 1) ---
            self.vel_x = dx

            # Pulo com Barra de Espaço
            if teclas[pygame.K_SPACE] and self.no_chao:
                self.vel_y = self.forca_pulo
                self.no_chao = False

            # Aplica gravidade vertical
            self.vel_y += self.gravidade
            self.y += self.vel_y

            # Delega a física de colisão horizontal/vertical de plataformas para a classe Colisao
            if plataformas:
                self.colisao.tratar_colisao_plataforma(self, plataformas)
            else:
                self.x += self.vel_x
                # Limites básicos da tela
                self.x = max(0, min(self.x, 1400 - self.largura))

        self._atualizar_animacao(andando)

    def _atualizar_animacao(self, andando):
        """Gerencia os frames de animação do sprite."""
        if andando:
            self.frame += self.velocidade_animacao
            anim_map = {
                "direita": self.animacao_direita,
                "esquerda": self.animacao_esquerda,
                "cima": self.animacao_cima,
                "baixo": self.animacao_baixo
            }
            lista_atual = anim_map.get(self.direcao, self.animacao_direita)

            if self.frame >= len(lista_atual):
                self.frame = 0
            self.imagem = lista_atual[int(self.frame)]
        else:
            self.frame = 0
            idle_map = {
                "direita": self.idle_right,
                "esquerda": self.idle_left,
                "cima": self.idle_up,
                "baixo": self.idle_down
            }
            self.imagem = idle_map.get(self.direcao, self.idle_right)

    def desenhar(self, janela, debug=False):
        if debug:
            self.colisao.desenhar_debug(janela)
        janela.blit(self.imagem, (int(self.x), int(self.y)))