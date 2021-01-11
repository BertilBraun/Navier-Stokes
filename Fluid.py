from Settings import *
from Fluid_Util import *
import numpy as np

# Fluid cube class
class Fluid:
    def __init__(self, dt, diffusion, viscosity):
        self.dt = dt
        self.diff = diffusion
        self.visc = viscosity
    
        self.s = np.array([0 for _ in range(N*N)], dtype=np.float64)
        self.density = np.array([0 for _ in range(N*N)], dtype=np.float64)
    
        self.Vx = np.array([0 for _ in range(N*N)], dtype=np.float64)
        self.Vy = np.array([0 for _ in range(N*N)], dtype=np.float64)  
        self.Vx0 = np.array([0 for _ in range(N*N)], dtype=np.float64)
        self.Vy0 = np.array([0 for _ in range(N*N)], dtype=np.float64)
        
  # step method
    def step(self):
        diffuse(1, self.Vx0, self.Vx, self.visc, self.dt)
        diffuse(2, self.Vy0, self.Vy, self.visc, self.dt)
    
        project(self.Vx0, self.Vy0, self.Vx, self.Vy)
    
        advect(1, self.Vx, self.Vx0, self.Vx0, self.Vy0, self.dt)
        advect(2, self.Vy, self.Vy0, self.Vx0, self.Vy0, self.dt)
    
        project(self.Vx, self.Vy, self.Vx0, self.Vy0)
        diffuse(0, self.s, self.density, self.diff, self.dt)
        advect(0, self.density, self.s, self.Vx, self.Vy, self.dt)

  # method to add density
    def addDensity(self, x, y, amount):
        self.density[IX(x, y)] += amount

  # method to add velocity
    def addVelocity(self, x, y, amount):
        self.Vx[IX(x, y)] += amount.x
        self.Vy[IX(x, y)] += amount.y

  # function to render density
    def renderD(self):
        for i in range(N):
            for j in range(N):
                fill(self.density[IX(i, j)])
                noStroke()
                rect(i * SCALE, j * SCALE, SCALE, SCALE)
                
  # function to render velocity
    def renderV(self):
        for i in range(N):
            for j in range(N):
                x = i * SCALE
                y = j * SCALE
                vx = self.Vx[IX(i, j)]
                vy = self.Vy[IX(i, j)]
                stroke(0)
        
                if abs(v) > 0.1:
                    line(x, y, x + vx * SCALE, y + vy * SCALE)
