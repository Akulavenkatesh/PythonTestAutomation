'''
Created on 10 Aug 2016

@author: Hitesh Sharma
@note: Contact sensor Test case
'''

from datetime import datetime, timedelta
import time

from behave import *

import BB_ReusableFunctionModule as bUtils
import CC_platformAPI as cUtils
import DD_Page_iOSApp as pageiOS
import FF_Platform_Utils as pUtils
import FF_alertmeApi as ALAPI
import FF_threadedSerial as AT
import FF_utils as utils


@given(u'The Hive product is paired with hub')
def setContactSensor(context):
    #get device version id
    oDeviceVersionList = pUtils.getNodeAndDeviceVersionID()
    print(oDeviceVersionList, "\n")
    oSensorEP = context.oThermostatClass.heatEP
    oSensorEP.reporter = context.reporter
    oSensorEP.iOSDriver = context.iOSDriver
    context.reporter.ActionStatus = True
    context.oThermostatEP = oSensorEP

@when(u'User redirect to the {nameContactSensor} screen {strClientType}')
def navigatetoContactSensorScreen(context,nameContactSensor,strClientType):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Navigate to given '+nameContactSensor+ ' Screen')
    utils.setClient(context, strClientType)
    context.oThermostatEP.navigatetoContactSensor(nameContactSensor)
    

@then(u'Verify the current status of the {nameContactSensor}')
def getCurrentDevicestatus(context,nameContactSensor):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Captured the current '+nameContactSensor+ ' status')
    currentStatus = context.oThermostatEP.currentCSStatus(nameContactSensor)
    if currentStatus == "open":
        print(currentStatus)
        print("Current Status of given contact sensor is open")
    else:
        print(currentStatus)
        print("Current Status of given contact sensor is closed")
     
        
@when(u'Get the response from API for {nameContactSensor} for {DeviceType}')
def getCurrentResponseAPI(context,nameContactSensor,DeviceType): 
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validating API status for given '+nameContactSensor+ ' status')
    
    ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
    session  = ALAPI.sessionObject()
    #get node lists
    oDeviceNodeVersionList = pUtils.getNodeAndDeviceVersionID()
    print(oDeviceNodeVersionList, "\n") 
    
    #Extract only node ID for given device type
    oDeviceNodeID= pUtils.getDeviceNodeID(DeviceType) 
    print(oDeviceNodeID, "\n")
    
    #Get the the final Status of Contact sensor from platform
    finalCSState = pUtils.getCSAttributes(oDeviceNodeID)
    
    print(finalCSState)               
    ALAPI.deleteSessionV6(session)
    #To Do - We are not comparing the current status of App and platform until robo arm logic in place or something else.

    
@then(u'User navigates to the event logs in the Client')
def navigateToTodaysLogScreen(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Hive user able to navigate to Log screen successfully')
    context.oThermostatEP.accessTodaysLog()

@when(u'User check {selectWeekDay} back in the event logs in the Client')
def verifyGivenDayLog(context, selectWeekDay):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Hive user able to navigate to '+selectWeekDay+ ' day back in log section')
    context.oThermostatEP.eventLogScreen(selectWeekDay)

@then(u'Validate the event logs are displayed')
def verifyEventLog(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Hive user able to see the event logs state on log detail screen')
    context.oThermostatEP.verfiyEventLogs()



@when(u'the below {Device} Sensor Checkin is verifiied every five mins infinitely via Telegisis')
def sensorCheckinVerify(context, Device):
    
    AT.flushRxQ()
    
    # Loop until all retries done
    respValue = ''
    respState = False
    doLoop = True
    intCntr = 0
    intTCStartTime = time.monotonic()
#     myTime = datetime.now().strftime("%H:%M:%S.%f") 
    while doLoop:
        
        # Some message received so do something with it
        if not AT.rxQueue.empty():
            resp = AT.rxQueue.get()
            
            print(resp)
            if "CHECKIN" in resp:
                intCntr = intCntr+ 1
                context.reporter.HTML_TC_BusFlowKeyword_Initialize(Device + 'Checkin Counter: ' + str(intCntr))
                intTCEndTime = time.monotonic()
                strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
                strTCDuration = AT.getDuration(strTCDuration)   
                intSeconds = float(strTCDuration.split(",")[1].strip().split(" ")[0])
                intMin = float(strTCDuration.split(",")[0].strip().split(" ")[0])
                intSeconds = intMin*60.0 + intSeconds
                print("Time taken: " + strTCDuration)
                context.reporter.ReportEvent('Test Validation', Device + 'Checkin Counter: ' + str(strTCDuration), "DONE")
                intTCStartTime = time.monotonic()