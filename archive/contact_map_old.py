import data_io

import numpy as np
import matplotlib.colors as colors
import matplotlib.pyplot as plt

import sys

def plot(contacts, predictions=None, output_prefix=None):
	L = len(contacts)

	plt.figure(figsize=(7.5, 6))
	X, Y = np.meshgrid(np.arange(L+1)+0.5, np.arange(L+1)+0.5)
	plt.pcolor(X, Y, contacts, vmin=0, vmax=32)
	plt.xlim(0.5, L + 0.5)
	plt.ylim(0.5, L + 0.5)
	plt.colorbar()

	if output_prefix:
		plt.savefig(output_prefix + "_dist.png")

	plt.figure(figsize=(6, 6))
	plt.pcolor(X, Y, np.logical_and(0 < contacts, contacts <= 8), cmap=colors.ListedColormap(['1.0', '0.2']))
	plt.xlim(0.5, L + 0.5)
	plt.ylim(0.5, L + 0.5)

	if predictions:
		good_predictions = np.array([(i, j) for (i, j) in predictions if 0 < contacts[i-1, j-1] <= 8])
		bad_predictions = np.array([(i, j) for (i, j) in predictions if contacts[i-1, j-1] > 8])
		plt.scatter(good_predictions[:,0], good_predictions[:,1], c='g', marker='o', lw=0)
		plt.scatter(good_predictions[:,1], good_predictions[:,0], c='g', marker='o', lw=0)
		plt.scatter(bad_predictions[:,0], bad_predictions[:,1], c='r', marker='x')
		plt.scatter(bad_predictions[:,1], bad_predictions[:,0], c='r', marker='x')

	if output_prefix:
		plt.savefig(output_prefix + ".png")

	if not output_prefix:
		plt.show()

def plot_file(data_path, sequence_name, prediction_method=None, prediction_fraction=1.0, output_prefix=None):
	sequence = data_io.read_sequence(data_path, sequence_name)
	L = len(sequence)
	contacts = data_io.read_contacts_matrix(data_path, sequence_name, L)
	predictions = None

	if prediction_method:
		predictions, prediction_scores = data_io.read_predicted_contacts(data_path, sequence_name, L, prediction_method, 5)
		predictions = predictions[:int(prediction_fraction * L)]

	plot(contacts, predictions, output_prefix)

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "Not enough arguments. Enter the path to the protein data and the sequence name."
	else:
		data_path = sys.argv[1]
		sequence_name = sys.argv[2]
		output_prefix = sys.argv[3] if len(sys.argv) > 3 else None

		prediction_method = sys.argv[4] if len(sys.argv) > 4 else None
		prediction_fraction = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0
		
		plot_file(data_path, sequence_name, prediction_method, prediction_fraction, output_prefix)
