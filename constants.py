data_path = 'data/'
intermediate_path = 'intermediate/'
results_path = 'results/'

number_of_cores = -1

alignments = [a + '_' + str(e) for a in ('hhblits', 'jackhmmer') for e in (1, -4, -10, -40)]
methods = ['psicov', 'plmdca']
combined_methods = [a + '_' + m for a in alignments for m in methods]

amino_acids = 'ARNDCEQGHILKMFPSTWYV'
background_frequencies = [0.0825, 0.0553, 0.0406, 0.0545, 0.0137, 0.0393, 0.0675, 0.0707, 0.0227, 0.0595, 0.0966, 0.0584, 0.0242, 0.0386, 0.0470, 0.0657, 0.0534, 0.0108, 0.0292, 0.0687]
secondary_structures = 'CEH'

number_of_folds = 5

min_separation = 5
extra_features = True
extra_features_window = 4
extra_same_ss_features = True

receptive_field = 5
number_of_layers = 5
