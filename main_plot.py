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
	print('Creating a figure...')


	######################### PREAMBLE #########################

	project_path: str = os.getcwd()                                                                    # current project directory
	input_folder: str = os.path.join(project_path, 'DM_CFL', 'M_x_R')                            # directory where the .csv files with the TOV solutions are saved
	output_folder: str = os.path.join(project_path, 'DM_CFL', 'FDM_m100_y0_CFL_B70_M_max_x_e0.png') # path where the image will be saved
    
    ############################################################


	#labels: list[str] = [r'DM central density = 3 x 10$^6$ MeV/fm$^3$', r'DM central density = 3 x 10$^{10}$ MeV/fm$^3$', r'DM central density = 3 x 10$^9$ MeV/fm$^3$', r'DM central density = 3 x 10$^{11}$ MeV/fm$^3$']                     
	labels: list[str] = [r'$\chi = 0.1$', r'$\chi = 0.3$', r'$\chi = 0.5$', r'$\chi = 0.7$', r'$\chi = 0.9$']
	#labels: list[str] = [r'CFL-FF100']   


    #markers: list[str] = ['s', '^', '*', 'o']
	markers: list[str] = ['-', '-', '-', '-', '-']

	colors: list[str] = ['red', 'blue', 'pink', 'green', 'orange']

	x: str = 'central_density'
	xlim: tuple = (0, 5e11)

    #xlabel: str = r'Central Energy Density of Quark Matter (MeV/fm$^3$)'
    #xlabel: str = r'Central Energy Density of Dark Matter (MeV/fm$^3$)'
	xlabel: str = r'Central Energy Density (MeV/fm$^3$)'
	#xlabel: str = r'$\chi$'


	y: str = 'total_mass'
	ylim: tuple = (0, 0.0007)
    
    #xlabel: str = r'$\chi$'
    #ylabel: str = r'Mass of Quark Matter (Solar Masses)'
    #ylabel: str = r'Mass of Dark Matter (Solar Masses)'
    #ylabel: str = r'Radius of Quark Matter (km)'
    #ylabel: str = r'Radius of Dark Matter (km)'
	ylabel: str = r'M ($M_{\odot}$)'


	fontsize: str = '10'
	loc: str = 'upper left'


	kind='line'


	plot_solution(x=x, y=y, input_folder=input_folder, output_folder=output_folder, labels=labels, 
        markers=markers, colors=colors, xlim=xlim, ylim=ylim, kind=kind, xlabel=xlabel, ylabel=ylabel, fontsize=fontsize, loc=loc)


	print('Figure created!')


if __name__ == '__main__':
    main()