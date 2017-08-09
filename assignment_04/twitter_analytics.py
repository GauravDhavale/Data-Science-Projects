# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 16:08:26 2017

@author: Gaurav
"""

import requests
import pandas as pd
# url for training data set
url_JSON_Events = 'http://kevincrook.com/utd/tweets.json'
json_data = {}
#This function is used to access the dataset URL, fetch the data and load it into the text file
def readTweets():
    r = requests.get(url_JSON_Events)
    frequency_counter = 0
    json_data = r.json()
    df = pd.DataFrame(json_data)
    df_grp = df.groupby(['lang'])[["text"]].count()
    df_grp_sorted = df_grp.sort_values('text', ascending=False)
    df_string = df_grp_sorted.to_string(header=False, index_names=False).split('\n')
    df_list_string = [','.join(item.split()) for item in df_string]
    with open("twitter_analytics.txt", "w", encoding = 'UTF-8') as txt:
        for item in json_data:
            if 'text' in item:
                frequency_counter += 1
        print(len(json_data), file = txt)
        print(frequency_counter, file = txt)
        for item in df_list_string:
            print(item, file = txt)
        
    
readTweets()