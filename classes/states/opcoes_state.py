import pygame

from classes.states.game_state import GameState
from classes.systems.assets import carregar_imagem
from classes.systems.audio import Audio
from classes.systems.configuracoes import Configuracoes
from classes.ui import Botao, SeletorOpcoes, Slider, desenhar_placa, texto_pixel


class OpcoesState(GameState):
    """Tela para ajustar volume, qualidade gráfica e brilho."""

    def __init__(self, gerenciador, largura, altura, voltar):
        super().__init__(gerenciador)
        self.largura = largura
        self.altura = altura
        self.voltar = voltar
        self.fundo = carregar_imagem("assets/sprites/telas/Tela_inicio.png",
                                     (largura, altura), (25, 30, 42))
        self.escurecedor = pygame.Surface((largura, altura), pygame.SRCALPHA)
        self.escurecedor.fill((0, 0, 0, 155))
        self.placa = pygame.Rect(0, 0, 1040, 540)
        self.placa.center = (largura // 2, altura // 2)

        centro_x = largura // 2
        self.volume = Slider("VOLUME", (centro_x, 280), Configuracoes.volume)
        self.qualidade = SeletorOpcoes(
            ("BAIXA", "MÉDIA", "ALTA"), (centro_x, 375), Configuracoes.qualidade)
        self.brilho = Slider("BRILHO", (centro_x, 470), Configuracoes.brilho)
        self.botao_voltar = Botao("VOLTAR", (centro_x, 580), tamanho=(320, 52))
        self.indice_selecionado = 0
        self.linhas = []
        for y in (280, 375, 470, 580):
            ret = pygame.Rect(0, 0, 960, 56)
            ret.center = (centro_x, y)
            self.linhas.append(ret)
        self._volume_arrastou = False

    def _selecionar_linha(self, indice):
        indice = indice % len(self.linhas)
        if indice != self.indice_selecionado:
            self.indice_selecionado = indice
            Audio.tocar("selecao")

    def _voltar(self):
        Configuracoes.salvar()
        self.gerenciador.mudar_estado(self.voltar())

    def _atualizar_volume(self, evento):
        mudou = self.volume.tratar_evento(evento, self.indice_selecionado == 0)
        if mudou:
            Configuracoes.definir_volume(self.volume.valor)
            if evento.type == pygame.KEYDOWN:
                Audio.tocar("clique")
            elif evento.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
                self._volume_arrastou = True

    def _atualizar_brilho(self, evento):
        if self.brilho.tratar_evento(evento, self.indice_selecionado == 2):
            Configuracoes.definir_brilho(self.brilho.valor)

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self._voltar()
                    return
                if evento.key in (pygame.K_UP, pygame.K_w):
                    self._selecionar_linha(self.indice_selecionado - 1)
                    continue
                if evento.key in (pygame.K_DOWN, pygame.K_s):
                    self._selecionar_linha(self.indice_selecionado + 1)
                    continue
                if (evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE)
                        and self.indice_selecionado == 3):
                    Audio.tocar("clique")
                    self._voltar()
                    return

            if (evento.type == pygame.MOUSEMOTION and not self.volume.arrastando
                    and not self.brilho.arrastando):
                for indice, linha in enumerate(self.linhas):
                    if linha.collidepoint(evento.pos):
                        self._selecionar_linha(indice)
                        break

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                for indice, linha in enumerate(self.linhas):
                    if linha.collidepoint(evento.pos):
                        self._selecionar_linha(indice)
                        break

            if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                volume_arrastava = self.volume.arrastando
                brilho_arrastava = self.brilho.arrastando
                self.volume.tratar_evento(evento, self.indice_selecionado == 0)
                self.brilho.tratar_evento(evento, self.indice_selecionado == 2)
                if volume_arrastava:
                    if self._volume_arrastou:
                        Audio.tocar("clique")
                    self._volume_arrastou = False
                if brilho_arrastava:
                    Configuracoes.definir_brilho(self.brilho.valor)
                continue

            self._atualizar_volume(evento)
            self._atualizar_brilho(evento)
            mudou_qualidade = self.qualidade.tratar_evento(
                evento, self.indice_selecionado == 1)
            if mudou_qualidade:
                Configuracoes.definir_qualidade(self.qualidade.valor)
                Audio.tocar("clique")

            if (evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1
                    and self.botao_voltar.rect.collidepoint(evento.pos)):
                Audio.tocar("clique")
                self._voltar()
                return

    def atualizar(self, dt=1 / 60):
        pass

    def desenhar(self, janela):
        janela.blit(self.fundo, (0, 0))
        janela.blit(self.escurecedor, (0, 0))
        desenhar_placa(janela, self.placa)
        titulo = texto_pixel("OPÇÕES", 18, (255, 214, 74), escala=3)
        janela.blit(titulo, titulo.get_rect(center=(self.largura // 2, self.placa.top + 65)))
        self.volume.desenhar(janela, self.indice_selecionado == 0)
        self.qualidade.desenhar(janela, self.indice_selecionado == 1)
        self.brilho.desenhar(janela, self.indice_selecionado == 2)
        self.botao_voltar.desenhar(janela, self.indice_selecionado == 3)
