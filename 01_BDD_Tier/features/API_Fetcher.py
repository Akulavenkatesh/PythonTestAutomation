import json
import ntpath
import os
import shutil
import subprocess
from sys import executable
import time
from tkinter import *
from tkinter import font
from tkinter import ttk, Text
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Style
import traceback
import webbrowser

import FF_utils as utils
import FF_alertmeApi as ALAPI


class UIClass(Frame):
    
        
    
    def __init__(self, parent):
        self.set_global_var()
        self.window = parent
        parent.title("Hive Test Automation - API Response")
        parent.configure(background='#F4FFFF')
        self.position_window(parent,w=920, h=500)
        Frame.__init__(self, parent)
        
        #Style - Background color
        s = ttk.Style()
        #s.configure('.', background='black')
        ttk.Style().configure("TButton", padding=6, relief="flat", bg='#000000',
                fg='#b7f731',background="pale green")
        
        #Frame
        self.mainframe = ttk.Frame(self, padding="50 10 30 255")
        self.mainframe.configure(style='TFrame')
        self.mainframe.grid(column=0, row=0, sticky=(N))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        #Frame
        self.resposeFrame = ttk.Frame(self, padding="10 10 10 10")
        self.resposeFrame.configure(style='TFrame')
        self.resposeFrame.grid(column=1, row=0, sticky=(N, W, E, S))
        self.resposeFrame.columnconfigure(0, weight=1)
        self.resposeFrame.rowconfigure(0, weight=1)
        
        #Variables    
        self.Environment = StringVar()
        self.APIValidation = StringVar()
        self.UserName = StringVar()
        self.Password = StringVar()
        self.Response = StringVar()
        self.EndPoint = StringVar()
        self.Node = StringVar()
                
        self.appHighlightFont = font.Font(family='Helvetica', size=22, weight='bold')
        ttk.Label(self.mainframe, text='Get', font=self.appHighlightFont).grid(column=3, row=0, sticky=E)
        ttk.Label(self.mainframe, text='API Response', font=self.appHighlightFont).grid(column=15, row=0, sticky=W)
        
        #Environment
        ttk.Label(self.mainframe, text='Environment:    ').grid(column=3, row=1, sticky=E)
        self.oEnvironment = ttk.Combobox(self.mainframe, textvariable=self.Environment)
        self.oEnvironment['values'] = ('isopInternProd', 'isopBeta', 'isopStaging', 'isopProd')
        self.oEnvironment.state(['readonly'])
        self.oEnvironment.set('isopInternProd')
        self.oEnvironment.grid(column=15, row=1, sticky=W)
        '''
        #API Validation
        ttk.Label(self.mainframe, text='API Validation:    ').grid(column=3, row=2, sticky=E)
        self.oAPIValidation = ttk.Combobox(self.mainframe, textvariable=self.APIValidation)
        self.oAPIValidation['values'] = ('Platform API')
        self.oAPIValidation.state(['readonly'])
        self.oAPIValidation.set('Platform API')
        self.oAPIValidation.grid(column=15, row=2, sticky=W)
        '''
        #User Name
        self.lblUserName = ttk.Label(self.mainframe, text='User Name:    ')
        self.lblUserName.grid(column=3, row=3, sticky=E)
        self.oUserName = ttk.Combobox(self.mainframe, textvariable=self.UserName)
        self.oUserName['values'] = ('auto1_v6', 'tester2', 'tester4_v6')
        self.oUserName.set(utils.getAttribute('common', 'userName'))
        self.oUserName.grid(column=15, row=3, sticky=W)
        
        #Password
        self.lblPassword = ttk.Label(self.mainframe, text='Password:    ')
        self.lblPassword.grid(column=3, row=4, sticky=E)
        self.oPassword = ttk.Combobox(self.mainframe, textvariable=self.Password)
        self.oPassword['values'] = ('password1', 'Password1', 'passw0rd')
        self.oPassword.set(utils.getAttribute('common', 'password'))
        self.oPassword.grid(column=15, row=4, sticky=W)
        self.boolUserPassDestroyed = False
        
        #End Point
        self.lblEPType, self.EPType = self.create_combobox(5, '     End Point:    ', self.EndPoint, (), "", False)    
        self.EPType['values'] = ('Heating', 'Hot Water', 'Common')
        self.EPType.bind('<<ComboboxSelected>>', self.update_available_nodes)
        self.EPType.state(['readonly'])
        self.EPType.set('Heating')
        #Nodes
        self.lblNode, self.oNode = self.create_combobox(6, 'Node:    ', self.Node, (), "", False)
        self.oNode['values'] = ('Mode', 'Schedule', 'Running State')
        self.oNode.state(['readonly'])
        self.oNode.set('Mode')
        
        self.update_available_nodes(None)
        #Respose and Load Scroll bars
        xscrollbar = Scrollbar(self.resposeFrame, orient=HORIZONTAL)
        xscrollbar.grid(row=2, column=17, sticky=E+W)        
        yscrollbar = Scrollbar(self.resposeFrame)
        yscrollbar.grid(row=2, column=17, sticky=N+S)
        self.Response = Text(self.resposeFrame, width = 70, height = 30, wrap=NONE, bd=0,
                    xscrollcommand=xscrollbar.set,
                    yscrollcommand=yscrollbar.set)
        self.Response.pack()
        self.Response.grid(column=17, row=2, sticky=W)
        xscrollbar.config(command=self.Response.xview)
        yscrollbar.config(command=self.Response.yview)
        
        #Exucute & Quit Buttons
        ttk.Label(self.mainframe, text='').grid(column=3, row=14, sticky=E)
        ttk.Label(self.mainframe, text='').grid(column=15, row=14, sticky=E)
        oExecute = ttk.Button(self.mainframe, text='Execute', command=self.load_response)
        oExecute.grid(column=15, row=15, sticky=W)       
        oExecute = ttk.Button(self.mainframe, text='Quit', command=self.closeWidget)
        oExecute.grid(column=15, row=15, sticky=E)
        
    def update_available_nodes(self, event):
        if self.EndPoint.get() == 'Heating':
            self.oNode['values'] = ('Mode', 'Schedule', 'Running State', 'Target Temperature', 'Local Temperature')
        if self.EndPoint.get() == 'Hot Water':
            self.oNode['values'] = ('Mode', 'Schedule', 'Running State')
        if self.EndPoint.get() == 'Common':
            self.oNode['values'] = ('Holiday Mode', 'Notifications', 'All', 'Kit Versions')
            self.oNode.set('Holiday Mode')
        
    def load_response(self):
        self.updateGlobalVarJson()
        self.Response.delete(1.0, END) 
        self.Response.insert(1.0, json.dumps(self.get_response(), indent=4, sort_keys=False))
        ALAPI.deleteSessionV6(self.session)
    
    def set_default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        raise TypeError

