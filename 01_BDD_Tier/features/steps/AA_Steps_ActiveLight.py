'''
Created on 14 Jan 2016

@author: ranganathan.veluswamy
'''

from datetime import timedelta
import time

from behave import *

import AA_Steps_SmartPlug as SP
import FF_alertmeApi as ALAPI
import FF_threadedSerial as AT
import FF_utils as utils
#from PIL.ImageEnhance import Brightness


lightSensorCalibration = {0: (1100, 2000),
                                         20:(3000, 3600),
                                         40:(7000, 8500),
                                         50:(9000, 11750),
                                         60:(13000, 15000),
                                         80:(19000, 22000),
                                         100:(26000, 30000)}

lightSensorCalibration = {0: (1100, 1500),
                                         20:(2200, 2700),
                                         40:(5000, 6500),
                                         50:(7000, 9250),
                                         60:(9000, 12000),
                                         80:(14000, 17000),
                                         100:(18000, 23000)}

lightSensorCalibration = {0: (0, 700),
                                         20:(850, 1200),
                                         40:(2400, 2800),
                                         50:(3450, 4150),
                                         60:(4500, 5500),
                                         80:(6900, 7600),
                                         100:(9000, 12000)}

@when(u'The {ActiveLightDevice} is switched ON and OFF state and brightness of the light is varied and validated for the below brightness values infinitely via Hub')
def validateActiveLightFunctionViaHub(context, ActiveLightDevice):
    
    oColorTempList = {0:"2700",
                                  20:"3460",
                                  40:"4220",
                                  60:"4980",
                                  80:"5740",
                                  100:"6500"}
    oColorTempList = {0:2700,
                                  20:3460,
                                  40:4220,
                                  60:4980,
                                  80:5740,
                                  100:6500}
    oColorTempPercentageList = list(oColorTempList.keys())
    
    #get node lists
    #nodeIdList = context.oThermostatEP.getNodeID(resp)
    nodeIdList = SP.getNodeAndDeviceVersionID()
    print(nodeIdList)
    print(ActiveLightDevice)
    if 'ActiveLight' in ActiveLightDevice:
        if 'FWBulb01_1' in nodeIdList:
            strLightNodeID = nodeIdList['FWBulb01_1']["nodeID"]
        elif 'LDS_DimmerLight_1' in nodeIdList:
            strLightNodeID = nodeIdList['LDS_DimmerLight_1']["nodeID"]
    elif  ActiveLightDevice in nodeIdList:
            strLightNodeID = nodeIdList[ActiveLightDevice]["nodeID"]
    else: 
        context.reporter.ReportEvent('Test Validation', "Active light Node is missing.", "FAIL")
        return False
    
    intCntr = 0
    
    #Open Text file to write the light parameters
    oFileWriter = open(context.reporter.strCurrentTXTFolder+ "LUXvsTEMP.txt", 'w')
    oFileWriter.write("Iteration,ColorTemp,0_%,20_%,40_%,60_%,80_%,100_% \n")
    oFileWriter.close()
    del oFileWriter
    
    while True:
        ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
        session  = ALAPI.sessionObject()
        
        strParameterValue = ""
        intCntr = intCntr + 1
        strParameterValue = str(intCntr)
        boolPass = True
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Active Light Brightness validation Counter: ' + str(intCntr))
        
        if "TWBULB" in ActiveLightDevice.upper():
            intTempCntr = intCntr % 5
            print(intTempCntr)
            myColourTemp = oColorTempList[oColorTempPercentageList[intTempCntr]]
            
            ALAPI.setActiveLightColourTemperature(session, strLightNodeID, myColourTemp)
            context.reporter.ReportEvent('Test Validation', "Active light is set to Color Temperature : <B>" + str(myColourTemp) + "</B>", "Done")
            strParameterValue = strParameterValue + "," + myColourTemp
        
        #Set Light ON
        ALAPI.setActiveLightState(session, strLightNodeID, "ON")
        context.reporter.ReportEvent('Test Validation', "Active light is switched <B>ON</B>", "PASS")
        time.sleep(5)
        oBrightnessList = []
        #ChangeBrightness
        for oRow in context.table:
            intBrightness = int(oRow['BrightnessValue'])
            #print("intBrightness", intBrightness)
            ALAPI.setActiveLightBrightness(session, strLightNodeID, intBrightness)
            context.reporter.ReportEvent('Test Validation', "Active light Brightness is set to : <B>" + str(intBrightness) + "</B>", "Done")
            time.sleep(5)
            if intBrightness in lightSensorCalibration:
                intLowLimit = lightSensorCalibration[intBrightness][0]
                intHighLimit = lightSensorCalibration[intBrightness][1]
                sensorValue,_,_ = utils.get_lux_value()
                if intLowLimit < sensorValue and intHighLimit > sensorValue:
                    context.reporter.ReportEvent('Test Validation', "The measured LUX value for Active light Brightness is: <B>" + str(sensorValue) + "</B>. Which is within the calibration limit: " + str(intLowLimit) + " - " + str(intHighLimit), "PASS")
                else: 
                    context.reporter.ReportEvent('Test Validation', "The measured LUX value for Active light Brightness is: <B>" + str(sensorValue) + "</B>. Which is <B>NOT</B> the calibration limit: " + str(intLowLimit) + " - " + str(intHighLimit), "FAIL")
                    boolPass = False
                    
                if not intBrightness in oBrightnessList: 
                    oBrightnessList.append(intBrightness)
                    strParameterValue = str(intBrightness) + "," + str(sensorValue)
            else:
                context.reporter.ReportEvent('Test Validation', "The Brightness values should be in multiples of 20", "FAIL")
        
        #Update Text file
        oFileWriter = open(context.reporter.strCurrentTXTFolder+ "LUXvsTEMP.txt", 'a')
        oFileWriter.write(strParameterValue + "\n")
        oFileWriter.close()
        del oFileWriter
        
        #Update the Pass and Fail counters
        context.reporter.intIterationCntr = intCntr
        if boolPass: context.reporter.intIterationPassCntr = context.reporter.intIterationPassCntr + 1
        else: context.reporter.intIterationFailCntr = context.reporter.intIterationFailCntr + 1
        
        #Set Light OFF
        ALAPI.setActiveLightState(session, strLightNodeID, "OFF")
        context.reporter.ReportEvent('Test Validation', "Active Plug is switched <B>OFF</B>", "PASS")
        time.sleep(5)
        ALAPI.deleteSessionV6(session)
        
