# -*- coding: utf-8 -*-
"""Multi linear perspectron model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MaPzpMCeor8ufEa15HIPB-eM9Ffabvr0
"""

from google.colab import files
files.upload()

import pandas as pd
import numpy as np
dataset = pd.read_csv('data set 12345678.csv')

from sklearn.model_selection import train_test_split

list(dataset.columns.values)

X = dataset[['Blast Furnace Slag (%)',
 'Fly Ash (%)',
 'Superplasticizer (%)',
 'w/c ratio ',
 '% of coarse aggregate',
 '% of fine aggregate ', 'Concrete compressive strength(MPa, megapascals) ' ]]
y = dataset[['Coarse Aggregate  (kg in a m^3 mixture)',
 'Fine Aggregate (kg in a m^3 mixture)',
 'Water  (kg in a m^3 mixture)',
 'Cement (kg in a m^3 mixture)']]

X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2)

import matplotlib.pyplot as plt   #Data visualisation libraries

dataset.corr()

from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# define base model
def baseline_model():
	# create model
	model = Sequential()
	model.add(Dense(7, input_dim=7, kernel_initializer='normal', activation='relu'))
	model.add(Dense(4, kernel_initializer='normal'))
	# Compile model
	model.compile(loss='mean_absolute_error', optimizer='adam')
	return model

# fix random seed for reproducibility
seed = 7
np.random.seed(seed)
# evaluate model with standardized dataset
estimator = KerasRegressor(build_fn=baseline_model, epochs=3000, batch_size=8474, verbose=0)

kfold = KFold(n_splits=10, random_state=seed)
results = cross_val_score(estimator, X, y, cv=kfold)
print("Results: %.2f (%.2f) MSE" % (results.mean(), results.std()))

# example of training a final regression model
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
# generate regression dataset
X, y = make_regression(n_samples=100, n_features=2, noise=0.1)
# fit final model
model = LinearRegression()
model.fit(X, y)
# new instances where we do not know the answer
Xnew, _ = make_regression(n_samples=3, n_features=2, noise=0.1, random_state=1)
# make a prediction
ynew = model.predict(Xnew)
# show the inputs and predicted outputs
for i in range(len(Xnew)):
	print("X=%s, Predicted=%s" % (Xnew[i], ynew[i]))

