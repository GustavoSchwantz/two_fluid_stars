import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.lines import Line2D

Array = np.ndarray



def plot_solution(x: str, y: str, input_folder: str, output_folder: str, labels: list[str], kind: str, colors: list[str], 
	xlim: tuple,  ylim: tuple, markers: list[str], xlabel: str, ylabel: str, fontsize: str, loc: str) -> None:

	fig, ax = plt.subplots()

	csv_files = glob.glob(os.path.join(input_folder, '*.csv'))

	csv_files.sort(key=os.path.getctime)

	if kind == 'scatter':

	    for csv_file, label, color, marker in zip(csv_files, labels, colors, markers):
		    pd.read_csv(csv_file).plot(x, y, xlim=xlim, ylim=ylim, ax=ax, 
			    label=label, marker=marker, color=color, kind=kind)

	else:

		for csv_file, label, color, marker in zip(csv_files, labels, colors, markers):
			pd.read_csv(csv_file).plot(x, y, xlim=xlim, ylim=ylim, ax=ax,
				label=label, linestyle=marker, color=color, kind=kind, linewidth=3, logy=False)
    
	
	#ax.xaxis.set_major_locator(ticker.MultipleLocator(2e11))
	#ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

	legend_elements = [
    	Line2D([0], [0], color='green', lw=9, label=r'DM central density = 1 x 10$^5$ MeV/fm$^3$', linestyle=':'),
    	Line2D([0], [0], color='red', lw=9, label=r'DM central density = 1 x 10$^6$ MeV/fm$^3$', linestyle=':'),
    	Line2D([0], [0], color='blue', lw=9, label=r'DM central density = 2 x 10$^6$ MeV/fm$^3$', linestyle=':')
    ]

	legend1 = ax.legend(handles=legend_elements, fontsize=fontsize)

	ax.add_artist(legend1)

	legend_elements = [
    	Line2D([0], [0], color='black', lw=3, label='CFL', linestyle=':'),
    	Line2D([0], [0], color='black', lw=2, label='pQCD', linestyle='--')
    ]

	ax.legend(handles=legend_elements, loc='upper right')

	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	#plt.legend(fontsize=fontsize, loc=loc)

	plt.savefig(output_folder)   
