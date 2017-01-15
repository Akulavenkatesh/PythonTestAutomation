'''
Created on 9 May 2015

@author: keith
'''

from calendar import timegm
import datetime
import time


dstStartString = '27/03/2016 01:00GMT'
dstEndString = '30/10/2016 01:00GMT'
timeFormat='%d/%m/%Y %H:%MGMT'

dstStartUTC = datetime.datetime.strptime(dstStartString,timeFormat)
dstEndUTC = datetime.datetime.strptime(dstEndString,timeFormat)



year = '2000'
month = '01'
day = '01'
hour = '00'
minute = '00'
second = '00'

attrUtcTime = '0000'
attrTimeStatus = '0001'
attrTimeZone = '0002'
attrDstStart = '0003'
attrDstEnd = '0004'
attrDstShift = '0005'
attrStandardTime = '0006'
attrLocalTime = '0007'

timeStatusMasterClkBit = 0x01      # If set then RTC is set
timeStatusSynchdBit = 0x02         # If set then time synched via zigbee 
timeStatusMasterZoneDstBit = 0x04  # If set then TimeZone,DSTStart, DSTEnd and DSTShift are all correct
timeStatusSupercedeBit = 0x08      # If this bit set then this source is prefered

dstStartString = '29/03/2015 01:00:00GMT'
dstEndString = '25/10/2015 01:00:00GMT'
zbEpochString = '01/01/2000 00:00:00GMT'
testTimeString = datetime.datetime.utcnow().strftime('%d/%m/%Y %H:%M:%SGMT')
#testTimeString = '25/10/2015 01:58:00GMT'


dateFormat = '%d/%m/%Y %H:%M:%S%Z' 

""" Method to map all local time events to UTC time """
def getEventUtcTime(eventDatetimeLocal):
    """ Return the UTC event time for an event.
    
        eventDatetimeLocal is a dt object with the correct date of the event and the local time of the
        event.  The time may be GMT or BST depending on the day of the year.
        
        Method uses day to work out UTC time (GMT). During GMT periods eventTimeUTC is same as
        eventTime.  During BST period eventTimeUTC is eventTime-1hr. Some logic required to handle
        events occurring during the DST sate/end periods where local time jumps by 1hr.
        
        Given:
        
        a) The date the event will occur on
        b) The local time (DST or GMT depending)
        
        Datetimes before DST start: eventTimeUTC = eventTimeLocal
        Datetimes during the missing DST start hour (clocks going forward): eventTimeUTC = 01:00am
        Datetimes after DST switch i.e. 02:00(local) to DSTend datetime: eventTimeUTC=eventTime-1hr
        Datetimes after DSTend switch: eventTimeUTC = eventTime
        
        Note: Since events are taken from a Q in the device, events occurring during the DSTend hour
              where clocks go back, do not occur twice.  The event has been consumed from the Q and 
              does not therefore get re-enacted at the second pass through.
    
    """

    # Check to see if we need to change the dstStart/dstEnd parameters
    if datetime.datetime.now().year != dstEndUTC.year or datetime.datetime.now().year != dstStartUTC.year:
        print("\n******")
        print("DST start and end dates are not for this year - please correct")
        print("\n******")
        exit()
    
    # GMT periods before and after BST period 
    if eventDatetimeLocal<dstStartUTC or eventDatetimeLocal>=dstEndUTC:
        eventDatetimeUTC = eventDatetimeLocal

    # During 1hr clock forward period
    dstStartLocal = dstStartUTC.replace(hour=2,minute=0)
    if eventDatetimeLocal>=dstStartUTC and eventDatetimeLocal<dstStartLocal:
        eventDatetimeUTC = dstStartUTC
        
    # During the DST period
    dstEndLocal = dstEndUTC.replace(hour=2,minute=0)
    if eventDatetimeLocal>=dstStartLocal and eventDatetimeLocal<dstEndLocal:
        eventDatetimeUTC = eventDatetimeLocal - datetime.timedelta(hours=1)
    
    return eventDatetimeUTC
