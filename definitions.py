from __future__ import annotations
from typing import List, Union
from numpy import pi, polynomial, sqrt


class Material:
    def __init__(
            self,
            E: float | int,
            poissons_ratio: float | int,
            sigma_y: float | int,
            density: float | int,
            cost: float | int) -> None:
        self._E = E
        self._poissons_ratio = poissons_ratio
        self._sigma_y = sigma_y
        self._density = density
        self._cost = cost

    @property
    def E(self):
        """Young's Modulus"""
        return self._E

    @property
    def poissons_ratio(self):
        """Poisson's ratio"""
        return self._poissons_ratio

    @property
    def sigma_y(self):
        """Yield stress"""
        return self._sigma_y

    @property
    def density(self):
        """Density"""
        return self._density

    @property
    def cost(self):
        """Material cost"""
        return self._cost


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
        self._L = L
        self._R = R
        self._p = p
        self._material = material
        self._propellant = propellant
        self._propellant_mass = self.volume * propellant.density(T)

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

    @property
    def L(self) -> float:
        """Total length [m]"""
        return self._L

    @property
    def R(self) -> float:
        """Radius [m]"""
        return self._R

    @property
    def volume(self) -> float:
        """Fuel tank volume in [m^3]."""
        return pi * self._R ** 2 * (4/3 * self._R + self._L - 2 * self._R)

    def t_1_pressure(self, SF_pressure: Union[float, int]) -> float:
        """Calculate t_1 in [m] required to withstand the internal pressure."""
        return self._p * self.R / (self._material.sigma_y / SF_pressure)
    
    def t_2_pressure(self, SF_pressure: Union[float, int]) -> float:
        """Calculate t_2 in [m] required to withstand the internal pressure."""
        return self.t_1_pressure(SF_pressure) * 0.5

    def L_R_ratio(self):
        """Calculate the L/R ratio of the tank."""
        return self.L / self.R
    
    def max_L_R_ratio(self) -> bool:
        """Calculate the maximum L/R ratio to withstand Euler buckling."""
        return sqrt(pi ** 2 * self._material.E / (2 * self._material.sigma_y ))

    def passes_Euler_buckling_check(self) -> bool:
        """Returns whether or not the tank dimensions can withstand Euler buckling."""
        return self.L_R_ratio() <= self.max_L_R_ratio()