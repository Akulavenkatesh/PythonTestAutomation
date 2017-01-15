import json
import ntpath
import os
import shutil
import subprocess
from sys import executable
import time
from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Style
import traceback
import webbrowser

sys.path.append("steps")
sys.path.append("steps/PageObjects")
sys.path.append("steps/Locators")
sys.path.append("steps/Function_Libraries")

import FF_utils as utils
import FF_device_utils as dUtils
import FF_alertmeApi as ALAPI
from tkinter.messagebox import showinfo


UDID = "8d25ba7d4a8f82f1a32cc35d907ad2a928b6e808"
DEVICE_NAME = "iPhone"
striOSAppiumConnectionString = "/Applications/Appium.app/Contents/Resources/node/bin/node \
                                                /Applications/Appium.app/Contents/Resources/node_modules/appium/bin/appium.js \
                                                --address 127.0.0.1 --command-timeout \"7200\" --debug-log-spacing \
                                                --platform-version \"8.4\" --platform-name \"iOS\" --app \"uk.co.britishgas.hive\" \
                                                --udid \" " + UDID + "\" --no-reset \
                                                --device-name \"" +  DEVICE_NAME + "\" --native-instruments-lib --log-level \"error\""

striOSAppiumConnectionString = "/Applications/Appium.app/Contents/Resources/node/bin/node \
                                                /Applications/Appium.app/Contents/Resources/node_modules/appium/bin/appium.js \
                                                --address 127.0.0.1 --command-timeout \"7200\" --debug-log-spacing \
                                                --udid \" " + UDID + "\" --no-reset \
                                                 --native-instruments-lib --log-level \"error\""

striOSAppiumConnectionString = "/Applications/Appium.app/Contents/Resources/node/bin/node \
                                                /Applications/Appium.app/Contents/Resources/node_modules/appium/bin/appium.js \
                                                --address 127.0.0.1 --command-timeout \"7200\" --debug-log-spacing \
                                                --no-reset \
                                                 --native-instruments-lib --log-level \"error\""



