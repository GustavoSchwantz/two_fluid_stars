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
from typing import Iterable

Array = np.ndarray


def main() -> None:
    print('Starting to create mixed stars...')
    start: float = time.time()

    ######################### PREAMBLE #########################

    N_SOL: int = 150  # number of times that the TOV equations will solved

    CHI: float = 0.1  # fraction of dark matter in a two-fluid star
    CHIs: list[float] = np.linspace(0.02, 0.98, 40)  # fractions of dark matter in a two-fluid star

    project_path: str = os.getcwd()  # current project directory
    tables_folder: str = os.path.join(project_path, 
                            'neutron_stars_computer/equationsofstate/tabulated_eos/')  # directory where the tables are stored
    csv_path: str = os.path.join(project_path, 'poster/m_DM_x_e0DM/') # directory where the .csv with the TOV solutions will be saved

    ############################################################


    ######################### DARK MATTER STUFF #########################

    MF: float = 100  # fermionic mass em GeV
    Y: int = 1000  # interaction parameter for the fermionics dark matter 

    #central_pressure_DM_L: float = 1.1e3   # smaller pressure value allowed for this EoS (m = 100, y = 0)
    #central_pressure_DM_R: float = 2.9e10  # central pressure for maximum mass configuration (m = 100, y = 0)

    central_pressure_DM_L: float = 1e2   # smaller pressure value allowed for this EoS ? (m = 100, y = 1000)
    central_pressure_DM_R: float = 1.4e6 # central pressure for maximum mass configuration (m = 100, y = 1000)

    eos_DM: EquationOfState = RIPEOS(tables_folder + f'DM_EOS/f_dm_m{MF}_y{Y}.csv')
    
    """ Fixed DM (MF = 100 GeV, Y = 0) pressure values used by Jürgen (2016) for two-fluid stars: """ 

    #cp_DM = 2.2e2  # 3 x 10^6  MeV/fm^3
    #cp_DM = 8.5e8  # 3 x 10^10 MeV/fm^3
    #cp_DM = 2e7    # 3 x 10^9  MeV/fm^3

    #cp_DM = 2.9e10  # 3 x 10^11  MeV/fm^3 (central density of the maximum mass configuration)

    """ Fixed DM (MF = 100 GeV, Y = 1000) pressure values used by Jürgen (2016) for two-fluid stars: """

    #cp_DM = 90e1  # 1 x 10^5 MeV/fm^3
    #cp_DM = 1e5   # 1 x 10^6 MeV/fm^3
    #cp_DM = 3e5   # 2 x 10^6 MeV/fm^3

    #cp_DM = 6.51e-4

    #central_pressures_DM = np.full(N_SOL, cp_DM)
    #central_pressures_DM = np.geomspace(central_pressure_DM_L, central_pressure_DM_R, 17)
    #central_pressures_DM = np.concatenate((np.linspace(2.5e8, 1.6e10, 20), np.linspace(1.6e10, 5e10, 30)))
    #central_pressures_DM = np.geomspace(1e3, 3.5e5, 17)
    #central_pressures_DM = np.concatenate((np.linspace(1e2, 0.75e6, 25), np.linspace(1e6, 1e7, 25)))
    #central_pressures_DM = np.linspace(1e-6, 2e5, N_SOL)
    central_pressures_DM = np.linspace(1e2, 1e7, N_SOL)

    #####################################################################


    ######################### BARIONIC MATTER STUFF #########################

    BAG_PRESS: float = 70
    X: float = 3

    eos_BM: EquationOfState = RIPEOS(tables_folder + f'QM_EOS/pQCD_X{X}.csv')
    #eos_BM: EquationOfState = MasslessMITBM()
    #eos_BM: EquationOfState = CFL(BAG_PRESS)

    #cp_BM = 173  # 606.4 MeV/fm^3 (CFL)
    #cp_BM = 1100 # 3095.6 MeV/fm^3 (CFL)
    #cp_BM = 2500  # 7034.6 MeV/fm^3 (CFL)
    #cp_BM = 150 # 709.42 MeV/fm^3 (pQCD)
    #cp_BM = 750 # 2723.87 MeV/fm^3 (pQCD)
    #cp_BM = 2000 # 6774.92 MeV/fm^3 (pQCD)
    #cp_BM = 124

    #cp_BM = 600   # 1726.8 MeV/fm^3 (CFL)
    #cp_BM = 2126  # 5973.3 MeV/fm^3 (CFL)
    #cp_BM = 450   # 1729.2 MeV/fm^3 (pQCD)
    cp_BM = 1750  # 5971.7 MeV/fm^3 (pQCD)
    #cp_BM = 500.67 # 1730.01 MeV/fm^3 (MIT)
    #cp_BM = 1914 # 5970 MeV/fm^3 (MIT)
    
    central_pressures_BM = np.full(N_SOL, cp_BM)
    #central_pressures_BM = np.geomspace(1e-9, 2150, N_SOL)
    #central_pressures_BM = np.linspace(1e-4, 800, N_SOL)
    #central_pressures_BM = np.linspace(1e-9, 8000, N_SOL)
      
    #########################################################################

    
    ################ SOLVES FOR TWO-FLUID STARS ################

    tov_input_two_fluid: TOVInputTwoFluid = TOVInputTwoFluid(eos_DM, eos_BM)

    fac = TwoFluidStarFactory(tov_input_two_fluid)


    """ Creates two-fluid stars given two EoSs and two sets of central pressures """
    two_fluid_stars: pd.DataFrame = create_mixed_stars(central_pressures_DM, central_pressures_BM, fac)


    """ Creates two-fluid stars with fixed fraction of dark matter """       
    #two_fluid_stars: pd.DataFrame = create_stars_with_fixed_DM(central_pressures_BM, chi, fac, central_pressure_DM_L, central_pressure_DM_R)

    """ Creates two-fluid stars with maximum masses """
    #two_fluid_stars: pd.DataFrame = create_mixed_stars_with_max_mass(central_pressures_DM, central_pressures_BM, fac, N_SOL)


    #list_of_two_fluid_stars: Iterable[pd.DataFrame] = create_stars_for_various_chis(central_pressures_BM, CHIs, fac, 
    #                                                                                    central_pressure_DM_L, central_pressure_DM_R)
    """
    list_of_dfs = []

    for chi in CHIs:
        two_fluid_stars: pd.DataFrame = pd.read_csv(csv_path + f'FDM_m{MF}_y{Y}_MIT_B{BAG_PRESS}_chi{chi}.csv')

        max_total_mass: pd.DataFrame = two_fluid_stars[two_fluid_stars['total_mass'] == two_fluid_stars['total_mass'].max()]

        list_of_dfs.append(max_total_mass)


    result: pd.DataFrame = pd.concat(list_of_dfs)
    result.reset_index(drop=True, inplace=True)

    result.to_csv(csv_path + 'result.csv')
    """

    ############################################################


    ####################### SAVE OR PLOT ######################           

    two_fluid_stars_scaled: pd.DataFrame = scale_solutions(two_fluid_stars, MF)  
    
    two_fluid_stars_scaled.to_csv(csv_path + f'FDM_m{MF}_y{Y}_pQCD_X{X}_cp{cp_BM}.csv')

    #plot_max_total_mass(two_fluid_stars, os.path.join(project_path, 'Jurgen_with_pQCD/', 'FIG_14.png'))

    #for two_fluid_stars, chi in zip(list_of_two_fluid_stars, CHIs):
    #    two_fluid_stars.to_csv(csv_path + f'FDM_m{MF}_y{Y}_CFL_B{BAG_PRESS}_chi{chi}.csv')

    ############################################################

    
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

    #two_fluid_stars = two_fluid_stars[ two_fluid_stars['central_density_1'] < 1.5e7 ]

    return two_fluid_stars


