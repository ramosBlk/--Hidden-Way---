import pytest

from classes.systems.fases import ConfigFase, FASES


def _config_fase(**alteracoes):
    dados = {
        "nome": "FASE DE TESTE",
        "fundo": "Mapa_teste",
        "cor_plataforma": (50, 60, 70),
        "cor_topo": (80, 90, 100),
        "spawn": (10, 20),
        "porta": (30, 40),
        "plataformas": [(0, 100, 50, 6)],
        "amuletos": [(20, 80)],
        "bau": (25, 50),
    }
    dados.update(alteracoes)
    return ConfigFase(**dados)


def test_fases_json_preserva_configuracoes_e_tuplas():
    assert len(FASES) == 3
    assert FASES[1].nome == "FASE 2 - A CAVERNA"
    assert FASES[2].nome == "FASE 3 - O CEU"
    assert FASES[1].plataformas[0] == (0, 478, 218, 7)
    assert FASES[2].inimigos[0] == ("morcego", 620, 860, 340)


def test_geometria_invalida_e_rejeitada():
    with pytest.raises(ValueError, match="dimensões positivas"):
        _config_fase(plataformas=[(0, 100, -1, 6)])


def test_intervalo_de_inimigo_invalido_e_rejeitado():
    with pytest.raises(ValueError, match="intervalo horizontal crescente"):
        _config_fase(inimigos=[("slime", 100, 50, 100)])
