'''
Created on 30 Mar 2016

@author: ranganathan.veluswamy
'''
from datetime import timedelta
import time

from behave import *

import FF_Platform_Utils as pUtils
import FF_alertmeApi as ALAPI
import FF_utils as utils
import FF_threadedSerial as AT
import FF_loggingConfig as config


@when(u'The Hub is rebooted via telegesis and validate the time taken for the devices to come Online and repeated infinitely')
def validateDeviceUptimeInfintely(context):
    
    global oDevicePresenceJson
    oDevicePresenceJson = {}
    intCntr = 0
    while True:        
        intCntr = intCntr + 1
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Hub Power Cycle Counter : ' + str(intCntr))   
        oDevicePresenceJson = resetDeviceListPresenceJson(context)
        
        #ReebootHub
        power_cycle_hub(context)
        time.sleep(60)
        '''ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
        session  = ALAPI.sessionObject()
        hubID = pUtils.getHubNodeID()
        ALAPI.rebootHubV6(session, hubID)
        ALAPI.deleteSessionV6(session)'''
        
        intTCStartTime = time.monotonic()
        intLoopCntr = 0
        flag = False
        intAbsentCounter = 0
        flagHubPresence = True
        flagDevicePresence = True
        for oRow in context.table:
            while intLoopCntr < 360:
                deviceType = oRow['DeviceType']
                context.reporter.ReportEvent("Test Validation", "Device Presence at this time is : <B>" + pUtils.getDevicePresence(deviceType).upper() + "</B>", "DONE")
                if not flag:
                    print(pUtils.getDevicePresence(deviceType).upper())
                    if "PRESENT" in pUtils.getDevicePresence(deviceType).upper():
                        print(pUtils.getDevicePresence(deviceType).upper())
                        intTCEndTime = time.monotonic()
                        strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
                        strTCDuration = utils.getDuration(strTCDuration)
                        oDevicePresenceJson[deviceType]["timeTakenToGetOnline"] = strTCDuration
                        oDevicePresenceJson[deviceType]["presence"] = True
                    else:
                        flag = True
                        intTCEndTime = time.monotonic()
                        strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
                        strTCDuration = utils.getDuration(strTCDuration)
                        oDevicePresenceJson[deviceType]["timeTakenToGetOnline"] = strTCDuration
                        oDevicePresenceJson[deviceType]["presence"] = True
                else:
                    intAbsentCounter = intAbsentCounter + 1
                    print("inner" + pUtils.getDevicePresence(deviceType).upper())
                    print("Hub Status "+ pUtils.getDevicePresence("NANO2").upper())
                    context.reporter.ReportEvent("Test Validation","Hub Status <B>"+ pUtils.getDevicePresence("NANO2").upper() + "</B>","Done")
                    if pUtils.getDevicePresence("NANO2").upper() == "PRESENT":
                        if "PRESENT" in pUtils.getDevicePresence(deviceType).upper():
                            if flagHubPresence:
                                time.sleep(180)
                                flagHubPresence = False
                            if flagDevicePresence:    
                                intLoopCntr = 350
                                flagDevicePresence = False
                        else:
                            flag = True
                            intAbsentCounter = intAbsentCounter + 1
                            if intAbsentCounter > 20:
                                context.reporter.ReportEvent("Test Validation", "Terminated", "DONE")
                                exit()
            time.sleep(10)
            intLoopCntr = intLoopCntr + 1
        
        
        for oKey in oDevicePresenceJson.keys():
            context.reporter.ReportEvent("Test Validation", "Device Type : <B>" + oKey + "</B>", "DONE")
            context.reporter.ReportEvent("Test Validation", "Device Presence : <B>" + str(oDevicePresenceJson[oKey]["presence"]) + "</B>", "DONE")
            context.reporter.ReportEvent("Test Validation", "Time taken to come Online : <B>" + str(oDevicePresenceJson[oKey]["timeTakenToGetOnline"]) + "</B>", "DONE")

def resetDeviceListPresenceJson(context):
    oDevicePresenceJson = {}    
    for oRow in context.table:
        deviceType = oRow['DeviceType']
        oDevicePresenceJson[deviceType] = {}
        oDevicePresenceJson[deviceType]["presence"] = False
        oDevicePresenceJson[deviceType]["timeTakenToGetOnline"] = ""
    return oDevicePresenceJson
#Power cycle the HUB
def power_cycle_hub(context):      
    strPORT = utils.get_Port_Id_TG()        
    if not strPORT == "":
        AT.stopThread.clear()  
        AT.startSerialThreads("/dev/" + strPORT, config.BAUD, printStatus=False, rxQ=True, listenerQ=True)
        respState,_,resp = utils.discoverNodeIDbyCluster('0006')
        if respState:
            utils.setSPOnOff(myNodeId = resp, strOnOff = 'OFF', boolZigbee = True)
            context.reporter.ReportEvent("Test Validation", "Hub is turned OFF", "DONE")
            time.sleep(300)                            
            utils.setSPOnOff(myNodeId = resp, strOnOff = 'ON', boolZigbee = True)
            context.reporter.ReportEvent("Test Validation", "Hub is turned ON", "DONE")
            time.sleep(10)
        AT.stopThreads() 

