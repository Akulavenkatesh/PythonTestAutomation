
import FF_utils as utils
import FF_loggingConfig as config
import FF_threadedSerial as AT
import time
from datetime import datetime
from datetime import timedelta

def setSPOnOff(myNodeId = None, strOnOff = 'ON'):
    """ Repeatedly turn device on/off with given periods.
    """
    
    if 'ON' in strOnOff.upper():
        AT.onOff(myNodeId, '09','0', '1')
    else: AT.onOff(myNodeId, '09','0', '0')
    

def getDuration(strDuration):
    arrDuration = strDuration.split(':')
    intHour = int(arrDuration[0])
    intMin = int(arrDuration[1])
    intSec = int(float(arrDuration[2]))
    
    if (intHour > 0):
        strDuration = str(intHour) + " hour(s), " + str(intMin) + " minute(s), " + str(intSec) + " seconds"
        if (intHour > 23): 
            intDay = intHour // 24
            intHour = intHour % 24
            strDuration = str(intDay) + " day(s), "  + str(intHour) + " hour(s), " + str(intMin) + " minute(s), " + str(intSec) + " seconds"
    else:
        strDuration = str(intMin) + " minute(s), " + str(intSec) + " seconds"
    return strDuration;
#Gets the Time stamp for creating the folder set or for reporting time stamp based on boolFolderCreate 
def getTimeStamp(boolFolderCreate):
    if boolFolderCreate:
        str_format = "%d-%b-%Y_%H-%M-%S"  
    else:
        str_format = "%d-%b-%Y %H:%M:%S" 
    today = datetime.today()
    return today.strftime(str_format)

if __name__ == '__main__':
    AT.stopThread.clear()  
    AT.startSerialThreads('/dev/ttyUSB0', config.BAUD, printStatus=False)
    #myNodeId = utils.discoverNodeIDbyCluster('0006')[2]
    strBPMacID = "001E5E09020F6B26"
    SPNodeID = 'DDEC'
    intCntr = 0
    intPassCntr = 0
    intFailCntr = 0
    
    setSPOnOff(SPNodeID, 'OFF')
    time.sleep(5)
    setSPOnOff(SPNodeID, 'ON')
    time.sleep(5)
    while True:
        intCntr = intCntr+1
        myNodeID = utils.get_device_node_from_ntable(strBPMacID)
        if not myNodeID is "":
            print("Remove Device from Network: " , myNodeID)
            utils.remove_device_from_network(myNodeID)
            
        print(getTimeStamp(False), "Join Device to the network")
        intStartTime = time.time()
        intTCStartTime = time.monotonic()
        respState,respCode,resp = utils.check_device_joined(strBPMacID, "FFD", "FF")
        if respState: 
            intPassCntr = intPassCntr+1
            myNodeID = resp
            print("Device Joined the network with Node ID : ", myNodeID)
        else: 
            intFailCntr = intFailCntr+1
            print("join is unsuccessfull")
            print("Restarting the Smart Plug")
            setSPOnOff(SPNodeID, 'OFF')
            time.sleep(5)
            setSPOnOff(SPNodeID, 'ON')
            time.sleep(5)
            
        intTCEndTime = time.monotonic()
        strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
        strTCDuration = getDuration(strTCDuration)
        print("Time taken: ", strTCDuration)
        print('intCntr', intCntr, 'intPassCntr', intPassCntr, 'intFailCntr', intFailCntr)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print()
        
            
    AT.stopThreads()
    
    
    
    
    