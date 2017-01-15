'''
Created on 22 May 2015

@author: ranganathan.veluswamy
'''

import json
import logging
import os
import platform
import time
import sys
import glob
import serial


sys.path.append("steps")
sys.path.append("steps/Definitions")
sys.path.append("steps/PageObjects")
sys.path.append("steps/Locators")
sys.path.append("steps/Function_Libraries")

from BB_ReusableFunctionModule import ReusableFunctionModule
import CC_platformAPI as pAPI
import FF_Platform_Utils as pUtils
import CC_thermostatModule as st
import DD_Page_AndroidApp as paygeAndroid
import DD_Page_WebApp as paygeWeb
import DD_Page_iOSApp as paygeiOS
from FF_Reporter import Reporter
import FF_alertmeApi as ALAPI
import FF_loggingConfig as config
import FF_threadedSerial as AT
import FF_utils as utils


BEHAVE_DEBUG_ON_ERROR = True

def setup_debug_on_error(userdata):
    global BEHAVE_DEBUG_ON_ERROR
    BEHAVE_DEBUG_ON_ERROR = True  #userdata.getbool("BEHAVE_DEBUG_ON_ERROR")

def before_all(context):
    setup_debug_on_error(context.config.userdata)
    if not context.config.log_capture:
        logging.basicConfig(level=logging.DEBUG)
    global reporter
    
    strEnvironmentFolderPAth = os.path.abspath(__file__ + "/../../../") + "/02_Manager_Tier/EnviromentFile/"
    strGlobVarFilePath = strEnvironmentFolderPAth + '/GlobalVar.json'    
    strJson = open(strGlobVarFilePath, mode='r')
    oJsonDict = json.loads(strJson.read())
    strJson.close()    
    context.oJsonDict = oJsonDict
    utils.oJsonDict = oJsonDict
    
    reporter = Reporter()  
    reporter.strOnError = 'Exit Test'  
    reporter.oDeviceVersionDict = getDeviceVersions()
    strExecSummaryHTMLFilePath = reporter.HTML_Execution_Summary_Initialize()
    context.reporter = reporter
    context.reporter.ActionStatus = True
    
    #Instantiate Reusable Function Module Class
    rFM = ReusableFunctionModule()
    context.rFM = rFM
    #Set Network Path
    if 'DARWIN' in platform.system().upper():
        context.networkBasePath = '/volumes/hardware/'
        context.PORT = '/dev/tty.SLAB_USBtoUART'
    elif 'LINUX' in platform.system().upper():        
        context.networkBasePath = '/home/pi/hardware/'
        context.PORT = '/dev/ttyUSB0'
    elif sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
        result = []
        FinalPort = ""
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
                FinalPort = port
            except (OSError, serial.SerialException):
                pass
        print(result)
        context.networkBasePath = "\\\\nas1\Hardware\\"
        context.PORT = FinalPort
    else:
        context.networkBasePath = ""
        context.PORT = config.PORT
        
        print('I should not be hereeeee \n')
    
    strAPIValidationType = utils.getAttribute('common', 'apiValidationType')
    if 'PLATFORM' in strAPIValidationType.upper(): 
        
        strCurrentEnvironment = utils.getAttribute('common', 'currentEnvironment')
        oPlatformAPIClass = pAPI.platformAPIClass(strCurrentEnvironment)
        context.oThermostatClass = oPlatformAPIClass
        context.APIType = 'PLATFORM'
        context.reporter.APIType = 'PLATFORM'
        
        context.iOSDriver = None
        context.AndroidDriver = None
        context.WebDriver = None
        #reporter.strTestResHTMLFilePath = strExecSummaryHTMLFilePath
        strMainClient = utils.getAttribute('common', 'mainClient')
        #login_client(context, strMainClient)
        print(utils.getAttribute('common', 'secondClient').upper())
        #if not context.reporter.ActionStatus: exit()
        if 'Y' in utils.getAttribute('common', 'secondClientValidateFlag').upper():
            strSecondaryClient = utils.getAttribute('common', 'secondClient')
            login_client(context, strSecondaryClient)
            reporter.strTestResHTMLFilePath = ""
            if not context.reporter.ActionStatus: utils.setAttribute('common', 'secondClientValidateFlag', 'No')
        
        context.oThermostatClass.iOSDriver = context.iOSDriver
        context.oThermostatClass.AndroidDriver = context.AndroidDriver
        context.oThermostatClass.WebDriver = context.WebDriver
        context.oThermostatClass.reporter = context.reporter
        context.reporter.update_result_json_kit_details(pUtils.getNodeAndDeviceVersionID())
        
    else:        
        # Reset the stop threads flag
        AT.stopThread.clear()  
        # Start the serial port read/write threads and attribute listener thread
        AT.startSerialThreads(context.PORT, config.BAUD, printStatus=False, rxQ=True, listenerQ=False)
        
        ''' AT.startAttributeListener(printStatus=False)
        context.nodes = getNodes()
        print(context.nodes, 'context.nodes')
        reporter.strNodeID = context.nodes['BM']
        config.node1 = context.nodes['BM']
        AT.getInitialData(reporter.strNodeID, "05", fastPoll=True, printStatus=False)'''
        #Instantiate ThermostatEndpoint class
        oThermostatClass = st.thermostatClass(context.reporter.strNodeID)
        context.oThermostatClass = oThermostatClass
        
        context.APIType  = 'ZIGBEE'
        context.reporter.APIType = 'ZIGBEE'
  
