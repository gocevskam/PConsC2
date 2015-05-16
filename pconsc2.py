import constants
import data_io
import fit_data
import predict_data
import prepare_dataset
import next_layer_dataset

import argparse
import os.path
import sys

def run_pconsc2(fold):
	k = fold - 1
	print 'Preparing data...'
	base_data, target, folds = prepare_dataset.prepare_dataset()
	for i in range(constants.number_of_layers + 1):
		if i == 0:
			data = base_data
		else: 
			print 'Getting layer ' + str(i) + ' data...'
			data = next_layer_dataset.next_layer_dataset(base_data, data, forest)

		print 'Fitting random forest...'
		forest = fit_data.fit_data(k, data, target, folds)
		data_io.save_random_forest(forest, constants.intermediate_path, 'pconsc2_random_forest_' + str(k) + '_layer_' + str(i) + '.pkl.tar.gz')
		print 'Predicting test data...'
		predict_data.predict_data(k, data, folds, forest, 'pconsc2_layer_' + str(i) + '/')


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Run PConsC2')
	parser.add_argument('-d', '--data')
	parser.add_argument('-i', '--intermediate')
	parser.add_argument('-r', '--results')
	parser.add_argument('-c', '--cores', type=int)
	parser.add_argument('-f', '--fold', type=int)
	args = parser.parse_args()

	if args.data:
		constants.data_path = args.data
	if args.intermediate:
		constants.intermediate_path = args.intermediate
	if args.results:
		constants.results_path = args.results
	if args.cores:
		constants.number_of_cores = args.cores

	if args.fold and 1 <= args.fold <= constants.number_of_folds:
		run_pconsc2(args.fold)
	else:
		for fold in range(1, constants.number_of_folds + 1):
			run_pconsc2(fold)

