from definitions import FuelTank
import numpy as np

# S/C Adapter Dimensions and Material
d_1 = 1666*10**-3
d_2 = 1780*10**-3
h = 450*10**-3
t = 5.5*10**-3
E = 72*10**9

#Stiffness of the S/C Adapter

K = E/(h/(t*np.pi*(d_2-d_1))*(np.log(abs((d_2-d_1)/h*h+d_1))-np.log(d_1)))
#K_2 = E*d_2*np.pi*t/h*10**-6
print('Spacecraft adapter stiffness: ' +str(K*10**-6)+'kN/mm')
#print(K_2)

#S/C Eigen Frequency
M = 1350 # kg S/C mass REVISE IT
f_sc = 1/(2*np.pi)*np.sqrt(K/M)
print('Spacecraft Natural Frequency: '+ str(f_sc))