@when(u'The Hub is rebooted via telegesis and validate the time taken for the devices to come Online')
def validateDeviceUptime(context):
    
    global oDevicePresenceJson
    oDevicePresenceJson = {}
    intCntr = 0   
    intCntr = intCntr + 1
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Hub Power Cycle Counter : ' + str(intCntr))   
    oDevicePresenceJson = resetDeviceListPresenceJson(context)
    
    #ReebootHub
    power_cycle_hub(context)
    time.sleep(60)
    '''ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session  = ALAPI.sessionObject()
    hubID = pUtils.getHubNodeID()
    ALAPI.rebootHubV6(session, hubID)
    ALAPI.deleteSessionV6(session)'''
    
    intTCStartTime = time.monotonic()
    intLoopCntr = 0
    flag = False
    intAbsentCounter = 0
    flagHubPresence = True
    flagDevicePresence = True
    for oRow in context.table:
        while intLoopCntr < 360:        
            deviceType = oRow['DeviceType']
            context.reporter.ReportEvent("Test Validation", "Device Presence at this time is : <B>" + pUtils.getDevicePresence(deviceType).upper() + "</B>", "DONE")
            if not flag:
                print(pUtils.getDevicePresence(deviceType).upper())
                if "PRESENT" in pUtils.getDevicePresence(deviceType).upper():
                    print(pUtils.getDevicePresence(deviceType).upper())
                    intTCEndTime = time.monotonic()
                    strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
                    strTCDuration = utils.getDuration(strTCDuration)
                    oDevicePresenceJson[deviceType]["timeTakenToGetOnline"] = strTCDuration
                    oDevicePresenceJson[deviceType]["presence"] = True
                else:
                    flag = True
                    intTCEndTime = time.monotonic()
                    strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
                    strTCDuration = utils.getDuration(strTCDuration)
                    oDevicePresenceJson[deviceType]["timeTakenToGetOnline"] = strTCDuration
                    oDevicePresenceJson[deviceType]["presence"] = True
            else:
                intAbsentCounter = intAbsentCounter + 1
                print("inner" + pUtils.getDevicePresence(deviceType).upper())
                print("Hub Status "+ pUtils.getDevicePresence("NANO2").upper())
                context.reporter.ReportEvent("Test Validation","Hub Status <B>"+ pUtils.getDevicePresence("NANO2").upper() + "</B>","Done")
                if pUtils.getDevicePresence("NANO2").upper() == "PRESENT":
                    if "PRESENT" in pUtils.getDevicePresence(deviceType).upper():
                        if flagHubPresence:
                            time.sleep(180)
                            flagHubPresence = False
                        if flagDevicePresence:    
                            intLoopCntr = 350
                            flagDevicePresence = False
                    else:
                        flag = True
                        intAbsentCounter = intAbsentCounter + 1
                        if intAbsentCounter > 20:
                            context.reporter.ReportEvent("Test Validation", "Terminated", "DONE")
                            exit()
        time.sleep(10)
        intLoopCntr = intLoopCntr + 1
    
    
    for oKey in oDevicePresenceJson.keys():
        context.reporter.ReportEvent("Test Validation", "Device Type : <B>" + oKey + "</B>", "DONE")
        context.reporter.ReportEvent("Test Validation", "Device Presence : <B>" + str(oDevicePresenceJson[oKey]["presence"]) + "</B>", "DONE")
        context.reporter.ReportEvent("Test Validation", "Time taken to come Online : <B>" + str(oDevicePresenceJson[oKey]["timeTakenToGetOnline"]) + "</B>", "DONE")

@when(u'The device is untouched and validate the presence status of the devices infinitely')
def validatePresence(context):
    global oDevicePresenceJson
    oDevicePresenceJson = {}
    oDevicePresenceJson = resetDeviceListPresenceJson(context)
    intTCStartTime = time.monotonic()
    intLoopCntr = 0
    for oRow in context.table:
        deviceType = oRow['DeviceType']
        while True:        
            context.reporter.HTML_TC_BusFlowKeyword_Initialize('Verification counter : ' + str(intLoopCntr))  
            if "PRESENT" in pUtils.getDevicePresence(deviceType).upper():
                print(pUtils.getDevicePresence(deviceType).upper())
                intTCEndTime = time.monotonic()
                strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
                strTCDuration = utils.getDuration(strTCDuration)
                oDevicePresenceJson[deviceType]["timeTakenToGetOnline"] = strTCDuration
                oDevicePresenceJson[deviceType]["presence"] = True
                context.reporter.ReportEvent("Test Validation", "Device Presence at this time is : <B>" + pUtils.getDevicePresence(deviceType).upper() + "</B>", "Pass")
            else:
                intTCEndTime = time.monotonic()
                strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
                strTCDuration = utils.getDuration(strTCDuration)
                oDevicePresenceJson[deviceType]["timeTakenToGetOnline"] = strTCDuration
                oDevicePresenceJson[deviceType]["presence"] = True
                context.reporter.ReportEvent("Test Validation", "Device Presence at this time is : <B>" + pUtils.getDevicePresence(deviceType).upper() + "</B>", "Fail")
            time.sleep(10)
            intLoopCntr = intLoopCntr + 1
    
    