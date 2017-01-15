
import FF_utils as utils
import FF_loggingConfig as config
import FF_threadedSerial as AT
import time
from datetime import datetime

def setSPOnOff(myNodeId = None, strOnOff = 'ON'):
    """ Repeatedly turn device on/off with given periods.
    """
    
    AT.stopThread.clear()  
    AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False)
    myNodeId = utils.discoverNodeIDbyCluster('0006')[2]

    if 'ON' in strOnOff.upper():
        AT.onOff(myNodeId, '09','0', '1')
    else: AT.onOff(myNodeId, '09','0', '0')
    
    AT.stopThreads()



if __name__ == '__main__':
    AT.stopThread.clear()  
    AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False)
    myNodeId = utils.discoverNodeIDbyCluster('0006')[2]
    while True:
        print("Swirching ON", datetime.today().strftime("%H:%M:%S" ))
        AT.onOff(myNodeId, '09','0', '1')
        time.sleep(45)
        print("Swirching OFF", datetime.today().strftime("%H:%M:%S" ))
        AT.onOff(myNodeId, '09','0', '0')
        time.sleep(300)
        
    AT.stopThreads()