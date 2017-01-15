
'''
Created on Feb 11, 2015

@author: keith
'''

from datetime import timedelta
import datetime
from getopt import getopt
import queue
import random
import re
import sys
import threading
import time

import redis
import serial
import FF_loggingConfig as lc
import FF_zigbeeClusters as zcl
import FF_convertTimeTemperature as tct

import sqlite3
'''Sno =0
global Sno'''
r = redis.StrictRedis(host='localhost', port=6379, db=0)

MANUFACTURER_ID=''
sequenceNumber = -1

# Default Thermostat setpoints
MANUAL_DEFAULT = 20
BOOST_DEFAULT = 22

debug = False
rxQueue = queue.Queue()
txQueue = queue.Queue()
listenerQueue = queue.Queue()

stopThread = threading.Event()
threadPool = []

""" Serial Port methods """
def serialReadHandler(ser,rxQ=False,listenerQ=False):
    """ Serial port read thread handler
        If serial timeout=None then this thread blocks until a new line is available
     
    """
    while not stopThread.isSet():
        reading = ser.readline().decode(errors='replace').strip()
        if reading!='':
            # Make sure Qs are not full and blocking
            if rxQ:
                if rxQueue.full():
                    print("*** DEBUG: rxQueue is full.  Dumping oldest message")
                    rxQueue.get()
                rxQueue.put(reading)
            
            # Deal with listerQueue if it is switched on
            if listenerQ:
                if listenerQueue.full():
                    print("*** DEBUG: listenerQueue is full.  Dumping oldest message")
                    listenerQueue.get()
                listenerQueue.put(reading)          
                
            myTime = datetime.datetime.now().strftime("%H:%M:%S.%f")
            if debug: print("DEBUG RX: {},  {}".format(myTime,reading))
    print('Serial read thread exit')
    return 0

def debug_serialReadHandler(ser):
    """ Serial port read thread handler
        If serial timeout=None then this thread blocks until a new line is available
     
    """
    reading=''
    while not stopThread.isSet():
        readChr = ser.read()
        # Now we can see whether we are getting \n\r or,
        # if in fact the read is blocking  
        print(readChr)
        reading += readChr.decode()
        if '\n' in reading:
            reading = reading.strip()
            if reading!='':
                rxQueue.put(reading)
                myTime = datetime.datetime.now().strftime("%H:%M:%S.%f")
                if debug: print("DEBUG RX: {},  {}".format(myTime,reading))
            reading=''
    return 0
def serialWriteHandler(ser):
    """ Serial port write handler
    
        Get from a queue blocks if queue is empty so we just loop
        and wait for items
    
    """
    while not stopThread.isSet():
        try:
            myMessage = txQueue.get(timeout=1)
            myTime = datetime.datetime.now().strftime("%H:%M:%S.%f")
            if debug: print("DEBUG Tx: {},  {}".format(myTime,myMessage))
            if type(myMessage) is str:
                ser.write(bytearray(myMessage + '\r\n','ascii'))
            else:
                ser.write(myMessage)
        except queue.Empty:
            pass
    print('Serial write thread exit')
    return 0
def startSerialThreads(port, baud, printStatus=False, rxQ=False, listenerQ=False):
    """ 
        rxQ and listenerQ are flags to switch on/off the appropriate Q
        defaults are off.
        
    """
    try:
        serial_port = serial.Serial(port, baud, timeout=1)
        global ser
        ser=serial_port
    except IOError as e:
        print('Error opening port.',e)
        exit()
    if printStatus: print("Serial port opened...{0}".format(port))

    # Make sure the stopThread event is not set
    stopThread.clear()

    # Start the serial port handler thread    
    readThread = threading.Thread(target=serialReadHandler, args=(serial_port,rxQ,listenerQ))
    readThread.daemon = True # This kills the thread when main program exits
    readThread.start()
    readThread.name = 'readThread'
    threadPool.append(readThread)
    if printStatus: print('Serial port read handler thread started.')
    
    writeThread = threading.Thread(target=serialWriteHandler, args=(serial_port,))
    writeThread.daemon = True # This kills the thread when main program exits
    writeThread.start()
    writeThread.name = 'writeThread'
    threadPool.append(writeThread)
    if printStatus: print('Serial port write handler thread started.')
    
    if printStatus:
        if rxQ:
            print('rxQueue is ON')
        else:
            print('rxQueue is OFF')
            
        if listenerQ:
            print('listenerQueue is ON')
        else:
            print('listenerQueue is OFF')
    print()
    return

def stopThreads():
    """ Set the stop event and wait for all threads to exit
    
    """
    stopThread.set()
    for t in threadPool:
        t.join()
    return

def printAllResponses():
    """
    """
    while True:
        if not rxQueue.empty():
            item = rxQueue.get()  # Pop first item from the Queue
            myTime = datetime.datetime.now().strftime("%H:%M:%S.%f")
            print("RX: {},  {}".format(myTime,item))
    return 0
def flushRxQ():
    """
    """
    while not rxQueue.empty():
        rxQueue.get()    
    return
def sendCommand(cmd,myExpectedResponses,maxAttempts=5,retryTimeout=30):
    """ Sends a command and reads the rxQueue looking for the raw response
        Returns the single line response or a list or responses if the 
        response is a SEQ (multi-row response)
    
    """
    
    intTCStartTime = time.monotonic()
    flushRxQ()

    txQueue.put(cmd)
    myTime = datetime.datetime.now().strftime("%H:%M:%S.%f")
    if debug: print("DEBUG Tx: {},  {},Expected Response={}".format(myTime,cmd,myExpectedResponses))
    lastTry = time.time()
    tryCount = 1
    
    # Loop until all retries done
    respValue = ''
    respState = False
    doLoop = True
    
    while doLoop:
        
        # Some message received so do something with it
        if not rxQueue.empty():
            resp = rxQueue.get()
            
            respState, respCode = matchResponse(resp, myExpectedResponses)
            
            # If it is what we want then exit
            if respState:
                respValue = resp
                #Comment for SQLITe data
                '''intTCEndTime = time.monotonic()
                strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
                strTCDuration = getDuration(strTCDuration)   
                intSeconds = float(strTCDuration.split(",")[1].strip().split(" ")[0])
                intMin = float(strTCDuration.split(",")[0].strip().split(" ")[0])
                intSeconds = intMin*60.0 + intSeconds
                #Sno = Sno + 1
                conn.executescript("insert into " + strTableName + " (Iteration, TimeStamp, AT_Command, TryCount, Duration) values ('" + str(intGetDurationCntr) + "', '" + str(getTimeStamp(False)) + "', '" + cmd + "', '" + str(tryCount) + "', '" + str(intSeconds) + "');")
                conn.commit()
                print(cmd)
                print("Time taken: " + strTCDuration)'''
                return respState, respCode, respValue
          
    
            # If unsupported command then exit
            if resp.startswith('DFTREP'):
                r = resp.split(',')
                if r[4]=='82':
                    respState = False
                    respCode = '82'
                    respValue = 'Unsupported Command'
                    return respState, respCode, respValue  
                  
            # If ERROR:18 then stick has gone into a bad mode.  Reset it.
            # if resp.startswith('ERROR:18'):
            #    print('ERROR 18: Resetting Telegesis USB with ATZ command')
            #    txQueue.put('ATZ')
                
            # If an ERROR or NACK then print an error
            if resp.startswith('ERROR') or resp.startswith('NACK'):
                print('Error : ',resp)
       
        # No valid response received so check for retry timeout
        # If yes then retry else do nothing        
        if time.time() > lastTry + retryTimeout:
            if tryCount<maxAttempts:
                # Retry and reset the retry timer
                myMessage = 'Timeout: Re-queue Tx command, {}'.format(cmd)
                myTime = datetime.datetime.now().strftime("%H:%M:%S.%f")
                if debug: print("DEBUG Tx: {},  {}".format(myTime,myMessage))
                lastTry = time.time()
                tryCount += 1
                txQueue.put(cmd)
            else:
                # All retries sent. Exit.
                doLoop = False
    
    # Command sent with retries.  No valid response.
    respState = False
    respCode = None
    respValue = "TIMEOUT: sendCommand() timeout"
    
    '''intTCEndTime = time.monotonic()
    strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
    strTCDuration = getDuration(strTCDuration)   
    print("Time taken: " + strTCDuration)'''
    return respState, respCode, respValue

""" Helper methods """
def matchResponse(myResp, myExpectedResponses):
    """ Returns a match if the given response matches one of the given expected responses.
    
        Expected responses should be in the form:
            READRPTCFGRSP:F14D,05,FC00,(..),00,0002
        The parameter in the curved brackets is the ZigBee response code.  We use regex to match against the
        string and extract the response code.
        
        Returns True if a match is found, else False
        Returns the 
    """    
    for er in myExpectedResponses:
        matchPattern = re.compile(er)
        match = matchPattern.search(myResp)
        if match:
            # If there is a response code then extract it
            if len(match.regs)>1:
                respCode = match.group(1)
            else:
                respCode = None
            return True, respCode
    return False, None
def byteSwap(myString):
    first = myString[0:2]
    last = myString[2:4]
    return last+first
def buildCombinedAttributeString(attrList, clustName):
    """ Returns a string of concatenated attributeId,Type,Value for multi attribute write
        Requires a list of Tuples (attribute name, attribute value)
        
    """
    attrString = ''
    for attr in attrList:
        attrId,_,attrType = zcl.getAttributeNameAndId(clustName, attr[0])
        attrString = attrString + ",{},{},{}".format(attrId,attrType,attr[1])
    return attrString
def getSequenceNumber():
    """
    """
    global sequenceNumber
    sequenceNumber += 1
    if sequenceNumber>255: sequenceNumber=0
    seqNumHex = "{:02x}".format(sequenceNumber)
    return seqNumHex
""" AT Command methods """
def buildClusterList(endpoint):
    """  Takes an object of the form:
         {'ep': '05', 'clusters': {'servers': ['1', '2'], 'clients': ['2', '3']}}
         
         Returns a list of the form:
         [{'server': '1'}, {'server': '2'}, {'client': '2'}, {'client': '3'}]
         
         This is easier to iterate over.
    """    
    myList = []
    for clust in endpoint['InCluster']:
        myList.append(('server',clust))
    for clust in endpoint['OutCluster']:
        myList.append(('client',clust))
    return myList
