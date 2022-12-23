from typing import Union

# Relevant S/C lengths
total_length = 4540.76 / 1000
l_2 = 989.26 / 1000
l_1 = 2273.51 / 1000

# Accelerations
g = 9.80665
a_long = 6 * g
a_lat = 2 * g

# Relevant S/C masses

SC_structure_mass = 350
fuel_mass = 587.9
tank_mass_commercial = 4 * 13.5 + 4 * 8.2
SC_wet_mass_initial = 1350.64
PTM_wet_mass = 166.3 + 256.62
structure_mass = SC_structure_mass * (l_2 / total_length)
#print(f'{structure_mass = }')
#print(f'{tank_mass_commercial = }')


def loads(distance_hydrazine: Union[int, float],
          distance_mon25: Union[int, float],
          tank_mass: Union[int, float] = None
          ):
    """Returns the load on the fuel and oxidizer tanks as a function of their position and mass."""
    if tank_mass is None:
        tank_mass = tank_mass_commercial
        SC_wet_mass = SC_wet_mass_initial
    else:
        SC_wet_mass = SC_wet_mass_initial - tank_mass_commercial + tank_mass

    # Calculate masses
    m_2 = fuel_mass + tank_mass + structure_mass
    m_1 = SC_wet_mass - PTM_wet_mass - m_2
    #print(f'********************************************** {m_2 = }, {m_1 = }')

    # Moment due to lateral loads
    M = a_lat * (m_1 * (l_2 + l_1 / 2) + m_2 * l_2 / 2)
    #print(f'{M = }')

    # Longitudinal loads
    F_long_total = (SC_wet_mass - PTM_wet_mass) * a_long

    # Loads on each tank
    F_hydrazine, F_mon25 = F_long_total / 4, F_long_total / 4
    #print(f'{F_hydrazine = }')
    F_hydrazine += (M / (2 * distance_hydrazine))
    F_mon25 += (M / (2 * distance_mon25))
    
    return F_hydrazine, F_mon25

#print(SC_wet_mass_initial - tank_mass_commercial + 2 *6.2065985156842975 + 2 * 4.209876886557542 + 0.5036)
