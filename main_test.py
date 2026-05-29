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
	eos_BM: EquationOfState = CFL(70)
	central_pressures_BM = np.geomspace(1e-4, 160, 300)
	#central_pressures_BM = np.linspace(1.0, 250.0, 250)
	#central_pressures_BM = np.array([100])

	eos_DM: EquationOfState = RIPEOS('/home/gustavo/Quarks/neutron_stars_computer/equationsofstate/tabulated_eos/DM_EOS/f_dm_m100_y0.csv')

	#stars = pd.read_csv('/home/gustavo/Quarks/Huang_2026/figura_2/FDM_m1_y0_geom_1e-2_400_150.csv')
	#stars = pd.read_csv('/home/gustavo/Quarks/Huang_2026/figura_2/CFL_B70_d160_ms150_geom_1e-9_300_150.csv')

	#print(stars)
	#print(stars[ stars['mass'] == stars['mass'].max() ])
	#p = stars[ stars['mass'] == stars['mass'].max() ]['central_pressure'].values[0]
	#print(p)
	#print(eos_DM.energy_density_from(p))

	#stars.plot('central_pressure', 'mass')
	#plt.savefig('fig_CFL.png')


	tov_input_two_fluid: TOVInputTwoFluid = TOVInputTwoFluid(eos_DM, eos_BM)

	chi_target = 0.7

	list_of_dfs = []

	for cp_BM in central_pressures_BM:

		cp_BM_arr = np.array([cp_BM])
		print(cp_BM)
		
		cp_DM_L = 1.1e3
		#cp_DM_R = 18.8  # central pressure for maximum mass configuration (m = 0.5, y = 0)
		#cp_DM_R = 301.0 # central pressure for maximum mass configuration (m = 1, y = 0)
		cp_DM_R = 2.9e10 # central pressure for maximum mass configuration (m = 100, y = 0)

		while True:
			cp_DM_M = (cp_DM_L + cp_DM_R) / 2
			central_pressures_DM = np.array([cp_DM_M])

			fac = TwoFluidStarFactory(tov_input_two_fluid)
			two_fluid_stars: pd.DataFrame = create_two_fluid_stellar_family(fac, central_pressures_DM, cp_BM_arr)

			#print(two_fluid_stars)

			two_fluid_stars["mass_1"] = two_fluid_stars["mass_1"] / cf.M_SUN_IN_KM
			two_fluid_stars["mass_2"] = two_fluid_stars["mass_2"] / cf.M_SUN_IN_KM

			chi_M = two_fluid_stars["mass_1"].values[0] / (two_fluid_stars["mass_1"].values[0] + two_fluid_stars["mass_2"].values[0])

			#print(chi_M)
			#print(cp_DM_M)

			if abs(chi_M - chi_target) < 1e-5:
				print('Hey!!')
				list_of_dfs.append(two_fluid_stars)
				break

			if abs(cp_DM_R - cp_DM_M) < 1e-5:
				break

			if chi_M < chi_target:
				cp_DM_L = cp_DM_M

			else:
				cp_DM_R = cp_DM_M

    
	#print(list_of_dfs)
	result = pd.concat(list_of_dfs)
	result.reset_index(drop=True, inplace=True)

	result['total_mass'] = result['mass_1'] + result['mass_2']
	result['radius'] = np.maximum(result['radius_1'], result['radius_2'])

	print(result)

	result.to_csv('/home/gustavo/Quarks/teste_m100_0.7.csv')
    

if __name__ == '__main__':
    main()	