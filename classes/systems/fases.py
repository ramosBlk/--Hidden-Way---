"""Carregamento e validação dos dados das fases e fábrica de estados."""
import json
from dataclasses import dataclass, field
from math import isfinite
from pathlib import Path


_ARQUIVO_FASES = Path(__file__).resolve().parents[2] / "assets" / "data" / "fases.json"


def _validar_tupla_numerica(valor, tamanho, nome, *, inteiros=False):
    if not isinstance(valor, (list, tuple)) or len(valor) != tamanho:
        raise ValueError(f"{nome} deve conter exatamente {tamanho} valores")
    if any(
        isinstance(item, bool)
        or not isinstance(item, (int, float))
        or not isfinite(item)
        or (inteiros and not isinstance(item, int))
        for item in valor
    ):
        raise ValueError(f"{nome} deve conter valores numéricos válidos")
    return tuple(valor)


def _validar_geometrias(valores, nome, tamanhos):
    if not isinstance(valores, list):
        raise ValueError(f"{nome} deve ser uma lista")
    resultado = []
    for indice, valor in enumerate(valores):
        if not isinstance(valor, (list, tuple)) or len(valor) not in tamanhos:
            formatos = " ou ".join(map(str, tamanhos))
            raise ValueError(f"{nome}[{indice}] deve conter {formatos} valores")
        geometria = _validar_tupla_numerica(
            valor, len(valor), f"{nome}[{indice}]", inteiros=True
        )
        if any(dimensao <= 0 for dimensao in geometria[2:]):
            raise ValueError(f"{nome}[{indice}] deve ter dimensões positivas")
        resultado.append(geometria)
    return resultado


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

    def __post_init__(self):
        if not isinstance(self.nome, str) or not self.nome.strip():
            raise ValueError("nome da fase não pode ser vazio")
        if not isinstance(self.fundo, str) or not self.fundo.strip():
            raise ValueError(f"{self.nome}: fundo não pode ser vazio")

        self.cor_plataforma = _validar_tupla_numerica(
            self.cor_plataforma, 3, f"{self.nome}.cor_plataforma", inteiros=True
        )
        self.cor_topo = _validar_tupla_numerica(
            self.cor_topo, 3, f"{self.nome}.cor_topo", inteiros=True
        )
        for nome, cor in (
            ("cor_plataforma", self.cor_plataforma),
            ("cor_topo", self.cor_topo),
        ):
            if any(canal < 0 or canal > 255 for canal in cor):
                raise ValueError(f"{self.nome}.{nome} deve usar canais entre 0 e 255")

        for nome in ("spawn", "porta", "bau"):
            setattr(
                self, nome,
                _validar_tupla_numerica(
                    getattr(self, nome), 2, f"{self.nome}.{nome}", inteiros=True
                ),
            )
        self.plataformas = _validar_geometrias(
            self.plataformas, f"{self.nome}.plataformas", (3, 4)
        )
        self.paredes = _validar_geometrias(
            self.paredes, f"{self.nome}.paredes", (4,)
        )
        self.espinhos = _validar_geometrias(
            self.espinhos, f"{self.nome}.espinhos", (3,)
        )

        if not isinstance(self.amuletos, list):
            raise ValueError(f"{self.nome}.amuletos deve ser uma lista")
        self.amuletos = [
            _validar_tupla_numerica(
                ponto, 2, f"{self.nome}.amuletos[{indice}]", inteiros=True
            )
            for indice, ponto in enumerate(self.amuletos)
        ]
        if not isinstance(self.inimigos, list):
            raise ValueError(f"{self.nome}.inimigos deve ser uma lista")
        for indice, inimigo in enumerate(self.inimigos):
            if (
                not isinstance(inimigo, (list, tuple))
                or len(inimigo) != 4
                or inimigo[0] not in ("slime", "slime_vermelho", "morcego")
            ):
                raise ValueError(f"{self.nome}.inimigos[{indice}] tem formato inválido")
            _validar_tupla_numerica(
                inimigo[1:], 3, f"{self.nome}.inimigos[{indice}]", inteiros=True
            )
            if inimigo[1] >= inimigo[2]:
                raise ValueError(
                    f"{self.nome}.inimigos[{indice}] deve ter intervalo horizontal crescente"
                )
            self.inimigos[indice] = tuple(inimigo)

        if (
            isinstance(self.forca_pulo, bool)
            or not isinstance(self.forca_pulo, (int, float))
            or not isfinite(self.forca_pulo)
            or self.forca_pulo >= 0
        ):
            raise ValueError(f"{self.nome}.forca_pulo deve ser um número negativo")
        if (
            isinstance(self.intensidade_brilho_porta, bool)
            or not isinstance(self.intensidade_brilho_porta, (int, float))
            or not isfinite(self.intensidade_brilho_porta)
            or self.intensidade_brilho_porta < 0
        ):
            raise ValueError(
                f"{self.nome}.intensidade_brilho_porta deve ser não negativa"
            )
        for nome in (
            "mostrar_plataformas",
            "mostrar_textura_porta",
            "halo_anel_porta",
        ):
            if not isinstance(getattr(self, nome), bool):
                raise ValueError(f"{self.nome}.{nome} deve ser booleano")


def carregar_configuracoes():
    """Carrega os mapas preservando suas tuplas e valida os dados antes do uso."""
    with _ARQUIVO_FASES.open(encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    if not isinstance(dados, list) or not dados:
        raise ValueError(f"{_ARQUIVO_FASES} deve conter uma lista de fases")
    if any(not isinstance(fase, dict) for fase in dados):
        raise ValueError(f"{_ARQUIVO_FASES} deve conter objetos de configuração")
    return [ConfigFase(**fase) for fase in dados]


FASES = [None, *carregar_configuracoes()]  # índice 0: Mapa 1 (Mapa1State)

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
