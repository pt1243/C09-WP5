from __future__ import annotations
from typing import List
from numpy import pi, polynomial


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
            L: float | int,  # Tank length [m]
            R: float | int,  # Tank radius [m]
            p: float | int,  # Tank pressure [Pa]
            T: float | int,  # Propellant temperature [K]
            material: Material,  # Tank material
            propellant: Propellant,  # Propellant
            stress_safety_factor: float | int  # Safety factor below the yield stress to use
            ) -> None:
        self._L = L
        self._R = R
        self._p = p
        self._material = material
        self._propellant = propellant
        self._propellant_mass = self.volume * propellant.density(T)
        self._t_1 = p * R / (material.sigma_y / stress_safety_factor)

    @classmethod
    def from_R(cls,
               R: float | int,  # Tank radius [m]
               p: float | int,  # Tank pressure [Pa]
               m: float | int,  # Propellant mass [kg]
               T: float | int,  # Propellant temperature [K]
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
               L: float | int,  # Tank length [m]
               p: float | int,  # Tank pressure [Pa]
               m: float | int,  # Propellant mass [kg]
               T: float | int,  # Propellant temperature [K]
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
    def L(self):
        """Total length [m]"""
        return self._L

    @property
    def R(self):
        """Radius [m]"""
        return self._R

    @property
    def volume(self):
        """Fuel tank volume in [m^3]."""
        return pi * self._R ** 2 * (4/3 * self._R + self._L - 2 * self._R)
