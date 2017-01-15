'''
Created on 5 May 2016

@author: ranganathan.veluswamy
'''

import time

import FF_loggingConfig as config
import FF_threadedSerial as AT
import FF_zigbeeClusters as zcl


NodeID = "6F88"
EP = "09"

selectedAttribute = {"0001":["0001"]}
reportingFrequency = 2

ResultRootPath="/volumes/hardware/TestFiles/"
#ResultRootPath="/home/pi/hardware/TestFiles/"



def ReadAttributes():
    
    #Open Text file to write the light parameters
    oFileWriter = open(ResultRootPath + "ReadAttribute.txt", 'w')
    oFileWriter.write("NodeID: " + NodeID + ", EP: " + EP + "\n")
    oFileWriter.close()
    del oFileWriter
    
    intCntr = 0
    while True:
        intCntr = intCntr + 1
        print("Reporting Counter: " + str(intCntr))
        for myCluster in selectedAttribute:        
            clustId, clustName = zcl.getClusterNameAndId(myCluster)
            for attribute in selectedAttribute[myCluster]:
                attrId, attrName, attrType = zcl.getAttributeNameAndId(clustId, attribute)
    
                respState, respCode, respTemp = AT.getAttribute(NodeID, EP, myCluster, attrId, 'server')
                respTemp =   str(int(respTemp,16) * 2)
                #if not respCode is "00": respTemp = (respState, respCode, respTemp)
                print(clustId, clustName,"<===>",  attrId, attrName, "<===>", respTemp)                
                oFileWriter = open(ResultRootPath + "ReadAttribute.txt", 'a')
                oFileWriter.write(clustId + "," +clustName + "," + "<===>" + "," + attrId + "," +attrName + "," +"<===>" + "," +respTemp + "\n")
                oFileWriter.close()
                del oFileWriter
        time.sleep(reportingFrequency)
        
def initialize():
    # Reset the stop threads flag
    AT.stopThread.clear()  
    # Start the serial port read/write threads and attribute listener thread
    AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False, rxQ=True, listenerQ=False)





def returnBaseState():
    AT.stopThreads()

if __name__ == '__main__':
    initialize()
    ReadAttributes()
    returnBaseState()