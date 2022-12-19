from typing import Union
from definitions import Material, Propellant, FuelTank


def propellant_masses(m_propellant: Union[float, int], mixture_ratio: Union[float, int], number_of_tanks: int):
    m_fuel = m_propellant / (1 + mixture_ratio)
    m_ox = m_propellant - m_fuel
    return m_fuel / number_of_tanks, m_ox / number_of_tanks


# Propellant definitions
mon25 = Propellant([1.6697, 4.622e-4, -4.80e-6])
hydrazine = Propellant([1.23078, -6.2668e-4, -4.5284e-7])

# Material definitions
Ti_6Al_4V = Material(113.8e9, 0.342, 880e6, 4430, 1)

# Temperature
T_hot = 357
T_cold = 310
T = (T_hot + T_cold) / 2

# Propellant masses
m_hydrazine, m_mon25 = propellant_masses(587.90, 0.85, 2)

hydrazine_tank = FuelTank.from_R(0.3, 27.6e5 * 1.5, m_hydrazine, T, Ti_6Al_4V, hydrazine)
mon25_tank = FuelTank.from_R(0.25, 27.6e5 * 1.5, m_mon25, T, Ti_6Al_4V, mon25)

print('Hydrazine tank:')
print(f'    t_1 for pressure: {hydrazine_tank.t_1_pressure(1.1) * 1000} mm')
print(f'    t_2 for pressure = {hydrazine_tank.t_2_pressure(1.1) * 1000} mm')
print(f'    L/R ratio: {hydrazine_tank.L_R_ratio()}')
print(f'    L/R maximum ratio for Euler buckling: {hydrazine_tank.max_L_R_ratio()}')
print(f'    Passes Euler buckling check: {hydrazine_tank.passes_Euler_buckling_check()}')
print('')
print('MON25 tank:')
print(f'    t_1 for pressure: {mon25_tank.t_1_pressure(1.1) * 1000} mm')
print(f'    t_2 for pressure = {mon25_tank.t_2_pressure(1.1) * 1000} mm')
print(f'    L/R ratio: {mon25_tank.L_R_ratio()}')
print(f'    L/R maximum ratio for Euler buckling: {mon25_tank.max_L_R_ratio()}')
print(f'    Passes Euler buckling check: {mon25_tank.passes_Euler_buckling_check()}')


print(hydrazine_tank.tank_mass(1.55 / 1000, 0.78 / 1000))
print(hydrazine_tank.L)

print(hydrazine_tank.shell_buckling(t_1=0.0015))