def getNetwork():
    """ Request the Network Information
        Returns deviceType, channel, power, pan ID and EPANID
    """
    myMsg = 'AT+N'
    expectedResponse = ['\+N=']
    
    respState,respCode,respValue = sendCommand(myMsg,expectedResponse)
    
    if respState:
        # +N=<devicetype>,<channel>,<power>,<PANID>,<EPANID>
        respTemp = respValue[3:]    # Strip the '+N=' string from the start
        respTemp = respTemp.split(',')
        if respTemp[0]=="NoPAN":
            respState = False
            resp = respTemp[0]
        else:
            resp={}
            respCode=zcl.statusCodes['SUCCESS']
            resp['deviceType'] = respTemp[0]
            resp['channel'] = respTemp[1]
            resp['power'] = respTemp[2]
            resp['panId'] = respTemp[3]
            resp['epanId'] = respTemp[4]
    else:
        resp = respValue
    return respState, respCode, resp
def getEUI(myDirectoryNode, myWantedNode):
    """ Returns the EUI of wantedNode
        DirectoryNode is the node that we will query to see if it has a record of the wanted node
        Generally we query a node for it's own EUI, but it is possible to query other nodes.
        If nodeId = 0000, then return EUI of the controller
    """
    index = '00'  # Index number - parameter to define whther child node addresses should also be returned
    myMsg = 'AT+EUIREQ:{0},{1},{2}'.format(myDirectoryNode,myWantedNode,index)
    expectedResponse = ['AddrResp:(..),{0}'.format(myWantedNode)]
    # AddrResp:00,6456,001E5E0902003DE1
    
    respState, respCode, respValue = sendCommand(myMsg, expectedResponse)

    if respState:
        resp = respValue.split(',')
        resp = resp[2]
    else:
        resp = respValue
        
    return respState,respCode,resp
def getNodeDesc(myDirectoryNode, myWantedNode):
    """ Request the Node description of wantedNode from the directoryNode
    """
    myMsg = 'AT+NODEDESC:{0},{1}'.format(myDirectoryNode,myWantedNode)
    expectedResponse = ['NodeDesc:{0},(..)'.format(myWantedNode)]
    
    respState,respCode,respValue = sendCommand(myMsg,expectedResponse)
    
    global MANUFACTURER_ID
    if respState:
        # Pop next line of the response from the queue
        # it should be 'Type:FFD' or similar
        r = rxQueue.get()
        r = r.split(':')
        if r[0]=='Type':
            resp=r[1]
            for _ in range(0,6):
                r = rxQueue.get()
                r = r.split(':')
                if r[0]=='ManufCode':
                    MANUFACTURER_ID=r[1]
            if MANUFACTURER_ID=='':
                print('Manufacturer Code not found in NodeDesc response.')
                exit()
        else:
            resp=respValue
    else:
        resp = respValue
    return respState, respCode, resp
def discEndpoints(myNodeId):
    """
    """
    myMsg = 'AT+ACTEPDESC:{0},{1}'.format(myNodeId,myNodeId)
    expectedResponses = ['ActEpDesc:{},(..)'.format(myNodeId)]    
    respState, respCode, respValue = sendCommand(myMsg, expectedResponses)    
    # Typical response format:
    # ActEpDesc:ACB0,00,05,06,07,08
    # Split on commas and discard first two fields
    if respState and respCode==zcl.statusCodes['SUCCESS']:
        respData = respValue.split(',')[2:]
    else:
        respData = respValue
    return respState, respCode, respData
def discClusters(myNodeId, myEP):
    """
    """
    myMsg = 'AT+CLUSDISC:{0},{1}'.format(myNodeId,myEP)
    expectedResponse = ['DISCCLUS:{0},(..),{1}'.format(myNodeId,myEP)]    
    respState, respCode, respValue = sendCommand(myMsg, expectedResponse)
    
    respData = {'servers':[],'clients':[]}
    
    if respState and respCode==zcl.statusCodes['SUCCESS']:
        # The next two items in the rxQueue should be a string for the server clusters 
        # and a string for the clients.  Pop then and save in a temporary list.
        myList = []
        myList.append(rxQueue.get())
        myList.append(rxQueue.get())
        
        for clustString in myList:
            clusterList = clustString.split(',')
            if clusterList[0].startswith('SERVER:'):
                clusterList[0]=clusterList[0].replace('SERVER:','')
                # Only add to the list if there is at least one cluster
                if clusterList[0]!='': respData['servers']=clusterList
            elif clusterList[0].startswith('CLIENT:'):
                clusterList[0]=clusterList[0].replace('CLIENT:','')
                # Only add to the list if there is at least one cluster
                if clusterList[0]!='': respData['clients']=clusterList
    else:
        respData = respValue
    return respState, respCode, respData
def discAttrs(myNodeId, myEP, myClusterId, myClusterType, myStart='0000',numAttrsToRetrieve='FF'):
    """ Returns all the attributes for the given cluster
        
        May send multiple discovery commands if the response does not contain a full list
    """
    startAttr = myStart
    attrCount = numAttrsToRetrieve
    discAttrsCmd = '0C'

    # Frame Control Bytes
    fcClientRead = '08'
    fcServerRead = '00'
    fcClientReadManSpecific = '0C'
    fcServerReadManSpecific = '04'
    
    allFound = False
    respData = []
    
    # DISCMATTR:D198,05,1039,00
    # DISCATTR:D198,05,00
    
    while not allFound:
        
        if myClusterId in zcl.BG_Clusters:
            manId = byteSwap(MANUFACTURER_ID)
            expectedResponse = ['DISCMATTR:{0},{1},{2}'.format(myNodeId,myEP,MANUFACTURER_ID)]
            if myClusterType == 'server':
                fc = fcServerReadManSpecific
            else:
                fc = fcClientReadManSpecific
        else:
            manId = ''
            expectedResponse = ['DISCATTR:{0},{1}'.format(myNodeId,myEP)]
            if myClusterType == 'server':
                fc = fcServerRead
            else:
                fc = fcClientRead

        sequenceNumber = getSequenceNumber()
        writeMsg = 'AT+RAWZCL:{0},{1},{2},{3}{4}{5}{6}{7}{8}'.format(myNodeId,
                                                                    myEP,
                                                                    myClusterId,
                                                                    fc,
                                                                    manId,
                                                                    sequenceNumber,
                                                                    discAttrsCmd,
                                                                    byteSwap(startAttr),
                                                                    attrCount)
        
        respState, respCode, respValue = sendCommand(writeMsg, expectedResponse)

#         DISCATTR:5ACF,05,00
#         
#         CLUS:0000,ATTR:0000,TYPE:20
#         CLUS:0000,ATTR:0001,TYPE:20
#         CLUS:0000,ATTR:0002,TYPE:20
#         CLUS:0000,ATTR:0003,TYPE:20
#         CLUS:0000,ATTR:0004,TYPE:42
#         CLUS:0000,ATTR:0005,TYPE:42
#         CLUS:0000,ATTR:0006,TYPE:42
#         CLUS:0000,ATTR:0007,TYPE:30
#         CLUS:0000,ATTR:0010,TYPE:42
#         CLUS:0000,ATTR:0013,TYPE:18
#         ENDDISCATTR

        if respState:
            
            # Determine whether or not all attributes have been found
            # DISCATTR line will finish with '01' if more to be found
            temp = respValue.split(',')
            exitCode = temp[len(temp)-1]
            
            if exitCode == '01':
                allFound = False
            else:
                allFound = True
                respCode = zcl.statusCodes['SUCCESS']           
            
            # Pop all the attribute lines from the rxQueue
            respTempList = []
            resp=rxQueue.get()
            while not resp.startswith('ENDDISCATTR') and not resp.startswith('ENDDISCMATTR'):
                #print(resp)
                respTempList.append(resp)
                resp=rxQueue.get()  
                
            # Convert the strings into value,type tuples
            # Find the highest attrId
            lastAttr='0000'
            for i in range(0,len(respTempList)):
                temp = respTempList[i].split(',')
                attrId = temp[1][5:]
                attrType = temp[2][5:]
                respData.append((attrId,attrType))
                if int(attrId,16) > int(lastAttr,16):
                    lastAttr=attrId
                
            # Create a start index for the next batch of attributes
            # Add 1 to the lastAttr value
            startAttr= '%04x' % (int(lastAttr,16)+1)

        else:
            respData=respValue
            break

    return respState, respCode, respData
def getAttribute(myNodeId, myEP, myClust, myAttr, myClusterType):
    """ Returns the attribute value and the respstate
        myClusterType should be 'client' or 'server'
        
    """
    # Build the AT command - one of 4.
    # Server & manufacturer Specific
    # Server & generic
    # Client & manufacturer specific
    # Client & generic 
    sendMode = '0'
    if myClust in zcl.BG_Clusters:
        if myClusterType == 'server':
            myMsg = 'AT+READMATR:{0},{1},{2},{3},{4},{5}'.format(myNodeId,myEP,sendMode,MANUFACTURER_ID,myClust,myAttr)
        else:
            myMsg = 'AT+READMCATR:{0},{1},{2},{3},{4},{5}'.format(myNodeId,myEP,sendMode,MANUFACTURER_ID,myClust,myAttr)
        # RESPMATTR:AB7E,05,1039,FD00,0000,00,00
        expectedResponse=['RESPMATTR:{0},{1},{2},{3},{4},(..)'.format(myNodeId,
                                                                      myEP,
                                                                      MANUFACTURER_ID,
                                                                      myClust,
                                                                      myAttr)]
    else:
        if myClusterType == 'server':
            myMsg = 'AT+READATR:{0},{1},{2},{3},{4}'.format(myNodeId,myEP,sendMode,myClust,myAttr)             
        else:
            myMsg = 'AT+READCATR:{0},{1},{2},{3},{4}'.format(myNodeId,myEP,sendMode,myClust,myAttr)
            
        # Typical responses.  Note temperatureMeasurement cluster has a different response..
        # TEMPERATURE:AEC3,09,0000,00,07E9
        # RESPATTR:7897,05,0201,0000,00,07E9
        
        if myClust == '0402':    
            expectedResponse = ['TEMPERATURE:{0},{1},{2},(..)'.format(myNodeId,myEP,myAttr)]
        else:
            expectedResponse = ['RESPATTR:{0},{1},{2},{3},(..)'.format(myNodeId,myEP,myClust,myAttr)]

    respState, respCode, respValue = sendCommand(myMsg, expectedResponse)
    
    if respState and respCode==zcl.statusCodes['SUCCESS']:
        respTemp = respValue.split(',')
        respTemp = respTemp[len(respTemp)-1]
    else:
        respTemp = respValue
        
    return respState, respCode, respTemp
