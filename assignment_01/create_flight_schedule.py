# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 18:15:06 2017

@author: Gaurav
"""

#['TailNo', 'A/B: Available/Busy', 'Gate: On Which gate or STN: No gate', 'BusyFrom','BusyTo']
aircraftdtl = [                            
            ['T1', 'A', 'STN', 0, 0],
            ['T2', 'A', 'STN', 0, 0],
            ['T3', 'A', 'STN', 0, 0],
            ['T4', 'A', 'STN', 0, 0],
            ['T5', 'A', 'STN', 0, 0],
            ['T6', 'A', 'STN', 0, 0]]

# ['B/F: Canbooked or not','Gate','Airport','A/B: Available/Busy', 'BusyFrom', 'BusyTo']
gatedtl = [['B', 'A', 'G1', 'AUS', 0, 0],
           ['B', 'A', 'G2', 'DAL', 0, 0],
           ['B', 'A', 'G3', 'DAL', 0, 0],
           ['B', 'A', 'G4', 'HOU', 0, 0],
           ['B', 'A', 'G5', 'HOU', 0, 0],
           ['B', 'A', 'G6', 'HOU', 0, 0]]

#gate values similar for same airport to avoide within airport flight booking
gateValue = {'G1':1, 'G2':2, 'G3':2, 'G4':3, 'G5':3, 'G6':3}

# Tail number, from Gate , from airport, To Gate, to airport
bookFlight = ['A', 'A','A','A','A']

#flight travel time between airports in minutes
flight_times = {'AUS-DAL': 50, 'DAL-AUS': 50, 'AUS-HOU' : 45, 'HOU-AUS' : 45, 'DAL-HOU': 65, 'HOU-DAL' : 65}

#airport minimum waiting time in minute
airport_wait_time = {'AUS': 25, 'DAL': 30, 'HOU': 35}

#Gates on airport
airportGates = {'G1': 'AUS', 'G2':'DAL', 'G3':'DAL', 'G4': 'HOU', 'G5':'HOU', 'G6':'HOU'}

#flights schedule entries are added in this list while preparing the schedule 
flight_schedule = []

#final flight schedule that holds records for printing
final_flight_schedule = [['tail_number','origin','destination','departure_time','arrival_time']]

start_time =360 #start time for flight schedule as 06:00 => (6 * 60) + 0 = 360
timer = 360 #this value will be used for looping check till end time
end_time = 1320 #end time of the day as 22:00 => (22 * 60) + 0 = 1320

#"""Convert time in minute since midnight to military time"""
def minutesSinceMidntToTime(mTime):
    return ("%02d%02d" % (divmod(mTime,60)))

#"""Function to print the flight schedule using list"""
def printFlightScedule():
    import csv
    sortFlightList()
    for row in flight_schedule:
        final_flight_schedule.append(row)
    #print(final_flight_schedule)
    with open('flight_schedule.csv', 'w', newline='') as schedule:
         wr = csv.writer(schedule, quoting=csv.QUOTE_ALL)
         for item in final_flight_schedule:
             wr.writerow(item)

#"""Sort the flight list tail_number, departure_time"""
def sortFlightList():
    import operator
    flight_schedule.sort(key=operator.itemgetter(0, 3))

#reset flight availability
def resetFlightAvailability():
    for item in aircraftdtl:
        if item[3] != 0 and item[4] != 0:
            if timer > item[4]:
                item[1] = 'A'
            else:
                item[1] = 'B'
        else:
            item[1] = 'A'

#reset gate availability
def resetGateAvailability():
    for item in gatedtl:
        item[0] = 'B'
        if item[4] != 0 and item[5] != 0:
            if timer > item[5]:
                item[1] = 'A'
            else:
                item[1] = 'B'
        else:
            item[1] = 'A' 

#search gate for flight
def searchGate():
    for gate in gatedtl:
        if gateValue[gate[2]] != gateValue[bookFlight[1]]:
            if gate[4] == 0  and gate[5] == 0:
                return gate[2]
            else:                
                arrivalTime = timer + flight_times[bookFlight[2]+'-'+airportGates[gate[2]]]
                if arrivalTime < end_time and arrivalTime > gate[5]:
                    return gate[2]
    return 'NG' # in case if no gate is availale

#update flight and gates ubsy timings
def updateBFBTForFlightAndGate():
    #update flight
    for item in aircraftdtl:
        if item[0] == bookFlight[0]:
            item[2] = bookFlight[3] # flight is on which gate 
            item[3] = timer #flight booked from
            # timer + flight travel time + minimum wait time : # flight booked till
            item[4] = timer + flight_times[bookFlight[2]+'-'+bookFlight[4]] + airport_wait_time[bookFlight[4]]                
            #print(item)
            break
    # update gate
    for item in gatedtl:        
        if item[2] == bookFlight[3]:
            # Gate will bbe busy from flight landing time till min airport wait time
            item[4] = timer + flight_times[bookFlight[2]+'-'+bookFlight[4]] 
            item[5] = timer + flight_times[bookFlight[2]+'-'+bookFlight[4]] + airport_wait_time[bookFlight[4]]
            #print(item)
            break

# Add flight entry into flight_schedule list
def updateFlightScheduleList():
    arrivaltime = timer + flight_times[bookFlight[2]+'-'+bookFlight[4]]
    row = [bookFlight[0],bookFlight[2],bookFlight[4], minutesSinceMidntToTime(timer), 
           minutesSinceMidntToTime(arrivaltime)
           #,bookFlight[1],bookFlight[3], minutesSinceMidntToTime(arrivaltime + airport_wait_time[bookFlight[4]]+1)
           ]
    flight_schedule.append(row)
    #print('row', row)

#increment global timer
def incrementTimer():
    global timer
    timer = timer+1
    
"""Flight Algorithm """
def prepareFlightSchedule():
    while timer < (end_time-65): #min time require by any flight for travel & airport wait is 65
        resetFlightAvailability()#reset flight status for new time check
        resetGateAvailability() #reset gate status for new time check            
        for flight in aircraftdtl:
            #print(timer)
            if(flight[1] == 'A'):
                bookFlight[0] = flight[0]
                #print('flight', flight[0])
                if flight[2] == 'STN':                                
                    for item in gatedtl:
                        if(item[1] == 'A' and item[0] == 'B'):
                            bookFlight[1] = item[2]
                            bookFlight[2] = airportGates[item[2]]
                            #print(item[2], airportGates[item[2]])
                            item[1] = 'B'
                            secondGate = searchGate()
                            #print('second', secondGate)
                            if secondGate != 'NG':
                                bookFlight[3] = secondGate
                                bookFlight[4] = airportGates[secondGate]
                                #print('second gate', secondGate, airportGates[secondGate])
                                # found flight and both gates now update BF, BT and Flight Schedule
                                flight[1] = 'B'
                                updateBFBTForFlightAndGate()
                                updateFlightScheduleList()
                                break
                else:
                    bookFlight[1] = flight[2]
                    bookFlight[2] = airportGates[flight[2]]
                    #now mark this gate as busy
                    for gate in gatedtl:
                        if gate[2] == flight[2]:
                            gate[1] = 'B'
                            break
                    secondGate = searchGate()
                    if secondGate != 'NG':
                        bookFlight[3] = secondGate
                        bookFlight[4] = airportGates[secondGate]
                        # found fligh and both gates now update BF, BT and Flight Schedule
                        flight[1] = 'B'
                        updateBFBTForFlightAndGate()
                        updateFlightScheduleList()
                        break
        incrementTimer() 
    printFlightScedule()
    #print(flight_schedule)
                            
prepareFlightSchedule()