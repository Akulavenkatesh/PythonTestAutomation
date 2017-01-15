'''
Created on 5 Nov 2015

@author: ranganathan.veluswamy
'''
from datetime import timedelta
import os
import platform
import time

from behave import *

import FF_ScheduleUtils as oSchdUt
import FF_alertmeApi as ALAPI
import FF_loggingConfig as config
import FF_threadedSerial as AT
import FF_utils as utils
import FF_zbOTA as ota
import FF_device_utils as dutils
import glob


firmwareRootFilePath = '/volumes/hardware/firmware-release-notes/'

@when(u'the {DeviceName} of {DeviceType} is upgraded and downgraded between {DeviceVersion1:.2f} and {DeviceVersion2:.2f} infinitely and validated')
def upgrade_downgrade_firmware(context, DeviceName, DeviceType, DeviceVersion1, DeviceVersion2):
    
        
    print(DeviceName, DeviceType, DeviceVersion1, DeviceVersion2, "\n")
    
    if not os.path.exists(context.networkBasePath):
        print("Network drive is not mounted. Please mount and rerun the test")
        return
    else:
        firmwareRootFilePath = context.networkBasePath + 'firmware-release-notes/'
        strFWFilePath1 = get_firmware_file(firmwareRootFilePath, DeviceType, DeviceVersion1)
        strFWFilePath2 = get_firmware_file(firmwareRootFilePath, DeviceType, DeviceVersion2)
        if strFWFilePath1 != "" and strFWFilePath2 != "":
            nodeId = context.nodes[DeviceName.upper()]
            ep = get_ep_for_deviceType(DeviceType.upper())
            
            while True:
                context.rFM.upgrade_or_owngrade_firmware(context.reporter, "Downgrade", strFWFilePath1, nodeId,ep, DeviceType, DeviceVersion1)
                time.sleep(900)
                context.rFM.validate_firmware_version(context.reporter, "Downgrade", nodeId,ep, DeviceType, DeviceVersion1)
                
                time.sleep(30)
                context.rFM.upgrade_or_owngrade_firmware(context.reporter, "Upgrade", strFWFilePath2, nodeId,ep, DeviceType, DeviceVersion2)
                time.sleep(900)
                context.rFM.validate_firmware_version(context.reporter, "Upgrade", nodeId,ep, DeviceType, DeviceVersion2)
                
        else:
            print("Firmware file for given combination is not present in the share path. Please make sure file exist and rerun the test")
            return

def verifyMCU(context,nodeId,ep,DeviceVersion):
    intLoopCounter  = 0
    boolAppVersionFlag = False
    boolFileVersionFlag = False
    AT.stopThread.clear()  
    AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False, rxQ=True, listenerQ=True)
    while intLoopCounter < 30:
        #time.sleep(120)
        sendMode = 0
        strClusterId = "0000"
        strAttrId = "0001"
        respState, _, respValue = utils.readAttribute("Manufacturer", nodeId, ep, sendMode, strClusterId, strAttrId)
        intConvert = DeviceVersion.split(".")[1]
        strHex = hex(int(intConvert)).split("x")[1]
        strHexAppString = DeviceVersion.split(".")[0]+str(strHex)
        print("Expected AppVersion :" +str(strHexAppString).upper())
        strActAppString = str(respValue).split(nodeId+","+ep+","+strClusterId+","+strAttrId+",")[1]
        
        print("Actual AppVersion :" +str(strActAppString).upper())
        if str(strHexAppString).upper() in str(strActAppString).upper():
            boolAppVersionFlag = True
            print("Application Version Passed")
        strClusterId = "0019"
        strAttrId = "0002"
        respState, _, respValue = utils.readAttribute("client", nodeId, ep, sendMode, strClusterId, strAttrId)
        print("FileVersion :" +str(respState) +" : " + str(respValue))
        strActFileString = str(respValue).split(nodeId+","+ep+","+strClusterId+","+strAttrId+",")[1]
        strFileVersion = DeviceVersion.replace(".","")
        print("EXP File: "+strFileVersion)    
        print("ACT File: "+strActFileString.split(",")[1][:-4])
        if str(strFileVersion) in str(strActFileString.split(",")[1]):
            boolFileVersionFlag = True
            print("Current File Version Passed")
        if boolAppVersionFlag and boolFileVersionFlag:
            intLoopCounter = 30
            print("All Passed")
        intLoopCounter = intLoopCounter + 1 
    if boolAppVersionFlag and boolFileVersionFlag:
        context.reporter.ReportEvent("Test Validation","The Application version updated in the zigbee as " + strHexAppString,"Pass")
        context.reporter.ReportEvent("Test Validation","The Current File version updated in the zigbee as " + strFileVersion,"Pass")
    else:
        context.reporter.ReportEvent("Test Validation","The Application version updated in the zigbee as " + strActAppString,"Fail")
        context.reporter.ReportEvent("Test Validation","The Current File version updated in the zigbee as " + strActFileString,"Fail")
        

