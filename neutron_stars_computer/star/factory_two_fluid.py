import functools
import numpy as np
from typing import Any
from dataclasses import dataclass, field

from .tov_solver_one_fluid import TOVInputOneFluid, solve_one_fluid_tov
from .tov_solver_two_fluid import TOVInputTwoFluid, solve_two_fluid_tov
from .structure import TwoFluidStar


@dataclass(slots=True)
class TwoFluidStarFactory:
    """Creates an admixedstar from two continuous EOS."""

    tov_input_two_fluid: TOVInputTwoFluid
    tov_solution_core:  Any = field(init=False)
    tov_solution_crust: Any = field(init=False)

    def create_two_fluid_star(self, central_pressure_1: float, central_pressure_2: float) -> TwoFluidStar:
        self.tov_solution_core: Any = solve_two_fluid_tov(self.tov_input_two_fluid, central_pressure_1, central_pressure_2)

        if self.tov_solution_core.y_events[1].size != 0:  

            p1     = self.tov_solution_core.y_events[1][0][2]

            r2     = self.tov_solution_core.t_events[1][0]
            m2     = self.tov_solution_core.y_events[1][0][1]
            m_core = self.tov_solution_core.y_events[1][0][0] + m2

            tov_input_one_fluid = TOVInputOneFluid(self.tov_input_two_fluid.eos1, MIN_RADIUS = r2)

            self.tov_solution_crust: Any = solve_one_fluid_tov(tov_input_one_fluid, m_core, p1)

            r1 = self.tov_solution_crust.t_events[0][0]
            m1 = self.tov_solution_crust.y_events[0][0][0] - m2
        
        else:
            
            p2     = self.tov_solution_core.y_events[0][0][3]

            r1     = self.tov_solution_core.t_events[0][0]
            m1     = self.tov_solution_core.y_events[0][0][0]
            m_core = m1 + self.tov_solution_core.y_events[0][0][1]

            tov_input_one_fluid = TOVInputOneFluid(self.tov_input_two_fluid.eos2, MIN_RADIUS = r1)

            self.tov_solution_crust: Any = solve_one_fluid_tov(tov_input_one_fluid, m_core, p2)

            r2 = self.tov_solution_crust.t_events[0][0]
            m2 = self.tov_solution_crust.y_events[0][0][0] - m1

        central_density_1 = self.tov_input_two_fluid.eos1.energy_density_from(central_pressure_1)
        central_density_2 = self.tov_input_two_fluid.eos2.energy_density_from(central_pressure_2)

        return TwoFluidStar(central_pressure_1, central_pressure_2, central_density_1, central_density_2, r1, r2, m1, m2)

    #def set_internal_profiles(self) -> InternalProfiles:
    #    return InternalProfiles(self.tov_solution.t, *self.tov_solution.y)
