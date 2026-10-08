import math
from enum import Enum

import pygame

from classes.systems.cenario import Cenario
from classes.entities.player import Player
from classes.entities.chave import Chave, EstadoChave
from classes.entities.bau import Bau, EstadoBau
from classes.entities.caverna import Caverna
from classes.states.game_state import GameState
from classes.systems.audio import Audio
from classes.systems.hud import Hud
from classes.systems.particulas import SistemaParticulas
from classes.systems.queda import QuedaNoBuraco, caiu_no_buraco
from classes.systems.transicao import Fade
from classes.ui import texto_pixel


class EstadoFase(Enum):
    JOGANDO = "jogando"                  # controle normal
    ABRINDO_BAU = "abrindo_bau"          # player parado enquanto o baú anima
    ENTRANDO_CAVERNA = "entrando_caverna"  # andar automático + fade
    CAINDO = "caindo"                    # morte por queda -> Game Over


class Mapa1State(GameState):
    # Posição da chave: ilha do toco de árvore (lado direito do mapa)
    POS_CHAVE = (1010, 138)

    def __init__(self, gerenciador, largura, altura):
        super().__init__(gerenciador)
        self.gerenciador = gerenciador
        self.largura = largura
        self.altura = altura

        # Player redimensionado e posicionado no início do Mapa 1
        self.player = Player(x=835, y=668, escala=0.6)

        # Cenário do Mapa 1 (plataformas)
        self.cenario = Cenario(
            caminho_imagem="assets/sprites/telas/Mapa_1.png",
            largura=self.largura,
            altura=self.altura,
            eh_plataforma=True
        )

        # Mecânica chave -> baú -> caverna
        self.particulas = SistemaParticulas()
        self.hud = Hud(largura, altura)
        self.chave = Chave(*self.POS_CHAVE, self.particulas)
        self.bau = Bau(self.particulas)
        self.caverna = Caverna(self.particulas)
        self.tem_chave = False

        self.estado = EstadoFase.JOGANDO
        self.tempo_estado = 0.0
        self.queda = QuedaNoBuraco(largura, altura)
        self.fade_entrada = Fade(largura, altura, 0.7, "entrada")
        self.fade_saida = None

    # ------------------------------------------------------------------ eventos
    def tratar_eventos(self, eventos):
        if self.estado != EstadoFase.JOGANDO:
            return
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_e:
                self._interagir_bau()

    def _interagir_bau(self):
        if not self.bau.perto(self.player.hitbox()):
            return
        resultado = self.bau.tentar_abrir(self.tem_chave)
        if resultado == "sem_chave":
            Audio.tocar("bau_negado")
            self.hud.avisar("Você precisa de uma chave!", cor=(255, 140, 120))
        elif resultado == "abrindo":
            Audio.tocar("bau_abrir")
            self._mudar_estado(EstadoFase.ABRINDO_BAU)

    def _mudar_estado(self, novo):
        self.estado = novo
        self.tempo_estado = 0.0

    # ------------------------------------------------------------------ lógica
    def atualizar(self, dt=1 / 60):
        self.particulas.atualizar(dt)
        self.hud.atualizar(dt)
        self.caverna.atualizar(dt)
        self.fade_entrada.atualizar(dt)
        self.tempo_estado += dt

        if self.chave.atualizar(dt):
            self.hud.chave_recebida()
            Audio.tocar("chave_hud")
        if self.bau.atualizar(dt):
            self._bau_aberto()

        if self.estado == EstadoFase.JOGANDO:
            self._atualizar_jogando()
        elif self.estado == EstadoFase.ABRINDO_BAU:
            self.player.animar(False)  # player parado olhando o baú; a transição ocorre em _bau_aberto
        elif self.estado == EstadoFase.ENTRANDO_CAVERNA:
            self._atualizar_entrando(dt)
        elif self.estado == EstadoFase.CAINDO:
            if self.queda.atualizar(dt):
                from classes.states.game_over_state import GameOverState
                self.gerenciador.mudar_estado(GameOverState(
                    self.gerenciador, self.largura, self.altura,
                    fundo=self.queda.quadro,
                    reiniciar=lambda: Mapa1State(self.gerenciador, self.largura, self.altura),
                    motivo="Você caiu no buraco!"))

    def _atualizar_jogando(self):
        # A parede da caverna só existe enquanto ela estiver trancada
        self.player.atualizar_movimento(gravidade_ativada=True, plataformas=self.cenario.plataformas,
                                        paredes=self.cenario.paredes + self.caverna.solidos())
        hitbox = self.player.hitbox()

        # Chave: coletada uma única vez
        if not self.tem_chave and self.chave.estado == EstadoChave.NO_MAPA and hitbox.colliderect(self.chave.hitbox):
            self.tem_chave = True
            self.chave.coletar(Hud.POS_CHAVE)
            self.hud.avisar("CHAVE OBTIDA!")
            Audio.tocar("chave")

        # Caverna trancada: avisa ao encostar na pedra
        if not self.caverna.liberada and hitbox.colliderect(self.caverna.parede.inflate(16, 0)):
            self.hud.avisar("A passagem está selada...", cor=(200, 200, 210))

        # Caverna liberada: entrar inicia a transição de fase
        if self.caverna.liberada and hitbox.colliderect(self.caverna.entrada):
            Audio.tocar("entrar")
            self._mudar_estado(EstadoFase.ENTRANDO_CAVERNA)

        # Buraco
        if caiu_no_buraco(self.player, self.altura):
            self.queda.iniciar(self.player, self.particulas)
            self._mudar_estado(EstadoFase.CAINDO)

    def _bau_aberto(self):
        """Fim da animação do baú: consome a chave e libera a caverna."""
        self.tem_chave = False
        self.caverna.liberar()
        Audio.tocar("caverna")
        self.hud.avisar("PASSAGEM DESBLOQUEADA!", duracao=3.0, cor=(170, 255, 190))
        self._mudar_estado(EstadoFase.JOGANDO)

    def _atualizar_entrando(self, dt):
        alvo = self.caverna.CENTRO[0]
        centro_player = self.player.x + self.player.largura / 2
        if abs(centro_player - alvo) > 2:  # anda até o meio da entrada
            self.player.direcao = "direita" if alvo > centro_player else "esquerda"
            self.player.x += math.copysign(min(140 * dt, abs(alvo - centro_player)), alvo - centro_player)
            self.player.animar(True)
        else:
            self.player.animar(False)
        self.caverna.brilho_extra = min(1.0, self.tempo_estado / 1.4)

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
                    **proxima_fase(0, self.gerenciador, self.largura, self.altura)))

    # ------------------------------------------------------------------ desenho
    def desenhar(self, janela):
        self.cenario.desenhar(janela)
        self.caverna.desenhar(janela)
        self.bau.desenhar(janela)
        self.chave.desenhar(janela)

        if self.estado == EstadoFase.CAINDO:
            self.queda.desenhar_player(janela, self.player)
        elif self.estado == EstadoFase.ENTRANDO_CAVERNA:
            # o player vai sumindo conforme entra na luz
            img = self.player.imagem.copy()
            progresso = min(1.0, max(0.0, (self.tempo_estado - 0.5) / 0.8))
            img.set_alpha(int(255 * (1 - progresso)))
            janela.blit(img, (int(self.player.x), int(self.player.y)))
        else:
            self.player.desenhar(janela)

        self.particulas.desenhar(janela)
        self._desenhar_prompt_bau(janela)
        self.hud.desenhar(janela, mostrar_chave=self.tem_chave and not self.chave.voando)

        if self.estado == EstadoFase.CAINDO:
            self.queda.desenhar_fade(janela)
        if self.fade_saida:
            self.fade_saida.desenhar(janela)
        self.fade_entrada.desenhar(janela)

    def _desenhar_prompt_bau(self, janela):
        if (self.estado == EstadoFase.JOGANDO and self.bau.estado == EstadoBau.FECHADO
                and self.bau.perto(self.player.hitbox())):
            txt = texto_pixel("PRESSIONE E PARA ABRIR", 9, (255, 255, 255), escala=2)
            y = self.bau.rect.top - 52 + int(3 * math.sin(pygame.time.get_ticks() / 200))
            janela.blit(txt, txt.get_rect(midtop=(max(txt.get_width() // 2 + 8, self.bau.rect.centerx), y)))
