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

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

Array = np.ndarray


def main() -> None:
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

    #"""
    plot_eos([PQCD(X = 2)], ['X = 2'], ['--'], ['green'], 
        np.linspace(1e-4, 1e1, 100), (1e-2, 1e1), (1e-4, 1e1), 4, 
        '/home/gustavo/Quarks/test.png')
    #"""
    
    labels: list[str] = ['CFL', 'MIT60', 'FF1', 'MIT90']
    linestyles: list[str] = ['-', '--', '--', ':']
    colors: list[str] = ['black', 'red', 'cyan', 'green']

    x: str = 'radius'
    y: str = 'mass'
    input_folder: str = '/home/gustavo/Quarks/Huang_2026/figura_1/'
    output_folder: str = '/home/gustavo/Quarks/Huang_2026/Figura_2.png'
    xlim: tuple = (0, 20)
    ylim: tuple = (0, 3)
    linewidth: float = 4
    xlabel: str = 'R [km]'
    ylabel: str = r'M [M$_{\odot}$]'
    fontsize: str = '10'
    #plot_solution(x=x, y=y, input_folder=input_folder, output_folder=output_folder, labels=labels, linestyles=linestyles, colors=colors, xlim=xlim, ylim=ylim, linewidth=linewidth, xlabel=xlabel, ylabel=ylabel, fontsize=fontsize)
    
    
    #stars = pd.read_csv(input_folder + 'CFL_B70_d160_ms150_geom_1e-9_300_150.csv')
    #stars = pd.read_csv(input_folder + 'MIT_B90_geom_1e-9_600_150.csv')
    """stars = pd.read_csv('/home/gustavo/Quarks/test/FDM_m1_y0_geom_5e-3_1e4_300.csv')

    print(stars)

    print(stars[ stars['mass'] == stars['mass'].max() ])

    stars.plot('radius', 'mass')
    plt.xlabel('Radius of DM')
    plt.ylabel('Mass of DM')

    plt.savefig("/home/gustavo/Quarks/test/FDM_m1_y0_geom_5e-3_1e4_300.png")"""
"""
    eos: EquationOfState = RIPEOS('/home/gustavo/Quarks/neutron_stars_computer/equationsofstate/tabulated_eos/DM_EOS/f_dm_m2_y0.csv')

    max_mass = stars[stars['mass'] == stars['mass'].max()]

    print(max_mass)

    print('M_max:', max_mass['mass'].values[0])
    print('R:', max_mass['radius'].values[0])
    print('e:', eos.energy_density_from(max_mass['central_pressure'].values[0]))"""


def create_stars(central_pressures: Array, tov_input: TOVInput, path: str) -> None:
    print('Starting to create stars...')
    start = time.time()

    fac = StarFactory(tov_input)
    stars: pd.DataFrame = create_stellar_family(fac, central_pressures)
   
    stars['mass'] = stars['mass'] / cf.M_SUN_IN_KM

    #print(stars)

    stars.to_csv(path)
    
    end = time.time()
    print('Stars created!')
    print(f'Time to complete: {end - start:.2f} s')


if __name__ == '__main__':
    main()
