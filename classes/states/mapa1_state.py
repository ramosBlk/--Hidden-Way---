import math
from enum import Enum

import pygame

from classes.systems.cenario import Cenario
from classes.entities.player import Player
from classes.entities.chave import Chave, EstadoChave
from classes.entities.amuleto import Amuleto
from classes.entities.bau import Bau, EstadoBau
from classes.entities.caverna import Caverna
from classes.entities.inimigo import Inimigo
from classes.states.game_state import GameState
from classes.systems.audio import Audio
from classes.systems.combate import SistemaCombate
from classes.systems.hud import Hud
from classes.systems.particulas import SistemaParticulas
from classes.systems.queda import QuedaNoBuraco, caiu_no_buraco
from classes.systems.transicao import Fade
from classes.ui import texto_pixel


class EstadoFase(Enum):
    JOGANDO = "jogando"                  # controle normal
    ABRINDO_BAU = "abrindo_bau"          # player parado enquanto o baú anima
    ENTRANDO_CAVERNA = "entrando_caverna"  # interação com a passagem + fade
    CAINDO = "caindo"                    # morte por queda -> Game Over


class Mapa1State(GameState):
    POS_AMULETOS = ((160, 432), (700, 311), (1010, 138))

    def __init__(self, gerenciador, largura, altura, vidas=3):
        super().__init__(gerenciador)
        self.gerenciador = gerenciador
        self.largura = largura
        self.altura = altura

        # Player redimensionado e posicionado no início do Mapa 1
        self.player = Player(x=835, y=668, escala=0.6, vidas=vidas)

        # Cenário do Mapa 1 (plataformas)
        self.cenario = Cenario(
            caminho_imagem="assets/sprites/telas/Mapa_1.png",
            largura=self.largura,
            altura=self.altura,
            eh_plataforma=True
        )

        # Mecânica amuletos -> baú/chave -> caverna
        self.particulas = SistemaParticulas()
        self.hud = Hud(largura, altura)
        self.amuletos = [
            Amuleto(x, y, self.particulas, indice)
            for indice, (x, y) in enumerate(self.POS_AMULETOS)
        ]
        self.amuletos_coletados = 0
        self.amuletos_recolhidos = [False] * len(self.amuletos)
        self.chave = None
        self.bau = Bau(self.particulas)
        self.caverna = Caverna(self.particulas)
        self.inimigos = [
            Inimigo("slime", 300, 370, 537, self.particulas),
            Inimigo("slime", 470, 630, 448, self.particulas),
            Inimigo("slime", 680, 720, 329, self.particulas),
            Inimigo("slime", 1230, 1360, 233, self.particulas),
        ]
        self.combate = SistemaCombate(self.player, self.inimigos, self.particulas)
        self.hud.configurar_jogador(self.player)
        self.tem_chave = False
        self.motivo_morte = "Você caiu no buraco!"

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
                self._interagir()
            elif (self.estado == EstadoFase.JOGANDO
                  and SistemaCombate.eh_evento_disparo(evento)):
                self.combate.atirar()

    def _interagir(self):
        hitbox = self.player.hitbox()
        if self.bau.estado == EstadoBau.FECHADO and self.bau.perto(hitbox):
            resultado = self.bau.tentar_abrir(self.amuletos_coletados == len(self.amuletos))
            if resultado == "sem_amuletos":
                Audio.tocar("bau_negado")
                self.hud.avisar_central("Você precisa dos 3 amuletos!", cor=(255, 180, 130))
            elif resultado == "abrindo":
                Audio.tocar("bau_abrir")
                self._mudar_estado(EstadoFase.ABRINDO_BAU)
            return

        if not self.caverna.entrada.inflate(70, 40).colliderect(hitbox):
            return
        if not self.tem_chave:
            self.hud.avisar_central("Você precisa da chave do baú!", cor=(255, 180, 130))
        elif not self.caverna.liberada:
            self.caverna.liberar()
            self.hud.avisar_central("Passagem desbloqueada!", cor=(170, 255, 190))
        else:
            Audio.tocar("entrar")
            self._mudar_estado(EstadoFase.ENTRANDO_CAVERNA)

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
        self.player.atualizar_estado(dt)

        if self.chave and self.chave.atualizar(dt):
            self.tem_chave = True
            self.hud.chave_recebida()
            self.hud.avisar_central("Chave Coletada")
            Audio.tocar("chave_hud")
        for amuleto in self.amuletos:
            amuleto.atualizar(dt)
        if self.bau.atualizar(dt):
            self._bau_aberto()

        if self.estado == EstadoFase.JOGANDO:
            for inimigo in self.inimigos:
                inimigo.atualizar(dt)
            self.combate.atualizar(dt)
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
                    motivo=self.motivo_morte))

    def _atualizar_jogando(self):
        # A parede da caverna só existe enquanto ela estiver trancada
        self.player.atualizar_movimento(gravidade_ativada=True, plataformas=self.cenario.plataformas,
                                        paredes=self.cenario.paredes + self.caverna.solidos())
        hitbox = self.player.hitbox()

        for inimigo in self.inimigos:
            if inimigo.vivo and hitbox.colliderect(inimigo.hitbox):
                if self.player.receber_dano():
                    if self.player.vidas <= 0:
                        self.motivo_morte = "Os inimigos acabaram com suas vidas!"
                        self.queda.iniciar(self.player, self.particulas, som="game_over")
                        self._mudar_estado(EstadoFase.CAINDO)
                        return
                    self.player.x += -16 if inimigo.x > self.player.x else 16
                    self.hud.avisar_central("Você foi atingido!", cor=(255, 150, 150))

        for indice, amuleto in enumerate(self.amuletos):
            if amuleto.estado == EstadoChave.NO_MAPA and hitbox.colliderect(amuleto.hitbox):
                amuleto.coletar(Hud.POS_AMULETOS[indice])
                self.amuletos_recolhidos[indice] = True
                self.amuletos_coletados += 1
                self.hud.avisar_central(
                    f"Amuleto Coletado {self.amuletos_coletados}/{len(self.amuletos)}")
                Audio.tocar("chave")

        # Buraco
        if caiu_no_buraco(self.player, self.altura):
            self.motivo_morte = "Você caiu no buraco!"
            self.queda.iniciar(self.player, self.particulas)
            self._mudar_estado(EstadoFase.CAINDO)

    def _bau_aberto(self):
        """Fim da animação do baú: revela a chave e inicia sua coleta."""
        self.chave = Chave(*self.bau.rect.center, self.particulas)
        self.chave.coletar(Hud.POS_CHAVE)
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
                    **proxima_fase(0, self.gerenciador, self.largura, self.altura,
                                   vidas=self.player.vidas)))

    # ------------------------------------------------------------------ desenho
    def desenhar(self, janela):
        self.cenario.desenhar(janela)
        self.caverna.desenhar(janela)
        self.bau.desenhar(janela)
        for amuleto in self.amuletos:
            amuleto.desenhar(janela)
        if self.chave:
            self.chave.desenhar(janela)
        for inimigo in self.inimigos:
            inimigo.desenhar(janela)
        self.combate.desenhar(janela)

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
        self._desenhar_prompt(janela)
        self.hud.desenhar_objetivos(
            janela, self.amuletos_recolhidos, self.tem_chave)
        self.hud.desenhar_vidas(janela, self.player)
        self.hud.desenhar(janela, mostrar_chave=False)

        if self.estado == EstadoFase.CAINDO:
            self.queda.desenhar_fade(janela)
        if self.fade_saida:
            self.fade_saida.desenhar(janela)
        self.fade_entrada.desenhar(janela)

    def _desenhar_prompt(self, janela):
        if self.estado != EstadoFase.JOGANDO:
            return
        hitbox = self.player.hitbox()
        if self.bau.estado == EstadoBau.FECHADO and self.bau.perto(hitbox):
            texto = "PRESSIONE E PARA ABRIR O BAÚ"
            y = self.bau.rect.top - 52
            centro_x = self.bau.rect.centerx
        elif self.caverna.entrada.inflate(70, 40).colliderect(hitbox):
            texto = "PRESSIONE E PARA ENTRAR" if self.caverna.liberada else "PRESSIONE E PARA ABRIR"
            y = self.caverna.entrada.top - 42
            centro_x = self.caverna.entrada.centerx
        else:
            return
        txt = texto_pixel(texto, 8, (255, 255, 255), escala=2)
        y += int(3 * math.sin(pygame.time.get_ticks() / 200))
        janela.blit(txt, txt.get_rect(midtop=(max(txt.get_width() // 2 + 8, centro_x), y)))
