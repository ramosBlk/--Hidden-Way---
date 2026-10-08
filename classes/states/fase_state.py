import math
from enum import Enum

import pygame

from classes.entities.chave import Chave, EstadoChave
from classes.entities.inimigo import Inimigo
from classes.entities.player import Player
from classes.entities.porta import Porta
from classes.states.game_state import GameState
from classes.systems.assets import carregar_imagem
from classes.systems.audio import Audio
from classes.systems.cenario import Cenario
from classes.systems.hud import Hud
from classes.systems.particulas import SistemaParticulas
from classes.systems.queda import QuedaNoBuraco, caiu_no_buraco
from classes.systems.transicao import Fade


class EstadoFaseGenerica(Enum):
    JOGANDO = "jogando"
    ENTRANDO_PORTA = "entrando_porta"   # andar automático até a porta + fade
    MORRENDO = "morrendo"               # animação de morte -> Game Over


class FaseState(GameState):
    """
    Fase genérica (2 a 5), descrita por uma ConfigFase: coletar TODAS as chaves abre a porta;
    inimigos (pisão derrota) e espinhos matam; cair no buraco também.
    """

    def __init__(self, gerenciador, largura, altura, config, indice):
        super().__init__(gerenciador)
        self.largura = largura
        self.altura = altura
        self.config = config
        self.indice = indice

        x, y_chao = config.spawn
        self.player = Player(x=x, y=y_chao - int(96 * 0.6), escala=0.6)
        self.plataformas = [pygame.Rect(x, y, w, 14) for x, y, w in config.plataformas]
        self.cenario = Cenario(f"assets/sprites/telas/{config.fundo}.png", largura=largura, altura=altura,
                               eh_plataforma=True, plataformas=self.plataformas, paredes=[])

        self.particulas = SistemaParticulas()
        self.hud = Hud(largura, altura)
        self.chaves = [Chave(cx, cy, self.particulas) for cx, cy in config.chaves]
        self.chaves_chegaram = 0     # chaves que já "voaram" até a HUD (contador exibido)
        self.inimigos = [Inimigo(t, x0, x1, y, self.particulas) for t, x0, x1, y in config.inimigos]
        self.espinhos = [pygame.Rect(x, y - 24, w, 24) for x, y, w in config.espinhos]
        self.porta = Porta(*config.porta, self.particulas)
        self.sprite_espinho = carregar_imagem("assets/sprites/itens/espinho.png", (51, 24), (200, 205, 215))

        self.estado = EstadoFaseGenerica.JOGANDO
        self.tempo_estado = 0.0
        self.tempo = 0.0
        self.motivo_morte = ""
        self.queda = QuedaNoBuraco(largura, altura)
        self.fade_entrada = Fade(largura, altura, 0.8, "entrada")
        self.fade_saida = None
        self.hud.avisar(config.nome, duracao=3.0)

    # ------------------------------------------------------------------ lógica
    def _mudar_estado(self, novo):
        self.estado = novo
        self.tempo_estado = 0.0

    def atualizar(self, dt=1 / 60):
        self.tempo += dt
        self.tempo_estado += dt
        self.particulas.atualizar(dt)
        self.hud.atualizar(dt)
        self.fade_entrada.atualizar(dt)
        self.porta.atualizar(dt)
        for inimigo in self.inimigos:
            inimigo.atualizar(dt)
        for chave in self.chaves:
            if chave.atualizar(dt):
                self.chaves_chegaram += 1
                self.hud.chave_recebida()
                Audio.tocar("chave_hud")

        if self.estado == EstadoFaseGenerica.JOGANDO:
            self._atualizar_jogando()
        elif self.estado == EstadoFaseGenerica.ENTRANDO_PORTA:
            self._atualizar_entrando(dt)
        elif self.estado == EstadoFaseGenerica.MORRENDO and self.queda.atualizar(dt):
            from classes.states.game_over_state import GameOverState
            from classes.systems.fases import criar_fase
            self.gerenciador.mudar_estado(GameOverState(
                self.gerenciador, self.largura, self.altura, fundo=self.queda.quadro,
                reiniciar=lambda: criar_fase(self.indice, self.gerenciador, self.largura, self.altura),
                motivo=self.motivo_morte))

    def _atualizar_jogando(self):
        self.player.atualizar_movimento(gravidade_ativada=True, plataformas=self.plataformas, paredes=[])
        hitbox = self.player.hitbox()

        # chaves
        for chave in self.chaves:
            if chave.estado == EstadoChave.NO_MAPA and hitbox.colliderect(chave.hitbox):
                chave.coletar(Hud.POS_CHAVE)
                Audio.tocar("chave")
                coletadas = sum(c.estado != EstadoChave.NO_MAPA for c in self.chaves)
                if coletadas == len(self.chaves):
                    self.porta.liberar()
                    self.hud.avisar("PORTA DESBLOQUEADA!", duracao=3.0, cor=(170, 255, 190))
                else:
                    self.hud.avisar(f"CHAVE OBTIDA! Faltam {len(self.chaves) - coletadas}")

        # inimigos
        for inimigo in self.inimigos:
            if inimigo.vivo and hitbox.colliderect(inimigo.hitbox):
                if inimigo.pisado_por(hitbox, self.player.vel_y):
                    inimigo.derrotar()
                    self.player.vel_y = -9      # quique
                    self.player.no_chao = False
                else:
                    self._morrer("Um inimigo te pegou!", "espinho")
                    return

        # espinhos
        for espinho in self.espinhos:
            if hitbox.colliderect(espinho.inflate(-8, -6)):
                self._morrer("Você caiu nos espinhos!", "espinho")
                return

        # buraco
        if caiu_no_buraco(self.player, self.altura):
            self._morrer("Você caiu no buraco!", "queda")
            return

        # porta
        if hitbox.colliderect(self.porta.entrada):
            if self.porta.liberada:
                Audio.tocar("entrar")
                self._mudar_estado(EstadoFaseGenerica.ENTRANDO_PORTA)
            else:
                faltam = len(self.chaves) - sum(c.estado != EstadoChave.NO_MAPA for c in self.chaves)
                self.hud.avisar(f"A porta está trancada! Faltam {faltam} chave(s)", cor=(255, 140, 120))

    def _morrer(self, motivo, som):
        self.motivo_morte = motivo
        self.queda.iniciar(self.player, self.particulas, som=som)
        self._mudar_estado(EstadoFaseGenerica.MORRENDO)

    def _atualizar_entrando(self, dt):
        alvo = self.porta.rect.centerx
        centro = self.player.x + self.player.largura / 2
        if abs(centro - alvo) > 2:
            self.player.direcao = "direita" if alvo > centro else "esquerda"
            self.player.x += math.copysign(min(140 * dt, abs(alvo - centro)), alvo - centro)
            self.player.animar(True)
        else:
            self.player.animar(False)
        self.porta.brilho_extra = min(1.0, self.tempo_estado / 1.4)

        if self.tempo_estado >= 0.9 and self.fade_saida is None:
            self.fade_saida = Fade(self.largura, self.altura, 1.0, "saida")
            Audio.tocar("transicao")
        if self.fade_saida:
            self.fade_saida.atualizar(dt)
            if self.fade_saida.concluido:
                from classes.states.fase_completa_state import FaseCompletaState
                from classes.systems.fases import proxima_fase
                self.gerenciador.mudar_estado(FaseCompletaState(
                    self.gerenciador, self.largura, self.altura,
                    **proxima_fase(self.indice, self.gerenciador, self.largura, self.altura)))

    # ------------------------------------------------------------------ desenho
    def desenhar(self, janela):
        self.cenario.desenhar(janela)
        cor, topo = self.config.cor_plataforma, self.config.cor_topo
        for p in self.plataformas:
            pygame.draw.rect(janela, cor, (p.x, p.y, p.w, 36))
            pygame.draw.rect(janela, topo, (p.x, p.y, p.w, 6))
            pygame.draw.rect(janela, tuple(c // 3 for c in cor), (p.x, p.y, p.w, 36), 3)
        for esp in self.espinhos:
            for x in range(esp.x, esp.right, 45):
                janela.blit(self.sprite_espinho, (x, esp.y), (0, 0, min(51, esp.right - x + 6), 24))

        self.porta.desenhar(janela)
        for chave in self.chaves:
            chave.desenhar(janela)
        for inimigo in self.inimigos:
            inimigo.desenhar(janela)

        if self.estado == EstadoFaseGenerica.MORRENDO:
            self.queda.desenhar_player(janela, self.player)
        elif self.estado == EstadoFaseGenerica.ENTRANDO_PORTA:
            img = self.player.imagem.copy()
            progresso = min(1.0, max(0.0, (self.tempo_estado - 0.5) / 0.8))
            img.set_alpha(int(255 * (1 - progresso)))
            janela.blit(img, (int(self.player.x), int(self.player.y)))
        else:
            self.player.desenhar(janela)

        self.particulas.desenhar(janela)
        self.hud.desenhar_contador(janela, self.chaves_chegaram, len(self.chaves))
        self.hud.desenhar(janela, mostrar_chave=False)

        if self.estado == EstadoFaseGenerica.MORRENDO:
            self.queda.desenhar_fade(janela)
        if self.fade_saida:
            self.fade_saida.desenhar(janela)
        self.fade_entrada.desenhar(janela)