def test_specialDates_getEventUtcTime():
    """ Test for getEventUtcTime() 
        Executes for a list of given test dates.
        
    """
    
    eventTimeStringList = [('1/1/2015 00:00GMT','1/1/2015 00:00GMT'),     # start of year GMT
                           ('29/3/2015 00:59GMT','29/3/2015 00:59GMT'),   # Just prior to dstStart
                           ('29/3/2015 01:00GMT','29/3/2015 01:00GMT'),    # dstStart - before DST applied
                           ('29/3/2015 01:59GMT','29/3/2015 01:00GMT'),    # Just prior to end of missing hour in dstStart
                           ('29/3/2015 02:00GMT','29/3/2015 01:00GMT'),    # Just after DST start
                           ('29/3/2015 02:01GMT','29/3/2015 01:01GMT'),    # More just after DST start
                           ('11/07/2015 01:30GMT','11/07/2015 00:30GMT'),   # Arbitrary mid year time
                           ('25/10/2015 02:00GMT','25/10/2015 02:00GMT'),   # dstEnd (local)
                           ('25/10/2015 02:01GMT','25/10/2015 02:01GMT'), # Just after dstEnd
                           ('25/12/2015 00:00GMT','25/12/2015 00:00GMT')]   # Close to end of year
    
    for event in eventTimeStringList:
        eventLocalDT = datetime.datetime.strptime(event[0],timeFormat)
        eventUTC = datetime.datetime.strptime(event[1],timeFormat)
        calculatedUTC = getEventUtcTime(eventLocalDT)
        try:
            assert eventUTC==calculatedUTC
        except AssertionError:
            print("*** UTC Convertion test failed")
            print('Local Time = {}'.format(eventLocalDT))
            print('Expected UTC = {}'.format(eventUTC))
            print('Calculated UTC = {}'.format(calculatedUTC))
            exit()
    
    print('ALL TESTS PASS')
    
    return 0

def utcDatetimeToZbHexTimestamp(myDatetime):
    zbEpochInt = utcDateStringToTimestamp(zbEpochString,dateFormat)
    timestamp = datetime.datetime.timestamp(myDatetime) -  zbEpochInt
    hexTimestamp = '%08x' % int(timestamp)
    return hexTimestamp

def utcDateStringToTimestamp(myString,dateFormat):
    timestamp = timegm(time.strptime(myString,dateFormat))
    return (timestamp)

""" ZigBee Time and Temperature type manipulations """
def roundTimeUp(myTime, baseSeconds=15*60):
    """ Take a given datetime and round up to the next nearest x seconds.
        Add x/2 minutes to given time and then round to next highest x minutes
        Default is 15 minutes rounding.  e.g. 10:32 gets rounded to 10:45
    """
    #epoch=datetime.datetime(1970,1,1)
    
    # Shift it by 0.5 times base
    myNewTime=myTime+datetime.timedelta(seconds=baseSeconds/2)
    # Covert to seconds
    myNewTimeSeconds=(myNewTime.timestamp())

    # Round to the nearest x minutes
    myNewTimeSeconds=int(baseSeconds * round(myNewTimeSeconds/baseSeconds))
    myNewTime=datetime.datetime.fromtimestamp(myNewTimeSeconds)
       
    return myNewTime 
def temperatureFloatToHexString(myTemp):
    """ Convert a temperature float type to a hex string
    
    """
    return "{:04x}".format(int(myTemp*100)).upper()
def temperatureHexStringToFloat(myTemp):
    """ Convert a temperature hex string to a float type
    
    """
    return int(myTemp,16)/100    
def timeHexToString(myTime):
    """ Convert a hex minutes since midnight into an hh:mm string
    
    """
    time = int(myTime,16)
    hours,minutes = divmod(time,60)
    timeStr='{:02}:{:02}'.format(hours,minutes)
    return timeStr