@when(u'the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis')
def upgrade_downgrade_firmware_forall(context):
    diviceNodesDict = {'SLR2': "2C41",
                                  'SLR1': "5EFA",
                                  'SLT3': "7416",
                                  'SLT4': "FC64",
                                  'SLT2': "42A3",
                                  'SLB1': "9237",
                                  'SLB3': "4DE0",
                                  'SLP2': "BAA4",
                                  'FWBulb01US': "17A2",
                                  'FWBulb01': "17A2",
                                  'TWBulb01UK': "B235",
                                  'TWBulb01US': "B234",
                                  'RGBBulb01UK': "B236",
                                  'RGBBulb01US': "B237",
                                  'HA_Repeater': "4DE0"}

    intCntr = 0
    while True:
        intCntr = intCntr + 1
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Upgrade-Downgrade Counter : ' + str(intCntr))   
        for oRow in context.table:
            DeviceName = oRow['DeviceName']
            DeviceType = oRow['DeviceType']
            if str(DeviceType).upper() == "GENERIC":
                strEnvironmentFilePath = os.path.abspath(__file__ + "/../../../../02_Manager_Tier/")
                context.networkBasePath = strEnvironmentFilePath
                DeviceName = utils.getAttribute("COMMON", "mainClient", None, None)
                #NodeID = dutils.getNodeIDbyDeciveID(DeviceName, False)
                oJson = dutils.getDeviceNode(DeviceName, False)
                MAcID = oJson['macID']
                MyDeviceType = oJson['name']
                myNodeId =  oJson['nodeID']
                context.nodeId = myNodeId
                myEp = oJson["endPoints"][0]
                strFirmwareFolder = strEnvironmentFilePath + "/firmware-release-notes/"+MyDeviceType+"_Firmware"
                strFirmwareFiles = strFirmwareFolder + "/*.ota"
                fileList = glob.glob(strFirmwareFiles)
                print(""+str(len(fileList)))
                if len(fileList) != 2:
                    context.reporter.ReportEvent("Test Validation","The folder should have only 2 ota files","Fail")
                    exit()
                
                '''strLower = ""
                strUpper = ''
                strLowerFileName = ""
                strUpperFileName = ""
                for f in fileList:                    
                    file = f.rpartition('/')[2]
                    if ".OTA" in str(file).upper():
                        print(str(file) + "\n")
                        i = fileList.index(f)
                        if strUpper == "":
                            strUpper = str(file).split("_")[1]
                            strUpperFileName = fileList[int(fileList.index(f))]
                        else:
                            intUpper = int(strUpper)
                            intLower = int(str(file).split("_")[1])
                            if intLower == intUpper:
                                context.reporter.ReportEvent("Test Validation","The folder contains same OTA Files","Fail")
                                exit()
                            elif intUpper > intLower:
                                strLower = str(intLower)
                                strLowerFileName = fileList[int(fileList.index(f))]
                            else:
                                strLower = strUpper
                                strLowerFileName = strUpperFileName
                                strUpper = str(intLower)
                                strUpperFileName = fileList[int(fileList.index(f))]
                        print("{0:>2}. {1}".format(i,file))
                
                    
                DeviceVersion1 = str(strLower[1:])
                DeviceVersion2 = str(strUpper[1:])
                print("1 ="+DeviceVersion1)
                print("\n 2 ="+DeviceVersion2)'''
                oDictOTAFiles = {}
                strLower = ""
                strUpper = ''
                strLowerFileName = ""
                strUpperFileName = ""
                for f in fileList:                    
                    file = f.rpartition('/')[2]
                    if ".OTA" in str(file).upper():
                        print(str(file) + "\n")
                        strUpper = str(file).split("_")[1]
                        strUpperFileName = f
                        oDictOTAFiles[strUpper] = strUpperFileName
                oSortedFileVersions = sorted(oDictOTAFiles)
                DeviceVersion1 = oSortedFileVersions[0]
                DeviceVersion2 =  oSortedFileVersions[1]
                print("1 ="+DeviceVersion1)
                print("\n 2 ="+DeviceVersion2)
            else:
                DeviceVersion1 = oRow['DeviceVersion1']
                DeviceVersion2 = oRow['DeviceVersion2']
            print(DeviceName, DeviceType, DeviceVersion1, DeviceVersion2, "\n")
            
            if not os.path.exists(context.networkBasePath):
                print("Network drive is not mounted. Please mount and rerun the test")
                return
            else:
                firmwareRootFilePath = context.networkBasePath + '/firmware-release-notes/'
                if str(DeviceType).upper() == "GENERIC":
                    nodeId = myNodeId
                    ep = myEp
                    DeviceType = MyDeviceType
                else:
                    nodeId = diviceNodesDict[DeviceType]
                    ep = get_ep_for_deviceType(DeviceType.upper())
                
                if not 'NA' in DeviceVersion1.upper():
                    strFWFilePath1 = get_firmware_file(firmwareRootFilePath, DeviceType, DeviceVersion1)
                    context.rFM.upgrade_or_downgrade_firmware(context.reporter, "Downgrade", strFWFilePath1, nodeId,ep, DeviceType, DeviceVersion1)
                    if DeviceType.upper() == "SLT4":
                        verifyMCU(context, nodeId, ep, DeviceVersion1)
                    '''if 'SLT3' in DeviceType.upper(): time.sleep(0)#time.sleep(1500)
                    else: time.sleep(0)'''
                    context.rFM.validate_firmware_version(context.reporter, "Downgrade", nodeId,ep, DeviceType, DeviceVersion1)
                    time.sleep(30)
                if not 'NA' in DeviceVersion2.upper():
                    strFWFilePath2 = get_firmware_file(firmwareRootFilePath, DeviceType, DeviceVersion2)
                    context.rFM.upgrade_or_downgrade_firmware(context.reporter, "Upgrade", strFWFilePath2, nodeId,ep, DeviceType, DeviceVersion2)
                    if DeviceType.upper() == "SLT4":
                        verifyMCU(context, nodeId, ep, DeviceVersion2)
                    '''if 'SLT3' in DeviceType.upper(): time.sleep(0)#time.sleep(1500)
                    else: time.sleep(500)'''                    
                    context.rFM.validate_firmware_version(context.reporter, "Upgrade", nodeId,ep, DeviceType, DeviceVersion2)
                        
                '''else:
                    print("Firmware file for given combination is not present in the share path. Please make sure file exist and rerun the test")'''
                    
