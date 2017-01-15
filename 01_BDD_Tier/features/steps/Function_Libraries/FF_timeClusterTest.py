""" Testing Time.
"""
import time
import datetime
#import FF_threadedSerial as AT
import FF_loggingConfig as config

from calendar import timegm

#AT.debug = False

#pythonTime = int(time.time())

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

def utcDateStringToTimestamp(myString,dateFormat):
    timestamp = timegm(time.strptime(myString,dateFormat))
    return (timestamp)

def utcDateStringToZbHexTimestamp(myString,dateFormat):
    zbEpochInt = utcDateStringToTimestamp(zbEpochString,dateFormat)
    timestamp = timegm(time.strptime(myString,dateFormat)) - zbEpochInt
    hexTimestamp = '%08x' % timestamp
    return (hexTimestamp)

def utcDatetimeToZbHexTimestamp(myDatetime):
    zbEpochInt = utcDateStringToTimestamp(zbEpochString,dateFormat)
    timestamp = datetime.datetime.timestamp(myDatetime) -  zbEpochInt
    hexTimestamp = '%08x' % int(timestamp)
    return hexTimestamp
    
def zbHexToDateString(myString):
    zbEpochInt = utcDateStringToTimestamp(zbEpochString,dateFormat)    
    dateInt = int(myString,16) + zbEpochInt
    dateString = datetime.datetime.utcfromtimestamp(dateInt)
    return (dateString)

'''def readTimes(nodeId):
    """ Read back the time parameters a few times
    
    """
    # Read time attributes from co-ord
    myTime = datetime.datetime.now().strftime("%H:%M:%S.%f")
    _,_,stickUtcTime = AT.getAtr('000A', attrUtcTime)
    _,_,stickStandardTime = AT.getAtr('000A', attrStandardTime)
    _,_,stickLocalTime = AT.getAtr('000A', attrLocalTime)
    _,_,stickTimeStatus = AT.getAtr('000A', attrTimeStatus)
    
    stickUtcTime=zbHexToDateString(stickUtcTime)
    stickStandardTime=zbHexToDateString(stickStandardTime)   
    stickLocalTime=zbHexToDateString(stickLocalTime)
    #'Timestamp, Device, UTC, Standard (UTC+TZ), Local (Standard + DST)'
    print("{},stick,{},{},{},{}".format(myTime,stickUtcTime,stickStandardTime,stickLocalTime,stickTimeStatus))

    myTime = datetime.datetime.now().strftime("%H:%M:%S.%f")
    # Read time attributes from BM
    _,_,nodeUTC = AT.getAttribute(nodeId, '05', '000A', attrUtcTime, 'server')
    _,_,nodeLocal = AT.getAttribute(nodeId, '05', '000A', attrLocalTime, 'server')
    _,_,nodeStatus = AT.getAttribute(nodeId, '05', '000A', attrTimeStatus, 'server')
    
    nodeUTC=zbHexToDateString(nodeUTC)
    nodeLocal=zbHexToDateString(nodeLocal)
    print("{},node ,{},{},{},{}".format(myTime,nodeUTC,'                   ',nodeLocal,nodeStatus))
    
#     print('{}, UTC      = {}'.format(stickUtcTime, zbHexToDateString(stickUtcTime)))
#     print('{}, Standard = {}'.format(stickStandardTime, zbHexToDateString(stickStandardTime)))
#     print('{}, Local    = {}'.format(stickLocalTime, zbHexToDateString(stickLocalTime)))
# 
#     print()
# 
#     print('{}, Node UTC    = {}'.format(nodeUTC, zbHexToDateString(nodeUTC)))
#     print('{}, Node Local  = {}'.format(nodeLocal, zbHexToDateString(nodeLocal)))
#     print('Node Status = {}'.format(nodeStatus))

    return stickLocalTime, nodeLocal

def setTimes():
    """ Set DST start, DST end, Time s
    """
    dstStartHex = utcDateStringToZbHexTimestamp(dstStartString,dateFormat)
    dstEndHex = utcDateStringToZbHexTimestamp(dstEndString,dateFormat)
    testTimeHex = utcDateStringToZbHexTimestamp(testTimeString,dateFormat)
    
    timeStatus = timeStatusMasterClkBit | timeStatusSynchdBit | timeStatusMasterZoneDstBit
    timeStatus = "%02x" % timeStatus
    
    print('\rNote: ZB timestamps Epoch Time is 01/01/2000 00:00\r\n')
    print('DST Start (UTC), ZB Hex Timestamp: {0}, {1}'.format(dstStartHex,dstStartString))
    print('DST End (UTC),   ZB Hex Timestamp: {0}, {1}'.format(dstEndHex,dstEndString))
    print('Test Time (UTC), ZB Hex Timestamp: {0}, {1}'.format(testTimeHex,testTimeString))
    print('Time Status = {0}'.format(timeStatus))
    
    # Build the configuration AT commands
    # dstStart, dstEnd, dstShift, timeStatus, settime
    dstShift = "%08x" % (60*60)

    print('Sending time commands..')
    AT.setAtr('000A',attrDstStart,dstStartHex)
    AT.setAtr('000A',attrDstEnd,dstEndHex)
    AT.setAtr('000A',attrDstShift, dstShift)
    AT.setAtr('000A',attrTimeStatus, '07')
    AT.setTime(format(testTimeHex))
    AT.setTimerRD()
    
    return'''

"""  Code Starts
"""
if __name__ == "__main__":
    pass
    '''
    # Reset the stop threads flag
    AT.stopThread.clear()  # Reset the threads stop flag for serial port thread and attribute listener thread.
        
    # Start the serial port read/write threads and attribute listener thread
    AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False)

    nodeId=config.nodeList[0]['node']
    epId=config.nodeList[0]['ep1']

    setTimes()
    
    print('\rStart Reading Times')
    print('Timestamp, Device, UTC, Standard (UTC+TZ), Local (Standard + DST)')
    stickLocal,nodeLocal = readTimes(nodeId)
    #while stickLocal!=nodeLocal:
    while True:
        stickLocal,nodeLocal = readTimes(nodeId)
        time.sleep(10)
    
    print('\rAll Done.')'''