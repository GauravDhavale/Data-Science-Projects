# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 18:55:52 2017

@author: Gaurav
"""
import requests
import operator


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
    from collections import Counter
    with open("market_basket_recommendations.txt", "w") as txt:
        for testItem in testData:
            tempTestData = testItem.copy()
            testItem.remove(testItem[0])
            #print(testItem)
            frequency_conuter = 0
            loop_counter = 0
            dict_frequency_conuter = {}
            setComapare = CompanyProducts - set(testItem)
            length_setComapare = len(list(setComapare))
            #print('setComapare' + str(setComapare))
            #print(length_setComapare)
            #print(item[1:len(item)])
            #iterate through loop till all product values are compared
            while length_setComapare > loop_counter:
                setCompareLoop = list(setComapare)[loop_counter]
                if loop_counter != 0:
                    testItem.pop()
                loop_counter = loop_counter + 1
                #print(loop_counter)
                #print("setCompareLoop :-" + str(setCompareLoop))
                testItem.append(setCompareLoop)
                setCompareValue = set(testItem)
                #print(setCompareValue)
                #get frequency count of item
                counter_result = Counter(((item[1])) for item in trainingData if set(item[1:len(item)]) == setCompareValue)
                #print(counter_result)
                if len(list(counter_result)) > 0:
                    frequency_conuter = counter_result[list(counter_result)[0]]
                else:
                    frequency_conuter = 0
                #print(frequency_conuter)
                dict_frequency_conuter[setCompareLoop] = frequency_conuter
            # sort dictionary based on counter value in descending order
            dict_frequency_conut = sorted(dict_frequency_conuter.items(), key = operator.itemgetter(1), reverse = True)
            #print(dict_frequency_conuter)
            #print(dict_frequency_conut, file=txt)
            #print(dict_frequency_conut[0][0]) 
            print(str(tempTestData[0]) + ',' + str(dict_frequency_conut[0][0]), file=txt)    
    
#used to invoke functions in sequence
def executeFunctions():
    downloadTrainingTestDataset()
    suggestNewProduct()

#execute functions   
executeFunctions()