#Login to the main & secondary Clients before the test could start  
def login_client(context, strClient):
    strUserName = utils.getAttribute('common', 'userName')
    strPassword = utils.getAttribute('common', 'password')
    if 'IOS' in strClient.upper():
        strAppPath = utils.getAttribute('iOS', 'appFileName')
        strDeviceName = utils.getAttribute('iOS', 'deviceName')
        oBasePage = paygeiOS.BasePage(None, reporter)
        context.iOSDriver  = oBasePage.setup_ios_driver(strDeviceName, strAppPath)
        oHomePage = paygeiOS.HomePage(context.iOSDriver, reporter)
        oHomePage.logout_hive_app()
        oLoginPage = paygeiOS.LoginPage(context.iOSDriver, reporter)
        oLoginPage.login_hive_app(strUserName, strPassword)
        
    elif 'ANDROID' in strClient.upper():
        oBasePage = paygeAndroid.BasePage(None, reporter)
        strAppPath = utils.getAttribute('android', 'appFileName')
        strAndroidPlatformVersion = utils.getAttribute('android', 'platformVersion')
        strDeviceName = utils.getAttribute('android', 'deviceName')
        context.AndroidDriver  = oBasePage.setup_android_driver(strAndroidPlatformVersion, strDeviceName, strAppPath)
        oLoginPage = paygeAndroid.LoginPage(context.AndroidDriver, reporter)
        oLoginPage.login_hive_app(strUserName, strPassword)
        print('inside android')
    
    elif 'WEB' in strClient.upper():
        strURL = utils.getAttribute('web', 'loginURL')
        strBrowserName = utils.getAttribute('web', 'browserName')
        oBasePage = paygeWeb.BasePage(None, reporter)
        context.WebDriver = oBasePage.setup_Selenium_driver(strBrowserName, strURL)
        oLoginPage = paygeWeb.LoginPage(context.WebDriver, reporter)
        oLoginPage.login_hive_app(strUserName, strPassword)
        
        
