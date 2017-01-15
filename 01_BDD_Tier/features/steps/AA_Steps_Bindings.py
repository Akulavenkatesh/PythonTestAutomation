'''
Created on 28 Sep 2015

@author: ranganathan.veluswamy
'''
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
#from SP_StandaloneModeTestBM import myNodeId


striOSAppiumConnectionString = "/Applications/Appium.app/Contents/Resources/node/bin/node \
                                                /Applications/Appium.app/Contents/Resources/node_modules/appium/bin/appium.js \
                                                --address 127.0.0.1 --command-timeout \"7200\" --debug-log-spacing \
                                                --no-reset --udid \"02d0e686d941f6d6486924a5f32ca3ee051b0d02\"\
                                                 --native-instruments-lib --log-level \"error\""
                                                 
striOSAppiumConnectionString = "/Applications/Appium.app/Contents/Resources/node/bin/node /Applications/Appium.app/Contents/Resources/node_modules/appium/bin/appium.js --address 127.0.0.1 --command-timeout  \"7200\"  --debug-log-spacing --no-reset --native-instruments-lib  -p 4723"
expectedNodeDescResp = ['NodeDesc:FD90,00',
'Type:FFD',
'ComplexDesc:No',
'UserDesc:No',
'APSFlags:00',
'FreqBand:40',
'MacCap:8E',
'ManufCode:1039',
'MaxBufSize:52',
'MaxInSize:00FF',
'SrvMask:0000',
'MaxOutSize:00FF',
'DescCap:00']

@given('The Hive product with the existing Bindings {isCleared} on the {Node}')
def bindingInitialize(context, isCleared, Node):
    Node = Node.upper().strip()
    validateNode(context, Node)
    
    Nodes = context.nodes
    strNodeID = Nodes[Node]
    
    if 'TH' in Node: 
        AT.getInitialData(Nodes['TH'], fastPoll=True, printStatus=False)
        
    utils.getAllClustersAttributes(strNodeID, Node)
    
    if not 'NOT' in isCleared.upper():
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Initialize Bindings')   
        strBtableHeader = 'No.' +"$$" + 'SrcAddr' +"$$" + 'SrcEP' +"$$" + 'ClusterID' +"$$" + 'DstAddr' +"$$" + 'DstEP' +"$$" +  'Status'  + '@@@'
        strBtableBody = ""
        intIndex = 0
        
        oBindTable = utils.getBind(strNodeID)
        print('got binding table')
        for oRow in range(3, len(oBindTable)):
            arrCell = oBindTable[oRow].split("|")
            strBtableBody = strBtableBody + str(intIndex) + "." +"$$" + utils.setUnBind(strNodeID, arrCell[2].strip(), arrCell[3].strip()) + "$~"
            intIndex = intIndex + 1
        if not strBtableBody=="":
            strBtableBody = strBtableBody[:len(strBtableBody) - 2]
            strBtable = strBtableHeader + strBtableBody
            context.reporter.ReportEvent('Test Validation', 'The below Binding table is Cleared for ' + Node + ' : ' + strNodeID, "PASS")
            context.reporter.ReportEvent("Test Validation", strBtable, "DONE")
        else:
            context.reporter.ReportEvent('Test Validation', 'There is NO existing Bindings to clear for ' + Node + ' : ' + strNodeID, "PASS")
    

def validateNode(context, Node):
    if Node.upper().strip() not in ['BM', 'SP', 'TH']:
        context.boolScenarioExecStatus = False
        context.strStepFailReason = 'Invalid Node passed in the Test scenario: ' + Node
        return False
    
    if Node.upper() not in utils.getNodeList():
        context.boolScenarioExecStatus = False
        context.strStepFailReason = 'Device Node either not paired or not loaded into the nodes_clusters_attributes.json: ' + Node
        return False
    