@when(u'the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB')
def upgrade_downgrade_firmware_forallViaHUB(context):
    print("ViaHub\n")
    
    oHeatScheduleDict = {'sat': [('07:00', 28.5), ('09:00', 10.5), ('16:30', 23.5), ('22:00', 15), ('22:00', 15), ('22:00', 15)], 
                                      'sun': [('01:00', 27.5), ('02:00', 1), ('03:00', 12), ('04:00', 1), ('05:00', 28.5), ('23:45', 1)], 
                                      'fri': [('17:30', 1), ('18:00', 11), ('18:30', 28), ('19:00', 1), ('19:30', 29), ('20:00', 1)], 
                                      'wed': [('06:30', 29.5), ('08:30', 13), ('12:00', 19), ('16:30', 22.5), ('22:00', 31), ('22:00', 31)], 
                                      'mon': [('11:30', 27.5), ('11:45', 1), ('12:00', 12), ('12:15', 1), ('12:30', 28.5), ('12:45', 1)], 
                                      'tue': [('06:30', 20), ('08:30', 10), ('16:30', 20), ('22:00', 10), ('22:00', 10), ('22:00', 10)], 
                                      'thu': [('06:30', 20), ('08:30', 18.5), ('16:30', 27), ('22:00', 21), ('22:00', 21), ('22:00', 21)]}
    
    oAtributeDict ={'HeatMode': '',
                             'WaterMode': '',
                             'HeatTemperature': '',
                             'HeatRunningState': '',
                             'WaterRuningState': '',
                             'HeatSchedule': '',
                             'WaterSchedule': ''
                             }
    
    oModeList = ['MANUAL', 'AUTO', 'OFF', 'BOOST']
    
    
    
    #get node lists
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session  = ALAPI.sessionObject()
    resp = ALAPI.getNodesV6(session)
    nodeIdList = context.oThermostatEP.getNodeID(resp)
    ALAPI.deleteSessionV6(session)
    
    #Get the existing API details
    context.heatEP  = context.oThermostatClass.heatEP
    context.waterEP  = context.oThermostatClass.waterEP
    
    intModeListCntr = 0
    intCntr = 0
    while True:
        intCntr = intCntr + 1
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Upgrade-Downgrade Counter : ' + str(intCntr))   
        for oRow in context.table:
            DeviceName = oRow['DeviceName']
            DeviceType = oRow['DeviceType']
            DeviceVersion1 = oRow['DeviceVersion1']
            DeviceVersion2 = oRow['DeviceVersion2']
            print(DeviceName, DeviceType, DeviceVersion1, DeviceVersion2, "\n")
            
            strModeToSet = ""
            targetHeatTemperature = 0.0
            scheduleLockDuration = 0
            oSchedule = {}
            if 'SLR' in DeviceType.upper():
                strModeToSet = oModeList[intModeListCntr]
                targetHeatTemperature = 1.0
                scheduleLockDuration = 0                
                if 'BOOST' in strModeToSet:
                    targetHeatTemperature = 22.0
                    scheduleLockDuration = 60
                if 'MANUAL' in strModeToSet:
                    targetHeatTemperature = 20.0
                                
                context.heatEP.setModeViaAPI(nodeIdList[DeviceType], strModeToSet, targetHeatTemperature, scheduleLockDuration)
                heatWeeklyScheduleBefore = context.heatEP.getSchedule()
                if 'SLR2' in DeviceType.upper(): 
                    context.waterEP.setModeViaAPI(nodeIdList[DeviceType], strModeToSet, targetHeatTemperature = None, scheduleLockDuration = scheduleLockDuration)
                    waterWeeklyScheduleBefore = context.waterEP.getSchedule()
                
                intModeListCntr = intModeListCntr + 1
                if intModeListCntr == 4: intModeListCntr = 0
                
            if not os.path.exists(context.networkBasePath):
                print("Network drive is not mounted")
            
            #Downgrade device
            if not 'NA' in DeviceVersion1.upper():
                context.rFM.upgrade_or_downgrade_firmwareViaHUB(context.oThermostatEP, context.reporter, "Downgrade", DeviceType, DeviceVersion1)
                if 'SLT3' in DeviceType.upper(): 
                    #time.sleep(6000)
                    #power_cycle_hub()
                    print(strModeToSet)
                else: 
                    if 'CL01' in DeviceType.upper():
                        if context.rFM.verifyfirmwareVersionsViaHUB(context.oThermostatEP, context.reporter, "Downgrade", DeviceType, DeviceVersion1) == True:
                            #time.sleep(12000)
                            print()
                    else:
                        if context.rFM.verifyfirmwareVersionsViaHUB(context.oThermostatEP, context.reporter, "Downgrade", DeviceType, DeviceVersion1) == True:
                            #time.sleep(2500)
                            print(strModeToSet)
                context.rFM.validate_firmware_versionViaHUB(context.oThermostatEP, context.reporter, "Downgrade", DeviceType, DeviceVersion1)
                
                if 'SLR' in DeviceType.upper():
                    if 'AUTO' in strModeToSet: targetHeatTemperature = oSchdUt.getCurrentTempFromSchedule(context.heatEP.getSchedule())[0]
                    heatWeeklyScheduleAfter = context.heatEP.getSchedule()
                    context.rFM.validateAndUpdateLog(context.reporter, context.heatEP, 'Test', strModeToSet, targetHeatTemperature)
                    
                    oSchdUt.validateSchedulesOfOtherWeekdays(context.reporter, oSchedule, heatWeeklyScheduleBefore, heatWeeklyScheduleAfter)  
                    if 'SLR2' in DeviceType.upper(): 
                        if 'AUTO' in strModeToSet: targetHeatTemperature = oSchdUt.getCurrentTempFromSchedule(context.waterEP.getSchedule())[0]
                        context.rFM.validateAndUpdateLog(context.reporter, context.waterEP, 'Test', strModeToSet, targetHeatTemperature)
                        waterWeeklyScheduleAfter = context.waterEP.getSchedule()
                        
                        waterWeeklyScheduleBefore = oSchdUt.converWaterStateForSchedule(waterWeeklyScheduleBefore)
                        waterWeeklyScheduleAfter = oSchdUt.converWaterStateForSchedule(waterWeeklyScheduleAfter)
                        oSchdUt.validateSchedulesOfOtherWeekdays(context.reporter, oSchedule, waterWeeklyScheduleBefore, waterWeeklyScheduleAfter)  
                time.sleep(30)
            
            #Upgrade Device
            if not 'NA' in DeviceVersion2.upper():
                context.rFM.upgrade_or_downgrade_firmwareViaHUB(context.oThermostatEP, context.reporter, "Upgrade", DeviceType, DeviceVersion2)
                if 'SLT3' in DeviceType.upper(): 
                    #time.sleep(6000)
                    #power_cycle_hub()
                    print()
                else: 
                    if 'CL01' in DeviceType.upper():
                        if context.rFM.verifyfirmwareVersionsViaHUB(context.oThermostatEP, context.reporter, "Upgrade", DeviceType, DeviceVersion1) == True:
                            #time.sleep(12000)
                            print()
                    else:
                        if context.rFM.verifyfirmwareVersionsViaHUB(context.oThermostatEP, context.reporter, "Upgrade", DeviceType, DeviceVersion2) == True:
                            #time.sleep(2500) 
                            print()                   
                context.rFM.validate_firmware_versionViaHUB(context.oThermostatEP, context.reporter, "Upgrade", DeviceType, DeviceVersion2)
                if 'SLR' in DeviceType.upper():
                    if 'AUTO' in strModeToSet: targetHeatTemperature = oSchdUt.getCurrentTempFromSchedule(context.heatEP.getSchedule())[0]
                    heatWeeklyScheduleAfter = context.heatEP.getSchedule()
                    context.rFM.validateAndUpdateLog(context.reporter, context.heatEP, 'Test', strModeToSet, targetHeatTemperature)
                    
                    oSchdUt.validateSchedulesOfOtherWeekdays(context.reporter, oSchedule, heatWeeklyScheduleBefore, heatWeeklyScheduleAfter)  
                    if 'SLR2' in DeviceType.upper(): 
                        if 'AUTO' in strModeToSet: targetHeatTemperature = oSchdUt.getCurrentTempFromSchedule(context.waterEP.getSchedule())[0]
                        context.rFM.validateAndUpdateLog(context.reporter, context.waterEP, 'Test', strModeToSet, targetHeatTemperature)
                        waterWeeklyScheduleAfter = context.waterEP.getSchedule()
                        
                        waterWeeklyScheduleBefore = oSchdUt.converWaterStateForSchedule(waterWeeklyScheduleBefore)
                        waterWeeklyScheduleAfter = oSchdUt.converWaterStateForSchedule(waterWeeklyScheduleAfter)
                        oSchdUt.validateSchedulesOfOtherWeekdays(context.reporter, oSchedule, waterWeeklyScheduleBefore, waterWeeklyScheduleAfter)  
                        
        context.reporter.intIterationCntr = context.reporter.intIterationCntr + 1
