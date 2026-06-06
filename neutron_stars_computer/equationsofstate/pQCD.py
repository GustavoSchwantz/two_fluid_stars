from scipy.differentiate import derivative
from dataclasses import dataclass, field
import numpy as np
import sympy as sp

from .eos import EquationOfState
import neutron_stars_computer.star.conversionfactors as cf


@dataclass()#slots=True, frozen=True)
class PQCD(EquationOfState):
    mu_B: float = 1
    c1: float   = 0.9008
    X: float    = 4
    d1: float   = 0.5034
    d2: float   = 1.452
    nu1: float  = 0.3553
    nu2: float  = 0.9101


    def energy_density_from(self, pressure: float) -> float:
        return pressure + self.mu_B * derivative(self.__pressure, x=self.mu_B).df

    def __pressure(self, mu_B: float):
        p_SB = 3 * (mu_B / 3)**4 / 4 * np.pi ** 2
        a = self.d1 * self.X ** (-self.nu1)
        b = self.d2 * self.X ** (-self.nu2)

        return p_SB * (self.c1 - a / (mu_B - b) )
        

    