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
from neutron_stars_computer.equationsofstate.tabulated_eos_maker import table_maker, pQCD_table_maker

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

Array = np.ndarray


def main() -> None:
    X: float = 4
    #pQCD_table_maker(X)
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

    
    plot_eos([RIPEOS(f'/home/gustavo/Quarks/neutron_stars_computer/equationsofstate/tabulated_eos/QM_EOS/pQCD_X2.csv'),
              RIPEOS(f'/home/gustavo/Quarks/neutron_stars_computer/equationsofstate/tabulated_eos/QM_EOS/pQCD_X3.csv'),
              RIPEOS(f'/home/gustavo/Quarks/neutron_stars_computer/equationsofstate/tabulated_eos/QM_EOS/pQCD_X4.csv')],
     ['X = 2', 'X = 3', 'X = 4'], ['-', ':', '--'], ['orange', 'green', 'red'], 
        np.geomspace(1e-1, 1e4, 200), (1e0, 1e5), (1e-1, 1e4), 4,
        '/home/gustavo/Quarks/pQCD_v2.png')
    
    
    labels: list[str] = [r'FF1']
                         

    markers: list[str] = ['s']
    #markers: list[str] = ['-', '-', '-', '-', '-']

    colors: list[str] = ['black']

    x: str = 'radius'
    xlim: tuple = (1000, 4000)

    #xlabel: str = r'Central Energy Density of Quark Matter (MeV/fm$^3$)'
    #xlabel: str = r'Central Energy Density of Dark Matter (MeV/fm$^3$)'
    #xlabel: str = r'Central Energy Density (MeV/fm$^3$)'
    #xlabel: str = r'$\chi$'
    xlabel: str = r'R (km)'


    y: str = 'mass'
    ylim: tuple = (0, 300)
    
    #xlabel: str = r'$\chi$'
    #ylabel: str = r'Mass of Quark Matter (Solar Masses)'
    #ylabel: str = r'Mass of Dark Matter (Solar Masses)'
    #ylabel: str = r'Radius of Quark Matter (km)'
    #ylabel: str = r'Radius of Dark Matter (km)'
    ylabel: str = r'M ($M_{\odot}$)'


    fontsize: str = '10'
    loc: str = 'upper right'


    kind='scatter'


    #plot_solution(x=x, y=y, input_folder='/home/gustavo/Quarks/', output_folder='/home/gustavo/Quarks/test.png', labels=labels, 
    #    markers=markers, colors=colors, xlim=xlim, ylim=ylim, kind=kind, xlabel=xlabel, ylabel=ylabel, fontsize=fontsize, loc=loc)
    
    #stars = pd.read_csv('/home/gustavo/Quarks/FDM_m1_y1000_geom_1e-9_300_150.csv')
    #stars = pd.read_csv(input_folder + 'MIT_B90_geom_1e-9_600_150.csv')
    #stars = pd.read_csv('/home/gustavo/Quarks/test/FDM_m1_y0_geom_5e-3_1e4_300.csv')

    MF = 1

    RL: float = (cf.PLANCK_MASS_IN_MEV * 1e-3) / MF**2  # in 1/GeV
    RL /= cf.GEV_TO_FM_1 / 1e-18  # in km (1e-18 km = 1 fm)
    ML: float = (cf.PLANCK_MASS_IN_MEV * 1e-3) ** 3 / MF**2  # in GeV
    """ 
    stars["mass_in_Msun"] = stars["mass"] / cf.M_SUN_IN_KM
    stars["mass_in_GeV"] = stars["mass_in_Msun"] * cf.M_SUN_TO_GEV
    stars["dimensionless_mass"] = stars["mass_in_GeV"] / ML

    stars["dimensionless_radius"] = stars["radius"] / RL
    """
    #print(stars)

   # print(stars[ stars['dimensionless_mass'] == stars['dimensionless_mass'].max() ])
"""
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

    print(stars)

    stars.to_csv(path)
    
    end = time.time()
    print('Stars created!')
    print(f'Time to complete: {end - start:.2f} s')


if __name__ == '__main__':
    main()
