'''
Created on 22 May 2015

@author: ranganathan.veluswamy
'''
from datetime import datetime
from datetime import timedelta
import json
import os
import time

import FF_loggingConfig as config
import FF_threadedSerial as AT
import FF_zigbeeClusters as zcl

#import sensor_TSL2561 as TSL2561
statusCodeValue = {'8C': 'TABLE_FULL',
                               '00': 'SUCCESS'
                               }
deviceMaxBindLimit = {'BM': 10,
                                    'TH': 5
                                   }

global oJsonDict
strEnvironmentFolderPAth = os.path.abspath(__file__ + "/../../../../../02_Manager_Tier/EnviromentFile/" )

strGlobVarFilePath = os.path.abspath(strEnvironmentFolderPAth + '/GlobalVar.json')    
strJson = open(strGlobVarFilePath, mode='r')
oJsonDict = json.loads(strJson.read())
strJson.close() 
#oJsonDict = {}
#Roud up float value to nearest Integer

#Get Lux value from Light Sensor
'''
def get_lux_value():
    tsl = TSL2561.tsl2561()
    full,ir = tsl.getRawLuminosityAutoGain()
    lux = tsl.luxCalculation(full,ir,tsl.gain,tsl.integrationTime)
    return lux
'''

def get_lux_value():
    return 0,0,0

def round_up(fltValue):
    round_up_val = lambda num: int(num + 1) if int(num) != num else int(num)
    fltValue = fltValue - 0.5
    return round_up_val(fltValue)

#Converts the Report log format to Console print log
def conertToPrintLog(strReportLog):
    arrReportLog = strReportLog.split("@@@")
    strPrintLog = arrReportLog[0].split("$$")[0] + ': ===>> Expected Thermostat Values:\n'
    for strRow in arrReportLog[1].split("$~"):
        strPrintLog = strPrintLog + strRow.split("$$")[0] + ' ===>> ' + strRow.split("$$")[1] + '\n'
        
    return strPrintLog


#Converts the hex value of the retrieved temperature
def convertHexTemp(hexTemperature, booWithCentigradeSymbol = True):
    if booWithCentigradeSymbol:
        strTemperature = str(int(hexTemperature, 16) / 100) + 'C'
    else:
        strTemperature = str(int(hexTemperature, 16) / 100)
    return strTemperature

#Get Attribute from the Global Var JSON file
def getAttribute(strHeader, strAttributeName, strCurrentAppVersion= None, Env = None):
    
    '''strGlobVarFilePath = strEnvironmentFolderPAth + 'GlobalVar.json'    
    strJson = open(strGlobVarFilePath, mode='r')
    oJsonDict = json.loads(strJson.read())
    strJson.close()'''
    
    if Env is None: strCurrentEnv = oJsonDict['globalVariables']['currentEnvironment']
    else: strCurrentEnv = Env
    
    #Return Current Environment
    if strAttributeName == 'currentEnvironment': 
        return strCurrentEnv
    elif strAttributeName == 'resultFolderLabel': return oJsonDict['globalVariables']['resultFolderLabel']
    
    
    if strAttributeName.upper() == 'ATZIGBEENODE': return oJsonDict['globalVariables']['atZigbeeNode']
    if strAttributeName.upper() == 'APIVALIDATIONTYPE': return oJsonDict['globalVariables']['apiValidationType']
    if strAttributeName.upper() == 'MAINCLIENT': return oJsonDict['globalVariables']['mainClient']
    if strAttributeName.upper() == 'USERNAME': return oJsonDict['globalVariables']['userName']
    if strAttributeName.upper() == 'PASSWORD': return oJsonDict['globalVariables']['password']
    if strAttributeName.upper() == 'TEST_SUITE': return oJsonDict['globalVariables']['test_suite']
    if strAttributeName.upper() == 'SECONDCLIENT': return oJsonDict['globalVariables']['secondClient']
    if strAttributeName.upper() == 'SECONDCLIENTVALIDATEFLAG': return oJsonDict['globalVariables']['secondClientValidateFlag']
    if strAttributeName.upper() == 'APPIUM_PORT': return oJsonDict['globalVariables']['appium_port']
    if strAttributeName.upper() == 'APPIUM_UDID': return oJsonDict['globalVariables']['appium_udid']
    
    if strAttributeName.upper() == 'CURRENTAPPVERSION': return oJsonDict['globalVariables']['currentAppVersion']
    if strHeader.upper() == 'CLIENTLIST': return oJsonDict['globalVariables']['clientList'][strAttributeName]
    if strHeader.upper() == 'VALIDATION': return oJsonDict['globalVariables']['validation'][strAttributeName]
    if strHeader.upper() == 'BATCH_EXECUTION': return oJsonDict['globalVariables']['batch_execution'][strAttributeName]
    
    #Get all attribute for the selected Environment
    oCurrentEnvDetailsDict = oJsonDict['globalVariables']['listOfEnvironments'][strCurrentEnv]
    strHeaderFolder = strHeader
    if strCurrentAppVersion is None: strCurrentAppVersion = oJsonDict['globalVariables']['currentAppVersion'] 
    if not strHeader.upper() == 'COMMON': strHeader = strHeader + strCurrentAppVersion
    if strHeader in oCurrentEnvDetailsDict:
        if strAttributeName in oCurrentEnvDetailsDict[strHeader]:
            #Return App filepath
            if strAttributeName == 'appFileName':
                strAppFolderName = oCurrentEnvDetailsDict['common']['appFolderName'] 
                return os.path.abspath(strEnvironmentFolderPAth + '/Apps/' + strHeaderFolder + '/' + strAppFolderName + '/' +  oCurrentEnvDetailsDict[strHeader][strAttributeName])
            #Else Return the attribute value
            return oCurrentEnvDetailsDict[strHeader][strAttributeName]
                
        else: return 'Missing Atribule'
    else: return 'Missing Header'

#Set Attribute from the Global Var JSON file
def setAttribute(strHeader, strAttributeName, strAttributeValue):
    if 'COMMON' in strHeader.upper():
        oJsonDict['globalVariables'][strAttributeName] = strAttributeValue
        
        #Write back the JSON to the GlobalVar.JSON
        oJson = open(strGlobVarFilePath, mode='w+')
        oJson.write(json.dumps(oJsonDict, indent=4, sort_keys=True))
        oJson.close()

#Set Attribute from the Global Var JSON file
def setAttribute_KitBatch(strHeader, strAttributeName, strAttributeValue):
    strKitBatchFilePath = os.path.abspath(strEnvironmentFolderPAth + '/kit_batch.json' )
    strKBJson = open(strKitBatchFilePath, mode='r')
    oKBJsonDict = json.loads(strKBJson.read())
    strKBJson.close()
    
    if 'batch_execution' in strHeader:
        oKBJsonDict['kit_batch']['batch_execution'][strAttributeName] = strAttributeValue
        
        #Write back the JSON to the GlobalVar.JSON
        strKBJson = open(strKitBatchFilePath, mode='w+')
        strKBJson.write(json.dumps(oKBJsonDict, indent=4, sort_keys=True))
        strKBJson.close()

