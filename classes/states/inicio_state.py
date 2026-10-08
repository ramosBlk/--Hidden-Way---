import pygame
from classes.systems.cenario import Cenario
from classes.entities.player import Player
from classes.systems.tutorial import Tutorial
from classes.states.game_state import GameState


class InicioState(GameState):
    def __init__(self, gerenciador, largura, altura):
        super().__init__(gerenciador)
        self.gerenciador = gerenciador
        self.largura = largura
        self.altura = altura

        self.player = Player(x=100, y=570, escala=1.0)
        self.tutorial = Tutorial(largura=self.largura, altura=self.altura)
        self.cenario = Cenario(
            caminho_imagem="assets/sprites/telas/Tela_inicio.png",
            caminho_segunda_imagem="assets/sprites/telas/arvore.png",
            largura=self.largura,
            altura=self.altura,
            velocidade=3.5,
            eh_plataforma=False
        )

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_e and self.tutorial.concluido:
                    if self.cenario.distancia_percorrida >= self.cenario.limite_maximo_distancia - 50:
                        from classes.states.mapa1_state import Mapa1State
                        self.gerenciador.mudar_estado(Mapa1State(self.gerenciador, self.largura, self.altura))

    def atualizar(self, dt=1 / 60):
        self.player.atualizar_movimento(gravidade_ativada=False)
        self.tutorial.atualizar(self.player, self.cenario)

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            self.cenario.mover(direcao_frente=True, player=self.player, tutorial=self.tutorial)
        elif teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            self.cenario.mover(direcao_frente=False, player=self.player, tutorial=self.tutorial)

        self.player.x = max(0, min(self.player.x, self.largura - self.player.largura))

    def desenhar(self, janela):
        self.cenario.desenhar(janela)

        # Aviso de interatividade na árvore
        if self.tutorial.concluido and self.cenario.distancia_percorrida >= self.cenario.limite_maximo_distancia - 50:
            fonte_interacao = pygame.font.SysFont("arial", 18, bold=True)
            texto_aviso = "[E] para Entrar"
            txt_surf = fonte_interacao.render(texto_aviso, True, (255, 255, 255))
            txt_sombra = fonte_interacao.render(texto_aviso, True, (0, 0, 0))

            pos_x = self.largura - 350
            pos_y = self.altura // 2 + 50

            janela.blit(txt_sombra, (pos_x + 1, pos_y + 1))
            janela.blit(txt_surf, (pos_x, pos_y))

        self.tutorial.desenhar(janela)
        self.player.desenhar(janela)