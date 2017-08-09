# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 16:08:26 2017

@author: Gaurav
"""

import requests
import pandas as pd
# url for training data set
url_JSON_Events = 'http://kevincrook.com/utd/tweets.json'
json_data = {} #store json data
#This function is used to access the dataset URL, fetch the data and load it into the text file
def readTweets():
    r = requests.get(url_JSON_Events)
    frequency_counter = 0
    json_data = r.json() # convert request object to json
    df = pd.DataFrame(json_data) #json data is store into dataframe
    df_grp = df.groupby(['lang'])[["text"]].count() #count of tweets group by language
    df_grp_sorted = df_grp.sort_values('text', ascending=False) #sort tweets based on counts
    #convert dataframe into string removing header and index to print only data
    df_string = df_grp_sorted.to_string(header=False, index_names=False).split('\n')
    # remmove spaces between language and tweets counts and join them with comma
    df_list_string = [','.join(item.split()) for item in df_string]
    with open("twitter_analytics.txt", "w", encoding = 'UTF-8') as txt:
        for item in json_data:
            if 'text' in item:
                #count total number of tweets
                frequency_counter += 1
        print(len(json_data), file = txt) #length for number of events
        print(frequency_counter, file = txt) # total number of tweets
        for item in df_list_string:
            print(item, file = txt) # tweets counts ased on language
    with open("tweets.txt", "w", encoding = 'UTF-8') as txt:
        for item in json_data:
            if 'text' in item:
                print(item['text'], file = txt) #tweets 
        


readTweets()