def setAttribute(myNodeId, myEP, myClust, myClusterType, myAttr, myAttrType,myAttrVal):
    """
    """
    sendMode='0'
    #Only currently support writing of sever type attributes
    assert myClusterType=='server'
    
    if myClust in zcl.BG_Clusters:
        myMsg = 'AT+WRITEMATR:{0},{1},{2},{3},{4},{5},{6},{7}'.format(myNodeId,myEP,sendMode,MANUFACTURER_ID,myClust,myAttr,myAttrType,myAttrVal)
        expectedResponse = ['WRITEMATTR:{0},{1},{2},{3},,(..)'.format(myNodeId,myEP,MANUFACTURER_ID,myClust)]
    else:
        myMsg = 'AT+WRITEATR:{0},{1},{2},{3},{4},{5},{6}'.format(myNodeId,myEP,sendMode,myClust,myAttr,myAttrType,myAttrVal)
        expectedResponse = ['WRITEATTR:{0},{1},{2},{3},(..)'.format(myNodeId,myEP,myClust,myAttr)]
    
    respState,respCode,respValue = sendCommand(myMsg, expectedResponse)

    if respState and respCode==zcl.statusCodes['SUCCESS']:
        respTemp = respValue.split(',')
        respTemp = respTemp[len(respTemp)-1]
    else:
        respTemp = respValue
        
    return respState, respCode, respTemp
                        
def getAttributeReporting(myNodeId, myEpId, myClustId, myDirection, myAttr):
    """ Get the reporting intervals (if any) set for the given attribute
    """
    if myClustId in zcl.BG_Clusters:
        myManufacturer = MANUFACTURER_ID        
        if myDirection == 'server':
            # AT+READMRPTCFG:2537,05,0,1039,FC00,0,0000
            sendMode = 0 # 0=Send command directly (rather than to a group)
            reportingDirection = '0' # 0=Reported, 1=Received
            myMsg = 'AT+READMRPTCFG:{0},{1},{2},{3},{4},{5},{6}'.format(myNodeId,
                                                                        myEpId,
                                                                        sendMode,
                                                                        myManufacturer,
                                                                        myClustId,
                                                                        reportingDirection,
                                                                        myAttr)
            repDir='00'
        else:
            # at+rawzcl:ca0f,02,fc00,0C 3910 00 08 010200
            zclFrameType = '0C' # serv to client and manuf specific.
            zclSequence = '00'  
            zclCmd = '08'       # 0x08 = Read reporting configuration 
            zclPayload = '01' + byteSwap(myAttr)   # Payload = direction + attribute ID, direction 0x01 = attribute received
            rawZcl = zclFrameType + byteSwap(MANUFACTURER_ID) + zclSequence + zclCmd + zclPayload
            myMsg = 'AT+RAWZCL:{0},{1},{2},{3}'.format(myNodeId, myEpId, myClustId,rawZcl)
            repDir='01'
        
        # Typical response:
        # READRPTCFGRSP:D198,05,0201,00,00,0000,29,FFFF,FFFF,8000
        # READMRPTCFGRSP:F14D,05,1039,FC00,00,00,0002,29,FFFF,FFFF,8000
        # READMRPTCFGRSP:7897,05,1039,FC00,00,0,0000,18,FFFF,FFFF
        expectedResponse = ['READMRPTCFGRSP:{0},{1},{2},{3},(..),{4},{5}'.format(myNodeId,
                                                                                myEpId,
                                                                                myManufacturer,
                                                                                myClustId,
                                                                                repDir,
                                                                                myAttr)]
    else:
        if myDirection == 'server':
            sendMode = 0 # 0 = send command directly (rather than to a group)
            myMsg = 'AT+READRPTCFG:{0},{1},{2},{3},{4},{5}'.format(myNodeId, myEpId, sendMode, myClustId, '0', myAttr)
        else:
            zclFrameType = '08' # 0x08 = server to client 0x00=client to server
            zclSequence = '00'  
            zclCmd = '08'       # 0x08 = Read reporting configuration 
            zclPayload = '00' + byteSwap(myAttr)   # Payload = direction + attribute ID, direction 0x00 = attribute reported
            rawZcl = zclFrameType + zclSequence + zclCmd + zclPayload
            myMsg = 'AT+RAWZCL:{0},{1},{2},{3}'.format(myNodeId, myEpId, myClustId,rawZcl)
        
        # Typical response:
        # READRPTCFGRSP:D198,05,0201,00,00,0000,29,FFFF,FFFF,8000
        # READMRPTCFGRSP:F14D,05,1039,FC00,00,00,0002,29,FFFF,FFFF,8000        
        repDir='00'
        expectedResponse = ['READRPTCFGRSP:{0},{1},{2},(..),{3},{4}'.format(myNodeId,
                                                                           myEpId,
                                                                           myClustId,
                                                                           repDir,
                                                                           myAttr)] 
    
    #time.sleep(0.5)
    # DFTREP:7112,09,0000,08,82 << DFT for "Unsupported General Command". 08 is a command id.
    #defaultResponse= "DFTREP:{},{},{},08".format(myNodeId,myEpId,myClustId)
    
    # READRPTCFGRSP:CA0F,02,0000,86,00,0000 < AlertMe device response for reporting not supported

    respState, respCode, respValue = sendCommand(myMsg, expectedResponse)
    
    if respState and respCode==zcl.statusCodes['SUCCESS']:
        resp = respValue.split(',')
        if myClustId in zcl.BG_Clusters:
            minRepVal = (resp[8] if len(resp)>=10 else '')
            maxRepVal = (resp[9] if len(resp)>=10 else '')
            changeRepVal = (resp[10] if (len(resp)==11) else '')
        else:
            minRepVal = (resp[7] if len(resp)>=9 else '')
            maxRepVal = (resp[8] if len(resp)>=9 else '')
            changeRepVal = (resp[9] if (len(resp)==10) else '')
        resp = '{0},{1},{2}'.format(minRepVal,maxRepVal,changeRepVal)
    else:
        resp = respValue
    return  respState,respCode,resp
def setAttributeReporting(myNodeId,myEp,myClustId,myAttrId,minRep,maxRep,changeRep):
    """  Set attribute reporting
    
    """
    sendMode = 0  # Send command to specific device
    direction = 0 # Send report (c.f. received report)
    
    _,_,attrType = zcl.getAttributeNameAndId(myClustId, myAttrId)
    
    if myClustId in zcl.BG_Clusters:
        cmd = "AT+CFGMRPT:{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}".format(myNodeId,
                                                                              myEp,
                                                                              sendMode,
                                                                              MANUFACTURER_ID,
                                                                              myClustId,
                                                                              direction,
                                                                              myAttrId,
                                                                              attrType,
                                                                              minRep,
                                                                              maxRep,
                                                                              changeRep)
    else:
        # AT+CFGRPT:<Address>,<EP>,<SendMode>, <ClusterID>,<Direction>,<AttrID>,[<DataType>,<MinimumReportingInterval>, <MaximumReportingInterval>, <ReportableChange>][<Timeout>]    
        cmd = "AT+CFGRPT:{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}".format(myNodeId,
                                                                         myEp,
                                                                         sendMode,
                                                                         myClustId,
                                                                         direction,
                                                                         myAttrId,
                                                                         attrType,
                                                                         minRep,
                                                                         maxRep,
                                                                         changeRep)
        
    # CFGRPTRSP:5ACF,05,0201,00
    # CFGMRPTRSP:2263,05,1039,FC00,00
    expectedResponse = ['CFGRPTRSP:{0},{1},{2},(..)'.format(myNodeId,myEp,myClustId),
                        'CFGMRPTRSP:{0},{1},{2},{3},(..)'.format(myNodeId,myEp,MANUFACTURER_ID,myClustId)]
    
    respState, respCode, respValue = sendCommand(cmd, expectedResponse)
    if respState==False and respCode==zcl.statusCodes['SUCCESS']:
        print('ERROR: Setting reporting configuration failed. ',respValue)
        exit()
    return respState,respCode,respValue

def getBindings(myNodeId):
    """  Retrieve binding table for the given nodeId
    
    """
    msg = ''
    expectedResponse = ['BTable:{0},(..)'.format(myNodeId)]
    
    finished = False
    tableRow=0
    rows=[]
    headersDone = False
    
    while not finished:
        
        # Typical Response.
        # BTable:0000,00
        # Length:03
        # No. | SrcAddr | SrcEP | ClusterID | DstAddr | DstEP
        # 0. | 000D6F000059474E | 01 | DEAD |1234567887654321 | 12
        # 1. | 000D6F000059474E | 01 | DEAD |E012345678876543 | E0
        # 2. | 000D6F000059474E | 01 | DEAD | ABCD 
        # ACK:01    
        
        # Read a page of the table
        hexIndex = '%02x' % tableRow
        msg = "AT+BTABLE:{},{}".format(hexIndex, myNodeId)
        respState, respCode, respValue = sendCommand(msg, expectedResponse)
        if (not respState) or (respCode!=zcl.statusCodes['SUCCESS']):
            print("Error with binding table read : ",respValue)
            exit()
        header1 = respValue
        
        # Extract the table length    
        header2 = rxQueue.get()
        if not header2.startswith('Length'):
            print("Error with binding table read - expected 'Length' ",header2)
            exit()
        tableLength = int(header2.split(':')[1],16)
        
        # Read the table header row (only if there are more than zero bindings)
        if tableLength>0:
            header3 = rxQueue.get()
            if not header3.startswith('No.'):
                print("Error with binding table read - Expected 'No.' ", header3)
                exit()
        else:
            header3 = None
        
        if not headersDone:
            rows.append(header1)
            rows.append(header2)
            rows.append(header3)
            headersDone = True
        
        if tableLength == 0:
            finished = True
        else:
            # Read the binding rows            
            pageRow=0
            while pageRow<3 and tableRow<tableLength:
                row=rxQueue.get()
                if int(row.split('|')[0].strip('. '))!=tableRow:
                    print("Error with binding table read - Row number mismatch.")
                    exit()
                tableRow+=1
                pageRow+=1
                #print(row)
                rows.append(row)
                
        if tableRow>=tableLength:
            finished = True
                
    return respState, respCode, rows
