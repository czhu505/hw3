# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 22:15:51 2018

@author: chunhui zhu
"""

import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import seaborn as sns

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


x_pkl=open("x.pickle","rb")
x=pickle.load(x_pkl)

y_pkl=open("y.pickle","rb")
y=pickle.load(y_pkl)

# cross validation
k_fold = KFold(n_splits=10, shuffle=True, random_state=0)

names = ["KNN", "Decision Tree", "Naive Bayes", "SVM"]
models = [
    KNeighborsClassifier(13),
    DecisionTreeClassifier(),
    GaussianNB(),
    SVC()]

model_scores = []

for name, clf in zip(names, models):
    clf.fit(x,y)
    scoring = 'accuracy'
    score = cross_val_score(clf, x, y, cv=k_fold, n_jobs=1, scoring=scoring)
    model_scores.append(round(np.mean(score),10))
  
names.append("GradientBoostingRegressor")
models.append(GradientBoostingRegressor())
regressor=models[-1]
regressor.fit(x,y)  
predicted=regressor.predict(x)
#0.9194521671513332
model_scores.append(round(roc_auc_score(y, predicted),10))

names.append("RandomForestRegressor")
models.append(RandomForestRegressor(n_estimators=1000, oob_score=True, n_jobs=-1, random_state=42, max_features="auto", min_samples_leaf = 8))
rfRegressor=models[-1]
rfRegressor.fit(x,y)
rfpredicted=rfRegressor.predict(x)
model_scores.append(round(roc_auc_score(y, rfpredicted),10))


scoredf=pd.DataFrame(list(zip(names,model_scores)),columns=['names','model_scores'])
scoredf.to_csv('score.csv', index=False)
#print(scoredf)
#                           0         1
#0                        KNN  0.756429
#1              Decision Tree  0.794532
#2                Naive Bayes  0.770961
#3                        SVM  0.795743
#4  GradientBoostingRegressor  0.919452
#5      RandomForestRegressor  0.913431

#Lookup the max score postion
position=model_scores.index(max(model_scores))


#use pickle to save best model
model_pkl=open("best_model.pickle","wb")
pickle.dump(models[position],model_pkl)
model_pkl.close()

#the final submition csv
#RandomForestRegressor has better outcome


