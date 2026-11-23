import json
from pathlib import Path


class Configuracoes:
    """Preferências persistentes do jogo, aplicadas imediatamente."""

    VOLUME_PADRAO = 100
    QUALIDADE_PADRAO = "alta"
    BRILHO_PADRAO = 100
    QUALIDADES = ("baixa", "media", "alta")
    CAMINHO = Path(__file__).resolve().parents[2] / "config.json"

    volume = VOLUME_PADRAO
    qualidade = QUALIDADE_PADRAO
    brilho = BRILHO_PADRAO

    @classmethod
    def definir_volume(cls, valor):
        try:
            valor = max(0, min(100, int(valor)))
        except (TypeError, ValueError, OverflowError):
            return cls.volume
        cls.volume = valor
        from classes.systems.audio import Audio
        Audio.definir_volume_mestre(valor)
        return cls.volume

    @classmethod
    def definir_qualidade(cls, qualidade):
        if not isinstance(qualidade, str) or qualidade.lower() not in cls.QUALIDADES:
            return cls.qualidade
        cls.qualidade = qualidade.lower()
        return cls.qualidade

    @classmethod
    def definir_brilho(cls, valor):
        try:
            valor = max(0, min(100, int(valor)))
        except (TypeError, ValueError, OverflowError):
            return cls.brilho
        cls.brilho = valor
        return cls.brilho

    @classmethod
    def fator_particulas(cls):
        return {"baixa": 0.25, "media": 0.5, "alta": 1.0}[cls.qualidade]

    @classmethod
    def brilhos_ativos(cls):
        return cls.qualidade != "baixa"

    @classmethod
    def carregar(cls):
        dados = {}
        try:
            with cls.CAMINHO.open("r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            if not isinstance(dados, dict):
                dados = {}
        except (OSError, json.JSONDecodeError, UnicodeDecodeError):
            dados = {}

        volume = dados.get("volume", cls.VOLUME_PADRAO)
        qualidade = dados.get("qualidade", cls.QUALIDADE_PADRAO)
        brilho = dados.get("brilho", cls.BRILHO_PADRAO)
        if not isinstance(volume, int) or isinstance(volume, bool) or not 0 <= volume <= 100:
            volume = cls.VOLUME_PADRAO
        if not isinstance(qualidade, str) or qualidade.lower() not in cls.QUALIDADES:
            qualidade = cls.QUALIDADE_PADRAO
        if not isinstance(brilho, int) or isinstance(brilho, bool) or not 0 <= brilho <= 100:
            brilho = cls.BRILHO_PADRAO

        cls.definir_volume(volume)
        cls.definir_qualidade(qualidade)
        cls.definir_brilho(brilho)

    @classmethod
    def salvar(cls):
        dados = {
            "volume": cls.volume,
            "qualidade": cls.qualidade,
            "brilho": cls.brilho,
        }
        try:
            with cls.CAMINHO.open("w", encoding="utf-8") as arquivo:
                json.dump(dados, arquivo, ensure_ascii=False, indent=2)
        except OSError:
            pass
