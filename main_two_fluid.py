from neutron_stars_computer.star.tov_solver_two_fluid import TOVInputTwoFluid
from neutron_stars_computer.star.factory_two_fluid import TwoFluidStarFactory
from neutron_stars_computer.star.constellation_two_fluid import create_two_fluid_stellar_family
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
    N_SOL = 55


    MF = 100
    Y = 0

    central_pressure_DM_L = 1.1e3   # smaller value allowed (m = 100, y = 0)
    central_pressure_DM_R = 2.9e10  # central pressure for maximum mass configuration (m = 100, y = 0)

    eos_DM: EquationOfState = RIPEOS(os.path.join(os.getcwd(), 
        f'neutron_stars_computer/equationsofstate/tabulated_eos/DM_EOS/f_dm_m{MF}_y{Y}.csv'))
    
    #cp_DM = 2.2e2  # 3 x 10^6  MeV/fm^3
    #cp_DM = 8.5e8  # 3 x 10^10 MeV/fm^3
    #cp_DM = 2e7    # 3 x 10^9  MeV/fm^3

    #cp_DM = 2.9e10  # 3 x 10^11  MeV/fm^3

    #central_pressures_DM = np.full(N_SOL, cp_DM)
    #central_pressures_DM = np.linspace(1.1e3, 4.5e10, N_SOL)

    
    BAG_PRESS = 70

    eos_BM: EquationOfState = CFL(BAG_PRESS)

    #cp_BM = 173  # 606.4 MeV/fm^3
    #cp_BM = 1100 # 3095.6 MeV/fm^3
    
    #central_pressures_BM = np.full(N_SOL, cp_BM)
    #central_pressures_BM = np.linspace(5, 1500, N_SOL)
    central_pressures_BM = np.geomspace(1e-4, 1200, 300) # for mixed stars with fixed DM (m = 100, y = 0)
      
    #print(eos_BM.energy_density_from(1100))

    tov_input_two_fluid: TOVInputTwoFluid = TOVInputTwoFluid(eos_DM, eos_BM)

    #create_mixed_stars(central_pressures_DM, central_pressures_BM, tov_input_two_fluid, 
    #        os.path.join(os.getcwd(), f'Jurgen_with_CFL/FIG_4/FDM_m{MF}_y{Y}_CFL_B{BAG_PRESS}_{cp_DM}.csv'))

    chi_target = 0.9

    #create_mixed_stars_with_fixed_DM(central_pressures_BM, chi_target, tov_input_two_fluid, central_pressure_DM_L,
    #    central_pressure_DM_R, os.path.join(os.getcwd(), f'DM_CFL/FDM_m{MF}_y{Y}_CFL_B{BAG_PRESS}_chi{chi_target}.csv'))
           

    
    #labels: list[str] = [r'DM central density = 3 x 10$^6$ MeV/fm$^3$', r'DM central density = 3 x 10$^{10}$ MeV/fm$^3$',
    #                     r'DM central density = 3 x 10$^9$ MeV/fm$^3$', r'DM central density = 3 x 10$^{11}$ MeV/fm$^3$']                     
    labels: list[str] = [r'$\chi = 0.1$', r'$\chi = 0.3$', r'$\chi = 0.5$', r'$\chi = 0.7$', r'$\chi = 0.9$', r'$\chi = 0$',
                         r'$\chi = 1$']
    #markers: list[str] = ['s', '^', '*', 'o']
    markers: list[str] = ['-', '-', '-', '-', '-', '-', '-']
    #colors: list[str] = ['blue', 'red', 'orange', 'green']
    colors: list[str] = ['red', 'blue', 'pink', 'green', 'orange', 'black', 'purple']

    x: str = 'radius'
    y: str = 'total_mass'
    input_folder: str = os.path.join(os.getcwd(), f'DM_CFL/')
    xlim: tuple = (0, 1.1)
    ylim: tuple = (0e-5, 70e-5)
    #xlabel: str = r'Central Energy Density of Quark Matter (MeV/fm$^3$)'
    #xlabel: str = r'Central Energy Density of Dark Matter (MeV/fm$^3$)'
    xlabel: str = 'R (km)'
    #ylabel: str = r'Mass of Quark Matter (Solar Masses)'
    #ylabel: str = r'Mass of Dark Matter (Solar Masses)'
    #ylabel: str = r'Radius of Quark Matter (km)'
    #ylabel: str = r'Radius of Dark Matter (km)'
    ylabel: str = r'M ($M_{\odot}$)'
    fontsize: str = '10'
    loc: str = 'lower right'
    output_folder: str = os.path.join(os.getcwd(), f'DM_CFL/FDM_m{MF}_y{Y}_CFL_B{BAG_PRESS}.png')

    kind='line'
    

    plot_solution(x=x, y=y, input_folder=input_folder, output_folder=output_folder, labels=labels, 
        markers=markers, colors=colors, xlim=xlim, ylim=ylim, kind=kind, xlabel=xlabel, ylabel=ylabel, fontsize=fontsize, loc=loc)


