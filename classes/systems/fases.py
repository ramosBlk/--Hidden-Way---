"""
Definição (dados) das fases 2 e 3 e fábrica de fases.

A fase 1 (Mapa 1: amuletos -> baú/chave -> caverna) tem estado próprio (Mapa1State). As demais
usam o FaseState genérico com a mesma progressão.

Convenções (px, tela de 1400x760):
    plataformas: (x, y_topo, largura[, altura])  amuletos: (x, y) centro
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
    amuletos: list
    bau: tuple
    inimigos: list = field(default_factory=list)
    espinhos: list = field(default_factory=list)
    paredes: list = field(default_factory=list)
    mostrar_plataformas: bool = True
    forca_pulo: float = -13.5
    mostrar_textura_porta: bool = True
    intensidade_brilho_porta: float = 1.0
    halo_anel_porta: bool = False


FASES = [
    None,  # índice 0: Mapa 1 (Mapa1State)

    # ---- Fase 2: 3 amuletos, 4 slimes vermelhos
    ConfigFase(
        nome="FASE 2 - A CAVERNA", fundo="Mapa_2",
        cor_plataforma=(74, 70, 98), cor_topo=(120, 116, 150),
        spawn=(1202, 212), porta=(0, 262), bau=(250, 555),
        plataformas=[
            (0, 478, 218, 7),
            (0, 262, 176, 7),
            (200, 280, 72, 6),
            (280, 318, 198, 6),
            (272, 494, 38, 6),
            (340, 476, 20, 5),
            (372, 460, 152, 2),
            (558, 278, 122, 2),
            (514, 394, 104, 6),
            (626, 396, 36, 5),
            (706, 430, 112, 4),
            (356, 178, 88, 3),
            (672, 258, 94, 5),
            (786, 198, 24, 4),
            (806, 530, 46, 6),
            (874, 554, 90, 4),
            (964, 470, 82, 6),
            (1148, 528, 122, 5),
            (1028, 514, 40, 5),
            (1194, 644, 156, 4),
            (970, 120, 174, 4),
            (1202, 212, 160, 4),
            (1118, 348, 52, 5),
            (1222, 428, 134, 5),
            (138, 604, 216, 5),
            (840, 340, 34, 4),
            (892, 352, 28, 5),
            (818, 186, 72, 3),
            (924, 334, 96, 3),
            (892, 146, 68, 4),
            (1068, 518, 24, 6),
            (1092, 522, 14, 5),
            (1106, 526, 42, 6),
        ],
        amuletos=[(1296, 410), (234, 582), (600, 260)],
        inimigos=[
            ("slime_vermelho", 280, 446, 320),
            ("slime_vermelho", 50, 180, 478),
            ("slime_vermelho", 532, 600, 394),
            ("slime_vermelho", 982, 1028, 470),
        ],
        # Corpos de rocha dos penhascos laterais (começam logo abaixo das bordas das plataformas)
        paredes=[
                    (-128, 264, 161, 219),
            (0, 485, 135, 275),
            (138, 612, 215, 148),
            (1355, 217, 67, 545),
            (1194, 540, 81, 45),
            (1194, 652, 161, 108),
        ],
        mostrar_plataformas=False,
    ),

    # ---- Fase 3: 3 amuletos, 1 slime e 4 morcegos
    ConfigFase(
        nome="FASE 3 - O CEU", fundo="Mapa_3",
        cor_plataforma=(44, 78, 66), cor_topo=(96, 150, 100),
        spawn=(60, 606), porta=(1305, 226), bau=(300, 384),
        plataformas=[
            (-4, 606, 248, 7),
            (268, 432, 102, 20),
            (442, 386, 88, 7),
            (360, 156, 92, 10),
            (546, 194, 72, 7),
            (-12, 274, 264, 8),
            (506, 372, 78, 6),
            (408, 554, 200, 6),
            (606, 658, 166, 6),
            (642, 484, 62, 6),
            (644, 430, 158, 2),
            (684, 262, 106, 6),
            (906, 432, 378, 2),
            (886, 554, 90, 5),
            (1162, 638, 128, 3),
            (1286, 538, 88, 6),
            (1100, 566, 54, 6),
            (1096, 252, 60, 2),
            (1204, 226, 202, 11),
            (292, 602, 100, 10),
            (926, 294, 92, 6),
        ],
        paredes = [
            (414, 556, 186, 127),
            (1292, 548, 72, 142),
        ],
        amuletos=[(318, 400), (580, 170), (1250, 600)],
        inimigos=[
            ("morcego", 620, 860, 340),
            ("morcego", 260, 440, 310),
            ("morcego", 500, 760, 250),
            ("morcego", 940, 1180, 350),
        ],
        mostrar_plataformas=False,
        mostrar_textura_porta=False,
        intensidade_brilho_porta=1.8,
        halo_anel_porta=True,
    ),

]

TOTAL_FASES = len(FASES)


def criar_fase(indice, gerenciador, largura, altura, vidas=3):
    """Cria o estado da fase `indice` (0 = Mapa 1)."""
    if indice == 0:
        from classes.states.mapa1_state import Mapa1State
        return Mapa1State(gerenciador, largura, altura, vidas=vidas)
    from classes.states.fase_state import FaseState
    return FaseState(gerenciador, largura, altura, FASES[indice], indice, vidas=vidas)


def proxima_fase(indice, gerenciador, largura, altura, vidas=3):
    """
    Argumentos (titulo, subtitulo, proxima_fase) para a FaseCompletaState depois de concluir
    a fase `indice`. Na última fase, proxima_fase é None (volta ao menu).
    """
    if indice + 1 < TOTAL_FASES:
        return dict(titulo="FASE COMPLETA!",
                    subtitulo=f"Você desbloqueou a fase {indice + 2}!",
                    proxima_fase=lambda: criar_fase(
                        indice + 1, gerenciador, largura, altura, vidas=vidas))
    return dict(titulo="JOGO COMPLETO!", subtitulo="Você escapou da Hidden Way. Parabéns!", proxima_fase=None)