#Get Attribute from the Global Var JSON file
def getAttribute_KitBatch(strHeader, strAttributeName):
    strKitBatchFilePath = os.path.abspath(strEnvironmentFolderPAth + '/kit_batch.json') 
    strKBJson = open(strKitBatchFilePath, mode='r')
    oKBJsonDict = json.loads(strKBJson.read())
    strKBJson.close()
    
    if 'batch_execution' in strHeader:
        return oKBJsonDict['kit_batch']['batch_execution'][strAttributeName]

       

def setClient(context, strString):           
        if 'PLATFORM' in context.APIType.upper():
            context.oThermostatEP.client = None
            for oClientName in strString.split(' '):
                if oClientName.upper() in context.clientDict.keys():
                    context.oThermostatEP.client = context.clientDict[oClientName.upper()].split(' ')[0]
                    
            if context.oThermostatEP.client == None:
                context.oThermostatEP.client = getAttribute('common', 'mainClient')
            print(context.oThermostatEP.client)
            
            
def setEP(context, strEndPoint):    
        #Set the Type Heat or Water
        if 'WATER' in strEndPoint.upper(): context.oThermostatEP  = context.oThermostatClass.waterEP
        elif'HEAT' in strEndPoint:  context.oThermostatEP  = context.oThermostatClass.heatEP
        else: context.oThermostatEP  = context.oThermostatClass.heatEP
        context.oThermostatEP.update()
            
def setSPOnOff(myNodeId = None, strOnOff = 'ON', boolZigbee = None):
    """ Repeatedly turn device on/off with given periods.
    """
    if boolZigbee is None:
        if not 'ZIGBEE' in getAttribute('common', 'apiValidationType').upper(): boolZigbee = False
        else: boolZigbee = True
            
    if myNodeId is None: myNodeId = discoverNodeIDbyCluster('0006')[2]
    if not boolZigbee:
        AT.stopThread.clear()  
        AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False, rxQ=True, listenerQ=True)
    if 'ON' in strOnOff.upper():
        AT.onOff(myNodeId, '09','0', '1')
    else: AT.onOff(myNodeId, '09','0', '0')
    
    if not boolZigbee: AT.stopThreads()
    
def setOnOff(myNodeId = None,myEP=None, strOnOff = 'ON', boolZigbee = None):
    """ Repeatedly turn device on/off with given periods.
    """
    if boolZigbee is None:
        if not 'ZIGBEE' in getAttribute('common', 'apiValidationType').upper(): boolZigbee = False
        else: boolZigbee = True
            
    if myNodeId is None: myNodeId = discoverNodeIDbyCluster('0006')[2]
    if not boolZigbee:
        AT.stopThread.clear()  
        AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False)
    if 'ON' in strOnOff.upper():
        AT.onOff(myNodeId, myEP,'0', '1')
    else: AT.onOff(myNodeId, myEP,'0', '0')
    
    if not boolZigbee: AT.stopThreads()

def getSPOnOFFStatus(myNodeId = None, boolZigbee = None):
    """ Repeatedly turn device on/off with given periods.
    """
    if not boolZigbee:
        AT.stopThread.clear()  
        AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False)
    if myNodeId is None: myNodeId = discoverNodeIDbyCluster('0006')[2]
    
    myEP = '09'
    sendMode = '0'
    myClust = '0006'
    myAttr = '0000'
    myMsg = 'AT+READATR:{0},{1},{2},{3},{4}'.format(myNodeId,myEP,sendMode,myClust,myAttr)             
    
    expectedResponse=['RESPATTR:{0},{1},{2},{3},{4},(..)'.format(myNodeId,
                                                                      myEP,
                                                                      myClust,
                                                                      myAttr, '00')]
        
    respState, respCode, respValue = AT.sendCommand(myMsg, expectedResponse)

    print(respValue, 'respValue')
    
    AT.stopThreads()
    intStatusAttribute = respValue.split(',')[len(respValue.split(','))-1]
    
    if intStatusAttribute == "00":
        strStatusAttribute = "OFF"
    elif intStatusAttribute == "01":
        strStatusAttribute = "ON"
        
    return strStatusAttribute

def setBind(myNodeId, myEndPoint,  hexClusterID, boolZigbee = None):
    """ Repeatedly turn device on/off with given periods.
    """
    if boolZigbee is None:
        if not 'ZIGBEE' in getAttribute('common', 'apiValidationType').upper(): boolZigbee = False
        else: boolZigbee = True
            
    if not boolZigbee:
        AT.stopThread.clear()  
        AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False)
        #AT.startAttributeListener(printStatus=False)
        #AT.getInitialData(myNodeId, fastPoll=True, printStatus=True)
        
    # Setup a binding
    _, _, mySrcAddr = AT.getEUI(myNodeId, myNodeId)
    _, _, myDstAddr = AT.getEUI('0000', '0000')
    respState, respCode, respValue = AT.setBinding(myNodeId, mySrcAddr, myEndPoint, hexClusterID, myDstAddr, '01')
    print(respState, respValue)
    '''if respState: status = "PASS"
    else: status = "FAIL"
    if not respCode == '00':
        status = respCode'''
    status = respCode
    if not boolZigbee: AT.stopThreads()
    return status, mySrcAddr + "$$" + myEndPoint + "$$" + hexClusterID + "$$" + myDstAddr + "$$" + '01' 

def setUnBind(myNodeId, myEndPoint,  hexClusterID, boolZigbee = None):
    """ Repeatedly turn device on/off with given periods.
    """
    if boolZigbee is None:
        if not 'ZIGBEE' in getAttribute('common', 'apiValidationType').upper(): boolZigbee = False
        else: boolZigbee = True
            
    if not boolZigbee:
        AT.stopThread.clear()  
        AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False)
        #AT.startAttributeListener(printStatus=False)
        #AT.getInitialData(myNodeId, fastPoll=True, printStatus=True)
        
    # Setup a binding
    _, _, mySrcAddr = AT.getEUI(myNodeId, myNodeId)
    _, _, myDstAddr = AT.getEUI('0000', '0000')
    respState, respCode, respValue = unBind(myNodeId, mySrcAddr, myEndPoint, hexClusterID, myDstAddr, '01')
    print(respState, respValue)
    if respState: status = "PASS"
    else: status = "FAIL"
    
    if not boolZigbee: AT.stopThreads()
    return status, mySrcAddr + "$$" + myEndPoint + "$$" + hexClusterID + "$$" + myDstAddr + "$$" + '01' + "$$" + status

def unBind(myNodeId, mySrcAddr, mySrcEp, myCluster, myDstAddr, myDstEp):
    """
        AT+BIND:<address>,<type>,<SrcAddress>,<SrcEP>,<ClusterID>,<DstAddress>
    """
    
    myType = '3' # 3=Unicast
    msg = 'AT+UNBIND:{0},{1},{2},{3},{4},{5},{6}'.format(myNodeId, myType, mySrcAddr, mySrcEp, myCluster, myDstAddr, myDstEp)
    expectedResponse = ['Unbind:{0},(..)'.format(myNodeId)]
    respState, respCode,respValue = sendCommand(msg,expectedResponse)
    if respState and respCode==zcl.statusCodes['SUCCESS']:
        respValue = respValue.replace('\r\n',',').split(',')
    return respState, respCode, respValue