def setBinding(myNodeId, mySrcAddr, mySrcEp, myCluster, myDstAddr, myDstEp, maxAttempts=3):
    """
        AT+BIND:<address>,<type>,<SrcAddress>,<SrcEP>,<ClusterID>,<DstAddress>
    """
    myType = '3' # 3=Unicast
    msg = 'AT+BIND:{0},{1},{2},{3},{4},{5},{6}'.format(myNodeId, myType, mySrcAddr, mySrcEp, myCluster, myDstAddr, myDstEp)
    expectedResponse = ['Bind:{0},(..)'.format(myNodeId)]
    print(msg, '\n')
    respState, respCode, respValue = sendCommand(msg,expectedResponse, maxAttempts) 
    if respState and respCode==zcl.statusCodes['SUCCESS']:
        respValue = respValue.replace('\r\n',',').split(',')
    return respState, respCode, respValue
def setUnBind(myNodeId, mySrcAddr, mySrcEp, myCluster, myDstAddr, myDstEp, maxAttempts=3):
    """
        AT+BIND:<address>,<type>,<SrcAddress>,<SrcEP>,<ClusterID>,<DstAddress>
    """
    #print("partial implementation")
    #raise junkError
    myType = '3' # 3=Unicast
    msg = 'AT+UNBIND:{0},{1},{2},{3},{4},{5},{6}'.format(myNodeId, myType, mySrcAddr, mySrcEp, myCluster, myDstAddr, myDstEp)
    expectedResponse = ['Unbind:{0},(..)'.format(myNodeId)]
    respState, respCode,respValue = sendCommand(msg,expectedResponse, maxAttempts)
    if respState and respCode==zcl.statusCodes['SUCCESS']:
        respValue = respValue.replace('\r\n',',').split(',')
    return respState, respCode, respValue
def fastPollStart(nodeId, timeout=630):
    """
    "Set up a binding first in order to start receiving the check-in messages
    
    1. Send an AT+FPSET (On) - to setup the checkIn Response
    2. Wait for a checkIn.  Fast poll will now be active
    3. Do whatever interactions are required
    4. AT+FPSET (off)
    
    """
    fpStartMsg = 'AT+FPSET:01,0FFF\r\n'
    checkInMsg = ['CHECKIN:{}'.format(nodeId)]

    print('\nAttempting to start Fast Poll...')
    
    startTime = time.time()
    while time.time() < startTime+timeout:
        respState, _ , respValue = sendCommand(fpStartMsg,checkInMsg)
        if respState:
            print('Fast Poll Started...', respValue)
            print()
            return 0
    
    print('CheckIn failed : ',respValue)
    exit()    
            
    return 0
def fastPollStop():
    fpStopMsg = 'AT+FPSET:00,001C\r\n'
    expectedResponse = ['OK']
    print('Stopping Fast Poll...\r\n')
    respState,respCode,respValue = sendCommand(fpStopMsg,expectedResponse)
    return respState,respCode,respValue
def onOff(myNodeID, myEp, mySendMode, myState):
    """ Send the AT+RONOFF message to switch node on or off
    
    """
    #AT+RONOFF:F567,09,0,0
    myMsg = 'AT+RONOFF:{0},{1},{2},{3}'.format(myNodeID,myEp,mySendMode,myState)
    expectedResponse = ['OK']
    respState,respCode,respValue = sendCommand(myMsg,expectedResponse)
    return respState,respCode,respValue
def moveToLevel(myNodeId, myEpId, myLevel='FF', myDuration=0):
    """
    AT+LCMVTOLEV:19EA,01,0,1,1A,0001
    DFTREP:19EA,01,0008,04,00
    """
    sendMode=0
    onOff = 1
    transitionDuration = '{:04x}'.format(myDuration*10)
    myMsg = 'AT+LCMVTOLEV:{},{},{},{},{},{}'.format(myNodeId,myEpId,sendMode,onOff,myLevel,transitionDuration)
    #expectedResponses = ["DFTREP:{},{},{},{},(..)".format(myNodeId,myEpId,'0008',onOff)]
    expectedResponses = ["DFTREP:{},{},{},(..)".format(myNodeId,myEpId,'0008')]
    print(myMsg)
    respState,respCode,respValue = sendCommand(myMsg, expectedResponses)
    return respState,respCode,respValue

""" Coordinator getter/setter methods """
def setAtr(clustId,attrId,attrVal):
    """  Used to set attributes on coordinator (TG stick)
    
    """
    myMsg='AT+SETATR:{0},{1},{2}'.format(clustId,attrId,attrVal)
    expectedResponse=['OK']
    respState,respCode,respValue = sendCommand(myMsg, expectedResponse)
    
    if respState:
        respTemp = respValue.split(',')
        respTemp = respTemp[len(respTemp)-1]
    else:
        respTemp = respValue
    return respState,respCode,respTemp           
def getAtr(clustId,attrId):
    """ USed to get attributes on controller (TG stick)
    
    """
    myMsg='AT+GETATR:{0},{1}'.format(clustId,attrId)
    # ATTR:1DBEFCAE
    expectedResponse=['ATTR:']
    
    respState,respCode,respValue = sendCommand(myMsg, expectedResponse)
    
    if respState:
        respTemp = respValue.split(':')
        respTemp = respTemp[len(respTemp)-1]
    else:
        respTemp = respValue
    return respState,respCode,respTemp     
def setTime(attrVal):
    """  Used to set attributes on controller (TG stick)
    
    """
    myMsg='AT+SETTIME:{0}'.format(attrVal)
    expectedResponse=['OK']
    respState,respCode,respValue = sendCommand(myMsg, expectedResponse)
    
    if respState:
        respTemp = respValue.split(',')
        respTemp = respTemp[len(respTemp)-1]
    else:
        respTemp = respValue
    return respState,respCode,respTemp           
def getTime():
    """ Used to get Time attribute on controller (TG stick)
    
    """
    myMsg='AT+GETTIME'
    # TIME:1DBEFCAE
    expectedResponse=['TIME:']
    
    respState,respCode,respValue = sendCommand(myMsg, expectedResponse)
    
    if respState:
        respTemp = respValue.split(',')
        respTemp = respTemp[len(respTemp)-1]
    else:
        respTemp = respValue
    return respState,respCode,respTemp  
def setTimerRD():
    """  Used to set attributes on controller (TG stick)
    
    """
    myMsg='AT+TIMERD'
    expectedResponse=['OK']
    respState,respCode,respValue = sendCommand(myMsg, expectedResponse)
    
    if respState:
        respTemp = respValue.split(',')
        respTemp = respTemp[len(respTemp)-1]
    else:
        respTemp = respValue
    return respState,respCode,respTemp
def cchange(chan):
    """ Used to change channel of controller
    """
    myMsg='AT+CCHANGE:{}'.format(chan)
    expectedResponse=['OK']
    respState,respCode,respValue = sendCommand(myMsg, expectedResponse)
    
    # Wait in a loop for 30s here to confirm channel has changed
    for _ in range(0,6):
        time.sleep(5)
        myMsg='AT+N'
        # +N=COO,12,8,AC4E,866C1D6C7C8EA2C8
        expectedResponse=['\+N=COO']
        respState,respCode,respValue = sendCommand(myMsg, expectedResponse)
        if respState:
            respTemp = respValue.split(',')
            respTemp = int(respTemp[1])
            if respTemp == chan:
                # Channel has changed
                return respState,respCode,respValue
        else:
            return respState,respCode,respValue
    
    assert respState!=None 
    return
def cswitch(chan):
    """ Used to silently change channel of controller without
        informing child nodes.
        
    """
    myMsg='AT+CSWITCH:{}'.format(chan)
    expectedResponse=['OK']
    respState,respCode,respValue = sendCommand(myMsg, expectedResponse)
    
    # Wait in a loop for 30s here to confirm channel has changed
    for _ in range(0,6):
        time.sleep(5)
        myMsg='AT+N'
        # +N=COO,12,8,AC4E,866C1D6C7C8EA2C8
        expectedResponse=['+N=COO']
        respState,respCode,respValue = sendCommand(myMsg, expectedResponse)
        if respState:
            respTemp = respValue.split(',')
            respTemp = int(respTemp[1])
            if respTemp == chan:
                # Channel has changed
                return respState,respCode,respValue
        else:
            return respState,respCode,respValue
    
    assert respState!=None 
    return
def pjoin(devTypeList):
    """ Put coordinator into pjoin until wanted device type joins
        then exit pjoin mode.
        Return the node id of the joined device
        If more than one device joins only first device of the wanted type
        is returned.
        
        Timeout after timeout seconds
        
    """
    myMsg='AT+PJOIN'
    # SED:001E5E0902099514,0030
    
    allFound=False
    timeout = time.time() + 60
    deviceMsgs = []
    
    txQueue.put(myMsg)
    while not allFound and time.time() < timeout:
        while not rxQueue.empty():
            myMsg=rxQueue.get()
            for myType in devTypeList:
                if myMsg.startswith(myType):
                    deviceMsgs.append(myMsg)
                    devTypeList.remove(myType)
                    if devTypeList == []:
                        allFound=True
                        respState=True
                        respValue=deviceMsgs
                    
    if not allFound:
        respState=False
        respValue='One or more devices failed to join'

    respCode = None
    return respState,respCode,respValue
def dassr(nodeId):
    """ Send a network leave command to the given nodeId
    
    """
    myMsg='AT+DASSR:{}'.format(nodeId)
    expectedResponse=['OK']
    respState, respCode, respValue = sendCommand(myMsg, expectedResponse)    
    return respState,respCode,respValue    

""" Thermostat Methods """
def setWeeklySchedule(myNodeId,myEp,myCluster,myDayBitmap,myPayload, boolStandaloneMode = False):
    """ Send a setWeeklySchedule message to the node.

    """    
    frameType='01'        # 0x01 = Command specific to cluster
    seqNumber='00'
    commandId='01'        # 0x01 = setWeeklySchedule
    
    numberOfEvents='06'
    modeForSequence='01'  # 0x01 = Heat Mode   
    
    header="{0}{1}{2}{3}{4}{5}".format(frameType,seqNumber,commandId,numberOfEvents,myDayBitmap,modeForSequence)
    
    myMsg = 'AT+RAWZCL:{0},{1},{2},{3}{4}'.format(myNodeId,myEp,myCluster,header,myPayload)
    expectedResponse=['CWSCHEDULE:{0},{1}'.format(myNodeId,myEp)]
    if boolStandaloneMode: expectedResponse = ['OK']
    respState,respCode,respValue = sendCommand(myMsg,expectedResponse)
    if respState and respCode==zcl.statusCodes['SUCCESS']:
        respValue = respValue.split(',')[5:]    
    
    return respState,respCode,respValue