def before_scenario(context, scenario):
    context.reporter.ActionStatus = True
    print("************************")
    #print("Before scenario " + scenario.name)
    #Setting Current scenario name
    if scenario.name.find("-- @") > 0: reporter.strCurrentScenario =scenario.name.split("-- @")[0].strip()
    else: reporter.strCurrentScenario =scenario.name
    
    if reporter.strPreviousScenario != "":        
        if reporter.strPreviousScenario != reporter.strCurrentScenario:
            reporter.HTML_TestCase_Footer()
            #reporter.HTML_Execution_Summary_TCAddLink()
            reporter.strPreviousScenario = reporter.strCurrentScenario
    else:
        reporter.strPreviousScenario = reporter.strCurrentScenario
    
    #Getting the iteration number from the scenario description
    strCurrentScenarioDesc = ""
    cntr = '1'
    if scenario.keyword == 'Scenario Outline' :
        cntr = scenario.name.split("-- @")[1].split(" ")[0].split(".")[1]    
        strCurrentScenarioDesc = scenario.name.split("-- @")[0]
        #print ("Iteration : " + cntr)
    else: strCurrentScenarioDesc = scenario.name
    
    #Get Global Variables
    context.intCheckDuration = int(utils.getAttribute('validation', 'duration'))
    context.intCheckIntervalTime = int(utils.getAttribute('validation', 'checkInterval'))
    intTmeUnits = utils.getAttribute('validation', 'timeUnits')
    if intTmeUnits.upper().find('MIN') >= 0: 
        context.intCheckDuration = context.intCheckDuration * 60
        context.intCheckIntervalTime = context.intCheckIntervalTime * 60
    context.APIType = utils.getAttribute('common', 'apiValidationType')
    context.mainClient = utils.getAttribute('common', 'mainClient')
    context.client1 = utils.getAttribute('clientList', 'client1')
    context.client2 = utils.getAttribute('clientList', 'client2')
    context.client3 = utils.getAttribute('clientList', 'client3')
    context.client4 = utils.getAttribute('clientList', 'client4')
    context.clientDict = {'CLIENT' : context.mainClient,
                                     'CLIENT1' : context.client1,
                                     'CLIENT2' : context.client2,
                                     'CLIENT3' : context.client3,
                                     'CLIENT4' : context.client4
                                    }
 
    #Updating the Header values for the summary report prior to the first iteration  
    if cntr == '1':
        reporter.strCurrentExecutionTerminal = "Mac"    
        reporter.strCurrentTestIterationList = '1'
        if scenario.name.find('_') > 0:
            reporter.strCurrentScenarioID = scenario.name.split("_")[0]
        else: reporter.strCurrentScenarioID = scenario.name
        
        #Getting the current tag for the scenario
        strTagName = ""
        for strTag in scenario.tags:
            strTagName = strTagName + strTag + ', ' 
            strTagName = strTagName[:len(strTagName) - 2]
        #Updating Tag, FeatureFile name & Scenario description to the summary report
        reporter.strCurrentTag = strTagName        
        reporter.strCurrentFeatureFileName = scenario.feature.filename.split('.')[0]
        reporter.strCurrentScenarioDesc = strCurrentScenarioDesc
        
        #Update Result Json
        context.reporter.create_scenario_result_json()
    
        #Initializing Test scenario reporting, with first iteration
        reporter.HTML_TestCase_Initialize(reporter.strCurrentScenarioID )
        reporter.HTML_Execution_Summary_TCAddLink()
        reporter.HTML_TC_Iteration_Initialize(1)
        
        context.oScenarioClientsDict = reportScenarioDetails(scenario, context.clientDict)
    else:
        #Initializing the Scenario Iteration from second onwards
        reporter.HTML_TC_Iteration_Initialize(cntr)        
        context.oScenarioClientsDict = reportScenarioDetails(scenario, context.clientDict)
    context.scenario = scenario
    
     
def reportScenarioDetails(scenario, clientDict):
    oBoldKeywords = ['BOOST', 'Always', 'OFF', 'ON', 'MANUAL', 'Mode', 'change', 'Hot',  'Water']
    reporter.HTML_TC_BusFlowKeyword_Initialize('Scenario Details')
    #get scenario name
    if scenario.keyword == 'Scenario Outline' :
        strCurrentScenarioDesc = scenario.name.split("-- @")[0]
    else: strCurrentScenarioDesc = scenario.name
    
    #Report feature & Scenario details
    strFeature = '<B>Feature: </B>' + scenario.feature.name
    strLog = strFeature + "$~" + '<B>Scenario: </B>' + strCurrentScenarioDesc
    reporter.ReportEvent("Test", strLog, "DONE", 'LEFT')
    
    oScenarioClientsDict = {}
    #Report Steps
    for  oStep in scenario.steps:        
        strStepName = oStep.name        
        if oStep.keyword.upper() == 'GIVEN': 
            for oStepWord in strStepName.split(' '):
                if oStepWord.upper() == 'API': strStepName = strStepName.replace(oStepWord, '<B>' + utils.getAttribute('common', 'apiValidationType') + '</B>')
                if oStepWord in oBoldKeywords: strStepName = strStepName.replace(oStepWord, '<B>' + oStepWord + '</B>')
        else: 
            for oStepWord in strStepName.split(' '):
                if oStepWord in oBoldKeywords: strStepName = strStepName.replace(oStepWord, '<B>' + oStepWord + '</B>')
                if oStepWord.upper() in clientDict.keys(): 
                    strStepName = strStepName.replace(oStepWord, '<B>' + clientDict[oStepWord.upper()] + '</B>')
                    if not clientDict[oStepWord.upper()] in oScenarioClientsDict.keys(): oScenarioClientsDict[clientDict[oStepWord.upper()]] = clientDict[oStepWord.upper()].split(' ')[0].upper()
        
        strLog =  "<B>" + oStep.keyword + ' : </B>' +  strStepName
        reporter.ReportEvent("", strLog, "", 'LEFT', False)
        if oStep.table is not None:
            strStepTableLog  = ""
            for oHead in oStep.table.headings:
                strStepTableLog = strStepTableLog + oHead + '$$'
            strStepTableLog = strStepTableLog[:len(strStepTableLog) - 2] + '@@@'
            for oRow in oStep.table.rows:
                for oCell in oRow.cells:
                    strStepTableLog = strStepTableLog + oCell + '$$'
                strStepTableLog = strStepTableLog[:len(strStepTableLog) - 2]
                strStepTableLog = strStepTableLog + '$~'
            strStepTableLog = strStepTableLog[:len(strStepTableLog) - 2]        
            reporter.ReportEvent("", strStepTableLog, "", 'LEFT', False)
    return oScenarioClientsDict

