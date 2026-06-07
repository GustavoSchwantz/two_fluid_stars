from neutron_stars_computer.equationsofstate.eos import EquationOfState

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

Array = np.ndarray

def plot_eos(EOSs: list[EquationOfState], labels: list[str], linestyles: list[str], colors: list[str],
	pressures: Array, xlim: tuple,  ylim: tuple, linewidth: float, path: str) -> None:

	fig, ax = plt.subplots()

	for eos, label, linestyle, color in zip(EOSs, labels, linestyles, colors):
		densities = np.array([eos.energy_density_from(p*1000)/1000 for p in pressures])

		pd.DataFrame({'p': pressures, 'e': densities}).plot('e', 'p', loglog=True, xlim=xlim, ylim=ylim, ax=ax, 
			label=label, linestyle=linestyle, color=color, linewidth=linewidth)


	plt.xlabel(r'$\epsilon$ [GeV/fm$^3$]')
	plt.ylabel(r'p [GeV/fm$^3$]')

	ax.tick_params(axis='both', which='both', top=True, bottom=True, left=True, right=True)

	plt.savefig(path)   