def getWeeklySchedule(myNodeId,myEp,myCluster,myDayBitmap):
    """ Get the schedule for the given day.
    
    """
    frameType = '01'     # 0x01 = Command specific to cluster
    seqNumber = '00'
    commandId = '02'     # 0x01 = getWeeklySchedule    
    modeForSequence='01' # 0x01 = Heat
    
    payload = "{0}{1}{2}{3}{4}".format(frameType,seqNumber,commandId,
                                       myDayBitmap,modeForSequence)
    myMsg = 'AT+RAWZCL:{0},{1},{2},{3}'.format(myNodeId,myEp,myCluster,payload)
    
    # at+rawzcl:FDDF,05,0201,0100020401
    # CWSCHEDULE:FDDF,05,06,04,01,0186,07D0,01FE,0064,02D0,0064,0348,0064,03DE,07D0,0528,0064
    expectedResponse = ['CWSCHEDULE:{0},{1},06,{2},01'.format(myNodeId,myEp,myDayBitmap)]
    respState,respCode,respValue = sendCommand(myMsg, expectedResponse)
    
    if respState and respCode==zcl.statusCodes['SUCCESS']:
        respValue = respValue.split(',')[5:]
    
    return respState,respCode,respValue
def setMode(myNodeId,myEp,myMode,myEpType,mySetpointFloat=None,myDuration=1):
    """ Sets the appropriate attributes in the thermostat cluster to achieve the required mode.
        Setpoint should be a float in the range 5-32.
        Setpoint ignored if endpoint is a hot water controller.
    
    """
    respState = False
    respValue = ''
    myCluster='0201'
    
    allowedModes = ['AUTO','MANUAL','OFF','BOOST']
    
    # Check parameters
    if not myMode in allowedModes:
        respState=False
        respValue='ERROR: {} is not an allowed mode switch'.format(myMode)
        return respState,None,respValue
    
    if myDuration not in range(0,7):
        respState=False
        respValue='ERROR: Boost Duration must be in the range 1-6. Or 0 for 2min test Boost'
        return respState,None,respValue
    else:
        # Create a hex duration value in minutes
        if myDuration==0:
            durationHex="{:04x}".format(2)
        else:
            durationHex="{:04x}".format(myDuration*60)        
    
    _,clustName = zcl.getClusterNameAndId(myCluster)
    sendMode='0'    
    
    if myMode=='OFF':
        # systemMode=0x00, TSH=0x00
        # at+writeatr:nodeId,ep,mode,clust,attrid,type1,val1,attr2,type2,val2
        attrs = [('systemMode','00'),('temperatureSetpointHold','00')]
        attrString = buildCombinedAttributeString(attrs, clustName)
        
        msg = "at+writeatr:{0},{1},{2},{3}{4}".format(myNodeId,myEp,sendMode,myCluster,attrString)
        expectedResponse = ['WRITEATTR:{0},{1},{2},,00'.format(myNodeId,myEp,myCluster)]
        respState,respCode,respValue = sendCommand(msg, expectedResponse)
        
    elif myMode=='AUTO':
        #systemMode=0x04, setpointHold=0x00
        attrs = [('systemMode','04'),('temperatureSetpointHold','00')]
        attrString = buildCombinedAttributeString(attrs, clustName)
        
        msg = "at+writeatr:{0},{1},{2},{3}{4}".format(myNodeId,myEp,sendMode,myCluster,attrString)
        expectedResponse = ['WRITEATTR:{0},{1},{2},,00'.format(myNodeId,myEp,myCluster)]
        respState,respCode,respValue = sendCommand(msg, expectedResponse)
        
    elif myMode=='MANUAL':
        # SLT3 sets 20'C when switching to manual, but we allow other setpoint value to be set
        # if it's provided.
        if mySetpointFloat==None:
            mySetpointFloat=MANUAL_DEFAULT
        else:
            respState,respValue = checkValidSetpoint(mySetpointFloat)
            if respState==False:
                print(respValue)
                return respState,None,respValue
            
        setpointHex = "{:04x}".format(int(mySetpointFloat*100))
        
        # systemMode=0x04, setpointHold=0x01 (setpointHoldDuration automatically set to 0xffff)
        # Also setting Occupied Heating Setpoint to emulate SLT3 behaviour
        
        # For heat set all three attrs
        if myEpType=='HEAT':
            attrs = [('systemMode','04'),('temperatureSetpointHold','01'),('occupiedHeatingSetpoint',setpointHex)]
        # For water we only set 2 attrs
        else:
            attrs = [('systemMode','04'),('temperatureSetpointHold','01')]
        attrString = buildCombinedAttributeString(attrs, clustName)
        
        msg = "at+writeatr:{0},{1},{2},{3}{4}".format(myNodeId,myEp,sendMode,myCluster,attrString)
        expectedResponse = ['WRITEATTR:{0},{1},{2},,00'.format(myNodeId,myEp,myCluster)]
        respState,respCode,respValue = sendCommand(msg, expectedResponse)              

    elif myMode=='BOOST':
        # If no setpoint given for BOOST then use the 22'C default.
        if myEpType=='HEAT' and mySetpointFloat==None:
            mySetpointFloat=BOOST_DEFAULT
        else:
            respState,respValue = checkValidSetpoint(mySetpointFloat)
            if respState==False:
                print(respValue)
                return respState,None,respValue    
            
        setpointHex = "{:04x}".format(int(mySetpointFloat*100))
        
        # systemMode=0x05, setpointHold=0x01, setpointHoldDuration=0x????, occupiedHeatingSetpoint=0x????
        if myEpType=='HEAT':
            attrs = [('systemMode','05'),('temperatureSetpointHold','01'),('temperatureSetpointHoldDuration',durationHex),
                     ('occupiedHeatingSetpoint',setpointHex)]
        else:
            attrs = [('systemMode','05'),('temperatureSetpointHold','01'),('temperatureSetpointHoldDuration',durationHex)]
            
        attrString = buildCombinedAttributeString(attrs, clustName)
        msg = "at+writeatr:{0},{1},{2},{3}{4}".format(myNodeId,myEp,sendMode,myCluster,attrString)
        expectedResponse = ['WRITEATTR:{0},{1},{2},,00'.format(myNodeId,myEp,myCluster)]
        respState,respCode,respValue = sendCommand(msg, expectedResponse)      
    
    return respState,respCode,respValue
def setSetpoint(myNodeId,myEp,mySetpointFloat=1):
    """ Set the thermostat Setpoint to the given value
    
    """
    respState,respValue=checkValidSetpoint(mySetpointFloat)
    if respState==False:
        print(respValue)
        return respState,None,respValue
        
    # at+writeatr:nodeId,ep,mode,clust,attrid,type1,val1,attr2,type2,val2
    sendmode='0'    # Send directly
    clustId='0201'  # Thermostat Cluster
    attrId,_,attrType=zcl.getAttributeNameAndId(clustId, 'occupiedHeatingSetpoint')
    attrVal="{:04x}".format(int(mySetpointFloat*100))

    msg="at+writeatr:{0},{1},{2},{3},{4},{5},{6}".format(myNodeId,myEp,sendmode,clustId,attrId,attrType,attrVal)
    expectedResponse = ['WRITEATTR:{0},{1},{2},,00'.format(myNodeId,myEp,clustId)]
    respState,respCode,respValue = sendCommand(msg, expectedResponse)
    
    return respState,respCode,respValue
def checkValidSetpoint(mySetpoint):
    """ Checks if a setpoint is in the valid range
        Returns True/False
        
        Setpoints can be in the following range:
        
        5.0 < setpoint < 32.0, or
        setpoint==1  (special case for frost protection)
        
    """
    errValue="ERROR: Setpoint must be in the range 5-32'C or 1'C (Frost Protection)"
    if mySetpoint==1 or (mySetpoint>=5 and mySetpoint<=32):
        return True, None
    else:
        return False,errValue

""" Queue Listener Methods (run as threads)"""
""" Custom Exception """
class junkError(Exception):
    def __init__(self,value):
        self.value=value
    def __str__(self, *args, **kwargs):
        return Exception.__str__(self, *args, **kwargs)

def startAttributeListener(printStatus=False):
    """
    """
    # Start the serial port handler thread    
    thread = threading.Thread(target=attributeListener, args=())
    thread.daemon = True # This kills the thread when main program exits
    thread.start()
    threadPool.append(thread)
    if printStatus: print('Attribute listener thread started.\n') 
    return 0
def attributeListener(timeToLive=180):
    """ Listen for wanted attribute reports and save them to REDIS cache
         
    """
    # Read the rxQueue
    while not stopThread.isSet():
        try:
            # Timeout required in order to allow thread to exit if stopThread is set.
            respVal = listenerQueue.get(timeout=1)       
            # REPORTATTR:FD51,05,0201,0000,29,089C
            # REPORTMATTR:2263,05,1039,FC00,0001,21,0000
            # TEMPERATURE:AEC3,09,0000,00,07E9
            # CWSCHEDULE:FDDF,05,06,04,01,0186,07D0,01FE,0064,02D0,0064,0348,0064,03DE,07D0,0528,0064
            # RESPATTR:0605,05,0000,0000,00,01
            # RESPMATTR:0605,05,1039,FD00,0031,00,02BC    
            if respVal.startswith(('TEMPERATURE','REPORTATTR','REPORTMATTR','CWSCHEDULE','RESPATTR','RESPMATTR')):
                resp = respVal.split(',')
                nodeId = resp[0].split(':')[1]
                epId = resp[1]
                if respVal.startswith('TEMPERATURE'):
                    attrId = resp[2]
                    attrVal = resp[4]
                elif respVal.startswith('REPORTMATTR'):
                    clustId = resp[3]
                    attrId = resp[4]
                    attrVal = resp[6]
                elif respVal.startswith('REPORTATTR'):
                    clustId = resp[2]
                    attrId = resp[3]
                    attrVal = resp[5]
                elif respVal.startswith('RESPATTR'):
                    clustId = resp[2]
                    attrId = resp[3]
                    attrVal = resp[5]
                elif respVal.startswith('RESPMATTR'):
                    clustId = resp[3]
                    attrId = resp[4]
                    attrVal = resp[6]
                elif respVal.startswith('CWSCHEDULE'):
                    clustId='0201'
                    attrId="sched{}".format(resp[3])  # In this case attrId is actually "sched" + the day of week bitmap
                    attrVal=''.join(resp[5:])
                
                # Check for BOOST or HOLIDAY before writing to REDIS
                #listenForSpecialModes(nodeId, epId, clustId, attrId, attrVal)
                # Write value to REDIS
                redisKey = "{0},{1},{2},{3}".format(nodeId,epId,clustId,attrId)
                r.set(redisKey,attrVal)
        except queue.Empty:
            pass
    print('Attribute listener thread exit')
    return 0
