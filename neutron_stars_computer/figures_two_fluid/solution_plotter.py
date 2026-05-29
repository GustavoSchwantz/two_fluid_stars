import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

Array = np.ndarray



def plot_solution(x: str, y: str, input_folder: str, output_folder: str, labels: list[str], kind: str, colors: list[str], 
	xlim: tuple,  ylim: tuple, markers: list[str], xlabel: str, ylabel: str, fontsize: str, loc: str) -> None:

	print('Creating a figure...')

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
				label=label, linestyle=marker, color=color, kind=kind)
    
	
	#ax.xaxis.set_major_locator(ticker.MultipleLocator(2e11))
	#ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.legend(fontsize=fontsize, loc=loc)

	plt.savefig(output_folder)   

	print('Figure created!')
