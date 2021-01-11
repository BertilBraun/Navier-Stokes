from Settings import *
from numba import vectorize, guvectorize, float64, int64, void


# function to use 1D array and fake the extra two dimensions --> 2D
@vectorize([int64(int64, int64),int64(int64, float64),int64(float64, int64),int64(float64, float64)])
def IX(x, y):
    return int64(x + y * N);

# Function of dealing with situation with boundary cells.
#@guvectorize([void(int64, float64[:])], '() -> ()', target="parallel")
def set_bnd(b, x):
    for i in range(1, N  - 1):
        x[IX(i, 0)] = -x[IX(i, 1)] if b == 2 else x[IX(i, 1)]
        x[IX(i, N - 1)] = -x[IX(i, N - 2)] if b == 2 else x[IX(i, N - 2)]
        
    for j in range(1, N  - 1):
        x[IX(0, j)] = -x[IX(1, j)] if b == 1 else x[IX(1, j)]
        x[IX(N - 1, j)] = -x[IX(N - 2, j)] if b == 1 else x[IX(N - 2, j)]

    x[IX(0, 0)] = 0.5 * (x[IX(1, 0)] + x[IX(0, 1)])
    x[IX(0, N - 1)] = 0.5 * (x[IX(1, N  - 1)] + x[IX(0, N - 2)])
    x[IX(N - 1, 0)] = 0.5 * (x[IX(N - 2, 0)] + x[IX(N - 1, 1)])
    x[IX(N - 1, N  - 1)] = 0.5 * (x[IX(N - 2, N - 1)] + x[IX(N - 1, N  - 1 - 2)])


#@guvectorize([void(int64, float64[:], float64[:], float64, float64)], '() -> ()', target="parallel")
def lin_solve(b, x, x0, a, c):
    cRecip = float64(1.0 / c)
    for t in range(iterations):
        out = x.copy()
        inner_lin_solve(x, x0, a, cRecip, out)
        x = out
        set_bnd(b, x)

@guvectorize([void(float64[:], float64[:], float64, float64, float64[:])], '(n),(n),(),() -> (n)', nopython=True)
def inner_lin_solve(x, x0, a, cRecip, out):
    #N = x.shape[0]
    for j in range(1, N  - 1):
        for i in range(1, N  - 1):
            out[IX(i, j)] = (x0[IX(i, j)] + a * \
                   (x[IX(i + 1, j)] + \
                    x[IX(i - 1, j)] + \
                    x[IX(i, j + 1)] + \
                    x[IX(i, j - 1)])) * cRecip

#@guvectorize([void(int64, float64[:], float64[:], float64, float64)], '() -> ()', target="parallel")
def diffuse(b, x, x0, diff, dt):
    a = dt * diff * (N - 2) * (N - 2)
    lin_solve(b, x, x0, a, 1 + 6 * a)

#Function of project : This operation runs through all the cells and fixes them up so everything is in equilibrium.
#@guvectorize([void(float64[:], float64[:], float64[:], float64[:])], '() -> ()', target="parallel")
def project(velX, velY, p, div):
    for j in range(1, N  - 1):
        for i in range(1, N  - 1):
            div[IX(i, j)] = (-0.5 * \
                   (velX[IX(i + 1, j)] - \
                    velX[IX(i - 1, j)] + \
                    velY[IX(i, j + 1)] - \
                    velY[IX(i, j - 1)])) / N
            
            p[IX(i, j)] = 0
            

    set_bnd(0, div)
    set_bnd(0, p)
    lin_solve(0, p, div, 1, 6)

    for j in range(1, N  - 1):
        for i in range(1, N  - 1):
            velX[IX(i, j)] -= 0.5 * (p[IX(i + 1, j)] - p[IX(i - 1, j)]) * N
            velY[IX(i, j)] -= 0.5 * (p[IX(i, j + 1)] - p[IX(i, j - 1)]) * N
    
    set_bnd(1, velX)
    set_bnd(2, velY)


# Function of advect: responsible for actually moving things around
#@guvectorize([void(int64, float64[:], float64[:], float64[:], float64[:], float64)], '() -> ()', target="parallel")
def advect(b, d, d0, velX, velY, dt):
    #@vectorize([float64(float64, float64, float64)])
    def clamp(x, l, u):
        return max(l, min(x, u))
    
    for j in range(1, N  - 1):
        for i in range(1, N  - 1):
            
            tmpx = dt * (N - 2) * velX[IX(i, j)]
            tmpy = dt * (N - 2) * velY[IX(i, j)]
            
            x = clamp(i - tmpx, 0.5, N - 1.5)
            y = clamp(j - tmpy, 0.5, N - 1.5)
        
            s1 = x - int(x)
            s0 = 1.0 - s1
            t1 = y - int(y)
            t0 = 1.0 - t1
    
            d[IX(i, j)] = \
                s0 * (t0 * d0[IX(int(x), int(y))] + t1 * d0[IX(int(x), int(y) + 1)]) + \
                s1 * (t0 * d0[IX(int(x) + 1, int(y))] + t1 * d0[IX(int(x) + 1, int(y) + 1)])

    set_bnd(b, d)
    