def getBind(myNodeId, boolZigbee = None):
    """ Repeatedly turn device on/off with given periods.
    """
    if boolZigbee is None:
        if not 'ZIGBEE' in getAttribute('common', 'apiValidationType').upper(): boolZigbee = False
        else: boolZigbee = True
            
    if not boolZigbee:
        AT.stopThread.clear()  
        AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False)
        #AT.startAttributeListener(printStatus=False)
        #AT.getInitialData(myNodeId, fastPoll=True, printStatus=True)
        
    #Get the bindings
    respState, _, respValue = getBindings(myNodeId)
    #print(respState, respValue)
    if not boolZigbee: AT.stopThreads()
    return respValue

def getNtable(myNodeId):
    
    """  Retrieve neighbor table for the given nodeId
    
    """
    msg = ''
    if myNodeId.upper() == 'FF':
        expectedResponse = ['NTable:{0},(..)'.format('0000')]
    else: expectedResponse = ['NTable:{0},(..)'.format(myNodeId)]
    
    finished = False
    tableRow=0
    rows=[]
    headersDone = False
    strIndex = "00"
    while not finished:
        tableRowReset = 0
        # Typical Response.
        # BTable:0000,00
        # Length:03
        # No. | SrcAddr | SrcEP | ClusterID | DstAddr | DstEP
        # 0. | 000D6F000059474E | 01 | DEAD |1234567887654321 | 12
        # 1. | 000D6F000059474E | 01 | DEAD |E012345678876543 | E0
        # 2. | 000D6F000059474E | 01 | DEAD | ABCD 
        # ACK:01    
        
        # Read a page of the table
        if len(strIndex) == 1:
            strIndex = "0"+strIndex
        hexIndex = '%02x' % tableRow
        msg = "AT+NTABLE:{},{}".format(strIndex, myNodeId)
        respState, respCode, respValue = AT.sendCommand(msg, expectedResponse)
        if (not respState) or (respCode!=zcl.statusCodes['SUCCESS']):
            print("Error with binding table read : ",respValue)
            exit()
        header1 = respValue
        
        # Extract the table length    
        header2 = AT.rxQueue.get()
        print(header2)
        if not header2.startswith('Length'):
            print("Error with binding table read - expected 'Length' ",header2)
            exit()
        tableLength = int(header2.split(':')[1],16)
        
        # Read the table header row (only if there are more than zero bindings)
        if tableLength>0:
            header3 = AT.rxQueue.get()
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
                row=AT.rxQueue.get()
                if str(row).startswith(str(tableRow)):
                    if int(row.split('|')[0].strip('. '))!= tableRow:
                        print("Error with binding table read - Row number mismatch.")
                        exit()
                    tableRow+=1
                    tableRowReset+= 1
                    print(row)
                    rows.append(row)
                pageRow+=1
                
                
        if tableRow>=tableLength:
            finished = True
        strIndex = str(tableRow)
    return respState, respCode, rows

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
        respState, respCode, respValue = AT.sendCommand(msg, expectedResponse)
        if (not respState) or (respCode!=zcl.statusCodes['SUCCESS']):
            print("Error with binding table read : ",respValue)
            exit()
        header1 = respValue
        
        # Extract the table length    
        header2 = AT.rxQueue.get()
        if not header2.startswith('Length'):
            print("Error with binding table read - expected 'Length' ",header2)
            exit()
        tableLength = int(header2.split(':')[1])
        
        # Read the table header row (only if there are more than zero bindings)
        if tableLength>0:
            header3 = AT.rxQueue.get()
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
            while pageRow<2 and tableRow<tableLength:
                row=AT.rxQueue.get()
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


def discoverNodeIDbyCluster(nodeSpecificAttribute):
    """ Returns the Node ID of Related to the Cluster
    """
    myMsg = 'AT+DISCOVER:{0}'.format(nodeSpecificAttribute)
    expectedResponse = ['DEV:(..)']
    # DEV:C58A,09
    
    respState, respCode, respValue = AT.sendCommand(myMsg, expectedResponse)

    if respState:
        resp = respValue.split(',')
        resp = resp[0].split(':')[1]
    else:
        resp = respValue
        
    return respState,respCode,resp
def getNodeList():
    oNCAJsonDict = getNodeClusterJson() 
    return oNCAJsonDict['nodes']['list_of_nodes']

def getModelforDevice(nodeID, ep):
        sendMode = "0"
        ClusterID = "0000"
        AttrID = "0005"
        expectedResponse =  ['RESPATTR:{0},{1},{2},{3},(..)'.format(nodeID,ep,ClusterID,AttrID)]
        msg = "AT+READATR:{0},{1},{2},{3},{4}".format(nodeID, ep, sendMode, ClusterID, AttrID)
        respState, respCode, respValue = AT.sendCommand(msg, expectedResponse)
        if (not respState) or (respCode!=zcl.statusCodes['SUCCESS']):
            print("Error with binding table read : ",respValue)
            exit()
        
        if respState:
            arrResp = respValue.split(',')
            resp = arrResp[len(arrResp)-1]
        else:
            resp = respValue
        return resp

def getNodeClusterJson():
    strNodeClustAttrPath = os.path.abspath(strEnvironmentFolderPAth + '/nodes_clusters_attributes.json')    
    strJson = open(strNodeClustAttrPath, mode='r')
    oNCAJsonDict = json.loads(strJson.read())
    strJson.close() 
    return oNCAJsonDict

def putNodeClusterJson(oNCAJsonDict):
    strNodeClustAttrPath = os.path.abspath(strEnvironmentFolderPAth + '/nodes_clusters_attributes.json')    
    #Write back the JSON to the GlobalVar.JSON
    oJson = open(strNodeClustAttrPath, mode='w+')
    oJson.write(json.dumps(oNCAJsonDict, indent=4, sort_keys=False))
    oJson.close()

