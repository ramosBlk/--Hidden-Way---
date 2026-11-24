import pygame

from classes.entities.pedra import Pedra
from classes.systems.audio import Audio


class SistemaCombate:
    """Gerencia disparos do jogador e colisões das pedras com inimigos."""

    INTERVALO_DISPARO = 0.28

    def __init__(self, jogador, inimigos, particulas):
        self.jogador = jogador
        self.inimigos = inimigos
        self.particulas = particulas
        self.projeteis = []
        self.tempo_disparo = 0.0

    @staticmethod
    def eh_evento_disparo(evento):
        return ((evento.type == pygame.KEYDOWN and evento.key == pygame.K_f)
                or (evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1))

    def atirar(self):
        if self.tempo_disparo > 0:
            return False
        jogador = self.jogador
        direcao = jogador.direcao
        hitbox = jogador.hitbox()
        x = hitbox.right + 5 if direcao == "direita" else hitbox.left - 5
        y = hitbox.centery - 4
        self.projeteis.append(Pedra(x, y, direcao))
        self.tempo_disparo = self.INTERVALO_DISPARO
        jogador.iniciar_animacao_disparo()
        Audio.tocar("pedra_disparo")
        return True

    def atualizar(self, dt):
        self.tempo_disparo = max(0.0, self.tempo_disparo - dt)
        restantes = []
        for pedra in self.projeteis:
            continua = pedra.atualizar(dt)
            trajetoria = pedra.rect.union(pedra.rect_anterior)
            atingiu = False
            for inimigo in self.inimigos:
                hitbox = inimigo.hitbox
                if inimigo.vivo and trajetoria.colliderect(hitbox):
                    inimigo.receber_dano()
                    self.particulas.emitir(
                        *trajetoria.clip(hitbox).center, 8,
                        [(160, 170, 182), (220, 226, 232), (90, 100, 115)],
                        velocidade=(35, 125), vida=(0.2, 0.45), tam=(2, 4))
                    atingiu = True
                    break
            if not atingiu and continua:
                restantes.append(pedra)
        self.projeteis = restantes

    def desenhar(self, janela):
        for pedra in self.projeteis:
            pedra.desenhar(janela)
