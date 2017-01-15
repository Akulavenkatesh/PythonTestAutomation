'''
Created on 12 Jun 2015

@author: ranganathan.veluswamy

@author: : Hitesh Sharma - 15 July 2016 
@note: created function setLowNotification and setHighNotification to add logic for iOS to set the heating notifications
@note: 10 Aug 2016 - Added function navigatetoContactSensor and currentCSStatus to navigate to contact sensor screen and get the current status for given CS status resp
'''
import json
import time

import DD_Page_AndroidApp as androidPage
import DD_Page_WebApp as webPage
import DD_Page_iOSApp as iOSPage
import FF_alertmeApi as ALAPI
import FF_Platform_Utils as pUtils



class platformAPIClass(object):
    def __init__(self,strServerName):
        self.AndroidDriver = None
        self.WebDriver = None
        self.iOSDriver = None
        self.reporter = None
        self.heatEP = thermostatEndpoint(self,strServerName,'HEAT')
        self.waterEP = thermostatEndpoint(self,strServerName,'WATER')
        self.sensorEP = thermostatEndpoint(self,strServerName,'SENSOR')

            
        return
    def update(self):
        """
        """
        self.heatEP.update()
        self.waterEP.update()
        return 0

class thermostatEndpoint(object):
    def __init__(self,platAPI,strServerName,epType):
        # Parent Tstat
        self.parentAPI= platAPI
        self.type = epType
        self.serverName = strServerName
        self.client = None
        self.mode = None
        self.localTemperature = 0.0
        self.occupiedHeatingSetpoint = 0.0
        self.thermostatRunningState = ''
        self._weeklySchedule = {}
        self.AndroidDriver = platAPI.AndroidDriver
        self.WebDriver = platAPI.WebDriver
        self.iOSDriver = platAPI.iOSDriver
        self.reporter = platAPI.reporter
        self.Web_ManualModeTargTemp = 20.0
        self.platformVersion = None
        self.occupiedHeatingSetpointChanged = False
        
        self.deviceType = ""
        self.currentDeviceNodeId = ""
        self.currentDeviceSDNodeId = ""
        self.CurrentDeviceState = ""
        self.activeLightBrightness = 0
    
    
    
    def update(self):   
        self.AndroidDriver = self.parentAPI.AndroidDriver
        self.WebDriver = self.parentAPI.WebDriver
        self.iOSDriver = self.parentAPI.iOSDriver
        self.reporter = self.parentAPI.reporter
        if self.platformVersion== 'V5':
            self._updateV5()
        else:
            if not self._updateV6():
                self._updateV5()
                
    def update_attributes_from_client(self):
        self.getAttributesFromClient()
        
    def _updateV6(self, nodeID= None):
        #Updating attributes for Light
        print("self.deviceType.upper()", self.deviceType.upper())
        if "FWBULB" in self.deviceType.upper(): 
            self.currentDeviceNodeId = pUtils.getDeviceNodeID(self.deviceType)
            self.mode, self.CurrentDeviceState, self.activeLightBrightness = pUtils.getLightAttributes(self.currentDeviceNodeId)
            self._weeklySchedule = pUtils.getDeviceScheduleInStandardFormat(self.deviceType)
            print(self._weeklySchedule)
            return True
            
        ALAPI.createCredentials(self.serverName, self.client)
        session  = ALAPI.sessionObject()
        if session.latestSupportedApiVersion != '6':
            self.platformVersion = 'V5'
            print("V5")
            return False
        else:
            self.platformVersion = 'V6'
            
                       
            resp = ALAPI.getNodesV6(session)
            if self.type == 'HEAT':
                boolWater = False
            else: boolWater = True
            for oNode in resp['nodes']:
                if not nodeID is None:
                    if  not oNode['parentNodeId'] == nodeID: continue 
                if 'supportsHotWater'  in oNode['attributes']:
                    if oNode['attributes']['supportsHotWater']['reportedValue'] == True and 'stateHotWaterRelay' in oNode['attributes']:
                        if boolWater:
                            print("water")
                            oAttributeList = oNode['attributes']                
                            #oJson = oAttributeList['schedule']['reportedValue']
                            oJson = self.getAttribute(oAttributeList, 'schedule')
                            if isinstance(oJson, str): oJson = json.loads(oJson)
                            self._weeklySchedule = self._formatScheduleV6(oJson)
                            #print('%%%%%%%%%%%^^^^^^^^^^^^^^^^^', oJson)
                            strRunningState = self.getAttribute(oAttributeList, 'stateHotWaterRelay')
                            if strRunningState == 'OFF': self.thermostatRunningState = '0000'
                            else: self.thermostatRunningState = '0001'
                            
                            
                            strActiveHeatCoolMode =  self.getAttribute(oAttributeList, 'activeHeatCoolMode') 
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
                            '''    
                            print(self._weeklySchedule)
                            print(self.mode)
                            print(self.thermostatRunningState)
                            '''
                    else:
                        if not boolWater  and 'stateHeatingRelay' in oNode['attributes']:
                            print('Heat')
                            oAttributeList = oNode['attributes']                
                            #oJson = oAttributeList['schedule']['reportedValue']
                            oJson = self.getAttribute(oAttributeList, 'schedule')
                            if isinstance(oJson, str): oJson = json.loads(oJson)
                            self._weeklySchedule = self._formatScheduleV6(oJson)
                            strRunningState = self.getAttribute(oAttributeList, 'stateHeatingRelay')
                            if strRunningState == 'OFF': self.thermostatRunningState = '0000'
                            else: self.thermostatRunningState = '0001'
                            if self.occupiedHeatingSetpointChanged: occupiedHeatingSetpoint = self.getAttribute(oAttributeList, 'targetHeatTemperature')
                            self.occupiedHeatingSetpoint = float('{:.1f}'.format(oAttributeList['targetHeatTemperature']['reportedValue']))
                                            
                            self.localTemperature = self.getAttribute(oAttributeList, 'temperature')
                            
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
                            
                            '''
                            print(self._weeklySchedule)
                            print(self.mode)
                            print(self.occupiedHeatingSetpoint)
                            print(self.thermostatRunningState)
                            print(self.localTemperature)
                            '''
            ALAPI.deleteSessionV6(session)
            return True
    
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
        
    def _updateV5(self):
        #print('update start ', datetime.today().strftime("%H:%M:%S" ))
        #Login and get HubID
        ALAPI.createCredentials(self.serverName, self.client)
        resp = ALAPI.login()
        strHubID = resp[1]
        #Get the Device ID
        resp =ALAPI.getDevices(ALAPI.API_CREDENTIALS.apiUsername, strHubID)
        respList = resp[0]
        for oDevice in respList:
            if oDevice['name'] == 'Your Receiver':
                strBMDeviceID = oDevice['id']
        
        #Create Myaccount Class
        myAccount =ALAPI.accountClass(ALAPI.API_CREDENTIALS.apiUsername)
        
        
        if self.type == 'HEAT':
            #Get Heat Schedule
            resp = ALAPI.getHeatSchedule(myAccount, strBMDeviceID)
            respDict = resp[0]
            self._weeklySchedule = self._formatSchedule(respDict)
            
            #Get Target Temperature
            resp = ALAPI.getTargetTemperature(ALAPI.API_CREDENTIALS.apiUsername)
            respDict = resp[0]    
            if 'temperature' in respDict: self.occupiedHeatingSetpoint = respDict['temperature']
            
            #Get Heat Running State
            resp = ALAPI.getHeatDetails(ALAPI.API_CREDENTIALS.apiUsername)
            respDict = resp[0]    
            if 'active' in respDict:
                boolRunningState = respDict['active']
            if not boolRunningState: self.thermostatRunningState = '0000'
            else: self.thermostatRunningState = '0001'
            
            #Get Local Temperature
            resp = ALAPI.getLocalTemperature(ALAPI.API_CREDENTIALS.apiUsername)
            respDict = resp[0]    
            if 'inside' in respDict:
                self.localTemperature = respDict['inside']['now']
            
            #Get Heat Mode
            resp = ALAPI.getHeatModeNew(ALAPI.API_CREDENTIALS.apiUsername)
            respDict = resp[0]    
            if 'control' in respDict:
                self.mode = respDict['control']
                if self.mode == 'SCHEDULE': self.mode ='AUTO'
            
        elif self.type == 'WATER':            
            #Get Water Schedule
            resp = ALAPI.getHotWaterSchedule(ALAPI.API_CREDENTIALS.apiUsername, strHubID, strBMDeviceID)
            respDict = resp[0]           
            self._weeklySchedule = self._formatSchedule(respDict)
            
            resp = ALAPI.getHotWaterModeAndRunState(ALAPI.API_CREDENTIALS.apiUsername, strBMDeviceID)
            respDict = resp[0]    
            if 'control' in respDict:
                self.mode = respDict['control']
                if self.mode == 'SCHEDULE': self.mode ='AUTO'
            if 'onOffState' in respDict:
                self.thermostatRunningState = respDict['onOffState']
            if self.thermostatRunningState=='OFF': self.thermostatRunningState = '0000'
            else: self.thermostatRunningState = '0001'
            if 'targetTemperature' in respDict:
                self.occupiedHeatingSetpoint = respDict['targetTemperature']
            if 'currentTemperature' in respDict:
                self.localTemperature = respDict['currentTemperature']
        
        
        #print('update stop ', datetime.today().strftime("%H:%M:%S" ))
    
    def _formatScheduleV6(self, respDict):
        oSchedDict = {}
        oNewSchedDict = {}  
        
        for oDay in respDict.keys():
            oSchedList = []
            oEventList = respDict[oDay]
            for oEvent in oEventList:
                intHour= int(oEvent['time'].split(':')[0])
                intMin = int(oEvent['time'].split(':')[1])
                oSchedList.append(('{:02d}:{:02d}'.format(intHour, intMin), oEvent['targetHeatTemperature']))        
            oSchedDict.update({oDay : oSchedList})
                
        if 'weekdays' in oSchedDict:
            oNewSchedDict['mon'] = oSchedDict['weekdays']
            oNewSchedDict['tue'] = oSchedDict['weekdays']
            oNewSchedDict['wed'] = oSchedDict['weekdays']
            oNewSchedDict['thu'] = oSchedDict['weekdays']
            oNewSchedDict['fri'] = oSchedDict['weekdays']
        else:
            oNewSchedDict['mon'] = oSchedDict['monday']
            oNewSchedDict['tue'] = oSchedDict['tuesday']
            oNewSchedDict['wed'] = oSchedDict['wednesday']
            oNewSchedDict['thu'] = oSchedDict['thursday']
            oNewSchedDict['fri'] = oSchedDict['friday']
            
        if 'weekend' in oSchedDict:
            oNewSchedDict['sat'] = oSchedDict['weekend']
            oNewSchedDict['sun'] = oSchedDict['weekend']
        elif 'weekends' in oSchedDict:
            oNewSchedDict['sat'] = oSchedDict['weekends']
            oNewSchedDict['sun'] = oSchedDict['weekends']
        else:
            oNewSchedDict['sat'] = oSchedDict['saturday']
            oNewSchedDict['sun'] = oSchedDict['sunday']
            
        return oNewSchedDict    
    
    #Formating the schedule dictionary as per Schedule dictionary used for Zigbee
    def _formatSchedule(self,respDict):
        oSchedDict = {}
        oNewSchedDict = {}  
        if 'days' in respDict:
            for oDay in respDict['days'].keys():
                oSchedList = []
                for eventDict in respDict['days'][oDay]:
                    oSchedList.append((eventDict['time'], eventDict['temperature']))
                oSchedDict.update({oDay : oSchedList})
                          
        if 'weekdays' in oSchedDict:
            oNewSchedDict['mon'] = oSchedDict['weekdays']
            oNewSchedDict['tue'] = oSchedDict['weekdays']
            oNewSchedDict['wed'] = oSchedDict['weekdays']
            oNewSchedDict['thu'] = oSchedDict['weekdays']
            oNewSchedDict['fri'] = oSchedDict['weekdays']
        else:
            oNewSchedDict['mon'] = oSchedDict['monday']
            oNewSchedDict['tue'] = oSchedDict['tuesday']
            oNewSchedDict['wed'] = oSchedDict['wednesday']
            oNewSchedDict['thu'] = oSchedDict['thursday']
            oNewSchedDict['fri'] = oSchedDict['friday']
            
        if 'weekend' in oSchedDict:
            oNewSchedDict['sat'] = oSchedDict['weekend']
            oNewSchedDict['sun'] = oSchedDict['weekend']
        else:
            oNewSchedDict['sat'] = oSchedDict['saturday']
            oNewSchedDict['sun'] = oSchedDict['sunday']
            
        return oNewSchedDict
    
    #Upgrade Firmware for the give device type
    def upgradeFirware(self, DeviceType, fwTargetVersion):
        ALAPI.createCredentials(self.serverName, self.client)
        session  = ALAPI.sessionObject()
        resp = ALAPI.getNodesV6(session)
        nodeIdList = self.getNodeID(resp)
        if DeviceType in nodeIdList:
            nodeId = nodeIdList[DeviceType]
            ALAPI.firmwareUpgrade(session, nodeId, fwTargetVersion)
        else: print("Unable to Fetch Node ID for the Given Device Type: " + DeviceType)
        ALAPI.deleteSessionV6(session)
        
        
    #Get the Node ID for the given device type
    def getNodeID(self, resp):
        oDeviceNodes = {}
        for oNode in resp['nodes']:
            if not ('supportsHotWater' or 'consumers' or 'producers') in oNode['attributes']:
                if 'nodeType' in oNode.keys():
                    if 'thermostatui.json' in oNode["nodeType"]:
                        strModel = oNode["attributes"]["model"]["reportedValue"]
                        oDeviceNodes[strModel] = oNode["id"]
                    elif 'thermostat.json' in oNode["nodeType"]:
                        if 'reportedValue' not in oNode["attributes"]["model"]: strModel = 'SLR2'
                        else: strModel = oNode["attributes"]["model"]["reportedValue"]
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
                    elif 'light.json' in oNode["nodeType"]:  #LDS_DimmerLight
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
    def getFWversion(self):
        ALAPI.createCredentials(self.serverName, self.client)
        session  = ALAPI.sessionObject()
        resp = ALAPI.getNodesV6(session)
        oDeviceVersion = {}
        for oNode in resp['nodes']:
            if not 'supportsHotWater'  in oNode['attributes']:
                if 'nodeType' in oNode.keys():
                    if 'thermostatui.json' in oNode["nodeType"]:
                        strModel = oNode["attributes"]["model"]["reportedValue"]
                        oDeviceVersion[strModel] = oNode["attributes"]["softwareVersion"]["reportedValue"]
                    elif 'thermostat.json' in oNode["nodeType"]:
                        if 'reportedValue' not in oNode["attributes"]["model"]: strModel = 'SLR2'
                        else: strModel = oNode["attributes"]["model"]["reportedValue"]
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
                    elif 'light.json' in oNode["nodeType"]:  #LDS_DimmerLight
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
    
    #Set Mode via platform API
    def setModeViaAPI(self, nodeId, setMode, targetHeatTemperature = None, scheduleLockDuration = 60):
        ALAPI.createCredentials(self.serverName, self.client)
        session  = ALAPI.sessionObject()
        nodeId = self.getChildNodeForBM(ALAPI.getNodesV6(session), nodeId)
        ALAPI.setModeV6(session, nodeId, setMode, targetHeatTemperature, scheduleLockDuration)
        if not 'WATER' in self.type.upper() and 'MANUAL' in setMode: 
            ALAPI.setTargTemperatureV6(session, nodeId, targetHeatTemperature)
        ALAPI.deleteSessionV6(session)
        
    #Set Schedule via platform API
    def setScheduleViaAPI(self, nodeId, payload):
        ALAPI.createCredentials(self.serverName, self.client)
        session  = ALAPI.sessionObject()
        
        ALAPI.setScheduleSP(session, nodeId, payload)
        
        
        '''if 'SLR' in deviceType.upper():
            nodeId = self.getChildNodeForBM(ALAPI.getNodesV6(session), nodeId)'''
        #elif 'SLP' in deviceType.upper() or ''
        '''if not 'WATER' in self.type.upper() and 'MANUAL' in setMode: 
            ALAPI.setTargTemperatureV6(session, nodeId, targetHeatTemperature)'''
        ALAPI.deleteSessionV6(session)
    
    def getChildNodeForBM(self, resp, BMNodeId):
        strChildNodeID = BMNodeId
        for oNode in resp['nodes']:
            if oNode['parentNodeId'] == BMNodeId:
                if ('WATER' in self.type.upper() and oNode['attributes']['supportsHotWater']['reportedValue'] == True) or ('WATER' not in self.type.upper() and oNode['attributes']['supportsHotWater']['reportedValue'] == False):
                    strChildNodeID = oNode['id']
                    print('strChildNodeID', strChildNodeID)
        return strChildNodeID
    
    def setMode(self,myMode, mySetpoint=None, myDuration=1):
        if 'ANDROID' in self.client.upper(): 
            if self.type == 'HEAT':
                oHomePage = androidPage.HomePage(self.AndroidDriver, self.reporter)
                oHomePage.navigate_to_heating_home_page()
                oHeatingHomePage = androidPage.HeatingHomePage(self.AndroidDriver, self.reporter)
                oHeatingHomePage.navigate_to_heating_control_page()
                oHeatControlPage = androidPage.HeatingControlPage(self.AndroidDriver, self.reporter)
                oHeatControlPage.set_heat_mode(myMode, mySetpoint, myDuration)
            elif self.type == 'WATER':
                oHomePage = androidPage.HomePage(self.AndroidDriver, self.reporter)
                oHomePage.navigate_to_hot_water_home_page()
                oHotWaterHomePage = androidPage.HotWaterHomePage(self.AndroidDriver, self.reporter)
                oHotWaterHomePage.navigate_to_hot_water_control_page()
                oHotWaterControlPage = androidPage.HotWaterControlPage(self.AndroidDriver, self.reporter)
                print('platform duration', myDuration)
                oHotWaterControlPage.set_hot_water_mode(myMode, myDuration)
        elif 'IOS' in self.client.upper(): 
            if self.type == 'HEAT':
                oHomePage = iOSPage.HomePage(self.iOSDriver, self.reporter)
                oHomePage.navigate_to_heating_control_page()
                oHeatControlPage = iOSPage.HeatingControlPage(self.iOSDriver, self.reporter)
                oHeatControlPage.set_heat_mode(myMode, mySetpoint, myDuration)
            if self.type == 'WATER':
                oHomePage = iOSPage.HomePage(self.iOSDriver, self.reporter)
                oHomePage.navigate_to_hot_water_control_page()
                oHotWaterControlPage = iOSPage.HotWaterControlPage(self.iOSDriver, self.reporter)
                oHotWaterControlPage.set_hot_water_mode(myMode, myDuration)
        elif 'WEB' in self.client.upper(): 
            if self.type == 'HEAT':
                oHoneycombDashboardPayge = webPage.HoneycombDashboardPage(self.WebDriver,self.reporter)
                oHoneycombDashboardPayge.navigate_to_heating_product_page()
                oHeatingPayge = webPage.HeatingPage(self.WebDriver, self.reporter)
                fltTargTemp = oHeatingPayge.set_heat_mode(myMode)
                if myMode == 'MANUAL': self.Web_ManualModeTargTemp = fltTargTemp
            elif self.type == 'WATER':
                oHoneycombDashboardPayge = webPage.HoneycombDashboardPage(self.WebDriver,self.reporter)
                oHoneycombDashboardPayge.navigate_to_hot_water_product_page()
                oHotWaterPage = webPage.HotWaterPage(self.WebDriver, self.reporter)
                fltTargTemp = oHotWaterPage.set_hot_water_mode(myMode)
                if myMode == 'MANUAL': self.Web_ManualModeTargTemp = fltTargTemp
        self.occupiedHeatingSetpointChanged = False
        
    def setSetpoint(self, mySetpoint):
        if 'ANDROID' in self.client.upper():      
            oHomePage = androidPage.HomePage(self.AndroidDriver, self.reporter)
            oHomePage.navigate_to_heating_home_page()
            oHeatingHomePage = androidPage.HeatingHomePage(self.AndroidDriver, self.reporter)
            oHeatingHomePage.navigate_to_heating_control_page()
            oHeatControlPage = androidPage.HeatingControlPage(self.AndroidDriver, self.reporter)
            oHeatControlPage.set_target_temperature(mySetpoint)
        elif 'IOS' in self.client.upper(): 
                oHomePage = iOSPage.HomePage(self.iOSDriver, self.reporter)
                oHomePage.navigate_to_heating_control_page()
                oHeatControlPage = iOSPage.HeatingControlPage(self.iOSDriver, self.reporter)
                oHeatControlPage.set_target_temperature(mySetpoint)
        elif 'WEB' in self.client.upper(): 
            oHoneycombDashboardPayge = webPage.HoneycombDashboardPage(self.WebDriver,self.reporter)
            oHoneycombDashboardPayge.navigate_to_heating_product_page()
            oHeatingPayge = webPage.HeatingPage(self.WebDriver, self.reporter)
            oHeatingPayge.set_target_temperature(mySetpoint)
            self.Web_ManualModeTargTemp = mySetpoint
        self.occupiedHeatingSetpointChanged = True
    def getSchedule(self):
        return self._weeklySchedule
    
    def setSchedule(self, oSchedule):
        if 'ANDROID' in self.client.upper(): 
            if self.type == 'HEAT':
                oHomePage = androidPage.HomePage(self.AndroidDriver, self.reporter)
                oHomePage.navigate_to_heating_home_page()
                oHeatingHomePage = androidPage.HeatingHomePage(self.AndroidDriver, self.reporter)
                oHeatingHomePage.navigate_to_heating_schedule_page()
                oSchedPage= androidPage.HeatingSchedulePage(self.AndroidDriver, self.reporter)
                oSchedPage.set_heating_schedule(oSchedule)
            elif self.type == 'WATER':
                oHomePage = androidPage.HomePage(self.AndroidDriver, self.reporter)
                oHomePage.navigate_to_hot_water_home_page()
                oHotWaterHomePage = androidPage.HotWaterHomePage(self.AndroidDriver, self.reporter)
                oHotWaterHomePage.navigate_to_hot_water_schedule_page()
                oSchedPage= androidPage.HotWaterSchedulePage(self.AndroidDriver, self.reporter)
                oSchedPage.set_hot_water_schedule(oSchedule)
        elif 'IOS' in self.client.upper(): 
            if self.type == 'HEAT':
                oHomePage = iOSPage.HomePage(self.iOSDriver, self.reporter)
                oHomePage.navigate_to_heating_schedule_page()
                oSchedPage= iOSPage.HeatingSchedulePage(self.iOSDriver, self.reporter)
                oSchedPage.set_heating_schedule(oSchedule)
            elif self.type == 'WATER':
                oHomePage = iOSPage.HomePage(self.iOSDriver, self.reporter)
                oHomePage.navigate_to_hot_water_schedule_page()
                oSchedPage= iOSPage.HotWaterSchedulePage(self.iOSDriver, self.reporter)
                oSchedPage.set_hot_water_schedule(oSchedule)
        elif 'WEB' in self.client.upper(): 
            if self.type == 'HEAT':
                oHoneycombDashboardPayge = webPage.HoneycombDashboardPage(self.WebDriver,self.reporter)
                oHoneycombDashboardPayge.navigate_to_heating_product_page()
                oHeatingPayge = webPage.HeatingPage(self.WebDriver, self.reporter)
                oHeatingPayge.set_heating_schedule(self._weeklySchedule, oSchedule)
            elif self.type == 'WATER':
                oHoneycombDashboardPayge = webPage.HoneycombDashboardPage(self.WebDriver,self.reporter)
                oHoneycombDashboardPayge.navigate_to_hot_water_product_page()
                oHotWaterPage = webPage.HotWaterPage(self.WebDriver, self.reporter)
                oHotWaterPage.set_hot_water_schedule(self._weeklySchedule, oSchedule)
                
    def getAttributesFromClient(self):
        if 'ANDROID' in self.client.upper(): 
            if self.type == 'HEAT':
                oHomePage = androidPage.HomePage(self.AndroidDriver, self.reporter)
                oHomePage.navigate_to_heating_home_page()
                oHeatingHomePage = androidPage.HeatingHomePage(self.AndroidDriver, self.reporter)
                oHeatingHomePage.navigate_to_heating_control_page(False)
                oHeatControlPage = androidPage.HeatingControlPage(self.AndroidDriver, self.reporter)
                self.mode, self.thermostatRunningState, self.occupiedHeatingSetpoint = oHeatControlPage.get_heating_attribute()
            elif self.type == 'WATER':
                oHomePage = androidPage.HomePage(self.AndroidDriver, self.reporter)
                oHomePage.navigate_to_hot_water_home_page()
                oHotWaterHomePage = androidPage.HotWaterHomePage(self.AndroidDriver, self.reporter)
                oHotWaterHomePage.navigate_to_hot_water_control_page(False)
                oHotWaterControlPage = androidPage.HotWaterControlPage(self.AndroidDriver, self.reporter)
                self.mode, self.thermostatRunningState, self.occupiedHeatingSetpoint = oHotWaterControlPage.get_hotwater_attribute()
        elif 'IOS' in self.client.upper(): 
            if self.type == 'HEAT':
                oHomePage = iOSPage.HomePage(self.iOSDriver, self.reporter)
                oHomePage.navigate_to_heating_control_page(False)
                oHeatControlPage = iOSPage.HeatingControlPage(self.iOSDriver, self.reporter)
                oHeatControlPage.stopBoost = False
                self.mode, self.thermostatRunningState, self.occupiedHeatingSetpoint = oHeatControlPage.get_heating_attribute()
            if self.type == 'WATER':
                oHomePage = iOSPage.HomePage(self.iOSDriver, self.reporter)
                oHomePage.navigate_to_hot_water_control_page(False)
                oHotWaterControlPage = iOSPage.HotWaterControlPage(self.iOSDriver, self.reporter)
                oHotWaterControlPage.stopBoost = False
                self.mode, self.thermostatRunningState, self.occupiedHeatingSetpoint = oHotWaterControlPage.get_hotwater_attribute()
        elif 'WEB' in self.client.upper(): 
            if self.type == 'HEAT':
                oHoneycombDashboardPayge = webPage.HoneycombDashboardPage(self.WebDriver,self.reporter)
                oHoneycombDashboardPayge.navigate_to_heating_product_page()
                oHeatingPayge = webPage.HeatingPage(self.WebDriver, self.reporter)
                self.mode, self.thermostatRunningState, self.occupiedHeatingSetpoint = oHeatingPayge.get_heating_attribute()
            elif self.type == 'WATER':
                oHoneycombDashboardPayge = webPage.HoneycombDashboardPage(self.WebDriver,self.reporter)
                oHoneycombDashboardPayge.navigate_to_hot_water_product_page()
                oHotWaterPage = webPage.HotWaterPage(self.WebDriver, self.reporter)
                self.mode, self.thermostatRunningState, self.occupiedHeatingSetpoint = oHotWaterPage.get_hotwater_attribute()
            
    def getHeatRule(self):

        ALAPI.createCredentials(self.serverName, self.client)
        session  = ALAPI.sessionObject()
        if session.latestSupportedApiVersion != '6':
            self.platformVersion = 'V5'
            print("hello")
            return False
        else:
            self.platformVersion = 'V6'
            rules = ALAPI.getRulesV6(session)
        #print(rules)
        #print(rules['rules'])

        oHeatRuleDict = {}
        heatRuleCount = 0
        if (rules['rules']):
            for oActions in rules['rules']:
                oRuleList=[]
                if oActions['name'] in ('TooHot','TooCold'):
                    heatRuleCount=heatRuleCount+1
                    #print('Rule : ' + oActions['name'])
                    #return oActions['name']
                    #print(" : ",end='')
                    for status in oActions['actions']:
                        #print(status['status'],end='')
                        #print(" : ",end='')
                        types = status['type']
                        for values in oActions['triggers']:
                            #print(values['value']+' : '+types)
                            #print('\n')
                            #oRuleList.append((values['value'],types,status['status']))
                            oRuleList.append(values['value'])
                            oRuleList.append(types)
                            oRuleList.append(status['status'])
                            oHeatRuleDict.update({oActions['name']:oRuleList})
                            if(heatRuleCount==0):
                                print('No Heating Rules are set')
            
        else:
            print('No rules are set')
            
        print(oHeatRuleDict)
        print('\n')
        
        return oHeatRuleDict
    
    def navigateToScreen(self,strPageName):
            oAccDetPage = androidPage.AccountDetails(self.AndroidDriver, self.reporter)
            oAccDetPage.open_acc_details(strPageName)
            
    def changePasswordScreen(self):
        if 'IOS' in self.client.upper():
            oHomePage = iOSPage.HomePage(self.iOSDriver, self.reporter)
            oHomePage.navigate_to_screen('Change Password')
            oChngPassPage = iOSPage.SetChangePassword(self.iOSDriver, self.reporter)
            oChngPassPage.change_password()
        if 'ANDROID' in self.client.upper():
            oHomePage = androidPage.HomePage(self.AndroidDriver, self.reporter)
            oHomePage.navigate_to_screen('Change Password')
            oChngPassPage = androidPage.SetChangePassword(self.AndroidDriver, self.reporter)
            oChngPassPage.change_password()
            
    def navigateToHoildayScreen(self,context):
     
        if 'Android' in self.client.upper():
            oHolidayPage = androidPage.HolidayMode(self.AndroidDriver,self.reporter)
            oHolidayPage.navigateToHoildayScreen(context)
        elif 'IOS' in self.client.upper(): 
            oHolidayPage=iOSPage.HolidayMode(self.iOSDriver, self.reporter)
            oHolidayPage.navigate_To_HolidayScreen(context)       
            
    def setHolidayMode(self,context, strHolidayStart, strHolidayStartTime, strDuration):   
        oHolidayPage = androidPage.HolidayMode(self.AndroidDriver,self.reporter)
        oHolidayPage.setHoildayMode(context, strHolidayStart, strHolidayStartTime, strDuration)
        
        if 'Android' in self.client.upper():
            oHolidayPage = androidPage.HolidayMode(self.AndroidDriver,self.reporter)
            oHolidayPage.setHoildayMode(context, strHolidayStart, strHolidayStartTime, strDuration)
        elif 'IOS' in self.client.upper():
            oHolidayPage=iOSPage.HolidayMode(self.iOSDriver, self.reporter)
            #oHolidayPage.set_Holiday_Mode(context, strHolidayStartDate, strHolidayStartTime, strHolidayEndDate, strHolidayEndTime, strClientType)
        
    def activateHolidayMode(self,context):
        print('hi')
    
    
    def verifyHolidayMode(self,context):
        print('hi')

    def navigate_to_settingScreen(self,strPageName):        
        if 'WEB' in self.client.upper():
            oLandingPage = webPage.BasePage(self.WebDriver, self.reporter)
            oLandingPage.navigate_to_settingScreen(strPageName)
        if 'ANDROID' in self.client.upper():
            print('test successful')
        
       
    def setHighNotification(self,oTargetHighTemp,oTargetLowTemp='',oBothAlert='No'):    
        if 'WEB' in self.client.upper():
            oAlertType = webPage.SetNotification(self.WebDriver,self.reporter)
            oAlertType.set_high_temperature(oTargetHighTemp,oTargetLowTemp,oBothAlert)
        if 'IOS' in self.client.upper():
            oLandingPage = iOSPage.SaveHeatingNotification(self.iOSDriver, self.reporter)
            oLandingPage.naivgate_to_ZoneNotificaiton()
            oLandingPage.setHighTemperature(oTargetHighTemp)
        if 'ANDROID' in self.client.upper():
            oLandingPage = androidPage.SaveHeatingNotification(self.AndroidDriver, self.reporter)
            oLandingPage.naivgate_to_ZoneNotificaiton()
            oLandingPage.setHighTemperature(oTargetHighTemp)
            

    def setLowNotification(self,oTargetLowTemp='',oBothAlert='No'):    
        if 'WEB' in self.client.upper():
            oAlertType = webPage.SetNotification(self.WebDriver,self.reporter)
            oAlertType.set_low_temperature(oTargetLowTemp,'Yes')
        if 'IOS' in self.client.upper():
            oLandingPage = iOSPage.SaveHeatingNotification(self.iOSDriver, self.reporter)
            oLandingPage.setLowTemperature(oTargetLowTemp)
            oLandingPage.receiveWarnings()
        if 'ANDROID' in self.client.upper():
            oLandingPage = androidPage.SaveHeatingNotification(self.AndroidDriver, self.reporter)
            oLandingPage.naivgate_to_ZoneNotificaiton()
            oLandingPage.setLowTemperature(oTargetLowTemp)
            oLandingPage.receiveWarnings()

           
    def setNotificationOnOff(self,strNotiState,strNotiType='Both'):    
        if 'WEB' in self.client.upper():
            oAlertType = webPage.SetNotification(self.WebDriver,self.reporter)
            oAlertType.setNotificationOnOff(strNotiState)
        if 'IOS' in self.client.upper():
            oLandingPage = iOSPage.SaveHeatingNotification(self.iOSDriver, self.reporter)
            oLandingPage.setNotificationONtoOFF(strNotiState)
        if 'ANDROID' in self.client.upper():
            oLandingPage = androidPage.SaveHeatingNotification(self.AndroidDriver, self.reporter)
            oLandingPage.naivgate_to_ZoneNotificaiton()
            oLandingPage.setNotificationONtoOFF(strNotiState)
            
            
    def getNotificationTempFromUI(self):
        if 'WEB' in self.client.upper():
            oAlertType = webPage.SetNotification(self.WebDriver,self.reporter)
            strExpectedTemp = oAlertType.getNotificationTempFromUI()
            return strExpectedTemp 
        
        
    def navigatetoContactSensor(self,nameContactSensor):
        if 'IOS' in self.client.upper():
            #if self.type == 'SENSOR':
                cLandingPage = iOSPage.ContactSensors(self.iOSDriver,self.reporter)
                print(self.reporter.strResultsPath)
                cLandingPage.navigate_to_contact_sensor(nameContactSensor)
    
    def currentCSStatus(self,nameContactSensor):
        if 'IOS' in self.client.upper():
                cLandingPage = iOSPage.ContactSensors(self.iOSDriver,self.reporter)
                #print(self.reporter.strResultsPath)
                currentStatus = cLandingPage.contactSensorCurrentStatus(nameContactSensor)
                return currentStatus
    
    def accessTodaysLog(self):
        if 'IOS' in self.client.upper():
            oTodaysLogPage = iOSPage.ContactSensors(self.iOSDriver,self.reporter)
            oTodaysLogPage.todaysLog()
            
    def eventLogScreen(self,selectWeekDay):
        if 'IOS' in self.client.upper():
            oEventLogScreen = iOSPage.ContactSensors(self.iOSDriver,self.reporter)
            oEventLogScreen.navigate_to_selected_weekday_log(selectWeekDay)
            
    def verfiyEventLogs(self):
        if 'IOS' in self.client.upper():
            oLogScreen = iOSPage.ContactSensors(self.iOSDriver,self.reporter)
            oLogScreen.verify_todayevent_logs()
            
            
    def navigateToDeviceScreen(self,nameMotionSensor):
        if 'IOS' in self.client.upper():
            oLogScreen = iOSPage.MotionSensor(self.iOSDriver,self.reporter)
            oLogScreen.navigate_to_motionsensor(nameMotionSensor)
        

    def setLocalValues(self,Settings,Value):
        if 'IOS' in self.client.upper():
            oLogScreen = iOSPage.ColourLights(self.iOSDriver,self.reporter)
            oLogScreen.setValues(Settings,Value)

    def navigateToDesiredSettings(self,Settings):
        if 'IOS' in self.client.upper():
            oLogScreen = iOSPage.ColourLights(self.iOSDriver,self.reporter)
            oLogScreen.navigateToSettings(Settings)

    def setValueForBulbBySwiping(self,Settings,Value):
        if 'IOS' in self.client.upper():
            oLogScreen = iOSPage.ColourLights(self.iOSDriver,self.reporter)
            oLogScreen.setValueForBulb(Settings,Value)

    def verifyValueInAPI(self,buldNodeID):
        if 'IOS' in self.client.upper():
            oLogScreen = iOSPage.ColourLights(self.iOSDriver,self.reporter)
            oLogScreen.verifyAPI(buldNodeID)     
           
        
        
        
        
        