class UIClass(Frame):
    
        
    
    def __init__(self, parent):
        self.set_global_var()
        self.window = parent
        parent.title("Hive Test Automation - Select Config Variables")
        #parent.configure(background='black')
        self.position_window(parent,w=560, h=330)
        self.window.minsize(width=660, height=330)
        Frame.__init__(self, parent)
        
        #Style - Background color
        s = ttk.Style()
        s.configure('.', background='white')
        ttk.Style().configure("TButton", padding=6, relief="flat", bg='#000000',
                fg='#b7f731',background="pale green")
        
        #Frame
        self.mainframe = ttk.Frame(self, padding="50 10 50 50")
        self.mainframe.configure(style='TFrame')
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        
        #Variables
        self.Environment = StringVar()
        self.APIValidation = StringVar()
        self.MainClient = StringVar()
        self.UserName = StringVar()
        self.Password = StringVar()
        self.TestSuite = StringVar()
        self.AppVersion = StringVar()
        self.ATNode = StringVar()
        self.OSVersion = StringVar()
        self.AppFilePath = StringVar()
        self.DeviceName = StringVar()
        self.UDID = StringVar()
        self.BrowserName = StringVar()
        self.URL = StringVar()
        
        self.boolAppFieldDestroyed = True
        self.boolUDIDFieldDestroyed = True
        self.boolZigbeeFieldDestroyed = True
        self.boolUserPassDestroyed = True
        self.boolWebFieldDestroyed = True
        
        self.appHighlightFont = font.Font(family='Helvetica', size=22, weight='bold')
        ttk.Label(self.mainframe, text='Hive Device /', font=self.appHighlightFont).grid(column=3, row=0, sticky=E)
        ttk.Label(self.mainframe, text='Client Test Automation', font=self.appHighlightFont).grid(column=15, row=0, sticky=W)
        
        #Environment
        ttk.Label(self.mainframe, text='Environment:    ').grid(column=3, row=1, sticky=E)
        self.oEnvironment = ttk.Combobox(self.mainframe, textvariable=self.Environment)
        self.oEnvironment['values'] = ('isopInternProd', 'isopBeta', 'isopStaging', 'isopProd')
        self.oEnvironment.bind('<<ComboboxSelected>>', self.api_selected_item_event)
        self.oEnvironment.state(['readonly'])
        self.oEnvironment.set(utils.getAttribute('common', 'currentEnvironment'))
        self.oEnvironment.grid(column=15, row=1, sticky=W)
        
        #API Validation
        ttk.Label(self.mainframe, text='API Validation:    ').grid(column=3, row=2, sticky=E)
        self.oAPIValidation = ttk.Combobox(self.mainframe, textvariable=self.APIValidation)
        self.oAPIValidation['values'] = ('Platform API', 'Zigbee API')
        self.oAPIValidation.bind('<<ComboboxSelected>>', self.api_selected_item_event)
        self.oAPIValidation.state(['readonly'])
        self.oAPIValidation.set(utils.getAttribute('common', 'apiValidationType'))
        self.oAPIValidation.grid(column=15, row=2, sticky=W)
        #Main Client
        self.lblMainClient = ttk.Label(self.mainframe, text='Main Client:    ')
        self.lblMainClient.grid(column=3, row=3, sticky=E)
        self.oMainClient = ttk.Combobox(self.mainframe, textvariable=self.MainClient)
        self.oMainClient['values'] = ('Android App', 'iOS App', 'Web App')
        self.oMainClient.bind('<<ComboboxSelected>>', self.load_app_details)
        self.oMainClient.state(['readonly'])
        self.oMainClient.set(utils.getAttribute('common', 'mainClient'))
        self.oMainClient.grid(column=15, row=3, sticky=W)
        #if 'Platform' in self.APIValidation.get(): 
        #self.load_platformAPI_controls()
        self.api_selected_item_event(None)
        #TestSuite
        '''
        oTestSuiteList = []
        strFeatureFolder = os.path.abspath(__file__ + "/../") 
        for strFile in os.listdir(strFeatureFolder):    
            if 'TS_' in strFile:
                oTestSuiteList.append(strFile)
        oTestSuiteList = tuple(oTestSuiteList)     
        '''   
        oTestSuiteList = ('BasicSmokeTest_Dual', 'BasicSmokeTest_Heating', 'BasicSmokeTest_HotWater', 'ScheduleTest_Dual', 'ScheduleTest_Heating', 'ScheduleTest_HotWater', 'Kings'  )
        # oTestSuiteList = ('SP_AllTest','SP_AllChannelPairingTest', 'SP_PairingTest', 'SP_ZigbeeDumpTest', 'SP_On-OffTest', 'SP_Upgrade-Downgrade')
        ttk.Label(self.mainframe, text='Test Suite:    ').grid(column=3, row=13, sticky=E)
        oTestSuite= ttk.Combobox(self.mainframe, textvariable=self.TestSuite, width = 30)
        oTestSuite['values'] = oTestSuiteList
        if len(oTestSuiteList) > 0: oTestSuite.set(oTestSuiteList[0])
        oTestSuite.grid(column=15, row=13, sticky=W)        
        
        #Exucute & Quit Buttons
        ttk.Label(self.mainframe, text='').grid(column=3, row=14, sticky=E)
        ttk.Label(self.mainframe, text='').grid(column=15, row=14, sticky=E)
        oExecute = ttk.Button(self.mainframe, text='Execute', command=self.updateGlobalVarJson)
        oExecute.grid(column=15, row=15, sticky=W)       
        oExecute = ttk.Button(self.mainframe, text='Quit', command=self.closeWidget)
        oExecute.grid(column=15, row=15, sticky=E)
        oExecute = ttk.Button(self.mainframe, text='Result', command=self.showResults)
        oExecute.grid(column=15, row=15)
        
    #Launch the Result Summary HTML
    def showResults(self):           
        try:
            strTempFile = os.path.abspath(__file__ + "/../../../") + "/02_Manager_Tier/EnviromentFile/scripts/Temp.txt" 
            oReader = open(strTempFile, 'r')
            oHTMLSummaryPath = 'file://' + oReader.read()
            webbrowser.open(oHTMLSummaryPath,new=2)
        except: print(traceback.format_exc())
        
    #Place Window on the center fo the screen
    def position_window(self, parent, w, h):
        # get screen width and height
        ws = parent.winfo_screenwidth()
        hs = parent.winfo_screenheight()
        # calculate position x, y
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        parent.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
    def load_platformAPI_controls(self):
        if 'Platform' in self.APIValidation.get():
            self.position_window(self.window, w=560, h=330)
            try:
                self.lblZigbeeEPNOde.destroy()
                self.oATNode.destroy()
                self.boolZigbeeFieldDestroyed = True
            except: pass
            
            
           
            oPlatClientTuple = ('Android App', 'iOS App', 'Web App')
            self.oMainClient['values'] = oPlatClientTuple
            strMainClient = utils.getAttribute('common', 'mainClient')
            if strMainClient not in oPlatClientTuple: 
                strMainClient = 'Android App'
                self.oMainClient.set(strMainClient)
                self.load_app_details(None)
            else: self.oMainClient.set(strMainClient)
            if self.boolUserPassDestroyed: 
                #App Version
                self.lblAppversion = ttk.Label(self.mainframe, text='App Version:    ')
                self.lblAppversion.grid(column=3, row=4, sticky=E)
                self.oAppVersion = ttk.Combobox(self.mainframe, textvariable=self.AppVersion)
                self.oAppVersion.bind('<<ComboboxSelected>>', self.load_app_details)
                self.oAppVersion['values'] = ('V6', 'V5')
                self.oAppVersion.state(['readonly'])
                self.oAppVersion.set(utils.getAttribute('common', 'currentAppVersion'))
                self.oAppVersion.grid(column=15, row=4, sticky=W)
                
                #User Name
                self.lblUserName = ttk.Label(self.mainframe, text='User Name:    ')
                self.lblUserName.grid(column=3, row=11, sticky=E)
                self.oUserName = ttk.Combobox(self.mainframe, textvariable=self.UserName)
                self.oUserName['values'] = ('auto1_v6', 'tester2', 'tester4_v6')
                self.oUserName.set(utils.getAttribute('common', 'userName'))
                self.oUserName.grid(column=15, row=11, sticky=W)
                
                #Password
                self.lblPassword = ttk.Label(self.mainframe, text='Password:    ')
                self.lblPassword.grid(column=3, row=12, sticky=E)
                self.oPassword = ttk.Combobox(self.mainframe, textvariable=self.Password)
                self.oPassword['values'] = ('password1', 'Password1', 'passw0rd')
                self.oPassword.set(utils.getAttribute('common', 'password'))
                self.oPassword.grid(column=15, row=12, sticky=W)
                self.boolUserPassDestroyed = False
        else:
            #Set Main client for ZigBee API validation
            oDeviceList =list(dUtils.getNodes(False).keys())
            if 'TGStick' in oDeviceList: oDeviceList.remove('TGStick')
            print(tuple(oDeviceList))
            if oDeviceList is []:oDeviceList = ['']
            self.oMainClient['values'] = tuple(oDeviceList)
            self.lblMainClient['text'] = 'Devices:    '
            if len(oDeviceList) >0: self.oMainClient.current(0)
            else: self.oMainClient.set("")
            #Destroy platform API fields
            try:
                self.oBrowse.destroy()
                self.lblAppversion.destroy()
                self.lblUserName.destroy()
                self.lblPassword.destroy()
                self.oAppVersion.destroy()
                self.oAppFilePath.destroy()
                self.oOSVersion.destroy()
                self.oDeviceName.destroy()
                self.oUDID.destroy()
                self.lblAppFileName.destroy()
                self.lblOSVersion.destroy()
                self.lblDeviceName.destroy()
                self.lblUDID.destroy()
                self.boolAppFieldDestroyed = True                
                self.boolUDIDFieldDestroyed = True
                self.boolUserPassDestroyed = True
                self.boolWebFieldDestroyed = True
                self.oUserName.destroy()
                self.oPassword.destroy()
                self.lblURL.destroy()
                self.oURL.destroy()
                self.lblBrowserName.destroy()
                self.oBrowserName.destroy()
            except: pass
            
            #Zigbee EP Node ID
            if self.boolZigbeeFieldDestroyed:
                self.lblZigbeeEPNOde = ttk.Label(self.mainframe, text='NodeID _ MacID:    ')
                self.lblZigbeeEPNOde.grid(column=3, row=4, sticky=E)
                self.oATNode = ttk.Combobox(self.mainframe, textvariable=self.ATNode)
                self.oATNode.set(utils.getAttribute('common', 'atZigbeeNode'))
                self.oATNode.grid(column=15, row=4, sticky=W)
                self.position_window(self.window, w=490, h=290)
                self.boolZigbeeFieldDestroyed = False
                    
    def load_app_details(self, event):
        if not 'Platform' in self.APIValidation.get(): 
            oDeviceNode = dUtils.getDeviceNode(self.MainClient.get(), False)
            if not oDeviceNode is '': self.oATNode.set(oDeviceNode['nodeID'] + '_' + oDeviceNode['macID'])
            else: self.oATNode.set('')
            return False
            
        print(self.MainClient.get().upper())
        if self.AppVersion.get() is '': strAppVer = utils.getAttribute('common', 'currentAppVersion')
        else: strAppVer = self.AppVersion.get()
        print('strAppVer', strAppVer)
        if 'WEB' in self.MainClient.get().upper():
            self.position_window(self.window, w=490, h=380)
            print('im in')
            try:
                self.oBrowse.destroy()
                self.oAppFilePath.destroy()
                self.oOSVersion.destroy()
                self.oDeviceName.destroy()
                self.oUDID.destroy()
                self.lblAppFileName.destroy()
                self.lblOSVersion.destroy()
                self.lblDeviceName.destroy()
                self.lblUDID.destroy()
                self.boolAppFieldDestroyed = True                
                self.boolUDIDFieldDestroyed = True
                print('Killed for web')
            except: pass
            if self.boolWebFieldDestroyed:
                #Browser Name
                self.lblBrowserName, self.oBrowserName = self.create_combobox(5, '     Browser Name:    ', self.BrowserName, (), "", False)    
                self.oBrowserName['values'] = ('Firefox', 'Chrome', 'Safari')
                self.oBrowserName.set(utils.getAttribute('web', 'browserName', strAppVer))
                #URL
                self.lblURL, self.oURL = self.create_combobox(6, 'Web URL:    ', self.URL, (), "", False)
                self.oURL.set(utils.getAttribute('web', 'loginURL', strAppVer))
                self.boolWebFieldDestroyed = False
        else:    
            try:
                self.lblURL.destroy()
                self.oURL.destroy()
                self.lblBrowserName.destroy()
                self.oBrowserName.destroy()
                self.boolWebFieldDestroyed = True
                print('killed for Mobile')
            except: pass
            
            if self.boolAppFieldDestroyed:
                #AppFilePath
                self.lblAppFileName, self.oAppFilePath = self.create_combobox(5, 'App File Name:    ', self.AppFilePath, (), "", False)  
                self.oAppFilePath.configure(width = 30)
                self.oBrowse = ttk.Button(self.mainframe, text='...', width = 2, command=self.browse_app_file)
                self.oBrowse.grid(column=17, row=5, sticky=W)          
                #OS platform version
                self.lblOSVersion, self.oOSVersion = self.create_combobox(6, 'Mobile OS Version:    ', self.OSVersion, (), "", False)        
                #Device Name             
                self.lblDeviceName, self.oDeviceName = self.create_combobox(7, 'Device Name:    ', self.DeviceName, (), "", False)  
                self.boolAppFieldDestroyed = False
            
            if self.boolUDIDFieldDestroyed:      
                #UDID
                self.lblUDID, self.oUDID = self.create_combobox(9, 'UDID:    ', self.UDID, (), "", False)
                self.oUDID.configure(width = 30)
                self.boolUDIDFieldDestroyed = False
            if 'IOS' in self.MainClient.get().upper():
                self.position_window(self.window, w=560, h=430)
                strFilePath = utils.getAttribute(self.MainClient.get().split()[0], 'appFileName')
                self.load_app_filename(strFilePath)
                self.oOSVersion['values'] = ('8.4', '8.2', '8.3', '8.1')
                self.oOSVersion.set(utils.getAttribute('iOS', 'platformVersion', strAppVer))
                self.oDeviceName.set(utils.getAttribute('iOS', 'deviceName', strAppVer))
                self.oUDID.set(utils.getAttribute('iOS', 'udid'))
                
            elif 'ANDROID' in self.MainClient.get().upper():
                self.position_window(self.window, w=560, h=410)
                strFilePath = utils.getAttribute(self.MainClient.get().split()[0].lower(), 'appFileName')
                self.load_app_filename(strFilePath)
                self.oOSVersion['values'] = ('5.1', '5.0', '4.4', '4.3')
                self.oOSVersion.set(utils.getAttribute('android', 'platformVersion', strAppVer))
                self.oDeviceName.set(utils.getAttribute('android', 'deviceName', strAppVer))
                self.oUDID.destroy()
                self.lblUDID.destroy()                
                self.boolUDIDFieldDestroyed = True
            
        
    def load_app_filename(self, strFilePath):    
        if self.MainClient.get().split()[0] == 'Android' : oAppExt = ("APK", "*.apk")
        else: oAppExt = ("APP", "*.app")
        strAPPFolderPAth = os.path.abspath(__file__ + "/../../../") + "/02_Manager_Tier/EnviromentFile/Apps/" + self.MainClient.get().split()[0] + '/' + self.Environment.get().split()[0]
        
        strFileName = ntpath.split(strFilePath)[1]
        oAppFileList = []
        oAllFileList = os.listdir(strAPPFolderPAth)
        for strFile in oAllFileList:    
            if os.path.splitext(strFile)[1].upper() == '.' + oAppExt[0]:
                oAppFileList.append(strFile)
        oAppFileTuple = tuple(oAppFileList)
        self.oAppFilePath['value'] = oAppFileTuple
        self.oAppFilePath.set(strFileName)
            
    def create_combobox(self, intRow, strLabel, oStringVar, oValueList, strDefaultValue, boolReadOnly):                
        oLabel = ttk.Label(self.mainframe, text=strLabel)
        oLabel.grid(column=3, row=intRow, sticky=E)
        oCombobox = ttk.Combobox(self.mainframe, textvariable=oStringVar)
        oCombobox['values'] = oValueList
        oCombobox.set(strDefaultValue)                
        if boolReadOnly: oCombobox.state(['readonly'])
        oCombobox.grid(column=15, row=intRow, sticky=W)
        return oLabel, oCombobox
   
    def closeWidget(self):
        exit()
        '''about_message =' suuper'
        top = Toplevel()
        top.title("View Test Results")
        self.position_window(top,w=200, h=330)
        msg = Message(top, text=about_message)
        msg.pack()
        
        button = Button(top, text="Dismiss", command=top.destroy)
        button.pack()'''
    
    def updateGlobalVarJson(self):
        #Reading all data from GlobalVar.Json
        if 'APP' in self.MainClient.get().upper() :
            ALAPI.createCredentials(self.Environment.get(), username = self.UserName.get(), password = self.Password.get())
            self.session = ALAPI.sessionObject()
            if self.session.statusCode != 200:
                resp =self.session.response
                if isinstance(resp, str): resp = json.loads(resp)
                showinfo('ERROR', resp)
                return
        
        strEnvironmentFolderPAth = os.path.abspath(__file__ + "/../../../") + "/02_Manager_Tier/EnviromentFile/"        
        strGlobVarFilePath = strEnvironmentFolderPAth + '/GlobalVar.json'    
        strJson = open(strGlobVarFilePath, mode='r')
        oJsonDict = json.loads(strJson.read())
        strJson.close()
        
        oGlobalDict = oJsonDict['globalVariables']
        #updating the json Dictionary based on the the input parameter selected on the GUI
        oGlobalDict['currentEnvironment'] = self.Environment.get()
        oGlobalDict['apiValidationType'] = self.APIValidation.get()
        oGlobalDict['mainClient'] = self.MainClient.get()
        
        oCurrentEnvDict = oGlobalDict['listOfEnvironments'][self.Environment.get()]
        if 'ZIGBEE' in self.APIValidation.get().upper():
            oGlobalDict['atZigbeeNode'] = self.ATNode.get()
        else:
            strAppVer = self.AppVersion.get()
            oGlobalDict['currentAppVersion']= self.AppVersion.get()
            oGlobalDict['userName']= self.UserName.get()
            oGlobalDict['password']= self.Password.get()
            
            if 'IOS' in self.MainClient.get().upper():
                oCurrentEnvDict['iOS' + strAppVer]['appFileName'] = self.AppFilePath.get()
                oCurrentEnvDict['iOS' + strAppVer]['platformVersion'] = self.OSVersion.get()
                oCurrentEnvDict['iOS' + strAppVer]['deviceName'] = self.DeviceName.get()
                oCurrentEnvDict['iOS' + strAppVer]['udid'] = self.UDID.get()
            elif 'ANDROID' in self.MainClient.get().upper():                
                oCurrentEnvDict['android' + strAppVer]['appFileName'] = self.AppFilePath.get()
                oCurrentEnvDict['android' + strAppVer]['platformVersion'] = self.OSVersion.get()
                oCurrentEnvDict['android' + strAppVer]['deviceName'] = self.DeviceName.get()
            elif 'WEB' in self.MainClient.get().upper():                
                oCurrentEnvDict['web' + strAppVer]['browserName'] = self.BrowserName.get()
                oCurrentEnvDict['web' + strAppVer]['loginURL'] = self.URL.get()
            
        oGlobalDict['listOfEnvironments'][self.Environment.get()] = oCurrentEnvDict
        oJsonDict['globalVariables'] = oGlobalDict
        
        #Write back the JSON to the GlobalVar.JSON
        strJson = open(strGlobVarFilePath, mode='w+')
        #strDict = json.dumps(oJsonDict, indent=4, sort_keys=True)
        #print(str(strDict))
        strJson.write(json.dumps(oJsonDict, indent=4, sort_keys=True))
        strJson.close()
        
        if not ('ZIGBEE' in self.APIValidation.get().upper() or 'WEB' in self.MainClient.get().upper()):
            subprocess.call('killall node', shell=True)               
            subprocess.Popen(striOSAppiumConnectionString, shell=True)
            
        if 'ANDROID' in self.MainClient.get().upper():
            #subprocess.call('adb kill-server', shell=True)
            #subprocess.call('adb start-server', shell=True) 
            print()
        time.sleep(5)
        
        if self.TestSuite.get() == 'BasicSmokeTest_Dual':
            subprocess.Popen("behave --tags=BasicSmokeTest", shell=True)
        elif self.TestSuite.get() == 'BasicSmokeTest_Heating':            
            subprocess.Popen("behave --tags=BasicSmokeTest --tags=Heating", shell=True)        
        elif self.TestSuite.get() == 'BasicSmokeTest_HotWater':            
            subprocess.Popen("behave --tags=BasicSmokeTest --tags=HotWater", shell=True)
        elif self.TestSuite.get() == 'ScheduleTest_Dual':
            subprocess.Popen("behave --tags=ScheduleTest --tags=Verify", shell=True)
        elif self.TestSuite.get() == 'ScheduleTest_Heating':
            subprocess.Popen("behave --tags=ScheduleTest --tags=Verify --tags=Heating", shell=True)
        elif self.TestSuite.get() == 'ScheduleTest_HotWater':
            subprocess.Popen("behave --tags=ScheduleTest --tags=Verify --tags=HotWater", shell=True)
        elif self.TestSuite.get() == 'Kings':
            subprocess.Popen("behave --tags=Kings", shell=True)
        elif self.TestSuite.get() == 'SP_AllTest':
            subprocess.Popen("behave --tags=Generic", shell=True)
        elif self.TestSuite.get() == 'SP_AllChannelPairingTest':
            subprocess.Popen("behave --tags=SC-GT-SC01-01", shell=True)
        elif self.TestSuite.get() == 'SP_PairingTest':
            subprocess.Popen("behave --tags=SC-GT-SC01-02", shell=True)
        elif self.TestSuite.get() == 'SP_ZigbeeDumpTest':
            subprocess.Popen("behave --tags=SC-GT-SC02-01", shell=True)
        elif self.TestSuite.get() == 'SP_On-OffTest':
            subprocess.Popen("behave --tags=SC-GT-SC03-01", shell=True)
        elif self.TestSuite.get() == 'SP_Upgrade-Downgrade':
            subprocess.Popen("behave --tags=SC-GT-SC04-01", shell=True)
        print('Test suite Triggered')
        
        
        
    def browse_app_file(self):
        if self.MainClient.get().split()[0] == 'Android' : oAppExt = ("APK", "*.apk")
        else: oAppExt = ("APP", "*.app")
        strAPPFolderPAth = os.path.abspath(__file__ + "/../../../") + "/02_Manager_Tier/EnviromentFile/Apps/" + self.MainClient.get().split()[0] + '/' + self.Environment.get().split()[0]
        strFilePath = askopenfilename(filetypes=[oAppExt], initialdir=strAPPFolderPAth, title="Select the Android APK file")        
        strFileName = ntpath.split(strFilePath)[1]
        if not strFileName is "":
            oAppFileList = []
            oAllFileList = os.listdir(strAPPFolderPAth)
            #if strFileName not in oAllFileList:
            if ntpath.split(strFilePath)[0] != strAPPFolderPAth:
                print('not in list')
                shutil.copy(strFilePath, strAPPFolderPAth)
            for strFile in oAllFileList:    
                if os.path.splitext(strFile)[1].upper() == '.' + oAppExt[0]:
                    oAppFileList.append(strFile)
            oAppFileTuple = tuple(oAppFileList)
            self.oAppFilePath['value'] = oAppFileTuple
            self.oAppFilePath.set(strFileName)
            
    def api_selected_item_event(self, event):
        print(self.APIValidation.get())
        self.load_platformAPI_controls()    
        self.load_app_details(None)

    def set_global_var(self):
        strEnvironmentFolderPAth = os.path.abspath(__file__ + "/../../../") + "/02_Manager_Tier/EnviromentFile"        
        strGlobVarFilePath = strEnvironmentFolderPAth + '/GlobalVar.json'    
        strJson = open(strGlobVarFilePath, mode='r')
        oJsonDict = json.loads(strJson.read())
        strJson.close()    
        utils.oJsonDict = oJsonDict
        
root = Tk()
UIClass(root).pack()
root.mainloop()
