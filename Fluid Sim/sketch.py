
from fluid import Fluid
from settings import N, scale, density_scale, vel_scale

from browser import document, html, timer

fluid = Fluid()

last_x, last_y = 0, 0

canvas = html.CANVAS(width=scale * N, height=scale * N)
ctx = canvas.getContext("2d")

document["canvas"] <= canvas


def update():
    fluid.update()


def draw():
    for i in range(N):
        for j in range(N):
            c = min(255, max(fluid.density[i, j] * 1000, 0))
            c = min(255, max(fluid.s[i, j] * 1000, 0))
            ctx.fillStyle = "rgb("+ c + ","+ c + ","+ c + ")"
            ctx.fillRect(i * scale, j * scale, scale, scale)


def canvasClick(ev):
    global last_x, last_y

    rect = canvas.getBoundingClientRect()
    x = (ev.x - rect.left) // scale
    y = (ev.y - rect.top) // scale

    if x < 0 or x >= N or y < 0 or y >= N:
        return

    fluid.addDensity(x, y, density_scale)
    fluid.addVelocity(x, y, (last_x - x) * vel_scale, (last_y - y) * vel_scale)

    last_x = x
    last_y = y


document["canvas"].bind('click', canvasClick)

while True:

    update()
    draw()

