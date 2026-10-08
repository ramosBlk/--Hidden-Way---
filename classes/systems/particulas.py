import math
import random

import pygame


class _Particula:
    __slots__ = ("x", "y", "vx", "vy", "vida", "vida_max", "cor", "tam", "gravidade")

    def __init__(self, x, y, vx, vy, vida, cor, tam, gravidade):
        self.x, self.y, self.vx, self.vy = x, y, vx, vy
        self.vida = self.vida_max = vida
        self.cor, self.tam, self.gravidade = cor, tam, gravidade


class SistemaParticulas:
    """Partículas quadradas (pixel art) que encolhem até sumir. Tempo em segundos (dt)."""

    def __init__(self):
        self.particulas = []

    def emitir(self, x, y, quantidade, cores, velocidade=(40, 140), vida=(0.4, 0.9), tam=(2, 4),
               gravidade=0.0, angulo=(0, 360), area=(0, 0)):
        for _ in range(quantidade):
            ang = math.radians(random.uniform(*angulo))
            vel = random.uniform(*velocidade)
            self.particulas.append(_Particula(
                x + random.uniform(-area[0], area[0]), y + random.uniform(-area[1], area[1]),
                math.cos(ang) * vel, -math.sin(ang) * vel,
                random.uniform(*vida), random.choice(cores), random.randint(*tam), gravidade))

    def atualizar(self, dt):
        for p in self.particulas:
            p.vida -= dt
            p.vy += p.gravidade * dt
            p.x += p.vx * dt
            p.y += p.vy * dt
        self.particulas = [p for p in self.particulas if p.vida > 0]

    def desenhar(self, janela):
        for p in self.particulas:
            t = p.vida / p.vida_max
            lado = max(1, round(p.tam * (0.4 + 0.6 * t)))
            pygame.draw.rect(janela, p.cor, (int(p.x), int(p.y), lado, lado))
