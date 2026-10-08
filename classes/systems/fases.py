"""
Definição (dados) das fases 2 a 5 e fábrica de fases.

A fase 1 (Mapa 1: chave -> baú -> caverna) tem estado próprio (Mapa1State). As demais usam o
FaseState genérico: coletar TODAS as chaves libera a porta; inimigos e espinhos aumentam a
dificuldade de fase em fase.

Convenções (px, tela de 1400x760):
  plataformas: (x, y_topo, largura)        chaves: (x, y) centro
  inimigos:    ("slime", x_min, x_max, y_chão)   |   ("morcego", x_min, x_max, y_base_voo)
  espinhos:    (x, y_topo_da_plataforma, largura)
  porta:       (x_centro, y_chão)          spawn: (x, y_chão)
"""
from dataclasses import dataclass, field


@dataclass
class ConfigFase:
    nome: str
    fundo: str
    cor_plataforma: tuple
    cor_topo: tuple
    spawn: tuple
    porta: tuple
    plataformas: list
    chaves: list
    inimigos: list = field(default_factory=list)
    espinhos: list = field(default_factory=list)


FASES = [
    None,  # índice 0: Mapa 1 (Mapa1State)

    # ---- Fase 2: 2 chaves, 1 inimigo
    ConfigFase(
        nome="FASE 2 - A CAVERNA", fundo="Mapa_2",
        cor_plataforma=(74, 70, 98), cor_topo=(120, 116, 150),
        spawn=(60, 660), porta=(1330, 660),
        plataformas=[(0, 660, 380), (480, 660, 240), (820, 660, 580),
                     (160, 540, 140), (400, 500, 130), (620, 480, 150), (860, 520, 150)],
        chaves=[(465, 470), (935, 490)],
        inimigos=[("slime", 920, 1240, 660)],
    ),

    # ---- Fase 3: 3 chaves, 2 inimigos (um voador)
    ConfigFase(
        nome="FASE 3 - A FLORESTA SOMBRIA", fundo="Mapa_3",
        cor_plataforma=(44, 78, 66), cor_topo=(96, 150, 100),
        spawn=(60, 660), porta=(1340, 660),
        plataformas=[(0, 660, 300), (400, 660, 200), (700, 660, 200), (1000, 660, 400),
                     (120, 540, 150), (480, 540, 140), (800, 540, 140), (1120, 540, 160),
                     (300, 420, 130), (620, 420, 130), (960, 420, 130), (1260, 420, 140)],
        chaves=[(365, 390), (1025, 390), (1200, 510)],
        inimigos=[("slime", 1040, 1260, 660), ("morcego", 450, 900, 480)],
    ),

    # ---- Fase 4: 3 chaves, 3 inimigos, espinhos
    ConfigFase(
        nome="FASE 4 - AS CAVERNAS GELADAS", fundo="Mapa_4",
        cor_plataforma=(70, 100, 140), cor_topo=(190, 225, 250),
        spawn=(60, 660), porta=(1340, 660),
        plataformas=[(0, 660, 300), (400, 660, 300), (800, 660, 200), (1100, 660, 300),
                     (200, 540, 140), (480, 540, 130), (740, 540, 130), (1000, 540, 130), (1260, 540, 140),
                     (330, 420, 130), (600, 420, 130), (860, 420, 130), (1120, 420, 130),
                     (480, 300, 160), (740, 300, 160), (1000, 300, 160)],
        chaves=[(560, 270), (930, 390), (1080, 270)],
        inimigos=[("slime", 1130, 1270, 660), ("morcego", 450, 900, 470), ("morcego", 800, 1300, 360)],
        espinhos=[(520, 660, 90), (880, 660, 60)],
    ),

    # ---- Fase 5: 4 chaves, 4 inimigos, muitos espinhos
    ConfigFase(
        nome="FASE 5 - O CORAÇÃO DO VULCÃO", fundo="Mapa_5",
        cor_plataforma=(96, 44, 36), cor_topo=(230, 120, 50),
        spawn=(60, 660), porta=(1350, 660),
        plataformas=[(0, 660, 260), (360, 660, 200), (660, 660, 200), (960, 660, 440),
                     (140, 550, 130), (400, 540, 120), (640, 540, 130), (900, 540, 120), (1160, 540, 140),
                     (280, 430, 120), (520, 420, 120), (780, 420, 120), (1040, 420, 120), (1280, 420, 120),
                     (400, 300, 140), (660, 300, 130), (920, 300, 130), (1180, 300, 140),
                     (540, 180, 140), (800, 180, 140), (1060, 180, 140)],
        chaves=[(610, 150), (1130, 150), (205, 520), (1250, 270)],
        inimigos=[("slime", 1190, 1290, 660), ("morcego", 300, 700, 380),
                  ("morcego", 700, 1200, 250), ("morcego", 400, 1000, 480)],
        espinhos=[(420, 660, 80), (730, 660, 70), (1100, 660, 80), (400, 540, 120)],
    ),
]

TOTAL_FASES = len(FASES)


def criar_fase(indice, gerenciador, largura, altura):
    """Cria o estado da fase `indice` (0 = Mapa 1)."""
    if indice == 0:
        from classes.states.mapa1_state import Mapa1State
        return Mapa1State(gerenciador, largura, altura)
    from classes.states.fase_state import FaseState
    return FaseState(gerenciador, largura, altura, FASES[indice], indice)


def proxima_fase(indice, gerenciador, largura, altura):
    """
    Argumentos (titulo, subtitulo, proxima_fase) para a FaseCompletaState depois de concluir
    a fase `indice`. Na última fase, proxima_fase é None (volta ao menu).
    """
    if indice + 1 < TOTAL_FASES:
        return dict(titulo="FASE COMPLETA!",
                    subtitulo=f"Você desbloqueou a fase {indice + 2}!",
                    proxima_fase=lambda: criar_fase(indice + 1, gerenciador, largura, altura))
    return dict(titulo="JOGO COMPLETO!", subtitulo="Você escapou da Hidden Way. Parabéns!", proxima_fase=None)
