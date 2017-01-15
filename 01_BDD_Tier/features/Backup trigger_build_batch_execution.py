'''
Created on 8 Sep 2015

@author: ranganathan.veluswamy
'''
from _datetime import timedelta
from datetime import datetime
import json
import os
import subprocess
import time
import traceback

import FF_utils as utils


current_batch_id = ""
global current_batch_id

striOSAppiumConnectionString = "/Applications/Appium.app/Contents/Resources/node/bin/node \
                                                /Applications/Appium.app/Contents/Resources/node_modules/appium/bin/appium.js \
                                                --address 127.0.0.1 --command-timeout \"7200\" --debug-log-spacing \
                                                --no-reset \
                                                 --native-instruments-lib --log-level \"error\""

#Function to execute the batch kits for the Build Pipeline
def build_execute_kitlist():        
    try: 
        oBKitJsonDict = get_kit_batch_json()
        current_batch_id = oBKitJsonDict["kit_batch"]['current_batch_id']
        oKitList = oBKitJsonDict["kit_batch"]['list_of_batches'][current_batch_id]['list_of_kits']
        if len(oKitList.keys()) > 0:
            utils.setAttribute_KitBatch('batch_execution', 'current_batch_result_folder', current_batch_id + '_' + getTimeStamp(True))
            
            
            oKitPriority = {}
            for current_kit_id in oKitList:
                oKitPriority[int(oKitList[current_kit_id]['priority'])] = current_kit_id
                
            for oPKey in sorted(oKitPriority.keys()):
                update_gloabalVar_json(current_batch_id, oKitPriority[oPKey])
                #Trigger the test execution for the Kit
                trigger_test_run()
        else: 
            print('No kits in the Selected batch')
    except:
        print('Batch Execution: Exception in build_execute_kitlist Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))   

#Updated the GlobalVarJson According to the Selected Kit
def update_gloabalVar_json(current_batch_id = None, current_kit_id = None):
    strEnvironmentFolderPAth = os.path.abspath(__file__ + "/../../../") + "/02_Manager_Tier/EnviromentFile/"        
    strGlobVarFilePath = strEnvironmentFolderPAth + '/GlobalVar.json'
    strJson = open(strGlobVarFilePath, mode='r')
    oGBVJsonDict = json.loads(strJson.read())
    strJson.close()
    
    oGlobalDict = oGBVJsonDict['globalVariables']
    if current_batch_id == None or current_kit_id == None: return
    
    if current_batch_id != "" and current_kit_id != "":
        oJsonDict = get_kit_batch_json()
        oKitDetails = oJsonDict["kit_batch"]['list_of_batches'][current_batch_id]['list_of_kits'][current_kit_id]
        oGlobalDict['currentEnvironment'] = oKitDetails['currentEnvironment']
        oGlobalDict['apiValidationType'] = oKitDetails['apiValidationType']
        oGlobalDict['mainClient'] = oKitDetails['mainClient']['name']
        strAppVer = oKitDetails['currentAppVersion']
        oGlobalDict['currentAppVersion'] = strAppVer
        oGlobalDict['userName'] = oKitDetails['userName']
        oGlobalDict['password'] = oKitDetails['password']
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
        
        '''oKitDetails['secondClient'] = {}
        oKitDetails['secondClient']['name'] = MainClient.get()
        oKitDetails['secondClient']['browserName'] = ""
        oKitDetails['secondClient']['loginURL'] = ""
        '''
        oGlobalDict['listOfEnvironments'][oKitDetails['currentEnvironment']] = oCurrentEnvDict
        oGBVJsonDict['globalVariables'] = oGlobalDict
        
        oGlobalDict['test_suite'] = oKitDetails['test_suite']
        #Write back the JSON to the GlobalVar.JSON
        oJson = open(strGlobVarFilePath, mode='w+')
        oJson.write(json.dumps(oGBVJsonDict, indent=4, sort_keys=True))
        oJson.close()
        
def trigger_test_run():
    
    set_global_var()
    if not ('ZIGBEE' in utils.getAttribute("common", 'apiValidationType').upper() or 'WEB' in utils.getAttribute("common", 'mainClient').upper()):
        subprocess.call('killall node', shell=True)               
        subprocess.Popen(striOSAppiumConnectionString, shell=True)
        
    if 'ANDROID' in utils.getAttribute("common", 'mainClient').upper():
        subprocess.call('adb kill-server', shell=True)
        subprocess.call('adb start-server', shell=True) 
        print()
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
            print(output)
    print("@@@@@@@@@@@Successfully completed", output)  
    
def get_kit_batch_json():
    strEnvironmentFolderPAth = os.path.abspath(__file__ + "/../../../") + "/02_Manager_Tier/EnviromentFile/"        
    strGlobVarFilePath = strEnvironmentFolderPAth + '/kit_batch.json'    
    strJson = open(strGlobVarFilePath, mode='r')
    oJsonDict = json.loads(strJson.read())
    strJson.close()
    return oJsonDict

def set_global_var():
    strEnvironmentFolderPAth = os.path.abspath(__file__ + "/../../../") + "/02_Manager_Tier/EnviromentFile"        
    strGlobVarFilePath = strEnvironmentFolderPAth + '/GlobalVar.json'    
    strJson = open(strGlobVarFilePath, mode='r')
    oJsonDict = json.loads(strJson.read())
    strJson.close()    
    utils.oJsonDict = oJsonDict
    
#Gets the Time stamp for creating the folder set or for reporting time stamp based on boolFolderCreate 
def getTimeStamp(boolFolderCreate):
    if boolFolderCreate:
        str_format = "%d-%b-%Y_%H-%M-%S"  
    else:
        str_format = "%d-%b-%Y %H:%M:%S" 
    today = datetime.today()
    return today.strftime(str_format)

#Batch Execution Summary
def Batch_Execution_Summary_Initialize():
    intPassKITCount = 0
    intFailKITCount = 0
    
    strResultsPath = os.path.abspath(__file__ + "/../../../") + '/03_Results_Tier/' + utils.getAttribute_KitBatch('batch_execution', 'current_batch_result_folder') + '/'
    strExecSummaryHTMLFilePath = strResultsPath + "HIVE_BATCH_ Execution_Summary.HTML";
    global strExecSummaryHTMLFilePath
    try:             
        strEnvironmentFilePath = os.path.abspath(__file__ + "/../../../") + "/02_Manager_Tier/EnviromentFile"
        oFileW = open(strEnvironmentFilePath + '/scripts/Temp.txt', 'w')
        oFileW.write(strExecSummaryHTMLFilePath)
        oFileW.close()
        strCSSFilePath = strEnvironmentFilePath + "/Style.CSS"    
        oFileReader = open(strCSSFilePath, 'r')
        oFileWriter = open(strExecSummaryHTMLFilePath, 'x')
        oFileWriter.write("<!DOCTYPE html>\n")
        oFileWriter.write("<html>\n")
        oFileWriter.write("<head>\n")
        oFileWriter.write("         <meta charset='UTF-8'>\n") 
        oFileWriter.write("         <title>Hive - Automation Execution Results Batch-Summary</title>\n") 
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
        oFileWriter.write("Hive - Automation Execution Results Batch-Summary\n") 
        oFileWriter.write("</th>\n") 
        oFileWriter.write("</tr>\n") 
        oFileWriter.write("<tr class='subheading'>\n") 
        oFileWriter.write("<th>&nbsp;Date&nbsp;&&nbsp;Time</th>\n") 
        #oFileWriter.write("<th>&nbsp;:&nbsp;25-Jul-2014&nbsp;05:02:20&nbsp;PM</th>\n")
        oFileWriter.write("<th>&nbsp;:&nbsp;" + getTimeStamp(False) + "</th>\n") 
        intExecStartTime = time.monotonic()
        oFileWriter.write("<th>&nbsp;Batch Name</th>\n") 
        oFileWriter.write("<th>&nbsp;:&nbsp;" + current_batch_id + "</th>\n") 
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
    except IOError as e:
        print("I/O error({0}): {1} in  Batch summary initialize".format(e.errno, e.strerror))
        
        
def HTML_Execution_Summary_TCAddLink(Kit_ID, Main_Client, Second_Client, User_ID, Kit_Setup, Test_Suite):
        
    try:
        oFileWriter = open(strExecSummaryHTMLFilePath, 'a')  
        oFileWriter.write("<tr class='content' >\n")
        oFileDet = os.path.split(utils.getAttribute_KitBatch('batch_execution', 'current_kit_result_summary_path'))
        oFileWriter.write("<td class='justified'><a href='" + './HTML/' + oFileDet[1] + "' target='about_blank'>" + Kit_ID + "</a></td>\n")
        oFileWriter.write("<td class='justified'>" + Main_Client + "</td>\n")
        oFileWriter.write("<td class='justified'>" + Second_Client + "</td>\n")
        oFileWriter.write("<td class='justified'>" + User_ID + "</td>\n")
        oFileWriter.write("<td class='justified'>" + Kit_Setup + "</td>\n")
        oFileWriter.write("<td class='justified'>" + Test_Suite + "</td>\n")
        oFileWriter.write("<td class='justified'>" + utils.getAttribute_KitBatch('batch_execution', 'current_kit_execution_time') + "</td>\n")
        strTCStatus = utils.getAttribute_KitBatch('batch_execution', 'current_kit_status')
        strStatusClass = strTCStatus[0:4].lower()
        oFileWriter.write("<td class='" + strStatusClass + "'>" + strTCStatus + "</td>\n")
        oFileWriter.write("</tr>\n")
 
        '''
        if (self.strTCStatus == "PASSED"): self.intPassTCCount += 1
        if (self.strTCStatus == "FAILED"): self.intFailTCCount += 1
        '''
        #Always close files.                
        oFileWriter.close()
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))

def HTML_Execution_Summary_Footer(self):
            
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
        if not self.intPassTCCount==0: oFileWriter.write("{  y: "+ str(self.intPassTCCount) + ", legendText:'PASS', indexLabel: '{y}' },\n")
        else: oFileWriter.write("{  y: "+ str(self.intPassTCCount) + ", legendText:'PASS'},\n")
        if not self.intFailTCCount==0: oFileWriter.write("{  y: " + str(self.intFailTCCount) + ", legendText:'FAIL' , indexLabel: '{y}'}\n")
        else: oFileWriter.write("{  y: " + str(self.intFailTCCount) + ", legendText:'FAIL'}\n")
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
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
    
        
            

#Build pipeline trigger method
build_execute_kitlist()