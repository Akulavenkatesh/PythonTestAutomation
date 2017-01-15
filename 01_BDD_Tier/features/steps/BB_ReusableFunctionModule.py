'''
Created on 25 May 2015

@author: ranganathan.veluswamy
'''
from datetime import datetime
from datetime import timedelta
import json
import os
from time import strptime
import time
import traceback
import FF_ScheduleUtils as oSchdUtil

import CC_thermostatModule as st
import CC_platformAPI as PAPI
import DD_Page_AndroidApp as paygeAndroid
import DD_Page_WebApp as paygeWeb
import DD_Page_iOSApp as paygeiOS
import FF_ScheduleUtils as oSchdUt
import FF_alertmeApi as ALAPI
import FF_utils as utils
import FF_Platform_Utils as pUtils
import FF_zbOTA as ota


class ReusableFunctionModule():
    
    
    
    def __init__(self):
        self.getWaterModes = {'MANUAL' : 'Always ON',
                                             'OFF' : 'Always OFF',
                                             'Always ON' : 'Always ON',           
                                             'ON' : 'Always ON',                                   
                                             'Always OFF' : 'Always OFF',
                                             'BOOST' : 'BOOST',
                                             'BOOST_CANCEL' : 'BOOST_CANCEL',
                                             'AUTO' : 'AUTO',
                                             'OVERRIDE' : 'OVERRIDE',
                                            None : 'None'
                                            }
    
    #Sets the Target temperature
    def setTargetTemperature(self, reporter, boolAutoMode, oThermostatEP, strSetTemperature):
        strBeforeTemperature = self.convertHexTemp(oThermostatEP.occupiedHeatingSetpoint, False)
        strBeforeMode = oThermostatEP.mode
        
        #Set Expected mode based on the expected logic
        if strBeforeMode == 'OFF' and int(strSetTemperature) > 1.0:
            strExpectedMode = 'MANUAL'
        elif strBeforeMode == 'AUTO':
            strExpectedMode = 'OVERRIDE'
        else:
            strExpectedMode = strBeforeMode
            
        reporter.HTML_TC_BusFlowKeyword_Initialize('Set Target Temperature : ' + str(strSetTemperature) + 'C') 
        #Set the Target temperature
        if boolAutoMode:
            strReportMode = 'Automatically'        
            oThermostatEP.setSetpoint(strSetTemperature)
        else:
            strReportMode = 'Manually' 
            input('\n*********************************************************************************************************************************\n' + \
                    '*************************************************** MANUAL INTERVENTION *********************************************************\n'
                    '*********************************************************************************************************************************\n'
                    'On the Thermostat Manually set up Target Temperature to ' + strSetTemperature +  + 'C\n' + \
                    'If Action is Completed then please type \'Y\' and press Enter key>>>')
            strReportLog = self.getLog(oThermostatEP, 'Test', strExpectedMode, strSetTemperature)
            print('\nPlease validate if the below attribute values are displayed on the Thermostat Screen:')
            print(self.conertToPrintLog(strReportLog[0]))
               
        reporter.ReportEvent('Test Validation', strReportMode + 'Setting up Target Temperature to <B>' + str(strSetTemperature) + \
                             ' <B>from </B>' + str(strBeforeTemperature) + 'C </B>with current system mode as <B>' + oThermostatEP.mode , 'Done')
        
        if not reporter.ActionStatus: return False
        
        #Validate the change and Log into the report
        if boolAutoMode and 'PLATFORM' not in reporter.APIType.upper(): self.validateAndUpdateLog(reporter, oThermostatEP, 'Model') 
        else: 
            
            print("Vlidating Main Client")
            self.validateAndUpdateLog(reporter, oThermostatEP, 'Main Client', strExpectedMode, strSetTemperature)
            
            strMainClientTemp = oThermostatEP.client
            if 'Y' in utils.getAttribute('common', 'secondClientValidateFlag'):
                print("Vlidating Second Client")
                oThermostatEP.client = utils.getAttribute('common', 'secondClient')
                try:
                    self.validateAndUpdateLog(reporter, oThermostatEP, 'Secondary Client', strExpectedMode, strSetTemperature)
                except: print('Error in Validating second client')
                oThermostatEP.client = strMainClientTemp
        self.validateAndUpdateLog(reporter, oThermostatEP, 'Test', strExpectedMode, strSetTemperature)
    
    #Sets the system mode for the given temperature if required
    def setSysMode(self, reporter, boolAutoMode, oThermostatEP, strMode, strSetTemperature = None, strSetDurationInHours = 1):
        print(strSetTemperature, 'strSetTemperature', '\n')
        if 'MANUAL' in strMode.upper():
            strExpectedTemperature = 20.0
            if reporter.APIType == 'PLATFORM' :
                if not oThermostatEP.Web_ManualModeTargTemp is None: strExpectedTemperature = oThermostatEP.Web_ManualModeTargTemp
        elif strMode.upper() =='OFF':
            strExpectedTemperature = 1.0
        elif strMode.upper() =='AUTO':
            fltTemp = oSchdUt.getCurrentTempFromSchedule(oThermostatEP.getSchedule())
            strExpectedTemperature = fltTemp[0]
        else:
            strExpectedTemperature = strSetTemperature
        
        strModeOnReport = strMode
        if oThermostatEP.type == 'WATER':
            if strMode.upper().find('ON') >= 0: strMode = 'MANUAL'
            elif strMode.upper().find('OFF') >= 0: strMode = 'OFF'
            strExpectedTemperature = None
            
        reporter.HTML_TC_BusFlowKeyword_Initialize('Set ' + strModeOnReport + ' Mode')   
        strWithTargTemp = ''
        if not strExpectedTemperature is None: strWithTargTemp = 'with Target Temperature as ' + str(strExpectedTemperature) + 'C'
        
        
        #Set the System Mode
        if boolAutoMode:
            strReportMode = 'Automatically'        
            print(strMode, strSetTemperature, strSetDurationInHours, '\n')
            oThermostatEP.setMode(strMode, strSetTemperature, strSetDurationInHours)
        else:
            strReportMode = 'Manually' 
            input('\n*********************************************************************************************************************************\n' + \
                    '*************************************************** MANUAL INTERVENTION *********************************************************\n'
                    '*********************************************************************************************************************************\n'
                    'On the Thermostat Manually set up ' + strModeOnReport + ' Mode ' +  strWithTargTemp + '\n' + \
                    'If Action is Completed then please type \'Y\' and press Enter key>>>')
            strReportLog = self.getLog(oThermostatEP, 'Test', strModeOnReport, strExpectedTemperature)
            print('\nPlease validate if the below attribute values are displayed on the Thermostat Screen:')
            print(self.conertToPrintLog(strReportLog[0]))
    
        reporter.ReportEvent('Test Validation',strReportMode + ' Setting up <B>' + strModeOnReport + '</B> Mode ' + strWithTargTemp, 'Done')
        
        #Check if action status is True. If False then skip Scenario
        if not reporter.ActionStatus: return False
    
        #Validate the change and Log into the report
        if boolAutoMode and reporter.APIType != 'PLATFORM' : self.validateAndUpdateLog(reporter, oThermostatEP, 'Model')    
        else: 
            self.validateAndUpdateLog(reporter, oThermostatEP, 'Main Client', strModeOnReport, strExpectedTemperature)
            strMainClientTemp = oThermostatEP.client
            if 'Y' in utils.getAttribute('common', 'secondClientValidateFlag'):
                oThermostatEP.client = utils.getAttribute('common', 'secondClient')
                try:
                    self.validateAndUpdateLog(reporter, oThermostatEP, 'Secondary Client', strModeOnReport, strExpectedTemperature)
                except: print('Error in Validating second client')
                oThermostatEP.client = strMainClientTemp
            
        self.validateAndUpdateLog(reporter, oThermostatEP, 'Test', strModeOnReport, strExpectedTemperature)


    #Sets the system mode for the given temperature if required
    def setHoldayMode(self, reporter, boolAutoMode, oThermostatEP, strMode, strSetTemperature = None, strSetDurationInHours = 1, strHoldayStart = "", strHoldayEnd = ""):        
        strExpectedTemperature = strSetTemperature
        strModeOnReport = strMode
        reporter.HTML_TC_BusFlowKeyword_Initialize('Set ' + strModeOnReport + ' Mode')   
        strWithTargTemp = ''
        if not strExpectedTemperature is None: strWithTargTemp = 'with Target Temperature as ' + str(strExpectedTemperature) + 'C'
        
        
        #Set the System Mode
        if boolAutoMode:
            strReportMode = 'Automatically'        
            print(strMode, strSetTemperature, strSetDurationInHours, strHoldayStart, strHoldayEnd, '\n')
            oThermostatEP.setHoliday(strHoldayStart, strHoldayEnd, strSetTemperature)
            
        else:
            strReportMode = 'Manually' 
            input('\n*********************************************************************************************************************************\n' + \
                    '*************************************************** MANUAL INTERVENTION *********************************************************\n'
                    '*********************************************************************************************************************************\n'
                    'On the Thermostat Manually set up ' + strModeOnReport + ' Mode ' +  strWithTargTemp + '\n' + \
                    'If Action is Completed then please type \'Y\' and press Enter key>>>')
            strReportLog = self.getLog(oThermostatEP, 'Test', strModeOnReport, strExpectedTemperature, strHoldayStart, strHoldayEnd)
            print('\nPlease validate if the below attribute values are displayed on the Thermostat Screen:')
            print(self.conertToPrintLog(strReportLog[0]))
    
        reporter.ReportEvent('Test Validation',strReportMode + ' Setting up <B>' + strModeOnReport + '</B> Mode ' + strWithTargTemp, 'Done')
        
        #Check if action status is True. If False then skip Scenario
        if not reporter.ActionStatus: return False
    
        #Validate the change and Log into the report
        if boolAutoMode and reporter.APIType != 'PLATFORM' : self.validateAndUpdateLog(reporter, oThermostatEP, 'Model')    
        else: 
            self.validateAndUpdateLog(reporter, oThermostatEP, 'Main Client', strModeOnReport, strExpectedTemperature, strHoldayStart, strHoldayEnd)
            strMainClientTemp = oThermostatEP.client
            if 'Y' in utils.getAttribute('common', 'secondClientValidateFlag'):
                oThermostatEP.client = utils.getAttribute('common', 'secondClient')
                try:
                    self.validateAndUpdateLog(reporter, oThermostatEP, 'Secondary Client', strModeOnReport, strExpectedTemperature, strHoldayStart, strHoldayEnd)
                except: print('Error in Validating second client')
                oThermostatEP.client = strMainClientTemp
            
        self.validateAndUpdateLog(reporter, oThermostatEP, 'Test', strModeOnReport, strExpectedTemperature, strHoldayStart, strHoldayEnd)
        
    def setSchedule(self, context, oSchedule, boolStandaloneMode = False, boolViaHub = False, nodeId = ""):
        context.oThermostatEP.update()    
        #Getting weekly schedule before the Set Schedule
        context.WeeklyScheduleBefore = context.oThermostatEP.getSchedule()
        #Sets the schedule
        context.reporter.HTML_TC_BusFlowKeyword_Initialize("Setting the given Schedule")
        '''
        if strAppVersion == 'V6' and 'WEB111' in context.oThermostatEP.client.upper():
            input('\n*********************************************************************************************************************************\n' + \
                '*************************************************** MANUAL INTERVENTION *********************************************************\n'
                '*********************************************************************************************************************************\n'
                'On the V6 Web App Manually setup the above Schedule' + '\n' +\
                'If Action is Completed then please type \'Y\' and press Enter key>>>')
        else:'''
        
        if not 'PLATFORM' in context.APIType.upper():
            context.oThermostatEP.setSchedule(oSchedule, boolStandaloneMode)  
            if boolStandaloneMode:   
                strEP = context.oThermostatEP.type        
                context.oThermostatClass = st.thermostatClass(context.reporter.strNodeID)
                if strEP.upper().find('WATER') >=0: context.oThermostatEP  = context.oThermostatClass.waterEP
                else: context.oThermostatEP  = context.oThermostatClass.heatEP
        else: 
            if boolViaHub: 
                oCurrrentSchedules = pUtils.getDeviceSchedule(context.deviceType)
                oCurrrentSchedulesFiltered = pUtils.removeDayFromScheduleAPI(oCurrrentSchedules, oSchedule.keys())
                payload = oSchdUtil.createScheduleForHubAPI(oSchedule, oCurrrentSchedulesFiltered)
                context.oThermostatEP.setScheduleViaAPI(nodeId, payload)
            else: context.oThermostatEP.setSchedule(oSchedule)
        #Check if action status is True. If False then skip Scenario
        
        if not context.reporter.ActionStatus: return False
        try:
            context.oThermostatEP.update()    
        except: pass
        
        #print(context.oThermostatEP.getSchedule())
        #Reporting the Schedule that is set 
        context.reporter.ReportEvent('Test Validation',  'Please find below the Schedule that has been set', 'DONE', 'CENTER')
        if context.oThermostatEP.type=='WATER': oSchedule = oSchdUt.converWaterStateForSchedule(oSchedule)
        oSchdUt.reportSchedule(context.oThermostatEP, context.reporter, oSchedule)    
        
        
        #Sets the mode to Auto
        if not boolViaHub: 
            context.oThermostatEP.setMode('AUTO')
            time.sleep(10)
            try:
                context.oThermostatEP.update()
            except: pass
        
        
        #Getting weekly schedule after the Set Schedule
        context.WeeklyScheduleAfter = context.oThermostatEP.getSchedule()
        #Validating the remaining schedules of the week after the new schedule is set
        if not len(oSchedule.keys()) == 6:
            context.reporter.HTML_TC_BusFlowKeyword_Initialize("Validating the remaining days of the schedule")
            if context.oThermostatEP.type=='WATER': 
                context.WeeklyScheduleBefore = oSchdUt.converWaterStateForSchedule(context.WeeklyScheduleBefore)
                context.WeeklyScheduleAfter = oSchdUt.converWaterStateForSchedule(context.WeeklyScheduleAfter)
                context.oSchedDict = oSchdUt.converWaterStateForSchedule(context.oSchedDict)
            oSchdUt.validateSchedulesOfOtherWeekdays(context.reporter, oSchedule, context.WeeklyScheduleBefore, context.WeeklyScheduleAfter)  
 
    def setScheduleViaHub(self, context, oSchedule):
        #Getting weekly schedule before the Set Schedule
        context.WeeklyScheduleBefore = context.oThermostatEP.getSchedule()
        
        #Sets the schedule
        context.reporter.HTML_TC_BusFlowKeyword_Initialize("Setting the given Schedule")
        
        context.oThermostatEP.setSchedule(oSchedule)  
            
        #Check if action status is True. If False then skip Scenario
        if not context.reporter.ActionStatus: return False
                
        #Reporting the Schedule that is set 
        context.reporter.ReportEvent('Test Validation',  'Please find below the Schedule that has been set', 'DONE', 'CENTER')
        if context.oThermostatEP.type=='WATER': oSchedule = oSchdUt.converWaterStateForSchedule(oSchedule)
        oSchdUt.reportSchedule(context.oThermostatEP, context.reporter, oSchedule)    
        
        #Sets the mode to Auto
        context.oThermostatEP.setMode('AUTO')
        time.sleep(10)
        try:
            context.oThermostatEP.update()
        except: pass
        
        #Getting weekly schedule after the Set Schedule
        context.WeeklyScheduleAfter = context.oThermostatEP.getSchedule()
        #Validating the remaining schedules of the week after the new schedule is set
        if not len(oSchedule.keys()) == 6:
            context.reporter.HTML_TC_BusFlowKeyword_Initialize("Validating the remaining days of the schedule")
            if context.oThermostatEP.type=='WATER': 
                context.WeeklyScheduleBefore = oSchdUt.converWaterStateForSchedule(context.WeeklyScheduleBefore)
                context.WeeklyScheduleAfter = oSchdUt.converWaterStateForSchedule(context.WeeklyScheduleAfter)
                context.oSchedDict = oSchdUt.converWaterStateForSchedule(context.oSchedDict)
            oSchdUt.validateSchedulesOfOtherWeekdays(context.reporter, oSchedule, context.WeeklyScheduleBefore, context.WeeklyScheduleAfter)  
 
    #Function to get Ep for given deviceTypes
    def get_ZbType_for_deviceType(self,strDeviceType):
        strPath = ""
        for deviceTypeDict in ota.deviceTypes:
            if deviceTypeDict['type'].upper() == strDeviceType.upper():
                strPath = deviceTypeDict['zbType']
                break
        return strPath
    
    #function to upgrade the firmware version
    def upgrade_or_downgrade_firmware(self, reporter, strUpgradeOrDowngrade, fullPath, nodeId,ep, strDeviceType, DeviceVersion):
        print(strUpgradeOrDowngrade, fullPath, nodeId,ep, '\n')
        strExpectedFWVersion =  str(DeviceVersion).replace(".", "")
        reporter.HTML_TC_BusFlowKeyword_Initialize(strUpgradeOrDowngrade.upper() + ' Firmware for : ' + strDeviceType.upper())  
        
        _, _, strTHVersion = utils.get_device_version(nodeId, ep)
        reporter.ReportEvent("Test Validation", "The Current version on the device before the upgrade: " + strTHVersion, "DONE")
        print(strExpectedFWVersion, str(strTHVersion)[:4])
        if (strExpectedFWVersion in str(strTHVersion)[:4]) or (str(strTHVersion)[:4] in strExpectedFWVersion):
            reporter.ReportEvent("Test Validation", "The Device : " + strDeviceType + " is already in version : " + strTHVersion + "<p>Hence skipping the " + strUpgradeOrDowngrade + "  process.", "PASS")
            return
                
        #Upgrade or Downgrade Firmware
        reporter.ReportEvent('Test Validation', 'The Firmware for ' + strDeviceType.upper() + ' is set to ' + strUpgradeOrDowngrade.upper() + ' to verion '  + str(DeviceVersion), "Done")
        _, strFileName = os.path.split(fullPath)
        reporter.ReportEvent('Test Validation', 'The ' + strUpgradeOrDowngrade.upper()  + ' Firmware OTA file download has started. <p> File Name : ' + strFileName, "Done")
        
        #Check if action status is True. If False then skip Scenario
        if not reporter.ActionStatus: return False
    
        '''# Open the image file
        if os.path.isfile(fullPath):
            f = open(fullPath, "rb")
        else:
            print("File not found {}".format(fullPath))
            reporter.ReportEvent('Test Validation', 'The Firmware file is not found: '  + fullPath, "Done")
            return False
        print('FW File = {0}\r\n'.format(fullPath))'''
    
        '''# Read header from the file
        header = ota.myOtaHeader()
        ota.readHeader(header,f)        '''
        #upgrade firmware
        zbType = self.get_ZbType_for_deviceType(strDeviceType)
        print(nodeId,ep,zbType,fullPath)
        result = ota.firmwareUpgrade(nodeId,ep,zbType,fullPath,printData = True)
        print(result)
        print('All Done. {}'.format(time.strftime("%H:%M:%S", time.gmtime())))
        reporter.ReportEvent('Test Validation', 'The Firmware ' + strUpgradeOrDowngrade.upper() + ' OTA file download completed', "Done")
        
        
        reporter.ReportEvent("Test Validation", "Firmware Install Started", "DONE")
        if 'SLT3' in strDeviceType.upper():
            intTCStartTime = time.monotonic()
            respState,_,resp = utils.check_device_back_after_restart(nodeId, ep)
            intTCEndTime = time.monotonic()
            strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
            strTCDuration = utils.getDuration(strTCDuration)
            reporter.ReportEvent("Test Validation", "Time taken for IMGQUERY response : " + strTCDuration, "DONE")
            reporter.ReportEvent("Test Validation", "Current Firmware version reported by IMGQUERY response : " + resp, "DONE")
            if not respState: reporter.ReportEvent("Test Validation", "IMGQUERY response failed with error" + resp, "FAIL")
            time.sleep(5)
        else: time.sleep(500)
        reporter.ReportEvent("Test Validation", "Firmware Install Completed", "DONE")
            
    #Validating the Firmware version
    def validate_firmware_version(self, reporter, strUpgradeOrDowngrade, nodeId,ep, strDeviceType, DeviceVersion):
        try:
            reporter.HTML_TC_BusFlowKeyword_Initialize('Validate ' + strUpgradeOrDowngrade.upper() + ' for Device : ' + strDeviceType)   
            strExpectedFWVersion =  str(DeviceVersion).replace(".", "")
            
            
            _, _, strTHVersion = utils.get_device_version(nodeId, ep)
            
            if (strExpectedFWVersion in str(strTHVersion)[:4]) or (str(strTHVersion)[:4] in strExpectedFWVersion):
                reporter.ReportEvent("Test Validation", "The Device : " + strDeviceType + " is successfully " + strUpgradeOrDowngrade + " to " + strTHVersion, "PASS")
            else: 
                reporter.ReportEvent("Test Validation", "The Device : " + strDeviceType + " is <B>NOT</B> " + strUpgradeOrDowngrade + " to " + DeviceVersion + "<br> Current version on the device : " + strTHVersion, "FAIL")
                exit()
        except:
            reporter.ReportEvent("Test Validation", 'Exception in validate_firmware_version Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')), "FAIL")
        
    #function to upgrade the firmware version
    def upgrade_or_downgrade_firmwareViaHUB(self, oThermostatEP, reporter, strUpgradeOrDowngrade, strDeviceType, DeviceVersion):
        print(strUpgradeOrDowngrade, strDeviceType, DeviceVersion, '\n')
                    
        reporter.HTML_TC_BusFlowKeyword_Initialize(strUpgradeOrDowngrade.upper() + ' Firmware for : ' + strDeviceType.upper())   
        
        strTHVersion = oThermostatEP.getFWversion()[strDeviceType]
        reporter.ReportEvent("Test Validation", "The Current version on the device before the upgrade: " + strTHVersion, "DONE")
        #Upgrade or Downgrade Firmware
        reporter.ReportEvent('Test Validation', 'The Firmware for ' + strDeviceType.upper() + ' is set to ' + strUpgradeOrDowngrade.upper() + ' to verion '  + str(DeviceVersion), "Done")
        
        if strTHVersion != str(DeviceVersion):
            #Check if action status is True. If False then skip Scenario
            if not reporter.ActionStatus: return False
            
            oThermostatEP.upgradeFirware(strDeviceType, DeviceVersion)
            
            print('All Done. {}'.format(time.strftime("%H:%M:%S", time.gmtime())))
            reporter.ReportEvent('Test Validation', 'The Firmware ' + strUpgradeOrDowngrade.upper() + ' is Started', "Done")
        
            intTCStartTime = time.monotonic()
            time.sleep(300)
            respState, errorMsg = self.wait_for_upgrade_completion(strDeviceType, reporter, strUpgradeOrDowngrade.upper())
            intTCEndTime = time.monotonic()
            strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
            strTCDuration = utils.getDuration(strTCDuration)
            reporter.ReportEvent("Test Validation", "Time taken for " + strUpgradeOrDowngrade.upper() + " : " + strTCDuration, "DONE")
            if not respState: 
                reporter.ReportEvent("Test Validation", strUpgradeOrDowngrade.upper() + " Failed with error: " + errorMsg, "FAIL")
                time.sleep(300)
                if "CL" in strDeviceType.upper():
                    exit()
            else: reporter.ReportEvent("Test Validation", "Firmware Install Completed", "DONE")
            time.sleep(60)
            if "CL" in strDeviceType.upper() or "PIR" in strDeviceType.upper() or "WDS" in strDeviceType.upper(): time.sleep(600)
            
        else:
            print('The test step is skipped - Same Version')    
            reporter.ReportEvent('Test Validation','The test step is skipped - Same Version',"Done")
    
    #Wait for upgrade/downgrade
    def wait_for_upgrade_completion(self, DeviceType, reporter, strUpgradeOrDowngrade):
        if "NANO" in DeviceType.upper(): 
            time.sleep(900)
            return True, ""
        
        ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
        session =ALAPI.superUserSessionObject()
        
        hubIDResp = ALAPI.getHubIdV6(session, utils.getAttribute('common', 'userName'))
        hubID = hubIDResp[0]["internalHubState"]["id"]
        strModel = DeviceType
        
        boolCompleted = False
        boolOneTimeRestartDone = False
        strErrorMsg = ""
        strUpgradeStatus = ""
        fltProgress = 0.0
        intCntr = 1
        intPercentagePrintCntr = 1.0
    
        #print("CurrentStatus: ", strUpgradeStatus)
        while strUpgradeStatus!="COMPLETE":
            boolNodeExisit = False
            boolUpgradeExist = False
            strLastRevceivedFailTimestamp = ""
            strFailLog = ""
            time.sleep(2)
            hubLogJson = ALAPI.getHubLogsV6(session, hubID)
            for oDict in hubLogJson["internalNodeStates"]:
                if 'model' in oDict:
                    '''strActualModel = oDict["model"]
                elif  'hardwareVersion' in oDict:
                    strActualModel = oDict["hardwareVersion"]
                else:
                    strActualModel = "" 
                    break'''
                
                    if strModel == oDict["model"]:
                        boolNodeExisit = True
                        if "upgradeState" in oDict:
                            boolUpgradeExist = True
                            strUpgradeStatus = oDict["upgradeState"]["status"]
                            #print(strUpgradeStatus)
                            if "FAIL" in strUpgradeStatus.upper():
                                if "lastReceived" in oDict["upgradeState"]:
                                    strLastRevceivedFailTimestamp = oDict["upgradeState"]["lastReceived"]
                                if "log" in oDict["upgradeState"]:
                                    strFailLog = oDict["upgradeState"]["log"]
                                return False,  strFailLog + "@ ==>" + strLastRevceivedFailTimestamp
                            if "progress" in oDict["upgradeState"]:
                                fltProgress = float(oDict["upgradeState"]["progress"])
                        else: 
                            print("Upgrade not happenning")
                            break
            
            if not boolNodeExisit:
                strErrorMsg = "Device Node is missing"
                print(strErrorMsg)
                break
            
            if not boolUpgradeExist:
                strErrorMsg = "Device " + strUpgradeOrDowngrade.upper() + " NOT triggered"
                print(strErrorMsg)
                break
            
            
            
            if fltProgress >= intPercentagePrintCntr * 10.0:
                print(intCntr, strUpgradeStatus, fltProgress)
                reporter.ReportEvent("Test Validation", "Current " + strUpgradeOrDowngrade.upper() + " progress: " + str(fltProgress) + "%", "DONE")
                print("Current " + strUpgradeOrDowngrade.upper() + " progress: " + str(fltProgress) + "%")
                intPercentagePrintCntr = intPercentagePrintCntr + 1.0
                
            '''if "CL" in DeviceType.upper():
                if fltProgress > 50.0 <80.0:
                    if not boolOneTimeRestartDone:
                        oNodeList = pUtils.getNodeAndDeviceVersionID()
                        hubID = oNodeList["NANO2"]["nodeID"]
                        ALAPI.rebootHubV6(session, hubID)
                        time.sleep(300)
                        boolOneTimeRestartDone = True'''
            
            intCntr = intCntr + 1
            if intCntr > 3600:
                break
        
            
        ALAPI.deleteSessionV6(session)
        if "COMPLETE" in strUpgradeStatus.upper():
            print("Firmware downgrade/upgrade successful.", strUpgradeStatus)
            boolCompleted = True
        else: print("Firmware downgrade/upgrade unsuccessful.", strUpgradeStatus)
        
        return boolCompleted, strErrorMsg
    
    #function to check if both the versions are same to stop waiting for validation
    def verifyfirmwareVersionsViaHUB(self, oThermostatEP, reporter, strUpgradeOrDowngrade, strDeviceType, DeviceVersion):
        strTHVersion = oThermostatEP.getFWversion()[strDeviceType]
        #Flag to check if both the versions are same to stop waiting for validation
        strFlag = True 
        if strTHVersion != str(DeviceVersion):
            strFlag = True;
            #Check if action status is True. If False then skip Scenario
            if not reporter.ActionStatus: return False
            oThermostatEP.upgradeFirware(strDeviceType, DeviceVersion)
        else:
            strFlag = False
        return strFlag
    
    #Validating the Firmware version
    def validate_firmware_versionViaHUB(self, oThermostatEP, reporter, strUpgradeOrDowngrade, strDeviceType, DeviceVersion):
        try:
            reporter.HTML_TC_BusFlowKeyword_Initialize('Validate ' + strUpgradeOrDowngrade.upper() + ' for Device : ' + strDeviceType)   
            strExpectedFWVersion =  str(DeviceVersion).replace(".", "")
            strTHVersion = oThermostatEP.getFWversion()[strDeviceType]
            if DeviceVersion in str(strTHVersion):
                reporter.ReportEvent("Test Validation", "The Device : " + strDeviceType + " is successfully " + strUpgradeOrDowngrade + " to " + strTHVersion, "PASS")
            else: 
                reporter.ReportEvent("Test Validation", "The Device : " + strDeviceType + " is <B>NOT</B> " + strUpgradeOrDowngrade + " to " + DeviceVersion + "<br> Current version on the device : " + strTHVersion, "FAIL")
                print("The Device : " + strDeviceType + " is <B>NOT</B> " + strUpgradeOrDowngrade + " to " + DeviceVersion + "<br> Current version on the device : " + strTHVersion)
                print(strUpgradeOrDowngrade, "FAILED. Test Exited")
        except:
            reporter.ReportEvent("Test Validation", 'Exception in validate_firmware_version Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')), "FAIL")
    
    #Validates the system mode for the given duration and logs the validation in check interval time
    def validateSysmode(self, reporter, boolAutoMode, oThermostatEP, strSysMode, strExpectedTemperature = 1.0, intCheckDuration = 600, intCheckTImeInterval = 30, strExpextedHolidayStart = "", strExpectedHolidayEnd = "", nextEventStartTime = None, nextEventDay = 'Today'):
        
        reporter.HTML_TC_BusFlowKeyword_Initialize('Validate ' + strSysMode + ' Mode')    
        if not oThermostatEP.type=='WATER': strTarg = 'Target Temperature'
        else: strTarg = 'Hot Water State'
        reporter.ReportEvent('Test Validation', 'Validating <B>' + strSysMode + ' </B>Mode with ' + strTarg + ' as <B>' + str(strExpectedTemperature) + \
                             '</B> for every <B>' + str(intCheckTImeInterval) + ' second(s) </B>for a duration of <B>' + str(round(intCheckDuration/60, 2)) + ' minute(s)', 'Done')
        
        #Iterate the validation of system mode
        for intCntr in range(int(intCheckDuration/intCheckTImeInterval)):
            #Log the Validation of current attributes with Expected Test and Model Attribute values
            if boolAutoMode and reporter.APIType != 'PLATFORM' : self.validateAndUpdateLog(reporter, oThermostatEP, 'Model')
            self.validateAndUpdateLog(reporter, oThermostatEP, 'Test', strSysMode, strExpectedTemperature, strExpextedHolidayStart, strExpectedHolidayEnd)
            
            #Wait for the Check Time interval
            time.sleep(intCheckTImeInterval)
            if intCntr==int(intCheckDuration/intCheckTImeInterval) - 1:
                time.sleep(intCheckDuration%intCheckTImeInterval)
            if not nextEventStartTime is None:
                if not oSchdUt.checkGuardTime(nextEventStartTime, nextEventDay): return 
        
    #Validates the SP system mode for the given duration and logs the validation in check interval time
    def validateSPSysmode(self, context, boolAutoMode, SPNodeID, strSysMode, strExpectedState = "OFF", intBrightness = 0, intCheckDuration = 600, intCheckTImeInterval = 30, strExpextedHolidayStart = "", strExpectedHolidayEnd = "", nextEventStartTime = None, nextEventDay = 'Today'):
        
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validate ' + strSysMode + ' Mode')   
        context.reporter.ReportEvent('Test Validation', 'Validating <B>' + strSysMode + ' </B>Mode with Device State as <B>' + str(strExpectedState) + \
                             '</B> for every <B>' + str(intCheckTImeInterval) + ' second(s) </B>for a duration of <B>' + str(round(intCheckDuration/60, 2)) + ' minute(s)', 'Done')
        
        #Iterate the validation of system mode
        for intCntr in range(int(intCheckDuration/intCheckTImeInterval)):
            #Log the Validation of current attributes with Expected Test and Model Attribute values
            if boolAutoMode and context.reporter.APIType != 'PLATFORM' : self.validateAndUpdateLog(context.reporter, 'Model')
            self.validateAndUpdateSPLog(context.reporter, 'Test', SPNodeID, strSysMode, strExpectedState, intBrightness, strExpextedHolidayStart, strExpectedHolidayEnd)
            
            #Wait for the Check Time interval
            time.sleep(intCheckTImeInterval)
            if intCntr==int(intCheckDuration/intCheckTImeInterval) - 1:
                time.sleep(intCheckDuration%intCheckTImeInterval)
            if not nextEventStartTime is None:
                if not oSchdUt.checkGuardTime(nextEventStartTime, nextEventDay): return 
                
    def validateSysmodeWithoutTargTemp(self, reporter, boolAutoMode, oThermostatEP, strSysMode, intCheckDuration = 600, intCheckTImeInterval = 30):
        reporter.HTML_TC_BusFlowKeyword_Initialize('Validate ' + strSysMode + ' Mode')    
        reporter.ReportEvent('Test Validation', 'Validating <B>' + strSysMode + ' </B>Mode for every <B>' + str(intCheckTImeInterval) + ' second(s) </B>for a duration of <B>' + str(round(intCheckDuration/60, 2)) + ' minute(s)', 'Done')
        
        #Iterate the validation of system mode
        for intCntr in range(int(intCheckDuration/intCheckTImeInterval)):
            #Log the Validation of current attributes with Expected Test and Model Attribute values
            if boolAutoMode and 'PLATFORM' not in reporter.APIType.upper():  self.validateAndUpdateLog(reporter, oThermostatEP, 'Model')
            self.validateAndUpdateLog(reporter, oThermostatEP, 'Test', strSysMode)
            
            #Wait for the Check Time interval
            time.sleep(intCheckTImeInterval)
            if intCntr==int(intCheckDuration/intCheckTImeInterval) - 1:
                time.sleep(intCheckDuration%intCheckTImeInterval)

    #Gets the log and validates the same and updates the report        
    def validateAndUpdateLog(self, reporter, oThermostatEP, strValidationType, strExpectedMode ='AUTO', strExpectedTemperature=1.0, strExpextedHolidayStart = "", strExpectedHolidayEnd = ""):
        if strValidationType.upper() == "MODEL":
            strLog, strStatus = self.getLog(oThermostatEP, strValidationType)
            reporter.ReportEvent('Model Validation', strLog, strStatus, 'Center')
        elif strValidationType.upper() == "TEST":
            strLog, strStatus = self.getLog(oThermostatEP, strValidationType, strExpectedMode, strExpectedTemperature,  strExpextedHolidayStart, strExpectedHolidayEnd)
            reporter.ReportEvent('Test Validation', strLog, strStatus, 'Center')
        elif strValidationType.upper() == "MAIN CLIENT":
            strLog, strStatus = self.getLog(oThermostatEP, strValidationType, strExpectedMode, strExpectedTemperature,  strExpextedHolidayStart, strExpectedHolidayEnd)
            reporter.ReportEvent('Main Client Validation', strLog, strStatus, 'Center')
        elif strValidationType.upper() == "SECONDARY CLIENT":
            strLog, strStatus = self.getLog(oThermostatEP, strValidationType, strExpectedMode, strExpectedTemperature,  strExpextedHolidayStart, strExpectedHolidayEnd)
            reporter.ReportEvent('Secondary Client Validation', strLog, strStatus, 'Center')
            
    #Gets the SP log and validates the same and updates the report        
    def validateAndUpdateSPLog(self, reporter, strValidationType, SPNodeID, strExpectedMode ='AUTO', strExpectedState = "OFF", intBrightness = 0, strExpextedHolidayStart = "", strExpectedHolidayEnd = ""):
        if strValidationType.upper() == "TEST":
            strLog, strStatus = self.getSPLog(strValidationType, SPNodeID, strExpectedMode, strExpectedState,  intBrightness, strExpextedHolidayStart, strExpectedHolidayEnd)
            reporter.ReportEvent('Test Validation', strLog, strStatus, 'Center')
            strLog, strStatus = self.getBrightnessALLog(strValidationType, SPNodeID, strExpectedMode, strExpectedState,  intBrightness, strExpextedHolidayStart, strExpectedHolidayEnd)
            reporter.ReportEvent('Test Validation', strLog, strStatus, 'Center')
        elif strValidationType.upper() == "MAIN CLIENT":
            strLog, strStatus = self.getSPLog(strValidationType, strExpectedMode, strExpectedState,  intBrightness, strExpextedHolidayStart, strExpectedHolidayEnd)
            reporter.ReportEvent('Main Client Validation', strLog, strStatus, 'Center')
        elif strValidationType.upper() == "SECONDARY CLIENT":
            strLog, strStatus = self.getSPLog(strValidationType, strExpectedMode, strExpectedState,  intBrightness, strExpextedHolidayStart, strExpectedHolidayEnd)
            reporter.ReportEvent('Secondary Client Validation', strLog, strStatus, 'Center')
            
    #Gets the Log to be updated in the Report
    def getLog(self, oThermostatEP, strValidationType, strExpectedMode ='', strExpectedSPTemp=1.0, strExpextedHolidayStart = "", strExpectedHolidayEnd = ""):
        '''
        strStatusCode = str(oThermostatEP.model.statusCode)
        print(strStatusCode)
        if len(strStatusCode.split(":"))>1:
            strStatusCode = strStatusCode[1] + ' for: <br>'
        print(strStatusCode)
        '''
        strLocalTemperature = 0.0
        strActualTSEPSPTemp = 0.0
        strExpectedTHRunState = ''
        if 'CLIENT' in strValidationType.upper(): oThermostatEP.update_attributes_from_client()
        else:
            try:  
                oThermostatEP.update()
            except: pass
            
        strActualTSEPMode = oThermostatEP.mode
        if not oThermostatEP.type=='WATER':
            strActualTSEPSPTemp = self.convertHexTemp(oThermostatEP.occupiedHeatingSetpoint, False)
            strLocalTemperature = self.convertHexTemp(oThermostatEP.localTemperature, False)
        strActualTSRunState = oThermostatEP.thermostatRunningState
        if strActualTSRunState == '0000': strActualTSRunState = 'OFF'
        else: strActualTSRunState = 'ON'
        
        #Setting Expected Thermostat run state for Test Validation
        if oThermostatEP.type=='WATER' and strValidationType.upper() != "MODEL":
            if self.getWaterModes[strExpectedMode]== 'Always OFF': strExpectedTHRunState = 'OFF'
            elif self.getWaterModes[strExpectedMode]=='AUTO':  
                print('Current Event ', oSchdUt.getCurrentTempFromSchedule(oThermostatEP.getSchedule()))
                if 0.0 in oSchdUt.getCurrentTempFromSchedule(oThermostatEP.getSchedule()): strExpectedTHRunState = 'OFF'
                else: strExpectedTHRunState = 'ON'
            elif self.getWaterModes[strExpectedMode]=='BOOST' or self.getWaterModes[strExpectedMode]=='Always ON':  strExpectedTHRunState = 'ON'
        #For Heating
        else:
            if float(strLocalTemperature) < float(strActualTSEPSPTemp):
                strExpectedTHRunState = 'ON'
            else:
                strExpectedTHRunState = 'OFF'
                
            
        #Get Expected values from Thermostat Model Validation
        if strValidationType.upper() == "MODEL":  
            strExpectedMode = oThermostatEP.model.mode
            if not oThermostatEP.type=='WATER':
                strExpectedSPTemp = oThermostatEP.model.occupiedHeatingSetpoint
                if not isinstance(strExpectedSPTemp, float): strExpectedSPTemp = self.convertHexTemp(strExpectedSPTemp, False)
            #Setting Expected Thermostat run state for Model validation
            strExpectedTHRunState = oThermostatEP.model.thermostatRunningState
            if strExpectedTHRunState == '0000': strExpectedTHRunState = 'OFF'
            else: strExpectedTHRunState = 'ON'
            #Holiday Mode
            if 'HOLIDAY' in strExpectedMode:
                strExpextedHolidayStart = oThermostatEP.model.holidayModeStart
                strExpectedHolidayEnd = oThermostatEP.model.holidayModeEnd
        
        #Set Water Mode Format
        if oThermostatEP.type=='WATER':
            strActualTSEPMode = self.getWaterModes[strActualTSEPMode]
            strExpectedMode = self.getWaterModes[strExpectedMode]
            if strActualTSEPMode=='AUTO': strActualTSEPMode = 'AUTO-' + strActualTSRunState
            if strExpectedMode=='AUTO': strExpectedMode = 'AUTO-' + strExpectedTHRunState
            
        #Holiday Mode
        if strExpectedMode is not None:
            if 'HOLIDAY' in strExpectedMode:
                strActualHolidayStart = oThermostatEP.holidayStart
                strActualHolidayEnd = oThermostatEP.holidayEnd
            
            
        
        strTempCompLog = ''
        boolStatus = 'PASS'
        #Mode
        if not oThermostatEP.type=='WATER':
            if not isinstance(strActualTSEPSPTemp, str): strActualTSEPSPTemp = str(strActualTSEPSPTemp)
        if str(strExpectedMode) == str(strActualTSEPMode):
            strActualTSEPMode = '$$' + str(strActualTSEPMode)
        else:            
            strActualTSEPMode = '$$||' + strActualTSEPMode
            boolStatus = 'FAIL'
        #Temperature
        if not oThermostatEP.type=='WATER':
            if str(strExpectedSPTemp) == str(strActualTSEPSPTemp):
                strActualTSEPSPTemp = '$$' + strActualTSEPSPTemp
            else:            
                strActualTSEPSPTemp = '$$||' + strActualTSEPSPTemp
                boolStatus = 'FAIL'
        #Running State
        if strExpectedTHRunState == strActualTSRunState:
            strActualTSRunState = '$$' + strActualTSRunState
        else:            
            strActualTSRunState = '$$||' + strActualTSRunState
            boolStatus = 'FAIL'
        #Adding C
        if not oThermostatEP.type=='WATER':
            strExpectedSPTemp = str(strExpectedSPTemp) + 'C' 
            strActualTSEPSPTemp = str(strActualTSEPSPTemp) + 'C'
        
        #Holiday Mode
        if strExpectedMode is not None:
            if 'HOLIDAY' in strExpectedMode:
                if str(strExpextedHolidayStart) == str(strActualHolidayStart):
                    strActualHolidayStart = '$$' + str(strActualHolidayStart)
                else:            
                    strActualHolidayStart = '$$||' + str(strActualHolidayStart)
                    boolStatus = 'FAIL'
                if str(strExpectedHolidayEnd) == str(strActualHolidayEnd):
                    strActualHolidayEnd = '$$' + str(strActualHolidayEnd)
                else:            
                    strActualHolidayEnd = '$$||' + str(strActualHolidayEnd)
                    boolStatus = 'FAIL'
        
        
        #Setting the Header for Pass and Fail
        if boolStatus=='PASS':
            strHeader = "Attributes$$" +  "Expected-" + strValidationType + "  and Actual-Thermostat Values" + "@@@"
            strActualTSEPMode =''
            strActualTSEPSPTemp = ''
            strActualTSRunState = ''
            strActualHolidayStart = ''
            strActualHolidayEnd = ''
        else:
            strHeader = "Attributes$$" +  "Expected-" + strValidationType + " Values$$" + "Actual-Thermostat Values" + "@@@"
        strLog = ''
        if strExpectedMode is not None:
            if not oThermostatEP.type=='WATER': 
                strTempCompLog ='$~Current Setpoint Temperature$$'     + strExpectedSPTemp     + strActualTSEPSPTemp    
            strLog = strHeader                                                                               + \
                     'Current System mode$$'                + strExpectedMode       + strActualTSEPMode      + strTempCompLog + \
                     '$~Current Thermostat Running State$$' + strExpectedTHRunState + strActualTSRunState
            
            if 'HOLIDAY' in strExpectedMode: 
                strLog = strLog + '$~Holiday Mode Start Date$$' + str(strExpextedHolidayStart) + str(strActualHolidayStart) + \
                '$~Holiday Mode End Date$$' + str(strExpectedHolidayEnd) + str(strActualHolidayEnd)
                
        return strLog, boolStatus
    
        #Gets the SP Log to be updated in the Report
    def getSPLog(self, strValidationType, SPNodeID, strExpectedMode ='', strExpectedState = "OFF", intBrightness = 0, strExpextedHolidayStart = "", strExpectedHolidayEnd = ""):
        
        strActualSPMode, strActualSPState, intActualBrightness = getSPAttributes(SPNodeID)
        
        strStateCompLog = ''
        boolStatus = 'PASS'
        #Mode
        if str(strExpectedMode) == str(strActualSPMode):
            strActualSPMode = '$$' + str(strActualSPMode)
        else:            
            strActualSPMode = '$$||' + strActualSPMode
            boolStatus = 'FAIL'
        #State
        if str(strExpectedState) == str(strActualSPState):
            strActualSPState = '$$' + strActualSPState
        else:            
            strActualSPState = '$$||' + strActualSPState
            boolStatus = 'FAIL'
        
        #Setting the Header for Pass and Fail
        if boolStatus=='PASS':
            strHeader = "Attributes$$" +  "Expected-" + strValidationType + "  and Actual-SP Values" + "@@@"
            strActualSPMode =''
            strActualSPState = ''
        else:
            strHeader = "Attributes$$" +  "Expected-" + strValidationType + " Values$$" + "Actual-SP Values" + "@@@"
        
        strStateCompLog ='$~Current State$$'     + strExpectedState     + strActualSPState 
        
        strLog = strHeader                                                                               + \
                 'Current System mode$$'                + strExpectedMode       + strActualSPMode      + strStateCompLog 
        
        
        return strLog, boolStatus
    
    def getBrightnessALLog(self, strValidationType, SPNodeID, strExpectedMode ='', strExpectedState = "OFF", intBrightness = 0, strExpextedHolidayStart = "", strExpectedHolidayEnd = ""):
        boolStatus = 'PASS'
        strActualSPMode, strActualSPState, intActualBrightness = getSPAttributes(SPNodeID)
        print("Brightness : " + str(intBrightness) + "\n")
        print("Actual Brightness : " + str(intActualBrightness)+ "\n")
        
        #Brightness
        if intBrightness == intActualBrightness:
            strActualBrightness = '$$' + str(intActualBrightness)
        else:            
            strActualBrightness = '$$||' + str(intActualBrightness)
            boolStatus = 'FAIL'
        
        
        #Setting the Header for Pass and Fail
        strHeader = "Attributes$$" +  "Expected-" + strValidationType + " Values$$" + "Actual-SP Values" + "@@@"
        
        strStateCompLog ='$~Current Brightness$$'     + str(intBrightness)     + strActualBrightness    
        strLog = strHeader                                                                               + \
                  strStateCompLog 
            
        return strLog, boolStatus
  
    #Converts the Report log format to Console print log
    def conertToPrintLog(self, strReportLog):
        arrReportLog = strReportLog.split("@@@")
        strPrintLog = arrReportLog[0].split("$$")[0] + ': ===>> Expected Thermostat Values:\n'
        for strRow in arrReportLog[1].split("$~"):
            strPrintLog = strPrintLog + strRow.split("$$")[0] + ' ===>> ' + strRow.split("$$")[1] + '\n'
            
        return strPrintLog
    
    
    #Converts the hex value of the retrieved temperature
    def convertHexTemp(self, hexTemperature, booWithCentigradeSymbol = True):
        if isinstance(hexTemperature, str):
            if booWithCentigradeSymbol:
                strTemperature = str(int(hexTemperature, 16) / 100) + 'C'
            else:
                strTemperature = str(int(hexTemperature, 16) / 100)
            return strTemperature
        else: return hexTemperature
    
    #initializes the required Client Drivers for the test
    def intializeDrivers(self, context):
        if 'PLATFORM' in context.APIType.upper():
            
            strUserName = utils.getAttribute('common', 'userName')
            strPassword = utils.getAttribute('common', 'password')
            boolAndroidDriverSetUp = False
            boolIOSDriverSetUp = False
            boolWebDriverSetUp = False
            boolLoadSecondaryClient = False
            
            #strMainClient = utils.getAttribute('common', 'mainClient')
            #strSecondaryClient = utils.getAttribute('common', 'secondClient')
            #if not 'WEB' in  strMainClient.upper(): boolLoadSecondaryClient = True
            print( context.oScenarioClientsDict)
            for  strClient in context.oScenarioClientsDict.keys():
                if strClient.upper().find('ANDROID') >= 0 and (not boolAndroidDriverSetUp):
                    oBasePage = paygeAndroid.BasePage(None, context.reporter)
                    strAppPath = utils.getAttribute('android', 'appFileName')
                    strAndroidPlatformVersion = utils.getAttribute('android', 'platformVersion')
                    strDeviceName = utils.getAttribute('android', 'deviceName')
                    context.oThermostatEP.AndroidDriver  = oBasePage.setup_android_driver(strAndroidPlatformVersion, strDeviceName, strAppPath)
                    oLoginPage = paygeAndroid.LoginPage(context.oThermostatEP.AndroidDriver, context.reporter)
                    #oLoginPage.login_hive_app(strUserName, strPassword)
                    boolAndroidDriverSetUp = True
                elif (strClient.upper().find('WEB') >= 0 and (not boolWebDriverSetUp)) or boolLoadSecondaryClient:
                    boolLoadSecondaryClient = False
                    strURL = utils.getAttribute('web', 'loginURL')
                    strBrowserName = utils.getAttribute('web', 'browserName')
                    oBasePage = paygeWeb.BasePage(None, context.reporter)
                    context.oThermostatEP.WebDriver = oBasePage.setup_Selenium_driver(strBrowserName, strURL)
                    oLoginPage = paygeWeb.LoginPage(context.oThermostatEP.WebDriver, context.reporter)
                    oLoginPage.login_hive_app(strUserName, strPassword)
                    boolWebDriverSetUp  =True
                elif strClient.upper().find('IOS') >= 0 and (not boolIOSDriverSetUp):
                    strAppPath = utils.getAttribute('iOS', 'appFileName')
                    strDeviceName = utils.getAttribute('iOS', 'deviceName')
                    oBasePage = paygeiOS.BasePage(None, context.reporter)
                    context.oThermostatEP.iOSDriver  = oBasePage.setup_ios_driver(strDeviceName, strAppPath)
                    oLoginPage = paygeiOS.LoginPage(context.oThermostatEP.iOSDriver, context.reporter)
                    oLoginPage.login_hive_app(strUserName, strPassword)
                    boolIOSDriverSetUp = True
                    '''
                    oHomePage = paygeiOS.HomePage(context.oThermostatEP.iOSDriver, context.reporter)
                    oHomePage.navigate_to_heating_control_page()
                    oHeatingControlPage = paygeiOS.HeatingControlPage(context.oThermostatEP.iOSDriver, context.reporter)
                    oHeatingControlPage.set_heat_mode('AUTO')
                    oBasePage.refresh_page()
                    context.oThermostatEP.iOSDriver.quit()
                    exit()
                    '''
                    
    #Kills the required Client Drivers for the test               
    def quitDrivers(self, context):
        if not context.AndroidDriver is None: context.AndroidDriver.quit()
        if not context.WebDriver is None: context.WebDriver.quit()
        if not context.iOSDriver is None: context.iOSDriver.quit()
        
    def navigateToScreen(self,reporter,oThermostatEP,strPage):
        reporter.HTML_TC_BusFlowKeyword_Initialize('Navigate to : ' + str(strPage) + ' screen') 
        #Set the page to navigate       
        oThermostatEP.navigateToScreen(strPage)           
        reporter.ReportEvent('Test Validation','navigate to <B>' + str(strPage), 'PASS')
        if not reporter.ActionStatus: return False
    
    def changePassword(self,reporter,oThermostatEP,strPage):
        reporter.HTML_TC_BusFlowKeyword_Initialize('Navigate to : ' + str(strPage) + ' screen') 
        #Set the page to navigate       
        oThermostatEP.changePasswordScreen(strPage)           
        reporter.ReportEvent('Test Validation','navigate to <B>' + str(strPage), 'PASS')
        if not reporter.ActionStatus: return False
                  
    def navigateToHoildayScreen(self,reporter,oThermostatEP,context,strPage):
        reporter.HTML_TC_BusFlowKeyword_Initialize('Navigate to : ' + str(strPage) + ' screen') 
        #Set the page to navigate       
        oThermostatEP.navigateToHoildayScreen(context)           
        reporter.ReportEvent('Test Validation','navigate to <B>' + str(strPage), 'PASS')
        if not reporter.ActionStatus: return False
        
    def setHoildayMode(self,reporter,oThermostatEP,context, strHolidayStart, strHolidayStartTime, strDuration):
        reporter.HTML_TC_BusFlowKeyword_Initialize('Set Holiday mode settings') 
        #Set the page to navigate       
        oThermostatEP.setHolidayMode(context, strHolidayStart, strHolidayStartTime, strDuration)       
        reporter.ReportEvent('Test Validation','Set Holiday mode settings', 'PASS')
        if not reporter.ActionStatus: return False
        
    def activateHolidayMode(self,context):
        print('hi')
    
    
    
    
    def verifyHolidayMode(self,context):
        print('hi')
    
    def validateNotification(self,reporter,boolAutoMode,oThermostatEP,strExpectedTemp,strRuleType) :
        reporter.HTML_TC_BusFlowKeyword_Initialize('Validate ' + strRuleType + ' Notification Alert')  
        reporter.ReportEvent('Test Validation', 'Validating <B>' + strRuleType + '</B> Notification Alert with Temperature set to <B>' + str(strExpectedTemp) + '</B>', 'Done') 
        self.validateAndUpdateRulesLog(reporter,oThermostatEP,'TEST',strExpectedTemp,strRuleType)
        
    def validateNotificationOnOff(self,reporter,boolAutoMode,oThermostatEP,strExpectedTemp,strRuleType,strExpectedRuleStatus) :
        reporter.HTML_TC_BusFlowKeyword_Initialize('Validate ' + strExpectedRuleStatus + ' Notification Alert')  
        reporter.ReportEvent('Test Validation', 'Validating Notification Alert as <B>' + strExpectedRuleStatus + '</B>', 'Done') 
        self.validateAndUpdateRulesLog(reporter,oThermostatEP,'TEST',strExpectedTemp,strRuleType,strExpectedRuleStatus)
            
    def validateAndUpdateRulesLog(self,reporter,oThermostatEP,strValidationType,strExpectedTemp,strRuleType,strExpectedRuleStatus='ACTIVE') :
        if strValidationType.upper() == 'TEST':
            strLog, strStatus = self.getRulesLog(oThermostatEP,strValidationType,strExpectedTemp,strRuleType,strExpectedRuleStatus)
            reporter.ReportEvent('Test Validation', strLog, strStatus, 'Center')
            
    def getRulesLog(self,oThermostatEP, strValidationType,strExpectedTemp,strRuleType,strExpectedRuleStatus):   
        oThermostatEP.update()     
        formattedRules=oThermostatEP.getHeatRule()
        boolStatus='PASS'
        strActualRules=[]
        strRulesAvailable = ('TooHot','TooCold')
        #RuleNameList = sorted(formattedRules)
        
            
              
        if strRuleType.upper().find('HIGH')>=0 :
            strExpRuleName = strRulesAvailable[0]
 
        else :
            strExpRuleName = strRulesAvailable[1]
 
            
        if strExpRuleName in formattedRules :
              
            strActualRuleName = strExpRuleName
            strActualRuleName = '$$' + strActualRuleName
            
            strActualRules=formattedRules[strExpRuleName]
               
            strActualRuleStatus = strActualRules[2]
            if strExpectedRuleStatus == strActualRuleStatus :
                strActualRuleStatus = '$$' + strActualRuleStatus                  
            else :
                strActualRuleStatus = '$$||' + strActualRuleStatus
                boolStatus = 'FAIL'
                
            strActualNotiTemp = strActualRules[0] 
            print(strActualNotiTemp)   
            if float(strActualNotiTemp) == float(strExpectedTemp):
                strActualNotiTemp = '$$' + strActualNotiTemp
                    
            else:            
                strActualNotiTemp = '$$||' + strActualNotiTemp
                boolStatus = 'FAIL'
                   
        else :
            strActualRuleName = '$$' + 'No '+ strExpRuleName +' rule set'
            boolStatus = 'FAIL'

         
        if boolStatus=='PASS':
            strHeader = "Attributes$$" +  "Expected-" + strValidationType + "  and Actual-Rule Values" + "@@@"
            strActualNotiTemp = ''
            strActualRuleName = ''
            strActualRuleStatus = ''
        else :
            strHeader = "Attributes$$" +  "Expected-" + strValidationType + " Values$$" + "Actual-Rule Values" + "@@@"
        
        strLog = ''
        strTempCompLog ='$~Current Rule Temperature$$'     + str(strExpectedTemp)    + str(strActualNotiTemp)    
        strLog = strHeader                                                                               + \
                'Current Rule name$$'                + strExpRuleName       + strActualRuleName      + strTempCompLog + \
                '$~Current Rule Status$$' + strExpectedRuleStatus + strActualRuleStatus
        
        return strLog, boolStatus
            #
                #print()

  
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
    intBrightness = 0
    syntheticNodeID = getSyntheticDeviceID(nodeID)
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session  = ALAPI.sessionObject()
    resp = ALAPI.getNodesV6(session)
    for oNode in resp['nodes']:
        if nodeID in oNode["id"]:
            strState = getAttribute(oNode["attributes"], "state")
            if 'brightness' in oNode["attributes"]:
                intBrightness = int(getAttribute(oNode["attributes"], "brightness"))
        elif oNode["id"] in syntheticNodeID:
            oJson = oNode["attributes"]["syntheticDeviceConfiguration"]["reportedValue"]
            if isinstance(oJson, str): oJson = json.loads(oJson)
            if oJson["enabled"]:
                strMode = "AUTO"
            else:
                strMode = "MANUAL"
                oNode["attributes"]
    return strMode, strState, intBrightness

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


    
    