def create_mixed_stars_with_fixed_DM(central_pressures_BM: Array, chi_target: float,
    tov_input_two_fluid: TOVInputTwoFluid, central_pressure_DM_L: float, central_pressure_DM_R: float, path: str) -> None:

    print('Starting to create mixed stars with fixed proportion of dark matter...')
    start = time.time()

    list_of_dfs = []

    for cp_BM in central_pressures_BM:

        cp_BM_arr = np.array([cp_BM])
        
        cp_DM_L = central_pressure_DM_L
        cp_DM_R = central_pressure_DM_R

        while True:
            cp_DM_M = (cp_DM_L + cp_DM_R) / 2
            central_pressures_DM = np.array([cp_DM_M])

            fac = TwoFluidStarFactory(tov_input_two_fluid)
            two_fluid_stars: pd.DataFrame = create_two_fluid_stellar_family(fac, central_pressures_DM, cp_BM_arr)

            two_fluid_stars["mass_1"] = two_fluid_stars["mass_1"] / cf.M_SUN_IN_KM
            two_fluid_stars["mass_2"] = two_fluid_stars["mass_2"] / cf.M_SUN_IN_KM

            chi_M = two_fluid_stars["mass_1"].values[0] / (two_fluid_stars["mass_1"].values[0] + two_fluid_stars["mass_2"].values[0])

            if abs(chi_M - chi_target) < 1e-5:
                list_of_dfs.append(two_fluid_stars)
                break

            if abs(cp_DM_R - cp_DM_M) < 1e-5:
                break

            if chi_M < chi_target:
                cp_DM_L = cp_DM_M

            else:
                cp_DM_R = cp_DM_M

    
    result = pd.concat(list_of_dfs)
    result.reset_index(drop=True, inplace=True)

    result['total_mass'] = result['mass_1'] + result['mass_2']
    result['radius'] = np.maximum(result['radius_1'], result['radius_2'])

    result.to_csv(path)

    end = time.time()
    print('Mixed stars created!')
    print(f"Time to complete: {end - start:.2f} s")


def create_mixed_stars(central_pressures_DM: Array, central_pressures_BM: Array, 
    tov_input_two_fluid: TOVInputTwoFluid, path: str) -> None:
    
    print('Starting to create mixed stars...')
    start = time.time()

    fac = TwoFluidStarFactory(tov_input_two_fluid)
    two_fluid_stars: pd.DataFrame = create_two_fluid_stellar_family(fac, central_pressures_DM, central_pressures_BM)

    two_fluid_stars["mass_1"] = two_fluid_stars["mass_1"] / cf.M_SUN_IN_KM
    two_fluid_stars["mass_2"] = two_fluid_stars["mass_2"] / cf.M_SUN_IN_KM
    
    print(two_fluid_stars)

    #two_fluid_stars = two_fluid_stars[ two_fluid_stars['central_density_1'] < 3.25e11 ]

    two_fluid_stars.to_csv(path)

    end = time.time()
    print('Mixed stars created!')
    print(f"Time to complete: {end - start:.2f} s")


if __name__ == '__main__':
    main()
