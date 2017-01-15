'''
Created on 5 Apr 2016

@author: ranganathan.veluswamy
'''
from datetime import timedelta
import datetime
from getopt import getopt
import queue
#import sqlite3
import sys
import threading
import time
import re

import serial

import FF_zigbeeClusters as zcl


# Serial Port Parameters
PORT = '/dev/tty.SLAB_USBtoUART'
BAUD = 115200
nodeList = [{'node':'3BB0','ep1':'01','ep2':None}]


MANUFACTURER_ID=''
sequenceNumber = -1

debug = False
rxQueue = queue.Queue()
txQueue = queue.Queue()
listenerQueue = queue.Queue()

stopThread = threading.Event()
threadPool = []


BG_Clusters=('FC00','FD00')
statusCodes = {'SUCCESS':                                      '00',
               'ZCL_MALFORMED_COMMAND':                        '80',
               'ZCL_UNSUPPORTED_CLUSTER_COMMAND':              '81',
               'ZCL_UNSUPPORTED_GENERAL_COMMAND':              '82',
               'ZCL_UNSUPPORTED_MANUFACTURER_CLUSTER_COMMAND': '83',
               'ZCL_UNSUPPORTED_MANUFACTURER_GENERAL_COMMAND': '84',
               'ZCL_INVALID_FIELD':                            '85',
               'ZCL_UNSUPPORTED_ATTRIBUTE':                    '86',
               'ZCL_INVALID_VALUE':                            '87',
               'ZCL_READ_ONLY':                                '88',
               'ZCL_INSUFFICIENT_SPACE':                       '89',
               'ZCL_DUPLICATE_EXISTS':                         '8A',
               'ZCL_NOT_FOUND':                                '8B',
               'ZCL_UNREPORTABLE_ATTRIBUTE':                   '8C',
               'ZCL_INVALID_DATA_TYPE':                        '8D'}


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

def serialReadHandler(ser):
    """ Serial port read thread handler
        If serial timeout=None then this thread blocks until a new line is available
     
    """
    while not stopThread.isSet():
        reading = ser.readline().decode().strip()
        if reading!='':
            rxQueue.put(reading)
            listenerQueue.put(reading)
            myTime = datetime.datetime.now().strftime("%H:%M:%S.%f")
            if debug: print("DEBUG RX: {},  {}".format(myTime,reading))
    print('Serial read thread exit')
    return 0

