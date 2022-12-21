from typing import Union
from definitions import Material, Propellant, FuelTank
from loads import loads


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

# Distances
hydrazine_distance = 0.8
mon25_distance = 0.8

# Safety factors
SF_pressure = 1.1
SF_shell = 1.1

# Propellant masses
m_hydrazine, m_mon25 = propellant_masses(587.90, 0.85, 2)

# Create propellant tanks
hydrazine_tank_initial = FuelTank.from_L_R_ratio(2.6, 27.6e5 * 1.5, m_hydrazine, T, Ti_6Al_4V, hydrazine)
mon25_tank_initial = FuelTank.from_L(hydrazine_tank_initial.L, 27.6e5 * 1.5, m_mon25, T, Ti_6Al_4V, mon25)

# Initial thicknesses from pressure
hydrazine_t_1_pressure = hydrazine_tank_initial.t_1_pressure(SF_pressure)
mon25_t_1_pressure = mon25_tank_initial.t_1_pressure(SF_pressure)
hydrazine_t_2_pressure = hydrazine_tank_initial.t_2_pressure(SF_pressure)
mon25_t_2_pressure = mon25_tank_initial.t_2_pressure(SF_pressure)

# Loads
hydrazine_tank_initial_load, mon25_tank_initial_load = loads(hydrazine_distance, mon25_distance)

# Tank masses
hydrazine_initial_mass = hydrazine_tank_initial.tank_mass(hydrazine_t_1_pressure, hydrazine_t_2_pressure)
mon25_initial_mass = mon25_tank_initial.tank_mass(mon25_t_1_pressure, mon25_t_2_pressure)

print('------------ Initial iteration ------------')
print(f'Hydrazine tank:')
print(f'    Tank properties:')
print(f'        R:   {hydrazine_tank_initial.R * 1000} mm')
print(f'        L:   {hydrazine_tank_initial.L * 1000} mm')
print(f'        Tank mass: {hydrazine_initial_mass} kg')
print(f'    Thicknesses for pressure:')
print(f'        t_1: {hydrazine_t_1_pressure * 1000} mm')
print(f'        t_2: {hydrazine_t_2_pressure * 1000} mm')
print(f'    Failure checks:')
print(f'        L/R: {hydrazine_tank_initial.L_R_ratio()}')
print(f'        Maximum L/R ratio for Euler buckling: {hydrazine_tank_initial.max_L_R_ratio()}')
print(f'        Passes Euler buckling check: {hydrazine_tank_initial.passes_Euler_buckling_check()}')
print(f'        Stress due to launch loads: {hydrazine_tank_initial.compressive_stress(hydrazine_tank_initial_load, hydrazine_t_1_pressure) / 1e6} MPa')
print(f'        Maximum stress for Euler buckling: {hydrazine_tank_initial.shell_buckling(hydrazine_t_1_pressure) / 1e6} MPa')
print(f'        Passes shell buckling check: {hydrazine_tank_initial.passes_shell_buckling_check(hydrazine_tank_initial_load, hydrazine_t_1_pressure, SF_shell)}')
print()
print(f'MON25 tank:')
print(f'    Tank properties:')
print(f'        R:   {mon25_tank_initial.R * 1000} mm')
print(f'        L:   {mon25_tank_initial.L * 1000} mm')
print(f'        Tank mass: {mon25_initial_mass} kg')
print(f'    Thicknesses for pressure:')
print(f'        t_1: {mon25_t_1_pressure * 1000} mm')
print(f'        t_2: {mon25_t_2_pressure * 1000} mm')
print(f'    Failure checks:')
print(f'        L/R: {mon25_tank_initial.L_R_ratio()}')
print(f'        Maximum L/R ratio for Euler buckling: {mon25_tank_initial.max_L_R_ratio()}')
print(f'        Passes Euler buckling check: {mon25_tank_initial.passes_Euler_buckling_check()}')
print(f'        Stress due to launch loads: {mon25_tank_initial.compressive_stress(mon25_tank_initial_load, mon25_t_1_pressure) / 1e6} MPa')
print(f'        Maximum stress for Euler buckling: {mon25_tank_initial.shell_buckling(mon25_t_1_pressure) / 1e6} MPa')
print(f'        Passes shell buckling check: {mon25_tank_initial.passes_shell_buckling_check(mon25_tank_initial_load, mon25_t_1_pressure, SF_shell)}')

hydrazine_tank_updated_load, mon25_tank_updated_load = loads(hydrazine_distance, mon25_distance, 2 * (hydrazine_initial_mass + mon25_initial_mass))

print('\n\n------------ Updated values iteration ------------')
print(f'Hydrazine tank:')
print(f'    Failure checks:')
print(f'        Stress due to launch loads: {hydrazine_tank_initial.compressive_stress(hydrazine_tank_updated_load, hydrazine_t_1_pressure) / 1e6} MPa')
print(f'        Maximum stress for Euler buckling: {hydrazine_tank_initial.shell_buckling(hydrazine_t_1_pressure) / 1e6} MPa')
print(f'        Passes shell buckling check: {hydrazine_tank_initial.passes_shell_buckling_check(hydrazine_tank_updated_load, hydrazine_t_1_pressure, SF_shell)}')
print()
print(f'MON25 tank:')
print(f'    Failure checks:')
print(f'        Stress due to launch loads: {mon25_tank_initial.compressive_stress(mon25_tank_updated_load, mon25_t_1_pressure) / 1e6} MPa')
print(f'        Maximum stress for Euler buckling: {mon25_tank_initial.shell_buckling(mon25_t_1_pressure) / 1e6} MPa')
print(f'        Passes shell buckling check: {mon25_tank_initial.passes_shell_buckling_check(mon25_tank_updated_load, mon25_t_1_pressure, SF_shell)}')
