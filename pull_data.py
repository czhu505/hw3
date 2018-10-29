# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 18:55:36 2018

@author: chunhui zhu
"""

import pandas as pd
import numpy as np

import pickle
from kaggle.api.kaggle_api_extended import KaggleApi

download_path = "C:\\Users\\czhu5\\Desktop\\Data-622-2-ML\\HW2"

api = KaggleApi()

api.authenticate()

#download the kaggle data set to local folder
api.competition_download_files('titanic', path=download_path)

test=pd.read_csv('test.csv')
train=pd.read_csv('train.csv')


#data clearning
#To combine two data set for filling missing data for both train and test
#first pop survived column from train then combine both
train1=train
train_s=train1.pop('Survived')

full_data=pd.concat([train1,test], axis=0)
full_data=full_data.set_index(['PassengerId'])

full_data['Title']=full_data['Name'].apply(lambda name: name.split(',')[1].split('.')[0].strip())


# normalize the titles
normalized_titles = {
    "Capt":       "Officer",
    "Col":        "Officer",
    "Major":      "Officer",
    "Jonkheer":   "Royalty",
    "Don":        "Royalty",
    "Sir" :       "Royalty",
    "Dr":         "Officer",
    "Rev":        "Officer",
    "the Countess":"Royalty",
    "Dona":       "Royalty",
    "Mme":        "Mrs",
    "Mlle":       "Miss",
    "Ms":         "Mrs",
    "Mr" :        "Mr",
    "Mrs" :       "Mrs",
    "Miss" :      "Miss",
    "Master" :    "Master",
    "Lady" :      "Royalty"
}

# map the normalized titles to the current titles 
full_data.Title = full_data.Title.map(normalized_titles)

grouped = full_data.groupby(['Sex','Pclass', 'Title'])  

full_data.Age = grouped.Age.apply(lambda x: x.fillna(x.median()))

full_data['SexCode'] = full_data.Sex.map({"male": 0, "female":1})

full_data['TicketCode']=full_data['Ticket'].apply(lambda tick: tick[0])

full_data['TicketCode'].value_counts()

full_data.TicketCode = full_data.TicketCode.map({"3": 3, "2":2, "1":1, "4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"S":101,"P":102,"C":103,"A":104,"W":105,"F":106,"L":107})

grouped = full_data.groupby(['TicketCode'])  


#filled the missing non using median with ticket starts number 3
#though it might not make sences, it won't be effect the result much since only 1 value missing
full_data['Fare']=full_data['Fare'].fillna(7.89580)

#get the first letter from string, and palce none if the value is missing
def clean_cabin(x):
    try:
        return x[0]
    except TypeError:
        return "None"
full_data['CabinCode']=full_data.Cabin.apply(clean_cabin)

#conver CabinCode into numeric number
full_data.CabinCode = full_data.CabinCode.map({"None": 0, "C":100, "B":101, "D":102,"E":103,"A":104,"F":105, "G":106, "T":107})

grouped=full_data[full_data['CabinCode']==101] 

#From the last result, these two missing value in Embarked either C or S, I randomly pick S.
full_data.Embarked=full_data['Embarked'].fillna('S')

#conver CabinCode into numeric number
full_data['EmbarkedCode'] = full_data.Embarked.map({"S": 0, "C":1, "Q":2 })

df=full_data._get_numeric_data()

trainSet=df.iloc[0:891,]
testSet=df.iloc[891:,]

#combine the survied column back to train data
train2=trainSet.assign(Survived=train_s.values)

df2=df
df2.Age=np.where(df2['Age'].between(0,17), 0, df2['Age'])
df2.Age=np.where(df2['Age'].between(17,32), 1, df2['Age'])
df2.Age=np.where(df2['Age'].between(32,41), 2, df2['Age'])
df2.Age=np.where(df2['Age'].between(41,100), 3, df2['Age'])

df2.Fare=np.where(df2['Fare'].between(0,17), 0, df2['Fare'])
df2.Fare=np.where(df2['Fare'].between(17,28), 1, df2['Fare'])
df2.Fare=np.where(df2['Fare'].between(28,1000), 2, df2['Fare'])

trainSet2=df2.iloc[0:891,]
testSet2=df2.iloc[891:,]

#use pickle to save the new train and test dataset
x_pkl=open("x.pickle","wb")
pickle.dump(trainSet2,x_pkl)
x_pkl.close()

y_pkl=open("y.pickle","wb")
pickle.dump(train_s,y_pkl)
y_pkl.close()

test_pkl=open("test.pickle","wb")
pickle.dump(testSet2,test_pkl)
test_pkl.close()


