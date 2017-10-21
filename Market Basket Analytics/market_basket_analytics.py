# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 18:55:52 2017

@author: Gaurav
"""
import requests
import operator
from collections import Counter

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
    #company products
    CompanyProducts = set({'P01', 'P02', 'P03','P04', 'P04', 'P05', 'P06', 'P07', 'P08', 'P09', 'P10'})
    testData = [ln.strip('\n').split(',') for ln in open('market_basket_test.txt', "r")]
    trainingData = [line.strip('\n').split(',') for line in open('market_basket_training.txt', 'r')]
    with open("market_basket_recommendations.txt", "w") as txt:
        for testItem in testData:
            #copy item for final file printing
            tempTestData = testItem.copy()
            #if tempTestData[0] == '068' or tempTestData[0] == '070':
            testItem.remove(testItem[0])
            frequency_conuter = 0
            loop_counter = 0
            dict_frequency_conuter = {}
            #remove existing items from set
            setComapare = CompanyProducts - set(testItem)
            length_setComapare = len(list(setComapare))
            #iterate through loop till all product values are compared
            while length_setComapare > loop_counter:
                setCompareLoop = list(setComapare)[loop_counter]
                if loop_counter != 0:
                    testItem.pop()
                loop_counter = loop_counter + 1
                testItem.append(setCompareLoop)
                setCompareValue = set(testItem)
                #get frequency count of item
                counter_result = Counter(((item[1])) for item in trainingData if set(item[1:len(item)]) == setCompareValue)
                if len(list(counter_result)) > 0:
                    frequency_conuter = counter_result[list(counter_result)[0]]
                else:
                    frequency_conuter = 0
                dict_frequency_conuter[setCompareLoop] = frequency_conuter
            # sort dictionary based on counter value in descending order
            dict_frequency_conut = sorted(dict_frequency_conuter.items(), key = operator.itemgetter(1), reverse = True) 
            # if all element are zero then remove item from list and then check for product match
            if dict_frequency_conut[0][1] == 0:
                testItem.pop()
                dict_frequency_conut = getbasketItem(testItem, CompanyProducts,trainingData, False)
            print(str(tempTestData[0]) + ',' + str(dict_frequency_conut[0][0]), file=txt)    

def getbasketItem(testItem, CompanyProducts,trainingData, recurssive):
    testItemLen = len(testItem)
    loopItr = 0
    dict_frequency_conuter = {}
    # iterate with different combination of element within set
    while loopItr < testItemLen:
        testItemCopy = testItem.copy()
        if recurssive:
            # during recurssive process remove 2 elements and compare
            if loopItr == 0:
                testItemCopy.remove(testItemCopy[0])
                testItemCopy.remove(testItemCopy[1])
            elif loopItr == 1:
                testItemCopy.remove(testItemCopy[1])
                testItemCopy.remove(testItemCopy[1])
            elif loopItr == 2:
                testItemCopy.remove(testItemCopy[0])
                testItemCopy.remove(testItemCopy[0])
        else:
            testItemCopy.remove(testItemCopy[loopItr])
        loopItr = loopItr + 1
        frequency_conuter = 0
        loop_counter = 0
        # remove existing element from company set to get unique element for comparison 
        setComapare = CompanyProducts - set(testItemCopy)
        length_setComapare = len(list(setComapare))
        #iterate through loop till all product values are compared
        while length_setComapare > loop_counter:
            setCompareLoop = list(setComapare)[loop_counter]
            if loop_counter != 0:
                testItemCopy.pop()
            loop_counter = loop_counter + 1
            testItemCopy.append(setCompareLoop)
            setCompareValue = set(testItemCopy)
            #get frequency count of item
            counter_result = Counter(((item[1])) for item in trainingData if set(item[1:len(item)]) == setCompareValue)
            if len(list(counter_result)) > 0:
                frequency_conuter = counter_result[list(counter_result)[0]]
            else:
                frequency_conuter = 0
            #check if element exist in dictionary or not and then update value accordingly
            if dict_frequency_conuter.get(setCompareLoop, "NA") == "NA":
                dict_frequency_conuter[setCompareLoop] = int(frequency_conuter)
            #update value only if existing value is smaller
            elif dict_frequency_conuter.get(setCompareLoop) < int(frequency_conuter):
                dict_frequency_conuter[setCompareLoop] = int(frequency_conuter)
        # sort dictionary based on counter value in descending order
    dict_frequency_conut = sorted(dict_frequency_conuter.items(), key = operator.itemgetter(1), reverse = True)
    # if frquency counter is still zero then give recurssive call wich will further remove one more item and then compare 
    if dict_frequency_conut[0][1] == 0:
        dict_frequency_conut = getbasketItem(testItemCopy, CompanyProducts,trainingData, True)
    return dict_frequency_conut
      
#used to invoke functions in sequence
def executeFunctions():
    #downloadTrainingTestDataset()
    suggestNewProduct()

#execute functions   
executeFunctions()