# def listenForSpecialModes(myNodeId,myEp,myClustId,myAttrId,myAttrVal):
#     """ Helper method for attribute listener.
#         
#         Used to deal with special cases where we need to detect changes in specific attributes.
#         
#         If BM signals a change to BOOST or HOLIDAY ACTIVE then we must read the following attributes
#         and stash them in REDIS directly before we update the mode in REDIS.  This means that when
#         the client reads REDIS and detects the mode change the previousMode attributes are already
#         set to the correct value and are ready to be read.
#         
#         previousHeatMode()
#         previousWaterMode()
#         previousHeatSetpoint()
#         
#         Note that REDIS will get updated twice.  Directly on this special attribute read method 
#         and again by the attribute listener (as all incoming messages are copied to the attribute
#         listener Queue for processing).
#         
#     """
#     # Capture a BOOST being set.
#     if myAttrId=='001C' and myClustId=='0201':
#         redisVal = getRedis(myNodeId, myEp, myClustId, myAttrId)
#         if redisVal!=None:
#             if redisVal!='05' and myAttrVal=='05':
#                 readPreviousModeAttributes(myNodeId)
#     
#     # Capture a HOLIDAY becoming active.
#     if myAttrId=='0021' and myClustId=='FD00':
#         redisVal = getRedis(myNodeId, myEp, myClustId, myAttrId)        
#         if redisVal!=None:
#             if redisVal=='00' and myAttrVal=='01':
#                 readPreviousModeAttributes(myNodeId)
#     
#     return 0
# def getRedis(myNodeId,myEp,myClustId,myAttrId):
#     """ Retrieve an entry from REDIS
#     
#     """
#     redisKey="{},{},{},{}".format(myNodeId,myEp,myClustId,myAttrId)
#     attrVal = r.get(redisKey)
#     if attrVal == None:
#         attrVal=attrVal
#         #raise queueListenerError('LISTENER ERROR: No REDIS entry for attribute. {}'.format(myAttrId))
#     else:
#         attrVal = attrVal.decode()    
#     return attrVal
# def readPreviousModeAttributes(myNodeId):
#     """ Read previousMode and previousSetpoint attributes
#         These are always on ep='05'
#     """
#     epId='05'
#     clustId='FD00'
#     
#     attrList=['previousHeatMode','previousWaterMode','previousHeatSetpoint']
#     
#     for attr in attrList:
#         attrId,_,_=zcl.getAttributeNameAndId('BG Cluster', attr)
#         respState,respVal = getAttribute(myNodeId, epId, clustId, attrId, 'server')
#         if not respState:
#             raise queueListenerError('LISTENER ERROR: ZB Attribute read failed. {}'.format(respVal))
#         
#         # Write the value to the REDIS cache
#         redisKey="{},{},{},{}".format(myNodeId,epId,clustId,attrId)
#         r.set(respVal)
#         
#         # DEBUG SECTION
#         print('********* PREVIOUS MODE ATTRIBUTES READ')
#         print(''.format(redisKey,respVal))
#         # \DEBUG SECTION
#         
#     return

""" OTA AT Command Methods """
def imageNotify(myNodeId,myEp,myManufCode,mySendMode='0',myPayloadType='03',
                myQueryJitter='64',myImageType='FFFF',myFileVersion='FFFFFFFF'):
    """ Send imageNotify message
    
        Defaults are:
        
        sendMode=0                # Send directly to node (not broadcast)
        payloadType = '03'        # 0x03 = jitter, manuf code, image type and new file version included
        queryJitter = '64'
        imageType = 'FFFF'        # 0xFFFF = All image types
        fileVersion = 'FFFFFFFF'  # 0xFFFFFFFF = All file versions
    
        timeout = 700             # More than 10mins to allow all devices a chance to 
                                  # send their next scheduled QNI
                                  # Backup for imageNotify not working.
    
    """
    expectedResponse = ['OK']
    msg = 'AT+IMGNOTIFY:{0},{1},{2},{3},{4},{5},{6},{7}'.format(myNodeId,
                                                                myEp,
                                                                mySendMode,
                                                                myPayloadType,
                                                                myQueryJitter,
                                                                myManufCode,
                                                                myImageType,
                                                                myFileVersion)
    
    respState, respCode, respValue = sendCommand(msg, expectedResponse)

    return respState,respCode,respValue
def queryNextImageResponse(myNodeId,myEp,myManufCode,myImgType,myFileVersion,myImgSize,mySeq,
                           mySendMode='0',myStatus='98'):
    """ Send queryNextImageResponse
        Sends either NO_IMAGE_AVAILABLE by default or valid new image data if provided
   
        Defaults:    
        
        sendMode = '0'       # 0 = Send directly (not broadcast)  
        statusCode = '98'    # 0x98 = NO_IMAGE_AVAILABLE, 0x00 = SUCESS
        
    """
    # Send NO_IMAGE_AVALIABLE
    if myStatus=='98':
        cmd = 'AT+QIMGRSP:{0},09,0,98,{1}'.format(myNodeId, mySeq)
        respState,respCode,respValue = sendCommand(cmd,['OK'])    
    
    # Send valid new image data
    else:   
        expectedResponse = ['OK']
        #QIMGRSP:<NodeID>,<EP>,<SendMode>, <Status>[,<ManufCode>,<ImgType>, <FileVersion>,<ImgSize>], <Seq>
        msg = 'AT+QIMGRSP:{0},{1},{2},{3},{4},{5},{6},{7},{8}'.format(myNodeId,
                                                                      myEp,
                                                                      mySendMode,
                                                                      myStatus,
                                                                      myManufCode,
                                                                      myImgType,
                                                                      myFileVersion,
                                                                      myImgSize,
                                                                      mySeq)
    
        respState, respCode, respValue = sendCommand(msg, expectedResponse)

    return respState, respCode, respValue

def imageBlockResponse(myNodeId,myEp,myManufCode,myImageType,myFileVersion,
                       myFileOffset,myDataSize,myPayload,mySeq,mySendMode='0',myStatus='00'):
    """ Send an OTA block
    
        Defaults:
        
        sendMode='0'     #  0 = Send directly (not broadcast)
        statusCode='00   #  0x00 = SUCCESS
    
    """
    expectedResponse = ['OK']
    msg = 'AT+IMGBRSP:{0},{1},{2},{3},{4},{5},{6},{7},{8}\r'.format(myNodeId,
                                                                    myEp,
                                                                    mySendMode,
                                                                    myStatus,
                                                                    myManufCode,
                                                                    myImageType,
                                                                    myFileVersion,
                                                                    myFileOffset,
                                                                    myDataSize,
                                                                    myPayload,
                                                                    mySeq)
    
    msg = bytes(msg,'ascii') + bytes.fromhex(myPayload) + bytes(',{}\r\n'.format(mySeq),'ascii')
    respState, respCode, respValue = sendCommand(msg, expectedResponse)
    return respState, respCode, respValue

def waitForQNI(myNodeId,myEp,timeout=700):
    """ QNIs get sent every 10mins so wait a bit more than that then timeout
        Returns: payload dict with the following fields:
        
        error:           timeout string
        manufCode:       manufacturing code in QNI
        imageType:       imageType in QNI
        currentVersion:  current FW version in QNI
        hardwareVersion: hardware version in QNI
        seqNum:          sequence number to use in response
    
    """
    # Wait for given message
    msgs = ['IMGQUERY:{0},{1}'.format(myNodeId,myEp)]
    msg = waitForMessage(msgs, timeout=timeout)
    
    # Parse the returned message
    payload = {'error':None,'manufCode':None,'imageType':None,'currentVersion':None,'hardwareVersion':None,'seqNum':None}
    if msg==None:
        # TIMEOUT
        payload['error']='TIMEOUT: waitForQNI timed out.'
        
    else:
        # IMGQUERY:<NodeID>,<EP>,<FieldControl>, <ManufCode>,<ImgType>,<CurrentFileVer> [,<HardwareVer>],<SequenceNumber>    
        qniResp = msg.split(',')

        payload['manufCode']=qniResp[3]
        payload['imageType']=qniResp[4]
        payload['currentVersion']=qniResp[5]
        
        # If no hardware version then seq number is in location 6
        if qniResp[2]=='00':
            payload['hardwareVersion']=None
            payload['seqNum'] = qniResp[6]
        # If hardware version then seq number if in location 7
        else:
            payload['hardwareVersion']=qniResp[6]
            payload['seqNum'] = qniResp[7]
    
    return payload


