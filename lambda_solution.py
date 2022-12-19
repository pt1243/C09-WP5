import tkinter
import matplotlib.pyplot as plt
import numpy as np
from numpy import pi

v = 0.342
R = 0.3
L = 0.778
t1 = 0.004

def k(lambda_half_waves):
    return lambda_half_waves + (12/pi**4)*(L**2/(R**2 * t1**2))*(1-v**2)*1/lambda_half_waves

x = np.linspace(210, 220, 1000)

min_found = np.inf
min_i = 0
for i in x:
    if k(i) < min_found:
        min_found = k(i)
        min_i = i


print(min_i)

plt.plot(x, k(x))
plt.show()