def startSerialThreads(port, baud, printStatus=False):
    """
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
    readThread = threading.Thread(target=serialReadHandler, args=(serial_port,))
    readThread.daemon = True # This kills the thread when main program exits
    readThread.start()
    readThread.name = 'readThread'
    threadPool.append(readThread)
    if printStatus: print('Serial port read handler thread started.\n')
    
    writeThread = threading.Thread(target=serialWriteHandler, args=(serial_port,))
    writeThread.daemon = True # This kills the thread when main program exits
    writeThread.start()
    writeThread.name = 'writeThread'
    threadPool.append(writeThread)
    if printStatus: print('Serial port write handler thread started.\n')
    
    return


def sendCommand(cmd,myExpectedResponses,maxAttempts=3,retryTimeout=30):
    """ Sends a command and reads the rxQueue looking for the raw response
        Returns the single line response or a list or responses if the 
        response is a SEQ (multi-row response)
    
    """
    
    intTCStartTime = time.monotonic()
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
                intTCEndTime = time.monotonic()
                strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
                strTCDuration = getDuration(strTCDuration)   
                intSeconds = float(strTCDuration.split(",")[1].strip().split(" ")[0])
                intMin = float(strTCDuration.split(",")[0].strip().split(" ")[0])
                intSeconds = intMin*60.0 + intSeconds
                #Sno = Sno + 1
                '''conn.executescript("insert into " + strTableName + " (Iteration, TimeStamp, AT_Command, TryCount, Duration) values ('" + str(intGetDurationCntr) + "', '" + str(getTimeStamp(False)) + "', '" + cmd + "', '" + str(tryCount) + "', '" + str(intSeconds) + "');")
                conn.commit()'''
                print(cmd)
                print("Time taken: " + strTCDuration)
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
            respCode=statusCodes['SUCCESS']
            resp['deviceType'] = respTemp[0]
            resp['channel'] = respTemp[1]
            resp['power'] = respTemp[2]
            resp['panId'] = respTemp[3]
            resp['epanId'] = respTemp[4]
    else:
        resp = respValue
    return respState, respCode, resp

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


def setBinding(myNodeId, mySrcAddr, mySrcEp, myCluster, myDstAddr, myDstEp, maxAttempts=3):
    """
        AT+BIND:<address>,<type>,<SrcAddress>,<SrcEP>,<ClusterID>,<DstAddress>
    """
    myType = '3' # 3=Unicast
    msg = 'AT+BIND:{0},{1},{2},{3},{4},{5},{6}'.format(myNodeId, myType, mySrcAddr, mySrcEp, myCluster, myDstAddr, myDstEp)
    expectedResponse = ['Bind:{0},(..)'.format(myNodeId)]
    print(msg, '\n')
    respState, respCode, respValue = sendCommand(msg,expectedResponse, maxAttempts) 
    if respState and respCode==statusCodes['SUCCESS']:
        respValue = respValue.replace('\r\n',',').split(',')
    return respState, respCode, respValue


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
    if myClust in BG_Clusters:
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
    
    if respState and respCode==statusCodes['SUCCESS']:
        respTemp = respValue.split(',')
        respTemp = respTemp[len(respTemp)-1]
    else:
        respTemp = respValue
        
    return respState, respCode, respTemp


def setLongPollInterval(myNodeId,myEpId,myDurationHex):
    """
    """
    sendMode=0
    # AT+LPINTVL:252C,02,0,00000014
    msg = 'AT+LPINTVL:{0},{1},{2},{3}'.format(myNodeId,myEpId,sendMode,myDurationHex)
    # DFTREP:252C,02,0020,02,00
    expectedResponse=['DFTREP:{},{},{},{},(..)'.format(myNodeId,myEpId,'0020','02')]
    respState, respCode, respValue = sendCommand(msg,expectedResponse)
    if respState and respCode==statusCodes['SUCCESS']:
        respValue = respValue.replace('\r\n',',').split(',')
    return respState, respCode, respValue

def getInitialData(nodeId, nodeEp, fastPoll=True, printStatus=False):
    """ Get PAN ID, Channel, EUIs, device type and MANUFACTURER_ID
        If device is a ZED then attempt to start fast polling.
        
    """
    
    params = {}
    params['nodeId']=nodeId
    
    # Retrieve and display network parameters 
    respState, respCode, network = getNetwork()
    if respState and respCode==statusCodes['SUCCESS']:
        if printStatus: print('Network Parameters: PanID={0}, Channel={1}'.format(network['panId'],network['channel']))
        params['panId']=network['panId']
        params['channel']=network['channel']
    else:
        print('Network error: {0}'.format(network))
    
    # Retrieve and display the IEEE addresses of the controller
    if fastPoll:
        respState,respCode,respValue = getEUI('0000','0000')
        if respState and respCode==statusCodes['SUCCESS']:
            controllerEUI = respValue        
            if printStatus: print('Controller EUI={}, nodeID=0000'.format(controllerEUI))
            params['controllerEUI']=controllerEUI
        else:
            print(respValue)
            exit()

    # Retrieve and display the device type.
    # If it's a sleepy end point then we may need to start fast polling
    respState, respCode, respValue = getNodeDesc(nodeId, nodeId)
    if respState and respCode==statusCodes['SUCCESS']:
        nodeType = respValue
        if printStatus: print('\r\nNode type = {}, Manufacturer Id = {}'.format(nodeType,MANUFACTURER_ID))
        params['nodeType']=nodeType
    else:
        print(respValue)
        exit()

    # Retrieve and display the IEEE addresses of the wanted node
    respState,respCode,respValue = getEUI(nodeId,nodeId)
    if respState and respCode==statusCodes['SUCCESS']:
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
        elif respState == True and respCode != statusCodes['SUCCESS']:
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

def setAttribute(myNodeId, myEP, myClust, myClusterType, myAttr, myAttrType,myAttrVal):
    """
    """
    sendMode='0'
    #Only currently support writing of sever type attributes
    assert myClusterType=='server'
    
    if myClust in BG_Clusters:
        myMsg = 'AT+WRITEMATR:{0},{1},{2},{3},{4},{5},{6},{7}'.format(myNodeId,myEP,sendMode,MANUFACTURER_ID,myClust,myAttr,myAttrType,myAttrVal)
        expectedResponse = ['WRITEMATTR:{0},{1},{2},{3},,(..)'.format(myNodeId,myEP,MANUFACTURER_ID,myClust)]
    else:
        myMsg = 'AT+WRITEATR:{0},{1},{2},{3},{4},{5},{6}'.format(myNodeId,myEP,sendMode,myClust,myAttr,myAttrType,myAttrVal)
        expectedResponse = ['WRITEATTR:{0},{1},{2},{3},(..)'.format(myNodeId,myEP,myClust,myAttr)]
    
    respState,respCode,respValue = sendCommand(myMsg, expectedResponse)

    if respState and respCode==statusCodes['SUCCESS']:
        respTemp = respValue.split(',')
        respTemp = respTemp[len(respTemp)-1]
    else:
        respTemp = respValue
        
    return respState, respCode, respTemp



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


def discEndpoints(myNodeId):
    """
    """
    myMsg = 'AT+ACTEPDESC:{0},{1}'.format(myNodeId,myNodeId)
    expectedResponses = ['ActEpDesc:{},(..)'.format(myNodeId)]    
    respState, respCode, respValue = sendCommand(myMsg, expectedResponses)    
    # Typical response format:
    # ActEpDesc:ACB0,00,05,06,07,08
    # Split on commas and discard first two fields
    if respState and respCode==statusCodes['SUCCESS']:
        respData = respValue.split(',')[2:]
    else:
        respData = respValue
    return respState, respCode, respData


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
    if respState and respCode==statusCodes['SUCCESS']:
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


def byteSwap(myString):
    first = myString[0:2]
    last = myString[2:4]
    return last+first

def getSequenceNumber():
    """
    """
    global sequenceNumber
    sequenceNumber = sequenceNumber + 1
    if sequenceNumber>255: sequenceNumber=0
    seqNumHex = "{:02x}".format(sequenceNumber)
    return seqNumHex
""" AT Command methods """

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
        
        if myClusterId in BG_Clusters:
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
                respCode = statusCodes['SUCCESS']           
            
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



def getAttributeReporting(myNodeId, myEpId, myClustId, myDirection, myAttr):
    """ Get the reporting intervals (if any) set for the given attribute
    """
    if myClustId in BG_Clusters:
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
    
    if respState and respCode==statusCodes['SUCCESS']:
        resp = respValue.split(',')
        if myClustId in BG_Clusters:
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


def stopThreads():
    """ Set the stop event and wait for all threads to exit
    
    """
    stopThread.set()
    for t in threadPool:
        t.join()
    return

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
    if respState and respCode==statusCodes['SUCCESS']:
        print("Endpoints: {0}".format(endpoints))
    else:
        print('Error finding endpoints')
        
    # Loop through each endpoint for clusters and attributes 
    for ep in endpoints:
        # Discover all clusters on this endpoint
        
        #respState,respCode,respValue = discClusters(nodeId,ep)
        respState,respCode,respValue = getSimpleDesc(nodeId,ep)        
        
        if respState and respCode==statusCodes['SUCCESS']:
            clusterList = buildClusterList(respValue)
        else:
            print('Problem with Cluster Discovery: ',respValue)
            exit()
        
        for clust in clusterList:
            clustId, clustName = zcl.getClusterNameAndId(clust[1])
            clustType = clust[0]          
            
            print("\nEndpoint={0}, Cluster={1},{2},{3}".format(ep, clust[1], clustName, clustType))

            respState,respCode,respValue = discAttrs(myNodeId,ep,clustId,clustType)
            if respState and respCode==statusCodes['SUCCESS']:
                for attr in respValue:
                    attrId = attr[0]
                    attrType = attr[1]
                    
                    # Get the attribute name from my library module
                    _, zclAttrName, zclAttrType = zcl.getAttributeNameAndId(clustId,attrId)
                    
                    # Get the attribute value
                    respState,respCode,respVal = getAttribute(myNodeId, ep, clustId, attrId, clustType)
                    if respState and respCode==statusCodes['SUCCESS']:
                        attrVal = respVal
                            
                        # Get the reporting intervals for the attribute
                        respState,respCode,attrReport = getAttributeReporting(myNodeId, ep, clustId, clustType, attrId)
#                         if not respState:
#                             attrReport = "Problem reading reporting config. {}".format(attrReport)
#                         if respState and respCode!=statusCodes['SUCCESS']:
#                             attrReport = "Problem reading reporting config. {}".format(zcl.lookupStatusCode(respCode))

                        if respState and respCode == statusCodes['SUCCESS']:
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

if __name__ == '__main__':
    #Comment for SQLITe data
    
    global Sno
    Sno =0
    global conn
    '''    conn = sqlite3.connect('APS.db')
    c = conn.cursor()
    
    # Create table
    global strTableName
    strTableName = "Table_" + getTimeStamp(True).replace("-", "_")
    print(strTableName)
    #" + strTableName + " 
    c.execute("CREATE TABLE  " + strTableName + " (Iteration real, TimeStamp text, AT_Command text, TryCount text, Duration text)")
    conn.commit()
    '''
    global intGetDurationCntr
    for intGetDurationCntr in range(1,201):
        #if intGetDurationCntr == 33: debug = True
        Sno = 0
        print("###########################")
        print("intCntr", intGetDurationCntr)
        print("###########################")
        
        # Check if any command line arguments provided
        nodeId, nodeEp, port = readArguments()
        
        nodeId = nodeList[0]['node']
        nodeEp = nodeList[0]['ep1']
        
        startSerialThreads(PORT, BAUD, printStatus=True)
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
    