import constants
import data_io
import fit_data
import predict_data
import prepare_dataset

import argparse
import os.path
import sys

def run_pconsc(fold_k):
	print 'Preparing data...'
	data, target, folds = prepare_dataset.prepare_dataset()
	print 'Fitting random forest...'
	forest = fit_data.fit_data(fold_k, data, target, folds)
	data_io.save_random_forest(forest, constants.intermediate_path, 'pconsc_random_forest_' + str(k) + '.pkl.tar.gz')
	print 'Predicting test data...'
	predict_data.predict_data(fold_k, data, folds, forest)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Run PConsC')
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

	if args.fold and 0 <= args.fold < constants.number_of_folds:
		run_pconsc(args.fold)
	else:
		for k in range(constants.number_of_folds):
			run_pconsc(k)
