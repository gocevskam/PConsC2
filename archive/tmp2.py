import numpy as np

from sklearn.externals import joblib

data = np.load('dataset_data.npy')
target = np.load('dataset_target.npy')
folds = np.load('dataset_folds.npy')

forest = joblib.load('forests/random_forest_0.pkl')
indices = np.load('forests/random_forest_0.pkl_05.npy')

print np.all(forest.estimators_[0].indices_ == indices)
print indices
a = forest.estimators_[0].predict(data[folds != 0])
print a
forest.estimators_[0].indices_ = np.array([])
b = forest.estimators_[0].predict(data[folds != 0])
print b
print np.all(a == b)

