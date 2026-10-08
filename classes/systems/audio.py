import math
from array import array

import pygame


class Audio:
    """
    Efeitos sonoros sintetizados em tempo de execução (o projeto não tem arquivos de áudio).
    Se não houver dispositivo de áudio, todas as chamadas viram no-op.
    """
    _sons = {}
    _pronto = False

    # nome -> lista de (frequência_inicial, frequência_final, duração) tocadas em sequência
    _RECEITAS = {
        "chave": [(988, 988, 0.07), (1319, 1319, 0.07), (1760, 1760, 0.18)],
        "bau_negado": [(150, 110, 0.14), (110, 90, 0.18)],
        "bau_abrir": [(180, 320, 0.30), (660, 660, 0.08), (880, 880, 0.08), (1320, 1320, 0.30)],
        "caverna": [(440, 880, 0.25), (880, 1320, 0.35)],
        "entrar": [(660, 220, 0.6)],
        "queda": [(700, 120, 0.7)],
        "game_over": [(330, 330, 0.18), (294, 294, 0.18), (262, 262, 0.18), (196, 196, 0.5)],
        "vitoria": [(523, 523, 0.12), (659, 659, 0.12), (784, 784, 0.12), (1047, 1047, 0.4)],
        "clique": [(880, 880, 0.04)],
    }

    @classmethod
    def _iniciar(cls):
        if cls._pronto:
            return
        cls._pronto = True
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            freq, formato, canais = pygame.mixer.get_init()
            if formato != -16:
                return
            for nome, notas in cls._RECEITAS.items():
                amostras = array("h")
                for f0, f1, dur in notas:
                    n = int(freq * dur)
                    fase = 0.0
                    for i in range(n):
                        t = i / n
                        fase += 2 * math.pi * (f0 + (f1 - f0) * t) / freq
                        env = min(1.0, i / 80) * (1 - t) ** 0.7
                        v = int(9000 * env * (1 if math.sin(fase) >= 0 else -1) * 0.6 + 6000 * env * math.sin(fase))
                        for _ in range(canais):
                            amostras.append(max(-32000, min(32000, v)))
                cls._sons[nome] = pygame.mixer.Sound(buffer=amostras.tobytes())
                cls._sons[nome].set_volume(0.35)
        except (pygame.error, NotImplementedError, ValueError):
            cls._sons.clear()

    @classmethod
    def tocar(cls, nome):
        cls._iniciar()
        som = cls._sons.get(nome)
        if som:
            som.play()