def getAllClustersAttributes(myNodeId, strNodeName):
    """ Uses discoverEndpoints, discoverClusters, discoverAttributes and READATTR to query all
        attribute values on the device and print a summary.
        
        Also recovers any reporting intervals for the attribute
        
        Print the Endpoint list
        Print the Clusters
        Print the Attribute values and Reporting Intervals
        
    """
    
    oNCAJsonDict = getNodeClusterJson()
    
    oLstNodes = oNCAJsonDict["nodes"]["list_of_nodes"]
    oLstNodes[strNodeName] = {}
    oNode = oLstNodes[strNodeName]
    oNode["node_id"] = myNodeId
    oNode["list_of_endpoints"] = {}
    
    # Retrieve and display the endpoints
    respState,respCode,endpoints = AT.discEndpoints(myNodeId)
    if respState and respCode==zcl.statusCodes['SUCCESS']:
        print("Endpoints: {0}".format(endpoints))
    else:
        print('Error finding endpoints')
        
    # Loop through each endpoint for clusters and attributes 
    for ep in endpoints:
        # Discover all clusters on this endpoint
        oNode["list_of_endpoints"][ep] = {}
        oNode["list_of_endpoints"][ep]["list_of_clusters"] = {}
        
        respState,respCode,respValue = AT.discClusters(myNodeId,ep)
        if respState and respCode==zcl.statusCodes['SUCCESS']:
            clusterList = AT.buildClusterList(respValue)
        else:
            print('Problem with Cluster Discovery: ',respValue)
            exit()
        
        for clust in clusterList:
            clustId, clustName = zcl.getClusterNameAndId(clust[1])
            clustType = clust[0]          
            oNode["list_of_endpoints"][ep]["list_of_clusters"][clustId] = {}
            oNode["list_of_endpoints"][ep]["list_of_clusters"][clustId]["cluster_name"] = clustName
            oNode["list_of_endpoints"][ep]["list_of_clusters"][clustId]["list_of_attributes"] = {}
            
            
            print("\nEndpoint={0}, Cluster={1},{2},{3}".format(ep, clust[1], clustName, clustType))

            respState,respCode,respValue =AT.discAttrs(myNodeId,ep,clustId,clustType)
            if respState and respCode==zcl.statusCodes['SUCCESS']:
                for attr in respValue:
                    attrId = attr[0]
                    attrType = attr[1]
                    _, zclAttrName, zclAttrType = zcl.getAttributeNameAndId(clustId,attrId)
                    oNode["list_of_endpoints"][ep]["list_of_clusters"][clustId]["list_of_attributes"][attrId] = {}
                    oNode["list_of_endpoints"][ep]["list_of_clusters"][clustId]["list_of_attributes"][attrId]["attrbute_name"] = zclAttrName
                    oNode["list_of_endpoints"][ep]["list_of_clusters"][clustId]["list_of_attributes"][attrId]["attrbute_type"] = zclAttrType
                    '''
                    # Get the attribute value
                    respState,respCode,respVal = AT.getAttribute(myNodeId, ep, clustId, attrId, clustType)
                    if respState and respCode==zcl.statusCodes['SUCCESS']:
                        if respVal=='86':
                            print('{0},Unsupported attribute'.format(attr[0]))
                            attrReport = 'Reporting not retrieved'                                
                        else:
                            attrVal = respVal
                            
                            # Get the reporting intervals for the attribute
                            respStatus,respCode,attrReport = AT.getAttributeReporting(myNodeId, ep, clustId, clustType, attrId)
                            if not respStatus:
                                attrReport = "Problem reading reporting config. {}".format(attrReport)
                            if respStatus and respCode!=zcl.statusCodes['SUCCESS']:
                                attrReport = "Problem reading reporting config. {}".format(zcl.lookupStatusCode(respCode))
                            # Get the attribute name from my library module
                            _, zclAttrName, zclAttrType = zcl.getAttributeNameAndId(clustId,attrId)
                            print("{0},{1},{2:32},{3:20},{4}".format(attrId, attrType, zclAttrName, attrVal,attrReport))
                            if attrType != zclAttrType: print("TYPE ERROR in zigbeeCluster Library !!!!!!!!!!!!!!!")
                    
                    else:
                        print("Problem finding attribute value")
                        exit()'''

            else:
                print("Problem with attribute discovery: ", respValue)
                exit()
                
    oNCAJsonDict["nodes"]["list_of_nodes"][strNodeName] = oNode
    
    putNodeClusterJson(oNCAJsonDict)
    
    return 0

def get_device_version(oNode, oEP):
    sendMode = '0'
    myClust = '0019'
    myAttr = '0002'
    myMsg = 'AT+READCATR:{0},{1},{2},{3},{4}'.format(oNode,oEP,sendMode,myClust,myAttr)             
    
    expectedResponse=['RESPATTR:{0},{1},{2},{3},{4},(..)'.format(oNode,
                                                                      oEP,
                                                                      myClust,
                                                                      myAttr, '00')]
    
    respState, respCode, respValue = AT.sendCommand(myMsg, expectedResponse, maxAttempts=20)

    if respState:
        arrResp = respValue.split(',')
        resp = arrResp[len(arrResp)-1]
    else:
        resp = respValue    
    return respState,respCode,resp

def check_device_back_after_restart(oNode, oEP):
    AT.debug = True
    myMsg = ''          
    
    expectedResponse=['IMGQUERY:{0},{1},(..)'.format(oNode,
                                                                      oEP)]
    
    respState, respCode, respValue = AT.sendCommand(myMsg, expectedResponse, maxAttempts=1350, retryTimeout=2)

    if respState:
        arrResp = respValue.split(',')
        resp = arrResp[len(arrResp)-2]
    else:
        resp = respValue    
    
    AT.debug = False
    return respState,respCode,resp

#Pjoin and Check for the Device and returns the Node ID
def check_device_joined(strMacID, oDeviceType = 'FFD', hexPjoinTimeOut = 'ff'):
    myMsg = 'AT+PJOIN:{0}'.format(hexPjoinTimeOut)             
    
    expectedResponse=[oDeviceType+':{0},(..)'.format(strMacID)]
    
    respState, respCode, respValue = AT.sendCommand(myMsg, expectedResponse, maxAttempts=3)

    if respState:
        arrResp = respValue.split(',')
        resp = arrResp[len(arrResp)-1]
    else:
        resp = respValue    
    return respState,respCode,resp 

#remove device from from network
def remove_device_from_network(oNode):
    myMsg = 'AT+DASSR:{0}'.format(oNode)             
    
    expectedResponse=['ACK:(..)']
    
    respState, respCode, respValue = AT.sendCommand(myMsg, expectedResponse, maxAttempts=1)

    return respState,respCode,respValue 

#remove device from from network
def disassociate_from_pan():
    myMsg = 'AT+DASSL'           
    
    expectedResponse=['LeftPAN']
    
    respState, respCode, respValue = AT.sendCommand(myMsg, expectedResponse, maxAttempts=1)

    return respState,respCode,respValue 

#remove device from from network
def establish_network(channel):
    myMsg = 'AT+EN:{0}'.format(str(channel)) 
    
    expectedResponse=['JPAN:{0}(..)'.format(str(channel))]
    
    respState, respCode, respValue = AT.sendCommand(myMsg, expectedResponse, maxAttempts=1)

    return respState,respCode,respValue 

#Get Device Node from nTable
def get_device_node_from_ntable(strMacID):
    respState, respCode, rows = getNtable('FF')
    for oRow in rows:
        if oRow is not None:
            if strMacID in oRow:
                strNodeId = ""
                intCntr = 0
                for oNode in oRow:
                    if intCntr == 3:
                        strNodeId = oNode.replace(" ","")
                return strNodeId
    return ""


#get the device constants
def get_device_constants(nodeID):
    myMsg = 'AT+NODEDESC:{0},{1}'.format(nodeID,nodeID)        
    expectedResponse=['NodeDesc:{0}(..)'.format(nodeID)]
    respState, respCode, respValue = AT.sendCommand(myMsg, expectedResponse, maxAttempts=5)
    
    intLoopCntr = 1
    while True:
        strResp = AT.rxQueue.get()
        respValue = respValue + '$$' + strResp
        if 'ACK' in strResp: break
        intLoopCntr = intLoopCntr + 1
        print(intLoopCntr)
        if intLoopCntr > 20: break
    
    return respState,respCode,respValue