@when(u'The {ActiveLightDevice} is switched ON and OFF state and brightness of the light is varied and validated for {TimePeriod} for the below brightness values infinitely via Hub')
def validateActiveLightFunctionForPeriodViaHub(context, ActiveLightDevice, TimePeriod):
    TimePeriodinSec = int(TimePeriod) * 60
    oColorTempList = {0:"2700",
                                  20:"3460",
                                  40:"4220",
                                  60:"4980",
                                  80:"5740",
                                  100:"6500"}
    oColorTempPercentageList = list(oColorTempList.keys())
    
    #get node lists
    #nodeIdList = context.oThermostatEP.getNodeID(resp)
    nodeIdList = SP.getNodeAndDeviceVersionID()
    print(nodeIdList)
    print(ActiveLightDevice)
    if 'ActiveLight' in ActiveLightDevice:
        if 'FWBulb01_1' in nodeIdList:
            strLightNodeID = nodeIdList['FWBulb01_1']["nodeID"]
        elif 'LDS_DimmerLight_1' in nodeIdList:
            strLightNodeID = nodeIdList['LDS_DimmerLight_1']["nodeID"]
    elif  ActiveLightDevice in nodeIdList:
            strLightNodeID = nodeIdList[ActiveLightDevice]["nodeID"]
    else: 
        context.reporter.ReportEvent('Test Validation', "Active light Node is missing.", "FAIL")
        return False
    
    intCntr = 0
    
    #Open Text file to write the light parameters
    oFileWriter = open(context.reporter.strCurrentTXTFolder+ "LUXvsTEMP.txt", 'w')
    oFileWriter.write("Iteration,ColorTemp,0_%,20_%,40_%,60_%,80_%,100_% \n")
    oFileWriter.close()
    del oFileWriter
    
    while True:
        ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
        session  = ALAPI.sessionObject()
        
        strParameterValue = ""
        intCntr = intCntr + 1
        strParameterValue = str(intCntr)
        boolPass = True
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Active Light Brightness validation Counter: ' + str(intCntr))
        
        if "TWBULB" in ActiveLightDevice.upper():
            intTempCntr = intCntr % 5
            print(intTempCntr)
            myColourTemp = oColorTempList[oColorTempPercentageList[intTempCntr]]
            
            ALAPI.setActiveLightColourTemperature(session, strLightNodeID, myColourTemp)
            context.reporter.ReportEvent('Test Validation', "Active light is set to Color Temperature : <B>" + str(myColourTemp) + "</B>", "Done")
            strParameterValue = strParameterValue + "," + myColourTemp
        
        #Set Light ON
        ALAPI.setActiveLightState(session, strLightNodeID, "ON")
        context.reporter.ReportEvent('Test Validation', "Active light is switched <B>ON</B>", "PASS")
        time.sleep(5)
        oBrightnessList = []
        #ChangeBrightness
        for oRow in context.table:
            intBrightness = int(oRow['BrightnessValue'])
            #print("intBrightness", intBrightness)
            ALAPI.setActiveLightBrightness(session, strLightNodeID, intBrightness)
            context.reporter.ReportEvent('Test Validation', "Active light Brightness is set to : <B>" + str(intBrightness) + "</B>", "Done")
            time.sleep(5)
            intCurrentTime = int(time.monotonic())
            intExpiryTime = intCurrentTime + TimePeriodinSec
            
            oFileWriter = open(context.reporter.strCurrentTXTFolder+ "LUXvsTEMP.txt", 'a')
            while intExpiryTime>intCurrentTime:                
                intCurrentTime = int(time.monotonic())
                if intBrightness in lightSensorCalibration:
                    intLowLimit = lightSensorCalibration[intBrightness][0]
                    intHighLimit = lightSensorCalibration[intBrightness][1]
                    sensorValue,_,_ = utils.get_lux_value()
                    if intLowLimit < sensorValue and intHighLimit > sensorValue:
                        #context.reporter.ReportEvent('Test Validation', "The measured LUX value for Active light Brightness is: <B>" + str(sensorValue) + "</B>. Which is within the calibration limit: " + str(intLowLimit) + " - " + str(intHighLimit), "PASS")
                        print('Test Validation', "The measured LUX value for Active light Brightness is: <B>" + str(sensorValue) + "</B>. Which is within the calibration limit: " + str(intLowLimit) + " - " + str(intHighLimit), "PASS")
                    else: 
                        #context.reporter.ReportEvent('Test Validation', "The measured LUX value for Active light Brightness is: <B>" + str(sensorValue) + "</B>. Which is <B>NOT</B> the calibration limit: " + str(intLowLimit) + " - " + str(intHighLimit), "FAIL")
                        print('Test Validation', "The measured LUX value for Active light Brightness is: <B>" + str(sensorValue) + "</B>. Which is <B>NOT</B> the calibration limit: " + str(intLowLimit) + " - " + str(intHighLimit), "FAIL")
                        boolPass = False
                        
                    if not intBrightness in oBrightnessList: 
                        oBrightnessList.append(intBrightness)
                        strParameterValue = str(intBrightness) + "," + str(sensorValue)
                    #Update Text file
                    strParameterValue = str(intBrightness) + "," + str(sensorValue) + "====>" + utils.getTimeStamp(False)
                    oFileWriter.write(strParameterValue + "\n")
                    time.sleep(0.5)
                else:
                    context.reporter.ReportEvent('Test Validation', "The Brightness values should be in multiples of 20", "FAIL")
            oFileWriter.close()
            
            del oFileWriter
        
        #Update Text file
        oFileWriter = open(context.reporter.strCurrentTXTFolder+ "LUXvsTEMP.txt", 'a')
        oFileWriter.write(strParameterValue + "\n")
        oFileWriter.close()
        del oFileWriter
        
        #Update the Pass and Fail counters
        context.reporter.intIterationCntr = intCntr
        if boolPass: context.reporter.intIterationPassCntr = context.reporter.intIterationPassCntr + 1
        else: context.reporter.intIterationFailCntr = context.reporter.intIterationFailCntr + 1
        
        #Set Light OFF
        ALAPI.setActiveLightState(session, strLightNodeID, "OFF")
        context.reporter.ReportEvent('Test Validation', "Active Plug is switched <B>OFF</B>", "PASS")
        time.sleep(5)
        ALAPI.deleteSessionV6(session)
        
        
           
