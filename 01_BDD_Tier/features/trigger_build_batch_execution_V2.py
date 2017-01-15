'''
Created on 8 Sep 2015

@author: ranganathan.veluswamy
'''
from datetime import datetime
from datetime import timedelta
import getpass
import json
import os
import platform
import socket
import subprocess
import threading
import time
import traceback

from lockfile import LockFile

import FF_alertmeApi as ALAPI
import FF_device_utils as deviceUtils
import FF_utils as utils


striOSAppiumConnectionString = "/Applications/Appium.app/Contents/Resources/node/bin/node \
                                                /Applications/Appium.app/Contents/Resources/node_modules/appium/bin/appium.js \
                                                --address 127.0.0.1 --command-timeout \"7200\" --debug-log-spacing \
                                                --no-reset \
                                                 --native-instruments-lib --log-level \"error\""

jobs = []
strAndroidAppFilePath = '/Users/ranganathan.veluswamy/Downloads/Hive-productV6Internalprod-release-1.2.0.72.apk'
#strAndroidAppFilePath = '/Users/ranganathan.veluswamy/Downloads/Hive-productV6BetaInternalTesters-release-1.2.0.72.apk'
class BatchTrigger():
    
    def __init__(self):
        self.strExecSummaryHTMLFilePath = ""
        self.intPassKITCount = 0
        self.intFailKITCount = 0
        self.lock = None
        
    #Function to execute the batch kits for the Build Pipeline
    def build_execute_kitlist(self):        
        try: 
            strEnvironmentFolderPAth = os.path.abspath(__file__ + "/../../../") + "/02_Manager_Tier/EnviromentFile/"        
            self.strAndroidDeviceJsonFilePath = strEnvironmentFolderPAth + '/android_device_list.json'
            self.lock = LockFile(self.strAndroidDeviceJsonFilePath)
            deviceUtils.create_android_device_json()
            time.sleep(10)
            deviceUtils.install_app_android_device(strAndroidAppFilePath)
            utils.setAttribute_KitBatch('batch_execution', 'status', 'YES')
            oBKitJsonDict = self.get_kit_batch_json()
            self.current_batch_id = oBKitJsonDict["kit_batch"]['current_batch_id']
            oKitList = oBKitJsonDict["kit_batch"]['list_of_batches'][self.current_batch_id]['list_of_kits']
            if len(oKitList.keys()) > 0:
                utils.setAttribute_KitBatch('batch_execution', 'current_batch_result_folder', self.current_batch_id + '_' + self.getTimeStamp(True))
                #Main Summary result
                self.Batch_Execution_Summary_Initialize()
                oKitPriority = {}
                #List Kits based on priority
                for current_kit_id in oKitList:
                    oKitPriority[int(oKitList[current_kit_id]['priority'])] = current_kit_id
                #Trigger the Execution for the kits
                for oPKey in sorted(oKitPriority.keys()):
                    #self.trigger_parallel_kit_execution(oKitPriority[oPKey])
                    # Start the Individual Kit parallel execution
                    
                    parallelExecThread = threading.Thread(target=self.trigger_parallel_kit_execution, args=(oKitPriority[oPKey],))
                    parallelExecThread.daemon = True # This kills the thread when main program exits
                    parallelExecThread.start()
                    parallelExecThread.name = oKitPriority[oPKey]
                    jobs.append(parallelExecThread)
                    time.sleep(50)
                for oJob in jobs:
                    oJob.join()
                #Footer for Batch summary report
                self.Batch_Execution_Summary_Footer()
                
            else: 
                print('No kits in the Selected batch')
            utils.setAttribute_KitBatch('batch_execution', 'status', 'NO')
        except:
            print('Batch Execution: Exception in build_execute_kitlist Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))   
            utils.setAttribute_KitBatch('batch_execution', 'status', 'NO')
    
    def trigger_parallel_kit_execution(self, oKitPkey):
        print("Hello")
        while True:
            boolGotDevice, strDevice, strPort, strDeviceID = self.get_device_from_json()
            print('boolGotDevice, strDevice, strPort ', boolGotDevice, strDevice, strPort )
            if boolGotDevice: break
            else: time.sleep(30)
            
        strResultFolder, User_ID, Test_Suite, Main_Client, Second_Client, strCurrentEnvironment = self.update_gloabalVar_json(self.current_batch_id, oKitPkey, strPort, strDeviceID)
        self.update_main_result_json(oKitPkey, strResultFolder, User_ID, Test_Suite, Main_Client, Second_Client, strCurrentEnvironment)
        
        strHTMLSummaryPath = strResultFolder + "/Hive-" + strCurrentEnvironment + "_Execution_Summary.HTML"
        #Trigger the test execution for the Kit
        #utils.setAttribute('common', 'appium_port', strPort)
        self.trigger_test_run(oKitPkey)
        #Add Hyper link for the Kit execution
        '''Main_Client = utils.getAttribute('common', 'mainClient')
        Second_Client = utils.getAttribute('common', 'secondClient')
        User_ID = utils.getAttribute('common', 'userName')
        Test_Suite = utils.getAttribute('common', 'test_suite')'''
        Kit_Setup = ""
        oDeviceVersionDict = self.get_device_details()
        print(oDeviceVersionDict)
        for oKey in oDeviceVersionDict.keys():
            Kit_Setup = Kit_Setup + oDeviceVersionDict[oKey]['model'] + ' ==> ' + oDeviceVersionDict[oKey]['version']+ '<br>'
        self.Batch_Execution_Summary_KitAddLink(oKitPkey, strHTMLSummaryPath, Main_Client, Second_Client, User_ID, Kit_Setup, Test_Suite)
        self.set_device_exec_status(strDevice, 'COMPLETED')
        
    def get_device_from_json(self):
        strPort = ""
        strDevice = ""
        boolGotDevice = False
        strDeviceID = ""
        try:
            if not self.lock.is_locked():
                self.lock.acquire()
                print(self.lock.path, 'is locked.')
                
                strJson = open(self.strAndroidDeviceJsonFilePath, mode='r')
                oADLJsonDict = json.loads(strJson.read())
                strJson.close()
                oANDLIST = oADLJsonDict['android_devicelist'] 
                for oDevice in oANDLIST:
                    strDeviceExecStatus = oANDLIST[oDevice]['status']
                    if not strDeviceExecStatus.upper()== 'IN PROGRESS':
                        strPort = oANDLIST[oDevice]['port']
                        strDeviceID = oANDLIST[oDevice]['device_id']
                        strDevice = oDevice
                        boolGotDevice = True
                        oANDLIST[oDevice]['status'] = 'IN PROGRESS'
                        oADLJsonDict['android_devicelist'] = oANDLIST
                        #Write back the JSON to the GlobalVar.JSON
                        oJson = open(self.strAndroidDeviceJsonFilePath, mode='w+')
                        oJson.write(json.dumps(oADLJsonDict, indent=4, sort_keys=True))
                        oJson.close()
                        break
                self.lock.release()
                print(self.lock.path, 'is unlocked.')
            return boolGotDevice, strDevice, strPort, strDeviceID
        except:
            print(traceback.format_exc())
            return boolGotDevice, strDevice, strPort, strDeviceID
        
    def set_device_exec_status(self, strDevice, strStatus):
        if not self.lock.is_locked():
            self.lock.acquire()
            print(self.lock.path, 'is locked.')
            strJson = open(self.strAndroidDeviceJsonFilePath, mode='r')
            oADLJsonDict = json.loads(strJson.read())
            strJson.close()
            oANDLIST = oADLJsonDict['android_devicelist'] 
            for oDevice in oANDLIST:
                if oDevice == strDevice:
                    oANDLIST[oDevice]['status'] = strStatus
                    oADLJsonDict['android_devicelist'] = oANDLIST
                    #Write back the JSON to the GlobalVar.JSON
                    oJson = open(self.strAndroidDeviceJsonFilePath, mode='w+')
                    oJson.write(json.dumps(oADLJsonDict, indent=4, sort_keys=True))
                    oJson.close()
        self.lock.release()
        print(self.lock.path, 'is unlocked.')
        
    #Updated the GlobalVarJson According to the Selected Kit
    def update_gloabalVar_json(self, current_batch_id = None, current_kit_id = None, appium_node = '4723', strDeviceID = ""):
        strEnvironmentFolderPAth = os.path.abspath(__file__ + "/../../../") + "/02_Manager_Tier/EnviromentFile/"        
        strGlobVarFilePath = strEnvironmentFolderPAth + '/GlobalVar.json'
        strJson = open(strGlobVarFilePath, mode='r')
        oGBVJsonDict = json.loads(strJson.read())
        strJson.close()
        
        oGlobalDict = oGBVJsonDict['globalVariables']
        if current_batch_id == None or current_kit_id == None: return
        
        if current_batch_id != "" and current_kit_id != "":
            oJsonDict = self.get_kit_batch_json()
            oKitDetails = oJsonDict["kit_batch"]['list_of_batches'][current_batch_id]['list_of_kits'][current_kit_id]
            oGlobalDict['currentEnvironment'] = oKitDetails['currentEnvironment']
            oGlobalDict['apiValidationType'] = oKitDetails['apiValidationType']
            oGlobalDict['mainClient'] = oKitDetails['mainClient']['name']
            oGlobalDict['secondClient'] = oKitDetails['secondClient']['name']
            strAppVer = oKitDetails['currentAppVersion']
            oGlobalDict['currentAppVersion'] = strAppVer
            oGlobalDict['userName'] = oKitDetails['userName']
            oGlobalDict['password'] = oKitDetails['password']
            oGlobalDict['appium_port'] = appium_node
            oGlobalDict['appium_udid'] = strDeviceID
            #Write result folder name
            oGlobalDict['batch_execution'] = {} 
            oGlobalDict['batch_execution']['status'] = "YES"
            strResultFolder = current_kit_id + '_' + oGlobalDict['test_suite'] + '_' + self.getTimeStamp(True) 
            oGlobalDict['batch_execution']['result_folder_name'] = strResultFolder
            print(strResultFolder)
            
            #oKitDetails['resultFolderLabel'] = "" # Environment.get()
            oCurrentEnvDict = oGlobalDict['listOfEnvironments'][oKitDetails['currentEnvironment']]
            
            if 'IOS' in oKitDetails['mainClient']['name'].upper():
                oCurrentEnvDict['iOS' + strAppVer]['appFileName'] = oKitDetails['mainClient']['appFileName']
                oCurrentEnvDict['iOS' + strAppVer]['deviceName'] = oKitDetails['mainClient']['deviceName']
                oCurrentEnvDict['iOS' + strAppVer]['udid'] = oKitDetails['mainClient']['udid']
                oCurrentEnvDict['iOS' + strAppVer]['platformVersion'] = oKitDetails['mainClient']['platformVersion']
            elif 'ANDROID' in oKitDetails['mainClient']['name'].upper():
                oCurrentEnvDict['android' + strAppVer]['appFileName'] = oKitDetails['mainClient']['appFileName']
                oCurrentEnvDict['android' + strAppVer]['deviceName'] = oKitDetails['mainClient']['deviceName']
                oCurrentEnvDict['android' + strAppVer]['platformVersion'] = oKitDetails['mainClient']['platformVersion']
            elif 'WEB' in oKitDetails['mainClient']['name'].upper():
                oCurrentEnvDict['web' + strAppVer]['browserName'] = oKitDetails['mainClient']['browserName']
                oCurrentEnvDict['web' + strAppVer]['loginURL'] = oKitDetails['mainClient']['loginURL']
            
            oGlobalDict['secondClientValidateFlag'] = oKitDetails['secondClientValidateFlag']
            if 'IOS' in oKitDetails['secondClient']['name'].upper():
                oCurrentEnvDict['iOS' + strAppVer]['appFileName'] = oKitDetails['secondClient']['appFileName']
                oCurrentEnvDict['iOS' + strAppVer]['deviceName'] = oKitDetails['secondClient']['deviceName']
                oCurrentEnvDict['iOS' + strAppVer]['udid'] = oKitDetails['secondClient']['udid']
                oCurrentEnvDict['iOS' + strAppVer]['platformVersion'] = oKitDetails['secondClient']['platformVersion']
            elif 'ANDROID' in oKitDetails['secondClient']['name'].upper():
                oCurrentEnvDict['android' + strAppVer]['appFileName'] = oKitDetails['secondClient']['appFileName']
                oCurrentEnvDict['android' + strAppVer]['deviceName'] = oKitDetails['secondClient']['deviceName']
                oCurrentEnvDict['android' + strAppVer]['platformVersion'] = oKitDetails['secondClient']['platformVersion']
            elif 'WEB' in oKitDetails['mainClient']['name'].upper():
                oCurrentEnvDict['web' + strAppVer]['browserName'] = oKitDetails['secondClient']['browserName']
                oCurrentEnvDict['web' + strAppVer]['loginURL'] = oKitDetails['secondClient']['loginURL']
                       
            
            oGlobalDict['listOfEnvironments'][oKitDetails['currentEnvironment']] = oCurrentEnvDict
            oGBVJsonDict['globalVariables'] = oGlobalDict
            
            oGlobalDict['test_suite'] = oKitDetails['test_suite']
            #Write back the JSON to the GlobalVar.JSON
            oJson = open(strGlobVarFilePath, mode='w+')
            oJson.write(json.dumps(oGBVJsonDict, indent=4, sort_keys=True))
            oJson.close()
            
            return strResultFolder, oGlobalDict['userName'], oGlobalDict['test_suite'], oGlobalDict['mainClient'], oGlobalDict['secondClient'], oGlobalDict['currentEnvironment']
    
    def update_main_result_json(self, oKitPkey, strResultFolder, User_ID, Test_Suite, Main_Client, Second_Client, strCurrentEnvironment):
        
        oMRJson = open(self.MainResultJsonPath, mode='r')
        oMRJsonDict = json.loads(oMRJson.read())
        oMRJson.close()
        
        oMRJsonDict["list_of_kits"][oKitPkey] = {"result_folder": strResultFolder,
                                                                    "username": User_ID,
                                                                    "test_suite": Test_Suite,
                                                                    "mainClient":Main_Client,
                                                                    "secondClient":Second_Client,
                                                                    "currentEnvironment": strCurrentEnvironment
                                                                    }
        
        #Write back the JSON to the GlobalVar.JSON
        oMRJson = open(self.MainResultJsonPath, mode='w+')
        oMRJson.write(json.dumps(oMRJsonDict, indent=4, sort_keys=True))
        oMRJson.close()
        
    #Create the Main Results Json
    def create_main_result_json(self):     
        self.MainResultJsonPath = self.BatchResultPath+ '/main_result.json'
        oMRJson = open(self.MainResultJsonPath, mode='w+')
        
        oJsonDict = {"main_result_folder": self.BatchResultPath, 
                            "current_batch_id": self.current_batch_id,
                             "list_of_kits":{}}
        
        oMRJson.write(json.dumps(oJsonDict, indent=4, sort_keys=False))        
        oMRJson.close()
    
    def trigger_test_run(self, strKitID = ""):
        
        self.set_global_var()
        '''if not ('ZIGBEE' in utils.getAttribute("common", 'apiValidationType').upper() or 'WEB' in utils.getAttribute("common", 'mainClient').upper()):
            subprocess.call('killall node', shell=True)               
            subprocess.Popen(striOSAppiumConnectionString, shell=True)'''
            
        '''if 'ANDROID' in utils.getAttribute("common", 'mainClient').upper():
            subprocess.call('adb kill-server', shell=True)
            subprocess.call('adb start-server', shell=True) 
            print()'''
        time.sleep(5)
        strTestSuite = utils.getAttribute("common", 'test_suite')
        if strTestSuite == 'BasicSmokeTest_Dual':
            oProcess = subprocess.Popen("behave --tags=BasicSmokeTest", stdout=subprocess.PIPE, shell=True) 
        elif strTestSuite == 'BasicSmokeTest_Heating':            
            oProcess = subprocess.Popen("behave --tags=BasicSmokeTest --tags=Heating", stdout=subprocess.PIPE, shell=True)        
        elif strTestSuite == 'BasicSmokeTest_HotWater':            
            oProcess = subprocess.Popen("behave --tags=BasicSmokeTest --tags=HotWater", stdout=subprocess.PIPE, shell=True)
        elif strTestSuite == 'ScheduleTest_Dual':
            oProcess = subprocess.Popen("behave --tags=ScheduleTest --tags=Verify", stdout=subprocess.PIPE, shell=True)
        elif strTestSuite == 'ScheduleTest_Heating':
            oProcess = subprocess.Popen("behave --tags=ScheduleTest --tags=Verify --tags=Heating", stdout=subprocess.PIPE, shell=True)
        elif strTestSuite == 'ScheduleTest_HotWater':
            oProcess = subprocess.Popen("behave --tags=ScheduleTest --tags=Verify --tags=HotWater", stdout=subprocess.PIPE, shell=True)
        elif strTestSuite == 'Test_Batch':
            oProcess = subprocess.Popen("behave --tags=Test_Batch", stdout=subprocess.PIPE, shell=True)
        print('Test suite Triggered')
        while True:
            output = oProcess.stdout.readline()
            if oProcess.poll() is not None:
                break
            if output:
                print(strKitID, output)
        print("@@@@@@@@@@@Successfully completed", strKitID, output)  
        
    def get_kit_batch_json(self):
        strEnvironmentFolderPAth = os.path.abspath(__file__ + "/../../../") + "/02_Manager_Tier/EnviromentFile/"        
        strGlobVarFilePath = strEnvironmentFolderPAth + '/kit_batch.json'    
        strJson = open(strGlobVarFilePath, mode='r')
        oJsonDict = json.loads(strJson.read())
        strJson.close()
        return oJsonDict 
    
    def set_global_var(self):
        strEnvironmentFolderPAth = os.path.abspath(__file__ + "/../../../") + "/02_Manager_Tier/EnviromentFile"        
        strGlobVarFilePath = strEnvironmentFolderPAth + '/GlobalVar.json'    
        strJson = open(strGlobVarFilePath, mode='r')
        oJsonDict = json.loads(strJson.read())
        strJson.close()    
        utils.oJsonDict = oJsonDict
        
    #Gets the Time stamp for creating the folder set or for reporting time stamp based on boolFolderCreate 
    def getTimeStamp(self, boolFolderCreate):
        if boolFolderCreate:
            str_format = "%d-%b-%Y_%H-%M-%S"  
        else:
            str_format = "%d-%b-%Y %H:%M:%S" 
        today = datetime.today()
        return today.strftime(str_format)


    #Batch Execution Summary
    def Batch_Execution_Summary_Initialize(self):
        strAPI = utils.getAttribute('common', 'apiValidationType')
        if 'ZIGBEE' in strAPI.upper():
            strAPIFolder = 'Device_Test_Automation/'
        else: strAPIFolder = 'Web-Mobile_Test_Automation'
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
        else: self.strResultsPath = os.path.abspath(__file__ + "/../../../") + '/03_Results_Tier/'
        strResultsPath = self.strResultsPath + utils.getAttribute_KitBatch('batch_execution', 'current_batch_result_folder') + '/'
        if not os.path.exists(strResultsPath):os.makedirs(strResultsPath)
        self.BatchResultPath = strResultsPath
        self.strExecSummaryHTMLFilePath = strResultsPath + "HIVE_BATCH_Execution_Summary.HTML"
        print(self.strExecSummaryHTMLFilePath)
        self.create_main_result_json()
        try:             
            strEnvironmentFilePath = os.path.abspath(__file__ + "/../../../") + "/02_Manager_Tier/EnviromentFile"
            oFileW = open(strEnvironmentFilePath + '/scripts/Temp.txt', 'w')
            oFileW.write(self.strExecSummaryHTMLFilePath)
            oFileW.close()
            strCSSFilePath = strEnvironmentFilePath + "/Style.CSS"    
            oFileReader = open(strCSSFilePath, 'r')
            strData = oFileReader.read()
            oFileReader.close()
            oFileWriter = open(self.strExecSummaryHTMLFilePath, 'w')
            oFileWriter.write("<!DOCTYPE html>\n")
            oFileWriter.write("<html>\n")
            oFileWriter.write("<head>\n")
            oFileWriter.write("         <meta charset='UTF-8'>\n") 
            oFileWriter.write("         <title>Hive - Automation Execution Results Batch-Summary</title>\n") 
            oFileWriter.write(strData + '\n')
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
            oFileWriter.write("Hive - Automation Execution Results Batch-Summary\n") 
            oFileWriter.write("</th>\n") 
            oFileWriter.write("</tr>\n") 
            oFileWriter.write("<tr class='subheading'>\n") 
            oFileWriter.write("<th>&nbsp;Date&nbsp;&&nbsp;Time</th>\n") 
            #oFileWriter.write("<th>&nbsp;:&nbsp;25-Jul-2014&nbsp;05:02:20&nbsp;PM</th>\n")
            oFileWriter.write("<th>&nbsp;:&nbsp;" + self.getTimeStamp(False) + "</th>\n") 
            self.intExecStartTime = time.monotonic()
            oFileWriter.write("<th>&nbsp;Batch Name</th>\n") 
            oFileWriter.write("<th>&nbsp;:&nbsp;" + self.current_batch_id + "</th>\n") 
            oFileWriter.write("</tr>\n") 
            oFileWriter.write("</thead>\n") 
            oFileWriter.write("</table>\n") 
            oFileWriter.write("<table id='main'>\n")
            oFileWriter.write("<colgroup>\n")
            oFileWriter.write("<col style='width: 10%' />\n")
            oFileWriter.write("<col style='width: 10%' />\n") 
            oFileWriter.write("<col style='width: 10%' />\n")
            oFileWriter.write("<col style='width: 15%' />\n") 
            oFileWriter.write("<col style='width: 15%' />\n") 
            oFileWriter.write("<col style='width: 15%' />\n") 
            oFileWriter.write("<col style='width: 15%' />\n") 
            oFileWriter.write("<col style='width: 10%' />\n") 
            oFileWriter.write("</colgroup>\n") 
             
            oFileWriter.write("<thead>\n") 
            oFileWriter.write("<tr class='heading'>\n") 
            oFileWriter.write("<th>Kit_ID</th>\n") 
            oFileWriter.write("<th>Main_Client</th>\n") 
            oFileWriter.write("<th>Second_Client</th>\n") 
            oFileWriter.write("<th>User_ID</th>\n") 
            oFileWriter.write("<th>Kit_Setup</th>\n") 
            oFileWriter.write("<th>Test_Suite</th>\n") 
            oFileWriter.write("<th>Execution_Time</th>\n") 
            oFileWriter.write("<th>Status</th>\n") 
            oFileWriter.write("</tr>\n") 
            oFileWriter.write("</thead>\n")
     
            #Always close files.    
            oFileWriter.close()
        except:
            print('Reporter Exception in BATCH_HTML_Execution_Summary_Initialize\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
            
            
    def Batch_Execution_Summary_KitAddLink(self, Kit_ID,strHTMLSummaryPath, Main_Client, Second_Client, User_ID, Kit_Setup, Test_Suite):
        try:
            oFileWriter = open(self.strExecSummaryHTMLFilePath, 'a')
            oFileWriter.write("<tr class='content' >\n")
            #oFileDet = os.path.split(utils.getAttribute_KitBatch('batch_execution', 'current_kit_result_summary_path'))
            #strFilePath = utils.getAttribute_KitBatch('batch_execution', 'current_kit_result_summary_path')
            oFileWriter.write("<td class='justified'><a href='" + './Kit_Results/' + strHTMLSummaryPath + "' target='about_blank'>" + str(Kit_ID) + "</a></td>\n")
            oFileWriter.write("<td class='justified'>" + Main_Client + "</td>\n")
            oFileWriter.write("<td class='justified'>" + Second_Client + "</td>\n")
            oFileWriter.write("<td class='justified'>" + User_ID + "</td>\n")
            oFileWriter.write("<td class='justified'>" + Kit_Setup + "</td>\n")
            oFileWriter.write("<td class='justified'>" + Test_Suite + "</td>\n")
            oFileWriter.write("<td class='justified'>" + utils.getAttribute_KitBatch('batch_execution', 'current_kit_execution_time') + "</td>\n")
            self.strKitStatus = utils.getAttribute_KitBatch('batch_execution', 'current_kit_status')
            strStatusClass = self.strKitStatus[0:4].lower()
            oFileWriter.write("<td class='" + strStatusClass + "'>" + self.strKitStatus + "</td>\n")
            oFileWriter.write("</tr>\n")
            if (self.strKitStatus == "PASSED"): self.intPassKITCount = self.intPassKITCount + 1
            if (self.strKitStatus == "FAILED"): self.intFailKITCount = self.intFailKITCount + 1
           
            #Always close files.                
            oFileWriter.close()
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
    
    def Batch_Execution_Summary_Footer(self):
                
        try:
            oFileWriter = open(self.strExecSummaryHTMLFilePath, 'a')  
            oFileWriter.write("</tbody>\n")
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
            if not self.intPassKITCount==0: oFileWriter.write("{  y: "+ str(self.intPassKITCount) + ", legendText:'PASS', indexLabel: '{y}' },\n")
            else: oFileWriter.write("{  y: "+ str(self.intPassKITCount) + ", legendText:'PASS'},\n")
            if not self.intFailKITCount==0: oFileWriter.write("{  y: " + str(self.intFailKITCount) + ", legendText:'FAIL' , indexLabel: '{y}'}\n")
            else: oFileWriter.write("{  y: " + str(self.intFailKITCount) + ", legendText:'FAIL'}\n")
            oFileWriter.write("]}]});chart.render();}\n")
            oFileWriter.write("</script>\n")
            oFileWriter.write("<script type='text/javascript' src='./Kit_Results/Temp/canvasjs.min.js'></script>\n")            
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
            oFileWriter.write("</tr>\n")
            oFileWriter.write("<tr class='subheading'>\n")
            oFileWriter.write("<td class='pass'>&nbsp;Tests passed</td>\n")
            oFileWriter.write("<td class='pass'>&nbsp;: {}</td>\n".format(self.intPassKITCount))
            oFileWriter.write("<td class='fail'>&nbsp;Tests failed</td>\n")
            oFileWriter.write("<td class='fail'>&nbsp;: {}</td>\n".format(self.intFailKITCount))
            oFileWriter.write("</tr>\n")
            oFileWriter.write("</tfoot>\n")
            oFileWriter.write("</table>\n")
            oFileWriter.write("</body>\n")
            oFileWriter.write("</html>\n")
     
            #Always close files.                
            oFileWriter.close()
            '''
            if os.path.exists(self.strCurrentTXTFolder + 'ExecutionInProgress.txt'): 
                os.remove(self.strCurrentTXTFolder + 'ExecutionInProgress.txt')'''
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
        
    def get_connectedAndroid_device(self):
        print()
    def get_device_details(self):
        env = utils.getAttribute('common', 'currentEnvironment')
        username = utils.getAttribute('common', 'userName')
        password = utils.getAttribute('common', 'password')
        ALAPI.createCredentials(env, username = username, password = password)
        self.session = ALAPI.sessionObject()
        resp = ALAPI.getNodesV6(self.session)
        oDeviceVersionDict = {}
        strSLTMacID = ""
        strSLRMacID = ""
        for oNode in resp['nodes']:
            if not 'supportsHotWater'  in oNode['attributes']:
                if 'hardwareVersion' in oNode['attributes']: 
                    intHardwareVersion = oNode['attributes']['hardwareVersion']['reportedValue']
                    intSoftwareVersion = oNode['attributes']['softwareVersion']['reportedValue']
                    if 'NANO' in  intHardwareVersion:
                        oDeviceVersionDict['HUB'] = {"model" : intHardwareVersion, "version" : intSoftwareVersion}
                if 'zigBeeNeighbourTable' in oNode['attributes']:
                    for oDevice in oNode['attributes']['zigBeeNeighbourTable']['reportedValue']:
                        if 'relationship' in oDevice:
                            if oDevice['relationship'] == 'CHILD':
                                strSLTMacID = oDevice['neighbourAddress']
                            elif oDevice['relationship'] == 'NONE':
                                strSLRMacID = oDevice['neighbourAddress']
                                
        for oNode in resp['nodes']:
            if not 'supportsHotWater'  in oNode['attributes']:
                if 'model' in oNode['attributes']: 
                    strModel = oNode['attributes']['model']['reportedValue']
                    intSoftwareVersion = oNode['attributes']['softwareVersion']['reportedValue']                            
                    if 'SLT' in strModel: 
                        oDeviceVersionDict['Thermostat'] = {"model" : strModel, "version" : intSoftwareVersion, 'mac_id': strSLTMacID}
                    elif'SLR' in strModel: 
                        oDeviceVersionDict['Boiler Module'] = {"model" : strModel, "version" : intSoftwareVersion, 'mac_id': strSLRMacID}
        return oDeviceVersionDict
    
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
    
    #Ensures the dirPath exists, if not creates the same
    def ensure_dir(self, dirpath):
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        return dirpath
    
    
#Build pipeline trigger method
oBatEx = BatchTrigger()
oBatEx.build_execute_kitlist()