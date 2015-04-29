import data_io

import matplotlib.pyplot as plt

import cPickle as pickle
import itertools

data_path = 'data/'
alignments = ['blits' + str(i) + '.' for i in range(2, 6)] + [''] + ['jackhmmer' + str(i) + '.' for i in range(4, 7)]
methods = ['psicov2', 'plmdca2']
method_names = ['PSICOV', 'plmDCA']
method_styles = ['k:', 'g--']

def average_ppv(method):
	top_predictions_fraction = 1.0

	sequence_names = data_io.read_sequence_names('sequence_names')
	ppv = []
	for sequence_name in sequence_names:
		L = len(data_io.read_sequence(data_path, sequence_name))
		contact_matrix = data_io.read_contacts_matrix(data_path, sequence_name, L)
		predictions, prediction_scores = data_io.read_predicted_contacts(data_path, sequence_name, L, method, 5)
		predictions = predictions[:int(top_predictions_fraction * L)]
		if len(predictions) > 0:
			ppv.append(sum(1 for (i, j) in predictions if 0 < contact_matrix[i-1,j-1] <= 8) / float(len(predictions)))
			print sequence_name, L, ppv[-1]
		else:
			print sequence_name, L, "No predictions"
	print 'Average PPV:', sum(ppv) / len(ppv)

def plot_ppv():
	max_predictions_fraction = 1.5

	def get_all_predictions():
		sequence_names = data_io.read_sequence_names('sequence_names')

		all_predictions = dict((method, []) for method in methods)

		for sequence_name in sequence_names:
			print sequence_name

			L = len(data_io.read_sequence(data_path, sequence_name))
			contact_matrix = data_io.read_contacts_matrix(data_path, sequence_name, L)

			for method in methods:
				for alignment in alignments:
					predictions, prediction_scores = data_io.read_predicted_contacts(data_path, sequence_name, L, alignment + method, 5)
					predictions = predictions[:int(max_predictions_fraction * L)]
					all_predictions[method].extend((100 * float(k) / L, 0 < contact_matrix[i-1,j-1] <= 8) for (k, (i, j)) in enumerate(predictions))

		return all_predictions

	def accumulate_predictions(predictions):
		ppv = {}

		for method in methods:
			predictions[method].sort()

			k = 0
			n = 0
			X = [0.0]
			Y = [0.0]
			for x, prediction_list in itertools.groupby(predictions[method], key=lambda x: x[0]):
				prediction_list = list(prediction_list)
				k += sum(1 for p in prediction_list if p[1])
				n += len(prediction_list)
				X.append(x)
				Y.append(float(k) / n)
			ppv[method] = (X, Y)

		return ppv

	def plot_ppv_curves(ppv):
		for (method, name, style) in zip(methods, method_names, method_styles):
			X, Y = ppv[method]
			plt.plot(X, Y, style, label=name)
		plt.legend()
		plt.show()

	try:
		predictions = pickle.load(open('evaluation_predictions.pickled', 'rb'))
	except:
		predictions = get_all_predictions()
		pickle.dump(predictions, open('evaluation_predictions.pickled', 'wb'))

	try:
		ppv = pickle.load(open('evaluation_ppv.pickled', 'rb'))
	except:
		ppv = accumulate_predictions(predictions)
		pickle.dump(ppv, open('evaluation_ppv.pickled', 'wb'))

	plot_ppv_curves(ppv)

if __name__ == "__main__":
	#average_ppv('blits2.psicov2')
	plot_ppv()
