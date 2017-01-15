'''
Created on 27 Jan 2016

@author: ranganathan.veluswamy

@author: Hitesh Sharma 10 Aug 2016
@note: added functions getSyntheticDeviceID - get the synthetic device id for CS, getCSAttributes - get the CS attributes, getAttribute- get the current state for CS from platform
@note: 13 Sept 2016 - added functions getTHENValueAndDurationForRecipe, getLightBulbAttributes and getColourTemprature for recipes and light bulb
'''


import collections
import json
import time
import FF_alertmeApi as ALAPI
import FF_utils as utils


oWeekDayList = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    
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
                    oDeviceDetails[strModel]["presence"] = oNode["attributes"]["presence"]["reportedValue"]
            elif "hardwareVersion" in oNode["attributes"]:
                strHubModel = oNode["attributes"]["hardwareVersion"]["reportedValue"]
                if "NANO" in strHubModel:
                    oDeviceDetails[strHubModel] = {}
                    oDeviceDetails[strHubModel]["nodeID"] = oNode["id"]
                    oDeviceDetails[strHubModel]["version"] = oNode["attributes"]["softwareVersion"]["reportedValue"]
                    oDeviceDetails[strHubModel]["presence"] = oNode["attributes"]["presence"]["reportedValue"]
    ALAPI.deleteSessionV6(session)
    return oDeviceDetails

#Get the Nodes 
def getNodes():
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session  = ALAPI.sessionObject()
    nodes = ALAPI.getNodesV6(session)
    ALAPI.deleteSessionV6(session)
    return nodes

#Get the Nodes for specific Node ID
def getNodeByID(nodeID):
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session  = ALAPI.sessionObject()
    nodes = ALAPI.getNodesByIDV6(session, nodeID)
    ALAPI.deleteSessionV6(session)
    return nodes

def getHubNodeID():
    oNodeIDList = getNodeAndDeviceVersionID()
    oKeyList = oNodeIDList.keys()
    oHubNodeID = oNodeIDList[searchSubStringInList(oKeyList, "NANO")[0]]["nodeID"]
    return oHubNodeID

def getDeviceNodeID(deviceType):
    oDeviceNodeID = ""
    oNodeIDList = getNodeAndDeviceVersionID()
    oKeyList = oNodeIDList.keys()
    oSearchedList = searchSubStringInList(oKeyList, deviceType) 
    if len(oSearchedList) > 0:
        strKey = oSearchedList[0]
        oDeviceNodeID = oNodeIDList[strKey]["nodeID"]
    return oDeviceNodeID

def getDeviceName(deviceType):
    oDeviceName = ""
    oNodeIDList = getNodeAndDeviceVersionID()
    oKeyList = oNodeIDList.keys()
    oSearchedList = searchSubStringInList(oKeyList, deviceType) 
    if len(oSearchedList) > 0:
        strKey = oSearchedList[0]
        oDeviceName = oNodeIDList[strKey]["name"]
    return oDeviceName


def getDeviceVersion(deviceType):
    oDeviceVersion = ""
    oNodeIDList = getNodeAndDeviceVersionID()
    oKeyList = oNodeIDList.keys()
    oSearchedList = searchSubStringInList(oKeyList, deviceType) 
    if len(oSearchedList) > 0:
        strKey = oSearchedList[0]
        oDeviceVersion = oNodeIDList[strKey]["version"]
    return oDeviceVersion

def getDevicePresence(deviceType):
    oDevicePresence = ""
    oNodeIDList = getNodeAndDeviceVersionID()
    oKeyList = oNodeIDList.keys()
    oSearchedList = searchSubStringInList(oKeyList, deviceType) 
    if len(oSearchedList) > 0:
        strKey = oSearchedList[0]
        oDevicePresence= oNodeIDList[strKey]["presence"]
    return oDevicePresence

def getDeviceSDNodeID(nodeID):
    oSDNodeID = ""
    nodes = getNodes()
    
    for oNode in nodes['nodes']:
        #if ('supportsHotWater'  not in oNode['attributes']) and "nodeType" in oNode:
        if  "nodeType" in oNode:
            if '.json' in oNode["nodeType"]:
                if "consumers" in oNode["attributes"]:
                    if nodeID.upper() in oNode["attributes"]["consumers"]["reportedValue"].upper():
                        
                        oSDNodeID = oNode["id"]
                        break
                
    return oSDNodeID, oNode

