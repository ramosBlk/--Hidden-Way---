import pygame


class GameOver:

    def __init__(self, largura=1400, altura=760):
        self.largura = largura
        self.altura = altura

        # Overlay escuro e sombrio de fundo
        self.overlay = pygame.Surface((largura, altura), pygame.SRCALPHA)
        self.overlay.fill((10, 5, 8, 240))

        # Fontes robustas para simular o estilo de jogo pixelado/arcade
        self.fonte_titulo = pygame.font.SysFont("impact", 72)
        self.fonte_botao = pygame.font.SysFont("arial", 20, bold=True)

    def desenhar(self, janela, motivo=""):
        """Desenha a tela de Game Over inspirada no estilo da referência."""
        # 1. Fundo escuro cobrindo a tela
        janela.blit(self.overlay, (0, 0))

        # Dimensões do painel principal de Game Over
        larg_painel = 700
        alt_painel = 320
        x_painel = (self.largura - larg_painel) // 2
        y_painel = (self.altura - alt_painel) // 2

        # -------------------------------------------------------------
        # 2. CRÂNIO E OSSOS NO TOPO DO PAINEL
        # -------------------------------------------------------------
        centro_x = self.largura // 2
        topo_painel_y = y_painel

        # Crânio central (forma base simulada com círculos/retângulos estilo pixel)
        pygame.draw.ellipse(janela, (160, 165, 175), (centro_x - 55, topo_painel_y - 50, 110, 75))  # Crânio maior
        pygame.draw.rect(janela, (160, 165, 175), (centro_x - 40, topo_painel_y, 80, 30))  # Maxilar
        # Olhos vazios do crânio
        pygame.draw.rect(janela, (20, 15, 20), (centro_x - 30, topo_painel_y - 25, 20, 25))
        pygame.draw.rect(janela, (20, 15, 20), (centro_x + 10, topo_painel_y - 25, 20, 25))
        # Nariz do crânio
        pygame.draw.polygon(janela, (20, 15, 20), [(centro_x, topo_painel_y - 5), (centro_x - 6, topo_painel_y + 8),
                                                   (centro_x + 6, topo_painel_y + 8)])

        # Crânios menores nas laterais
        pygame.draw.ellipse(janela, (130, 135, 145), (centro_x - 100, topo_painel_y - 35, 65, 50))
        pygame.draw.ellipse(janela, (130, 135, 145), (centro_x + 35, topo_painel_y - 35, 65, 50))
        pygame.draw.rect(janela, (20, 15, 20), (centro_x - 80, topo_painel_y - 18, 12, 15))
        pygame.draw.rect(janela, (20, 15, 20), (centro_x + 68, topo_painel_y - 18, 12, 15))

        # -------------------------------------------------------------
        # 3. PLACA DE PEDRA ESCURA PRINCIPAL
        # -------------------------------------------------------------
        # Sombra da placa
        surf_sombra = pygame.Surface((larg_painel, alt_painel), pygame.SRCALPHA)
        surf_sombra.fill((0, 0, 0, 180))
        janela.blit(surf_sombra, (x_painel + 8, y_painel + 8))

        # Fundo da placa (cinza escuro / chumbo)
        pygame.draw.rect(janela, (35, 42, 48), (x_painel, y_painel, larg_painel, alt_painel))
        # Borda metálica/pedra da placa
        pygame.draw.rect(janela, (95, 105, 115), (x_painel, y_painel, larg_painel, alt_painel), 6)
        pygame.draw.rect(janela, (20, 25, 30), (x_painel + 6, y_painel + 6, larg_painel - 12, alt_painel - 12), 4)

        # -------------------------------------------------------------
        # 4. TEXTO "YOU DIED" VERMELHO SANGUE COM EFEITO
        # -------------------------------------------------------------
        # Sombra interna do texto
        txt_sombra = self.fonte_titulo.render("YOU DIED", True, (40, 10, 12))
        txt_principal = self.fonte_titulo.render("YOU DIED", True, (175, 35, 35))

        rect_txt = txt_principal.get_rect(center=(centro_x, y_painel + alt_painel // 2))

        janela.blit(txt_sombra, (rect_txt.x + 4, rect_txt.y + 4))
        janela.blit(txt_principal, rect_txt)

        # -------------------------------------------------------------
        # 5. TEIAS DE ARANHA E TRINCAS SOBRE O TEXTO
        # -------------------------------------------------------------
        ponto_centro_teia = (centro_x, y_painel + alt_painel // 2)
        cor_teia = (180, 185, 195, 160)  # Cinza claro translúcido

        # Linhas principais da teia irradiando do centro
        angulos = [0, 45, 90, 135, 180, 225, 270, 315]
        for ang in angulos:
            import math
            rad = math.radians(ang)
            fim_x = ponto_centro_teia[0] + int(math.cos(rad) * 280)
            fim_y = ponto_centro_teia[1] + int(math.sin(rad) * 120)
            pygame.draw.line(janela, (150, 155, 165), ponto_centro_teia, (fim_x, fim_y), 1)

        # Arcos concêntricos da teia
        pygame.draw.arc(janela, (160, 165, 175), (centro_x - 120, y_painel + 80, 240, 140), 0, 3.14, 1)
        pygame.draw.arc(janela, (160, 165, 175), (centro_x - 220, y_painel + 50, 440, 200), 0, 3.14, 1)

        # Manchas de sangue escorrendo dos crânios
        pygame.draw.rect(janela, (140, 20, 20), (centro_x - 15, topo_painel_y + 45, 6, 25))
        pygame.draw.rect(janela, (140, 20, 20), (centro_x + 35, topo_painel_y + 45, 4, 35))
        pygame.draw.rect(janela, (140, 20, 20), (centro_x - 50, topo_painel_y + 35, 5, 20))

        # -------------------------------------------------------------
        # 6. BOTÃO "Return" NA PARTE INFERIOR
        # -------------------------------------------------------------
        larg_botao = 160
        alt_botao = 45
        x_botao = centro_x - (larg_botao // 2)
        y_botao = y_painel + alt_painel - (alt_botao // 2)

        # Fundo e borda do botão estilo moldura de pedra
        pygame.draw.rect(janela, (40, 45, 55), (x_botao, y_botao, larg_botao, alt_botao))
        pygame.draw.rect(janela, (110, 120, 135), (x_botao, y_botao, larg_botao, alt_botao), 3)
        pygame.draw.rect(janela, (20, 22, 28), (x_botao + 3, y_botao + 3, larg_botao - 6, alt_botao - 6), 1)

        # Texto do Botão ("Return")
        txt_botao = self.fonte_botao.render("Return", True, (240, 240, 240))
        rect_botao = txt_botao.get_rect(center=(centro_x, y_botao + alt_botao // 2))
        janela.blit(txt_botao, rect_botao)