from neutron_stars_computer.star.tov_solver import TOVInput
from neutron_stars_computer.star.factory import StarFactory
from neutron_stars_computer.star.constellation import create_stellar_family
from neutron_stars_computer.equationsofstate.eos import EquationOfState
from neutron_stars_computer.equationsofstate.massless_mit_bm import MasslessMITBM
from neutron_stars_computer.equationsofstate.interpolate import RIPEOS
from neutron_stars_computer.equationsofstate.cfl import CFL
from neutron_stars_computer.figures_two_fluid.eos_plotter import plot_eos
from neutron_stars_computer.figures_two_fluid.solution_plotter import plot_solution
import neutron_stars_computer.star.conversionfactors as cf
from neutron_stars_computer.equationsofstate.pQCD import PQCD
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

    N_SOL: int = 300  # number of times that the TOV equations will solved

    BAG_PRESS: float = 70
    X: float = 4

    project_path: str = os.getcwd()  # current project directory
    tables_folder: str = os.path.join(project_path, 
                            'neutron_stars_computer/equationsofstate/tabulated_eos/')  # directory where the tables are stored
    csv_path: str = os.path.join(project_path, f'DM_pQCD/pQCD_X{X}.csv') # directory where the .csv with the TOV solutions will be saved

    #eos: EquationOfState = CFL(BAG_PRESS)
    eos: EquationOfState = RIPEOS(tables_folder + f'QM_EOS/pQCD_X{X}.csv')

    central_pressures = np.geomspace(1e-6, 2150, N_SOL)

    ############################################################


    ###################### CREATES TABLES ######################
    
    #pQCD_table_maker(X=2)
    #pQCD_table_maker(X=3)
    #pQCD_table_maker(X=4)
    FDM_table_maker(MF=30, Y=1000)

    ############################################################


    ################ SOLVES FOR ONE-FLUID STARS ################
    
    tov_input: TOVInput = TOVInput(eos)
    fac: StarFactory = StarFactory(tov_input)

    #stars: pd.DataFrame = create_stars(central_pressures, fac)

    #print(stars)

    #stars.to_csv(csv_path)

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
