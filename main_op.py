from neutron_stars_computer.star.tov_solver import TOVInput
from neutron_stars_computer.star.factory import StarFactory
from neutron_stars_computer.star.constellation import create_stellar_family
from neutron_stars_computer.equationsofstate.eos import EquationOfState
#from neutron_stars_computer.equationsofstate.massless_mit_bm import MasslessMITBM
from neutron_stars_computer.equationsofstate.interpolate import RIPEOS
#from neutron_stars_computer.equationsofstate.cfl import CFL
#from neutron_stars_computer.figures_two_fluid.eos_plotter import plot_eos
#from neutron_stars_computer.figures_two_fluid.solution_plotter import plot_solution
import neutron_stars_computer.star.conversionfactors as cf
#from neutron_stars_computer.equationsofstate.pQCD import PQCD
from neutron_stars_computer.equationsofstate.tabulated_eos_maker import FDM_table_maker, pQCD_table_maker

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

    N_SOL: int = 150  # number of times that the TOV equations will solved

    MF = 100  # in GeV
    Y = 0
    BAG_PRESS: float = 70
    X: float = 4

    project_path: str = os.getcwd()  # current project directory
    tables_folder: str = os.path.join(project_path, 
                            'neutron_stars_computer/equationsofstate/tabulated_eos/')  # directory where the tables are stored
    csv_path: str = os.path.join(project_path, f'results/mf{MF}_y{Y}.csv') # directory where the .csv with the TOV solutions will be saved

    #FDM_table_maker(MF=MF, Y=Y)

    #eos: EquationOfState = CFL(BAG_PRESS)
    eos: EquationOfState = RIPEOS(tables_folder + f'DM_EOS/f_dm_m{MF}_y{Y}.csv')

    #central_pressures = np.geomspace(1e-6, 2150, N_SOL)

    dimensionless_central_pressures = np.geomspace(
        1e-13, 3.3333, N_SOL
    )  # values similar to the ones used in the paper
    central_pressures_in_GeV4 = dimensionless_central_pressures * MF**4
    central_pressures = central_pressures_in_GeV4 * cf.GEV4_TO_MEVFM3

    ############################################################


    ###################### CREATES TABLES ######################
    
    #pQCD_table_maker(X=2)
    #pQCD_table_maker(X=3)
    #pQCD_table_maker(X=4)
    #FDM_table_maker(MF=30, Y=1000)

    ############################################################


    ################ SOLVES FOR ONE-FLUID STARS ################
    
    #tov_input: TOVInput = TOVInput(eos)
    tov_input = TOVInput(
        eos,
        ABSOLUTE_TOLERANCE=[1e-4, 1e-8, 1e-6],
        RELATIVE_TOLERANCE=1e-13,
        MIN_RADIUS=1e-10,
        MAX_RADIUS=1e-2,
    )
    fac: StarFactory = StarFactory(tov_input)

    stars: pd.DataFrame = create_stars(np.array([2.8e10]), fac)

    print(stars)

    #stars.to_csv(csv_path)

    #stars.plot('radius', 'mass')

    #plt.savefig(project_path + f'/f_dm_m{MF}_y{Y}.png')

    ############################################################

    
    end: float = time.time()
    print('Stars created!')
    print(f"Time to complete: {end - start:.2f} s")


def create_stars(central_pressures: Array, fac: StarFactory) -> pd.DataFrame:

    stars: pd.DataFrame = create_stellar_family(fac, central_pressures)
   
    stars['mass'] = stars['mass'] / cf.M_SUN_IN_KM

    return stars


if __name__ == '__main__':
    main()
