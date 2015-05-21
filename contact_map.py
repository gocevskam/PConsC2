import constants
import data_io

import numpy as np
import matplotlib.colors as colors
import matplotlib.pyplot as plt

import sys

def plot(contacts, predictions=None, output_prefix=None):
	L = len(contacts)

	contact_map = np.zeros_like(contacts) + np.logical_and(0 < contacts, contacts <= 8)
	if predictions:
		for (i, j) in predictions:
			 if 0 < contacts[i-1, j-1] <= 8:
			 	contact_map[i-1, j-1] = 2
			 	contact_map[j-1, i-1] = 2
			 else:
			 	contact_map[i-1, j-1] = 3
			 	contact_map[j-1, i-1] = 3

	plt.figure(figsize=(7.5, 6))
	X, Y = np.meshgrid(np.arange(L+1)+0.5, np.arange(L+1)+0.5)
	plt.pcolor(X, Y, np.ma.array(contacts, mask=~np.tri(L, k=0, dtype='bool')), vmin=0, vmax=32)
	plt.colorbar()
	plt.pcolor(X, Y, np.ma.array(contact_map, mask=np.tri(L, k=0, dtype='bool')), cmap=colors.ListedColormap(['1.0', '0.2', 'g', 'r']), vmin=0, vmax=3)
	plt.xlim(0.5, L + 0.5)
	plt.ylim(0.5, L + 0.5)
	plt.xlabel('Residue number')
	plt.ylabel('Residue number')

	if output_prefix:
		plt.savefig(output_prefix + '.png')

	if not output_prefix:
		plt.show()

def plot_file(sequence_name, prediction_method=None, prediction_fraction=1.0, output_prefix=None):
	sequence = data_io.read_sequence(constants.data_path, sequence_name)
	L = len(sequence)
	contacts = data_io.read_contacts_matrix(constants.data_path, sequence_name, L)
	predictions = None

	if prediction_method:
		predictions, prediction_scores = data_io.read_predicted_contacts(constants.results_path, prediction_method, sequence_name, L, constants.min_separation)
		predictions = predictions[:int(prediction_fraction * L)]

	plot(contacts, predictions, output_prefix)

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Not enough arguments. Enter the path the sequence name."
	else:
		sequence_name = sys.argv[1]
		output_prefix = sys.argv[2] if len(sys.argv) > 2 else None

		prediction_method = sys.argv[3] if len(sys.argv) > 3 else None
		prediction_fraction = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
		
		plot_file(sequence_name, prediction_method, prediction_fraction, output_prefix)
