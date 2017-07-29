# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 18:55:52 2017

@author: Gaurav
"""
import requests
import pandas as pd


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
    

#This function will iterate through cart and previous transaction and will suggest the new product
def suggestNewProduct():
    trainingData = []
    testData = []
    testData = [ln.strip() for ln in open('market_basket_test.txt', "r")]
    trainingData = [line.strip() for line in open('market_basket_training.txt', 'r')]
    #convert into series of list using pandas
    trainingDataSeries = pd.Series(item.split(',') for item in trainingData)
    testDataSeries = pd.Series(item.split(',') for item in testData)
    with open("market_basket_recommendations.txt", "w") as txt:
        for item in testDataSeries:
            tempTrainData = []
            #print(item[1:len(item)], file=txt)
            #iterate through training data set for every item in the cart
            for item1 in trainingDataSeries:
                if (set(item[1:len(item)]).issubset(set(item1[1:len(item1)]))):
                    tempTrainData.append(item1) 
            if len(tempTrainData)> 0:
                #print(tempTrainData[0], file=txt)
                #sort the list based on length of list and then transaction no in descending order
                tempTrainData.sort(key=lambda k: (-len(k), -int(k[0])))
                # get the difference of sets to find suggesting prodcut item only
                tempList = set(tempTrainData[0][1:len(tempTrainData[0])]) - set(item[1:len(item)])
                for setItem in tempList:
                    print(item[0] + ',' + setItem, file=txt)
                    break
            else:
                # case when item in the cart doesn't find any match in the training dataset
                print(item[0], file=txt)
    
    
#used to invoke functions in sequence
def executeFunctions():
    downloadTrainingTestDataset()
    suggestNewProduct()
    
executeFunctions()
