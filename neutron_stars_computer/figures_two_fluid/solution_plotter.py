import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

Array = np.ndarray

def plot_solution(x: str, y: str, input_folder: str, output_folder: str, labels: list[str], linestyles: list[str], colors: list[str], 
	xlim: tuple,  ylim: tuple, linewidth: float, xlabel: str, ylabel: str, fontsize: str) -> None:
	print('Creating a figure...')

	fig, ax = plt.subplots()

	folder_path = Path(input_folder)

	for f, label, linestyle, color in zip(folder_path.iterdir(), labels, linestyles, colors):
		#print(f.name)
		#print(color)
		pd.read_csv(input_folder + f.name).plot(x, y, xlim=xlim, ylim=ylim, ax=ax, 
			label=label, linestyle=linestyle, color=color, linewidth=linewidth)
        
    
	ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
	ax.yaxis.set_major_locator(ticker.MultipleLocator(0.2))

	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	#plt.legend(fontsize)

	plt.savefig(output_folder)   

	print('Figure created!')
