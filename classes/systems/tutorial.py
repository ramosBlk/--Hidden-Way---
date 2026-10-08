import pygame


class Tutorial:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

        # Estado atual do tutorial (1 a 4)
        self.passo_atual = 1
        self.concluido = False

        # Variáveis para o efeito de texto digitado (máquina de escrever)
        self.texto_completo = ""
        self.texto_atual_exibido = ""
        self.indice_letra = 0
        self.tempo_ultimo_caractere = 0
        self.velocidade_digitacao = 45  # Milissegundos por letra

        # Fontes maiores e com boa legibilidade direto na tela
        self.fonte_texto = pygame.font.SysFont("arial", 28, bold=True)

        # Mensagens dos passos
        self.mensagens = {
            1: "Pressione D para andar para frente.",
            2: "Ótimo! Agora pressione A para voltar.",
            3: "Excelente! Pressione W para cima e S para baixo.",
            4: "Perfeito! Pressione ESPAÇO para pular.\nVá até a árvore gigante para iniciar sua jornada."
        }

        self.atualizar_texto_passo()

        self.distancia_caminhada = 0
        self.usou_w = False
        self.usou_s = False

    def atualizar_texto_passo(self):
        """Atualiza o texto completo com base no passo e reseta a digitação"""
        self.texto_completo = self.mensagens.get(self.passo_atual, "")
        self.texto_atual_exibido = ""
        self.indice_letra = 0
        self.tempo_ultimo_caractere = pygame.time.get_ticks()

    def atualizar(self, player, cenario):
        if self.concluido:
            return

        # Tutorial opcional: chegar na árvore conclui o tutorial em qualquer passo
        if cenario.distancia_percorrida >= cenario.limite_maximo_distancia:
            self.concluido = True
            return

        # Efeito de máquina de escrever
        tempo_atual = pygame.time.get_ticks()
        if self.indice_letra < len(self.texto_completo):
            if tempo_atual - self.tempo_ultimo_caractere > self.velocidade_digitacao:
                self.texto_atual_exibido += self.texto_completo[self.indice_letra]
                self.indice_letra += 1
                self.tempo_ultimo_caractere = tempo_atual

        teclas = pygame.key.get_pressed()

        # ==========================================
        # PASSO 1: Andar para a frente (Tecla D)
        # ==========================================
        if self.passo_atual == 1:
            if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
                self.distancia_caminhada += abs(player.velocidade)
                if self.distancia_caminhada > 150:
                    self.passo_atual = 2
                    self.atualizar_texto_passo()
                    self.distancia_caminhada = 0

        # ==========================================
        # PASSO 2: Andar para trás (Tecla A)
        # ==========================================
        elif self.passo_atual == 2:
            if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
                self.distancia_caminhada += abs(player.velocidade)
                if self.distancia_caminhada > 120:
                    self.passo_atual = 3
                    self.atualizar_texto_passo()

        # ==========================================
        # PASSO 3: Usar W (cima) e S (baixo)
        # ==========================================
        elif self.passo_atual == 3:
            if teclas[pygame.K_w] or teclas[pygame.K_UP]:
                self.usou_w = True
            if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
                self.usou_s = True

            if self.usou_w and self.usou_s:
                self.passo_atual = 4
                self.atualizar_texto_passo()

        # ==========================================
        # PASSO 4: Ir até a árvore gigante
        # ==========================================
        elif self.passo_atual == 4:
            if cenario.distancia_percorrida >= cenario.limite_maximo_distancia:
                self.concluido = True

    def desenhar(self, janela):
        if self.concluido:
            return

        # Posição Y mais abaixo no topo da tela, centralizada horizontalmente
        y_pos = 50

        # Renderiza o texto linha por linha diretamente na janela (sem caixas)
        if "\n" in self.texto_atual_exibido:
            linhas = self.texto_atual_exibido.split("\n")
            for i, linha in enumerate(linhas):
                txt_render = self.fonte_texto.render(linha, True, (255, 255, 255))

                # Sombra preta para destacar o texto no fundo
                sombra_render = self.fonte_texto.render(linha, True, (0, 0, 0))

                x_pos = (self.largura - txt_render.get_width()) // 2

                janela.blit(sombra_render, (x_pos + 2, y_pos + (i * 35) + 2))
                janela.blit(txt_render, (x_pos, y_pos + (i * 35)))
        else:
            txt_render = self.fonte_texto.render(self.texto_atual_exibido, True, (255, 255, 255))
            sombra_render = self.fonte_texto.render(self.texto_atual_exibido, True, (0, 0, 0))

            x_pos = (self.largura - txt_render.get_width()) // 2

            janela.blit(sombra_render, (x_pos + 2, y_pos + 2))
            janela.blit(txt_render, (x_pos, y_pos))