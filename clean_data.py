from constants import *

import os
import shutil

old_data_path = 'old_data/'
data_path = 'data/'

old_alignments = ['blits' + str(i) + '.' for i in range(2, 6)] + [''] + ['jackhmmer' + str(i) + '.' for i in range(4, 7)]
old_methods = ['psicov2', 'plmdca2']

def create_dir(path):
	if not os.path.exists(path):
		os.makedirs(path)

create_dir(data_path)
with open(data_path + 'sequence_names', 'w') as f:
	sequence_names = sorted(sequence_name for sequence_name in os.listdir(old_data_path) if os.path.isdir(os.path.join(old_data_path, sequence_name)))
	f.write('\n'.join(sequence_names))

create_dir(data_path + 'sequences/')
for sequence_name in sequence_names:
	shutil.copy(old_data_path + sequence_name + '/sequence.fa', data_path + 'sequences/' + sequence_name + '.fa')

create_dir(data_path + 'contacts/')
for sequence_name in sequence_names:
	shutil.copy(old_data_path + sequence_name + '/contacts.CB', data_path + 'contacts/' + sequence_name + '.CB')

for ae, an in zip(old_alignments, alignments):
	for me, mn in zip(old_methods, methods):
		subdir = an + '_' + mn + '/'
		create_dir(data_path + subdir)
		for sequence_name in sequence_names:
			shutil.copy(old_data_path + sequence_name + '/sequence.fa.' + ae + me, data_path + subdir + sequence_name + '.pred')