""" Abstracted Methods """
def getInitialData(nodeId, nodeEp, fastPoll=True, printStatus=False):
    """ Get PAN ID, Channel, EUIs, device type and MANUFACTURER_ID
        If device is a ZED then attempt to start fast polling.
        
    """
    
    params = {}
    params['nodeId']=nodeId
    
    # Retrieve and display network parameters 
    respState, respCode, network = getNetwork()
    if respState and respCode==zcl.statusCodes['SUCCESS']:
        if printStatus: print('Network Parameters: PanID={0}, Channel={1}'.format(network['panId'],network['channel']))
        params['panId']=network['panId']
        params['channel']=network['channel']
    else:
        print('Network error: {0}'.format(network))
    
    # Retrieve and display the IEEE addresses of the controller
    if fastPoll:
        respState,respCode,respValue = getEUI('0000','0000')
        if respState and respCode==zcl.statusCodes['SUCCESS']:
            controllerEUI = respValue        
            if printStatus: print('Controller EUI={}, nodeID=0000'.format(controllerEUI))
            params['controllerEUI']=controllerEUI
        else:
            print(respValue)
            exit()

    # Retrieve and display the device type.
    # If it's a sleepy end point then we may need to start fast polling
    respState, respCode, respValue = getNodeDesc(nodeId, nodeId)
    if respState and respCode==zcl.statusCodes['SUCCESS']:
        nodeType = respValue
        if printStatus: print('\r\nNode type = {}, Manufacturer Id = {}'.format(nodeType,MANUFACTURER_ID))
        params['nodeType']=nodeType
    else:
        print(respValue)
        exit()

    # Retrieve and display the IEEE addresses of the wanted node
    respState,respCode,respValue = getEUI(nodeId,nodeId)
    if respState and respCode==zcl.statusCodes['SUCCESS']:
        nodeEUI = respValue        
        params['nodeEUI']=nodeEUI
        if printStatus: print('Node EUI={0}, nodeID={1}'.format(nodeEUI,nodeId))
    else:
        print(respValue)
        exit()

    # Possibly start fast poll here if required.
    # If it's a sleepy end point the setup fast polling.
    # First set a binding so that checkIns are received
    # Then start fast polling
    if nodeType =='ZED' and fastPoll:
        # Setup binding
        # Wait for checkin - setup fast poll
        if printStatus: print('\nSetting poll control binding..')
        srcEp = nodeEp
        pollCluster = '0020'
        dstEp = '01'
        respState, respCode, respValue = setBinding(nodeId, nodeEUI, srcEp, pollCluster, controllerEUI, dstEp)
        if respState == False:
            print('Poll control cluster binding failed.')
            exit()
        elif respState == True and respCode != zcl.statusCodes['SUCCESS']:
            print('Poll control cluster binding failed')
            print(respValue)
            exit()
        
        # Read the longPollInterval and the checkInInterval prior to setting them for the getTelemetry
        print("\nSetting a short check-in interval and long poll interval to keep device awake for the attribute dump")

        # Get original long poll interval
        longPollIntId,_,_ = zcl.getAttributeNameAndId('Poll Control Cluster', 'longPollInterval')
        pollControlClustId,_=zcl.getClusterNameAndId("Poll Control Cluster")
        respState, respCode, respValue = getAttribute(nodeId, srcEp, pollControlClustId, longPollIntId, 'server')
        if respState==False:
            print("Get long poll interval failed")
            exit()
        params['longPollInt'] = respValue
        
        # Set a new shorter long poll interval
        myInterval = 5 # 5s
        myIntervalHex = "{:08X}".format(myInterval*4)
        respState,respCode,respValue = setLongPollInterval(nodeId, srcEp, myIntervalHex)
        if respState == False:
            print("Setting short long poll interval failed")
            exit()
        
        # Get original check-in interval
        checkInId,_,checkInType = zcl.getAttributeNameAndId("Poll Control Cluster", "checkInInterval")        
        respState, respCode, respValue = getAttribute(nodeId, srcEp, pollControlClustId, checkInId, 'server')
        if respState==False:
            print("Get check-in interval failed")
            exit()
        params['checkInInt'] = respValue        
        
        # Set a short check-in interval to keep device in fast poll for duration of this getTelemetry
        myInterval=30
        myIntervalHex="{:08X}".format(myInterval*4)
        respState,respCode,respValue = setAttribute(nodeId, srcEp, pollControlClustId, 'server', checkInId, checkInType, myIntervalHex)
        if respState == False:
            print("Setting short check-in interval failed")
            exit()
    
        print("\n*** Long poll interval and check-in interval have been modified to allow attribute dump")
        print("Original long poll interval = {}".format(params['longPollInt']))
        print("Original check-in interval  = {}\n".format(params['checkInInt']))
        
        print('Attempting to start fast poll...')
        fpStarted = fastPollStart(nodeId)
        if not fpStarted:
            print("Fast Poll failed to start")
            exit()
    
    return params

def getSimpleDesc(myNodeId,myEp):
    """
    """
    myMsg = 'AT+SIMPLEDESC:{},{},{}'.format(myNodeId,myNodeId,myEp)
    
    # SimpleDesc:7C62,00
    # EP:01
    # ProfileID:0104
    # DeviceID:0101v02
    # InCluster:0000,0004,0003,0006,0008,0005
    # OutCluster:0019
    expectedResponses=['SimpleDesc:{},(..)'.format(myNodeId)]
    respState, respCode, respValue = sendCommand(myMsg, expectedResponses)
    # Grab remaining lines from multi-line response
    respData={}
    respHeaders = ["EP","ProfileID","DeviceID","InCluster","OutCluster"]
    if respState and respCode==zcl.statusCodes['SUCCESS']:
        for h in respHeaders:
            line = rxQueue.get()
            if line.startswith(h):
                respData[h]=line
            else:
                respState=False
                return respState,respCode,respData
        
        # Parse the InCluster and OutCluster lines into lists
        
        for c in ["InCluster","OutCluster"]:
            clusters = respData[c]
            clusters = clusters.split(',')
            clusters[0] = clusters[0].split(":")[1]
            respData[c] = clusters
        
    else:
        respData = respValue
    return respState, respCode, respData
def getAllAttributes(myNodeId):
    """ Uses discoverEndpoints, discoverClusters, discoverAttributes and READATTR to query all
        attribute values on the device and print a summary.
        
        Also recovers any reporting intervals for the attribute
        
        Print the Endpoint list
        Print the Clusters
        Print the Attribute values and Reporting Intervals
        
    """
    nodeId = myNodeId
    # Retrieve and display the endpoints
    respState,respCode,endpoints = discEndpoints(nodeId)
    if respState and respCode==zcl.statusCodes['SUCCESS']:
        print("Endpoints: {0}".format(endpoints))
    else:
        print('Error finding endpoints')
        
    # Loop through each endpoint for clusters and attributes 
    for ep in endpoints:
        # Discover all clusters on this endpoint
        
        #respState,respCode,respValue = discClusters(nodeId,ep)
        respState,respCode,respValue = getSimpleDesc(nodeId,ep)        
        
        if respState and respCode==zcl.statusCodes['SUCCESS']:
            clusterList = buildClusterList(respValue)
        else:
            print('Problem with Cluster Discovery: ',respValue)
            exit()
        
        for clust in clusterList:
            clustId, clustName = zcl.getClusterNameAndId(clust[1])
            clustType = clust[0]          
            
            print("\nEndpoint={0}, Cluster={1},{2},{3}".format(ep, clust[1], clustName, clustType))

            respState,respCode,respValue = discAttrs(myNodeId,ep,clustId,clustType)
            if respState and respCode==zcl.statusCodes['SUCCESS']:
                for attr in respValue:
                    attrId = attr[0]
                    attrType = attr[1]
                    
                    # Get the attribute name from my library module
                    _, zclAttrName, zclAttrType = zcl.getAttributeNameAndId(clustId,attrId)
                    
                    # Get the attribute value
                    respState,respCode,respVal = getAttribute(myNodeId, ep, clustId, attrId, clustType)
                    if respState and respCode==zcl.statusCodes['SUCCESS']:
                        attrVal = respVal
                            
                        # Get the reporting intervals for the attribute
                        respState,respCode,attrReport = getAttributeReporting(myNodeId, ep, clustId, clustType, attrId)
#                         if not respState:
#                             attrReport = "Problem reading reporting config. {}".format(attrReport)
#                         if respState and respCode!=zcl.statusCodes['SUCCESS']:
#                             attrReport = "Problem reading reporting config. {}".format(zcl.lookupStatusCode(respCode))

                        if respState and respCode == zcl.statusCodes['SUCCESS']:
                            print("{0},{1},{2:32},{3:20},{4}".format(attrId, attrType, zclAttrName, attrVal,attrReport))
                            if attrType != zclAttrType: print("TYPE ERROR in zigbeeCluster Library !!!!!!!!!!!!!!!")
                        else:
                            myRespCode = zcl.lookupStatusCode(respCode)
                            print('{0},{1},{2:32},{3:20},**** PROBLEM,{4},{5}'.format(attrId,
                                                                                      attrType,
                                                                                      zclAttrName,
                                                                                      attrVal,
                                                                                      respVal,
                                                                                      myRespCode))
                    
                    else:
                        myRespCode = zcl.lookupStatusCode(respCode)
                        print('{0},{1},{2:32},{3:20},**** PROBLEM,{4},{5}'.format(attrId,
                                                                                  attrType,
                                                                                  zclAttrName,
                                                                                  "??",
                                                                                  respVal,
                                                                                  myRespCode))

            else:
                print("Problem with attribute discovery: ", respValue)
                exit()
                
    return 0
def getAllBindings():
    """ Get the binding table and print the results
    """
    print()
    print('Binding Table:')
    state, respCode, bindings = getBindings(nodeId)
    if state and respCode==zcl.statusCodes['SUCCESS']:
        if len(bindings)>0:
            for bind in bindings: 
                if bind!=None: print(bind)
        else:
            print('No bindings set.')
    else:
        print("Get bindings failed")
        exit()
    return 0
def deviceStatus(myNodeId):
    """ Query all bindings, attribute values and reporting intervals
        for a given device.
    """
    getAllAttributes(myNodeId)
    getBindings(myNodeId)
    return 0
def onOffTest(myNodeId, myEpId, onTime=1, offTime=1):
    """ Repeatedly turn device on/off with given periods.
    """
    
    while True:
        onOff(myNodeId, myEpId,'0', '1')
        time.sleep(onTime)
        onOff(myNodeId, myEpId,'0', '0')
        time.sleep(offTime)
    return 0
def dimmingTest(myNodeId,myEpId,minLevel,maxLevel,duration,iterations):

    while True:
        for l in range(0,10):
            time.sleep(0.3)
            level = round(minLevel+(maxLevel*l/10))
            levelHex = '{:02x}'.format(level)
            moveToLevel(myNodeId, myEpId, levelHex, duration)
            print(level,levelHex)
        
        for l in range(10,0,-1):
            time.sleep(0.3)
            level = round(minLevel+(maxLevel*l/10))
            levelHex = '{:02x}'.format(level)
            moveToLevel(myNodeId, myEpId, levelHex, duration)
            print(level,levelHex)

    return
            
""" Command line argument methods """
def readArguments():
    """ Read command line parameters 
        Use them if provided.
    """
    helpString = "\n*** threadedSerial Module\n\n" +\
                 "Use these command line options to select the node and firmware file:\n\n" +\
                 "-h Print this help\n" +\
                 "-n node        Node ID of target node\n" +\
                 "-e endpoint    Endpoint of target node\n" +\
                 "-p port        /dev/portId"

    myNodeId = ''
    myNodeEp = ''
    myPort = ''

    opts = getopt(sys.argv[1:], "hn:e:f:p:")[0]
    
    for opt, arg in opts:
        #print(opt, arg)
        if opt == '-h':
            print(helpString)
            exit()
        if opt == '-n':
            myNodeId = arg.upper()
        if opt == '-e':
            myNodeEp = arg
        if opt == '-p':
            myPort = arg
    
    return myNodeId, myNodeEp, myPort

