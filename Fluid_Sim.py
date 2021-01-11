from Vec2 import Vec2
from Fluid import Fluid
from Settings import *
import random
import math

fluid = None
t = 0

def setup():
    global fluid
    #frameRate(22)
    fluid = Fluid(0.2, 0, 0.0000001)


def draw():
    global fluid
    global t

    print("step", int(t * 50))

    for i in range(-1, 2):
        for j in range(-1, 2):
            fluid.addDensity(N // 2 + i, N // 2 + j, random.randint(50, 150))
    
    for i in range(2):
        #let angle = noise(t) * TWO_PI * 2
        #let v = p5.Vector.fromAngle(angle)
        v = Vec2(math.sin(t), math.cos(t)) * 0.2
        t += 0.01
        fluid.addVelocity(N // 2, N // 2, v)
    
    fluid.step()

setup()

while True:
    try:
        draw()
    except Exception as e:
        print(e)
        exit()