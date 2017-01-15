'''
Created on 6 Jan 2016

@author: ranganathan.veluswamy
'''
from datetime import timedelta
import os
import subprocess
import time
import traceback

from behave import *

import DD_Page_iOSApp as paygeiOS
from EE_Locators_iOSApp import HeatingControlPageLocators
import FF_alertmeApi as ALAPI
import FF_threadedSerial as AT
import FF_utils as utils
from asyncio.tasks import sleep
import FF_device_utils as dutils
import AA_Steps_SmartPlug as SP


@given(u'The telegesis is paired with given devices')
def pair_given_devices(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('List of Devices Paired')
    '''respState, nTable, rows = utils.getNtable("FF")
    strNtableHeader = 'No.' +"$$" + 'Dev' +"$$" + 'EUI' +"$$" + 'NodeID' +"$$" + 'LQI'  + '@@@'
    strNtableBody = ""
    intIndex = 0
    
    for oRow in range(3, len(rows)):
        print(oRow)
        arrCell = rows[oRow].split("|")
        strNtableBody = strNtableBody + str(intIndex) + "." +"$$" +  arrCell[1].strip() +"$$" +  arrCell[2].strip() +"$$" +  arrCell[3].strip() +"$$" + arrCell[4].strip() + "$~"
        intIndex = intIndex + 1
    context.reporter.ReportEvent("Test Validation", strNtableHeader + strNtableBody, "PASS", "CENTER")'''

@when(u'the below devices are paired and unpaired sequentially and validated {strCount} via Telegesis')
def pair_unpair_devices(context,strCount):
    intModeListCntr = 0
    intCntr = 0
    intPassCntr = 0
    intFailCntr = 0
    intLoopCtr = 1
    #strCount = ""
    if str(strCount).upper() == "INFINITELY":
        intLoopCtr = 0
    else:
        strCount = strCount.replace(" times","")
        intLoopCtr = int(strCount)
    
    flag = True
    while flag:
        for intIter in range(0 , intLoopCtr):
            intCntr = intCntr + 1
            context.reporter.HTML_TC_BusFlowKeyword_Initialize('Pair-Unpair Counter : ' + str(intCntr))   
            MAcID = ""
            for oRow in context.table:
                NodeID = ""
                DeviceType = ""
                if str(oRow['DeviceType']).upper() == "GENERIC":
                    DeviceName = utils.getAttribute("COMMON", "mainClient", None, None)
                    #NodeID = dutils.getNodeIDbyDeciveID(DeviceName, False)
                    oJson = dutils.getDeviceNode(DeviceName, False)
                    MAcID = oJson['macID']
                    DeviceType = oJson['name']
                    NodeID =  oJson['nodeID']
                else:
                    DeviceName = oRow['DeviceName']
                    DeviceType = oRow['DeviceType']
                    MAcID = oRow['MacID']                    
                    NodeID = utils.get_device_node_from_ntable(MAcID)
                    
                print(DeviceName, DeviceType, NodeID, MAcID, "\n")
                #Unpair the Device from Telegesis
                context.reporter.HTML_TC_BusFlowKeyword_Initialize('Unpair the Device from Telegesis: ' )   
    
                context.reporter.ReportEvent("Test Validation", "NodeID : <B>" + NodeID + "</B>", "Done")
                context.reporter.ReportEvent("Test Validation", "MAcID : <B>" + MAcID + "</B>", "Done")
                
                utils.remove_device_from_network(NodeID)
                time.sleep(30)
                '''time.sleep(5)
                utils.setSPOnOff("DAF8", "OFF")
                time.sleep(2)
                utils.setSPOnOff("DAF8", "ON")
                time.sleep(5)'''
                
                #Pair the Device from Telegesis
                context.reporter.HTML_TC_BusFlowKeyword_Initialize('Pair the Device to Telegesis: ' )  
                print(utils.getTimeStamp(False), "Join Device to the network")
                intStartTime = time.time()
                intTCStartTime = time.monotonic()
                respState,respCode,resp = utils.check_device_joined(MAcID, "FFD", "1E")
                print("respState", respState)
                if respState: 
                    intPassCntr = intPassCntr+1
                    myNodeID = resp
                    time.sleep(60)
                    if str(oRow['DeviceType']).upper() == "GENERIC":
                        oNodeJson = dutils.getZigbeeDevicesJson()
                        oNodeJson[DeviceName]['nodeID'] = myNodeID
                        dutils.putZigbeeDevicesJson(oNodeJson)
                    context.reporter.ReportEvent("Test Validation", "Device Joined the network with Node ID : <B>" + myNodeID + "</B>", "PASS")
                    print("Device Joined the network with Node ID : ", myNodeID)
                else: 
                    intFailCntr = intFailCntr+1
                    context.reporter.ReportEvent("Test Validation", "Join is unsuccessfull", "FAIL")
                    print("join is unsuccessfull")
                    return False
                    '''print("Restarting the Smart Plug")
                    utils.setSPOnOff(NodeID, 'OFF')
                    time.sleep(5)
                    utils.setSPOnOff(NodeID, 'ON')
                    time.sleep(5)'''
                    
                intTCEndTime = time.monotonic()
                strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
                strTCDuration = utils.getDuration(strTCDuration)
                intSeconds = int(strTCDuration.split(",")[1].strip().split(" ")[0])
                if intSeconds >20: strStatus = "FAIL"
                else: strStatus = "PASS"
                context.reporter.ReportEvent("Test Validation", "Time taken: " + strTCDuration, strStatus)
                print("Time taken: ", strTCDuration)
                print('intCntr', intCntr, 'intPassCntr', intPassCntr, 'intFailCntr', intFailCntr)
                print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                print()
                if str(strCount).upper() == "INFINITELY":
                    intIter = 0
                if intIter == intLoopCtr-1:
                    flag = False
                    break
                
@when(u'the selected devices are paired and unpaired sequentially and validated {intCount} times via Telegesis')
def pair_unpair_devices_specific_time(context,intCount):
    intModeListCntr = 0
    intCntr = 0
    intPassCntr = 0
    intFailCntr = 0
    while intCntr < int(intCount):
        intCntr = intCntr + 1
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Pair-Unpair Counter : ' + str(intCntr))   
        
        NodeID = utils.getAttribute("COMMON", "mainClient", None, None)
        MAcID = utils.getAttribute("COMMON", "macID", None, None)
        
        #NodeID = utils.get_device_node_from_ntable(MAcID)
        #print(DeviceName, DeviceType, NodeID, MAcID, "\n")
        #Unpair the Device from Telegesis
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Unpair the Device from Telegesis: ' )   

        context.reporter.ReportEvent("Test Validation", "NodeID : <B>" + NodeID + "</B>", "Done")
        context.reporter.ReportEvent("Test Validation", "MAcID : <B>" + MAcID + "</B>", "Done")
        
        utils.remove_device_from_network(NodeID)
        time.sleep(30)
        '''time.sleep(5)
        utils.setSPOnOff("DAF8", "OFF")
        time.sleep(2)
        utils.setSPOnOff("DAF8", "ON")
        time.sleep(5)'''
        
        #Pair the Device from Telegesis
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Pair the Device to Telegesis: ' )  
        print(utils.getTimeStamp(False), "Join Device to the network")
        intStartTime = time.time()
        intTCStartTime = time.monotonic()
        
        respState,respCode,resp = utils.check_device_joined(MAcID, "FFD", "1E")
        print("respState", respState)
        if respState: 
            intPassCntr = intPassCntr+1
            myNodeID = resp
            utils.setAttribute("COMMON", "mainClient", myNodeID)
            context.reporter.ReportEvent("Test Validation", "Device Joined the network with Node ID : <B>" + myNodeID + "</B>", "PASS")
            print("Device Joined the network with Node ID : ", myNodeID)
            time.sleep(60)
        else: 
            intFailCntr = intFailCntr+1
            context.reporter.ReportEvent("Test Validation", "Join is unsuccessfull", "FAIL")
            print("join is unsuccessfull")
            return False
            '''print("Restarting the Smart Plug")
            utils.setSPOnOff(NodeID, 'OFF')
            time.sleep(5)
            utils.setSPOnOff(NodeID, 'ON')
            time.sleep(5)'''
            
        intTCEndTime = time.monotonic()
        strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
        strTCDuration = utils.getDuration(strTCDuration)
        intSeconds = int(strTCDuration.split(",")[1].strip().split(" ")[0])
        if intSeconds >20: strStatus = "FAIL"
        else: strStatus = "PASS"
        context.reporter.ReportEvent("Test Validation", "Time taken: " + strTCDuration, strStatus)
        print("Time taken: ", strTCDuration)
        print('intCntr', intCntr, 'intPassCntr', intPassCntr, 'intFailCntr', intFailCntr)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print()

@when(u'the below devices are paired and unpaired sequentially on all Zigbee Channels and validated{strDuration}via Telegesis')
def pair_unpair_devices_on_all_channels(context,strDuration):            
    intModeListCntr = 0
    intCntr = 0
    intPassCntr = 0
    intFailCntr = 0
    ZigbeeChannelList = []
    for intChannel in range(11,27):
        ZigbeeChannelList.append(intChannel)
    intTotalChannel = len(ZigbeeChannelList)
    
    
    intLoopCtr = 0
    flag = True
    while flag:
        intCntr = intCntr + 1
        MAcID = ""
        #Get new Channel number
        channelIndex = intCntr % intTotalChannel
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Pair-Unpair Counter : ' + str(intCntr))   
        for oRow in context.table:
            DeviceType = ""
            NodeID = ""
            if str(oRow['DeviceType']).upper() == "GENERIC":
                DeviceName = utils.getAttribute("COMMON", "mainClient", None, None)
                #NodeID = dutils.getNodeIDbyDeciveID(DeviceName, False)
                oJson = dutils.getDeviceNode(DeviceName, False)
                MAcID = oJson['macID']
                DeviceType = oJson['name']
                NodeID =  oJson['nodeID']
            else:
                DeviceName = oRow['DeviceName']
                DeviceType = oRow['DeviceType']
                MAcID = oRow['MacID']                    
                NodeID = utils.get_device_node_from_ntable(MAcID)
            print(DeviceName, DeviceType, NodeID, MAcID, "\n")
            #Unpair the Device from Telegesis
            context.reporter.HTML_TC_BusFlowKeyword_Initialize('Unpair the Device from Telegesis: ' )   

            context.reporter.ReportEvent("Test Validation", "NodeID : <B>" + NodeID + "</B>", "Done")
            context.reporter.ReportEvent("Test Validation", "MAcID : <B>" + MAcID + "</B>", "Done")
            
            utils.remove_device_from_network(NodeID)
            time.sleep(2)
            '''time.sleep(5)
            utils.setSPOnOff("DAF8", "OFF")
            time.sleep(2)
            utils.setSPOnOff("DAF8", "ON")
            time.sleep(5)'''
            
            
            #Reset Telegesis to a new channel
            context.reporter.HTML_TC_BusFlowKeyword_Initialize('Reset Telegesis to a new channel' )
            utils.disassociate_from_pan()
            
            #Establish Network on new channel
            context.reporter.ReportEvent("Test Validation", "Establish Network on the Channel : <B>" + str(ZigbeeChannelList[channelIndex]) + "</B>", "PASS")
            utils.establish_network(ZigbeeChannelList[channelIndex])
            
            #Pair the Device from Telegesis
            context.reporter.HTML_TC_BusFlowKeyword_Initialize('Pair the Device to Telegesis: ' )  
            print(utils.getTimeStamp(False), "Join Device to the network")
            intStartTime = time.time()
            intTCStartTime = time.monotonic()
            
            respState,respCode,resp = utils.check_device_joined(MAcID, "FFD", "1E")
            print("respState", respState)
            if respState: 
                intPassCntr = intPassCntr+1
                myNodeID = resp
                if str(oRow['DeviceType']).upper() == "GENERIC":
                    oNodeJson = dutils.getZigbeeDevicesJson()
                    oNodeJson[DeviceName]['nodeID'] = myNodeID
                    dutils.putZigbeeDevicesJson(oNodeJson)
                context.reporter.ReportEvent("Test Validation", "Device Joined the network with Node ID : <B>" + myNodeID + "</B>", "PASS")
                print("Device Joined the network with Node ID : ", myNodeID)
            else: 
                intFailCntr = intFailCntr+1
                context.reporter.ReportEvent("Test Validation", "Join is unsuccessfull", "FAIL")
                print("join is unsuccessfull")
                return False
                '''print("Restarting the Smart Plug")
                utils.setSPOnOff(NodeID, 'OFF')
                time.sleep(5)
                utils.setSPOnOff(NodeID, 'ON')
                time.sleep(5)'''
                
            intTCEndTime = time.monotonic()
            strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
            strTCDuration = utils.getDuration(strTCDuration)
            intSeconds = int(strTCDuration.split(",")[1].strip().split(" ")[0])
            if intSeconds >20: strStatus = "FAIL"
            else: strStatus = "PASS"
            context.reporter.ReportEvent("Test Validation", "Time taken: " + strTCDuration, strStatus)
            print("Time taken: ", strTCDuration)
            print('intCntr', intCntr, 'intPassCntr', intPassCntr, 'intFailCntr', intFailCntr)
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print()
            time.sleep(60)
            if strDuration.replace(" ","") == "":
                intLoopCtr += 1
                if intLoopCtr > 15:
                    flag = False
                    break
            


@when(u'the selected device is paired and unpaired sequentially on all Zigbee Channels and validated infinitely via Telegesis')
def pair_unpair_selected_device_on_all_channels(context):            
    intModeListCntr = 0
    intCntr = 0
    intPassCntr = 0
    intFailCntr = 0
    ZigbeeChannelList = []
    for intChannel in range(11,27):
        ZigbeeChannelList.append(intChannel)
    intTotalChannel = len(ZigbeeChannelList)
    
    while True:
        intCntr = intCntr + 1
        
        #Get new Channel number
        channelIndex = intCntr % intTotalChannel
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Pair-Unpair Counter : ' + str(intCntr))   
        NodeID = utils.getAttribute("COMMON", "mainClient", None, None)
        MAcID = utils.getAttribute("COMMON", "macID", None, None)
        
        #NodeID = utils.get_device_node_from_ntable(MAcID)
        
        #Unpair the Device from Telegesis
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Unpair the Device from Telegesis: ' )   

        context.reporter.ReportEvent("Test Validation", "NodeID : <B>" + NodeID + "</B>", "Done")
        context.reporter.ReportEvent("Test Validation", "MAcID : <B>" + MAcID + "</B>", "Done")
        
        utils.remove_device_from_network(NodeID)
        time.sleep(2)
        '''time.sleep(5)
        utils.setSPOnOff("DAF8", "OFF")
        time.sleep(2)
        utils.setSPOnOff("DAF8", "ON")
        time.sleep(5)'''
        
        
        #Reset Telegesis to a new channel
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Reset Telegesis to a new channel' )
        utils.disassociate_from_pan()
        
        #Establish Network on new channel
        context.reporter.ReportEvent("Test Validation", "Establish Network on the Channel : <B>" + str(ZigbeeChannelList[channelIndex]) + "</B>", "PASS")
        utils.establish_network(ZigbeeChannelList[channelIndex])
        
        #Pair the Device from Telegesis
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Pair the Device to Telegesis: ' )  
        print(utils.getTimeStamp(False), "Join Device to the network")
        intStartTime = time.time()
        intTCStartTime = time.monotonic()
        
        respState,respCode,resp = utils.check_device_joined(MAcID, "FFD", "1E")
        print("respState", respState)
        if respState: 
            intPassCntr = intPassCntr+1
            myNodeID = resp
            utils.setAttribute("COMMON", "mainClient", myNodeID)
            context.reporter.ReportEvent("Test Validation", "Device Joined the network with Node ID : <B>" + myNodeID + "</B>", "PASS")
            print("Device Joined the network with Node ID : ", myNodeID)
        else: 
            intFailCntr = intFailCntr+1
            context.reporter.ReportEvent("Test Validation", "Join is unsuccessfull", "FAIL")
            print("join is unsuccessfull")
            return False
            
        intTCEndTime = time.monotonic()
        strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
        strTCDuration = utils.getDuration(strTCDuration)
        intSeconds = int(strTCDuration.split(",")[1].strip().split(" ")[0])
        if intSeconds >20: strStatus = "FAIL"
        else: strStatus = "PASS"
        context.reporter.ReportEvent("Test Validation", "Time taken: " + strTCDuration, strStatus)
        print("Time taken: ", strTCDuration)
        print('intCntr', intCntr, 'intPassCntr', intPassCntr, 'intFailCntr', intFailCntr)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print()
        if intCntr >= 15:
            break
        time.sleep(60)
            
@when(u'the below devices are paired and unpaired sequentially and validated infinitely via {HubType} Hub')
def pair_unpair_devices_via_hub(context, HubType):
    HubType = HubType.upper().strip()
    intModeListCntr = 0
    intCntr = 0
    intPassCntr = 0
    intFailCntr = 0
    while True:
        intCntr = intCntr + 1
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Pair-Unpair Counter : ' + str(intCntr))   
        for oRow in context.table:
            DeviceName = oRow['DeviceName']
            DeviceType = oRow['DeviceType']
            #HubType = oRow['HubType']
            #get node lists
            ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
            session  = ALAPI.sessionObject()
            #nodeIdList = context.oThermostatEP.getNodeID(resp)
            nodeIdList = SP.getNodeAndDeviceVersionID()
            if DeviceType in nodeIdList:
                NodeID = nodeIdList[DeviceType]["nodeID"]
                print(DeviceName, DeviceType, NodeID, "\n")
                #Unpair the Device from Telegesis
                context.reporter.HTML_TC_BusFlowKeyword_Initialize('Unpair the Device ' + DeviceType + ' from HUb: ' )   
    
                context.reporter.ReportEvent("Test Validation", "NodeID : <B>" + NodeID + "</B>", "Done")
                
                print(utils.getTimeStamp(False), "Sending Leave request for device")
                ALAPI.deleteDeviceV6(session, NodeID)
                print(utils.getTimeStamp(False), "Wait for 40 seconds")
                time.sleep(90)
            
            '''time.sleep(5)
            utils.setSPOnOff("DAF8", "OFF")
            time.sleep(2)
            utils.setSPOnOff("DAF8", "ON")
            time.sleep(5)'''
            
            #Pair the Device via Hub
            context.reporter.HTML_TC_BusFlowKeyword_Initialize('Pair the Device ' + DeviceType + ' to Hub: ' )  
            print(utils.getTimeStamp(False), "Join Device to the network")
            ALAPI.setHubStateV6(session, nodeIdList[HubType]["nodeID"], "DISCOVERING")
            intStartTime = time.time()
            intTCStartTime = time.monotonic()
            
            
            boolPairStatus = False
            sleepTime = 0
            while True:
                #Validate if node is added the network
                nodeIdList = SP.getNodeAndDeviceVersionID()
                if DeviceType in nodeIdList:
                    boolPairStatus = True
                    break
                elif sleepTime>250: break
                time.sleep(30)
                sleepTime = sleepTime + 30
                    
            ALAPI.setHubStateV6(session, nodeIdList[HubType]["nodeID"], "UP")
            ALAPI.deleteSessionV6(session)
            
            print("boolPairStatus", boolPairStatus)
            if boolPairStatus: 
                intPassCntr = intPassCntr+1
                myNodeID = nodeIdList[DeviceType]["nodeID"]
                
                context.reporter.ReportEvent("Test Validation", "Device " + DeviceType + " Joined the network with Node ID : <B>" + myNodeID + "</B>", "PASS")
                print("Device Joined the network with Node ID : ", myNodeID)
            else: 
                intFailCntr = intFailCntr+1
                context.reporter.ReportEvent("Test Validation", "Join is unsuccessfull", "FAIL")
                print("join is unsuccessfull")
                return False
                '''print("Restarting the Smart Plug")
                utils.setSPOnOff(NodeID, 'OFF')
                time.sleep(5)
                utils.setSPOnOff(NodeID, 'ON')
                time.sleep(5)'''
                
            intTCEndTime = time.monotonic()
            strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
            strTCDuration = utils.getDuration(strTCDuration)
            intSeconds = int(strTCDuration.split(",")[1].strip().split(" ")[0])
            intMin = int(strTCDuration.split(",")[0].strip().split(" ")[0])
            intSeconds = intMin*60 + intSeconds
            if intSeconds >60: strStatus = "FAIL"
            else: strStatus = "PASS"
            context.reporter.ReportEvent("Test Validation", "Time taken: " + strTCDuration, strStatus)
            print("Time taken: ", strTCDuration)
            print('intCntr', intCntr, 'intPassCntr', intPassCntr, 'intFailCntr', intFailCntr)
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print()
            time.sleep(180)
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            
            