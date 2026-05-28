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
    N_SOL = 35


    MF = 100
    Y = 0

    eos_DM: EquationOfState = RIPEOS(os.path.join(os.getcwd(), 
        f'neutron_stars_computer/equationsofstate/tabulated_eos/DM_EOS/f_dm_m{MF}_y{Y}.csv'))
    
    #cp_DM = 2.2e2  # 3 x 10^6  MeV/fm^3
    #cp_DM = 8.5e8  # 3 x 10^10 MeV/fm^3
    #cp_DM = 2e7    # 3 x 10^9  MeV/fm^3

    #central_pressures_DM = np.full(N_SOL, cp_DM)
    central_pressures_DM = np.linspace(1.1e3, 4.5e10, N_SOL)

    
    BAG_PRESS = 70

    eos_BM: EquationOfState = CFL(BAG_PRESS)

    #cp_BM = 173  # 606.4 MeV/fm^3
    cp_BM = 1100 # 3095.6 MeV/fm^3
    
    central_pressures_BM = np.full(N_SOL, cp_BM)
    #central_pressures_BM = np.linspace(5, 1015, N_SOL)
      
    #print(eos_BM.energy_density_from(1100))

    tov_input_two_fluid: TOVInputTwoFluid = TOVInputTwoFluid(eos_DM, eos_BM)

    #create_mixed_stars(central_pressures_DM, central_pressures_BM, tov_input_two_fluid, 
    #        os.path.join(os.getcwd(), f'Jurgen_with_CFL/FIG_6/FDM_m{MF}_y{Y}_CFL_B{BAG_PRESS}_{cp_BM}.csv'))
           

    
    labels: list[str] = [r'BM central density = 606.4 MeV/fm$^3$', r'BM central density = 3095.6 MeV/fm$^3$']
                         #r'DM central density = 3 x 10$^9$ MeV/fm$^3$']                     
    markers: list[str] = ['s', '^']#, '*']
    colors: list[str] = ['blue', 'red']#, 'orange']

    x: str = 'central_density_1'
    y: str = 'radius_1'
    input_folder: str = os.path.join(os.getcwd(), f'Jurgen_with_CFL/FIG_6/')
    xlim: tuple = (-0.5e11, 5e11)
    ylim: tuple = (0.6e-3, 1.4e-3)
    #xlabel: str = r'Central Energy Density of Quark Matter (MeV/fm$^3$)'
    xlabel: str = r'Central Energy Density of Dark Matter (MeV/fm$^3$)'
    #ylabel: str = r'Mass of Quark Matter (Solar Masses)'
    #ylabel: str = r'Mass of Dark Matter (Solar Masses)'
    #ylabel: str = r'Radius of Quark Matter (km)'
    ylabel: str = r'Radius of Dark Matter (km)'
    fontsize: str = '10'
    loc: str = 'upper right'
    output_folder: str = os.path.join(os.getcwd(), f'Jurgen_with_CFL/FIG_7.png')

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

    #two_fluid_stars = two_fluid_stars[ two_fluid_stars['central_density_1'] < 3.25e11 ]

    two_fluid_stars.to_csv(path)

    end = time.time()
    print('Mixed stars created!')
    print(f"Time to complete: {end - start:.2f} s")


if __name__ == '__main__':
    main()
