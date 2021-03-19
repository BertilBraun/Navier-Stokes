
from fluid import Fluid
from settings import N, scale, density_scale, vel_scale
from timeme import timeme

import pygame
pygame.init()

fluid = Fluid()
screen = pygame.display.set_mode([scale * N, scale * N])

last_x, last_y = 0, 0

@timeme
def update():
    global last_x, last_y

    x, y = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]:
        fluid.addDensity(x // scale, y // scale, density_scale)
        fluid.addVelocity(x // scale, y // scale, (last_x - x) * vel_scale, (last_y - y) * vel_scale)

    last_x = x
    last_y = y
    fluid.update()


def draw():
    screen.fill((255, 255, 255))
    for i in range(N):
        for j in range(N):
            c = min(255, max(fluid.density[i, j] * 1000, 0))
            c = min(255, max(fluid.s[i, j] * 1000, 0))
            screen.fill((c, c, c), ((i * scale, j * scale), (scale, scale)))


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        update()
        draw()

        pygame.display.flip()


if __name__ == "__main__":
    main()
