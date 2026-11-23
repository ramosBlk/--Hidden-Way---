from pathlib import Path
import sys

import pygame

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from classes.systems.fases import FASES


LARGURA = 1400
ALTURA = 760


class EditorPlataformas:
    """Editor das plataformas configuradas na fase 3."""

    def __init__(self):
        self.plataformas = [
            list(plataforma) for plataforma in FASES[2].plataformas
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

        if evento.key == pygame.K_TAB:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                self.indice -= 1
            else:
                self.indice += 1
            self.indice %= len(self.plataformas)

        elif evento.key == pygame.K_n:
            self.plataformas.append([100, 100, 120, 10])
            self.indice = len(self.plataformas) - 1

        elif evento.key == pygame.K_DELETE:
            if len(self.plataformas) > 1:
                self.plataformas.pop(self.indice)
                self.indice %= len(self.plataformas)

        elif evento.key == pygame.K_RETURN:
            print("\nplataformas = [")
            for x, y, largura, altura in self.plataformas:
                print(f"    ({x}, {y}, {largura}, {altura}),")
            print("]")

    def update(self):
        teclas = pygame.key.get_pressed()
        x, y, largura, altura = self.plataforma

        if teclas[pygame.K_LEFT]:
            x -= self.velocidade
        if teclas[pygame.K_RIGHT]:
            x += self.velocidade
        if teclas[pygame.K_UP]:
            y -= self.velocidade
        if teclas[pygame.K_DOWN]:
            y += self.velocidade

        if teclas[pygame.K_q]:
            largura = max(10, largura - 2)
        if teclas[pygame.K_e]:
            largura += 2
        if teclas[pygame.K_a]:
            altura = max(2, altura - 1)
        if teclas[pygame.K_d]:
            altura += 1

        self.plataformas[self.indice] = [x, y, largura, altura]

    def draw(self, tela):
        for i, (x, y, largura, altura) in enumerate(self.plataformas):
            cor = (255, 0, 0) if i == self.indice else (0, 255, 0)
            pygame.draw.rect(tela, cor, (x, y, largura, altura), 2)

        x, y, largura, altura = self.plataforma
        texto = self.fonte.render(
            f"Plataforma {self.indice + 1}/{len(self.plataformas)}   "
            f"X:{x}   Y:{y}   L:{largura}   A:{altura}",
            True,
            (255, 255, 255),
        )
        tela.blit(texto, (10, 10))

        ajuda = self.fonte.render(
            "TAB=Trocar | N=Nova | DEL=Excluir | Q/E=Largura | "
            "A/D=Altura | ENTER=Exportar",
            True,
            (255, 255, 0),
        )
        tela.blit(ajuda, (10, 35))


def main():
    pygame.init()

    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Editor de Plataformas - Cenário 3")

    caminho_cenario = (
        Path(__file__).resolve().parent.parent
        / "assets"
        / "sprites"
        / "telas"
        / "Mapa_3.png"
    )
    cenario = pygame.image.load(str(caminho_cenario)).convert()
    cenario = pygame.transform.scale(cenario, (LARGURA, ALTURA))

    editor = EditorPlataformas()
    clock = pygame.time.Clock()
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


if __name__ == "__main__":
    main()
