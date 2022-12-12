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
print(hydrazine_tank.L)

mon25_tank = FuelTank.from_R(0.25, 27.6e5 * 1.5, m_mon25, T, Ti_6Al_4V, mon25)
print(mon25_tank.L)