def getDeviceSchedule(deviceType):
    nodeID = getDeviceNodeID(deviceType)
    SDNodeID, oNode = getDeviceSDNodeID(nodeID)
    SDConfig = oNode["attributes"]["syntheticDeviceConfiguration"]["reportedValue"]
    
    if isinstance(SDConfig, str): SDConfig = json.loads(SDConfig)
    oSchedule = SDConfig["schedule"]
    
    return oSchedule

def getDeviceScheduleInStandardFormat(deviceType):
    nodeID = getDeviceNodeID(deviceType)
    SDNodeID, oNode = getDeviceSDNodeID(nodeID)
    SDConfig = oNode["attributes"]["syntheticDeviceConfiguration"]["reportedValue"]
    
    if isinstance(SDConfig, str): SDConfig = json.loads(SDConfig)
    oSchedule = SDConfig["schedule"]
    oFormattedched = {}
    for oDaySchedList in oSchedule:
        strDay = oWeekDayList[int(oDaySchedList["dayIndex"]) - 1]
        oTransitions = oDaySchedList["transitions"]
        oSchedList = []
        for oEvent in oTransitions:
            strTime = oEvent["time"]
            strState = oEvent["action"]["state"]
            if "brightness" in oEvent["action"]: 
                intBrightness = oEvent["action"]["brightness"]
                oSchedList.append((strTime, strState, intBrightness))
            else: oSchedList.append((strTime, strState))
        oFormattedched[strDay] = oSchedList
    return oFormattedched

def removeDayFromScheduleAPI(oSchedule, oDayList):
    
    for strDay in oDayList:
        for oDayNode in oSchedule:
            intDayIndex = oDayNode["dayIndex"]
            strDayOnSchd = oWeekDayList[intDayIndex - 1]
            if strDayOnSchd == strDay:
                del oSchedule[oSchedule.index(oDayNode)]
                break
    
    return oSchedule

#Get Light Attributes
def getLightAttributes(nodeID):
    strLightMode = ""
    strLightState = ""
    intLightBrightness = 0
    oNode = getNodeByID(nodeID)
    #print(oNode)
    oNode = oNode["nodes"][0]
    if "model" in oNode["attributes"]: 
        if not "FWBULB" in oNode["attributes"]["model"]["reportedValue"].upper():
            return strLightMode, strLightState, intLightBrightness
    
    #Get State
    strLightState = oNode["attributes"]["state"]["reportedValue"]
    #Get Brightness
    intLightBrightness = int(oNode["attributes"]["brightness"]["reportedValue"])
    #GetMode
    SDNodeID,_ = getDeviceSDNodeID(nodeID)    
    oSDNode = getNodeByID(SDNodeID)    
    SDConfig = oSDNode["nodes"][0]["attributes"]["syntheticDeviceConfiguration"]["reportedValue"]    
    if isinstance(SDConfig, str): SDConfig = json.loads(SDConfig)
    boolSchedule = str(SDConfig["enabled"])
    if "TRUE" in boolSchedule.upper(): strLightMode = "AUTO"
    else: strLightMode = "MANUAL"
    
    return strLightMode, strLightState, intLightBrightness
    
    
  
def searchSubStringInList(oList, strSearchString):
    return [oHeader for oHeader in oList if isinstance(oHeader, collections.Iterable) and (strSearchString in oHeader)]


def getSyntheticDeviceID(nodeID):
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session  = ALAPI.sessionObject()
    resp = ALAPI.getNodesV6(session)
    strSyntheticDeviceID = ""
    for oNode in resp['nodes']:
        if "nodeType" in oNode:
            if '.json' in oNode["nodeType"] and "producers" in oNode["attributes"]:
                strProducerID = oNode["attributes"]["producers"]["reportedValue"]
                print("strProducerID", strProducerID)
                if nodeID in strProducerID:
                    strSyntheticDeviceID = oNode["id"]
                    break
    ALAPI.deleteSessionV6(session)       
    return strSyntheticDeviceID