@when(u'The ActiveLight is switched ON and OFF state and brightness of the light is varied and validated for the below brightness values for {Duration} via telegesis')
def activeLightBrightnessValidation(context, Duration):
    boolInfiniteExec = False
    if "INFIN" in Duration.upper():
        boolInfiniteExec = True
    else: 
        intMaxExecSeconds = int(Duration) * 60
    
    oColorTempList = {0:"00A5",
                                  20:"00C8",
                                  40:"00F0",
                                  60:"0118",
                                  80:"0140",
                                  100:"0172"}
    
    oColorTempList = {0:2700,
                                  20:3460,
                                  40:4220,
                                  60:4980,
                                  80:5740,
                                  100:6500}
     
     
    oColorTempPercentageList = list(oColorTempList.keys())
    _,_,myNodeId = utils.discoverNodeIDbyCluster("0000")
    #Get Model
    _, _, model = AT.getAttribute(myNodeId, "01", "0000", "0005", 'server')
    print(model)
    intTCStartTime = time.monotonic()
    intCntr = 0
    #Open Text file to write the light parameters
    oFileWriter = open(context.reporter.strCurrentTXTFolder+ "LUXvsTEMP.txt", 'w')
    oFileWriter.write("Iteration,ColorTemp,0_%,20_%,40_%,60_%,80_%,100_% \n")
    oFileWriter.close()
    del oFileWriter
    while True:
        strParameterValue = ""
        intCntr = intCntr + 1
        strParameterValue = str(intCntr)
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Active Light Brightness validation Counter: ' + str(intCntr))   
        if "TWBULB01" in model.upper():
            intTempCntr = intCntr % 5
            print(intTempCntr)
            myColourTemp = oColorTempList[oColorTempPercentageList[intTempCntr]]
            AT.colourTemperature(myNodeId, "01", 0, myColourTemp,0)
            context.reporter.ReportEvent('Test Validation', "Active light is set to Color Temperature : <B>" + str(myColourTemp) + "</B>", "Done")
            strParameterValue = strParameterValue + "," + str(myColourTemp)
        
        oBrightnessList = []
        for oRow in context.table:
            strBrightnesValue = oRow['BrightnessValue']
            intTimeLapse = int(oRow['TimeLapse'])
            
            print(strBrightnesValue, strBrightnesValue, "\n")
            print("myNodeId", myNodeId)
            
            
            if "ON" in strBrightnesValue.upper():
                AT.onOff(myNodeId, "01", 0, 1)
                context.reporter.ReportEvent('Test Validation', "Active light is set to : <B>" + str(strBrightnesValue) + "</B>", "Done")
            elif "OFF" in strBrightnesValue.upper():
                AT.onOff(myNodeId, "01", 0, 0)
                context.reporter.ReportEvent('Test Validation', "Active light is set to : <B>" + str(strBrightnesValue) + "</B>", "Done")
            else:                
                strBrightnesValue = int(strBrightnesValue)                
                #hexBrightnesValue = '{:02x}'.format(int(strBrightnesValue*2.55))
                intTimeLapseRep = '{:04x}'.format(intTimeLapse)
                respState,respCode,respValue =  AT.moveToLevel(myNodeId, "01",0, int(strBrightnesValue), int(intTimeLapseRep))
                print(intCntr, respState,respCode,respValue)
                context.reporter.ReportEvent('Test Validation', "Active light Brightness is set to : <B>" + str(strBrightnesValue) + "</B>", "Done")      
            #Validate Lux
            time.sleep(5)
            if strBrightnesValue in lightSensorCalibration:
                intLowLimit = lightSensorCalibration[strBrightnesValue][0]
                intHighLimit = lightSensorCalibration[strBrightnesValue][1]
                sensorValue,_,_ = utils.get_lux_value()
                if intLowLimit < sensorValue and intHighLimit > sensorValue:
                    context.reporter.ReportEvent('Test Validation', "The measured LUX value for Active light Brightness is: <B>" + str(sensorValue) + "</B>. Which is within the calibration limit: " + str(intLowLimit) + " - " + str(intHighLimit), "PASS")
                else: 
                    context.reporter.ReportEvent('Test Validation', "The measured LUX value for Active light Brightness is: <B>" + str(sensorValue) + "</B>. Which is <B>NOT</B> the calibration limit: " + str(intLowLimit) + " - " + str(intHighLimit), "FAIL")
                    boolPass = False
                    
                if not strBrightnesValue in oBrightnessList: 
                    oBrightnessList.append(strBrightnesValue)
                    strParameterValue = strParameterValue + "," + str(sensorValue)
            else:
                if not ("ON" in strBrightnesValue.upper() or "OFF" in strBrightnesValue.upper()):
                    context.reporter.ReportEvent('Test Validation', "The Brightness values should be in multiples of 20", "FAIL")
            time.sleep(intTimeLapse + 2)
        
        #Update Text file
        oFileWriter = open(context.reporter.strCurrentTXTFolder+ "LUXvsTEMP.txt", 'a')
        oFileWriter.write(strParameterValue + "\n")
        oFileWriter.close()
        del oFileWriter
        
        intTCEndTime = time.monotonic()
        strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
        strTCDuration = utils.getDuration(strTCDuration)   
        intSeconds = float(strTCDuration.split(",")[1].strip().split(" ")[0])
        intMin = float(strTCDuration.split(",")[0].strip().split(" ")[0])
        intSeconds = intMin*60.0 + intSeconds
        
        if not boolInfiniteExec:
            if intSeconds > intMaxExecSeconds:
                return
            
