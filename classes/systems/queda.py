import pygame

from classes.systems.audio import Audio
from classes.systems.transicao import Fade

# Limite (em px) a partir do qual o player é considerado dentro do buraco: o pé passou do chão
# mais baixo do mapa (plataforma em y=725) e está quase saindo da tela.
MARGEM_BURACO = 15


def caiu_no_buraco(player, altura_tela):
    return player.y + player.altura > altura_tela - MARGEM_BURACO


class QuedaNoBuraco:
    """
    Sequência de morte por queda: congelamento (hit stop) -> player gira e encolhe caindo ->
    tela escurece. Quando `atualizar` devolve True, o estado da fase deve abrir o Game Over
    usando `quadro` (último quadro do jogo) como fundo.
    """
    T_CONGELA = 0.25
    T_QUEDA = 0.65
    T_FADE = 0.5

    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.ativa = False
        self.tempo = 0.0
        self.quadro = None
        self.fade = None

    def iniciar(self, player, particulas):
        self.ativa = True
        self.tempo = 0.0
        self.fade = Fade(self.largura, self.altura, self.T_FADE, "saida", alpha_max=175)
        Audio.tocar("queda")
        particulas.emitir(player.x + player.largura / 2, player.y + player.altura, 14,
                          [(120, 150, 100), (200, 200, 190), (90, 70, 50)],
                          velocidade=(40, 140), vida=(0.4, 0.9), tam=(2, 4), gravidade=200, angulo=(20, 160))

    def atualizar(self, dt):
        self.tempo += dt
        if self.tempo >= self.T_CONGELA + self.T_QUEDA:
            self.fade.atualizar(dt)
        return self.fade.concluido

    def desenhar_player(self, janela, player):
        t = self.tempo - self.T_CONGELA
        if t <= 0:  # congelado, com um clarão rápido
            janela.blit(player.imagem, (int(player.x), int(player.y)))
            flash = pygame.Surface(player.imagem.get_size(), pygame.SRCALPHA)
            flash.fill((255, 255, 255, int(150 * (1 - self.tempo / self.T_CONGELA))))
            janela.blit(flash, (int(player.x), int(player.y)), special_flags=pygame.BLEND_RGBA_ADD)
            return
        k = min(1.0, t / self.T_QUEDA)
        img = pygame.transform.rotozoom(player.imagem, k * 540, 1 - 0.7 * k)
        img.set_alpha(int(255 * (1 - k * k)))
        centro = (player.x + player.largura / 2, player.y + player.altura / 2 + 70 * t)
        janela.blit(img, img.get_rect(center=(int(centro[0]), int(centro[1]))))

    def desenhar_fade(self, janela):
        """Guarda o quadro atual (sem o escurecimento) e aplica o fade por cima."""
        self.quadro = janela.copy()
        if self.tempo >= self.T_CONGELA + self.T_QUEDA:
            self.fade.desenhar(janela)
