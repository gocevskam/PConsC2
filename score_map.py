import constants
import data_io

import numpy as np
import matplotlib.colors as colors
import matplotlib.pyplot as plt

import sys

def plot(scores_a, scores_b, output_prefix):
	L = len(scores_a)

	merged = np.zeros((L, L))
	merged[np.tril_indices(L, k=constants.min_separation)] = scores_a[np.tril_indices(L, k=constants.min_separation)]
	merged[np.triu_indices(L, k=-constants.min_separation)] = scores_b[np.triu_indices(L, k=-constants.min_separation)]

	plt.figure(figsize=(6, 6))
	X, Y = np.meshgrid(np.arange(L+1)+0.5, np.arange(L+1)+0.5)
	plt.pcolor(X, Y, merged, cmap='Blues', vmin=0, vmax=1)
	plt.xlim(0.5, L + 0.5)
	plt.ylim(0.5, L + 0.5)
	plt.xlabel('Residue number')
	plt.ylabel('Residue number')

	if output_prefix:
		plt.savefig(output_prefix + '_scores.png')

	if not output_prefix:
		plt.show()

def plot_file(sequence_name, method_a, method_b, output_prefix=None):
	sequence = data_io.read_sequence(constants.data_path, sequence_name)
	L = len(sequence)

	predictions_a, scores_a = data_io.read_predicted_contacts(constants.results_path, method_a, sequence_name, L, constants.min_separation)
	predictions_b, scores_b = data_io.read_predicted_contacts(constants.results_path, method_b, sequence_name, L, constants.min_separation)

	plot(scores_a, scores_b, output_prefix)

if __name__ == "__main__":
	if len(sys.argv) < 4:
		print "Not enough arguments. Enter the sequence name and the two methods."
	else:
		sequence_name = sys.argv[1]
		method_a = sys.argv[2]
		method_b = sys.argv[3]
		output_prefix = sys.argv[4] if len(sys.argv) > 4 else None
		
		plot_file(sequence_name, method_a, method_b, output_prefix)