""" Basic Thermostat Method Tests"""
def tstatMethodTests(myNodeId,myEpId):
    
    # Set all possible setpoints
    for sp in range(10,64):
        setpoint=sp/2        
        print('Setpoint={}'.format(setpoint))
        setSetpoint(myNodeId, myEpId, setpoint)
        time.sleep(10)
    
    print("SETTING MODE TO OFF")
    print(setMode(myNodeId, myEpId,'OFF'))
    time.sleep(20)
     
    print("SETTING MODE TO AUTO")
    print(setMode(myNodeId, myEpId,'AUTO'))
    time.sleep(20)
    
    print("SETTING MODE TO MANUAL")
    print(setMode(myNodeId, myEpId,'MANUAL'))
    time.sleep(20)
    
    print("SETTING MODE TO OVERRIDE")
    print(setMode(myNodeId, myEpId,'OVERRIDE',mySetpointFloat=31))
    time.sleep(20)
    
    boostDuration = random.randint(1,6)
    print("SETTING MODE TO BOOST, Duration={}hrs".format(boostDuration))
    print(setMode(myNodeId, myEpId,'BOOST',mySetpointFloat=31,myDuration=boostDuration))
    time.sleep(20)
    
    return 0
    
def setLongPollInterval(myNodeId,myEpId,myDurationHex):
    """
    """
    sendMode=0
    # AT+LPINTVL:252C,02,0,00000014
    msg = 'AT+LPINTVL:{0},{1},{2},{3}'.format(myNodeId,myEpId,sendMode,myDurationHex)
    # DFTREP:252C,02,0020,02,00
    expectedResponse=['DFTREP:{},{},{},{},(..)'.format(myNodeId,myEpId,'0020','02')]
    respState, respCode, respValue = sendCommand(msg,expectedResponse)
    if respState and respCode==zcl.statusCodes['SUCCESS']:
        respValue = respValue.replace('\r\n',',').split(',')
    return respState, respCode, respValue

def resetSedAttrs(params):
    """
    """
    if params['nodeType']=='ZED':
        
        print("\nAttempting reset of original check-in interval and long poll interval")
        
        pollControlClustId,_= zcl.getClusterNameAndId("Poll Control Cluster")
        checkInId,_,checkInType = zcl.getAttributeNameAndId("Poll Control Cluster", "checkInInterval") 
        
        # Reset check-in interval
        myIntervalHex=params['checkInInt']
        respState,_,_ = setAttribute(nodeId, nodeEp, pollControlClustId, 'server', checkInId, checkInType, myIntervalHex)
        if respState == False:
            print("Reset of short check-in interval failed")
            exit()       
        
        # Reset long poll interval    
        myIntervalHex = params['longPollInt']
        respState,_,_ = setLongPollInterval(nodeId, nodeEp, myIntervalHex)
        if respState == False:
            print("Reset of long poll interval failed")
            exit()        

        print("Reset is complete.")

    return

def getDuration(strDuration):
    arrDuration = strDuration.split(':')
    intHour = int(arrDuration[0])
    intMin = int(arrDuration[1])
    intSec = float(arrDuration[2])
    
    if (intHour > 0):
        strDuration = str(intHour) + " hour(s), " + str(intMin) + " minute(s), " + str(intSec) + " seconds"
        if (intHour > 23): 
            intDay = intHour // 24
            intHour = intHour % 24
            strDuration = str(intDay) + " day(s), "  + str(intHour) + " hour(s), " + str(intMin) + " minute(s), " + str(intSec) + " seconds"
    else:
        strDuration = str(intMin) + " minute(s), " + str(intSec) + " seconds"
    return strDuration

def getTimeStamp(boolFolderCreate):
    if boolFolderCreate:
        str_format = "%d-%b-%Y_%H-%M-%S"  
    else:
        str_format = "%d-%b-%Y %H:%M:%S" 
    today = datetime.datetime.today()
    return today.strftime(str_format)
    
    
def setpointValidationChecks():
    for sp in range (-10,80):
        print(sp/2,checkValidSetpoint(sp/2))



#TODO: Generic wait for msg with some pattern match

def waitForImageBlockReqOrUpgradeEndReq(myNodeId,myEp,timeout=120):
    """ Wait for imageBlockRequest or upgradeEndRequest from given node
        
        Returns a dict:
        
        {'error': status string - TIMEOUT or ERRORs,
         'upgradeEnd': boolean,
         'seqNum': seqNum string,
         'offset': fileOffset index,
         'maxDataSize': max block size (we can use smaller blocks)} 
        
    """
    # Wait for one of the given messages
    msgs = ['IMGBREQ:{0}'.format(myNodeId),
            'UPGRADEREQ:{0},{1}'.format(myNodeId,myEp)]
    msg = waitForMessage(msgs, timeout=timeout)

    # Parse the returned message
    payload = {'error': None,'upgradeEnd': False,'seqNum': None,'offset': None,'maxDataSize': None} 
    if msg==None:
        payload['error']='TIMEOUT: waitForImageBlockRequest timeout.'
        return payload
    
    elif msg.startswith(msgs[0]):
        # imageBlockRequest Receieved
        # IMGBREQ:<NodeID>,<EP>,<FieldControl>, <ManufCode>,<ImgType>,<FileVer>, <Offset>,<MaxDataSize> [,<RequestNodeAddress>, <BlockRequestDelay>],<SequenceNumber>
        resp = msg.split(',')
        
        payload['offset'] = resp[6]
        payload['maxDataSize'] = resp[7] 

        # Find seqNum depending on whether requestNodeAddess and blockRequest delay are in the response
        if resp[2] == '00':
            payload['seqNum'] = resp[8]
        else:
            payload['seqNum'] = resp[10]
       
    elif msg.startswith(msgs[1]):
        # upgradeEndRequestReceived
        # UPGRADEREQ: <NodeID>,<EP>,<Status>,<ManufCode>,<ImgType>,<FileVer>,<SequenceNumber>
        resp = msg.split(',')
        payload['seqNum']=resp[6]
        payload['upgradeEnd']=True
    
    return payload

def waitForMessage(myMsgs,timeout):
    """ Wait for a wanted message.
        Return full message if message arrives, return None if timeout
        
    """
    endTime = time.time() + timeout
    while time.time() < endTime:
        try:
            resp = rxQueue.get(timeout=1)
            for msg in myMsgs:       
                if resp.startswith(msg):
                    #print(resp)
                    return resp
        except queue.Empty:
            pass
        
    return None

def upgradeEndResponse(myNodeId,myEp,myManufCode,myImageType,myFileVersion,seqNum,currentTime=None,upgradeTime=None):
    """ Send an upgrade end response
    
        Defaults:
        
        sendMode=0                  # 0 = Send directly (not broadcast)
        currentTime = '00000000'    # '0x00000000 = 01/01/2000 00:00
        upgradeTime = '00000000'    # '0x00000000 = 01/01/2000 00:00
        
    """
    mySendMode='0'
    
    if currentTime!=None:
        currentTime = tct.utcDatetimeToZbHexTimestamp(currentTime)
        upgradeTime = tct.utcDatetimeToZbHexTimestamp(upgradeTime)
    else:
        currentTime='00000000'
        upgradeTime='00000000'
    
    # AT+UPGRADE:<NodeID>,<EP>,<SendMode>, <ManufacturerCode>,<ImageType>,<FileVersion>, <CurrentTime>,<UpgradeTime>,<Seq>
    msg = 'AT+UPGRADE:{0},{1},{2},{3},{4},{5},{6},{7},{8}'.format(myNodeId,
                                                                  myEp,
                                                                  mySendMode,
                                                                  myManufCode,
                                                                  myImageType,
                                                                  myFileVersion,
                                                                  currentTime,
                                                                  upgradeTime,
                                                                  seqNum)
    expectedResponse = ['OK']
    respState,respCode,respValue = sendCommand(msg, expectedResponse)
    return respState,respCode,respValue


""" Main code starts """
if __name__ == "__main__":
    
    #Comment for SQLITe data
    
    #global Sno
    #Sno =0
    global conn
    conn = sqlite3.connect('APS.db')
    c = conn.cursor()
    
    # Create table
    global strTableName
    strTableName = "Table_" + getTimeStamp(True).replace("-", "_")
    print(strTableName)
    #" + strTableName + " 
    c.execute("CREATE TABLE  " + strTableName + " (Iteration real, TimeStamp text, AT_Command text, TryCount text, Duration text)")
    conn.commit()
    
    global intGetDurationCntr
    for intGetDurationCntr in range(1,201):
        #if intGetDurationCntr == 33: debug = True
        #Sno = 0
        print("###########################")
        print("intCntr", intGetDurationCntr)
        print("###########################")
        
        # Check if any command line arguments provided
        nodeId, nodeEp, port = readArguments()
        
        if nodeId=='': 
            nodeId = lc.nodeList[0]['node']
            nodeEp = lc.nodeList[0]['ep1']
        if port=='': port=lc.PORT
        baud=lc.BAUD
        
        startSerialThreads(port, baud, printStatus=True)
        """ Get initial data - may have to set fp=True here for some devices """
        fp = False
        params = getInitialData(nodeId, nodeEp, fastPoll=fp, printStatus=True)
        if fp: resetSedAttrs(params)
        
        """ Iterate through all endpoints, clusters and attributes and bindings """
            
        getAllAttributes(nodeId)
            
        #getAllBindings()
        
        # Turn off the serial port worker thread
        print()
        stopThreads()
        ser.close()
        
    print('\nAll Done')
    '''#printAllResponses()

    #onOffTest(nodeId, '01', 2, 0.5)
    #dimmingTest(nodeId, lc.ep1, 20, 128, 0, 1)
    #onOff(nodeId, '01', '0', '0')
    #exit()
    
    # Get data from device
    params = getInitialData(nodeId, fastPoll=False, printStatus=True)
    getAllAttributes(nodeId)
    getAllBindings()
    
    # Turn off the serial port worked thread
    stopThreads()
    
    print('All Done')'''
