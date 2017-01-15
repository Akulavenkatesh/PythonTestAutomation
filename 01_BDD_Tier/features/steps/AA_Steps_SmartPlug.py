'''
Created on 19 Jan 2016

@author: ranganathan.veluswamy
'''

import time

from behave import *

import FF_ScheduleUtils as SchUtils
import FF_alertmeApi as ALAPI
import FF_utils as utils
import FF_Platform_Utils as pUtils
from asyncio.tasks import sleep
import FF_device_utils as dutils

@given(u'The {} are paired with the Hive Hub')
def setUpSmartPlugs(context, device):
    #get device versions
    oDeviceVersionList = pUtils.getNodeAndDeviceVersionID()
    print(device)
    print(oDeviceVersionList, "\n")
    
@when(u'The schedule for the below smart plugs are set and continuously validated via Hub')
def setSPSchedulesAndValidateViaHub(context):
    
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session  = ALAPI.sessionObject()
    #get node lists
    oDeviceNodeVersionList = getNodeAndDeviceVersionID()

    oDeviceDetails = {}
    intCntr = 1
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Continuous Schedule Test Week: ' + str(intCntr))   
    for oRow in context.table:
        SmartPlug = oRow['SmartPlug']
        intNoOfEvents = int(oRow['NoOfEvents'])
        
        oDeviceDetails[SmartPlug] = {}
        oDeviceDetails[SmartPlug]["id"] = SmartPlug
        oDeviceDetails[SmartPlug]["noOfEvents"] = intNoOfEvents
        oDeviceDetails[SmartPlug]["nodeId"] = oDeviceNodeVersionList[SmartPlug]["nodeID"]
        oDeviceDetails[SmartPlug]["syntheticID"] = getSyntheticDeviceID(oDeviceNodeVersionList[SmartPlug]["nodeID"])
        print('oDeviceNodeVersionList[SmartPlug]["nodeID"]', oDeviceNodeVersionList[SmartPlug]["nodeID"])
        print("syntheticID", oDeviceDetails[SmartPlug]["syntheticID"])
        
        
        payload, oSPSchedDict = SchUtils.createScheduleForSP(intNoOfEvents)
        print(oSPSchedDict, "\n")
        context.oSPSchedDict = oSPSchedDict
        context.SPNodeID = oDeviceDetails[SmartPlug]["nodeId"]
        r,success = ALAPI.setScheduleSP(session, oDeviceDetails[SmartPlug]["syntheticID"], payload)
        print(r,success)
    ALAPI.deleteSessionV6(session)
    

    SchUtils.runSPValidationForWeekSchedule(context)

    '''while True:
        intCntr = intCntr + 1
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Continuous Schedule Test Week: ' + str(intCntr))   
        for oRow in context.table:
            SmartPlug = oRow['SmartPlug']
            intNoOfEvents = int(oRow['NoOfEvents'])
            
            payload, oScheduleDict = SchUtils.createScheduleForSP(intNoOfEvents)
            
            # ALAPI.setScheduleSP(session, nodeId, payload)'''
            


#Get the Node ID for the given device type
def getNodeAndDeviceVersionID():
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session  = ALAPI.sessionObject()
    resp = ALAPI.getNodesV6(session)
    oDeviceDetails = {}
    for oNode in resp['nodes']:
        if ('supportsHotWater'  not in oNode['attributes']) and "nodeType" in oNode:
            if '.json' in oNode["nodeType"] and "model" in oNode["attributes"]:
                if "reportedValue" in oNode["attributes"]["model"]:
                    strModel = oNode["attributes"]["model"]["reportedValue"]
                    strModelTemp = strModel
                    intDeviceCntr = 0
                    while True:
                        intDeviceCntr = intDeviceCntr + 1
                        strModel = strModelTemp + "_" + str(intDeviceCntr)
                        if strModel in oDeviceDetails: continue
                        else: break
                        
                    oDeviceDetails[strModel] = {}
                    strName = ""
                    oDeviceDetails[strModel]["nodeID"] = oNode["id"]
                    if "name" in oNode: strName = oNode["name"]
                    oDeviceDetails[strModel]["name"] = strName
                    oDeviceDetails[strModel]["version"] = oNode["attributes"]["softwareVersion"]["reportedValue"]
            elif "hardwareVersion" in oNode["attributes"]:
                strHubModel = oNode["attributes"]["hardwareVersion"]["reportedValue"]
                if "NANO" in strHubModel:
                    oDeviceDetails[strHubModel] = {}
                    oDeviceDetails[strHubModel]["nodeID"] = oNode["id"]
                    oDeviceDetails[strHubModel]["version"] = oNode["attributes"]["softwareVersion"]["reportedValue"]
    return oDeviceDetails
    ALAPI.deleteSessionV6(session)
    
    
    #Get the synthetic Node ID for the given device node ID
