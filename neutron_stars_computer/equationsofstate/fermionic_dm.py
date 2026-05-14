from dataclasses import dataclass
from math import pi, sqrt, asinh
import numpy as np

from .eos import EquationOfState


@dataclass(slots=True, frozen=True)
class FermionicDarkMatter(EquationOfState):
    MF: float = 1 

    def energy_density_from(self, pressure: float) -> float:
        pass

    def energy_density(self, z: float) -> float:
        return ( self.MF**4 / (8*pi**2) ) * ( (2*z**3 + z)*sqrt(1 + z**2) - asinh(z))

    def pressure(self, z: float) -> float:
        return ( self.MF**4 / (24*pi**2) ) * ( (2*z**3 - 3*z)*sqrt(1 + z**2) + 3*asinh(z))    
