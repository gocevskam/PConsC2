import os
import shutil

old_data_path = 'old_data/'
contacts_path = 'native_contacts/'
data_path = 'data/'

alignment_extensions = ['blits' + str(i) + '.' for i in range(2, 6)] + [''] + ['jackhmmer' + str(i) + '.' for i in range(4, 7)]
alignment_names = [a + '_' + str(e) for a in ('hhblits', 'jackhmmer') for e in (1, -4, -10, -40)]

method_extensions = ['psicov2', 'plmdca2']
method_names = ['psicov', 'plmdca']

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
	if contacts_path and os.path.exists(contacts_path):
		shutil.copy(contacts_path + sequence_name + '_contacts.CB', data_path + 'contacts/' + sequence_name + '.CB')
	else:
		shutil.copy(old_data_path + sequence_name + '/contacts.CB', data_path + 'contacts/' + sequence_name + '.CB')

for ae, an in zip(alignment_extensions, alignment_names):
	for me, mn in zip(method_extensions, method_names):
		subdir = an + '_' + mn + '/'
		create_dir(data_path + subdir)
		for sequence_name in sequence_names:
			shutil.copy(old_data_path + sequence_name + '/sequence.fa.' + ae + me, data_path + subdir + sequence_name + '.pred')