def getSyntheticDeviceID(nodeID):
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session  = ALAPI.sessionObject()
    resp = ALAPI.getNodesV6(session)
    strSyntheticDeviceID = ""
    for oNode in resp['nodes']:
        if "nodeType" in oNode:
            if '.json' in oNode["nodeType"] and "consumers" in oNode["attributes"]:
                strConsumersID = oNode["attributes"]["consumers"]["reportedValue"]
                print("strConsumersID", strConsumersID)
                if nodeID in strConsumersID:
                    strSyntheticDeviceID = oNode["id"]
                    break
    ALAPI.deleteSessionV6(session)       
    return strSyntheticDeviceID


def getAttribute(oAttributeList, strAttributeName):
    reported = oAttributeList[strAttributeName]['reportedValue']
    if 'targetValue' in oAttributeList[strAttributeName]:
        target =  oAttributeList[strAttributeName]['targetValue']
        targetTime = oAttributeList[strAttributeName]['targetSetTime']
        currentTime = int(time.time() * 1000)
        if ((currentTime - targetTime) < 40000): 
            print('taken target value for', strAttributeName)
            return target;
    return reported;
    
#Get SP Attributes
def getSPAttributes(nodeID):
    strMode = ""
    strState = ""
    syntheticNodeID = getSyntheticDeviceID(nodeID)
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session  = ALAPI.sessionObject()
    resp = ALAPI.getNodesV6(session)
    for oNode in resp['nodes']:
        if nodeID in oNode["id"]:
            strState = getAttribute(oNode["attributes"], "state")
        elif oNode["id"] in syntheticNodeID:
            if getAttribute(oNode["attributes"]["syntheticDeviceConfiguration"], "enabled").upper() == "TRUE":
                strMode = "AUTO"
                strMode = "MANUAL"
    
    return strMode, strState
    
@when(u'the {strDeviceType} state is changed to below states and validated using the zigbee attribute and repeated infinitely')
def onOFFValidation(context,strDeviceType):
    context.nodeId = ""
    context.ep = ""
    myNodeId = ""
    myEp = ""
    
    intCntr = 0
    while True:
        intCntr = intCntr + 1
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('ON-OFF Counter : ' + str(intCntr))   
        if str(strDeviceType).upper() == "SMARTPLUG":
            for oRow in context.table:
                DeviceType = ""
                NodeID = ""
                if str(oRow['DeviceType']).upper() == "GENERIC":
                    DeviceName = utils.getAttribute("COMMON", "mainClient", None, None)
                    #NodeID = dutils.getNodeIDbyDeciveID(DeviceName, False)
                    oJson = dutils.getDeviceNode(DeviceName, False)
                    MAcID = oJson['macID']
                    DeviceType = oJson['name']
                    myNodeId =  oJson['nodeID']
                    context.nodeId = myNodeId
                    myEp = oJson["endPoints"][0]
                else:
                    DeviceName = oRow['DeviceName']
                    DeviceType = oRow['DeviceType']
                    MAcID = oRow['MacID']                    
                    myNodeId = utils.get_device_node_from_ntable(MAcID)
                    myEp = "09"
                print(DeviceName, DeviceType, myNodeId, MAcID, "\n")
                strExp = ""
                strOpp = ""
                if str(oRow['State']).upper() == "OFF":
                    strExp = "00"
                    strOpp = "01"
                    strOppText = "ON"
                elif str(oRow['State']).upper() == "ON":
                    strExp = "01"
                    strOpp = "00"
                    strOppText = "OFF"
                else:
                    context.report().ReportEvent("Test Validation","Invalid State","FAIL")
                    exit()
                utils.setSPOnOff(myNodeId, oRow['State'], True)
                intCounter = 0
                context.reporter.ReportEvent("Test Validation","Smart Plug state is set to "+oRow['State'],"DONE")
                while intCounter < 6:
                    
                    respState, respCode, respValue = utils.readAttribute("MANUFACTURER", myNodeId, myEp, 0, "0006", "0000")
                    if respValue == "RESPATTR:"+myNodeId+","+myEp+",0006,0000,00,"+strExp:
                        context.reporter.ReportEvent("Test Validation","Current smart Plug state is "+oRow['State'],"PASS")
                    elif respValue == "RESPATTR:"+myNodeId+","+myEp+",0006,0000,00,01":
                        context.reporter.ReportEvent("Test Validation","Current smart Plug state is "+strOppText,"FAIL")
                    elif respValue == "RESPATTR:"+myNodeId+","+myEp+",0006,0000,86":
                        context.reporter.ReportEvent("Test Validation","Attribute is unreadable","FAIL")
                    else:
                        context.reporter.ReportEvent("Test Validation","Unexpected response: "+respValue,"FAIL")
                    time.sleep(10)
                    intCounter += 1