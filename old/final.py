print 'Importing Required Modules...'


import csv as csv
import urllib
import os
import json
import time
import random
import numpy as np
from sklearn.ensemble.weight_boosting import AdaBoostClassifier
from sklearn.ensemble.forest import RandomForestClassifier, ExtraTreesClassifier
from sklearn.cross_validation import cross_val_score
import glob
from sklearn import tree
import numpy as np
from collections import Counter
import pylab as pl
from sklearn import svm, datasets
from sklearn.utils import shuffle
from sklearn.metrics import roc_curve, auc
print 'Module Imports Complete.'


""" WE HAVE ALREADY SCRAPED AND CLEANED THE DATA
# Scrape stock price information from Yahoo Finance

symbols = ['BTH','ZUMZ','NFLX','GTIV','BBY']
# The above tickers represent the five most volatile stocks of 2013

for symbol in symbols:
    time.sleep(.1+random.random())

    try:
        url = 'http://ichart.finance.yahoo.com/table.csv?s=%s&a=00&b=1&c=2013&d=11&e=31&f=2013&g=d&ignore=.csv' % symbol
        print url
        data = urllib.urlopen(url).read()
        file = '%s_data.csv' % (symbol)
        f = open(file,'w')
        f.write('%s' % str(data))
        f.close()
        print 'File Written as %s' % file
        data = data.split('\n')

    except:
        print 'Failed for %s' % symbol

#This points to our most volatile stock price data file
file = 'BTH_data.csv'
"""

# Set file, threshold and cross-validation folds
features = 'features.csv'
classes = 'classes.csv'
threshold = float(14)
cv = 10

"""
# Load the file into memory. 
def loadData(file):
    file = open(file).read()
    return file
"""



# Build input data for the classifier
def organizeData(data1,data2):
    data1 = data1.split('\n')
    data2 = data2.split('\n')
    X = []
    y = []
"""
# Import features as X

    for d in data1:
        tmp=[]
        d = d.split(',')
        tmp.append(d[0]) # PrevDayHoliday
        tmp.append(d[1]) # NextDayHoliday
        tmp.append(d[2]) # PrevDayVol
        tmp.append(d[3]) # MaxTemp
        tmp.append(d[4]) # MinTemp
        tmp.append(d[5]) # MaxHumid
        tmp.append(d[6]) # MinHumid
        tmp.append(d[7]) # MaxWind
        tmp.append(d[8]) # Precip
        X.append(tmp)
        # print tmp
 
# Import classes as Y vector

    for d in data2:
        tmp=[]
        d = d.split(',')
        tmp.append(d[0]) # Trading Volume low/med/high
        y.append(tmp)

    return np.array(X),np.array(y)
"""
def classify(X,y,cv):
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X,y)

    score = cross_val_score(clf, X, y, cv=cv)
    print '%s-fold cross validation accuracy: %s' % (cv,sum(score)/score.shape[0])
    
    preds = clf.predict(X)
    return clf

"""
    # The below measures are from Rob's GitHub code
    print 'Predictions Counter'
    print Counter(clf.predict(X))
    fp=0
    tp=0
    fn=0
    tn=0
    for a in range(len(y)):
        if y[a]==preds[a]:
            if preds[a]==0:
                tn+=1
            elif preds[a]==1:
                tp+=1
        elif preds[a]==1:fp+=1
        elif preds[a]==0:fn+=1
    
    print 'True Positives:', tp
    print 'True Negatives:', tn
    print 'False Positives:', fp
    print 'False Negatives:', fn
    print 'Precision:',float(tp)/(tp+fp)
    print 'Recall (tp)/(tp+fn):',float(tp)/(tp+fn)
    print 'False Positive Rate (fp)/(fp+tn):', float(fp)/(fp+tn)
    print 'False Positive Rate2 (fp)/(fp+tp):', float(fp)/(fp+tp)
    print 'Prediction Accuracy: %s%s' % (100*float(tp+tn)/(tp+tn+fp+fn),'%') 
    return clf
"""

# Running the above components

# import CSVs as numpy arrays

classes = []
features = []

print 'Loading Data...'

with open('classes.csv','rU') as csv_file_object:
    reader = csv.reader(csv_file_object)
    for row in reader:
        classes.append(row)

classes = np.array(classes)
print classes

with open('features.csv','rU') as csv_file_object:
    reader = csv.reader(csv_file_object)
    for row in reader:
        features.append(row)

features = np.array(features)
print features

print 'Loading Data Complete.'

"""
print 'Organizing Data for Training'
X,y = organizeData(data1, data2)
print 'Data Organization Complete.'
"""

X = features
y = classes

print 'Training Classifier...'

clf=classify(features,classes,cv)
print clf.predict([0,0,1,38,31,85,22,15,0.08])

print 'Training Complete.'


# Evaluate Classifier Using ROC

fpr, tpr, thresholds = roc_curve(y, clf.predict(X))
roc_auc = auc(fpr, tpr)
print 'Area under the ROC curve: %s' % roc_auc

