from numba import njit
from settings import N, dt, iterations

@njit(cache=True)
def set_bnd(b: int, x):
    for i in range(1, N - 1):
        x[i, 0] = -x[i, 1] if b == 2 else x[i, 1]
        x[i, N-1] = -x[i, N-2] if b == 2 else x[i, N-2]

    for j in range(1, N - 1):
        x[0, j] = -x[1, j] if b == 1 else x[1, j]
        x[N-1, j] = -x[N-2, j] if b == 1 else x[N-2, j]

    x[0, 0] = 0.33 * (x[1, 0] + x[0, 1] + x[0, 0])
    x[0, N-1] = 0.33 * (x[1, N-1] + x[0, N-2] + x[0, N-1])

    x[N-1, 0] = 0.33 * (x[N-2, 0] + x[N-1, 1] + x[N-1, 0])
    x[N-1, N-1] = 0.33 * (x[N-2, N-1] + x[N-1, N-2] + x[N-1, N-1])


@njit(cache=True)
def lin_solve(b: int, x, x0, a: float, c: float):

    cRecip = 1.0 / c

    for k in range(iterations):
        for j in range(1, N - 1):
            for i in range(1, N - 1):
                x[i, j] = (x0[i, j] + a * (+ x[i+1, j]
                                           + x[i-1, j]
                                           + x[i, j+1]
                                           + x[i, j-1]
                                           )) * cRecip

        set_bnd(b, x)


@njit(cache=True)
def diffuse(b: int, x, x0, diff: float):
    a = dt * diff * (N - 2) * (N - 2)
    lin_solve(b, x, x0, a, 1 + 6 * a)


@njit(cache=True)
def clamp(x, minimum, maximum):
    return max(minimum, min(x, maximum))


@njit(cache=True)
def advect(b: int, d, d0, velocX, velocY):

    dtx = dt * (N - 2)
    dty = dt * (N - 2)

    for j in range(1, N - 1):
        for i in range(1, N - 1):
            x = i - (dtx * velocX[i, j])
            y = j - (dty * velocY[i, j])

            i0 = int(clamp(x, 0.5, N + 0.5))
            j0 = int(clamp(y, 0.5, N + 0.5))

            i1 = i0 + 1
            j1 = j0 + 1

            s1 = x - i0
            s0 = 1.0 - s1
            t1 = y - j0
            t0 = 1.0 - t1

            d[i, j] = s0 * (t0 * d0[i0, j0] + (t1 * d0[i0, j1])) \
                + s1 * (t0 * d0[i1, j0] + (t1 * d0[i1, j1]))

    set_bnd(b, d)


@njit(cache=True)
def project(velocX, velocY, p, div):

    for j in range(1, N - 1):
        for i in range(1, N - 1):
            div[i, j] = -0.5 * (
                + velocX[i+1, j]
                - velocX[i-1, j]
                + velocY[i, j+1]
                - velocY[i, j-1]
            ) / N
            p[i, j] = 0

    set_bnd(0, div)
    set_bnd(0, p)
    lin_solve(0, p, div, 1, 6)

    for j in range(1, N - 1):
        for i in range(1, N - 1):
            velocX[i, j] -= 0.5 * (p[i+1, j] - p[i-1, j]) * N
            velocY[i, j] -= 0.5 * (p[i, j+1] - p[i, j-1]) * N

    set_bnd(1, velocX)
    set_bnd(2, velocY)