#Get the Port of the Telegesis stick
def get_Port_Id_TG():
    strPORT = ""
    for filenames in os.walk("/dev"):
        for file_list in filenames:
            for file_name in file_list:
                if 'TTY' in file_name.upper() and 'USB' in file_name.upper():
                    strPORT = file_name
                    return strPORT
    return strPORT
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
    return strDuration
#Gets the Time stamp for creating the folder set or for reporting time stamp based on boolFolderCreate 
def getTimeStamp(boolFolderCreate):
    if boolFolderCreate:
        str_format = "%d-%b-%Y_%H-%M-%S"  
    else:
        str_format = "%d-%b-%Y %H:%M:%S" 
    today = datetime.today()
    return today.strftime(str_format)


def createBaselineDeviceDumpJsonFile():
    strAndroidDeviceListPath = os.path.abspath(strEnvironmentFolderPAth + '/android_device_list.json')    
    strJson = open(strAndroidDeviceListPath, mode='r')
    oADLJsonDict = json.loads(strJson.read())
    strJson.close() 
    return oADLJsonDict

def createBaselineDeviceAttrbDumpJson(myNodeId, boolUpdateBaseline = True):
    """ Uses discoverEndpoints, discoverClusters, discoverAttributes and READATTR to query all
        attribute values on the device and print a summary.
        
        Also recovers any reporting intervals for the attribute
        
        Print the Endpoint list
        Print the Clusters
        Print the Attribute values and Reporting Intervals
        
    """
    
    
    # Retrieve and display the endpoints
    respState,respCode,endpoints =AT. discEndpoints(myNodeId)
    endpoints.sort()
    if respState and respCode==zcl.statusCodes['SUCCESS']:
        print("Endpoints: {0}".format(endpoints))
    else:
        print('Error finding endpoints')
    
    modelID = getModelforDevice(myNodeId, endpoints[0])
    deviceVersion = get_device_version(myNodeId, endpoints[0])[2]
    
    oBSJson = {}
    oBSJson["DeviceModelID"] = modelID
    oBSJson["DeviceVersion"] = deviceVersion
    oBSJson["ListOfEndPoints"] = {}
    oListOfEP = {}
    # Loop through each endpoint for clusters and attributes 
    for ep in endpoints:
        # Discover all clusters on this endpoint
        
        oListOfEP[ep] = {}
        oListOfEP[ep]["EndPoint"] = ep
        oListOfEP[ep]["ListOfClusters"] = {}
        oListOfClusters = {}
        #respState,respCode,respValue = discClusters(nodeId,ep)
        respState,respCode,respValue = AT.getSimpleDesc(myNodeId,ep)        
        
        if respState and respCode==zcl.statusCodes['SUCCESS']:
            clusterList = AT.buildClusterList(respValue)
        else:
            print('Problem with Cluster Discovery: ',respValue)
            exit()
        
        for clust in clusterList:
            clustId, clustName = zcl.getClusterNameAndId(clust[1])
            clustType = clust[0]          
            oListOfEP[ep] 
            print("\nEndpoint={0}, Cluster={1},{2},{3}".format(ep, clust[1], clustName, clustType))
            
            clustIdNode = clustId + "_" + clustName
            oListOfClusters[clustIdNode] = {}
            oListOfClusters[clustIdNode]["ClusterID"] = clustId
            oListOfClusters[clustIdNode]["ClusterName"] = clustName
            oListOfClusters[clustIdNode]["ClusterType"] = clustType
            oListOfClusters[clustIdNode]["ListOfAttributes"] = {}
            oListOfAttributes = {}
            
            
            respState,respCode,respValue = AT.discAttrs(myNodeId,ep,clustId,clustType)
            if respState and respCode==zcl.statusCodes['SUCCESS']:
                for attr in respValue:
                    attrId = attr[0]
                    attrType = attr[1]
                    
                    # Get the attribute name from my library module
                    _, zclAttrName, zclAttrType = zcl.getAttributeNameAndId(clustId,attrId)
                    
                    # Get the attribute value
                    respState,respCode,respVal = AT.getAttribute(myNodeId, ep, clustId, attrId, clustType)
                    if respState and respCode==zcl.statusCodes['SUCCESS']:
                        attrVal = respVal
                            
                        # Get the reporting intervals for the attribute
                        respState,respCode,attrReport = AT.getAttributeReporting(myNodeId, ep, clustId, clustType, attrId)
#                         if not respState:
#                             attrReport = "Problem reading reporting config. {}".format(attrReport)
#                         if respState and respCode!=zcl.statusCodes['SUCCESS']:
#                             attrReport = "Problem reading reporting config. {}".format(zcl.lookupStatusCode(respCode))

                        if respState and respCode == zcl.statusCodes['SUCCESS']:
                            print("{0},{1},{2:32},{3:20},{4}".format(attrId, attrType, zclAttrName, attrVal,attrReport))
                            if attrType != zclAttrType: print("TYPE ERROR in zigbeeCluster Library !!!!!!!!!!!!!!!")
                        else:
                            myRespCode = zcl.lookupStatusCode(respCode)
                            if respCode == zcl.statusCodes['ZCL_NOT_FOUND']:
                                print("{0},{1},{2:32},{3:20},Attribute reporting not set".format(attrId,
                                                                                                 attrType,
                                                                                                 zclAttrName,
                                                                                                 attrVal))
                            elif respCode == zcl.statusCodes['ZCL_UNREPORTABLE_ATTRIBUTE']:
                                print('{0},{1},{2:32},{3:20},ZCL_UNREPORTABLE_ATTRIBUTE'.format(attrId,
                                                                                                     attrType,
                                                                                                     zclAttrName,
                                                                                                     attrVal))
                                
                            else:
                                print('{0},{1},{2:32},{3:20},**** PROBLEM,{4},{5}'.format(attrId,
                                                                                          attrType,
                                                                                          zclAttrName,
                                                                                          attrVal,
                                                                                          respVal,
                                                                                          myRespCode))
                            if attrType != zclAttrType: print("TYPE ERROR in zigbeeCluster Library !!!!!!!!!!!!!!!")
                    
                    else:
                        myRespCode = zcl.lookupStatusCode(respCode)
                        print('{0},{1},{2:32},{3:20},**** PROBLEM,{4},{5}'.format(attrId,
                                                                                  attrType,
                                                                                  zclAttrName,
                                                                                  "??",
                                                                                  respVal,
                                                                                  myRespCode))
                    attrIdNode = attrId + "_" + zclAttrName
                    oListOfAttributes[attrIdNode] = {}
                    oListOfAttributes[attrIdNode]["AttributeID"] = attrId
                    oListOfAttributes[attrIdNode]["AttributeName"] = zclAttrName
                    oListOfAttributes[attrIdNode]["AttributeType"] = zclAttrType
                    oListOfAttributes[attrIdNode]["DefaultValue"] = attrVal
                    if respCode == zcl.statusCodes['ZCL_UNREPORTABLE_ATTRIBUTE']: attrReport = "ZCL_UNREPORTABLE_ATTRIBUTE"
                    oListOfAttributes[attrIdNode]["ReportableConfigState"] = attrReport
                    
                    
                oListOfClusters[clustIdNode]["ListOfAttributes"] = oListOfAttributes        
            else:
                print("Problem with attribute discovery: ", respValue)
                exit()
    
        oListOfEP[ep]["ListOfClusters"] = oListOfClusters
    oBSJson["ListOfEndPoints"] = oListOfEP

    strAttrDumpFolderPAth = os.path.abspath(strEnvironmentFolderPAth + "/Device_Attribute_Dumps/")
    if boolUpdateBaseline:
        strDumpJsonFileName = modelID +  "_Baseline_Dump.json"     
        strDumpJsonFileNamePath = os.path.abspath(strAttrDumpFolderPAth + '/' + strDumpJsonFileName)
        oJson = open(strDumpJsonFileNamePath, mode='w')
        oJson.write(json.dumps(oBSJson, indent=4, sort_keys=True))
        oJson.close()
    strDumpJsonFileName = modelID + "_" + deviceVersion +"_Dump.json"
    strLatAttrDumpFolderPAth = strEnvironmentFolderPAth + "/Latest_Attribute_Dump/"
    strDumpJsonFileNamePath = os.path.abspath(strLatAttrDumpFolderPAth + strDumpJsonFileName)
    oJson = open(strDumpJsonFileNamePath, mode='w')
    oJson.write(json.dumps(oBSJson, indent=4, sort_keys=True))
    oJson.close()
    
    return 0

