from neutron_stars_computer.star.tov_solver_dimensionless import TOVInput
from neutron_stars_computer.star.factory_dimensionless import StarFactory
from neutron_stars_computer.star.constellation_dimensionless import create_stellar_family
from neutron_stars_computer.equationsofstate.eos import EquationOfState
from neutron_stars_computer.equationsofstate.interpolate import RIPEOS
import neutron_stars_computer.star.conversionfactors as cf


import os
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

Array = np.ndarray


def main() -> None:
    print('Starting to create stars...')
    start: float = time.time()


    ######################### PREAMBLE #########################

    N_SOL: int = 500  # number of times that the TOV equations will solved

    Y = 0

    project_path: str = os.getcwd()  # current project directory
    tables_folder: str = os.path.join(project_path, 
                            'neutron_stars_computer/equationsofstate/tabulated_eos/')  # directory where the tables are stored
    csv_path: str = os.path.join(project_path, f'results/dimensionless_y{Y}.csv') # directory where the .csv with the TOV solutions will be saved


    eos: EquationOfState = RIPEOS(tables_folder + f'DM_EOS/dimesionless_f_dm_m_y{Y}.csv')


    dimensionless_central_pressures = np.geomspace(#1e-12, 1e6, N_SOL
        1e-13, 3.3333, N_SOL
    )  # values similar to the ones used in the paper
    #central_pressures_in_GeV4 = dimensionless_central_pressures * MF**4
    #central_pressures = central_pressures_in_GeV4 * cf.GEV4_TO_MEVFM3

    #print(eos.energy_density_from(1e-13))
    #print(eos.energy_density_from(3.3333)) 
    

    max_steps = np.linspace(0.01, 0.001, N_SOL)

    ############################################################


    ################ SOLVES FOR ONE-FLUID STARS ################
    
    #tov_input: TOVInput = TOVInput(eos)
    tov_input = TOVInput(
        eos,
        ABSOLUTE_TOLERANCE=[1e-8, 1e-6],
        RELATIVE_TOLERANCE=1e-13,
        #MIN_RADIUS=1e-10,
        #MAX_RADIUS=1e2,
    )
    fac: StarFactory = StarFactory(tov_input)

    stars: pd.DataFrame = create_stars(dimensionless_central_pressures, max_steps, fac)

    print(stars)

    stars.to_csv(csv_path)

    stars.plot('radius', 'mass')

    plt.savefig(project_path + f'/dimesionless_f_dm_m_y{Y}.png')

    ############################################################

    
    end: float = time.time()
    print('Stars created!')
    print(f"Time to complete: {end - start:.2f} s")


def create_stars(central_pressures: Array, max_steps: Array, fac: StarFactory) -> pd.DataFrame:

    stars: pd.DataFrame = create_stellar_family(fac, central_pressures, max_steps)
   
    #stars['mass'] = stars['mass'] / cf.M_SUN_IN_KM

    return stars


if __name__ == '__main__':
    main()
