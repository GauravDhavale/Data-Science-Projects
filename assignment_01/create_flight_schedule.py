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
flight_schedule = []
final_flight_schedule = [['tail_number','origin','destination','departure_time','arrival_time']]
start_time =360
counter = 0
end_time = 1320

"""Convert time in minute since midnight to military time"""
def minutesSinceMidntToTime(mTime):
    return ("%02d%02d" % (divmod(mTime,60)))


"""Function to print the flight schedule using list"""
def printFlightScedule():
    import csv
    sortFlightList()
    for row in flight_schedule:
        final_flight_schedule.append(row)
    with open('flight_schedule.csv', 'w', newline='') as schedule:
         wr = csv.writer(schedule, quoting=csv.QUOTE_ALL)
         for item in final_flight_schedule:
             wr.writerow(item)

"""search element in flight list"""


"""Sort the flight list tail_number, departure_time"""
def sortFlightList():
    return flight_schedule.sort(key = lambda x: (x[1], x[4]))

"""Flight Algorithm """
def prepareSchedule():
    counter = start_time
    while counter <= end_time:
        if counter + flight_times['AUS-DAL'] < end_time:
            templist = [aircraft[0], airport[0], airport[1],minutesSinceMidntToTime(counter),
                        minutesSinceMidntToTime(counter+flight_times['AUS-DAL'])]            
            flight_schedule.append(templist)
        counter += flight_times['AUS-DAL'] + airport_wait_time['DAL'] + 1
        
        if counter + flight_times['DAL-AUS'] < end_time:
            templist = [aircraft[0], airport[0], airport[1],minutesSinceMidntToTime(counter),
                        minutesSinceMidntToTime(counter+flight_times['AUS-DAL'])]            
            flight_schedule.append(templist)
        counter += flight_times['DAL-AUS'] + airport_wait_time['AUS'] + 1
    printFlightScedule()
    
        
    




   

    

 