@when(u'The ActiveLight is switched ON and OFF state and brightness of the light is varied to {Brightness} and validated {Duration} with timelapse of {Timelapse} second via telegesis')
def activeLightSpecificBrightnessValidation(context, Duration, Brightness, Timelapse):
    boolInfiniteExec = False
    if "INFIN" in Duration.upper():
        boolInfiniteExec = True
    else: 
        intMaxExecSeconds = int(Duration) * 60
    
    oColorTempList = {0:"00A5",
                                  20:"00C8",
                                  40:"00F0",
                                  50:"0104",
                                  60:"0118",
                                  80:"0140",
                                  100:"0172"}
    
    oColorTempList = {0:2700,
                                  20:3460,
                                  40:4220,
                                  50:4600,
                                  60:4980,
                                  80:5740,
                                  100:6500}
     
     
    oColorTempPercentageList = list(oColorTempList.keys())
    _,_,myNodeId = utils.discoverNodeIDbyCluster("0000")
    #Get Model
    _, _, model = AT.getAttribute(myNodeId, "01", "0000", "0005", 'server')
    print(model)
    intTCStartTime = time.monotonic()
    intCntr = 0
    oBrightnessList = []
    #Open Text file to write the light parameters
    oFileWriter = open(context.reporter.strCurrentTXTFolder+ "LUXvsTEMP.txt", 'w')
    oFileWriter.write("Iteration,ColorTemp,0_%,20_%,40_%,60_%,80_%,100_% \n")
    oFileWriter.close()
    del oFileWriter
    strParameterValue = ""
    intCntr = 0
    strParameterValue = str(intCntr)
    strBrightnesValue = Brightness
    intTimeLapse = int(Timelapse)
    if "TWBULB01" in model.upper():
            intTempCntr = intCntr % 5
            print(intTempCntr)
            myColourTemp = oColorTempList[oColorTempPercentageList[intTempCntr]]
            AT.colourTemperature(myNodeId, "01", 0, myColourTemp,0)
            context.reporter.ReportEvent('Test Validation', "Active light is set to Color Temperature : <B>" + str(myColourTemp) + "</B>", "Done")
            strParameterValue = strParameterValue + "," + str(myColourTemp)
            
            
            
            print(strBrightnesValue, strBrightnesValue, "\n")
            print("myNodeId", myNodeId)
            
            
            if "ON" in strBrightnesValue.upper():
                AT.onOff(myNodeId, "01", 0, 1)
                context.reporter.ReportEvent('Test Validation', "Active light is set to : <B>" + str(strBrightnesValue) + "</B>", "Done")
            elif "OFF" in strBrightnesValue.upper():
                AT.onOff(myNodeId, "01", 0, 0)
                context.reporter.ReportEvent('Test Validation', "Active light is set to : <B>" + str(strBrightnesValue) + "</B>", "Done")
            else:                
                strBrightnesValue = int(strBrightnesValue)                
                #hexBrightnesValue = '{:02x}'.format(int(strBrightnesValue*2.55))
                intTimeLapseRep = '{:04x}'.format(intTimeLapse)
                respState,respCode,respValue =  AT.moveToLevel(myNodeId, "01",0, int(strBrightnesValue), int(intTimeLapseRep))
                print(intCntr, respState,respCode,respValue)
                context.reporter.ReportEvent('Test Validation', "Active light Brightness is set to : <B>" + str(strBrightnesValue) + "</B>", "Done")  
    if "FWBULB01" in model.upper():
            intTempCntr = intCntr % 5
            print(intTempCntr)
            #myColourTemp = oColorTempList[oColorTempPercentageList[intTempCntr]]
            #AT.colourTemperature(myNodeId, "01", 0, myColourTemp,0)
            #context.reporter.ReportEvent('Test Validation', "Active light is set to Color Temperature : <B>" + str(myColourTemp) + "</B>", "Done")
            #strParameterValue = strParameterValue + "," + str(myColourTemp)
            
            
            
            print(strBrightnesValue, strBrightnesValue, "\n")
            print("myNodeId", myNodeId)
            
            
            if "ON" in strBrightnesValue.upper():
                AT.onOff(myNodeId, "01", 0, 1)
                context.reporter.ReportEvent('Test Validation', "Active light is set to : <B>" + str(strBrightnesValue) + "</B>", "Done")
            elif "OFF" in strBrightnesValue.upper():
                AT.onOff(myNodeId, "01", 0, 0)
                context.reporter.ReportEvent('Test Validation', "Active light is set to : <B>" + str(strBrightnesValue) + "</B>", "Done")
            else:                
                strBrightnesValue = int(strBrightnesValue)                
                #hexBrightnesValue = '{:02x}'.format(int(strBrightnesValue*2.55))
                intTimeLapseRep = '{:04x}'.format(intTimeLapse)
                respState,respCode,respValue =  AT.moveToLevel(myNodeId, "01",0, int(strBrightnesValue), int(intTimeLapseRep))
                print(intCntr, respState,respCode,respValue)
                context.reporter.ReportEvent('Test Validation', "Active light Brightness is set to : <B>" + str(strBrightnesValue) + "</B>", "Done")  
    while True:
        strParameterValue = ""
        intCntr = intCntr + 1
        strParameterValue = str(intCntr)
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Active Light Brightness validation Counter: ' + str(intCntr))   
            
        #Validate Lux
        time.sleep(5)
        if strBrightnesValue in lightSensorCalibration:
            intLowLimit = lightSensorCalibration[strBrightnesValue][0]
            intHighLimit = lightSensorCalibration[strBrightnesValue][1]
            sensorValue,_,_ = utils.get_lux_value()
            if intLowLimit < sensorValue and intHighLimit > sensorValue:
                context.reporter.ReportEvent('Test Validation', "The measured LUX value for Active light Brightness is: <B>" + str(sensorValue) + "</B>. Which is within the calibration limit: " + str(intLowLimit) + " - " + str(intHighLimit), "PASS")
            else: 
                context.reporter.ReportEvent('Test Validation', "The measured LUX value for Active light Brightness is: <B>" + str(sensorValue) + "</B>. Which is <B>NOT</B> the calibration limit: " + str(intLowLimit) + " - " + str(intHighLimit), "FAIL")
                boolPass = False
                
            if not strBrightnesValue in oBrightnessList: 
                oBrightnessList.append(strBrightnesValue)
                strParameterValue = strParameterValue + "," + str(sensorValue)
        else:
            if not ("ON" in strBrightnesValue.upper() or "OFF" in strBrightnesValue.upper()):
                context.reporter.ReportEvent('Test Validation', "The Brightness values should be in multiples of 20", "FAIL")
        time.sleep(intTimeLapse + 2)
        
        #Update Text file
        oFileWriter = open(context.reporter.strCurrentTXTFolder+ "LUXvsTEMP.txt", 'a')
        oFileWriter.write(strParameterValue + "\n")
        oFileWriter.close()
        del oFileWriter
        
        intTCEndTime = time.monotonic()
        strTCDuration = str((timedelta(seconds=intTCEndTime - intTCStartTime)).strftime('%H:%M:%S'))
        strTCDuration = utils.getDuration(strTCDuration)   
        intSeconds = float(strTCDuration.split(",")[1].strip().split(" ")[0])
        intMin = float(strTCDuration.split(",")[0].strip().split(" ")[0])
        intSeconds = intMin*60.0 + intSeconds
        
        if not boolInfiniteExec:
            if intSeconds > intMaxExecSeconds:
                return   