#Power cycle the HUB
def power_cycle_hub():      
    strPORT = utils.get_Port_Id_TG()        
    if not strPORT == "":
        AT.stopThread.clear()  
        AT.startSerialThreads("/dev/" + strPORT, config.BAUD, printStatus=False)
        respState,_,resp = utils.discoverNodeIDbyCluster('0006')
        if respState:
            utils.setSPOnOff(myNodeId = resp, strOnOff = 'OFF', boolZigbee = True)
            time.sleep(20)                            
            utils.setSPOnOff(myNodeId = resp, strOnOff = 'ON', boolZigbee = True)
            time.sleep(1000)
        AT.stopThreads()
            
#Function to get the firmware from share
def get_firmware_file(firmwareRootFilePath, DeviceType, DeviceVersion):
    strFWFilePath = ""
    DeviceVersion = str(DeviceVersion)
    if "SLR" in DeviceType.upper():
        DeviceVersion = "V" + DeviceVersion.replace(".", "_")
    if "SLT3" in DeviceType.upper():
        DeviceVersion = "MCU_V" + DeviceVersion.replace(".", "")
    if "SLT4" in DeviceType.upper():
        DeviceVersion = "bgstu41_" + DeviceVersion.replace(".", "")
    if "SLT2" in DeviceType.upper():
        DeviceVersion = "FW0" + DeviceVersion
    if "SLP2" in DeviceType.upper():
        DeviceVersion = "SLP2_0" + DeviceVersion.replace(".", "")
    if "SLB1" in DeviceType.upper():
        DeviceVersion = "SLB1_0" + DeviceVersion.replace(".", "")
    if "SLB3" in DeviceType.upper():
        DeviceVersion = "HA_Range_Extender_3587_0" + DeviceVersion.replace(".", "")
    if "BULB" in DeviceType.upper():
        DeviceVersion = DeviceVersion.replace(".", "")
    if "HA" in DeviceType.upper():
        DeviceVersion = DeviceVersion.replace(".", "")
        
    oFileList = os.listdir(firmwareRootFilePath)
    for oFile in oFileList:
        if get_path_for_deviceType(DeviceType).upper() in oFile.upper():
            oOTAFileList = os.listdir(firmwareRootFilePath + oFile)
            for oOTAFile in oOTAFileList:
                if oOTAFile.upper().endswith(".OTA"):
                    if DeviceVersion.upper() in oOTAFile.upper():
                        strFWFilePath = firmwareRootFilePath + oFile + "/" + oOTAFile
                        break
    return strFWFilePath


#Function to get Ep for given deviceTypes
def get_ep_for_deviceType(strDeviceType):
    strEP = ""
    for deviceTypeDict in ota.deviceTypes:
        if deviceTypeDict['type'].upper() == strDeviceType.upper():
            strEP = deviceTypeDict['ep']
            break
    return strEP

#Function to get Ep for given deviceTypes
def get_path_for_deviceType(strDeviceType):
    strPath = ""
    for deviceTypeDict in ota.deviceTypes:
        if deviceTypeDict['type'].upper() == strDeviceType.upper():
            strPath = deviceTypeDict['path']
            break
    return strPath
        