def getJSONObjectFromFile(context,baselineDumpFile, latestDumpFile):
    oJson = open(baselineDumpFile, mode='r')
    oBSDumpJson = json.loads(oJson.read())
    context.BaseDumpJson = oBSDumpJson
    oJson.close() 
    
    oJson = open(latestDumpFile, mode='r')
    oLatestDumpJson = json.loads(oJson.read())
    context.TestDumpJson = oLatestDumpJson
    oJson.close() 

def getDeviceVersion(myNodeId):
    # Retrieve and display the endpoints
    respState,respCode,endpoints =AT.discEndpoints(myNodeId)
    endpoints.sort()
    if respState and respCode==zcl.statusCodes['SUCCESS']:
        print("Endpoints: {0}".format(endpoints))
    else:
        print('Error finding endpoints')
    
    deviceVersion = get_device_version(myNodeId, endpoints[0])[2]
    return deviceVersion

def getDeviceModeId(myNodeId):
    # Retrieve and display the endpoints
    respState,respCode,endpoints =AT.discEndpoints(myNodeId)
    endpoints.sort()
    if respState and respCode==zcl.statusCodes['SUCCESS']:
        print("Endpoints: {0}".format(endpoints))
    else:
        print('Error finding endpoints')
    
    modelID = getModelforDevice(myNodeId, endpoints[0])
    
    return modelID


def validateDumpJsonAndReport(context,reporter, baselineDumpFile, latestDumpFile):
    
    oJson = open(baselineDumpFile, mode='r')
    oBSDumpJson = json.loads(oJson.read())
    context.BaseDumpJson = oBSDumpJson
    oJson.close() 
    
    oJson = open(latestDumpFile, mode='r')
    oLatestDumpJson = json.loads(oJson.read())
    context.TestDumpJson = oLatestDumpJson
    oJson.close() 
    
    
    print(oBSDumpJson["DeviceVersion"])
    
    
    strHeader = "Cluster$$"  + "Attribute ID$$" + "Attribute Name$$" + "Attribute Type$$" +"Default Value$$" + " ReportableConfigState$$" + "@@@"
    strLog = ""   
    
    for ep in sorted(oBSDumpJson["ListOfEndPoints"].keys()):
        oEP = oBSDumpJson["ListOfEndPoints"][ep]
        context.ep = oEP
        strExpEndPoint = oEP["EndPoint"]
        for oClust in sorted(oEP["ListOfClusters"].keys()):
            oClust = oEP["ListOfClusters"][oClust]
            strExpClusterID = oClust["ClusterID"]
            strExpClusterName = oClust["ClusterName"]
            strExpClusterTYpe = oClust["ClusterType"]
            if strExpClusterID + "_" + strExpClusterName in oLatestDumpJson["ListOfEndPoints"][ep]["ListOfClusters"]: 
                oActClust = oLatestDumpJson["ListOfEndPoints"][ep]["ListOfClusters"][strExpClusterID + "_" + strExpClusterName]            
                strActClusterID = oActClust["ClusterID"]
                strActClusterName = oActClust["ClusterName"]
                strActClusterTYpe = oActClust["ClusterType"]
            else:
                oActClust = oClust
                strExpClusterID = "||" + strExpClusterID
            if strExpClusterTYpe != strActClusterTYpe:
                strExpClusterTYpe = "||" + strExpClusterTYpe +" ==> " + strActClusterTYpe
            
            boolFirstAttr = True
            for oAttr in sorted(oClust["ListOfAttributes"].keys()):
                oAttr = oClust["ListOfAttributes"][oAttr]
                strExpAttrID = oAttr["AttributeID"]
                strExpAttrName = oAttr["AttributeName"]
                strExpAttrType = oAttr["AttributeType"]
                strExpAttrValue = oAttr["DefaultValue"]
                strExpAttrRCS = oAttr["ReportableConfigState"]
                if strExpAttrID + "_" + strExpAttrName in oActClust["ListOfAttributes"]:
                    oActAttr = oActClust["ListOfAttributes"][strExpAttrID + "_" + strExpAttrName]   
                else: 
                    oActAttr = oAttr 
                    strExpAttrID = "||" + strExpAttrID              
                strActAttrName = oActAttr["AttributeName"]
                strActAttrType = oActAttr["AttributeType"]
                strActAttrValue = oActAttr["DefaultValue"]
                strActAttrRCS = oActAttr["ReportableConfigState"]
                
                if strExpAttrType != strActAttrType:
                    strExpAttrType =  "||" + strExpAttrType +" ==> " + strActAttrType
                if strExpAttrValue != strActAttrValue:
                    strExpAttrValue =  "||" + strExpAttrValue +" ==> " + strActAttrValue
                if strExpAttrRCS != strActAttrRCS:
                    strExpAttrRCS =  "||" + strExpAttrRCS +" ==> " + strActAttrRCS
                
                if boolFirstAttr: 
                    strLog = strLog + "$~" +  strExpClusterID + "_" + strExpClusterName + '&R&'+str(len(oClust["ListOfAttributes"])) + "$$" + strExpAttrID + "$$" + strExpAttrName + "$$" + strExpAttrType + "$$" + strExpAttrValue + "$$" + strExpAttrRCS
                else: 
                    if strExpAttrType is not None:
                        strLog = strLog + "$~" + strExpAttrID + "$$" + strExpAttrName + "$$" + strExpAttrType + "$$" + strExpAttrValue + "$$" + strExpAttrRCS
                    else:
                        print("$~" + strExpAttrID + "$$" + strExpAttrName + "$$"  + "$$ \n")
                #strLog = strLog + "$~" + strExpClusterID + "_" + strExpClusterName + "$$" + strExpAttrID + "$$" + strActAttrName + "$$" + strExpAttrType + "$$" + strExpAttrValue + "$$" + strExpAttrRCS
                boolFirstAttr = False
                    
                        
    reporter.ReportEvent('Test Validation', strHeader + strLog, 'Done')
    return oBSDumpJson,oLatestDumpJson

