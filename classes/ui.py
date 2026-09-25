import pygame


def desenhar_caixa_dialogo(
    janela,
    texto,
    titulo="Papa Figo",
    entrada="",
    status="",
    resolvido=False,
):
    """Renderiza exclusivamente o painel de diálogo e o campo de resposta."""
    largura_janela, altura_janela = janela.get_size()

    largura_caixa = largura_janela - 100
    altura_caixa = 180
    x_caixa = 50
    y_caixa = altura_janela - altura_caixa - 30

    # Fundo escuro semitransparente
    fundo = pygame.Surface((largura_caixa, altura_caixa), pygame.SRCALPHA)
    fundo.fill((10, 10, 20, 235))
    janela.blit(fundo, (x_caixa, y_caixa))

    # Borda: Verde para resolvido, Dourada para pendente
    cor_borda = (50, 205, 50) if resolvido else (255, 215, 0)
    pygame.draw.rect(
        janela, cor_borda, (x_caixa, y_caixa, largura_caixa, altura_caixa), 3
    )

    # Título do NPC
    fonte_titulo = pygame.font.SysFont("arial", 20, bold=True)
    texto_titulo = fonte_titulo.render(f"Enigma: {titulo}", True, cor_borda)
    janela.blit(texto_titulo, (x_caixa + 20, y_caixa + 15))

    # Conteúdo da Pergunta
    fonte_texto = pygame.font.SysFont("arial", 18)
    texto_conteudo = fonte_texto.render(texto, True, (255, 255, 255))
    janela.blit(texto_conteudo, (x_caixa + 20, y_caixa + 48))

    if not resolvido:
        cor_status = (
            (255, 100, 100) if "Incorreto" in status else (200, 200, 200)
        )
        txt_status = fonte_texto.render(status, True, cor_status)
        janela.blit(txt_status, (x_caixa + 20, y_caixa + 80))

        # Campo de Texto
        pygame.draw.rect(
            janela, (40, 40, 60), (x_caixa + 20, y_caixa + 115, 220, 35)
        )
        pygame.draw.rect(
            janela, (100, 100, 150), (x_caixa + 20, y_caixa + 115, 220, 35), 2
        )

        txt_entrada = fonte_texto.render(f"{entrada}_", True, (255, 255, 0))
        janela.blit(txt_entrada, (x_caixa + 30, y_caixa + 120))

        txt_fechar = fonte_texto.render(
            "[ENTER] Confirmar | [E] Sair", True, (160, 160, 160)
        )
        janela.blit(
            txt_fechar, (x_caixa + largura_caixa - 260, y_caixa + 135)
        )
    else:
        txt_sucesso = fonte_texto.render(
            "Parabéns! Código correto. O enigma foi resolvido!",
            True,
            (100, 255, 100),
        )
        janela.blit(txt_sucesso, (x_caixa + 20, y_caixa + 90))

        txt_fechar = fonte_texto.render("[E] Sair", True, (160, 160, 160))
        janela.blit(
            txt_fechar, (x_caixa + largura_caixa - 120, y_caixa + 135)
        )