@when('the Bindings are set for the below Clusters on the {Node}')
def setBindings(context, Node):
    validateNode(context, Node)
    strNodeID = context.nodes[Node]
    
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Set Bindings')
    context.reporter.ReportEvent('Test Validation', 'The below Binding table is set:', "PASS")
    strBtableHeader = 'No.' +"$$" + 'SrcAddr' +"$$" + 'SrcEP' +"$$" + 'ClusterID' +"$$" + 'DstAddr' +"$$" + 'DstEP' +"$$" +  'Status'  + '@@@'
    context.reporter.ReportEvent("Test Validation", strBtableHeader, "DONE")
    intIndex = 0
    oExpBindList = {}
    for oRow in context.table:
        strBtableBody = ""
        strEndPoint = oRow['End Point']
        hexClusterID = oRow['Cluster ID']
        print(strEndPoint, hexClusterID)   
        statusCode, strBody = utils.setBind(strNodeID, strEndPoint, hexClusterID)
        if statusCode.upper().strip():
            status = statusCode.upper().strip() + ' - ' + utils.statusCodeValue[statusCode.upper().strip()]
            
        oExpBindList[intIndex] = strBody
        strBtableBody =strBtableBody + str(intIndex) + "." +"$$" + strBody + "$$" + status + "$~"
        intIndex = intIndex + 1
    strBtableBody = strBtableBody[:len(strBtableBody) - 2]
    strBtable = strBtableHeader + strBtableBody
    context.reporter.ReportEvent('Test Validation', 'The below Binding table is set:', "PASS")
    context.reporter.ReportEvent("Test Validation", strBtable, "DONE")
    context.oExpBindList = oExpBindList

def setBindingsClusters(context, myNodeId, arrBindingClusters, endPoint):
    strNodeID = myNodeId
    
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Set Bindings')
    #context.reporter.ReportEvent('Test Validation', 'The below Binding table is set:', "PASS")
    strBtableHeader = 'No.' +"$$" + 'SrcAddr' +"$$" + 'SrcEP' +"$$" + 'ClusterID' +"$$" + 'DstAddr' +"$$" + 'DstEP' +"$$" +  'Status'  + '@@@'
    #context.reporter.ReportEvent("Test Validation", strBtableHeader, "DONE")
    intIndex = 0
    oExpBindList = {}
    strBtableBody = ""
    for oClusterId in arrBindingClusters:
        
        strEndPoint = endPoint
        hexClusterID = oClusterId
        print(strEndPoint, hexClusterID + "\n")   
        statusCode, strBody = utils.setBind(strNodeID, strEndPoint, hexClusterID)
        if statusCode.upper().strip():
            status = statusCode.upper().strip() + ' - ' + utils.statusCodeValue[statusCode.upper().strip()]
            
        oExpBindList[intIndex] = strBody
        print("strBody =========================="+ strBody + "\n")
        strBtableBody =strBtableBody + str(intIndex) + "." +"$$" + strBody + "$$" + status + "$~"
        intIndex = intIndex + 1
    strBtableBody = strBtableBody[:len(strBtableBody) - 2]
    strBtable = strBtableHeader + strBtableBody
    context.reporter.ReportEvent('Test Validation', 'The below Binding table is set:', "PASS")
    context.reporter.ReportEvent("Test Validation", strBtable, "DONE")
    context.oExpBindList = oExpBindList
    utils.setAttribute('common', 'atZigbeeNode', context.nodeId)
    
def setUnBindingsClusters(context, myNodeId, arrBindingClusters, endPoint):
    strNodeID = myNodeId
    
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Set Bindings')
    #context.reporter.ReportEvent('Test Validation', 'The below Binding table is set:', "PASS")
    strBtableHeader = 'No.' +"$$" + 'SrcAddr' +"$$" + 'SrcEP' +"$$" + 'ClusterID' +"$$" + 'DstAddr' +"$$" + 'DstEP' +"$$" +  'Status'  + '@@@'
    #context.reporter.ReportEvent("Test Validation", strBtableHeader, "DONE")
    intIndex = 0
    oExpBindList = {}
    strBtableBody = ""
    for oClusterId in arrBindingClusters:
        
        strEndPoint = endPoint
        hexClusterID = oClusterId
        print(strEndPoint +" - "+ hexClusterID + "\n")   
        statusCode, strBody = utils.setUnBind(strNodeID, strEndPoint, hexClusterID, True)
        if statusCode.upper().strip():
            if statusCode == "PASS":
                context.reporter.ReportEvent("Test Validation", "Unbind cluster "+oClusterId+" is successfull", "Pass")
            else:
                context.reporter.ReportEvent("Test Validation", "Unbind cluster "+oClusterId+" is successfull", "Fail")
            
        oExpBindList[intIndex] = strBody
        strBtableBody =strBtableBody + str(intIndex) + "." +"$$" + strBody + "$$" + statusCode + "$~"
        intIndex = intIndex + 1
    strBtableBody = strBtableBody[:len(strBtableBody) - 2]
    strBtable = strBtableHeader + strBtableBody
    context.reporter.ReportEvent('Test Validation', 'The below Binding table is unset:', "PASS")
    context.reporter.ReportEvent("Test Validation", strBtable, "DONE")
    utils.setAttribute('common', 'atZigbeeNode', context.nodeId)
    context.oExpBindList = oExpBindList
    