def setAttributeReporting(context,myNodeId, myEp, myClustId, myAttrId, minRep, maxRep, changeRep):
    AT.stopThread.clear()  
    AT.startSerialThreads(context.PORT, config.BAUD, printStatus=False, rxQ=True, listenerQ=True)
    respState,respCode,respValue = AT.setAttributeReporting(myNodeId, myEp, myClustId, myAttrId, minRep, maxRep, changeRep)
    if not respState or respCode != zcl.statusCodes['SUCCESS']:
        context.reporter.ReportEvent('Test Validation',"ERROR: setAttrVal {},{}".format(respCode,respValue) , 'Fail')
        print("ERROR: setAttrVal {},{}".format(respCode,respValue))
    else:
        context.reporter.ReportEvent('Test Validation',"SUCCESS: setAttrVal {},{}".format(respCode,respValue) , 'Pass')
    AT.stopThreads()
    
def sendCommand(cmd,myExpectedResponses,maxAttempts=5,retryTimeout=30):
    """ Sends a command and reads the rxQueue looking for the raw response
        Returns the single line response or a list or responses if the 
        response is a SEQ (multi-row response)
    
    """
    
    intTCStartTime = time.monotonic()
    AT.flushRxQ()
    AT.txQueue.put(cmd)
    myTime = datetime.now().strftime("%H:%M:%S.%f")
    if AT.debug: print("DEBUG Tx: {},  {},Expected Response={}".format(myTime,cmd,myExpectedResponses))
    lastTry = time.time()
    tryCount = 1
    
    # Loop until all retries done
    respValue = ''
    respState = False
    doLoop = True
    
    while doLoop:
        
        # Some message received so do something with it
        if not AT.rxQueue.empty():
            resp = AT.rxQueue.get()
            respState, respCode = AT.matchResponse(resp, myExpectedResponses)
            
            # If it is what we want then exit
            if respState:
                respValue = resp
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
                #print("10s Pause to capture serial traffic after error")
                # Flush the Rx buffer
                #flushRxQ()
                #time.sleep(10)

        # No valid response received so check for retry timeout
        # If yes then retry else do nothing        
        if time.time() > lastTry + retryTimeout:
            if tryCount<maxAttempts:
                # Retry and reset the retry timer
                myMessage = 'Timeout: Re-queue Tx command, {}'.format(cmd)
                myTime = datetime.now().strftime("%H:%M:%S.%f")
                if AT.debug: print("DEBUG Tx: {},  {}".format(myTime,myMessage))
                lastTry = time.time()
                tryCount += 1
                AT.txQueue.put(cmd)
            else:
                # All retries sent. Exit.
                doLoop = False
    
    # Command sent with retries.  No valid response.
    respState = False
    respCode = None
    respValue = "TIMEOUT: sendCommand() timeout"
    '''
    intTCEndTime = time.monotonic()
    strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
    strTCDuration = getDuration(strTCDuration)   
    print("Time taken: " + strTCDuration)'''
    return respState, respCode, respValue

def validateDefaultReporting(context,reporter,oBSDumpJson,oTestDumpJson):
    strLog = ""
    strHeader = "Cluster$$"  + "Attribute ID$$" + "Attribute Name$$" + "Attribute Type$$" +"Default Value$$" + " ReportableConfigState$$" + "@@@"
    
    for ep in sorted(oBSDumpJson["ListOfEndPoints"].keys()):
        oEP = oBSDumpJson["ListOfEndPoints"][ep]
        
        strExpEndPoint = oEP["EndPoint"]
        context.ep = strExpEndPoint
        for oClust in sorted(oEP["ListOfClusters"].keys()):
            oClust = oEP["ListOfClusters"][oClust]
            strExpClusterID = oClust["ClusterID"]
            strExpClusterName = oClust["ClusterName"]
            strExpClusterTYpe = oClust["ClusterType"]
            if strExpClusterID + "_" + strExpClusterName in oTestDumpJson["ListOfEndPoints"][ep]["ListOfClusters"]: 
                oActClust = oTestDumpJson["ListOfEndPoints"][ep]["ListOfClusters"][strExpClusterID + "_" + strExpClusterName]            
                strActClusterID = oActClust["ClusterID"]
                strActClusterName = oActClust["ClusterName"]
                strActClusterTYpe = oActClust["ClusterType"]
            else:
                oActClust = oClust
            
            boolFirstAttr = True
            for oAttr in sorted(oClust["ListOfAttributes"].keys()):
                oAttr = oClust["ListOfAttributes"][oAttr]
                strExpAttrID = oAttr["AttributeID"]
                strExpAttrName = oAttr["AttributeName"]
                strExpAttrType = oAttr["AttributeType"]
                strExpAttrValue = oAttr["DefaultValue"]
                strExpAttrRCS = oAttr["ReportableConfigState"]
                if strExpAttrID + "_" + strExpAttrName in oActClust["ListOfAttributes"]:
                    oActAttr = oActClust["ListOfAttributes"][strExpAttrID + "_" + strExpAttrName]   
                else: 
                    oActAttr = oAttr 
                strActAttrValue = oActAttr["DefaultValue"]
                
                if strExpAttrRCS != "ZCL_UNREPORTABLE_ATTRIBUTE":
                    if strExpAttrValue != strActAttrValue:
                        strExpAttrValue =  "||" + strExpAttrValue +" ==> " + strActAttrValue
                        strLog = strLog + "$~" +  strExpClusterID + "_" + strExpClusterName + '&R&1' + "$$" + strExpAttrID + "$$" + strExpAttrName + "$$" + strExpAttrType + "$$" + strExpAttrValue + "$$" + strExpAttrRCS
                        reporter.ReportEvent('Test Validation',strHeader + strLog , 'Fail')
                    else:
                        strLog = strLog + "$~" +  strExpClusterID + "_" + strExpClusterName + '&R&1'+ "$$" + strExpAttrID + "$$" + strExpAttrName + "$$" + strExpAttrType + "$$" + strExpAttrValue + "$$" + strExpAttrRCS
                        
                
                boolFirstAttr = False
    print(strLog + "\n")
    reporter.ReportEvent('Test Validation',strHeader + strLog , 'Pass')

