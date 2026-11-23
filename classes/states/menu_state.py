import pygame

from classes.states.game_state import GameState
from classes.systems.assets import carregar_imagem
from classes.systems.audio import Audio
from classes.ui import Botao, NavegadorBotoes, texto_pixel


class MenuState(GameState):
    """Menu principal do jogo."""

    def __init__(self, gerenciador, largura, altura):
        super().__init__(gerenciador)
        self.largura = largura
        self.altura = altura
        self.fundo = carregar_imagem("assets/sprites/telas/Tela_inicio.png",
                                     (largura, altura), (25, 30, 42))
        self.escurecedor = pygame.Surface((largura, altura), pygame.SRCALPHA)
        self.escurecedor.fill((0, 0, 0, 145))
        self.titulo = texto_pixel("HIDDEN WAY", 28, (255, 214, 74), escala=4, sombra=(55, 36, 12))
        textos = ("JOGAR", "OPÇÕES", "CRÉDITOS", "SAIR")
        centros = [(largura // 2, 365 + i * 68) for i in range(len(textos))]
        self.botoes = [Botao(texto, centro, tamanho=(360, 54))
                       for texto, centro in zip(textos, centros)]
        self.navegador = NavegadorBotoes(self.botoes)

    def tratar_eventos(self, eventos):
        for evento in eventos:
            indice = self.navegador.tratar_evento(evento)
            if indice is not None:
                Audio.tocar("clique")
                if indice == 0:
                    from classes.states.inicio_state import InicioState
                    estado = InicioState(self.gerenciador, self.largura, self.altura)
                elif indice == 1:
                    from classes.states.opcoes_state import OpcoesState
                    estado = OpcoesState(
                        self.gerenciador, self.largura, self.altura,
                        voltar=lambda: MenuState(self.gerenciador, self.largura, self.altura))
                elif indice == 2:
                    from classes.states.creditos_state import CreditosState
                    estado = CreditosState(
                        self.gerenciador, self.largura, self.altura,
                        voltar=lambda: MenuState(self.gerenciador, self.largura, self.altura))
                else:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                    return
                self.gerenciador.mudar_estado(estado)
                return

    def atualizar(self, dt=1 / 60):
        pass

    def desenhar(self, janela):
        janela.blit(self.fundo, (0, 0))
        janela.blit(self.escurecedor, (0, 0))
        janela.blit(self.titulo, self.titulo.get_rect(center=(self.largura // 2, 220)))
        self.navegador.desenhar(janela)
