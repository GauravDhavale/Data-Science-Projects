# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 18:55:52 2017

@author: Gaurav
"""
import requests
import pandas as pd
trainingData = []
testData = []

# url for training data set
url_training_data = 'http://kevincrook.com/utd/market_basket_training.txt'
url_test_data = 'http://kevincrook.com/utd/market_basket_test.txt'

#This function is used to access the dataset URL, fetch the data and load it into the text file
def downloadTrainingTestDataset():
    r = requests.get(url_training_data)
    p = requests.get(url_test_data)
    tf1 = open('market_basket_training.txt', "wb")
    tf2 = open('market_basket_test.txt', "wb")
    tf1.write(r.content) # write content to market_basket_training.txt file
    tf1.close()
    tf2.write(p.content) # write content to market_basket_test.txt file
    tf2.close()
    
 
def readDataset():
    global trainingData
    global testData
    testData = [ln.strip() for ln in open('market_basket_test.txt', "r")]
    trainingData = [line.strip() for line in open('market_basket_training.txt', 'r')]
    trainingDataSeries = pd.Series(item.split(',') for item in trainingData)
    testDataSeries = pd.Series(item.split(',') for item in testData)
    for item in testDataSeries:
        testitem = [item1[1:len(item1)] for item1 in trainingDataSeries if item in (item1[1:len(item1)])]
        print(testitem)
        break
        #if(item[1:len(item)]) in (item1[1:len(item1)] for item1 in trainingDataSeries):
        #data.iloc[0:3] in 
    
    
#used to invoke functions in sequence
def executeFunctions():
    downloadTrainingTestDataset()
    #readDataset()
    
executeFunctions()
