# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 16:08:26 2017

@author: Gaurav
"""

import requests
# url for training data set
url_JSON_Events = 'http://kevincrook.com/utd/tweets.json'
json_data = {}
#This function is used to access the dataset URL, fetch the data and load it into the text file
def readTweets():
    r = requests.get(url_JSON_Events)
    frequency_counter = 0
    json_data = r.json()
    with open("twitter_analytics.txt", "w") as txt:
        for item in json_data:
            if 'text' in item:
                frequency_counter += 1
        print(len(json_data), file = txt)
        print(frequency_counter, file = txt)
    
readTweets()