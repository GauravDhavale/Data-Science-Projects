# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 18:15:06 2017

@author: Gaurav
"""

aircraft = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6']
airport = ['AUS', 'DAL', 'HOU']
flight_times = [['AUS', 'DAL', 45], ['DAL', 'AUS', 45]]
airport_wait_time = [['AUS', 25], ['DAL', 30], ['HOU', 35]]
airport_gate = [['AUS', 1], ['DAL', 2], ['HOU', 3]]
flight_schedule = [['tail_number','origin','destination','departure_time','arrival_time']]

"""Function to print the flight schedule using list"""
def printFlightScedule():
    import csv
    with open('flight_schedule.csv', 'w') as schedule:
         wr = csv.writer(schedule, quoting=csv.QUOTE_ALL)
         for item in flight_schedule:
             wr.writerow(item)


   

    

 
