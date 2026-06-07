from scipy.differentiate import derivative
from dataclasses import dataclass, field
import numpy as np
import sympy as sp

from .eos import EquationOfState
import neutron_stars_computer.star.conversionfactors as cf


@dataclass(slots=True, frozen=True)
class PQCD(EquationOfState):
    X: float    = 4

    c1: float = field(default=0.9008, init=False)
    d1: float = field(default=0.5034, init=False)
    d2: float = field(default=1.452, init=False)
    v1: float = field(default=0.3553, init=False)
    v2: float = field(default=0.9101, init=False)

    a: float = field(init=False)
    b: float = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, 'a', self.d1*self.X**(-self.v1))
        object.__setattr__(self, 'b', self.d2*self.X**(-self.v2))

    def stephan_boltzmann_pressure_from_mu(self, muB):
        return (3/(4*np.pi**2))*(muB/3)**4

    def pressure_from_mu(self, muB):
        pSB = self.stephan_boltzmann_pressure_from_mu(muB)
        return pSB*(self.c1 - self.a/(muB - self.b))

    def baryon_density_from_mu(self, muB):
        pSB = self.stephan_boltzmann_pressure_from_mu(muB)
        return ((muB/3)**3/np.pi**2*(self.c1 - self.a/(muB - self.b))
                + pSB*(self.a/(muB - self.b)**2))

    def energy_density_from_mu(self, muB):
        p = self.pressure_from_mu(muB)
        nB = self.baryon_density_from_mu(muB)
        return -p + muB*nB

    def energy_density_from(self, pressure: float) -> float:
        pass    

    