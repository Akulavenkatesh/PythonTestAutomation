'''
Created on 26 Jun 2015

@author: ranganathan.veluswamy
'''
import os
import time

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from steps.EE_Locators_iOSApp import EditTimeSlotPageLocators
from steps.EE_Locators_iOSApp import HeatingControlPageLocators
from steps.EE_Locators_iOSApp import HomePageLocators
from steps.EE_Locators_iOSApp import HotWaterControlPageLocators
from steps.EE_Locators_iOSApp import LoginPageLocators
from steps.EE_Locators_iOSApp import SchedulePageLocators
import steps.FF_alertmeApi as ALAPI
global iOSDriver
EXPLICIT_WAIT_TIME = 20

class iOS(object):

    def setUp(self):
        
        #strResponse = {"meta":{},"links":{},"linked":{},"nodes":[{"id":"bfdd6417-0731-47fb-ba3e-759dad1dd5b0","href":"https://api.staging.zoo.alertme.com:443/omnia/nodes/bfdd6417-0731-47fb-ba3e-759dad1dd5b0","links":{},"name":"Your Receiver","parentNodeId":"1249da59-48c8-4aaa-8134-0a2d1a359042","attributes":{}},{"id":"01354ca1-01bd-47c6-984b-3b9c766330de","href":"https://api.staging.zoo.alertme.com:443/omnia/nodes/01354ca1-01bd-47c6-984b-3b9c766330de","links":{},"name":"Your Receiver","parentNodeId":"bfdd6417-0731-47fb-ba3e-759dad1dd5b0","attributes":{}},{"id":"5e4de5e6-2ba8-47c6-afde-e57daa5af056","href":"https://api.staging.zoo.alertme.com:443/omnia/nodes/5e4de5e6-2ba8-47c6-afde-e57daa5af056","links":{},"name":"Your Receiver","parentNodeId":"bfdd6417-0731-47fb-ba3e-759dad1dd5b0","attributes":{}},{"id":"bb8cf8a8-1029-49fd-bdbf-4691dc6b41a8","href":"https://api.staging.zoo.alertme.com:443/omnia/nodes/bb8cf8a8-1029-49fd-bdbf-4691dc6b41a8","links":{},"name":"Your Thermostat","parentNodeId":"1249da59-48c8-4aaa-8134-0a2d1a359042","attributes":{}},{"id":"1249da59-48c8-4aaa-8134-0a2d1a359042","href":"https://api.staging.zoo.alertme.com:443/omnia/nodes/1249da59-48c8-4aaa-8134-0a2d1a359042","links":{},"parentNodeId":"1249da59-48c8-4aaa-8134-0a2d1a359042","attributes":{}}]}
        
        '''    
        #Login and get HubID
        ALAPI.createCredentials('isopStage', 'WEB')
        resp = ALAPI.loginV6()
        resp = ALAPI.getNodes()
        print(resp)
        strHubID = resp[1]
        exit()'''
        
        
        desired_caps = {}
        desired_caps['appium-version'] = '1.0'
        desired_caps['platformName'] = 'iOS'
        desired_caps['platformVersion'] = '9.2'
        desired_caps['deviceName'] = 'iPhone 6 Plus'
        desired_caps['udid'] = '8d25ba7d4a8f82f1a32cc35d907ad2a928b6e808'
        desired_caps['app'] = os.path.abspath('/Users/ranganathan.veluswamy/Desktop/Ranga/Workspace/EclipseWorkspace/HiveTestAutomation/02_Manager_Tier/EnviromentFile/Apps/iOS/isopBeta/Hive_new.ipa')
        desired_caps['noReset'] = True
        iOSDriver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        self.iOSDriver = iOSDriver
        '''
        iOSDriver.implicitly_wait(60)
        textfield = iOSDriver.find_elements_by_name("Username")[1]
        text = 'ranga@yopmail.com'
        iOSDriver.execute_script("au.getElement('%s').setValue('%s')" % (textfield.id, text))
        
        textfield = iOSDriver.find_elements_by_name("Password")[1]
        text = 'password1'
        iOSDriver.execute_script("au.getElement('%s').setValue('%s')" % (textfield.id, text))
        
        iOSDriver.find_element_by_name("Log in").click()
        
        
        iOSDriver.find_elements_by_name("Username")[1].click()
        iOSDriver.find_elements_by_name("Username")[1].send_keys('ranga@yopmail.com')
        iOSDriver.find_elements_by_name("Password")[1].click()
        iOSDriver.find_elements_by_name("Password")[1].send_keys('password1')
        iOSDriver.find_elements_by_name("Log in")[1].click()
        '''
        '''
        iOSDriver.find_element_by_xpath("//*[@label='Username']").send_keys('ranga@yopmail.com')
        iOSDriver.find_element_by_xpath("//*[@label='Password']").send_keys('password1')
        iOSDriver.find_element_by_xpath("//*[@label='Log in']").click()
           
        elif 'SELECTED' in iOSDriver.find_element_by_xpath("//*[contains(@label, 'Schedule')]").text.upper(): 
            print('Scedule is selected')
        elif 'SELECTED' in iOSDriver.find_element_by_xpath("//*[contains(@label, 'Manual')]").text.upper(): 
            print('Manual is selected')     
        elif 'SELECTED' in iOSDriver.find_element_by_xpath("//*[contains(@label, 'Off')]").text.upper(): 
            print('Off is selected')       
        '''
    
        
    
        #Get Hot Water Attributes
        strScreenName = iOSDriver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name')
        print(strScreenName)
        if 'HOT WATER BOOST' in strScreenName.upper():
            strMode = 'BOOST'
            if self.wait_for_element_exist(*HotWaterControlPageLocators.RUNNING_STATE_ON): strRunningState = 'ON'
            else: strRunningState = 'OFF'
        else: 
            strSelectedModeLabel = iOSDriver.find_element(*HotWaterControlPageLocators.SELECTED_MODE_LINK).text.upper()
            print(strSelectedModeLabel)
            if 'HOT WATER MODE SCHEDULE' in strSelectedModeLabel: 
                strMode = 'AUTO'
                if self.wait_for_element_exist(*HotWaterControlPageLocators.RUNNING_STATE_ON): strRunningState = 'ON'
                else: strRunningState = 'OFF'
            elif 'HOT WATER MODE ON' in strSelectedModeLabel: 
                strMode = 'ON'
                if self.wait_for_element_exist(*HotWaterControlPageLocators.RUNNING_STATE_ON): strRunningState = 'ON'
                else: strRunningState = 'OFF'
            elif 'HOT WATER MODE OFF' in strSelectedModeLabel: 
                strMode = 'OFF'
                if self.wait_for_element_exist(*HotWaterControlPageLocators.RUNNING_STATE_OFF): strRunningState = 'OFF'
                else: strRunningState = 'ON'
            
        print(strMode, strRunningState)
        input("hi")
        iOSDriver.quit()
        exit()
      
        #Heating Attributes
        strScreenName = iOSDriver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name')
        if 'HEATING BOOST' in strScreenName.upper():
            strMode = 'BOOST'
        else: 
            strSelectedModeLabel = iOSDriver.find_element(*HeatingControlPageLocators.SELECTED_MODE_LINK).text.upper()
            print(strSelectedModeLabel)
            if 'HEATING MODE SCHEDULE' in strSelectedModeLabel: 
                strMode = 'AUTO'
            elif 'HEATING MODE MANUAL' in strSelectedModeLabel: 
                strMode = 'MANUAL'
            elif 'HEATING MODE OFF' in strSelectedModeLabel: 
                strMode = 'OFF'
                
        oScrolElement = iOSDriver.find_element(*HeatingControlPageLocators.TARGET_TEMPERATURE_SCROLL)
        oScrolElementVAlue = oScrolElement.get_attribute('value')
        if 'point' in oScrolElementVAlue: fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[0] + '.' + oScrolElementVAlue.split(' ')[2])
        else: fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[0])
        
        strFlameLabel = iOSDriver.find_element(*HeatingControlPageLocators.FLAME_ICON).text.upper()
        print(strFlameLabel)
        if 'ON' in strFlameLabel: strRunningState = 'ON'
        elif 'OFF' in strFlameLabel: strRunningState = 'OFF'
        
        print(strMode, strRunningState, fltCurrentTargTemp)
        iOSDriver.quit()
        exit()
        
  
            
     
        
       
        
        
        
        #Heating, current inside temperature
        iOSDriver.quit()
        exit()
        input('hi')
        oel =iOSDriver.find_elements_by_xpath("//UIAButton[contains(@name, 'Hot water o')]")
        #oel = oel.find_element_by_xpath("//*[contains(@name, 'Hot water o')]")
        #oScrolElement = iOSDriver.find_element_by_xpath("//*[contains(@label,'Your heating schedule')]")
        iOSDriver.swipe(200, 200, 200, 500, 500)
        #scroll_element_to_value(oScrolElement, 2, 1, 1, 0.1)
        
        
        oEL = iOSDriver.find_element_by_xpath("//*[contains(@label, 'Manual')]")
        time.sleep(5)
        action = TouchAction(oEL.parent)
        action.press(oEL).perform()
        
        time.sleep(5)
        
        iOSDriver.quit()
        
    def wait_for_element_exist(self,by, value, intWaitTime = 0):
        if intWaitTime == 0: intWaitTime = EXPLICIT_WAIT_TIME
        try:
            wait = WebDriverWait(self.iOSDriver, intWaitTime)
            wait.until(EC.presence_of_element_located((by, value)))
            time.sleep(1)
            return True
        except TimeoutException:
            return False
        print(by, value, 'element not found')
        #Heating, current inside 
    def scroll_element_to_value(self,oScrolElement, fltCurrentValue, fltSetValue, fltPrecision, fltScrolPrecesion):
        intLeftX = oScrolElement.location['x']
        intUpperY = oScrolElement.location['y']
        intWidth = oScrolElement.size['width']
        intHieght = oScrolElement.size['height']
        intStX = intLeftX + intWidth/2
        intStY = intUpperY + fltScrolPrecesion* (intHieght/4)
        intEndX = intStX
        intEndY = intUpperY + 3*(intHieght/4)
        if not fltSetValue==fltCurrentValue:
            if fltSetValue < fltCurrentValue:
                intTemp = intEndY
                intEndY = intStY
                intStY = intTemp
            intIterCount = int(abs(fltSetValue-fltCurrentValue)/fltPrecision)
            for intCnt in range(intIterCount):
                oScrolElement.parent.swipe(intStX, intEndY, intEndX, intStY, 1000)
                time.sleep(0.5)
        
        input("Hi")
if __name__ == '__main__':
    ios = iOS()
    ios.setUp()
    