@then('validate if the Bindings are set correctly')
def validateBindings(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Get the current Bindings')  
    strBMModeID = utils.getAttribute('common', 'atZigbeeNode')
    oBindTable = utils.getBind(strBMModeID)
    oBindTable.remove(oBindTable[0])
    oBindTable.remove(oBindTable[0])
    strBtableHeader = oBindTable[0].replace("|", "$$")
    strBtableBody = ""
    oActBindList = []
    strBtableheader = oBindTable[0]
    for oRow in range(1, len(oBindTable)):
        strBody = oBindTable[oRow].replace("|", "$$") 
        strBtableBody = strBtableBody + strBody + "$~"
        oActBindList.append(strBody[strBody.find("$$") + 2:].replace(" ", ""))
        print("Actual Body ~~~~~~~~~~~~~~~~~~~~"+strBody[strBody.find("$$") + 2:].replace(" ", "")+"\n")
    strBtableBody = strBtableBody[:len(strBtableBody) - 2]
    
    strBtable = strBtableHeader + "@@@" + strBtableBody
    context.reporter.ReportEvent('Test Validation', 'The Current Binding Table:', "PASS")
    context.reporter.ReportEvent("Test Validation", strBtable, "DONE")
    boolBindSet = True
    oFailedBindList = []
    intCounter = 0
    for oBind in context.oExpBindList:
        print(str(oBind) + str(oBind in oActBindList) + "************** \n")
        if not oBind in oActBindList: 
            if (context.oExpBindList[intCounter] not in oActBindList):
                boolBindSet = False
                oFailedBindList.append(oBind)
            else:
                print(context.oExpBindList[intCounter] +"&&&&&&&----Pass-----&&&&&& \n")
        intCounter = intCounter + 1
    if not boolBindSet:
        intIndex = 0
        strBtableBody = ""
        strBtableheader = strBtableheader.replace("|", "$$") + "@@@"
        for oBind in oFailedBindList:
            strBtableBody =strBtableBody + str(intIndex) + "." +"$$" + str(oBind) + "$~"
            intIndex = intIndex + 1
        strBtableBody = strBtableBody[:len(strBtableBody) - 2]
        strBtable = strBtableHeader + "@@@" + strBtableBody
        context.reporter.ReportEvent('Test Validation', 'The below Bindings are not set:', "FAIL")
        context.reporter.ReportEvent("Test Validation", strBtable, "FAIL")
    else:
        context.reporter.ReportEvent('Test Validation', 'All the Expected Bindings are set successfully:', "PASS")
        

@when(u'The the nodedesc AT command is passed the return message is validated infinitely')
def validateNodeDescMessage(context):
    
    intIterCntr = 1
    while True:
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('Node Desc Message validation Counter: ' + str(intIterCntr))
        print('Node Desc Message validation Counter: ' + str(intIterCntr))
        intIterCntr = intIterCntr + 1
        #nodeID =context.nodes['BM']
        _,_,nodeID = utils.discoverNodeIDbyCluster("0000")
        _,_, resp =utils.get_device_constants(nodeID)
        resp = resp.split("ACK")[0]
        actualNodeDescResp = resp.split("$$")
        
        intMaxRow = max(len(expectedNodeDescResp), len(actualNodeDescResp))
        strHeader = 'Expected Node Desc Response   $$  Actual Node Desc Response   @@@'
        strRow = ""
        boolStatus = 'PASS'
        for intCntr in range(intMaxRow):
            strExpVal = ""
            strActVal = ""
            if intCntr < len(expectedNodeDescResp): strExpVal = expectedNodeDescResp[intCntr]
            if intCntr < len(actualNodeDescResp): strActVal = actualNodeDescResp[intCntr]
            
            if str(strExpVal) == str(strActVal):
                strActVal = '$$' + strActVal
            else:            
                strActVal = '$$||' + strActVal
                boolStatus = 'FAIL'
            
            strRow = strRow + '$~'  + strExpVal + strActVal    
        
        context.reporter.ReportEvent('Test Validation', strHeader + strRow , boolStatus, 'Center')
        print(strHeader+ strRow)
        time.sleep(20)


@when(u'The the app is unstalled and installed with latest version then the 32C temperature spike is verified')
def instaliOSAPP(context):
    
    intIterCntr = 1
    while True:
        context.reporter.HTML_TC_BusFlowKeyword_Initialize('App Installation Verification counter: ' + str(intIterCntr))        
        print('App Installation Verification counter: ' + str(intIterCntr))
        intIterCntr = intIterCntr + 1
        
        
        strNewAppFilePath = os.path.abspath(__file__ + "/../../../../") + "/02_Manager_Tier/EnviromentFile/Apps/iOS/isopBeta/Hive_new.ipa"
        strOldAppFilePath = os.path.abspath(__file__ + "/../../../../") + "/02_Manager_Tier/EnviromentFile/Apps/iOS/isopBeta/Hive_old.ipa"
        '''print(striOSAppiumConnectionString)
        subprocess.call('killall node', shell=True)               
        subprocess.Popen(striOSAppiumConnectionString, shell=True)'''
        
        for strAppPath in [strOldAppFilePath, strNewAppFilePath]:
            print('Uninstalling the APP')
            context.reporter.ReportEvent('Test Validation', 'Uninstalling the APP', "PASS")
            strCmd = "ideviceinstaller -U uk.co.britishgas.hive"
            getShellCommandOutput(strCmd, 'Uninstall APP', boolPrintOutput = True)
            time.sleep(5)
            print('Installing the APP')
            context.reporter.ReportEvent('Test Validation', 'Installing the APP', "PASS")
            strCmd = "ideviceinstaller -i " + strAppPath
            getShellCommandOutput(strCmd, 'Install APP', boolPrintOutput = True)
            
            
            context.reporter.ReportEvent('Test Validation', 'Launching the APP', "PASS")
            strDeviceName = utils.getAttribute('iOS', 'deviceName')
            oBasePage = paygeiOS.BasePage(None, context.reporter)
            iOSDriver  = oBasePage.setup_ios_driver(strDeviceName, strAppPath)
            oHomePage = paygeiOS.HomePage(iOSDriver, context.reporter)
            time.sleep(5)
            context.reporter.ReportEvent('Test Validation', 'Swipe the APP to go to Heating Control Page', "PASS")
            iOSDriver.swipe(50, 500, 300, 500, 500)
            time.sleep(5)
            fltCurrentTargTemp = 0.0
            try:
                oScrolElement = iOSDriver.find_element(*HeatingControlPageLocators.TARGET_TEMPERATURE_SCROLL)
                oScrolElementVAlue = oScrolElement.get_attribute('value')
                if 'point' in oScrolElementVAlue: fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[0] + '.' + oScrolElementVAlue.split(' ')[2])
                else: fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[0])
            except:
                context.reporter.ReportEvent('Test Validation','IOS App : NoSuchElementException: in navigate_to_change_password_screen\n {0}'.format(traceback.format_exc().replace('File', '$~File')), "FAIL")
            
            fltAPITargetTemp = 0.0
            ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
            session  = ALAPI.sessionObject()
            resp = ALAPI.getNodesV6(session)
            for oNode in resp['nodes']:
                if 'supportsHotWater'  in oNode['attributes']:
                    if 'stateHeatingRelay' in oNode['attributes']:
                        oAttributeList = oNode['attributes']    
                        fltAPITargetTemp = float('{:.1f}'.format(oAttributeList['targetHeatTemperature']['reportedValue']))
                        if fltAPITargetTemp ==1.0: fltAPITargetTemp = 7.0
            ALAPI.deleteSessionV6(session)
            
            if fltAPITargetTemp == 32.0 or fltAPITargetTemp != fltCurrentTargTemp:
                context.reporter.ReportEvent('Test Validation', 'App Display Target Temperature: ' + str(fltCurrentTargTemp) + '\nReported API Target Temperature: ' + str(fltAPITargetTemp), "FAIL", driver = iOSDriver)
            else:
                context.reporter.ReportEvent('Test Validation', 'App Display Target Temperature: ' + str(fltCurrentTargTemp) + '\nReported API Target Temperature: ' + str(fltAPITargetTemp), "PASS", driver = iOSDriver)
            
            iOSDriver.quit()
        
        
        
        '''
        _,_, resp =utils.get_device_constants(context.nodes['BM'])
        resp = resp.split("ACK")[0]
        actualNodeDescResp = resp.split("$$")
        
        intMaxRow = max(len(expectedNodeDescResp), len(actualNodeDescResp))
        strHeader = 'Expected Node Desc Response   $$  Actual Node Desc Response   @@@'
        strRow = ""
        boolStatus = 'PASS'
        for intCntr in range(intMaxRow):
            strExpVal = ""
            strActVal = ""
            if intCntr < len(expectedNodeDescResp): strExpVal = expectedNodeDescResp[intCntr]
            if intCntr < len(actualNodeDescResp): strActVal = actualNodeDescResp[intCntr]
            
            if str(strExpVal) == str(strActVal):
                strActVal = '$$' + strActVal
            else:            
                strActVal = '$$||' + strActVal 
                boolStatus = 'FAIL'
            
            strRow = strRow + '$~'  + strExpVal + strActVal    
        
        context.reporter.ReportEvent('Test Validation', strHeader + strRow , boolStatus, 'Center')
        print(strHeader+ strRow)
        time.sleep(20)'''

