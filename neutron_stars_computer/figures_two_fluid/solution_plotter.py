import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

Array = np.ndarray

def plot_solution(x: str, y: str, input_folder: str, output_folder: str, labels: list[str], linestyles: list[str], colors: list[str], 
	xlim: tuple,  ylim: tuple, linewidth: float, xlabel: str, ylabel: str, fontsize: str) -> None:
	fig, ax = plt.subplots()

	folder_path = Path(input_folder)

	for f, label, linestyle, color in zip(folder_path.iterdir(), labels, linestyles, colors):
		pd.read_csv(input_folder + f.name).plot(x, y, xlim=xlim, ylim=ylim, ax=ax, 
			label=label, linestyle=linestyle, color=color, linewidth=linewidth)


	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	#plt.legend(fontsize)

	plt.savefig(output_folder)   
