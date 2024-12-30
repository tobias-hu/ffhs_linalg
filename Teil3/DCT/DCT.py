import numpy as np
import sympy as sp

"""
Created on: 30.12.2024
Author: Tobias Gasche
Description: define forward dct and inverse dct.
define helperfunctions normalize and denormalize
"""

def fdct(N):
    M = np.zeros((N, N))
    for k in range(N):
        for n in range(N):
            M[k, n] = np.sqrt(1 / N) if k == 0 else np.sqrt(2 / N) * sp.cos((sp.pi * (2 * n + 1) * k) / (2 * N))

    return M


def idct(N):
    T = np.zeros((N, N))
    for n in range(N):
        for k in range(N):
            T[n, k] = np.sqrt(1 / N) if k == 0 else np.sqrt(2 / N) * sp.cos((sp.pi * (2 * n + 1) * k) / (2 * N))

    return T


def normalize(data):
    return data - 128


def denormalize(data):
    return data + 128
