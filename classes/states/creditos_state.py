import pygame

from classes.states.game_state import GameState
from classes.systems.assets import carregar_imagem
from classes.systems.audio import Audio
from classes.ui import Botao, NavegadorBotoes, desenhar_placa, texto_pixel


def quebrar_linha_por_largura(texto, largura, base=8, escala=2):
    """Quebra um parágrafo em linhas que cabem na largura informada."""
    palavras = texto.split()
    linhas = []
    linha = ""
    for palavra in palavras:
        candidata = f"{linha} {palavra}".strip()
        if linha and texto_pixel(candidata, base, escala=escala).get_width() > largura:
            linhas.append(linha)
            linha = palavra
        else:
            linha = candidata
    if linha:
        linhas.append(linha)
    return linhas


class CreditosState(GameState):
    """Créditos do jogo e botão para retornar ao menu."""

    SECOES = (
        ("SOBRE O JOGO",
         "Hidden Way é uma aventura 2D de plataforma, exploração e mistério. No modo single-player, "
         "o jogador explora cenários, pula entre plataformas, coleta chaves, enfrenta inimigos e "
         "encontra a saída de cada fase."),
        ("DIFERENCIAL",
         "a proposta de jogos como Fireboy and Watergirl trazida para um modo single-player, "
         "mantendo a exploração e a resolução de desafios com apenas um personagem."),
        ("EQUIPE",
         "Pedro Henrique Faria Silva, Pedro Henrique Ramos de Carvalho, Raphael Antonio Ferreira "
         "e Victor Hugo Silva de Assis."),
        ("PROJETO ACADÊMICO",
         "desenvolvido para a disciplina Programação para Jogos do curso de Ciência da Computação "
         "do Centro Universitário Presidente Antônio Carlos (UNIPAC), sob orientação do professor "
         "Rodrigo Fernandes dos Santos."),
        ("TECNOLOGIAS", "Python, Pygame-CE, Git e GitHub."),
    )

    def __init__(self, gerenciador, largura, altura, voltar):
        super().__init__(gerenciador)
        self.largura = largura
        self.altura = altura
        self.voltar = voltar
        self.fundo = carregar_imagem("assets/sprites/telas/Tela_inicio.png",
                                     (largura, altura), (25, 30, 42))
        self.escurecedor = pygame.Surface((largura, altura), pygame.SRCALPHA)
        self.escurecedor.fill((0, 0, 0, 155))
        self.placa = pygame.Rect(0, 0, 1160, 670)
        self.placa.center = (largura // 2, altura // 2)
        self.botao = Botao("VOLTAR", (largura // 2, self.placa.bottom - 42),
                           tamanho=(300, 48))
        self.navegador = NavegadorBotoes([self.botao])
        self.linhas = []
        y = self.placa.top + 112
        largura_texto = self.placa.width - 100
        for titulo, conteudo in self.SECOES:
            self.linhas.append((texto_pixel(titulo, 9, (255, 214, 74), escala=2), 0, y))
            y += 25
            for linha in quebrar_linha_por_largura(conteudo, largura_texto):
                imagem = texto_pixel(linha, 8, (235, 235, 240), escala=2)
                self.linhas.append((imagem, 0, y))
                y += imagem.get_height() + 2
            y += 8
        for indice, (imagem, _, pos_y) in enumerate(self.linhas):
            self.linhas[indice] = (imagem, self.placa.centerx - imagem.get_width() // 2, pos_y)

    def _voltar(self):
        self.gerenciador.mudar_estado(self.voltar())

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                self._voltar()
                return
            if evento.type == pygame.KEYDOWN and evento.key in (
                    pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                Audio.tocar("clique")
                self._voltar()
                return
            if self.navegador.tratar_evento(evento) is not None:
                Audio.tocar("clique")
                self._voltar()
                return

    def atualizar(self, dt=1 / 60):
        pass

    def desenhar(self, janela):
        janela.blit(self.fundo, (0, 0))
        janela.blit(self.escurecedor, (0, 0))
        desenhar_placa(janela, self.placa)
        titulo = texto_pixel("CRÉDITOS", 18, (255, 214, 74), escala=3)
        janela.blit(titulo, titulo.get_rect(center=(self.largura // 2, self.placa.top + 55)))
        for imagem, x, y in self.linhas:
            janela.blit(imagem, (x, y))
        self.navegador.desenhar(janela)
