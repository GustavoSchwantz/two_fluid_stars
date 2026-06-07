from scipy.differentiate import derivative
from dataclasses import dataclass, field
import numpy as np
import sympy as sp

from .eos import EquationOfState
import neutron_stars_computer.star.conversionfactors as cf


class PQCD(EquationOfState):
    def __init__(self, X=2):
        self.__c1 = 0.9008
        d1 = 0.5034
        d2 = 1.452
        v1 = 0.3553
        v2 = 0.9101

        self.__a = d1*X**(-v1)
        self.__b = d2*X**(-v2)
        pass

    def stephan_boltzmann_pressure_from_mu(self, muB):
        return (3/(4*np.pi**2))*(muB/3)**4

    def pressure_from_mu(self, muB):
        pSB = self.stephan_boltzmann_pressure_from_mu(muB)
        return pSB*(self.__c1 - self.__a/(muB - self.__b))

    def baryon_density_from_mu(self, muB):
        pSB = self.stephan_boltzmann_pressure_from_mu(muB)
        return ((muB/3)**3/np.pi**2*(self.__c1 - self.__a/(muB - self.__b))
                + pSB*(self.__a/(muB - self.__b)**2))

    def energy_density_from_mu(self, muB):
        p = self.pressure_from_mu(muB)
        nB = self.baryon_density_from_mu(muB)
        return -p + muB*nB

    def energy_density_from(self, pressure: float) -> float:
        pass    

"""
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
"""        

    