#Get Shell command output
def getShellCommandOutput(strCmd, strRpiID, boolPrintOutput = False):    
    oProcess = subprocess.Popen(strCmd, stdout=subprocess.PIPE, shell=True)
    outputList = []
    while True:
        output = oProcess.stdout.readline()
        if oProcess.poll() is not None:
            break
        if output:
            if boolPrintOutput: print(strRpiID, output)
            outputList.append(str(output))
        else:
            break
    return outputList

#Active Light 

@then(u'the values of the reportable attributes should be the {strValue} value')
def verifyAttributeValues(context,strValue):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Read attribute reports')
    if strValue == "default":
        oBSDumpJson = context.BaseDumpJson
        oTestDumpJson = context.TestDumpJson
        utils.validateDefaultReporting(context,context.reporter,oBSDumpJson,oTestDumpJson)
    elif strValue == "set":
        minRep = context.minAttrRep
        maxRep = context.maxAttrRep
        intCounter = 0
        myClustId = ""
        myAttrId = ""
        myNodeId = context.nodeId
        changeRep = ""
        myEp = context.ep
        for item in context.arrRepAttributeAndClusterId:
            for j in item:
                print(myClustId +"-----"+ myAttrId)
                if intCounter == 0:
                    myClustId = j
                elif intCounter == 1:
                    myAttrId = j
                intCounter = intCounter + 1
            print(myClustId +"-----"+ myAttrId)
            respState,respCode,resp = AT.getAttributeReporting(myNodeId, myEp, myClustId, 'server', myAttrId)
            print("Resp = "+ resp + "\n")
            
            if '{0},{1}'.format(minRep,maxRep) in resp:
                context.reporter.ReportEvent("Test Validation","The attribute reporting is set correctly as "+ resp,"Pass")
            else:
                context.reporter.ReportEvent("Test Validation","The attribute reporting is set incorrectly as "+ resp,"Fail")
            
            intCounter = 0
    