def create_mixed_stars_with_max_mass(central_pressures_DM: Array, central_pressures_BM: Array, 
                        fac: TwoFluidStarFactory, N_SOL: int) -> pd.DataFrame:

    list_of_dfs = []

    for p0_DM in central_pressures_DM:

        fixed_central_pressures_DM = np.full(N_SOL, p0_DM)

        two_fluid_stars: pd.DataFrame = create_two_fluid_stellar_family(fac, fixed_central_pressures_DM, central_pressures_BM)

        two_fluid_stars["mass_1"] = two_fluid_stars["mass_1"] / cf.M_SUN_IN_KM
        two_fluid_stars["mass_2"] = two_fluid_stars["mass_2"] / cf.M_SUN_IN_KM

        max_mass = two_fluid_stars[two_fluid_stars['mass_2'] == two_fluid_stars['mass_2'].max()]

        max_mass["total_mass"] = max_mass["mass_1"] + max_mass["mass_2"]

        max_mass["DM_fraction"] = max_mass["mass_1"] / max_mass["total_mass"]

        list_of_dfs.append(max_mass)


    max_masses: pd.DataFrame = pd.concat(list_of_dfs)
    max_masses.reset_index(drop=True, inplace=True)

    print(max_masses)

    return max_masses


def plot_max_total_mass(max_masses: pd.DataFrame, path: str) -> None:

    x = max_masses["DM_fraction"]
    y = max_masses["total_mass"] 

    m, b = np.polyfit(x, y, 1)

    plt.scatter(x, y, color="black", marker='s')

    plt.plot(x, m * x + b, color='red', linestyle='solid', label=f'y = {m:.2f}x + {b:.2f}')

    plt.xlabel(r"Fraction of dark matter ($M_{int}/M_{total, max}$)")
    plt.ylabel(r"Maximum total mass $M_{total, max}$")
    plt.legend()

    plt.savefig(path)


def create_stars_for_various_chis(central_pressures_BM: Iterable[float], CHIs: Iterable[float], fac: TwoFluidStarFactory,
                                    cp_DM_L: float, cp_DM_R: float) -> Iterable[pd.DataFrame]: 
    
    list_of_dfs = []

    for chi in CHIs:

        print(f'Creating stars with \u03C7 = {chi} ...')
        start: float = time.time()

        two_fluid_stars: pd.DataFrame = create_stars_with_fixed_DM(central_pressures_BM, chi, fac, cp_DM_L, cp_DM_R)

        list_of_dfs.append(two_fluid_stars)

        end: float = time.time()
        print(f'Stars with \u03C7 = {chi} created in {end - start:.2f} s')


    return list_of_dfs


def scale_solutions(two_fluid_stars: pd.DataFrame, MF: float) -> pd.DataFrame:

    print(MF)
    print(two_fluid_stars['mass_1'])

    ML: float = (cf.PLANCK_MASS_IN_MEV * 1e-3) ** 3 / MF**2  # in GeV

    print(ML)

    two_fluid_stars['mass_1__in_GeV'] = two_fluid_stars['mass_1'] * cf.M_SUN_TO_GEV
    print(two_fluid_stars['mass_1__in_GeV'])
    two_fluid_stars['dimensionless_mass_1'] = two_fluid_stars['mass_1__in_GeV'] / ML

    print(two_fluid_stars['dimensionless_mass_1'])

    two_fluid_stars['central_density_1_in_GEV4'] = two_fluid_stars['central_density_1'] / cf.GEV4_TO_MEVFM3
    two_fluid_stars['dimensionless_central_density_1'] = two_fluid_stars['central_density_1_in_GEV4'] / MF**4

    return two_fluid_stars


if __name__ == '__main__':
    main()
