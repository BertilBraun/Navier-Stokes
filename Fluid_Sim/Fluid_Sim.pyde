from Vec2 import Vec2
from Fluid import Fluid
from Settings import *

fluid = None
t = 0

def setup():
    global fluid
    size(N * SCALE, N * SCALE)
    #frameRate(22)
    fluid = Fluid(0.2, 0, 0.0000001)


def draw():
    global fluid
    global t

    print("step", int(t * 50))

    for i in range(-1, 2):
        for j in range(-1, 2):
            fluid.addDensity(N // 2 + i, N // 2 + j, random(50, 150))
    
    for i in range(2):
        #let angle = noise(t) * TWO_PI * 2
        #let v = p5.Vector.fromAngle(angle)
        v = Vec2(sin(t * 2), cos(t * 2)) * 0.2
        t += 0.01
        fluid.addVelocity(N // 2, N // 2, v)
    
    fluid.step()
    fluid.renderD()
