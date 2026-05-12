from neutron_stars_computer.star.tov_solver_two_fluid import TOVInputTwoFluid
from neutron_stars_computer.star.factory_two_fluid import TwoFluidStarFactory
from neutron_stars_computer.star.constellation_two_fluid import create_two_fluid_stellar_family
from neutron_stars_computer.equationsofstate.eos import EquationOfState
from neutron_stars_computer.equationsofstate.massless_mit_bm import MasslessMITBM
from neutron_stars_computer.equationsofstate.interpolate import RIPEOS

import time
import numpy as np
import pandas as pd


def main() -> None:
    print('Starting...')
    start = time.time()

    eos_DM: EquationOfState = RIPEOS("./neutron_stars_computer/equationsofstate/tabulated_eos/DM_EOS/f_dm_m100_y0.csv")
    central_pressures_DM    = np.linspace(2e8, 43056933389.02066, 100)

    eos_BM: EquationOfState = MasslessMITBM()
    central_pressures_BM    = np.linspace(5, 300, 100)

    tov_input_two_fluid: TOVInputTwoFluid = TOVInputTwoFluid(eos_DM, eos_BM)

    fac = TwoFluidStarFactory(tov_input_two_fluid)
    two_fluid_stars: pd.DataFrame = create_two_fluid_stellar_family(fac, central_pressures_DM, central_pressures_BM)
    
    print(two_fluid_stars)

    end = time.time()
    print(f"Time to complete: {end - start:.2f} s")


if __name__ == '__main__':
    main()