@when(u'the binding table on the device is verified via telegesis stick')
def verifyBindindTable(context):
    myNodeId = context.nodeId
    respState, _, respValue = utils.getBind(myNodeId, True)
    context.bindingValues = respValue


@then(u'the binding table on the device should have {strCount} entries')
def validateTheEntriesInBindingTalbe(context,strCount):
    verifyBindindTable(context)
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Check binding table for '+strCount+" entries")
    if "all" in strCount:
        arrBindingClusters = context.arrBindingClusters
        
    respValue = context.bindingValues
    if context.bindingValues != None:
        if len(respValue) == int(strCount):
            context.reporter.ReportEvent("Test Validation","The binding table has "+strCount+" entries","Pass")
        else:
            context.reporter.ReportEvent("Test Validation","The binding table does not have "+strCount+" entries but has "+ len(respValue) +" entries","Fail")
    else:
            context.reporter.ReportEvent("Test Validation","The binding table has "+strCount+" entries","Pass")

@when(u'the zigbee clusters on the device are bound to the telegesis stick')
def bindClusters(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Set the bindings')
    oBSDumpJson = context.BaseDumpJson
    oTestDumpJson = context.TestDumpJson
    arrBindingClusters,repAttributeAndClusterId = utils.getBindingClusters(context, oBSDumpJson, oTestDumpJson)
    context.arrRepAttributeAndClusterId = repAttributeAndClusterId
    context.arrBindingClusters = arrBindingClusters
    context.oExpBindList = arrBindingClusters
    myNodeId = context.nodeId
    myEp = context.ep
    setBindingsClusters(context,myNodeId , arrBindingClusters, myEp)

@when(u'the reportable attributes are set to report for the {strDuration} timeperiod')
def setReportableAttributes(context,strDuration):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Set attribure report configuration for the '+strDuration+" timeperiod")
    if strDuration == "given":
        minRep = "000F"
        maxRep = "000F"
    elif strDuration == "default":
        minRep = "FFFF"
        maxRep = "FFFF"
    myNodeId = context.nodeId
    myEp = context.ep
    myClustId = ""
    myAttrId = ""
    
    context.minAttrRep = minRep
    
    context.maxAttrRep = maxRep
    changeRep = ""
    intCounter = 0
    for item in context.arrRepAttributeAndClusterId:
        for j in item:
            print(myClustId +"-----"+ myAttrId)
            if intCounter == 0:
                myClustId = j
            elif intCounter == 1:
                myAttrId = j
            intCounter = intCounter + 1
        print(myClustId +"-----"+ myAttrId)
        utils.setAttributeReporting(context, myNodeId, myEp, myClustId, myAttrId, minRep, maxRep, changeRep)
        intCounter = 0
    

@then(u'the telegesis stick is mornitored and verified whether the attributes report for the {strDuration}')
def verifyTheAttributeReporting(context,strDuration):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Verify attribute reporting for the '+strDuration)
    if strDuration == "specified timeperiod":
        utils.validateReportingOfAttributes(context)
    elif strDuration == "change immediately":
        myNodeId = context.nodeId
        myEp = context.ep
        myClustId = "0006"
        myAttrId = "0000"
        myAttrType = "10"
        timeout = 15
        myMsgs = "REPORTATTR:"+myNodeId+","+myEp+","+myClustId+","+myAttrId+","+myAttrType
        utils.waitForMessage(myMsgs, timeout)
    elif strDuration == "default timeperiod":
        utils.validateDefaultReportingOfAttributes(context)
    
@when(u'the device state is changed to {strState}')
def onOffBulb(context,strState):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Change the device state to '+strState)
    myNodeId = context.nodeId
    myEp = context.ep
    utils.setOnOff(myNodeId,myEp, strState, True)
    context.reporter.ReportEvent("Test Validation","The devices is set to "+strState,"Done")

@when(u'the bindings are cleared on the device')
def clearBindingTable(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Clear the bindings')
    arrBindingClusters = context.arrBindingClusters
    myNodeId = context.nodeId
    myEp = context.ep
    setUnBindingsClusters(context, myNodeId, arrBindingClusters, myEp)


            
            
            
            
            
            
            