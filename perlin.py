import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random as rd
import numpy as np
import math
import time

fig, ax = plt.subplots()
rd.seed(1)
N = 100

X = list(range(0,N+1))
Y = list(map(lambda _: rd.random(), range(0,N+1)))


# plot discret noise
ax.plot(X,Y,'xr')


def interpolate_cosinus(a, b, t):
    c = (1. - math.cos(t * math.pi)) / 2.

    return (a * (1. - c)) + (b * c)

def interpolate_cubic(before_p0, p0, p1, after_p1, t):
    a3 = -0.5*before_p0 + 1.5*p0 - 1.5*p1 + 0.5*after_p1
    a2 = before_p0 - 2.5*p0 + 2*p1 - 0.5*after_p1
    a1 = -0.5*before_p0 + 0.5*p1
    a0 = p0

    return (a3 * t*t*t) + (a2 * t*t) + (a1 * t) + a0


# discret noise
def noise(x):
    n = math.floor(x)
    n = min(N,max(0,n))

    return Y[n]

# smooth noise with cosinus
def smooth_cosinus_noise(x):
    a = noise(x)
    b = noise(x + 1)
    t = x - math.floor(x)

    return interpolate_cosinus(a,b,t)

# smooth noise with cubic
def smooth_cubic_noise(x):
    p0 = noise(x - 1)
    p1 = noise(x)
    p2 = noise(x + 1)
    p3 = noise(x + 2)
    t = x - math.floor(x)

    return interpolate_cubic(p0,p1,p2,p3,t)


sampling = N * 10
x = list(np.linspace(0,N,sampling))
y = list(map(smooth_cubic_noise,x))

# plot cubic interpolation
ax.plot(x,y)


def perlin_noise(x):
    octave = 4
    amplitude = 1.
    frequency = 1. / pow(5,octave-1)
    persitance = .5

    result = 0

    for i in range(0,octave):
        t = i * 10
        result += amplitude * smooth_cubic_noise(((x * frequency) + t) % N)
        frequency *= 5
        amplitude *= persitance

    geom_lim = (1. - persitance) / (1. - amplitude)

    return result * geom_lim


sampling = N * 10
x = list(np.linspace(0,N,sampling))
y = list(map(perlin_noise,x))

ax.plot(x,y)
plt.show()