def timeHexToMinutes(myTime):
    """ Convert a hex minutes to an integer minutes
    
    """
    minutes = int(myTime,16)
    return minutes
def timeStringToMinutes(myTime):
    """ Convert an 'hh:mm' string to an integer number of minutes since midnight
    
    """
    hours,minutes = myTime.split(':')
    minutes = (int(hours)*60) + int(minutes)
    return minutes
def timeStringToHex(myTime):
    """ Convert a 'hh:mm' string to a hex number of minutes since midnight
    
    """
    mins = timeStringToMinutes(myTime)
    timeHex="{:04x}".format(mins)
    return timeHex
def timeHexToDatetime(myTime):
    """ Convert a time in hex minutes since midnight to a datetime
    
    """
    myHours,myMins=divmod(timeHexToMinutes(myTime),60)
    myDatetime = datetime.datetime.now().replace(hour=myHours,minute=myMins,second=0,microsecond=0)
    return myDatetime
def getMinutesSinceMidnight():
    """ Returns current time expressed as minutes since midnight
    
    """
    now = datetime.datetime.now()
    minutes_since_midnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()/60
    return minutes_since_midnight
def timeStringToDatetimeUTC(myTime,myDate):
    """ Convert a given time string to a UTC datetime on the given day.
        myTime is of form 'hh:mm' (local time - so covert to UTC)
        myDate is a datetime on the day we want to use.
    
    """
    hours,minutes=myTime.split(':')
    hours=int(hours)
    minutes=int(minutes)
    
    myDatetime = myDate.replace(hour=hours,minute=minutes,second=0,microsecond=0)
    myDatetimeUTC = getEventUtcTime(myDatetime)
    
    return myDatetimeUTC

""" Guardzone methods """
def checkGuardZone(nowDatetime, events, guardZoneSeconds=30):
    """ Check if now time is within +/- guardZone seconds of any of the given events

        Parameters:
            nowDatetime - The current test time (may not be clock time if using a simulated time)
            events - Dictionary of the events to check.  Dict is in the form..
                    {'nameOfEvent1':datetime1, 'nameOfEvent2':datetime2}
            guardZoneSeconds - +/- seconds period around each event which we will consider to be the danger zone.

        Returns:
            status (true/false) - True=close to event, False = no proximity to event.
            secondsRemaining - When to re-try (based on first proximity match).
                               re-try after event + guardZoneSeconds
                               Or None if no proximity detected.
            eventName - Name of the event taken from the given dict of events
                        None if no proximity detected.
        
    """        
    # Check proximity to events in the given dict    
    for event in events:
        inBand,secondsRemaining=timeBand(nowDatetime, events[event], guardZoneSeconds)
        if inBand:
            return inBand, secondsRemaining, event
    
    # No event proximity found so return false
    return False,None,None
def timeBand(nowTime,eventTime,guardZoneSeconds):
    """ Check if given time lies with +/- seconds of eventTime
    
    """
    inBand = False
    secondsRemaining = None
    
    if eventTime!=None:
        timeDelta = datetime.timedelta(seconds=guardZoneSeconds)
        lowerBound = eventTime-timeDelta
        upperBound = eventTime+timeDelta        
        
        if nowTime>lowerBound and nowTime<upperBound:
            inBand=True
            secondsRemaining=(upperBound-nowTime).total_seconds()

    return inBand,secondsRemaining

if __name__=="__main__":

    print("Testing datetime UTC conversion functions.")
    test_specialDates_getEventUtcTime()
    
    print()
    timeDelta=datetime.timedelta(seconds=60)
    events={'nowTime':datetime.datetime.now(),
            'pastTime':datetime.datetime.now()-timeDelta,
            'futureTime':datetime.datetime.now()+timeDelta}
    
    print(events)
    print(checkGuardZone(datetime.datetime.now(), events, 30))