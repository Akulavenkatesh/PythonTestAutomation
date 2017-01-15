'''
Created on 19 May 2015

@author: ranganathan.veluswamy
'''

from datetime import datetime
from datetime import timedelta
import json
import os
import re, uuid
import shutil
import time
import traceback
import platform
import socket
import getpass
import FF_utils as utils
import FF_device_utils as dutils


class Reporter():
    
    def __init__(self):
        #Initializing Variables
        self.strBaseFrameworkFolder = ""   #Ex: /volumes/user....../HiveTestAutomation
        self.strResultsPath = ""
        self.strBackupDirPath = ""
        self.strCurrentResFolder = ""
        self.strCurrentHTMLFolder = ""
        self.strCurrentTXTFolder = ""
        
        self.strExecSummaryHTMLFilePath = ""
        self.strTestResHTMLFilePath = ""
        self.strCSSFilePath = ""
        
        self.intPassTCCount = 0
        self.intFailTCCount = 0
        
        self.strCurrentApplication = ""
        self.strCurrentEnvironment = ""
        self.strCurrentTestIterationList = ""
        self.strCurrentExecutionTerminal = ""
        
        self.strCurrentModule = ""
        self.strCurrentTag = ""
        self.strCurrentFeatureFileName = ""
        self.strPreviousScenario = ""
        self.strCurrentScenario = ""
        self.intScenarioCounter = 1
        self.strCurrentScenarioID = ""
        self.strCurrentScenarioDesc = ""
        self.strCurrentTestID = ""
        self.strCurrentTestDesc = ""
        self.intCurrentIteration = ""
        self.strCurrentBusFlowKeyword = ""
        
        self.intStepNumber = 1
        self.intPassStepCount = 0
        self.intFailStepCount = 0
        
        self.ActionStatus = True
        self.strTCStatus = ""
        self.intExecStartTime = 0.0
        self.intTCStartTime = 0.0
        self.strTCDuration = 0.0
        self.strOnError = ""
        self.intScreenshotCount = 1
        self.strEndPoint = ""
        self.strNodeID = ""
        self.platformVersion = ""
        self.oDeviceVersionDict = {}
        
        self.intIterationCntr = 0
        self.intIterationPassCntr = 0
        self.intIterationFailCntr = 0
        
        self.APIType = ""
        
        self.oDictWeekDays = {'sun' : 'Sunday',
                                            'mon' : 'Monday',
                                            'tue' : 'Tuesday',
                                            'wed' : 'Wednesday',
                                            'thu' : 'Thursday',
                                            'fri' : 'Friday',
                                            'sat' : 'Saturday'
                                            }
        
        #Creating the Test Results folder set
        self.create_test_folders()
        
        
    #Ensures the dirPath exists, if not creates the same
    def ensure_dir(self, dirpath):
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        return dirpath
    
    
    #Gets the Time stamp for creating the folder set or for reporting time stamp based on boolFolderCreate 
    def getTimeStamp(self, boolFolderCreate):
        if boolFolderCreate:
            str_format = "%d-%b-%Y_%H-%M-%S"  
        else:
            str_format = "%d-%b-%Y %H:%M:%S" 
        today = datetime.today()
        return today.strftime(str_format)
    
                
    #Create the folder structure for the results
    def create_test_folders(self):

        self.strBaseFrameworkFolder = os.path.abspath(__file__ + "/../../../../../")
        strAPI = utils.getAttribute('common', 'apiValidationType')
        if 'ZIGBEE' in strAPI.upper():
            strAPIFolder = 'Device_Test_Automation/'
        else: strAPIFolder = 'Web-Mobile_Test_Automation/'
        strSystemResultFolderName = ''
        if 'DARWIN' in platform.system().upper():
            if os.path.exists("/volumes/hardware"):
                strSystemResultFolderName = getpass.getuser() + "_" + socket.gethostname().split(".")[0]
                strTestResultFolder ="/volumes/hardware/" + strAPIFolder + '/Test_Results/'
                self.ensure_dir(strTestResultFolder + strSystemResultFolderName)
        elif 'LINUX' in platform.system().upper():
            if os.path.exists("/home/pi/hardware"):
                strSystemResultFolderName = socket.gethostname().split(".")[0].split("-")[1]
                strTestResultFolder ="/home/pi/hardware/" + strAPIFolder + '/Test_Results/'
                self.ensure_dir(strTestResultFolder + strSystemResultFolderName)
        if not strSystemResultFolderName == "":
            self.strResultsPath = strTestResultFolder + strSystemResultFolderName + '/'
        else: self.strResultsPath = os.path.abspath(self.strBaseFrameworkFolder + "/03_Results_Tier/")
        self.ensure_dir(self.strResultsPath)
        self.strBackupDirPath = self.ensure_dir(os.path.abspath(self.strResultsPath + '/Backup/'))
        #self.backup_previous_results()
        
        strKitBatchFilePath = os.path.abspath(self.strBaseFrameworkFolder + "/02_Manager_Tier/EnviromentFile/kit_batch.json")
        strJson = open(strKitBatchFilePath, mode='r')
        oKitBatchDict = json.loads(strJson.read())
        strJson.close()
        if 'Y' in oKitBatchDict['kit_batch']['batch_execution']['status'].upper(): 
            self.strResultsPath = os.path.abspath(self.strResultsPath + oKitBatchDict['kit_batch']['batch_execution']['current_batch_result_folder'] + '/Kit_Results/')
            self.ensure_dir(self.strResultsPath)
            self.ensure_dir(os.path.abspath(self.strResultsPath + '/Temp'))
        
        if 'Y' in utils.getAttribute('batch_execution', 'status').upper() and utils.getAttribute('batch_execution', 'result_folder_name') != "":
            self.strKitResultFolderName = os.path.abspath(utils.getAttribute('batch_execution', 'result_folder_name') + '/')
        else: self.strKitResultFolderName = utils.getAttribute('common', 'resultFolderLabel') + '_' + self.getTimeStamp(True) + '/'
        self.strCurrentResFolder = self.ensure_dir(os.path.abspath(self.strResultsPath + '/' + self.strKitResultFolderName))
        
        self.strCurrentHTMLFolder = self.ensure_dir(os.path.abspath(self.strCurrentResFolder + '/HTML' + '/'))
        self.strCurrentTXTFolder = self.ensure_dir(os.path.abspath(self.strCurrentResFolder + '/Text' + '/'))
        self.strCurrentScreenshotFolder = self.ensure_dir(os.path.abspath(self.strCurrentResFolder + '/Screenshot' + '/'))
        self.create_result_json()
        strScriptsFolder = os.path.abspath(self.strBaseFrameworkFolder + "/02_Manager_Tier/EnviromentFile/scripts")
        strSourceCanvasJSFilePath = os.path.abspath(strScriptsFolder + "/canvasjs.min.js")  
        strSourceGoJSFilePath = os.path.abspath(strScriptsFolder + "/go.js")
        strSourceGoSamplesJSFilePath = os.path.abspath(strScriptsFolder + "/goSamples.js")
        strSourceGoSamplesCSSFilePath = os.path.abspath(strScriptsFolder + "/highlight.css")
        strSourceHighlightJsFilePath = os.path.abspath(strScriptsFolder + "/highlight.js")
         
        strSourceTGImageFilePath = os.path.abspath(strScriptsFolder + "/Images/HSTGStick.png")
        strSourceDWSImageFilePath = os.path.abspath(strScriptsFolder + "/Images/HSDWS003.png")
        strSourceWDSImageFilePath = os.path.abspath(strScriptsFolder + "/Images/HSWDS00140002.png")
        strSourceFWUKImageFilePath = os.path.abspath(strScriptsFolder + "/Images/HSFWBulb01.png")
        strSourceFWUSImageFilePath = os.path.abspath(strScriptsFolder + "/Images/HSFWBulb01US.png")
        strSourceTWUKImageFilePath = os.path.abspath(strScriptsFolder + "/Images/HSTWBulb01UK.png")
        strSourceTWUSImageFilePath = os.path.abspath(strScriptsFolder + "/Images/HSTWBulb01US.png")
        strSourceRGBUKImageFilePath = os.path.abspath(strScriptsFolder + "/Images/HSRGBBulb01UK.png")
        strSourceRGBUSImageFilePath = os.path.abspath(strScriptsFolder + "/Images/HSRGBBulb01US.png")
        strSourceMOTImageFilePath = os.path.abspath(strScriptsFolder + "/Images/HSMOT003.png")
        strSourcePIRImageFilePath = os.path.abspath(strScriptsFolder + "/Images/HSPIR00140005.png")
        strSourceSLP2ImageFilePath = os.path.abspath(strScriptsFolder + "/Images/HSSLP2.png")
        strSourceSLP2bImageFilePath = os.path.abspath(strScriptsFolder + "/Images/HSSLP2b.png")
        strSourceSLP2cImageFilePath = os.path.abspath(strScriptsFolder + "/Images/HSSLP2c.png")
        strSourceSLR1ImageFilePath = os.path.abspath(strScriptsFolder + "/Images/HSSLR1.png")
        strSourceSLR1bImageFilePath = os.path.abspath(strScriptsFolder + "/Images/HSSLR1b.png")
        strSourceSLR2ImageFilePath = os.path.abspath(strScriptsFolder + "/Images/HSSLR2.png")
        strSourceSLR2bImageFilePath = os.path.abspath(strScriptsFolder + "/Images/HSSLR2b.png")
        strSourceSLT3ImageFilePath = os.path.abspath(strScriptsFolder + "/Images/HSSLT3.png")
        strSourceSLT3bImageFilePath = os.path.abspath(strScriptsFolder + "/Images/HSSLT3b.png")
        strSourceSLB1ImageFilePath = os.path.abspath(strScriptsFolder + "/Images/HSSLB1.png")
        strSourceSLB1aImageFilePath = os.path.abspath(strScriptsFolder + "/Images/HSSLB1a.png")
        strSourceSLB1bImageFilePath = os.path.abspath(strScriptsFolder + "/Images/HSSLB1b.png")
        strSourceSLB3ImageFilePath = os.path.abspath(strScriptsFolder + "/Images/HSSLB3.png")
        
        
        
        oFileWriter = open(self.strCurrentTXTFolder + 'ExecutionInProgress.txt', 'w')    
        oFileWriter.write("ExecutionInProgress\n")
        oFileWriter.close()
        if os.path.exists(strSourceCanvasJSFilePath):
            strDestCanvasJSFilePath = os.path.abspath(self.strCurrentScreenshotFolder + '/canvasjs.min.js')
            shutil.copyfile(strSourceCanvasJSFilePath, strDestCanvasJSFilePath)
            strDestgoJSFilePath = os.path.abspath(self.strCurrentScreenshotFolder + '/go.js')
            shutil.copyfile(strSourceGoJSFilePath, strDestgoJSFilePath)
            strDestGoSamplesJSFilePath = os.path.abspath(self.strCurrentScreenshotFolder + '/goSamples.js')
            shutil.copyfile(strSourceGoSamplesJSFilePath, strDestGoSamplesJSFilePath)
            strDestGoSamplesCSSFilePath = os.path.abspath(self.strCurrentScreenshotFolder + '/highlight.css')
            shutil.copyfile(strSourceGoSamplesCSSFilePath, strDestGoSamplesCSSFilePath)
            strDestHighlightJSFilePath = os.path.abspath(self.strCurrentScreenshotFolder + '/highlight.js')
            shutil.copyfile(strSourceHighlightJsFilePath, strDestHighlightJSFilePath)
            strDestTGImageFilePath = os.path.abspath(self.strCurrentScreenshotFolder + '/HSTGStick.png')
            shutil.copyfile(strSourceTGImageFilePath, strDestTGImageFilePath)
            strDestDWSImageFilePath = os.path.abspath(self.strCurrentScreenshotFolder + '/HSDWS003.png')
            shutil.copyfile(strSourceDWSImageFilePath, strDestDWSImageFilePath)
            strDestWDSImageFilePath = os.path.abspath(self.strCurrentScreenshotFolder + '/HSWDS00140002.png')
            shutil.copyfile(strSourceWDSImageFilePath, strDestWDSImageFilePath)
            strDestFWUKImageFilePath = os.path.abspath(self.strCurrentScreenshotFolder + '/HSFWBulb01.png')
            shutil.copyfile(strSourceFWUKImageFilePath, strDestFWUKImageFilePath)
            strDestFWUSImageFilePath = os.path.abspath(self.strCurrentScreenshotFolder + '/HSFWBulb01US.png')
            shutil.copyfile(strSourceFWUSImageFilePath, strDestFWUSImageFilePath)
            strDestTWUKImageFilePath = os.path.abspath(self.strCurrentScreenshotFolder + '/HSTWBulb01UK.png')
            shutil.copyfile(strSourceTWUKImageFilePath, strDestTWUKImageFilePath)
            strDestTWUSImageFilePath = os.path.abspath(self.strCurrentScreenshotFolder + '/HSTWBulb01US.png')
            shutil.copyfile(strSourceTWUSImageFilePath, strDestTWUSImageFilePath)
            strDestRGBUKImageFilePath = os.path.abspath(self.strCurrentScreenshotFolder + '/HSRGBBulb01UK.png')
            shutil.copyfile(strSourceRGBUKImageFilePath, strDestRGBUKImageFilePath)
            strDestRGBUSImageFilePath = os.path.abspath(self.strCurrentScreenshotFolder + '/HSRGBBulb01US.png')
            shutil.copyfile(strSourceRGBUSImageFilePath, strDestRGBUSImageFilePath)
            strDestMOTImageFilePath = os.path.abspath(self.strCurrentScreenshotFolder + '/HSMOT003.png')
            shutil.copyfile(strSourceMOTImageFilePath, strDestMOTImageFilePath)
            strDestPIRImageFilePath = os.path.abspath(self.strCurrentScreenshotFolder + '/HSPIR00140005.png')
            shutil.copyfile(strSourcePIRImageFilePath, strDestPIRImageFilePath)
            strDestSLP2ImageFilePath = os.path.abspath(self.strCurrentScreenshotFolder + '/HSSLP2.png')
            shutil.copyfile(strSourceSLP2ImageFilePath, strDestSLP2ImageFilePath)
            strDestSLP2bImageFilePath = os.path.abspath(self.strCurrentScreenshotFolder + '/HSSLP2b.png')
            shutil.copyfile(strSourceSLP2bImageFilePath, strDestSLP2bImageFilePath)
            strDestSLP2cImageFilePath = os.path.abspath(self.strCurrentScreenshotFolder + '/HSSLP2c.png')
            shutil.copyfile(strSourceSLP2cImageFilePath, strDestSLP2cImageFilePath)
            strDestSLR1ImageFilePath = os.path.abspath(self.strCurrentScreenshotFolder + '/HSSLR1.png')
            shutil.copyfile(strSourceSLR1ImageFilePath, strDestSLR1ImageFilePath)
            strDestSLR2ImageFilePath = os.path.abspath(self.strCurrentScreenshotFolder + '/HSSLR2.png')
            shutil.copyfile(strSourceSLR2ImageFilePath, strDestSLR2ImageFilePath)
            strDestSLR1bImageFilePath = os.path.abspath(self.strCurrentScreenshotFolder + '/HSSLR1b.png')
            shutil.copyfile(strSourceSLR1bImageFilePath, strDestSLR1bImageFilePath)
            strDestSLR2bImageFilePath = os.path.abspath(self.strCurrentScreenshotFolder + '/HSSLR2b.png')
            shutil.copyfile(strSourceSLR2bImageFilePath, strDestSLR2bImageFilePath)
            strDestSLT3ImageFilePath = os.path.abspath(self.strCurrentScreenshotFolder + '/HSSLT3.png')
            shutil.copyfile(strSourceSLT3ImageFilePath, strDestSLT3ImageFilePath)
            strDestSLT3bImageFilePath = os.path.abspath(self.strCurrentScreenshotFolder + '/HSSLT3b.png')
            shutil.copyfile(strSourceSLT3bImageFilePath, strDestSLT3bImageFilePath)
            strDestSLB1ImageFilePath = os.path.abspath(self.strCurrentScreenshotFolder + '/HSSLB1.png')
            shutil.copyfile(strSourceSLB1ImageFilePath, strDestSLB1ImageFilePath)
            strDestSLB1aImageFilePath = os.path.abspath(self.strCurrentScreenshotFolder + '/HSSLB1a.png')
            shutil.copyfile(strSourceSLB1aImageFilePath, strDestSLB1aImageFilePath)
            strDestSLB1bImageFilePath = os.path.abspath(self.strCurrentScreenshotFolder + '/HSSLB1b.png')
            shutil.copyfile(strSourceSLB1bImageFilePath, strDestSLB1bImageFilePath)
            strDestSLB3ImageFilePath = os.path.abspath(self.strCurrentScreenshotFolder + '/HSSLB3.png')
            shutil.copyfile(strSourceSLB3ImageFilePath, strDestSLB3ImageFilePath)
            if 'Y' in oKitBatchDict['kit_batch']['batch_execution']['status'].upper():
                shutil.copyfile(strSourceCanvasJSFilePath, os.path.abspath(self.strResultsPath + '/Temp/canvasjs.min.js'))
            
        
    #Backup the the previously created test result folder
    def backup_previous_results(self):        
        for str_subdir in os.listdir(self.strResultsPath):    
            if str_subdir.rfind('Backup') < 0:
                str_subdir_abspath = os.path.abspath(self.strResultsPath + str_subdir)
                #print(str_subdir)
                if not os.path.exists(self.strBackupDirPath + str_subdir):
                    if not os.path.exists(os.path.abspath(str_subdir_abspath + '/Text/' + 'ExecutionInProgress.txt')): 
                        dt_obj = datetime.fromtimestamp(os.stat(str_subdir_abspath).st_ctime)
                        strMonthYear = datetime.strftime(dt_obj, "%b_%Y")
                        strDay = datetime.strftime(dt_obj, "%d")
                        strPathToMoveFIleTo = os.path.abspath(self.strBackupDirPath + strMonthYear + "/" + strDay + '/')
                        self.ensure_dir(strPathToMoveFIleTo)
                        if not os.path.exists(strPathToMoveFIleTo + str_subdir):
                            shutil.move(str_subdir_abspath, strPathToMoveFIleTo)
    
    def HTML_Execution_Summary_Initialize(self, strCurrentApplication = "Hive", strCurrentEnvironment = "Beta_Env"):
        self.intPassTCCount = 0
        self.intFailTCCount = 0
        self.strCurrentApplication = strCurrentApplication
        self.strCurrentEnvironment = utils.getAttribute('common', 'currentEnvironment')
        self.SummaryFileName = self.strCurrentApplication + "-" + self.strCurrentEnvironment + "_Execution_Summary.HTML"
        utils.setAttribute_KitBatch('batch_execution', 'current_kit_result_summary_path', self.strKitResultFolderName + self.SummaryFileName)
        self.strExecSummaryHTMLFilePath = os.path.abspath(self.strCurrentResFolder + '/' + self.SummaryFileName)
        try:             
            strEnvironmentFilePath = os.path.abspath(self.strBaseFrameworkFolder + "/02_Manager_Tier/EnviromentFile")
            
            oFileW = open(os.path.abspath(strEnvironmentFilePath + '/scripts/Temp.txt'), 'w')
            oFileW.write(self.strExecSummaryHTMLFilePath)
            oFileW.close()
            self.strCSSFilePath = os.path.abspath(strEnvironmentFilePath + "/Style.CSS")    
            oFileReader = open(self.strCSSFilePath, 'r')
            
            oFileWriter = open(self.strExecSummaryHTMLFilePath, 'w')               
            
            oFileWriter.write("<!DOCTYPE html>\n")
            oFileWriter.write("<html>\n")
            oFileWriter.write("<head>\n")
            oFileWriter.write("         <meta charset='UTF-8'>\n") 
            strChartData = ""
            if str(utils.getAttribute("COMMON", "apiValidationType", None, None)).upper() == "ZIGBEE API":
                oFileWriter.write("<script type='text/javascript' src='./Screenshot/go.js'></script>\n") 
                oFileWriter.write("<script type='text/javascript' src='./Screenshot/goSamples.js'></script>\n") 
                strNetworkPath = strEnvironmentFilePath + "/ZigbeeDevices.json"  
                oJson = dutils.getZigbeeDevicesJson()
                
                oNodes = str(oJson.keys()).replace("dict_keys([","").replace("'","").replace("])","").split(",")
                oAllNodes = {}
                for intCounter in range( 0,len(oNodes)):
                    strDevice = str(oNodes[intCounter]).replace(" ","")
                    strkey = str(oJson[strDevice]["name"])+"-"+str(oJson[strDevice]["nodeID"])
                    oAllNodes[strkey] = {}
                    oAllNodes[strkey]["key"] = strkey
                    oAllNodes[strkey]["macID"] = oJson[strDevice]["macID"]
                    oAllNodes[strkey]["name"] = strDevice
                    oAllNodes[strkey]["ModeId"] = str(oJson[strDevice]["name"])
                    if str(oJson[strDevice]["type"]) != "RFD":
                        oAllNodes[strkey]["childNode"] = oJson[strDevice]["childNodes"]
                    else:
                        oAllNodes[strkey]["childNode"] = []
                strChartData = "["
                nodesList = []
                intNodeCtr = 0
                nodesList.append([])
                nodesList[intNodeCtr].append("TGStick-0000")
                nodesList[intNodeCtr].append("")
                nodesList[intNodeCtr].append("")
                flag = True
                
                while flag:
                    flag = False
                    for oNodeId in nodesList:
                        if oNodeId[1] == "False" or oNodeId[1] == "":
                            strChartData = strChartData + "{"
                            strChartData = strChartData + "\"key\":\""+oAllNodes[oNodeId[0]]["key"]+"\","
                            strChartData = strChartData + "\"name\":\""+oAllNodes[oNodeId[0]]["name"]+"\","
                            strChartData = strChartData + "\"model\":\""+oAllNodes[oNodeId[0]]["ModeId"]+"\","
                            strChartData = strChartData + "\"macID\":\""+oAllNodes[oNodeId[0]]["macID"]+"\","
                            if oNodeId[1] == "":
                                oNodeId[1] = "True"
                                strChartData = strChartData[:-1]
                            if oNodeId[1] == "False":
                                oNodeId[1] = "True"
                                strChartData = strChartData + "\"parent\":\""+str(oNodeId[2])+"\""
                            strChartData = strChartData + "},"
                            for oNode in oAllNodes[oNodeId[0]]["childNode"]:
                                flag = True
                                intNodeCtr = intNodeCtr + 1
                                nodesList.append([])
                                for oRow in oAllNodes:
                                    if oNode in oRow:
                                        nodesList[intNodeCtr].append(oRow)
                                nodesList[intNodeCtr].append("False")
                                nodesList[intNodeCtr].append(oNodeId[0])
                        
                strChartData = strChartData[:-1]
                strChartData = strChartData + "]"
                print(strChartData)
            oFileWriter.write("         <title>Hive - Automation Execution Results Summary</title>\n") 
            strData = oFileReader.read().replace("CHARTDATA",strChartData)
            oFileWriter.write(strData + '\n')
            oFileReader.close()
            
            oFileWriter.write("</head>\n") 
            if str(utils.getAttribute("COMMON", "apiValidationType", None, None)).upper() == "ZIGBEE API":
                oFileWriter.write("<body onload=\"init()\">")
            else:
                oFileWriter.write("<body>\n")
            oFileWriter.write("<table id='header'>\n") 
            oFileWriter.write("<colgroup>\n")
            oFileWriter.write("<col style='width: 25%' />\n") 
            oFileWriter.write("<col style='width: 25%' />\n") 
            oFileWriter.write("<col style='width: 25%' />\n") 
            oFileWriter.write("<col style='width: 25%' />\n") 
            oFileWriter.write("</colgroup>\n") 
     
            oFileWriter.write("<thead>\n") 
            oFileWriter.write("<tr class='heading'>\n") 
            oFileWriter.write("<th colspan='4' style='font-family:Copperplate Gothic Bold; font-size:1.4em;'>\n") 
            oFileWriter.write("Hive -  Automation Execution Result Summary\n") 
            oFileWriter.write("</th>\n") 
            oFileWriter.write("</tr>\n") 
            oFileWriter.write("<tr class='subheading'>\n") 
            oFileWriter.write("<th>&nbsp;Date&nbsp;&&nbsp;Time</th>\n") 
            #oFileWriter.write("<th>&nbsp;:&nbsp;25-Jul-2014&nbsp;05:02:20&nbsp;PM</th>\n")
            oFileWriter.write("<th>&nbsp;:&nbsp;" + self.getTimeStamp(False) + "</th>\n") 
            self.intExecStartTime = time.monotonic()
            oFileWriter.write("<th>&nbsp;OnError</th>\n") 
            oFileWriter.write("<th>&nbsp;:&nbsp;" + self.strOnError + "</th>\n") 
            oFileWriter.write("</tr>\n") 
            oFileWriter.write("<tr class='subheading'>\n") 
            oFileWriter.write("<th>&nbsp;Application</th>\n") 
            oFileWriter.write("<th>&nbsp;:&nbsp;" + self.strCurrentApplication + "</th>\n") 
            oFileWriter.write("<th>&nbsp;Environment</th>\n") 
            oFileWriter.write("<th>&nbsp;:&nbsp;" + self.strCurrentEnvironment + "</th>\n") 
            oFileWriter.write("</tr>\n") 
            
            for oKey in self.oDeviceVersionDict.keys():
                oFileWriter.write("<tr class='subheading'>\n") 
                oFileWriter.write("<th>&nbsp;" + oKey + " Model</th>\n") 
                oFileWriter.write("<th>&nbsp;:&nbsp;" + self.oDeviceVersionDict[oKey].split('$$')[0] + "</th>\n") 
                oFileWriter.write("<th>&nbsp;" + oKey + " Version</th>\n") 
                oFileWriter.write("<th>&nbsp;:&nbsp;" + self.oDeviceVersionDict[oKey].split('$$')[1] + "</th>\n") 
                oFileWriter.write("</tr>\n") 
            
            oFileWriter.write("</thead>\n") 
            oFileWriter.write("</table>\n") 
            
            if str(utils.getAttribute("COMMON", "apiValidationType", None, None)).upper() == "ZIGBEE API":
                oFileWriter.write("<table id='network'>\n") 
                oFileWriter.write("<tr>\n") 
                oFileWriter.write("<th><div id=\"myDiagramDiv\" style=\"background-color: #939393; border: solid 1px black; width:100%; height: 300px\"></div></th>\n")
                oFileWriter.write("</tr>\n") 
                oFileWriter.write("</table>\n")
             
            oFileWriter.write("<table id='main'>\n") 
            oFileWriter.write("<colgroup>\n") 
            oFileWriter.write("<col style='width: 10%' />\n") 
            oFileWriter.write("<col style='width: 10%' />\n") 
            oFileWriter.write("<col style='width: 54%' />\n") 
            oFileWriter.write("<col style='width: 16%' />\n") 
            oFileWriter.write("<col style='width: 10%' />\n") 
            oFileWriter.write("</colgroup>\n") 
             
            oFileWriter.write("<thead>\n") 
            oFileWriter.write("<tr class='heading'>\n") 
            oFileWriter.write("<th>Feature_Filename</th>\n") 
            oFileWriter.write("<th>Scenario_ID</th>\n") 
            oFileWriter.write("<th>Scenario_Description</th>\n") 
            oFileWriter.write("<th>Execution_Time</th>\n") 
            oFileWriter.write("<th>Test_Status</th>\n") 
            oFileWriter.write("</tr>\n") 
            oFileWriter.write("</thead>\n")
     
            # Always close files.    
            oFileWriter.close()
            return self.strExecSummaryHTMLFilePath
        except:
            print('Reporter Exception in HTML_Execution_Summary_Initialize\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
            print(self.strExecSummaryHTMLFilePath)
            
    def HTML_TestCase_Initialize(self, strCurrentScenarioID):
        self.ActionStatus = True
        self.strCurrentScenarioID = strCurrentScenarioID
        self.strCurrentTestDesc = 'This Test validated the System Mode'
        self.strTestResHTMLFilePath = os.path.abspath(self.strCurrentHTMLFolder + '/' + self.strCurrentApplication + "-" + self.strCurrentEnvironment + \
                                self.strCurrentTag + "_" + self.strCurrentScenarioID + ".HTML")
        self.intStepNumber = 1
        self.intPassStepCount = 0
        self.intFailStepCount = 0
        self.strTCStatus = "PASSED"
        
        try:
            print(os.path.exists(self.strCSSFilePath)) 
            oFileReader = open(self.strCSSFilePath, 'r')
            
            oFileWriter = open(self.strTestResHTMLFilePath, 'x') 
            
            oFileWriter.write("<!DOCTYPE html>\n")
            oFileWriter.write("<html>\n")
            oFileWriter.write("<head>\n")
            oFileWriter.write("         <meta charset='UTF-8'>\n") 
            oFileWriter.write("         <title>" + self.strCurrentApplication + " Application - "+
                                    self.strCurrentScenarioID + " Automation Execution Results</title>\n") 
            
            
            strData = oFileReader.read()
            oFileWriter.write(strData + '\n')
            oFileReader.close()
            
            oFileWriter.write("</head>\n")        
            oFileWriter.write("<body>\n") 
            oFileWriter.write("<table id='header'>\n") 
            oFileWriter.write("<colgroup>\n") 
            oFileWriter.write("<col style='width: 25%' />\n") 
            oFileWriter.write("<col style='width: 25%' />\n") 
            oFileWriter.write("<col style='width: 25%' />\n") 
            oFileWriter.write("<col style='width: 25%' />\n") 
            oFileWriter.write("</colgroup>\n") 
            
            oFileWriter.write("<thead>\n") 
            oFileWriter.write("<tr class='heading'>\n") 
            oFileWriter.write("<th colspan='4' style='font-family:Copperplate Gothic Bold; font-size:1.4em;'>\n") 
            oFileWriter.write(self.strCurrentApplication + " Application - "+ \
                                self.strCurrentScenarioID + " Automation Execution Results\n")
            oFileWriter.write("</th>\n") 
            oFileWriter.write("</tr>\n")
            oFileWriter.write("<tr class='subheading'>\n") 
            oFileWriter.write("<th>&nbsp;Date&nbsp;&&nbsp;Time</th>\n") 
            oFileWriter.write("<th>&nbsp;:&nbsp;" + self.getTimeStamp(False) + "</th>\n") 
            self.intTCStartTime = time.monotonic()
            oFileWriter.write("<th>&nbsp;Iterations</th>\n") 
            oFileWriter.write("<th>&nbsp;:&nbsp;" + self.strCurrentTestIterationList + "</th>\n") 
            oFileWriter.write("</tr>\n") 
            
            oFileWriter.write("<tr class='subheading'>\n") 
            oFileWriter.write("<th>&nbsp;Terminal</th>\n") 
            oFileWriter.write("<th>&nbsp;:&nbsp;" + self.strCurrentExecutionTerminal + "</th>\n") 
            oFileWriter.write("<th>&nbsp;Executed&nbsp;on</th>\n") 
            strLocalHostName = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
            oFileWriter.write("<th>&nbsp;:&nbsp;" + strLocalHostName + "</th>\n") 
            oFileWriter.write("</tr>\n") 
            
            oFileWriter.write("<tr class='subheading'>\n") 
            oFileWriter.write("<th>&nbsp;Node&nbsp;ID</th>\n") 
            oFileWriter.write("<th>&nbsp;:&nbsp;" + self.strNodeID + "</th>\n") 
            oFileWriter.write("<th>&nbsp;End&nbsp;Point</th>\n") 
            strEndPoint = self.strEndPoint
            if strEndPoint == '05':
                strEndPoint = '05 - Central Heating'
            elif strEndPoint == '06':
                strEndPoint = '06 - Water Heating'
            oFileWriter.write("<th>&nbsp;:&nbsp;" + strEndPoint + "</th>\n") 
            oFileWriter.write("</tr>\n")
            
            oFileWriter.write("</thead>\n") 
            oFileWriter.write("</table>\n") 
        
            oFileWriter.write("<table id='main'>\n") 
            oFileWriter.write("<colgroup>\n") 
            oFileWriter.write("<col style='width: 5%' />\n") 
            oFileWriter.write("<col style='width: 10%' />\n") 
            oFileWriter.write("<col style='width: 12%' />\n") 
            oFileWriter.write("<col style='width: 65%' />\n") 
            oFileWriter.write("<col style='width: 8%' />\n") 
            oFileWriter.write("</colgroup>\n") 
            
            oFileWriter.write("<thead>\n") 
            oFileWriter.write("<tr class='heading'>\n") 
            oFileWriter.write("<th>Log_No</th>\n") 
            oFileWriter.write("<th>Time_Stamp</th>\n") 
            oFileWriter.write("<th>Validation Type</th>\n") 
            oFileWriter.write("<th>Log_Details</th>\n") 
            oFileWriter.write("<th>Status</th>\n") 
            oFileWriter.write("</tr>\n") 
            oFileWriter.write("</thead>\n") 
            
            #Always close files.                
            oFileWriter.close()
        except:
            print('Reporter Exception in HTML_TestCase_Initialize \n {0}'.format(traceback.format_exc().replace('File', '$~File')))
            print(self.strTestResHTMLFilePath)
    
    def HTML_TC_Iteration_Initialize(self, intIteration):
        self.ActionStatus = True
        self.intStepNumber = 1
        self.intCurrentIteration = str(intIteration)
        try:
            
            oFileWriter = open(self.strTestResHTMLFilePath, 'a')
            
            #strIteration = "Iteration: " + intCurrentIteration
            oFileWriter.write("<tbody>\n")
            oFileWriter.write("<tr class='section'>\n")
            oFileWriter.write("<td colspan='5' onclick=\"toggleMenu('Iteration" + self.intCurrentIteration + "')\">+ Iteration: " + self.intCurrentIteration + "</td>\n") 
            oFileWriter.write("</tr>\n") 
            oFileWriter.write("</tbody>\n") 
            oFileWriter.write("<tbody id='Iteration" + self.intCurrentIteration + "' style='display:table-row-group'>\n")
            
            #Always close files.                
            oFileWriter.close()
            self.intIterationCntr =self.intIterationCntr + 1
        except:
            print('Reporter Exception in HTML_TC_Iteration_Initialize \n {0}'.format(traceback.format_exc().replace('File', '$~File')))
            print(self.strTestResHTMLFilePath)
            
    def HTML_TC_Iteration_Footer(self):
            
        try:
            
            oFileWriter = open(self.strTestResHTMLFilePath, 'a')            
            oFileWriter.write("</tbody>\n")
            
            #Always close files.                
            oFileWriter.close()
        except:
            print('Reporter Exception in HTML_TC_Iteration_Footer Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
            print(self.strTestResHTMLFilePath)
            
    def HTML_TC_BusFlowKeyword_Initialize(self, strBusFlowKeyword):
        self.intStepNumber = 1;
        self.strCurrentBusFlowKeyword = strBusFlowKeyword
        try:
            
            oFileWriter = open(self.strTestResHTMLFilePath, 'a')
            
            oFileWriter.write("<tr class='subheading subsection'>\n")
            oFileWriter.write("<td colspan='5' onclick=\"toggleSubMenu('Iteration"+ self.intCurrentIteration + self.strCurrentBusFlowKeyword + "')\">&nbsp;+ " + self.strCurrentBusFlowKeyword + "</td>\n")  
            oFileWriter.write("</tr>\n")  
            
            #Always close files.                
            oFileWriter.close()
        except:
            print('Reporter Exception in HTML_TC_BusFlowKeyword_Initialize \n {0}'.format(traceback.format_exc().replace('File', '$~File')))
            print(self.strTestResHTMLFilePath)
                
    def ReportEvent(self, strValidationType, strLogDescription, strStatus, strTableAlign = 'LEFT', boolLogwithTimeStamp = True, driver = None):
            
        try:
            strStatus = strStatus.upper()
            oFileWriter = open(self.strTestResHTMLFilePath, 'a')
            
            oFileWriter.write("<tr class='content' id='Iteration" + self.intCurrentIteration + self.strCurrentBusFlowKeyword + "{0}'>\n".format(self.intStepNumber)) 
            if boolLogwithTimeStamp:
                oFileWriter.write("<td>" + str(self.intStepNumber) + "</td>\n") 
                oFileWriter.write("<td><small>" + self.getTimeStamp(False) + "</small></td>\n") 
                oFileWriter.write("<td class='justified'>" + strValidationType + "</td>\n")  
            else:
                oFileWriter.write("<td></td>\n") 
                oFileWriter.write("<td><small></small></td>\n") 
                oFileWriter.write("<td class='justified'></td>\n")  
            #oFileWriter.write("<td class='innertable'>" + strLogDescription + "</td>\n")  
            oFileWriter.write("<td class='justified'>\n")
            if strTableAlign.upper() == 'LEFT': oFileWriter.write("<TABLE class='lefttable'  BORDER='1'>\n")
            elif strTableAlign.upper() == 'CENTER': oFileWriter.write("<TABLE class='innertable'  BORDER='1'>\n")
            
            if strLogDescription.find("@@@") >= 0:
                arrRows = strLogDescription.split("@@@")
                strRow = arrRows[0]
                if strRow.find("$$") >= 0:
                        oFileWriter.write("<TR align=center>\n")
                        arrCol = strRow.split("$$")
                        for strCol in arrCol:
                            strColor = "BLACK"
                            if strCol.find('||') >=0:
                                strColor = "RED"
                                strCol = strCol.split('||')[1]
                            oFileWriter.write("<TH><FONT COLOR=" + strColor + ">" + strCol.strip() + "</FONT></TH>\n")
                        oFileWriter.write("<TR\>\n")
                else:   
                    oFileWriter.write("<TR>\n")
                    oFileWriter.write("<TH>" + strRow.strip() + "</TH>\n")
                    oFileWriter.write("</TR>\n")                    
                strLogDescription = arrRows[1]  
                    
            if strLogDescription.find("$~") >= 0:
                arrRows = strLogDescription.split("$~")
                for strRow in arrRows:
                    oFileWriter.write("<TR>\n")
                    if strRow.find("$$") >= 0:
                        arrCol = strRow.split("$$")
                        for strCol in arrCol:
                            strSpan = ""                            
                            strBold = ''
                            strColor = "BLACK"
                            if strCol.find('||') >=0:
                                strColor = "RED"
                                strCol = strCol.split('||')[1]
                                strBold = '<B>'
                            elif strCol.find("££") >= 0:
                                strCol = strCol.split("££")[1]
                                strColor = "PURPLE"
                                strBold = '<B>'
                            elif strCol.find('&R&') >= 0:
                                strSpan = 'rowspan= '  + strCol.split('&R&')[1]
                                strCol = strCol.split('&R&')[0]
                            elif strCol.find("&C&") >= 0:
                                strSpan = 'colspan=' +  strCol.split("&C&")[1]
                                strCol = strCol.split("&C&")[0]
                            oFileWriter.write("<TD " + strSpan + "><FONT COLOR=" + strColor + ">" + strBold +  strCol.strip() + "</FONT></TD>\n")
                    else:
                        oFileWriter.write("<TD>" + strRow + "</TD>\n")
                    oFileWriter.write("</TR>\n")
            elif strLogDescription.find("$$") >= 0:
                arrCol = strLogDescription.split("$$")
                oFileWriter.write("<TR>\n")
                for strCol in arrCol:
                    strBold = ''
                    if strCol.find("||") >= 0:
                        strCol = strCol.split("||")[1]
                        strColor = "RED"
                        strBold = '<B>'
                    elif strCol.find("££") >= 0:
                        strCol = strCol.split("££")[1]
                        strColor = "PURPLE"
                        strBold = '<B>'
                    else:
                        strColor = "BLACK"
                    oFileWriter.write("<TD><FONT COLOR=" + strColor + ">" + strBold + strCol.strip() + "</FONT></TD>\n")
                oFileWriter.write("</TR>\n")               
            else:
                oFileWriter.write("<TR>\n")
                oFileWriter.write("<TD>" + strLogDescription + "</TD>\n")
                oFileWriter.write("</TR>\n")
                
            oFileWriter.write("</TABLE>\n") 
            oFileWriter.write("</td>")
            
            
            
            '''
            if (((GlbVar.boolScreenshotForPass) and (strStatus == "PASS")) || ((GlbVar.boolScreenshotForFail) && (strStatus == "FAIL"))){                
                String strScreeshotPath = GlbVar.strTestRunResultPath +  "SCREENSHOTS" + GlbVar.sysFileSeperator + strCurrentApplication + strCurrentTag + "-" + 
                                                        strCurrentScenarioID + strCurrentScenarioID + "-" +  intScreenshotCount + ".png";
                CaptureScreenShot(strScreeshotPath);
             '''
            
            if not driver is None:
                
                strScreenShotPathHyperlink = '.' + os.sep + '..' + os.sep + 'Screenshot' + os.sep  + self.strCurrentApplication + self.strCurrentTag + "-" + self.strCurrentScenarioID + "-" +  str(self.intScreenshotCount) + ".png";
                strScreenShotPath= os.path.abspath(self.strCurrentScreenshotFolder + '/' + self.strCurrentApplication + self.strCurrentTag + "-" + self.strCurrentScenarioID + "-" +  str(self.intScreenshotCount) + ".png");
                
                driver.get_screenshot_as_file(strScreenShotPath)
                oFileWriter.write("<td class='" + strStatus.lower() + "'><a href='" + strScreenShotPathHyperlink + "'>" + strStatus + "</a></td>\n")
                self.intScreenshotCount += 1
            else:
                oFileWriter.write("<td class='" + strStatus.lower() + "'>" + strStatus + "</td>\n")  
            oFileWriter.write("</tr>\n") 
            
            self.intStepNumber += 1
            if (strStatus == "PASS"): 
                self.intPassStepCount += 1
            elif(strStatus == "FAIL"):
                self.intFailStepCount += 1
                self.strTCStatus = "FAILED"
                
            #Always close files.                
            oFileWriter.close()
            
            #Update the result json
            if "FAIL" in strStatus.upper():
                self.update_scenario_result_json(strStatus, strLogDescription)
            else: self.update_scenario_result_json("In-Progress", "")
                
        except:
            print('self.strTestResHTMLFilePath', self.strTestResHTMLFilePath)
            print('Reporter Exception in ReportEvent \n {0}'.format(traceback.format_exc().replace('File', '$~File')))
                    
    def getDuration(self, strDuration):
        arrDuration = strDuration.split(':')
        intHour = int(arrDuration[0])
        intMin = int(arrDuration[1])
        intSec = int(float(arrDuration[2]))
        
        if (intHour > 0):
            strDuration = str(intHour) + " hour(s), " + str(intMin) + " minute(s), " + str(intSec) + " seconds"
            if (intHour > 23): 
                intDay = intHour // 24
                intHour = intHour % 24
                strDuration = str(intDay) + " day(s), "  + str(intHour) + " hour(s), " + str(intMin) + " minute(s), " + str(intSec) + " seconds"
        else:
            strDuration = str(intMin) + " minute(s), " + str(intSec) + " seconds"
        return strDuration;
        
    def HTML_TestCase_Footer(self):
        
        try:
            
            oFileWriter = open(self.strTestResHTMLFilePath, 'a')
            
            oFileWriter.write("</table>\n")   
            
            oFileWriter.write("<table>\n")
            oFileWriter.write("<script type='text/javascript'>\n")
            oFileWriter.write("window.onload = function () {\n")
            oFileWriter.write("CanvasJS.addColorSet('chartshades',\n")
            oFileWriter.write("[//colorSet Array\n")            
            oFileWriter.write("'lightgreen',\n")
            oFileWriter.write("'red'           \n")    
            oFileWriter.write("]);\n")
            oFileWriter.write("var chart = new CanvasJS.Chart('chartContainer',\n")
            oFileWriter.write("{\n")
            oFileWriter.write("colorSet: 'chartshades',\n")
            oFileWriter.write("zoomEnabled: true,\n")
            oFileWriter.write("title:{\n")            
            oFileWriter.write("fontColor: '#C6FFEC',\n")
            oFileWriter.write("text: 'Execution Status'\n")
            oFileWriter.write("},\n")
            oFileWriter.write("animationEnabled: true,\n")
            oFileWriter.write("backgroundColor: 'black',\n")
            oFileWriter.write("legend:{\n")
            oFileWriter.write("fontColor: '#C6FFEC',\n")
            oFileWriter.write("verticalAlign: 'bottom',\n")
            oFileWriter.write("horizontalAlign: 'center'\n")
            oFileWriter.write("},data: [{        \n")
            oFileWriter.write("indexLabelFontSize: 20,\n")
            oFileWriter.write("indexLabelFontFamily: 'Monospace',     \n")  
            oFileWriter.write("indexLabelFontColor: '#C6FFEC', \n")
            oFileWriter.write("indexLabelLineColor: '#C6FFEC',     \n")   
            oFileWriter.write("indexLabelPlacement: 'auto',\n")
            oFileWriter.write("type: 'pie',       \n")
            oFileWriter.write("showInLegend: true,\n")
            oFileWriter.write("toolTipContent: '{y} - <strong>#percent%</strong>',\n")
            oFileWriter.write("dataPoints: [\n")
            if not self.intPassStepCount==0: oFileWriter.write("{  y: "+ str(self.intPassStepCount) + ", legendText:'PASS', indexLabel: '{y}' },\n")
            else: oFileWriter.write("{  y: "+ str(self.intPassStepCount) + ", legendText:'PASS'},\n")
            if not self.intFailStepCount==0: oFileWriter.write("{  y: " + str(self.intFailStepCount) + ", legendText:'FAIL' , indexLabel: '{y}'}\n")
            else: oFileWriter.write("{  y: " + str(self.intFailStepCount) + ", legendText:'FAIL'}\n")
            oFileWriter.write("]}]});chart.render();}\n")
            oFileWriter.write("</script>\n")
            oFileWriter.write("<script type='text/javascript' src='./../Screenshot/canvasjs.min.js'></script>\n")            
            oFileWriter.write("<tr  class='content' ><td><div id='chartContainer' style='height: 300px; width: 100%;'></div></td></tr></table>\n")
            
            oFileWriter.write("<table id='footer'>\n")
            oFileWriter.write("<colgroup>\n")
            oFileWriter.write("<col style='width: 25%' />\n")
            oFileWriter.write("<col style='width: 25%' />\n")
            oFileWriter.write("<col style='width: 25%' />\n")
            oFileWriter.write("<col style='width: 25%' />\n")
            oFileWriter.write("</colgroup>\n")
             
            oFileWriter.write("<tfoot>\n")
            oFileWriter.write("<tr class='heading'>\n")
            intTCEndTime = time.monotonic()
            self.strTCDuration = str(timedelta(seconds=intTCEndTime - self.intTCStartTime))
            self.strTCDuration = self.getDuration(self.strTCDuration)
            oFileWriter.write("<th colspan='4'>Execution Duration: " + self.strTCDuration + "</th>\n")
            oFileWriter.write("</tr>\n")
            oFileWriter.write("<tr class='subheading'>\n")
            oFileWriter.write("<td class='pass'>&nbsp;Steps passed</td>\n")
            oFileWriter.write("<td class='pass'>&nbsp;: {0}</td>\n".format(self.intPassStepCount))
            oFileWriter.write("<td class='fail'>&nbsp;Steps failed</td>\n")
            oFileWriter.write("<td class='fail'>&nbsp;: " + str(self.intFailStepCount) + "</td>\n")
            oFileWriter.write("</tr>\n")
            oFileWriter.write("</tfoot>\n")
            oFileWriter.write("</table>\n")
            oFileWriter.write("</body>\n")
            oFileWriter.write("</html>\n")
         
            self.intStepNumber += 1
            #Always close files.                
            oFileWriter.close()
            
            strStatusClass = self.strTCStatus.lower()
            strStatusClass = strStatusClass[0:4] 
            #Update HTML Summary on status and duration        
            oFileReader = open(self.strExecSummaryHTMLFilePath, 'r')
            strData = oFileReader.read()
            oFileReader.close()
            '''print('inprogress', strStatusClass)
            print('In-Progress', self.strTCStatus)'''
            strData = strData.replace("class='inprogress'", "class='" + strStatusClass + "'")
            strData = strData.replace('In-Progress', self.strTCStatus)            
            strData = strData.replace('------', str(self.strTCDuration))
            oFileWriter = open(self.strExecSummaryHTMLFilePath, 'w')
            oFileWriter.write(strData + '\n')             
            oFileWriter.close()
            if (self.strTCStatus == "PASSED"): self.intPassTCCount += 1
            if (self.strTCStatus == "FAILED"): self.intFailTCCount += 1
        except:
            print('Reporter Exception in HTML_TestCase_Footer \n {0}'.format(traceback.format_exc().replace('File', '$~File')))
            print(self.strTestResHTMLFilePath)
        
    def HTML_Execution_Summary_TCAddLink(self):
            
        try:
            
            oFileWriter = open(self.strExecSummaryHTMLFilePath, 'a')               
            
            oFileWriter.write("<tr class='content' >\n")
            oFileWriter.write("<td class='justified'>" + self.strCurrentFeatureFileName + "</td>\n")
            oFileDet = os.path.split(self.strTestResHTMLFilePath)
            oFileWriter.write("<td class='justified'><a href='" + './HTML/' + oFileDet[1] + "' target='about_blank'>" + self.strCurrentScenarioID + "</a></td>\n")
            oFileWriter.write("<td class='justified'>" + self.strCurrentScenarioDesc + "</td>\n")
            oFileWriter.write("<td>" + '------' + "</td>\n")   
            #str(self.strTCDuration)
            strStatusClass = self.strTCStatus.lower()
            strStatusClass = strStatusClass[0:4] 
            strStatusClass = 'inprogress'
            strTCStatus = 'In-Progress'
            oFileWriter.write("<td class='" + strStatusClass + "'>" + strTCStatus + "</td>\n")
            oFileWriter.write("</tr>\n")
     
            '''
            if (self.strTCStatus == "PASSED"): self.intPassTCCount += 1
            if (self.strTCStatus == "FAILED"): self.intFailTCCount += 1
            '''
            #Always close files.                
            oFileWriter.close()
        except:
            print('Reporter Exception in HTML_Execution_Summary_TCAddLink \n {0}'.format(traceback.format_exc().replace('File', '$~File')))
            print(self.strExecSummaryHTMLFilePath)
    
    def HTML_Execution_Summary_Footer(self):
            
        try:
            oFileWriter = open(self.strExecSummaryHTMLFilePath, 'a')
            oFileWriter.write("</tbody>\n")
            oFileWriter.write("</table>\n")
            oFileWriter.write("<table>\n")
            oFileWriter.write("<script type='text/javascript'>\n")
            oFileWriter.write("window.onload = function () {\n")
            oFileWriter.write("init()\n")
            oFileWriter.write("CanvasJS.addColorSet('chartshades',\n")
            oFileWriter.write("[//colorSet Array\n")
            oFileWriter.write("'lightgreen',\n")
            oFileWriter.write("'red'           \n")
            oFileWriter.write("]);\n")
            oFileWriter.write("var chart = new CanvasJS.Chart('chartContainer',\n")
            oFileWriter.write("{\n")
            oFileWriter.write("colorSet: 'chartshades',\n")
            oFileWriter.write("zoomEnabled: true,\n")
            oFileWriter.write("title:{\n")
            oFileWriter.write("fontColor: '#C6FFEC',\n")
            oFileWriter.write("text: 'Execution Status'\n")
            oFileWriter.write("},\n")
            oFileWriter.write("animationEnabled: true,\n")
            oFileWriter.write("backgroundColor: 'black',\n")
            oFileWriter.write("legend:{\n")
            oFileWriter.write("fontColor: '#C6FFEC',\n")
            oFileWriter.write("verticalAlign: 'bottom',\n")
            oFileWriter.write("horizontalAlign: 'center'\n")
            oFileWriter.write("},data: [{        \n")
            oFileWriter.write("indexLabelFontSize: 20,\n")
            oFileWriter.write("indexLabelFontFamily: 'Monospace',     \n")
            oFileWriter.write("indexLabelFontColor: '#C6FFEC', \n")
            oFileWriter.write("indexLabelLineColor: '#C6FFEC',     \n")
            oFileWriter.write("indexLabelPlacement: 'auto',\n")
            oFileWriter.write("type: 'pie',       \n")
            oFileWriter.write("showInLegend: true,\n")
            oFileWriter.write("toolTipContent: '{y} - <strong>#percent%</strong>',\n")
            oFileWriter.write("dataPoints: [\n")
            if not self.intPassTCCount==0: oFileWriter.write("{  y: "+ str(self.intPassTCCount) + ", legendText:'PASS', indexLabel: '{y}' },\n")
            else: oFileWriter.write("{  y: "+ str(self.intPassTCCount) + ", legendText:'PASS'},\n")
            if not self.intFailTCCount==0: oFileWriter.write("{  y: " + str(self.intFailTCCount) + ", legendText:'FAIL' , indexLabel: '{y}'}\n")
            else: oFileWriter.write("{  y: " + str(self.intFailTCCount) + ", legendText:'FAIL'}\n")
            if self.intFailTCCount > 0: utils.setAttribute_KitBatch('batch_execution', 'current_kit_status', 'FAILED')
            else: utils.setAttribute_KitBatch('batch_execution', 'current_kit_status', 'PASSED')
            oFileWriter.write("]}]});chart.render();}\n")
            oFileWriter.write("</script>\n")
            oFileWriter.write("<script type='text/javascript' src='./Screenshot/canvasjs.min.js'></script>\n")            
            oFileWriter.write("<tr  class='content' ><td><div id='chartContainer' style='height: 300px; width: 100%;'></div></td></tr></table>\n")
            
                      
            oFileWriter.write("<table id='footer'>\n")
            oFileWriter.write("<colgroup>\n")
            oFileWriter.write("<col style='width: 25%' />\n")
            oFileWriter.write("<col style='width: 25%' />\n")
            oFileWriter.write("<col style='width: 25%' />\n")
            oFileWriter.write("<col style='width: 25%' />\n")
            oFileWriter.write("</colgroup>\n")
             
            oFileWriter.write("<tfoot>\n")
            oFileWriter.write("<tr class='heading'>\n")
    
            intExecEndTime = time.monotonic()
            strDuration = str(timedelta(seconds=intExecEndTime - self.intExecStartTime))
            strDuration = self.getDuration(strDuration)
            oFileWriter.write("<th colspan='4'>Total Duration: " + strDuration + "</th>\n")
            utils.setAttribute_KitBatch('batch_execution', 'current_kit_execution_time', strDuration)
            oFileWriter.write("</tr>\n")
            oFileWriter.write("<tr class='subheading'>\n")
            oFileWriter.write("<td class='pass'>&nbsp;Tests passed</td>\n")
            oFileWriter.write("<td class='pass'>&nbsp;: {}</td>\n".format(self.intPassTCCount))
            oFileWriter.write("<td class='fail'>&nbsp;Tests failed</td>\n")
            oFileWriter.write("<td class='fail'>&nbsp;: {}</td>\n".format(self.intFailTCCount))
            oFileWriter.write("</tr>\n")
            oFileWriter.write("</tfoot>\n")
            oFileWriter.write("</table>\n")
            oFileWriter.write("</body>\n")
            oFileWriter.write("</html>\n")
     
            #Always close files.                
            oFileWriter.close()
            
            if os.path.exists(self.strCurrentTXTFolder + 'ExecutionInProgress.txt'): 
                os.remove(self.strCurrentTXTFolder + 'ExecutionInProgress.txt')
        except:
            print('Reporter Exception in HTML_Execution_Summary_Footer \n {0}'.format(traceback.format_exc().replace('File', '$~File')))
            print(self.strExecSummaryHTMLFilePath)


    def create_result_json(self):     
        try:
            self.ResultJsonPath = os.path.abspath(self.strCurrentResFolder+ '/results.json')
            oRJson = open(self.ResultJsonPath, mode='w+')
            
            if "Y" in utils.getAttribute('common', 'secondClientValidateFlag').upper():
                strSecondaryClient = utils.getAttribute('common', 'secondClient')
            else: strSecondaryClient = ""
            
            oJsonDict = {"result_folder": self.strKitResultFolderName, 
                                "kit_details": {},
                                 "list_of_scenarios":{},
                                 "username":utils.getAttribute('common', 'userName'),
                                 "environment":utils.getAttribute('common', 'currentEnvironment'),
                                 "main_client":utils.getAttribute('common', 'mainClient'),
                                 "secondary_client":strSecondaryClient,
                                 "test_start_time_stamp":self.getTimeStamp(False),
                                 "update_time_stamp":self.getTimeStamp(False)}
            
            oRJson.write(json.dumps(oJsonDict, indent=4, sort_keys=False))        
            oRJson.close()
        except:
            print('Reporter Exception in update_scenario_result_json \n {0}'.format(traceback.format_exc().replace('File', '$~File')))
            
    
    def update_result_json_kit_details(self, oKitDetailsDict):
        try:
            oRJson = open(self.ResultJsonPath, mode='r')
            oJsonDict = json.loads(oRJson.read())
            oRJson.close()
            
            oJsonDict["kit_details"] = oKitDetailsDict
            
            #Write back the JSON to the GlobalVar.JSON
            oJson = open(self.ResultJsonPath, mode='w+')
            oJson.write(json.dumps(oJsonDict, indent=4, sort_keys=True))
            oJson.close()
        except:
            print('Reporter Exception in update_scenario_result_json \n {0}'.format(traceback.format_exc().replace('File', '$~File')))
            
        
    def create_scenario_result_json(self):
        try:
            oRJson = open(self.ResultJsonPath, mode='r')
            oJsonDict = json.loads(oRJson.read())
            oRJson.close()
            
            strSCID = "scenario_"+str(self.intScenarioCounter)
            oJsonDict["list_of_scenarios"][strSCID] = {}
            oJsonDict["list_of_scenarios"][strSCID]["id"] = self.strCurrentScenarioID
            oJsonDict["list_of_scenarios"][strSCID]["name"] = self.strCurrentScenarioDesc
            oJsonDict["list_of_scenarios"][strSCID]["status"] = "In-Progress"
            oJsonDict["list_of_scenarios"][strSCID]["error_description"] = ""
            oJsonDict["list_of_scenarios"][strSCID]["iteration"] = 1
            oJsonDict["list_of_scenarios"][strSCID]["pass_counter"] = 0
            oJsonDict["list_of_scenarios"][strSCID]["fail_counter"] = 0
            
            
            #Write back the JSON to the GlobalVar.JSON
            oJson = open(self.ResultJsonPath, mode='w+')
            oJson.write(json.dumps(oJsonDict, indent=4, sort_keys=True))
            oJson.close()
    
        except:
            print('Reporter Exception in update_scenario_result_json \n {0}'.format(traceback.format_exc().replace('File', '$~File')))
            
    def update_scenario_result_json(self, strStatus, errDescription = "" ):
        try:
            oRJson = open(self.ResultJsonPath, mode='r')
            oJsonDict = json.loads(oRJson.read())
            oRJson.close()
            strSCID = "scenario_"+str(self.intScenarioCounter)
            strUpdateStatus = "IN-PROGRESS"
            strPrevStatus = oJsonDict["list_of_scenarios"][strSCID]["status"].upper()
            
            if "COMPLETE" in strStatus.upper():
                if "FAIL" in strPrevStatus: strUpdateStatus = "FAILED"
                else: strUpdateStatus = "COMPLETED"
                
            elif "FAIL" in strStatus.upper(): 
                strUpdateStatus = "FAIL"
            else:
                if "FAIL" in strPrevStatus: strUpdateStatus = strPrevStatus
            
            oJsonDict["list_of_scenarios"][strSCID]["status"] = strUpdateStatus
            
            if not errDescription is "":
                oJsonDict["list_of_scenarios"][strSCID]["error_description"] = ""
            
                
            oJsonDict["list_of_scenarios"][strSCID]["iteration"] = self.intIterationCntr
            oJsonDict["list_of_scenarios"][strSCID]["pass_counter"] = self.intIterationPassCntr
            oJsonDict["list_of_scenarios"][strSCID]["fail_counter"] = self.intIterationFailCntr
            oJsonDict["update_time_stamp"] = self.getTimeStamp(False)
            
            #Write back the JSON to the GlobalVar.JSON
            oJson = open(self.ResultJsonPath, mode='w+')
            oJson.write(json.dumps(oJsonDict, indent=4, sort_keys=True))
            oJson.close()
    
        except:
            print('Reporter Exception in update_scenario_result_json \n {0}'.format(traceback.format_exc().replace('File', '$~File')))
            
if __name__ == '__main__':
    reporter = Reporter()