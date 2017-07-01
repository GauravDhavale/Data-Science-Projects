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
gatedtl = [
           ['B', 'A', 'G1', 'AUS', 0, 0], 
           ['B', 'A', 'G2', 'DAL', 0, 0],
           ['B', 'A', 'G5', 'HOU', 0, 0],                    
           ['B', 'A', 'G3', 'DAL', 0, 0],
           ['B', 'A', 'G4', 'HOU', 0, 0],
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
flight_schedule_final = []

#final flight schedule that holds records for printing
flight_schedule_hdr = 'tail_number,origin,destination,departure_time,arrival_time'
fileName = 'flight_schedule.csv';
start_time =360 #start time for flight schedule as 06:00 => (6 * 60) + 0 = 360
timer = 360 #this value will be used for looping check till end time
end_time = 1320 #end time of the day as 22:00 => (22 * 60) + 0 = 1320

replace_gate = '';
missing_gate = '';

#"""Convert time in minute since midnight to military time"""
def minutesSinceMidntToTime(mTime):
    return ("%02d%02d" % (divmod(mTime,60)))

#"""Function to print the flight schedule using list"""
def printFlightScedule():
    sortFlightList()
    for x in flight_schedule_final:
        del x[5:7]
    with open(fileName,'wt') as f:
        print(flight_schedule_hdr, file=f)
        for s in flight_schedule_final:
            print(','.join(s), file=f)

#"""Sort the flight list tail_number, departure_time"""
def sortFlightList():
    import operator
    flight_schedule_final.sort(key=operator.itemgetter(0, 3))

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
    import operator
    gatedtl.sort(key=operator.itemgetter(5))
    for gate in gatedtl:
        if gateValue[gate[2]] != gateValue[bookFlight[1]]:
            if gate[4] == 0  and gate[5] == 0:
                return gate[2]
            else:                
                arrivalTime = timer + flight_times[bookFlight[2]+'-'+airportGates[gate[2]]]
                if arrivalTime < end_time and arrivalTime >= gate[5]:
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
           ,bookFlight[1],bookFlight[3]
          # , str(airport_wait_time[bookFlight[4]]),str(bookFlight[2] + '-'+ bookFlight[4])
           ]
    flight_schedule.append(row)
    #print('row', row)

#check flight location
def checkMissingGateInfo():
    global replace_gate
    global missing_gate
    for gate in airportGates.keys():
        if sum(x.count(gate) for x in aircraftdtl) > 1:
            replace_gate = gate            
        if sum(x.count(gate) for x in aircraftdtl) == 0:
            missing_gate = gate
            return True
    return False
            
def modifySchedule():
    global flight_schedule_final
    flight_schedule_final = flight_schedule
    for index, item in enumerate(reversed(flight_schedule)):
        counter = len(flight_schedule)- index - 1 
        if item[6] == replace_gate and item[5] != missing_gate:
            x, y = divmod(int(item[3]),100)
            flightStartTime = x*60 + y
            flight_schedule_final[counter][4] = minutesSinceMidntToTime(flightStartTime+flight_times[item[1]+'-'+ airportGates[replace_gate]])
            flight_schedule_final[counter][2] = airportGates[missing_gate]
            flight_schedule_final[counter][6] = missing_gate
            break
    

#increment global timer
def incrementTimer():
    global timer
    timer = timer+1
    
"""Flight Algorithm """
def prepareFlightSchedule():
    while timer < (end_time): 
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
    if(checkMissingGateInfo()):
        modifySchedule()
    printFlightScedule()
    #print(flight_schedule)
                            
prepareFlightSchedule()