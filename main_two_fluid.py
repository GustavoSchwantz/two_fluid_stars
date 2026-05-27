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

    eos_DM: EquationOfState = RIPEOS(os.path.join(os.getcwd(), 
        f'neutron_stars_computer/equationsofstate/tabulated_eos/DM_EOS/f_dm_m{MF}_y{Y}.csv'))
    
    cp_DM = 2.2e2  # 3 x 10^6  MeV/fm^3
    #cp_DM = 8.5e8  # 3 x 10^10 MeV/fm^3
    #cp_DM = 2e7    # 3 x 10^9  MeV/fm^3

    central_pressures_DM = np.full(N_SOL, cp_DM)

    
    BAG_PRESS = 70

    eos_BM: EquationOfState = CFL(BAG_PRESS)
    central_pressures_BM = np.linspace(5, 1015, N_SOL)

    #central_pressures_BM = np.full(300, 124)   # 484.9 MeV/fm^3
    #central_pressures_BM = np.full(300, 924)     # 2609.9 MeV/fm^3

    #print(eos_BM.energy_density_from(924))

    tov_input_two_fluid: TOVInputTwoFluid = TOVInputTwoFluid(eos_DM, eos_BM)

    #create_mixed_stars(central_pressures_DM, central_pressures_BM, tov_input_two_fluid, 
    #        os.path.join(os.getcwd(), f'Jurgen_with_CFL/FIG_4/FDM_m{MF}_y{Y}_CFL_B{BAG_PRESS}_{cp_DM}.csv'))
           

    
    labels: list[str] = [r'DM central density = 3 x 10$^6$ MeV/fm$^3$', r'DM central density = 3 x 10$^{10}$ MeV/fm$^3$']
                         #r'DM central density = 3 x 10$^9$ MeV/fm$^3$']
    markers: list[str] = ['s', '^']#, '*']
    colors: list[str] = ['blue', 'red']#, 'orange']

    x: str = 'central_density_2'
    y: str = 'radius_2'
    input_folder: str = os.path.join(os.getcwd(), f'Jurgen_with_CFL/FIG_4/')
    xlim: tuple = (0, 3000)
    ylim: tuple = (0, 14)
    xlabel: str = r'Central Energy Density of Quark Matter (MeV/fm$^3$)'
    #ylabel: str = r'Mass of Quark Matter (Solar Masses)'
    ylabel: str = r'Radius of Quark Matter (km)'
    fontsize: str = '10'
    loc: str = 'lower right'
    output_folder: str = os.path.join(os.getcwd(), f'Jurgen_with_CFL/FIG_5.png')

    kind='scatter'
    

    plot_solution(x=x, y=y, input_folder=input_folder, output_folder=output_folder, labels=labels, 
        markers=markers, colors=colors, xlim=xlim, ylim=ylim, kind=kind, xlabel=xlabel, ylabel=ylabel, fontsize=fontsize, loc=loc)


def create_mixed_stars(central_pressures_DM: Array, central_pressures_BM: Array, 
    tov_input_two_fluid: TOVInputTwoFluid, path: str) -> None:
    
    print('Starting to create mixed stars...')
    start = time.time()

    fac = TwoFluidStarFactory(tov_input_two_fluid)
    two_fluid_stars: pd.DataFrame = create_two_fluid_stellar_family(fac, central_pressures_DM, central_pressures_BM)

    two_fluid_stars["mass_1"] = two_fluid_stars["mass_1"] / cf.M_SUN_IN_KM
    two_fluid_stars["mass_2"] = two_fluid_stars["mass_2"] / cf.M_SUN_IN_KM
    
    print(two_fluid_stars)

    two_fluid_stars.to_csv(path)

    end = time.time()
    print('Mixed stars created!')
    print(f"Time to complete: {end - start:.2f} s")


if __name__ == '__main__':
    main()