def getCSAttributes(nodeID):
    finalCSState = ""
    #syntheticNodeID = getSyntheticDeviceID(nodeID)
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session  = ALAPI.sessionObject()
    resp = ALAPI.getNodesV6(session)
    for oNode in resp['nodes']:
        #if "nodeType" in oNode:
            #if '.json' in oNode["nodeType"]:
        if nodeID in oNode["id"]:
            finalCSState = getAttribute(oNode["attributes"], "state")
                #if nodeID in oNode["id"]:
                #finalState = getAttribute(oNode["attributes"], "state")
            print('Reported state for contact sensor is' +  finalCSState )
        else:
            print('Reported state for contact sensor is missing' )    

    return finalCSState

def getColourBulbValues(nodeID,attributeVerify,attributeName):

    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session =ALAPI.sessionObject()
    resp = ALAPI.getNodesV6(session)
    attributeValue = ""
    for oNode in resp['nodes']:
        if nodeID in oNode["id"]:
            attributeValue = oNode["attributes"][attributeVerify][attributeName]
            return (attributeValue)
        else:
            continue

def getAttribute(oAttributeList, strAttributeName):
    csState = oAttributeList[strAttributeName]['reportedValue']
    print(csState)
    return csState;

def getTHENValueAndDurationForRecipe(nodeID):
    finalDuration = ""
    strValue = ""
    syntheticNodeID = getSyntheticDeviceIDForRecipe(nodeID)
    print(syntheticNodeID)
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session  = ALAPI.sessionObject()
    resp = ALAPI.getNodesV6(session)
    for oNode in resp['nodes']:
        if oNode["id"] in syntheticNodeID:          
                tempDuration = oNode["attributes"]["syntheticDeviceConfiguration"]["reportedValue"]
                if isinstance(tempDuration, str): 
                    tempDuration = json.loads(tempDuration) 
                    print(tempDuration, "\n")  
                    finalDuration = tempDuration["action"]["duration"]
                    
                oAction = tempDuration["action"]["action"]
                print(oAction, "\n")
                if isinstance(oAction, str):
                    print("oAction is string")
                changeList = oAction["changes"]
                for newDict in changeList:
                    strValue =newDict["value"]                  
                return finalDuration, strValue
            

def getSyntheticDeviceIDForRecipe(nodeID):
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session  = ALAPI.sessionObject()
    resp = ALAPI.getNodesV6(session)
    strSyntheticDeviceID = ""
    for oNode in resp['nodes']:
        if "nodeType" in oNode:
            if '.json' in oNode["nodeType"] and "producers" in oNode["attributes"]:
                strProducersID = oNode["attributes"]["producers"]["reportedValue"]
                print(strProducersID, "\n")
                                        
                if nodeID in strProducersID:
                    strSyntheticDeviceID = oNode["id"]
                    print(strSyntheticDeviceID)
                    break
    ALAPI.deleteSessionV6(session)       
    return strSyntheticDeviceID

def getLightBulbAttributes(nodeID):
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session =ALAPI.sessionObject()
    resp = ALAPI.getNodesV6(session)
    lightBulbBrigtness = ""
    
    for oNode in resp['nodes']:
        if nodeID in oNode["id"]:
            lightBulbBrigtness = getAttribute(oNode["attributes"], "brightness")         
            print(lightBulbBrigtness, "\n")
        else:
            print("Light bulb brightness value is missing")
    return lightBulbBrigtness

def getColourTemprature(nodeID):
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session =ALAPI.sessionObject()
    resp = ALAPI.getNodesV6(session)
    reportedValue =""
    targetValue = ""
    
    for oNode in resp['nodes']:
        if nodeID in oNode["id"]:
            reportedValue = getAttribute(oNode["attributes"], "colourTemperature")
            targetValue =   getAttribute(oNode["attributes"], "colourTemperature")     
            print(reportedValue, "\n")
            print(targetValue, "\n")
        else:
            print("Light bulb brightness value is missing")
    return reportedValue, targetValue


if __name__ == '__main__':
    pass