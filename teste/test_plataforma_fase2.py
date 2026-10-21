import pygame

pygame.init()

LARGURA = 1400
ALTURA = 760

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Editor de Plataformas (com Altura)")

cenario = pygame.image.load("assets/sprites/telas/Mapa_2.png").convert()
cenario = pygame.transform.scale(cenario, (LARGURA, ALTURA))

clock = pygame.time.Clock()


class EditorPlataformas:

    def __init__(self):
        # Lista com (x, y, largura, altura)
        self.plataformas = [
            [0, 478, 218, 7],
            [0, 262, 176, 7],
            [200, 280, 72, 6],
            [280, 318, 198, 6],
            [272, 494, 38, 6],
            [340, 476, 20, 5],
            [372, 460, 152, 2],
            [558, 278, 122, 2],
            [514, 394, 104, 6],
            [626, 396, 36, 5],
            [706, 430, 112, 4],
            [356, 178, 88, 3],
            [672, 258, 94, 5],
            [786, 198, 24, 4],
            [806, 530, 46, 6],
            [874, 554, 90, 4],
            [964, 470, 82, 6],
            [1148, 528, 122, 5],
            [1028, 514, 40, 5],
            [1194, 644, 156, 4],
            [970, 120, 174, 4],
            [1202, 212, 160, 4],
            [1118, 348, 52, 5],
            [1218, 428, 134, 5],
            [138, 604, 216, 5],
            [840, 340, 34, 4],
            [892, 352, 28, 5],
            [818, 186, 72, 3],
            [924, 334, 96, 3],
            [892, 146, 68, 4],
            [1068, 518, 24, 6],
            [1092, 522, 14, 5],
            [1106, 526, 42, 6],
        ]

        self.indice = 0
        self.velocidade = 2
        self.fonte = pygame.font.SysFont("consolas", 18)

    @property
    def plataforma(self):
        return self.plataformas[self.indice]

    def eventos(self, evento):
        if evento.type != pygame.KEYDOWN:
            return

        # Próxima plataforma
        if evento.key == pygame.K_TAB:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                self.indice -= 1
            else:
                self.indice += 1
            self.indice %= len(self.plataformas)

        # Nova plataforma
        elif evento.key == pygame.K_n:
            self.plataformas.append([100, 100, 120, 10])
            self.indice = len(self.plataformas) - 1

        # Excluir plataforma
        elif evento.key == pygame.K_DELETE:
            if len(self.plataformas) > 1:
                self.plataformas.pop(self.indice)
                self.indice %= len(self.plataformas)

        # Exportar plataformas no terminal
        elif evento.key == pygame.K_RETURN:
            print("\nplataformas = [")
            for x, y, largura, altura in self.plataformas:
                print(f"    ({x}, {y}, {largura}, {altura}),")
            print("]")

    def update(self):
        teclas = pygame.key.get_pressed()
        x, y, largura, altura = self.plataforma

        # Movimento das posições
        if teclas[pygame.K_LEFT]:
            x -= self.velocidade
        if teclas[pygame.K_RIGHT]:
            x += self.velocidade
        if teclas[pygame.K_UP]:
            y -= self.velocidade
        if teclas[pygame.K_DOWN]:
            y += self.velocidade

        # Controle de Largura
        if teclas[pygame.K_q]:
            largura = max(10, largura - 2)
        if teclas[pygame.K_e]:
            largura += 2

        # Controle de Altura
        if teclas[pygame.K_a]:
            altura = max(2, altura - 1)
        if teclas[pygame.K_d]:
            altura += 1

        self.plataformas[self.indice] = [x, y, largura, altura]

    def draw(self, tela):
        for i, (x, y, largura, altura) in enumerate(self.plataformas):
            cor = (255, 0, 0) if i == self.indice else (0, 255, 0)

            # Desenha o retângulo completo com x, y, largura e altura
            pygame.draw.rect(
                tela,
                cor,
                (x, y, largura, altura),
                2
            )

        x, y, largura, altura = self.plataforma

        texto = self.fonte.render(
            f"Plataforma {self.indice + 1}/{len(self.plataformas)}   X:{x}   Y:{y}   L:{largura}   A:{altura}",
            True,
            (255, 255, 255)
        )
        tela.blit(texto, (10, 10))

        ajuda = self.fonte.render(
            "TAB=Trocar | N=Nova | DEL=Excluir | Q/E=Largura | A/D=Altura | ENTER=Exportar",
            True,
            (255, 255, 0)
        )
        tela.blit(ajuda, (10, 35))


editor = EditorPlataformas()
rodando = True

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        editor.eventos(evento)

    editor.update()

    tela.blit(cenario, (0, 0))
    editor.draw(tela)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()