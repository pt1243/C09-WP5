from definitions import FuelTank
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# S/C Adapter Dimensions and Material
d_1 = 1666*10**-3
d_2 = 1780*10**-3
h = 450*10**-3
t = 5.5*10**-3
E = 72*10**9
sns.set_theme(style='darkgrid')
#Stiffness of the S/C Adapter

K = E/(h/(t*np.pi*(d_2-d_1))*(np.log(abs((d_2-d_1)/h*h+d_1))-np.log(d_1)))
#K_2 = E*d_2*np.pi*t/h*10**-6
print('Spacecraft adapter stiffness: ' +str(K*10**-6)+'kN/mm')
#print(K_2)

#S/C Eigen Frequency
M = 1350 # kg S/C mass REVISE IT
f_sc = 1/(2*np.pi)*np.sqrt(K/M)
print('Spacecraft Natural Frequency: '+ str(f_sc))

#solution
k = 9248.767 #N/m
m = 675 #kg
g = 9.81 #m/s^2
w_f = 2*np.pi*100 #
w_n = np.sqrt(k/m)
f_0 = 0.8*g/m
x_0 = 0
v_0 = 10 #HAS TO BE RESONED FOR

def x_h(t):
    return (x_0-f_0/(w_n**2-w_f**2))*np.cos(w_n*t)*10**3#+v_0/w_n*np.sin(w_n*t)*10**3

def x_p(t):
    return (f_0/(w_n**2-w_f**2))*np.cos(w_f*t)*10**3

t = np.linspace(0,30,500)
x = x_h(t)+x_p(t)
xh = x_h(t)
xp = x_p(t)
sns.relplot(aspect=11/14)
plt.plot(t, x, label='General', color='seagreen')
plt.plot(t, xh, label='Homogeneous', linewidth=0.5, color='purple', linestyle='dashed')
plt.plot(t, xp, label='Particular', linewidth=0.5, color='blue', linestyle='dashed')
plt.axhline(0, color='grey', linewidth=0.75)
plt.xlabel('t [s]')
plt.ylabel('x [mm]')
plt.legend(loc='upper left')
print(xh)
plt.savefig('.\Solution.pdf', dpi=1200)
plt.show()

w_f = np.linspace(0,2*np.pi*100,200)
T = f_0/(w_n**2-w_f**2)
plt.plot(w_f,T, color='green', linewidth=1)
plt.xlabel('\u03C9$_{f}$ [1/rad]')
plt.ylabel('T []')
plt.savefig('.\Transient.pdf', dpi=1200)
#plt.show()

