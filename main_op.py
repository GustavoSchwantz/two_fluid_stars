from neutron_stars_computer.star.stability import CentralRadOscInput
from neutron_stars_computer.star.tov_solver import TOVInput
from neutron_stars_computer.star.factory import StarStabilityFactory, StarFactory
from neutron_stars_computer.star.constellation import create_stellar_family
from neutron_stars_computer.equationsofstate.eos import EquationOfState
from neutron_stars_computer.equationsofstate.massless_mit_bm import MasslessMITBM
from neutron_stars_computer.equationsofstate.interpolate import RIPEOS
from neutron_stars_computer.equationsofstate.cfl import CFL
from neutron_stars_computer.figures_two_fluid.eos_plotter import plot_eos

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main() -> None:
    print('Starting...')
    start = time.time()

    #eos: EquationOfState = MasslessMITBM(60)
    #central_pressures = np.geomspace(1e-1, 1e4, 100)
    #tov_input = TOVInput(
    #    eos,
    #    ABSOLUTE_TOLERANCE=[1e-4, 1e-4, 1e-6],
    #    RELATIVE_TOLERANCE=1e-3
    #)


    #fac = StarFactory(tov_input)
    #stars: pd.DataFrame = create_stellar_family(
    #    fac,
    #    central_pressures
    #)
    #print(stars)

    plot_eos([MasslessMITBM(60), MasslessMITBM(90), 
                RIPEOS("./neutron_stars_computer/equationsofstate/tabulated_eos/DM_EOS/f_dm_m1_y0.csv"),
                RIPEOS("./neutron_stars_computer/equationsofstate/tabulated_eos/DM_EOS/f_dm_m0.5_y0.csv"),
                RIPEOS("./neutron_stars_computer/equationsofstate/tabulated_eos/DM_EOS/f_dm_m2_y0.csv"),
                CFL(70)], 
                ['MIT60', 'MIT90', 'FF1', 'FF0.5', 'FF2', 'CFL'],
                ['--', ':', '--', '-', ':', '-'],
                ['red', 'green', 'cyan', 'blue', 'magenta', 'black'],
                np.geomspace(1e-1, 1e4, 100), (1e0, 1e5), (1e-1, 1e4), 4, "/home/gustavo/Quarks//Huang_2026/Figure_1_2.png")

    end = time.time()
    print(f"Time to complete: {end - start:.2f} s")


if __name__ == '__main__':
    main()