def getNodes():
    BMID = utils.discoverNodeIDbyCluster('0201')[2]
    return {'BM':BMID}
    time.sleep(2)
    #SPID = utils.discoverNodeIDbyCluster('0006')[2]
    time.sleep(2)
    THID = ""
    NTAble = utils.getNtable('ff')[2]
    boolTHfound = False
    for oRow in NTAble:
        if 'RFD' in oRow:
            THID = oRow.split('|')[3].strip()
            boolTHfound = True
    if not boolTHfound:
        NTAble = utils.getNtable(BMID)[2]
        for oRow in NTAble:
            if 'RFD' in oRow:
                THID = oRow.split('|')[3].strip()
                boolTHfound = True
    '''if not boolTHfound:
        NTAble = utils.getNtable(SPID)[2]
        for oRow in NTAble:
            if 'RFD' in oRow:
                THID = oRow.split('|')[3].strip()
                boolTHfound = True'''
            
    return {'BM':BMID, 'TH':THID}#, 'SP':SPID}
    
    
def before_step(context, step):
    context.boolScenarioExecStatus = True
    context.strStepFailReason = ""
    #print(step.name)
    #input("Enter")

def after_step(context, step):
    if BEHAVE_DEBUG_ON_ERROR and step.status == "failed":
        # -- ENTER DEBUGGER: Zoom in on failure location.
        # NOTE: Use IPython debugger, same for pdb (basic python debugger).
        import ipdb
        ipdb.post_mortem(step.exc_traceback)
        
    if not context.boolScenarioExecStatus:
        reporter.HTML_TC_BusFlowKeyword_Initialize('Error')
        reporter.ReportEvent('Test Validation', context.strStepFailReason, 'FAIL')
        print('Step Failed!\n Step: ' +  step.keyword + ': ' + step.name)
        print(context.strStepFailReason)
        context.scenario.skip()
    if not context.reporter.ActionStatus: 
        print('context.reporter.ActionStatus', context.reporter.ActionStatus)
        context.scenario.skip()

def after_scenario(context, scenario):
    reporter.HTML_TC_Iteration_Footer()
    reporter.update_scenario_result_json("Completed")
    reporter.intScenarioCounter = reporter.intScenarioCounter + 1
    #print(context.oSchedDict)
    
  
def after_all(context):
    reporter.HTML_TestCase_Footer()
    #reporter.HTML_Execution_Summary_TCAddLink()
    reporter.HTML_Execution_Summary_Footer()
    if 'PLATFORM' in context.APIType.upper():
        context.rFM.quitDrivers(context)
    else:
        try: 
            AT.stopThreads()
        except: pass
    
def getDeviceVersions():
    oDeviceVersionDict = {}
    strModel = "'"
    if 'PLATFORM' in utils.getAttribute('common', 'apiValidationType').upper():
        serverName = utils.getAttribute('common', 'currentEnvironment')
        strPlatformVersion = ALAPI.createCredentials(serverName)
        session  = ALAPI.sessionObject()
        if strPlatformVersion == 'V6':
            resp = ALAPI.getNodesV6(session)
            for oNode in resp['nodes']:
                if not 'supportsHotWater'  in oNode['attributes']:
                    if 'hardwareVersion' in oNode['attributes']: 
                        intHardwareVersion = oNode['attributes']['hardwareVersion']['reportedValue']
                        intSoftwareVersion = oNode['attributes']['softwareVersion']['reportedValue']
                        if intHardwareVersion == '00': 
                            if "reportedValue" in oNode['attributes']['model']:
                                strModel =  oNode['attributes']['model']['reportedValue']
                                oDeviceVersionDict['Thermostat'] = strModel + '$$' + intSoftwareVersion
                        elif intHardwareVersion == '01': 
                            if 'reportedValue' in oNode['attributes']['model']: strModel =  oNode['attributes']['model']['reportedValue']
                            oDeviceVersionDict['Boiler Module'] = strModel + '$$' + intSoftwareVersion
                        elif 'NANO' in  intHardwareVersion:
                            oDeviceVersionDict['HUB'] = intHardwareVersion + '$$' + intSoftwareVersion
            ALAPI.deleteSessionV6(session)
            
    return oDeviceVersionDict