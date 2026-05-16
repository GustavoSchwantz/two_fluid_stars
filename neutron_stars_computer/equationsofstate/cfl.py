from dataclasses import dataclass
from math import pi, sqrt
import neutron_stars_computer.star.conversionfactors as cf

from .eos import EquationOfState


@dataclass(slots=True, frozen=True)
class CFL(EquationOfState):
    BAG_PRESS: float = 57
    delta: float = 160
    ms: float = 150 

    def energy_density_from(self, pressure: float) -> float:
        alpha = 2 * self.delta**2 / 3 - self.ms**2 / 6
        mi_square = sqrt( 9 * alpha**2 + 4 * pi**2 * ((self.BAG_PRESS + pressure)*cf.MEV_FM3_TO_MEV4) / 3 ) - 3 * alpha

        return 3 * pressure + 4 * self.BAG_PRESS - (9 * alpha * mi_square / pi**2) / cf.MEV_FM3_TO_MEV4
