from __future__ import annotations
from typing import List, Union
from numpy import pi, polynomial, sqrt, exp


class Material:
    def __init__(
            self,
            E: float | int,
            poissons_ratio: float | int,
            sigma_y: float | int,
            density: float | int,
            cost: float | int) -> None:
        self.E = E
        self.poissons_ratio = poissons_ratio
        self.sigma_y = sigma_y
        self.density = density
        self.cost = cost


class Propellant:
    def __init__(self, density_coefficients: List[float | int]) -> None:
        self._density_coefficients = density_coefficients

    def density(self, T: float | int):
        """Computes density [kg/m^3] given temperature [K]."""
        result = 0
        for power, coefficient in enumerate(self._density_coefficients):
            result += coefficient * T ** power
        return result * 1000


class FuelTank:
    def __init__(
            self,
            L: Union[float, int],  # Tank length [m]
            R: Union[float, int],  # Tank radius [m]
            p: Union[float, int],  # Tank pressure [Pa]
            T: Union[float, int],  # Propellant temperature [K]
            material: Material,  # Tank material
            propellant: Propellant,  # Propellant
            ) -> None:
        self.L = L
        self.R = R
        self.p = p
        self.material = material
        self.propellant = propellant
        self.propellant_mass = self.volume() * self.propellant.density(T)

    @classmethod
    def from_R(cls,
               R: Union[float, int],  # Tank radius [m]
               p: Union[float, int],  # Tank pressure [Pa]
               m: Union[float, int],  # Propellant mass [kg]
               T: Union[float, int],  # Propellant temperature [K]
               material: Material,  # Tank material
               propellant: Propellant,  # Propellant type
               ) -> FuelTank:
        """Creates a fuel tank of a given radius [m] to hold a certain mass [kg] of propellant."""
        desired_volume = m / propellant.density(T)  # [m^3]
        end_cap_volume = 4/3 * pi * R ** 3  # volume of end caps only (L = 2R) [m^3]
        if desired_volume < end_cap_volume:
            L = 2 * R
            print(f'Warning: propellant tank requested with volume {desired_volume * 1000} L, '
                  f'but minimum volume is {end_cap_volume * 1000} L. Consider using a smaller radius.')
        else:
            L = 2 * R + (desired_volume - end_cap_volume) / (pi * R ** 2)
        tank = cls(L, R, p, T, material, propellant)
        tank._propellant_mass = m
        return tank

    @classmethod
    def from_L(cls,
               L: Union[float, int],  # Tank length [m]
               p: Union[float, int],  # Tank pressure [Pa]
               m: Union[float, int],  # Propellant mass [kg]
               T: Union[float, int],  # Propellant temperature [K]
               material: Material,  # Tank material
               propellant: Propellant,  # Propellant type
               ) -> FuelTank:
        """Creates a fuel tank of a given length [m] to hold a certain mass [kg] of propellant."""
        desired_volume = m / propellant.density(T)  # [m^3]
        radius_equation_coefficients = [-desired_volume, 0, pi * L, -2/3 * pi]
        radius_equation = polynomial.polynomial.Polynomial(radius_equation_coefficients)
        radius_equation_roots = radius_equation.roots()
        R = radius_equation_roots[1]
        tank = cls(L, R, p, T, material, propellant)
        tank._propellant_mass = m
        return tank

    def volume(self) -> float:
        """Fuel tank volume in [m^3]."""
        return pi * self.R ** 2 * (4/3 * self.R + self.L - 2 * self.R)

    def t_1_pressure(self, SF_pressure: Union[float, int]) -> float:
        """Calculate t_1 in [m] required to withstand the internal pressure."""
        return self.p * self.R / (self.material.sigma_y / SF_pressure)

    def t_2_pressure(self, SF_pressure: Union[float, int]) -> float:
        """Calculate t_2 in [m] required to withstand the internal pressure."""
        return self.t_1_pressure(SF_pressure) * 0.5

    def L_R_ratio(self):
        """Calculate the L/R ratio of the tank."""
        return self.L / self.R

    def max_L_R_ratio(self) -> bool:
        """Calculate the maximum L/R ratio to withstand Euler buckling."""
        return sqrt(pi ** 2 * self.material.E / (2 * self.material.sigma_y))

    def passes_Euler_buckling_check(self) -> bool:
        """Returns whether or not the tank dimensions can withstand Euler buckling."""
        return self.L_R_ratio() <= self.max_L_R_ratio()

    def shell_buckling(self, t_1: Union[float, int]) -> float:
        """Calculates the critical stress for shell buckling."""
        lambda_half_waves = 214
        k = lambda_half_waves \
            + (12 / pi ** 4) * (self.L ** 4 / (self.R ** 2 * t_1 ** 2)) \
            * (1 - self.material.poissons_ratio ** 2) * (1 / lambda_half_waves)
        Q = (self.p / self.material.E) * (self.R / t_1) ** 2
        sigma_cr = (1.983 - 0.983 * exp(-23.14 * Q)) * k * (pi ** 2 * self.material.E) \
            / (12 * (1 - self.material.poissons_ratio ** 2)) * (t_1 / self.L) ** 2
        return sigma_cr

    def tank_mass(self, t_1: Union[float, int], t_2: Union[float, int]) -> float:
        """Returns the tank mass in [kg]."""
        ends_mass = 4 * pi * self.R ** 2 * self.material.density * t_2
        cylinder_mass = (self.L - 2 * self.R) * 2 * pi * self.R * t_1 * self.material.density
        return ends_mass + cylinder_mass

    def compressive_stress(self, load: Union[float, int], t_1: Union[float, int]) -> float:
        """Returns the compressive stress on the tank in [Pa]."""
        load_bearing_area = 2 * pi * self.R * t_1
        sigma = load / load_bearing_area
        return sigma

    def passes_shell_buckling_check(self, load: Union[float, int], t_1: Union[float, int],
                                 SF_shell: Union[float, int]) -> bool:
        """Check if the design passes the shell buckling failure test."""
        return self.compressive_stress(load, t_1) * SF_shell <= self.shell_buckling(t_1)
