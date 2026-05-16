from neutron_stars_computer.equationsofstate.eos import EquationOfState
from neutron_stars_computer.equationsofstate.interpolate import RIPEOS
from neutron_stars_computer.equationsofstate.massless_mit_bm import MasslessMITBM
from neutron_stars_computer.equationsofstate.cfl import CFL

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main() -> None:
	EOSs: list[EquationOfState] = [MasslessMITBM(60), MasslessMITBM(90), 
	                                RIPEOS("./neutron_stars_computer/equationsofstate/tabulated_eos/DM_EOS/f_dm_m1_y0.csv"),
	                                RIPEOS("./neutron_stars_computer/equationsofstate/tabulated_eos/DM_EOS/f_dm_m0.5_y0.csv"),
	                                RIPEOS("./neutron_stars_computer/equationsofstate/tabulated_eos/DM_EOS/f_dm_m2_y0.csv"),
	                                CFL(70)]
	labels: list[str] = ['MIT60', 'MIT90', 'FF1', 'FF0.5', 'FF2', 'CFL']
	linestyles: list[str] = ['--', ':', '--', '-', ':', '-']
	colors: list[str] = ['red', 'green', 'cyan', 'blue', 'magenta', 'black']

	pressures = np.geomspace(1e-1, 1e4, 100)

	fig, ax = plt.subplots()

	for eos, label, linestyle, color in zip(EOSs, labels, linestyles, colors):
		densities = np.array([eos.energy_density_from(p) for p in pressures])

		pd.DataFrame({'p': pressures, 'd': densities}).plot('d', 'p', loglog=True, xlim=(1e0, 1e5), ylim=(1e-1, 1e4), ax=ax, 
			label=label, linestyle=linestyle, color=color, linewidth=4)


	plt.xlabel(r'$\epsilon$ [MeV/fm$^3$]')
	plt.ylabel(r'p [MeV/fm$^3$]')
	plt.savefig('./Huang_2026/Figure_1.png')   

if __name__ == '__main__':
	main()