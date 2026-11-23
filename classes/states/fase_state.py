import math
from enum import Enum

import pygame

from classes.entities.chave import Chave, EstadoChave
from classes.entities.amuleto import Amuleto
from classes.entities.bau import Bau, EstadoBau
from classes.entities.inimigo import Inimigo
from classes.entities.player import Player
from classes.entities.porta import Porta
from classes.states.game_state import GameState
from classes.systems.assets import carregar_imagem
from classes.systems.audio import Audio
from classes.systems.combate import SistemaCombate
from classes.systems.cenario import Cenario
from classes.systems.hud import Hud
from classes.systems.particulas import SistemaParticulas
from classes.systems.queda import QuedaNoBuraco, caiu_no_buraco
from classes.systems.transicao import Fade
from classes.ui import texto_pixel


class EstadoFaseGenerica(Enum):
    JOGANDO = "jogando"
    ABRINDO_BAU = "abrindo_bau"
    ENTRANDO_PORTA = "entrando_porta"   # interação com a porta + fade
    MORRENDO = "morrendo"               # animação de morte -> Game Over


class FaseState(GameState):
    """
    Fase genérica (2 a 3): coletar amuletos, abrir o baú e usar a chave para sair.
    """

    ESPESSURA = 36   # altura (px) das plataformas, usada na colisão e no desenho

    def __init__(self, gerenciador, largura, altura, config, indice, vidas=3):
        super().__init__(gerenciador)
        self.largura = largura
        self.altura = altura
        self.config = config
        self.indice = indice
        self.mostrar_debug_paredes = False

        x, y_chao = config.spawn
        self.player = Player(x=x, y=y_chao - int(96 * 0.6), escala=0.6, vidas=vidas)
        self.player.forca_pulo = config.forca_pulo
        # Altura opcional (4º valor); sem ela, a colisão tem a espessura da plataforma desenhada
        self.plataformas = [pygame.Rect(p[0], p[1], p[2], p[3] if len(p) > 3 else self.ESPESSURA)
                            for p in config.plataformas]
        self.paredes = [pygame.Rect(x, y, largura, altura)
                        for x, y, largura, altura in config.paredes]
        self.cenario = Cenario(f"assets/sprites/telas/{config.fundo}.png", largura=largura, altura=altura,
                       eh_plataforma=True, plataformas=self.plataformas, paredes=self.paredes)

        self.particulas = SistemaParticulas()
        self.hud = Hud(largura, altura)
        self.amuletos = [
            Amuleto(cx, cy, self.particulas, indice)
            for indice, (cx, cy) in enumerate(config.amuletos)
        ]
        self.amuletos_coletados = 0
        self.amuletos_recolhidos = [False] * len(self.amuletos)
        self.bau = Bau(self.particulas, config.bau)
        self.chave = None
        self.tem_chave = False
        self.inimigos = [Inimigo(t, x0, x1, y, self.particulas) for t, x0, x1, y in config.inimigos]
        self.combate = SistemaCombate(self.player, self.inimigos, self.particulas)
        self.hud.configurar_jogador(self.player)
        self.espinhos = [pygame.Rect(x, y - 24, w, 24) for x, y, w in config.espinhos]
        self.porta = Porta(
            *config.porta,
            self.particulas,
            mostrar_textura=config.mostrar_textura_porta,
            intensidade_brilho=config.intensidade_brilho_porta,
            halo_anel=config.halo_anel_porta,
        )
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
    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_F3:
                self.mostrar_debug_paredes = not self.mostrar_debug_paredes
            elif (evento.type == pygame.KEYDOWN and evento.key == pygame.K_e
                  and self.estado == EstadoFaseGenerica.JOGANDO):
                self._interagir()
            elif (self.estado == EstadoFaseGenerica.JOGANDO
                  and SistemaCombate.eh_evento_disparo(evento)):
                self.combate.atirar()

    def _interagir(self):
        hitbox = self.player.hitbox()
        if self.bau.estado == EstadoBau.FECHADO and self.bau.perto(hitbox):
            resultado = self.bau.tentar_abrir(
                self.amuletos_coletados == len(self.amuletos))
            if resultado == "sem_amuletos":
                Audio.tocar("bau_negado")
                self.hud.avisar_central("Você precisa dos 3 amuletos!", cor=(255, 180, 130))
            elif resultado == "abrindo":
                Audio.tocar("bau_abrir")
                self._mudar_estado(EstadoFaseGenerica.ABRINDO_BAU)
            return

        if not self.porta.rect.inflate(70, 40).colliderect(hitbox):
            return
        if not self.tem_chave:
            self.hud.avisar_central("Você precisa da chave do baú!", cor=(255, 180, 130))
        elif not self.porta.liberada:
            self.porta.liberar()
            self.hud.avisar_central("Porta desbloqueada!", cor=(170, 255, 190))
        else:
            Audio.tocar("entrar")
            self._mudar_estado(EstadoFaseGenerica.ENTRANDO_PORTA)

    def _mudar_estado(self, novo):
        self.estado = novo
        self.tempo_estado = 0.0

    def atualizar(self, dt=1 / 60):
        self.tempo += dt
        self.tempo_estado += dt
        self.player.atualizar_estado(dt)
        self.particulas.atualizar(dt)
        self.hud.atualizar(dt)
        self.fade_entrada.atualizar(dt)
        self.porta.atualizar(dt)
        if self.bau.atualizar(dt):
            self._bau_aberto()
        for inimigo in self.inimigos:
            inimigo.atualizar(dt)
        for amuleto in self.amuletos:
            amuleto.atualizar(dt)
        if self.chave and self.chave.atualizar(dt):
            self.tem_chave = True
            self.hud.chave_recebida()
            self.hud.avisar_central("Chave Coletada")
            Audio.tocar("chave_hud")

        if self.estado == EstadoFaseGenerica.ABRINDO_BAU:
            self.player.animar(False)
        elif self.estado == EstadoFaseGenerica.JOGANDO:
            self.combate.atualizar(dt)
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

    def _bau_aberto(self):
        self.chave = Chave(*self.bau.rect.center, self.particulas)
        self.chave.coletar(Hud.POS_CHAVE)
        self._mudar_estado(EstadoFaseGenerica.JOGANDO)

    def _atualizar_jogando(self):
        self.player.atualizar_movimento(gravidade_ativada=True, plataformas=self.plataformas,
                        paredes=self.paredes)
        hitbox = self.player.hitbox()

        # Amuletos
        for indice, amuleto in enumerate(self.amuletos):
            if amuleto.estado == EstadoChave.NO_MAPA and hitbox.colliderect(amuleto.hitbox):
                amuleto.coletar(Hud.POS_AMULETOS[indice])
                self.amuletos_recolhidos[indice] = True
                self.amuletos_coletados += 1
                self.hud.avisar_central(
                    f"Amuleto Coletado {self.amuletos_coletados}/{len(self.amuletos)}")
                Audio.tocar("chave")

        # inimigos
        for inimigo in self.inimigos:
            if inimigo.vivo and hitbox.colliderect(inimigo.hitbox):
                if self.player.receber_dano():
                    if self.player.vidas <= 0:
                        self._morrer("Os inimigos acabaram com suas vidas!", "espinho")
                        return
                    self.player.x += -16 if inimigo.x > self.player.x else 16
                    self.hud.avisar_central("Você foi atingido!", cor=(255, 150, 150))

        # espinhos
        for espinho in self.espinhos:
            if hitbox.colliderect(espinho.inflate(-8, -6)):
                self._morrer("Você caiu nos espinhos!", "espinho")
                return

        # buraco
        if caiu_no_buraco(self.player, self.altura):
            self._morrer("Você caiu no buraco!", "queda")
            return

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
                    **proxima_fase(self.indice, self.gerenciador, self.largura, self.altura,
                                   vidas=self.player.vidas)))

    # ------------------------------------------------------------------ desenho
    def desenhar(self, janela):
        self.cenario.desenhar(janela)
        if self.mostrar_debug_paredes:
            for parede in self.paredes:
                pygame.draw.rect(janela, (255, 0, 0), parede, 2)

        cor, topo = self.config.cor_plataforma, self.config.cor_topo
        if self.config.mostrar_plataformas:
            for p in self.plataformas:
                pygame.draw.rect(janela, cor, (p.x, p.y, p.w, p.h))
                pygame.draw.rect(janela, topo, (p.x, p.y, p.w, min(6, p.h)))
                pygame.draw.rect(janela, tuple(c // 3 for c in cor), (p.x, p.y, p.w, p.h), 3)
        for esp in self.espinhos:
            for x in range(esp.x, esp.right, 45):
                janela.blit(self.sprite_espinho, (x, esp.y), (0, 0, min(51, esp.right - x + 6), 24))

        self.porta.desenhar(janela)
        self.bau.desenhar(janela)
        for amuleto in self.amuletos:
            amuleto.desenhar(janela)
        if self.chave:
            self.chave.desenhar(janela)
        for inimigo in self.inimigos:
            inimigo.desenhar(janela)
        self.combate.desenhar(janela)

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
        self._desenhar_prompt(janela)
        self.hud.desenhar_objetivos(
            janela, self.amuletos_recolhidos, self.tem_chave)
        self.hud.desenhar_vidas(janela, self.player)
        self.hud.desenhar(janela, mostrar_chave=False)

        if self.estado == EstadoFaseGenerica.MORRENDO:
            self.queda.desenhar_fade(janela)
        if self.fade_saida:
            self.fade_saida.desenhar(janela)
        self.fade_entrada.desenhar(janela)

    def _desenhar_prompt(self, janela):
        if self.estado != EstadoFaseGenerica.JOGANDO:
            return
        hitbox = self.player.hitbox()
        if self.bau.estado == EstadoBau.FECHADO and self.bau.perto(hitbox):
            texto = "PRESSIONE E PARA ABRIR O BAÚ"
            y = self.bau.rect.top - 52
            centro_x = self.bau.rect.centerx
        elif self.porta.rect.inflate(70, 40).colliderect(hitbox):
            texto = "PRESSIONE E PARA ENTRAR" if self.porta.liberada else "PRESSIONE E PARA ABRIR"
            y = self.porta.rect.top - 42
            centro_x = self.porta.rect.centerx
        else:
            return
        txt = texto_pixel(texto, 8, (255, 255, 255), escala=2)
        y += int(3 * math.sin(pygame.time.get_ticks() / 200))
        janela.blit(txt, txt.get_rect(midtop=(max(txt.get_width() // 2 + 8, centro_x), y)))
