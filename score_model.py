# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 21:25:22 2018

@author: chunhui zhu
"""


import pandas as pd
import numpy as np

from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import roc_auc_score

import pickle


test_pkl=open("test.pickle","rb")
test=pickle.load(test_pkl)

#Use pickle to save the model: when opening the file next, it saves the time to reprocess the previous steps to train the regenerate the model
model_pkl = open("best_model.pickle", 'rb')
model = pickle.load(model_pkl )

pred=model.predict(test)

results=[]
for x in pred:
    results.append("{:.0f}".format(float(x)))
    
submission=pd.DataFrame({
    'PassengerId': test.index,
    'Survived':results
})
    
submission.to_csv('submission.csv', index=False)
#submission=pd.read_csv('submission.csv')
#submission.head()

#image = misc.imread("score.png")
#print (image.shape)