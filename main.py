import os
import pygame
from classes.cenario import Cenario
from classes.game_over import GameOver
from classes.npc import NPC
from classes.player import Player
from classes.ui import desenhar_caixa_dialogo

pygame.init()

LARGURA = 1400
ALTURA = 760

janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Hidden Way")

# Instâncias principais
cenario = Cenario(
    "assets/sprites/telas/Tela_inicio.png",
    largura=LARGURA,
    altura=ALTURA,
    velocidade=3.5,
)
player = Player(x=100, y=570)
tela_game_over = GameOver(largura=LARGURA, altura=ALTURA)

caminho_sprite_npc = os.path.join(
    "assets", "sprites", "personagem_secundario", "rotations", "south-west.png"
)
npc_enigma = NPC(
    x_mundo=1610,
    y_mundo=510,
    caminho_imagem=caminho_sprite_npc,
    fala_puzzle="Opa, me chamo Papa Figo! Me ajude com este código para abrir portas, caso contrário iremos brigar. Decifre o código: qual é a representação em binário do número decimal 22?",
)

# Estado do Enigma e do Jogo
RESPOSTA_CORRETA = "10110"
MAX_TENTATIVAS = 3

texto_digitado = ""
tentativas_erradas = 0
puzzle_resolvido = False
game_over = False
exibindo_dialogo = False
mensagem_status = f"Digite a resposta em binário (0 e 1) e pressione ENTER (Tentativas: 0/{MAX_TENTATIVAS}):"

LIMITE_DIREITO_TELA = 900
LIMITE_ESQUERDO_TELA = 300

relogio = pygame.time.Clock()
rodando = True


def resetar_jogo():
    global player, cenario, texto_digitado, tentativas_erradas, puzzle_resolvido, game_over, exibindo_dialogo, mensagem_status
    player = Player(x=100, y=570)
    cenario.distancia_percorrida = 0
    cenario.x1 = 0
    cenario.x2 = cenario.largura
    texto_digitado = ""
    tentativas_erradas = 0
    puzzle_resolvido = False
    game_over = False
    exibindo_dialogo = False
    mensagem_status = f"Digite a resposta em binário (0 e 1) e pressione ENTER (Tentativas: 0/{MAX_TENTATIVAS}):"


pygame.event.clear()

# =======================
# LOOP PRINCIPAL
# =======================
while rodando:
    relogio.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        elif evento.type == pygame.KEYDOWN:
            if game_over and evento.key == pygame.K_r:
                resetar_jogo()

            elif not game_over:
                if evento.key == pygame.K_e:
                    exibindo_dialogo = (
                        not exibindo_dialogo if npc_enigma.proximo else False
                    )

                elif exibindo_dialogo and not puzzle_resolvido:
                    if evento.key == pygame.K_RETURN:
                        if texto_digitado.strip() == RESPOSTA_CORRETA:
                            puzzle_resolvido = True
                        else:
                            tentativas_erradas += 1
                            texto_digitado = ""
                            if tentativas_erradas >= MAX_TENTATIVAS:
                                exibindo_dialogo = False
                                game_over = True
                            else:
                                mensagem_status = f"Incorreto! Tentativa {tentativas_erradas}/{MAX_TENTATIVAS}. Tente novamente:"

                    elif evento.key == pygame.K_BACKSPACE:
                        texto_digitado = texto_digitado[:-1]

                    elif evento.unicode in "01" and len(texto_digitado) < 7:
                        texto_digitado += evento.unicode

    teclas = pygame.key.get_pressed()
    npc_enigma.atualizar(player.x, player.y, cenario.distancia_percorrida)

    # Movimento do Jogador e Câmera
    if not exibindo_dialogo and not game_over:
        player.mover()

        if player.x >= LIMITE_DIREITO_TELA and (
            teclas[pygame.K_d] or teclas[pygame.K_RIGHT]
        ):
            player.x = LIMITE_DIREITO_TELA
            cenario.mover_cenario(player.velocidade, para_frente=True)

        elif (
            player.x <= LIMITE_ESQUERDO_TELA
            and (teclas[pygame.K_a] or teclas[pygame.K_LEFT])
            and cenario.distancia_percorrida > 0
        ):
            player.x = LIMITE_ESQUERDO_TELA
            cenario.mover_cenario(player.velocidade, para_frente=False)

        if player.x < 0:
            player.x = 0
        elif player.x > LARGURA - player.largura:
            player.x = LARGURA - player.largura

    # Renderização por camadas
    cenario.desenhar(janela)
    npc_enigma.desenhar(janela, cenario.distancia_percorrida)
    player.desenhar(janela)

    if exibindo_dialogo:
        desenhar_caixa_dialogo(
            janela,
            npc_enigma.fala_puzzle,
            titulo="Papa Figo",
            entrada=texto_digitado,
            status=mensagem_status,
            resolvido=puzzle_resolvido,
        )

    # Exibe a tela de Game Over usando a nova classe
    if game_over:
        tela_game_over.desenhar(
            janela,
            motivo="Você errou o código 3 vezes! Papa Figo perdeu a paciência e te derrotou.",
        )

    pygame.display.flip()

pygame.quit()