from neutron_stars_computer.star.tov_solver_two_fluid import TOVInputTwoFluid
from neutron_stars_computer.star.factory_two_fluid import TwoFluidStarFactory
from neutron_stars_computer.star.constellation_two_fluid import create_two_fluid_stellar_family, create_stars_with_fixed_DM
from neutron_stars_computer.equationsofstate.eos import EquationOfState
from neutron_stars_computer.equationsofstate.massless_mit_bm import MasslessMITBM
from neutron_stars_computer.equationsofstate.interpolate import RIPEOS
from neutron_stars_computer.equationsofstate.cfl import CFL
import neutron_stars_computer.star.conversionfactors as cf
from neutron_stars_computer.figures_two_fluid.solution_plotter import plot_solution

import os
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

Array = np.ndarray


def main() -> None:
    print('Starting to create mixed stars...')
    start: float = time.time()

    ######################### PREAMBLE #########################

    N_SOL: int = 300 # number of times that the TOV equations will solved

    CHI: float = 0.1                              # fraction of dark matter in a two-fluid star
    CHIS: list[float] = [0.1, 0.3, 0.5, 0.7, 0.9] # fractions of dark matter in a two-fluid star

    project_path: str = os.getcwd()                       # current project directory
    csv_path: str = os.path.join(project_path, 'DM_CFL/')  # directory where the .csv with the TOV solutions will be saved

    ############################################################


    ######################### DARK MATTER STUFF #########################

    MF: float = 100 # fermionic mass em GeV
    Y: int = 0      # interaction parameter for the fermionics dark matter 

    central_pressure_DM_L: float = 1.1e3   # smaller pressure value allowed for this EoS (m = 100, y = 0)
    central_pressure_DM_R: float = 2.9e10  # central pressure for maximum mass configuration (m = 100, y = 0)

    eos_DM: EquationOfState = RIPEOS(os.path.join(project_path, 
        f'neutron_stars_computer/equationsofstate/tabulated_eos/DM_EOS/f_dm_m{MF}_y{Y}.csv'))
    
    """ Fixed DM (MF = 100 GeV, Y = 0) pressure values used by Jürgen (2016) for two-fluid stars: """ 

    #cp_DM = 2.2e2  # 3 x 10^6  MeV/fm^3
    #cp_DM = 8.5e8  # 3 x 10^10 MeV/fm^3
    #cp_DM = 2e7    # 3 x 10^9  MeV/fm^3

    #cp_DM = 2.9e10  # 3 x 10^11  MeV/fm^3 (central density of the maximum mass configuration)

    #central_pressures_DM = np.full(N_SOL, cp_DM)
    #central_pressures_DM = np.geomspace(central_pressure_DM_L, central_pressure_DM_R, 17)

    #####################################################################


    ######################### BARIONIC MATTER STUFF #########################

    BAG_PRESS: float = 70

    eos_BM: EquationOfState = CFL(BAG_PRESS)

    #cp_BM = 173  # 606.4 MeV/fm^3
    #cp_BM = 1100 # 3095.6 MeV/fm^3
    
    #central_pressures_BM = np.full(N_SOL, cp_BM)
    #central_pressures_BM = np.linspace(5, 1500, N_SOL)
    central_pressures_BM = np.geomspace(1e-4, 1200, N_SOL) # for mixed stars with fixed DM (m = 100, y = 0)
      
    #########################################################################


    tov_input_two_fluid: TOVInputTwoFluid = TOVInputTwoFluid(eos_DM, eos_BM)

    fac = TwoFluidStarFactory(tov_input_two_fluid)


    """ Creates two-fluid stars given two EoSs and two sets of central pressures """
    #two_fluid_stars: pd.DataFrame = create_mixed_stars(central_pressures_DM, central_pressures_BM, fac)


    """ Creates two-fluid stars with fixed fraction of dark matter """       
    #two_fluid_stars = create_stars_with_fixed_DM(central_pressures_BM, chi, fac, central_pressure_DM_L, central_pressure_DM_R)

    #two_fluid_stars.to_csv(csv_path)

    list_of_dfs = []

    for chi in np.linspace(0.02, 0.98, 40):

        print(f'Starting to create stars with \u03C7 = {chi} ...')
        s: float = time.time()

        two_fluid_stars: pd.DataFrame = create_stars_with_fixed_DM(central_pressures_BM, chi, fac, 
            central_pressure_DM_L, central_pressure_DM_R)

        two_fluid_stars.to_csv(csv_path + f'FDM_m100_y0_CFL_B70_{chi}.csv')

        max_mass_sol = two_fluid_stars[ two_fluid_stars['total_mass'] == two_fluid_stars['total_mass'].max() ]
        list_of_dfs.append(max_mass_sol)

        e: float = time.time()
        print(f'Stars with \u03C7 = {chi} created!')
        print(f"Time to complete: {e - s:.2f} s")


    max_solutions = pd.concat(list_of_dfs)    
    max_solutions.reset_index(drop=True, inplace=True)

    max_solutions.to_csv(csv_path + 'solution.csv')

    
    end: float = time.time()
    print('Mixed stars created!')
    print(f"Time to complete: {end - start:.2f} s")


def create_mixed_stars(central_pressures_DM: Array, central_pressures_BM: Array, 
                        fac: TwoFluidStarFactory) -> pd.DataFrame:

    two_fluid_stars: pd.DataFrame = create_two_fluid_stellar_family(fac, central_pressures_DM, central_pressures_BM)

    two_fluid_stars["mass_1"] = two_fluid_stars["mass_1"] / cf.M_SUN_IN_KM
    two_fluid_stars["mass_2"] = two_fluid_stars["mass_2"] / cf.M_SUN_IN_KM

    two_fluid_stars['central_density'] = two_fluid_stars['central_density_1'] + two_fluid_stars['central_density_2']
    
    print(two_fluid_stars)

    #two_fluid_stars = two_fluid_stars[ two_fluid_stars['central_density_1'] < 3.25e11 ]

    return two_fluid_stars


if __name__ == '__main__':
    main()
