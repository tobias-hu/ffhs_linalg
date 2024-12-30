from DCT import fdct, idct, normalize, denormalize
import numpy as np

"""
Created on: 30.12.2024
Author: Tobias Gasche
Description: This file contains code to perform the DCT and IDCT with the methods from DCT.py
"""

M = fdct(3)
T = idct(3)

img = normalize(np.array([255,128,45]))

print(M)

dct_res = M @ img

print(dct_res)

res = denormalize(np.round(T @ dct_res))

print(res)
