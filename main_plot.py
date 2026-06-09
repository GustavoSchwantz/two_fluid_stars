from neutron_stars_computer.star.tov_solver_two_fluid import TOVInputTwoFluid
from neutron_stars_computer.star.factory_two_fluid import TwoFluidStarFactory
from neutron_stars_computer.star.constellation_two_fluid import create_two_fluid_stellar_family, create_stars_with_fixed_DM
from neutron_stars_computer.equationsofstate.eos import EquationOfState
from neutron_stars_computer.equationsofstate.massless_mit_bm import MasslessMITBM
from neutron_stars_computer.equationsofstate.interpolate import RIPEOS
from neutron_stars_computer.equationsofstate.cfl import CFL
import neutron_stars_computer.star.conversionfactors as cf
from neutron_stars_computer.figures_two_fluid.solution_plotter import plot_solution
from neutron_stars_computer.figures_two_fluid.eos_plotter import plot_eos

import os
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

Array = np.ndarray


def main() -> None:
	print('Creating a figure...')


	######################### PREAMBLE #########################

	project_path: str = os.getcwd()  # current project directory
	tables_folder: str = os.path.join(project_path, 
	                        'neutron_stars_computer/equationsofstate/tabulated_eos/')  # directory where the tables are stored
	input_folder: str = os.path.join(project_path, 'Jurgen_with_pQCD/')  # directory where the .csv files with the TOV solutions are stored
	output_folder: str = os.path.join(project_path, 'Jurgen_with_pQCD/FIG_12.png') # path where the image will be stored
    
    ############################################################

	
    ################ CODE TO PLOT TOV SOLUTIONS ################

	#labels: list[str] = [r'DM central density = 1 x 10$^5$ MeV/fm$^3$', r'DM central density = 2 x 10$^6$ MeV/fm$^3$']#, r'DM central density = 3 x 10$^{11}$ MeV/fm$^3$']                     
	labels: list[str] = [r'BM central density =  709.42 MeV/fm$^3$', r'BM central density =  6774.92 MeV/fm$^3$']
	#labels: list[str] = [r'$\chi = 0.1$', r'$\chi = 0.3$', r'$\chi = 0.5$', r'$\chi = 0.7$', r'$\chi = 0.9$']
	#labels: list[str] = [r'CFL-FF100']   
	#labels: list[str] = ['X = 2', 'X = 3', 'X = 4']
	                     

	markers: list[str] = ['s', '^']
	#markers: list[str] = ['--', '-', ':']

	colors: list[str] = ['black', 'red']

	x: str = 'central_density_1'
	xlim: tuple = (-0.5e7, 2.5e7)
	#xlim: tuple = (0, 3500)

	#xlabel: str = r'Central Energy Density of Quark Matter (MeV/fm$^3$)'
	xlabel: str = r'Central Energy Density of Dark Matter (MeV/fm$^3$)'
	#xlabel: str = r'Central Energy Density (MeV/fm$^3$)'
	#xlabel: str = r'$\chi$'
	#xlabel: str = r'R (km)'


	y: str = 'radius_1'
	#ylim: tuple = (2.5e-5, 6.5e-5)
	#ylim: tuple = (0.5e-3, 1.7e-3)
	#ylim: tuple = (0, 14)
	ylim: tuple = (0.12, 0.31)
    
    #xlabel: str = r'$\chi$'
	#ylabel: str = r'Mass of Quark Matter (Solar Masses)'
	#ylabel: str = r'Mass of Dark Matter (Solar Masses)'
	#ylabel: str = r'Radius of Quark Matter (km)'
	ylabel: str = r'Radius of Dark Matter (km)'
	#ylabel: str = r'M ($M_{\odot}$)'


	fontsize: str = '10'
	loc: str = 'upper right'


	kind='scatter'


	plot_solution(x=x, y=y, input_folder=input_folder, output_folder=output_folder, labels=labels, 
        markers=markers, colors=colors, xlim=xlim, ylim=ylim, kind=kind, xlabel=xlabel, ylabel=ylabel, fontsize=fontsize, loc=loc)
    
    ############################################################
    


    ##################### CODE TO PLOT EOS #####################

	EOSs: EquationOfState = [RIPEOS(tables_folder + 'QM_EOS/pQCD_X2.csv'), 
                                RIPEOS(tables_folder + 'QM_EOS/pQCD_X3.csv'), 
                                    RIPEOS(tables_folder + 'QM_EOS/pQCD_X4.csv')]
    
	labels: list[str]     = ['X = 2', 'X = 3', 'X = 4']
	colors: list[str]     = ['green', 'orange', 'gray']
	linestyles: list[str] = ['--', '-', ':']
	pressures: Array      = np.geomspace(1e-4, 1e1, 200)
	xlim: tuple           = (1e-2, 1e1)
	ylim: tuple           = (1e-4, 1e1)
	linewidth: float      = 2

	#plot_eos(EOSs=EOSs, labels=labels, linestyles=linestyles, colors=colors, pressures=pressures,
    #            xlim=xlim, ylim=ylim, linewidth=linewidth, path=output_folder)         

    ############################################################

	print('Figure created!')


if __name__ == '__main__':
    main()