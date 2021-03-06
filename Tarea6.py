#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

'''
Pregunta 1
'''


def inicializa_n(n, x_steps, h):
    for i in range(x_steps):
        x = i * h
        n[i] = np.exp(-x**2 / 0.1)
    n[0] = 1
    n[-1] = 0


def calcula_b(b, x_steps, r, mu):
    for j in range(1, x_steps - 1):
        b[j] = r * n[j+1] + (2 - 2 * r +
                             dt * mu * (1 - n[j])) * n[j] + r * n[j-1]


def calcula_alfa_y_beta(alfa, beta, b, r, x_steps):
    Amas = -1 * r
    A0 = (2 + 2 * r)
    Amenos = -1 * r
    alfa[0] = 0
    beta[0] = 1

    for i in range(1, x_steps):
        alfa[i] = -Amas / (A0 + Amenos*alfa[i-1])
        beta[i] = (b[i] - Amenos*beta[i-1]) / (Amenos*alfa[i-1] + A0)


def avanza_paso_temporal(n, n_next, alfa, beta, x_steps, t_steps):
    n_next[0] = 1
    n_next[-1] = 0

    for i in range(x_steps - 2, 0, -1):
        n_next[i] = alfa[i] * n_next[i+1] + beta[i]


# Setup

# Constantes y condiciones iniciales/finales
gamma = 0.001
mu = 1.5
ti = 0
tf = 50
xi = 0
xf = 1

# Cantidad de pasos espacial y temporal para discretización
x_steps = 500
t_steps = 7500

# Pasos
dt = (tf - ti) / (t_steps - 1)
h = (xf - xi) / (x_steps - 1)
r = dt / (2 * h**2)
r = r * gamma

# Inicializar vectores a utilizar
n = np.zeros(x_steps)
n_next = np.zeros(x_steps)
n_final = np.zeros((t_steps, x_steps))
b = np.zeros(x_steps)
alfa = np.zeros(x_steps)
beta = np.zeros(x_steps)

# Inicializar vectores n y n final con los respectivos valores iniciales
inicializa_n(n, x_steps, h)
n_final[0, :] = n.copy()

for i in range(1, t_steps):
    calcula_b(b, x_steps, r, mu)
    calcula_alfa_y_beta(alfa, beta, b, r, x_steps)
    avanza_paso_temporal(n, n_next, alfa, beta, x_steps, t_steps)
    n = n_next.copy()
    n_final[i, :] = n.copy()


# Gráficos
fig = plt.figure(1)
fig.clf()

ax = fig.add_subplot(111)

x = np.linspace(0, xf, x_steps)
ax.set_ylim(0, 1)

for i in range(0, t_steps, tf):
    ax.plot(x, n_final[i, :])

plt.xlabel('x')
plt.ylabel('n (x)')
plt.title("Densidad de la especie en funcion del espacio.")
plt.savefig("densidad.png")

plt.show()
plt.draw()
