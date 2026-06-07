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

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

Array = np.ndarray


def main() -> None:

    ###################### CREATES TABLES ######################
    
    pQCD_table_maker(X=2)
    pQCD_table_maker(X=3)
    pQCD_table_maker(X=4)

    ############################################################


    """
    create_stars(np.geomspace(1e-9, 300, 150), TOVInput(
        RIPEOS('/home/gustavo/Quarks/neutron_stars_computer/equationsofstate/tabulated_eos/DM_EOS/f_dm_m1_y1000.csv')), 
    '/home/gustavo/Quarks/FDM_m1_y1000_geom_1e-9_300_150.csv')
    """

    #create_stars(np.geomspace(1e-9, 300, 150), TOVInput(CFL(70)), '/home/gustavo/Quarks/Huang_2026/figura_1/CFL_B70_d160_ms150_geom_1e-9_300_150.csv')

    #create_stars(np.geomspace(1e-9, 600, 150), TOVInput( MasslessMITBM(90) ), '/home/gustavo/Quarks/Huang_2026/figura_1/MIT_B90_geom_1e-9_600_150.csv')
    """
    create_stars(np.geomspace(5e-3, 1e4, 300), 
        TOVInput( RIPEOS('/home/gustavo/Quarks/neutron_stars_computer/equationsofstate/tabulated_eos/DM_EOS/f_dm_m1_y0.csv'),
                  #ABSOLUTE_TOLERANCE=[1e-4, 1e-8, 1e-6],
                  #RELATIVE_TOLERANCE=1e-13,
                  #MIN_RADIUS=1e-10,
                  #MAX_RADIUS=1e-2, 
        ), 
        '/home/gustavo/Quarks/test/FDM_m1_y0_geom_5e-3_1e4_300.csv')"""

    
    
    
    
    
    


def create_stars(central_pressures: Array, tov_input: TOVInput, path: str) -> None:
    print('Starting to create stars...')
    start = time.time()

    fac = StarFactory(tov_input)
    stars: pd.DataFrame = create_stellar_family(fac, central_pressures)
   
    stars['mass'] = stars['mass'] / cf.M_SUN_IN_KM

    print(stars)

    stars.to_csv(path)
    
    end = time.time()
    print('Stars created!')
    print(f'Time to complete: {end - start:.2f} s')


if __name__ == '__main__':
    main()