@when(u'The hue value of the bulb is changed and validated for the given hue value {Duration} via telegesis')
def RGBColorValidation(context,Duration):
    boolInfiniteExec = False
    print(Duration.upper()+"\n")
    if "INFIN" in Duration.upper():
        boolInfiniteExec = True
    else: 
        intMaxExecSeconds = int(Duration) * 60
    PORT = '/dev/tty.SLAB_USBtoUART'
    BAUD = 115200

    AT.debug = True

    AT.stopThread.clear()  
    # Start the serial port read/write threads and attribute listener thread
    AT.startSerialThreads(PORT, BAUD, printStatus=False, rxQ=True, listenerQ=True)
    intTCStartTime = time.monotonic()

    myEp = '01'
    sat = 'Fe'
    _,_,myNodeId = utils.discoverNodeIDbyCluster("0000")
    while True:
        for oRow in context.table:
            hexHue = oRow['HueValue']
            print(hexHue)
            moveToHueAndSat(myNodeId,myEp,hexHue,sat,myDuration='0000')
            time.sleep(int(oRow['TimeLapse']))
            #moveToHue(myNodeId,myEp,hexHue,myDuration='0000')
            #time.sleep(0.1)
        intTCEndTime = time.monotonic()
        strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
        strTCDuration = utils.getDuration(strTCDuration)   
        intSeconds = float(strTCDuration.split(",")[1].strip().split(" ")[0])
        intMin = float(strTCDuration.split(",")[0].strip().split(" ")[0])
        intSeconds = intMin*60.0 + intSeconds
        if not boolInfiniteExec:
                if intSeconds > intMaxExecSeconds:
                    return
            
def moveToHueAndSat(myNodeId,myEp,hue,sat,myDuration='0000'):
    
    sendMode=0
    myMsg='AT+CCMVTOHUS:{},{},{},{},{},{}'.format(myNodeId,myEp,sendMode,hue,sat,myDuration)
    #expectedResponses=['DFTREP:0EE1,01,0300,0A,00']
    expectedResponses=['DFTREP:{},{},{},(..)'.format(myNodeId,myEp,'0300')]
    respState,respCode,respValue=AT.sendCommand(myMsg, expectedResponses)
    return respState,respCode,respValue
