from neutron_stars_computer.star.tov_solver_two_fluid import TOVInputTwoFluid
from neutron_stars_computer.star.factory_two_fluid import TwoFluidStarFactory
from neutron_stars_computer.star.constellation_two_fluid import create_two_fluid_stellar_family
from neutron_stars_computer.equationsofstate.eos import EquationOfState
from neutron_stars_computer.equationsofstate.massless_mit_bm import MasslessMITBM
from neutron_stars_computer.equationsofstate.interpolate import RIPEOS
from neutron_stars_computer.equationsofstate.cfl import CFL
import neutron_stars_computer.star.conversionfactors as cf
from neutron_stars_computer.figures_two_fluid.solution_plotter import plot_solution

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

Array = np.ndarray


def main() -> None:
    eos_DM: EquationOfState = RIPEOS('/home/gustavo/Quarks/neutron_stars_computer/equationsofstate/tabulated_eos/DM_EOS/f_dm_m100_y0.csv')
    #central_pressures_DM = np.full(150, 2.2e2) # 3 x 10^6  MeV/fm^3
    #central_pressures_DM = np.full(150, 8.5e8) # 3 x 10^10 MeV/fm^3
    central_pressures_DM = np.full(150, 2e7)   # 3 x 10^9  MeV/fm^3

    eos_BM: EquationOfState = CFL(70)
    central_pressures_BM = np.linspace(1e-6, 924, 150)

    tov_input_two_fluid: TOVInputTwoFluid = TOVInputTwoFluid(eos_DM, eos_BM)

    #create_mixed_stars(central_pressures_DM, central_pressures_BM, tov_input_two_fluid, 
    #    '/home/gustavo/Quarks/Jurgen_with_CFL/FDM_m100_y0_CFL_B70_p0_dark_2e7_lin_1e-6_924_150.csv')

    
    labels: list[str] = [r'Densidade central de matéria escura: 3 x 10$^6$ MeV/fm$^3$',
                         r'Densidade central de matéria escura: 3 x 10$^{10}$ MeV/fm$^3$',
                         r'Densidade central de matéria escura: 3 x 10$^9$ MeV/fm$^3$']
    linestyles: list[str] = ['-', '-', '-']
    colors: list[str] = ['pink', 'blue', 'red']

    x: str = 'central_density_2'
    y: str = 'mass_2'
    input_folder: str = '/home/gustavo/Quarks/Jurgen_with_CFL/'
    output_folder: str = '/home/gustavo/Quarks/Jurgen_with_CFL/FIG_4.png'
    xlim: tuple = (0, 3000)
    ylim: tuple = (0, 3)
    linewidth: float = 2
    xlabel: str = 'Central Energy Density of Quark Matter (MeV/fm$^3$)'
    ylabel: str = 'Mass of Quark Matter (in Solar Masses)'
    fontsize: str = '7.5'
    plot_solution(x=x, y=y, input_folder=input_folder, output_folder=output_folder, labels=labels, linestyles=linestyles, colors=colors, xlim=xlim, ylim=ylim, linewidth=linewidth, xlabel=xlabel, ylabel=ylabel, fontsize=fontsize)
    

    #mixed_stars = pd.read_csv("/home/gustavo/Quarks/Jurgen_with_CFL/FDM_m100_y0_CFL_B70_p0_dark_2.2e2.csv")
    
    #mixed_stars.plot('central_density_2', 'mass_2')

    #plt.savefig("/home/gustavo/Quarks/Jurgen_with_CFL/FIG_4.png")


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