def getBindingClusters(context,oBSDumpJson,oTestDumpJson):
    bindingClusterId=[]
    intCounter = 0 
    repAttributeAndClusterId = []
    repAttributeAndClusterId.append([])
    
    for ep in sorted(oBSDumpJson["ListOfEndPoints"].keys()):
        oEP = oBSDumpJson["ListOfEndPoints"][ep]
        for oClust in sorted(oEP["ListOfClusters"].keys()):
            oClust = oEP["ListOfClusters"][oClust]
            strExpClusterID = oClust["ClusterID"]
            strExpClusterName = oClust["ClusterName"]
            if strExpClusterID + "_" + strExpClusterName in oTestDumpJson["ListOfEndPoints"][ep]["ListOfClusters"]: 
                oActClust = oTestDumpJson["ListOfEndPoints"][ep]["ListOfClusters"][strExpClusterID + "_" + strExpClusterName]          
                strActClusterID = oActClust["ClusterID"]
            else:
                oActClust = oClust
                strExpClusterID = "||" + strExpClusterID
            boolFlag = True
            boolFirstAttr = True
            for oAttr in sorted(oClust["ListOfAttributes"].keys()):
                oAttr = oClust["ListOfAttributes"][oAttr]
                strExpAttrID = oAttr["AttributeID"]
                strExpAttrType = oAttr["AttributeType"]
                strExpAttrName = oAttr["AttributeName"]
                strExpAttrRCS = oAttr["ReportableConfigState"]
                if strExpAttrID + "_" + strExpAttrName in oActClust["ListOfAttributes"]:
                    oActAttr = oActClust["ListOfAttributes"][strExpAttrID + "_" + strExpAttrName]   
                else: 
                    oActAttr = oAttr 
                    strExpAttrID = "||" + strExpAttrID     
                
                if strExpAttrRCS != "ZCL_UNREPORTABLE_ATTRIBUTE":
                    if boolFlag:
                        bindingClusterId.append(strActClusterID)
                        print("Counter ------"+strActClusterID+"--**********---")
                        boolFlag = False
                    print("Counter ------"+strActClusterID+"-------" + str(intCounter))
                    #repAttributeAndClusterId.insert(intCounter, ["","",""])
                    repAttributeAndClusterId.append([])
                    repAttributeAndClusterId[intCounter].append(strActClusterID)
                    repAttributeAndClusterId[intCounter].append(strExpAttrID)
                    repAttributeAndClusterId[intCounter].append(strExpAttrType)
                    intCounter = intCounter + 1
                
                boolFirstAttr = False
                
    return bindingClusterId,repAttributeAndClusterId

def validateReportingOfAttributes(context):
    AT.stopThread.clear()  
    AT.startSerialThreads(context.PORT, config.BAUD, printStatus=False, rxQ=True, listenerQ=True)
    myClustId = ""
    myAttrId = ""
    myAttrType = ""
    myNodeId = context.nodeId
    myEp = context.ep
    msg = ""
    intCounter = 0
    waitingTime = 15
    boolFalg = True
    for item in context.arrRepAttributeAndClusterId:
        for j in item:
            if intCounter == 0:
                myClustId = j
            elif intCounter == 1:
                myAttrId = j
            elif intCounter == 1:
                myAttrType = j
            intCounter = intCounter + 1
        msg = "REPORTATTR:"+myNodeId+","+myEp+","+myClustId+","+myAttrId+","+myAttrType
        waitAndValidateMessage(context,msg, waitingTime, 1,"Specified")
        intCounter = 0
        
def validateDefaultReportingOfAttributes(context):
    AT.stopThread.clear()  
    AT.startSerialThreads(context.PORT, config.BAUD, printStatus=False, rxQ=True, listenerQ=True)
    myClustId = ""
    myAttrId = ""
    myAttrType = ""
    myNodeId = context.nodeId
    myEp = context.ep
    msg = ""
    intCounter = 0
    waitingTime = 15
    boolFalg = True
    for item in context.arrRepAttributeAndClusterId:
        for j in item:
            if intCounter == 0:
                myClustId = j
            elif intCounter == 1:
                myAttrId = j
            elif intCounter == 1:
                myAttrType = j
            intCounter = intCounter + 1
        msg = "REPORTATTR:"+myNodeId+","+myEp+","+myClustId+","+myAttrId+","+myAttrType
        waitAndValidateMessage(context,msg, waitingTime, 1,"Default")
        intCounter = 0

def waitForMessage(myMsgs,timeout):
    """ Wait for a wanted message.
        Return full message if message arrives, return None if timeout
        
    """
    endTime = time.time() + timeout
    while time.time() < endTime:
        try:
            resp = AT.rxQueue.get(timeout=1)
            if myMsgs in resp:
                print(resp + " = resp\n")
                print(myMsgs + " = Exp\n")
                return resp
            else:
                print(resp + " = not valid for "+myMsgs+"\n")
        except AT.queue.Empty:
            pass
        
    return None

def waitAndValidateMessage(context,msg,waitingTime,repetitionTime,validationType):
    
    intCounter = 0
    myMsgs = msg
    ts = time.time()
    dTs = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    prevDTs = dTs
    
    while intCounter < repetitionTime:
        #print("Expected : MSG : "+myMsgs +"\n")
        resp = waitForMessage(myMsgs, waitingTime)
        if validationType == "Specified":
            if(resp is not None):
                ts = time.time()
                dTs = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                if intCounter == 0:
                    context.reporter.ReportEvent("Test Validation","The attribute is reported at"+dTs,"Pass")
                elif (datetime.strptime(dTs,'%Y-%m-%d %H:%M:%S')-datetime.strptime(prevDTs,'%Y-%m-%d %H:%M:%S')).total_seconds() < waitingTime:
                    context.reporter.ReportEvent("Test Validation","The attribute is reported again at"+dTs,"Fail")
                elif (datetime.strptime(dTs,'%Y-%m-%d %H:%M:%S')-datetime.strptime(prevDTs,'%Y-%m-%d %H:%M:%S')).total_seconds() == waitingTime:
                    context.reporter.ReportEvent("Test Validation","The attribute is reported at"+dTs,"Pass")
                else:
                    context.reporter.ReportEvent("Test Validation", str((datetime.strptime(dTs,'%Y-%m-%d %H:%M:%S')-datetime.strptime(prevDTs,'%Y-%m-%d %H:%M:%S')).total_seconds()) + " Seconds taken","Fail")
            else:
                context.reporter.ReportEvent("Test Validation",str(intCounter)+ " ATTEMPT: The attribute is not reported at "+ dTs,"Fail")
            prevDTs = dTs
        elif validationType == "Default":
            if(resp is not None):
                context.reporter.ReportEvent("Test Validation","The attribute is reported at"+dTs,"Fail")
            else:
                context.reporter.ReportEvent("Test Validation","The attribute is not reported","Pass")
        intCounter = intCounter + 1
        
def readAttribute(strType,nodeId,ep,sendMode,strClusterId,strAttrId):
    if str(strType).upper() == "CLIENT":
        cmd = 'AT+READCATR:{0},{1},{2},{3},{4}'.format(nodeId,ep,sendMode,strClusterId,strAttrId)             
        print(cmd)
        myExpectedResponses=['RESPATTR:{0},{1},{2},{3},{4},(..)'.format(nodeId,
                                                                          ep,
                                                                          strClusterId,
                                                                          strAttrId, '00')]
        respState, respCode, respValue = sendCommand(cmd, myExpectedResponses, 5, 10)
    elif str(strType).upper() == "MANUFACTURER":
        cmd = 'AT+READATR:{0},{1},{2},{3},{4}'.format(nodeId,ep,sendMode,strClusterId,strAttrId)             
        
        print(cmd)
        myExpectedResponses=['RESPATTR:{0},{1},{2},{3},{4},(..)'.format(nodeId,
                                                                          ep,
                                                                          strClusterId,
                                                                          strAttrId, '00')]
        respState, respCode, respValue = sendCommand(cmd, myExpectedResponses, 5, 10)
    return respState, respCode, respValue
        
if __name__ == '__main__':
    pass