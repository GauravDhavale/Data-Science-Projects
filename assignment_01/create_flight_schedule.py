# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 18:15:06 2017

@author: Gaurav
"""

aircraft = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6']
airport = ['AUS', 'DAL', 'HOU']
flight_times = {'AUS-DAL': 50, 'DAL-AUS': 50, 'AUS-HOU' : 45, 'HOU-AUS' : 45, 'DAL-HOU': 65, 'HOU-DAL' : 65}
airport_waiting = [['AUS', 25], ['DAL', 30], ['HOU', 35]]
airport_wait_time = dict(airport_waiting)
airport_gate = [['AUS', 1], ['DAL', 2], ['HOU', 3]]
airport_gate_no = dict(airport_gate)
flight_schedule = [['tail_number','origin','destination','departure_time','arrival_time']]
start_time =360
counter = start_time
end_time = 1320

def minutesSinceMidntToTime(mTime):
    return str(int(mTime/60)) +":"+ str(mTime % 60)


"""Function to print the flight schedule using list"""
def printFlightScedule():
    import csv
    with open('flight_schedule.csv', 'w') as schedule:
         wr = csv.writer(schedule, quoting=csv.QUOTE_ALL)
         for item in flight_schedule:
             wr.writerow(item)


"""Flight Algorithm """
def searchTime():
    while counter <= end_time:
        if counter + flight_times['AUS-DAL'] < end_time:
            templist = [aircraft[0], airport[0], airport[1],minutesSinceMidntToTime(counter),
                        minutesSinceMidntToTime(counter+flight_times['AUS-DAL'])]            
            flight_schedule.append(templist)
        counter += flight_times['AUS-DAL']
    




   

    

 
