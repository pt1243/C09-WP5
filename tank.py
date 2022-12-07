import numpy as np

E = 72e9
I = 1
A = 0.25 * np.pi
L = 2

t1 = 0.004
v = 0.12
R = 0.5
p = 10e5
hw = 0.2

sigma_euler = (np.pi**2 * E * I) / (A * L**2)

Q = (p/E)*(R/t1)**2
k = hw + (12/np.pi**4)*(L**4/R**2 * t1**2)*(1-v**2)*(1/hw)
sigma_shell = (1.983 - 0.983*np.exp(-23.14*Q))*k*((np.pi**2 * E)/(12*(1-v**2)))*(t1/L)**2

print("Eluer critical load (MPa):", sigma_euler/10e6)
print("\nShell critical load (MPa):", sigma_shell/10e6)