#Get the Node ID for the given device type
    def getNodeID(self, resp):
        oDeviceNodes = {}
        for oNode in resp['nodes']:
            if not 'supportsHotWater'  in oNode['attributes']:
                if 'thermostatui.json' in oNode["nodeType"]:
                    strModel = oNode["attributes"]["model"]["reportedValue"]
                    oDeviceNodes[strModel] = oNode["id"]
                elif 'thermostat.json' in oNode["nodeType"]:
                    strModel = oNode["attributes"]["model"]["reportedValue"]
                    oDeviceNodes[strModel] = oNode["id"]
                elif 'hub.json' in oNode["nodeType"]:
                    strModel = oNode["attributes"]["hardwareVersion"]["reportedValue"]
                    oDeviceNodes[strModel] = oNode["id"]
                elif 'smartplug.json' in oNode["nodeType"]:
                    strModel = oNode["attributes"]["model"]["reportedValue"]
                    oDeviceNodes[strModel] = oNode["id"]
                elif 'extender.json' in oNode["nodeType"]:
                    strModel = oNode["attributes"]["model"]["reportedValue"]
                    oDeviceNodes[strModel] = oNode["id"]
                elif 'contact.sensor.json' in oNode["nodeType"]:
                    strModel = oNode["attributes"]["model"]["reportedValue"]
                    oDeviceNodes[strModel] = oNode["id"]
                elif 'motion.sensor.json' in oNode["nodeType"]:
                    strModel = oNode["attributes"]["model"]["reportedValue"]
                    oDeviceNodes[strModel] = oNode["id"]
                elif 'connected.boiler.json' in oNode["nodeType"]:
                    strModel = oNode["attributes"]["model"]["reportedValue"]
                    oDeviceNodes[strModel] = oNode["id"]
        return oDeviceNodes
    
    #Get the FirmwareVersion for the given device type
    def getFWversion(self, resp):
        ALAPI.createCredentials(self.Environment.get())
        session  = ALAPI.sessionObject()
        resp = ALAPI.getNodesV6(session)
        oDeviceVersion = {}
        for oNode in resp['nodes']:
            if not 'supportsHotWater'  in oNode['attributes']:
                if 'thermostatui.json' in oNode["nodeType"]:
                    strModel = oNode["attributes"]["model"]["reportedValue"]
                    oDeviceVersion[strModel] = oNode["attributes"]["softwareVersion"]["reportedValue"]
                elif 'thermostat.json' in oNode["nodeType"]:
                    strModel = oNode["attributes"]["model"]["reportedValue"]
                    oDeviceVersion[strModel] = oNode["attributes"]["softwareVersion"]["reportedValue"]
                elif 'hub.json' in oNode["nodeType"]:
                    strModel = oNode["attributes"]["hardwareVersion"]["reportedValue"]
                    oDeviceVersion[strModel] = oNode["attributes"]["softwareVersion"]["reportedValue"]
                elif 'smartplug.json' in oNode["nodeType"]:
                    strModel = oNode["attributes"]["model"]["reportedValue"]
                    oDeviceVersion[strModel] = oNode["attributes"]["softwareVersion"]["reportedValue"]
                elif 'extender.json' in oNode["nodeType"]:
                    strModel = oNode["attributes"]["model"]["reportedValue"]
                    oDeviceVersion[strModel] = oNode["attributes"]["softwareVersion"]["reportedValue"]
                elif 'contact.sensor.json' in oNode["nodeType"]:
                    strModel = oNode["attributes"]["model"]["reportedValue"]
                    oDeviceVersion[strModel] = oNode["attributes"]["softwareVersion"]["reportedValue"]
                elif 'motion.sensor.json' in oNode["nodeType"]:
                    strModel = oNode["attributes"]["model"]["reportedValue"]
                    oDeviceVersion[strModel] = oNode["attributes"]["softwareVersion"]["reportedValue"]
                elif 'connected.boiler.json' in oNode["nodeType"]:
                    strModel = oNode["attributes"]["model"]["reportedValue"]
                    oDeviceVersion[strModel] = oNode["attributes"]["softwareVersion"]["reportedValue"]
        ALAPI.deleteSessionV6(session)
        return oDeviceVersion
    
    def get_response(self):
        ALAPI.createCredentials(self.Environment.get())
        self.session = ALAPI.sessionObject()
        if self.session.latestSupportedApiVersion != '6':
            self.platformVersion = 'V5'
            print("hello")
            self.Response.insert(1.0, 'User is V5. Retry with V6 User')
            return False
        else:
            self.platformVersion = 'V6'
            
            if self.Node.get() == 'Notifications':                 
                respRules = ALAPI.getRulesV6(self.session)
                return respRules
            
            resp = ALAPI.getNodesV6(self.session)
            if 'HEAT' in self.EndPoint.get().upper():
                boolWater = False
            else: boolWater = True
            
            if self.Node.get() == 'Holiday Mode':
                oHolDict = {}
                for oNode in resp['nodes']:
                    if 'holidayMode'  in oNode['attributes']:
                        oHolDict['holidayMode']  = oNode['attributes']['holidayMode']
                    if 'holidayModeEnabled'  in oNode['attributes']:
                        oHolDict['holidayModeEnabled']  = oNode['attributes']['holidayModeEnabled']
                    if 'holidayModeActive'  in oNode['attributes']:
                        oHolDict['holidayModeActive']  = oNode['attributes']['holidayModeActive']
                return oHolDict
            
            if self.Node.get() == 'All':
                return resp
            
            if self.Node.get() == 'Kit Versions':
                print(self.getNodeID(resp))
                print(self.getFWversion(resp))
                oDeviceVersionDict = {}
                strSLTMacID = ""
                strSLRMacID = ""
                for oNode in resp['nodes']:
                    if not 'supportsHotWater'  in oNode['attributes']:
                        if 'hardwareVersion' in oNode['attributes']: 
                            intHardwareVersion = oNode['attributes']['hardwareVersion']['reportedValue']
                            intSoftwareVersion = oNode['attributes']['softwareVersion']['reportedValue']
                            if 'NANO' in  intHardwareVersion:
                                #oDeviceVersionDict['HUB'] = intHardwareVersion + '$$' + intSoftwareVersion
                                #strHubMacId = oNode['attributes']['zigBeeNeighbourTable']['reportedValue'][0]['neighbourAddress']
                                oDeviceVersionDict['HUB'] = {"model" : intHardwareVersion, "version" : intSoftwareVersion}#,  'mac_id': strHubMacId}
                        if 'zigBeeNeighbourTable' in oNode['attributes']:
                            for oDevice in json.loads(oNode['attributes']['zigBeeNeighbourTable']['reportedValue']):
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
                                #oDeviceVersionDict['Thermostat'] = strModel + '$$' + intSoftwareVersion
                                oDeviceVersionDict['Thermostat'] = {"model" : strModel, "version" : intSoftwareVersion, 'mac_id': strSLTMacID}
                            elif'SLR' in strModel: 
                                #oDeviceVersionDict['Boiler Module'] = strModel + '$$' + intSoftwareVersion
                                oDeviceVersionDict['Boiler Module'] = {"model" : strModel, "version" : intSoftwareVersion, 'mac_id': strSLRMacID}
                return oDeviceVersionDict
            
            for oNode in resp['nodes']:
                if 'supportsHotWater'  in oNode['attributes']:
                    if oNode['attributes']['supportsHotWater']['reportedValue'] == True  and 'stateHotWaterRelay' in oNode['attributes']:
                        if boolWater:
                            print("water")
                            oAttributeList = oNode['attributes']  
                            
                            if self.Node.get() == 'Schedule': 
                                oSchedDict = {}
                                oJsonAll = oAttributeList['schedule']
                                for oKey in oJsonAll:
                                    oJson = oJsonAll[oKey]
                                    if oKey == 'targetValue' or oKey == 'reportedValue':
                                        if isinstance(oJson, str): oJson = json.loads(oJson)
                                    oSchedDict[oKey] = oJson
                                return {"schedule" : oSchedDict}
                            
                            elif self.Node.get() ==  'Running State':
                                return {"stateHotWaterRelay" : oAttributeList['stateHotWaterRelay']} 
                            elif self.Node.get() == 'Mode':  
                                strActiveHeatCoolMode =  self.getAttribute(oAttributeList, 'activeHeatCoolMode') 
                                boolActiveScheduleLock = self.getAttribute(oAttributeList, 'activeScheduleLock')
                                print(boolActiveScheduleLock, 'boolActiveScheduleLock')
                                lstActiveOverrides = self.getAttribute(oAttributeList, 'activeOverrides') 
                                
                                if strActiveHeatCoolMode == 'OFF':
                                    self.mode = 'OFF'
                                elif strActiveHeatCoolMode == 'HEAT' and boolActiveScheduleLock:
                                    self.mode = 'MANUAL'
                                elif len(lstActiveOverrides) > 0 and lstActiveOverrides[0] == "TARGET_HEAT_TEMPERATURE":
                                    self.mode = 'OVERRIDE'
                                elif strActiveHeatCoolMode == 'HEAT' and not boolActiveScheduleLock:
                                    self.mode = 'AUTO'
                                elif strActiveHeatCoolMode == 'BOOST':
                                    self.mode = 'BOOST'
                                
                                return {"currentMode" : self.mode, "activeHeatCoolMode" : oAttributeList['activeHeatCoolMode'], "activeScheduleLock" : oAttributeList['activeScheduleLock'], "activeOverrides" :oAttributeList['activeOverrides'], "scheduleLockDuration" : oAttributeList["scheduleLockDuration"], "stateHotWaterRelay" : oAttributeList['stateHotWaterRelay']}
                            
                    else:
                        if not boolWater and 'stateHeatingRelay' in oNode['attributes']:
                            print('Heat')
                            oAttributeList = oNode['attributes']             
                            
                            if self.Node.get() == 'Schedule': 
                                oSchedDict = {}
                                oJsonAll = oAttributeList['schedule']
                                for oKey in oJsonAll:
                                    oJson = oJsonAll[oKey]
                                    if oKey == 'targetValue' or oKey == 'reportedValue':
                                        if isinstance(oJson, str): oJson = json.loads(oJson)
                                    oSchedDict[oKey] = oJson
                                return {"schedule" : oSchedDict}
                            
                            elif self.Node.get() ==  'Running State':
                                return {"stateHeatingRelay" : oAttributeList['stateHeatingRelay']}
                            
                            
                            elif self.Node.get() ==  'Target Temperature':
                                return {"targetHeatTemperature" : oAttributeList['targetHeatTemperature']}
                                        
                            elif self.Node.get() ==  'Local Temperature':
                                return {"temperature" : oAttributeList['temperature']}
                            
                            elif self.Node.get() == 'Mode':  
                                strActiveHeatCoolMode = self.getAttribute(oAttributeList, 'activeHeatCoolMode') 
                                boolActiveScheduleLock = self.getAttribute(oAttributeList, 'activeScheduleLock')
                                lstActiveOverrides = self.getAttribute(oAttributeList, 'activeOverrides') 
                                
                                if strActiveHeatCoolMode == 'OFF':
                                    self.mode = 'OFF'
                                elif strActiveHeatCoolMode == 'HEAT' and boolActiveScheduleLock:
                                    self.mode = 'MANUAL'
                                elif strActiveHeatCoolMode == 'HEAT' and not boolActiveScheduleLock:
                                    self.mode = 'AUTO'
                                elif strActiveHeatCoolMode == 'BOOST':
                                    self.mode = 'BOOST'
                                elif len(lstActiveOverrides) > 0 and lstActiveOverrides[0] == "TARGET_HEAT_TEMPERATURE":
                                    self.mode = 'OVERRIDE'
                            
                                return {"currentMode" : self.mode, "activeHeatCoolMode" : oAttributeList['activeHeatCoolMode'], "activeScheduleLock" : oAttributeList['activeScheduleLock'], "activeOverrides" :oAttributeList['activeOverrides'], "scheduleLockDuration" : oAttributeList["scheduleLockDuration"], "stateHeatingRelay" : oAttributeList['stateHeatingRelay']}
                
    def getAttribute(self, oAttributeList, strAttributeName):
        reported = oAttributeList[strAttributeName]['reportedValue']
        if 'targetValue' in oAttributeList[strAttributeName]:
            target =  oAttributeList[strAttributeName]['targetValue']
            targetTime = oAttributeList[strAttributeName]['targetSetTime']
            currentTime = int(time.time() * 1000)
            if ((currentTime - targetTime) < 20000): 
                print('taken target value for', strAttributeName)
                return target;
        return reported;
    
   
        
    #Place Window on the center fo the screen
    def position_window(self, parent, w, h):
        # get screen width and height
        ws = parent.winfo_screenwidth()
        hs = parent.winfo_screenheight()
        # calculate position x, y
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        parent.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
          
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
        #Tk().clipboard_append(self.Response.get())
        exit()
    
    def updateGlobalVarJson(self):
        #Reading all data from GlobalVar.Json
        strEnvironmentFolderPAth = os.path.abspath(__file__ + "/../../../") + "/02_Manager_Tier/EnviromentFile/"        
        strGlobVarFilePath = strEnvironmentFolderPAth + '/GlobalVar.json'    
        strJson = open(strGlobVarFilePath, mode='r')
        oJsonDict = json.loads(strJson.read())
        strJson.close()
        
        oGlobalDict = oJsonDict['globalVariables']
        #updating the json Dictionary based on the the input parameter selected on the GUI
        oGlobalDict['currentEnvironment'] = self.Environment.get()
        oGlobalDict['userName']= self.UserName.get()
        oGlobalDict['password']= self.Password.get()
        oJsonDict['globalVariables'] = oGlobalDict
        
        #Write back the JSON to the GlobalVar.JSON
        strJson = open(strGlobVarFilePath, mode='w+')
        #strDict = json.dumps(oJsonDict, indent=4, sort_keys=True)
        #print(str(strDict))
        strJson.write(json.dumps(oJsonDict, indent=4, sort_keys=True))
        strJson.close()
        
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
