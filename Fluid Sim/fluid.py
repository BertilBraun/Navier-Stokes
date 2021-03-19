import numpy as np
from settings import N, visc, diff
from simulation import diffuse, project, advect


class Fluid:
    def __init__(self):
        size = (N, N)
        self.s = np.zeros(size)
        self.density = np.zeros(size)

        self.Vx = np.zeros(size)
        self.Vy = np.zeros(size)

        self.Vx0 = np.zeros(size)
        self.Vy0 = np.zeros(size)

    def update(self):

        diffuse(1, self.Vx0, self.Vx, visc)
        diffuse(2, self.Vy0, self.Vy, visc)

        project(self.Vx0, self.Vy0, self.Vx, self.Vy)

        advect(1, self.Vx, self.Vx0, self.Vx0, self.Vy0)
        advect(2, self.Vy, self.Vy0, self.Vx0, self.Vy0)

        project(self.Vx, self.Vy, self.Vx0, self.Vy0)

        diffuse(0, self.s, self.density, diff)
        advect(0, self.density, self.s, self.Vx, self.Vy)

    def addDensity(self, x: int, y: int, amount: float):
        self.density[x, y] += amount

    def addVelocity(self, x: int, y: int, amountX: float, amountY: float):
        self.Vx[x, y] += amountX
        self.Vy[x, y] += amountY
