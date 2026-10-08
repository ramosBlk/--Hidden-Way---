import pygame
from classes.systems.audio import Audio
from classes.systems.colisao import Colisao
from classes.systems.sprites_player import SpritesPlayer


class Player:
    def __init__(self, x=50, y=570, escala=1.0):
        self.escala = escala
        self.largura = int(96 * escala)
        self.altura = int(96 * escala)
        self.direcao = "direita"

        # Hitbox: metade central do sprite (as laterais da imagem são transparentes)
        self.hitbox_offset_x = int(self.largura * 0.25)
        self.hitbox_largura = int(self.largura * 0.5)

        self.x = float(x)
        self.y = float(y)
        self.velocidade = 3.5
        self.colisao = Colisao(largura=1400, altura=760)

        # Física: altura do pulo ≈ forca_pulo² / (2 * gravidade)  (-13.5 ≈ 150 px)
        self.vel_x = 0
        self.vel_y = 0
        self.gravidade = 0.6
        self.forca_pulo = -13.5
        self.no_chao = False

        # Animação
        self.frame = 0
        self.velocidade_animacao = 0.2
        self.sprites = SpritesPlayer((self.largura, self.altura))
        self.imagem = self.sprites.idle_de("direita")

    # ------------------------------------------------------------------ movimento
    def atualizar_movimento(self, gravidade_ativada=False, plataformas=None, paredes=None):
        """Lê o teclado e delega para o modo de movimento atual."""
        teclas = pygame.key.get_pressed()
        dx = self._ler_horizontal(teclas)

        if gravidade_ativada:
            self._mover_plataforma(teclas, dx, (plataformas or []) + (paredes or []))
            andando = dx != 0
        else:
            andando = self._mover_topdown(teclas, dx)

        self._atualizar_animacao(andando)

    def _ler_horizontal(self, teclas):
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            self.direcao = "esquerda"
            return -self.velocidade
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            self.direcao = "direita"
            return self.velocidade
        return 0

    def _pular(self, com_som=False):
        self.vel_y = self.forca_pulo
        self.no_chao = False
        if com_som:
            Audio.tocar("pulo")

    def _mover_topdown(self, teclas, dx):
        """Tela inicial: movimento livre nos 4 sentidos + pulo simples. Retorna se está andando."""
        dy = 0
        if teclas[pygame.K_w] or teclas[pygame.K_UP]:
            dy = -self.velocidade
        elif teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            dy = self.velocidade

        if dy and dx == 0:
            self.direcao = "cima" if dy < 0 else "baixo"

        meio = self.largura / 2
        if dx and self.colisao.pode_andar(self.x + dx + meio, self.y + self.altura):
            self.x += dx
        if dy and not teclas[pygame.K_SPACE] and self.colisao.pode_andar(self.x + meio, self.y + dy + self.altura):
            self.y += dy

        if teclas[pygame.K_SPACE] and self.no_chao:
            self._pular()

        if not self.no_chao or self.vel_y != 0:
            self.vel_y += self.gravidade
            self.y += self.vel_y
            if self.y >= 570:
                self.y, self.vel_y, self.no_chao = 570, 0, True

        return dx != 0 or dy != 0

    def _mover_plataforma(self, teclas, dx, solidos):
        """Mapas de plataforma: gravidade + colisão com plataformas e paredes."""
        self.vel_x = dx

        if teclas[pygame.K_SPACE] and self.no_chao:
            self._pular(com_som=True)

        self.vel_y += self.gravidade

        if solidos:
            self.colisao.tratar_colisao_plataforma(self, solidos)
        else:
            self.y += self.vel_y
            self.x = max(0, min(self.x + self.vel_x, 1400 - self.largura))

    # ------------------------------------------------------------------ animação
    def animar(self, andando):
        """Avança a animação sem processar input (cutscenes/andar automático)."""
        self._atualizar_animacao(andando)

    def _atualizar_animacao(self, andando):
        # No ar: o frame do pulo acompanha a física (0 = saída do chão, 0.5 = pico, 1 = queda)
        if not self.no_chao:
            pulo = self.sprites.pulo_de(self.direcao)
            if pulo:
                progresso = (self.vel_y - self.forca_pulo) / (-2 * self.forca_pulo)
                self.imagem = pulo[max(0, min(len(pulo) - 1, int(progresso * len(pulo))))]
                return

        if andando:
            lista = self.sprites.corrida_de(self.direcao)
            self.frame += self.velocidade_animacao
            if self.frame >= len(lista):
                self.frame = 0
            self.imagem = lista[int(self.frame)]
        else:
            self.frame = 0
            self.imagem = self.sprites.idle_de(self.direcao)

    # ------------------------------------------------------------------ utilidades
    def hitbox(self):
        """Retângulo de colisão do player (usado por itens, baú, caverna...)."""
        return pygame.Rect(int(self.x) + self.hitbox_offset_x, int(self.y), self.hitbox_largura, self.altura)

    def desenhar(self, janela, debug=False):
        if debug:
            self.colisao.desenhar_debug(janela)
        janela.blit(self.imagem, (int(self.x), int(self.y)))