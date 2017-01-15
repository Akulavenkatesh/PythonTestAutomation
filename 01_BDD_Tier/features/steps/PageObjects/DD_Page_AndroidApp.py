'''
Created on 16 Jun 2015

@author: ranganathan.veluswamy
'''

#from element import BasePageElement
import os
import time
import traceback

from appium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from EE_Locators_AndroidApp import LoginPageLocators, HomePageLocators, HeatingControlPageLocators, HotWaterControlPageLocators, SchedulePageLocators, EditTimeSlotPageLocators, EditBoostTimePageLocators,AccountDetailsLocators,HeatingHomePageLocators,HotWaterHomePageLocators,HolidayModeLocators,ChangePasswordLocators ,\
    LogoutLocators, TextControlLocators, HoneycombDasbordLocators,HeatingNotificationsLocators,PinLock,MotionSensorLocators
import FF_utils as utils
import FF_ScheduleUtils as oSchedUtils
from datetime import timedelta
from datetime import datetime


class BasePage(object):

    #Contructor for BasePage
    def __init__(self, driver, reporter):
        self.driver = driver
        self.reporter = reporter 
        self.EXPLICIT_WAIT_TIME = 25
        self.currentAppVersion = utils.getAttribute('common', 'currentAppVersion').upper()
        #Set the object property value based on app veersion
        if self.currentAppVersion == 'V6':
            self.REFRESH_BUTTON = HomePageLocators.REFRESH_BUTTON_V6
            self.MENU_BUTTON = HomePageLocators.MENU_BUTTON_V6
            self.OFF_MODE_LINK = HeatingControlPageLocators.OFF_MODE_LINK_V6
            self.RUNNING_STATE_CIRCLE = HotWaterControlPageLocators.RUNNING_STATE_CIRCLE_V6
            self.CH_BOOST_MODE_LINK = HeatingControlPageLocators.BOOST_MODE_LINK_V6
            self.HW_BOOST_MODE_LINK = HotWaterControlPageLocators.BOOST_MODE_LINK_V6
            self.ADD_BUTTON = EditTimeSlotPageLocators.ADD_BUTTON_V6            
            
        else:
            self.REFRESH_BUTTON = HomePageLocators.REFRESH_BUTTON
            self.MENU_BUTTON = HomePageLocators.MENU_BUTTON
            self.OFF_MODE_LINK = HeatingControlPageLocators.OFF_MODE_LINK
            self.RUNNING_STATE_CIRCLE = HotWaterControlPageLocators.RUNNING_STATE_CIRCLE
            self.CH_BOOST_MODE_LINK = HeatingControlPageLocators.BOOST_MODE_LINK
            self.HW_BOOST_MODE_LINK = HotWaterControlPageLocators.BOOST_MODE_LINK
            self.ADD_BUTTON = EditTimeSlotPageLocators.ADD_BUTTON
    
    
    #Waits for the given element exists for EXPLICIT_WAIT_TIME 
    def wait_for_element_exist(self, by, value, intWaitTime = 0):
        if intWaitTime == 0: intWaitTime = self.EXPLICIT_WAIT_TIME
        try:
            wait = WebDriverWait(self.driver, intWaitTime)
            wait.until(EC.presence_of_element_located((by, value)))
            time.sleep(1)
            return True
        except TimeoutException:
            print(by, value, 'element not found')
            return False
        
    #Waits for the given element exists for EXPLICIT_WAIT_TIME 
    def wait_for_element_exist_for_given_time(self, by, value, intWaitTime = 0):
        if intWaitTime == 0: intWaitTime = self.EXPLICIT_WAIT_TIME
        intWaitTime = 4
        intCntr = 0
        boolElementExist = False
        while not (intCntr > intWaitTime or boolElementExist):
            try:
                #oElement = self.driver.find_element(by, value)
                boolElementExist = True
            except:
                boolElementExist = False
                intCntr += 1
                time.sleep(1)
        if boolElementExist: return True
        else: return False
        
    #Initializes the Appium Android Web Driver
    def setup_android_driver(self, strAndroidPlatformVersion, strDeviceName, strAppPath):
        desired_caps = {}
        desired_caps['appium-version'] = '1.4.8'
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = strAndroidPlatformVersion
        desired_caps['deviceName'] = strDeviceName
        desired_caps['app'] = os.path.abspath(strAppPath)
        desired_caps['appPackage'] = utils.getAttribute('android', 'appPackage')
        desired_caps['appActivity'] = utils.getAttribute('android', 'appActivity')
        desired_caps['udid'] = utils.getAttribute('android', 'appium_udid')
        desired_caps['noReset'] = True
        strPort = utils.getAttribute('common', 'appium_port')
        if strPort == "": strPort = "4723"
        print('using Port', strPort)
        intNumb = strPort[3:]
        print('http://127.0.0.' + intNumb + ':' + strPort + '/wd/hub')
        #oAndroidDriver = webdriver.Remote('http://127.0.0.' + intNumb + ':' + strPort + '/wd/hub', desired_caps)
        oAndroidDriver = webdriver.Remote('http://127.0.0.1:' + strPort + '/wd/hub', desired_caps)
        
        '''desired_caps = {}
        desired_caps['browserName'] = ""
        desired_caps['appiumVersion'] = "1.4.13"
        desired_caps['deviceName'] = "LG Nexus 4 Emulator"
        desired_caps['deviceOrientation'] = "portrait"
        desired_caps['platformVersion'] = "4.4"
        desired_caps['platformName'] = "Android"
        desired_caps['app'] = "sauce-storage:intProd46.apk"
        desired_caps["noReset"] = True
    
        oAndroidDriver = webdriver.Remote(command_executor="http://BGCHIS:3c0fd44d-951a-48b4-aa77-80fe20904233@ondemand.saucelabs.com:80/wd/hub", desired_capabilities = desired_caps)
        '''
        oAndroidDriver.implicitly_wait(60)
        
        return oAndroidDriver
    
    #Report the Failure step the HTML report
    def report_fail(self, strFailDescription):    
        self.reporter.ActionStatus = False
        self.reporter.ReportEvent('Test Validation', strFailDescription, "FAIL", 'Center', True, self.driver)
    
    #Report the Pass step the HTML report
    def report_pass(self, strPassDescription):    
        self.reporter.ActionStatus = True
        self.reporter.ReportEvent('Test Validation', strPassDescription, "PASS", 'Center', True, self.driver)
    
    #Report the Done step the HTML report
    def report_done(self, strStepDescription):    
        self.reporter.ActionStatus = True
        self.reporter.ReportEvent('Test Validation', strStepDescription, "DONE", 'Center', True, self.driver)
        
    #Report the Done step the HTML report
    def report_step(self, strStepDescription):    
        self.reporter.ActionStatus = True
        self.reporter.ReportEvent('Test Validation', strStepDescription, "DONE", 'Center', True)
    
    
    #Scrolls on the Scrollable element to set the specific value passed 
    ''' def scroll_element_to_value(self, oScrolElement, fltCurrentValue, fltSetValue, fltPrecision, fltScrolPrecesion):
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
                self.driver.swipe(intStX, intEndY, intEndX, intStY, 1000)
                time.sleep(0.5)'''
            
    #Add/Delete Events to match the expected count
    def add_or_remove_events(self, intExpectedEventCount): 
        if self.reporter.ActionStatus:
            self.report_done('Android-App : ScreenShot of existing schedule')
            #Get Event Count
            lstMoreOptions = self.driver.find_elements(*SchedulePageLocators.EVENT_OPTIONS_BUTTON)
            intActualCount = len(lstMoreOptions)
            print(intActualCount, intExpectedEventCount)
            if intActualCount > intExpectedEventCount:
                #Delete Event
                self.report_step('Deleting additional events')
                for intCntr in range((intActualCount -1), intExpectedEventCount-1, -1):
                    #input('KK')
                    lstMoreOptions[intCntr].click()
                    self.report_done('Android-App : Deleting additional event number : ' + str(intCntr + 1))
                    self.driver.find_element(*SchedulePageLocators.DELETE_EVENT_SUBMENU).click()  
                    self.wait_for_element_exist(*self.REFRESH_BUTTON)
            elif intActualCount < intExpectedEventCount:
                #Add Event
                self.report_step('Adding additional events')
                for intCntr in range((intExpectedEventCount - 1), intActualCount - 1, -1):
                    self.driver.find_element(*SchedulePageLocators.SCHEDULE_OPTIONS_BUTTON).click() 
                    self.wait_for_element_exist(*SchedulePageLocators.ADD_TIME_SLOT_SUBMENU)
                    self.driver.find_element(*SchedulePageLocators.ADD_TIME_SLOT_SUBMENU).click() 
                    self.report_done('Android-App : Adding additional event number : ' + str(intCntr + 1))
                    self.driver.find_element(*self.ADD_BUTTON).click()  
                    self.wait_for_element_exist(*self.REFRESH_BUTTON)
            
            self.driver.find_element(*self.REFRESH_BUTTON).click()
            time.sleep(5)
            self.wait_for_element_exist(*self.REFRESH_BUTTON)
            self.report_pass('Android-App : ScreenShot after all additional events are added/removed')

#Navigate to the Day of the Week
    def _navigate_to_day(self, strDay):     
        if self.reporter.ActionStatus:
            try:   
                if strDay.upper() == 'MON': self.driver.find_element(*SchedulePageLocators.MON_SCHEDULE_BUTTON).click()
                elif strDay.upper() == 'TUE': self.driver.find_element(*SchedulePageLocators.TUE_SCHEDULE_BUTTON).click()
                elif strDay.upper() == 'WED': self.driver.find_element(*SchedulePageLocators.WED_SCHEDULE_BUTTON).click()
                elif strDay.upper() == 'THU': self.driver.find_element(*SchedulePageLocators.THU_SCHEDULE_BUTTON).click()
                elif strDay.upper() == 'FRI': self.driver.find_element(*SchedulePageLocators.FRI_SCHEDULE_BUTTON).click()
                elif strDay.upper() == 'SAT': self.driver.find_element(*SchedulePageLocators.SAT_SCHEDULE_BUTTON).click()
                elif strDay.upper() == 'SUN': self.driver.find_element(*SchedulePageLocators.SUN_SCHEDULE_BUTTON).click()
                
                self.driver.find_element(*self.REFRESH_BUTTON).click()
                time.sleep(5)
                self.wait_for_element_exist(*self.REFRESH_BUTTON)
            
            except:
                self.report_fail('Android App : NoSuchElementException: in _navigate_to_day Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
                
            
    #Set the Even Target temperature
    def set_schedule_event_hour(self, intSetHour): 
        if self.reporter.ActionStatus:
            try: 
                if self.wait_for_element_exist(*EditTimeSlotPageLocators.HOUR_SCROLL):
                    oScrolElement = self.driver.find_element(*EditTimeSlotPageLocators.HOUR_SCROLL)
                    intSetHour = int(intSetHour)
                    intCurrentHour = int(oScrolElement.find_element(*EditTimeSlotPageLocators.NUMBER_INSDE_SCROLL_ITEM).get_attribute('name'))  

                    self.scroll_element_to_value(oScrolElement, intCurrentHour, intSetHour, 1, 1.8)
                else:
                    self.report_fail("Android-App : Control not active on the Edit Time Slot for schedule Page to set the Event start time Hour")
                
            except:
                self.report_fail('Android App : NoSuchElementException: in set_schedule_event_hour Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
                
                
    #Set the Boost Time
    def set_boost_time_duration(self, intSetHour): 
        if self.reporter.ActionStatus:
            try: 
                
                self.driver.find_element(*HeatingControlPageLocators.BOOST_TIMER).click()
                time.sleep(2)
                if self.wait_for_element_exist(*EditBoostTimePageLocators.BOOST_TIME_SCROLL):
                    oScrolElement = self.driver.find_element(*EditBoostTimePageLocators.BOOST_TIME_SCROLL)
                    intSetHour = int(intSetHour)
                    if intSetHour == 0.5: intSetHour = 0
                    intCurrentHour = oScrolElement.find_element(*EditTimeSlotPageLocators.NUMBER_INSDE_SCROLL_ITEM).get_attribute('name')  
                    if '30' in intCurrentHour: intCurrentHour = 0
                    else: intCurrentHour = int(intCurrentHour.split(' ')[0])
                    self.scroll_element_to_value(oScrolElement, intCurrentHour, intSetHour, 1, 1.8)
                    self.driver.find_element(*EditBoostTimePageLocators.SAVE_BUTTON).click()
                    
                else:
                    self.report_fail("Android-App : Control not active on the Edit Boost Time for schedule Page to set the Boost duration Hour")
                
            except:
                self.report_fail('Android App : Exception: in set_boost_time_duration Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
                
                
    #Set the Even Target temperature
    def set_schedule_event_minute(self, intSetMinute): 
        if self.reporter.ActionStatus:
            try: 
                if self.wait_for_element_exist(*EditTimeSlotPageLocators.MINUTE_SCROLL):
                    oScrolElement = self.driver.find_element(*EditTimeSlotPageLocators.MINUTE_SCROLL)
                    intSetMinute = int(intSetMinute)
                    intCurrentMinute = int(oScrolElement.find_element(*EditTimeSlotPageLocators.NUMBER_INSDE_SCROLL_ITEM).get_attribute('name'))  
                    self.scroll_element_to_value(oScrolElement, intCurrentMinute, intSetMinute, 15, 1.8)
                    
                else:
                    self.report_fail("Android-App : Control not active on the Edit Time Slot for Heating schedule Page to set the Event start time Minute")
                
            except:
                self.report_fail('Android App : NoSuchElementException: in set_schedule_event_hour Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
                
    #Refresh Page
    def refresh_page(self):
        try:          
            self.driver.find_element(*self.REFRESH_BUTTON).click()
            time.sleep(5)
            self.wait_for_element_exist(*self.REFRESH_BUTTON)
        except:
            self.report_fail('Android App : NoSuchElementException: in refresh_page Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
    
    #replace a object's xpath value in runtime
    def set_TO_property(self,tplObject, propName, propValue): 
        lst = list(tplObject)
        lst[1] = str(lst[1]).replace(propName, propValue)
        return tuple(lst)
    
            
#Page Class for Login page. Has all the methods for the Login page

class LoginPage(BasePage):
    #Log in to the Hive Mobile App
    def login_hive_app(self, strUserName, strPassword): 
        if self.reporter.ActionStatus:
            #self.driver.reset()
            try: 
                if self.wait_for_element_exist(*HomePageLocators.SKIP_BUTTON):
                    self.driver.find_element(*HomePageLocators.SKIP_BUTTON).click()
                if self.wait_for_element_exist(*LoginPageLocators.TITLE_LABEL):
                    self.driver.find_element(*LoginPageLocators.USERNAME_EDTBOX).send_keys(strUserName)
                    self.driver.hide_keyboard()
                    self.driver.find_element(*LoginPageLocators.PASSWORD_EDTBOX).send_keys(strPassword)
                    self.driver.hide_keyboard()
                    self.driver.find_element(*LoginPageLocators.LOGIN_BUTTON).click()
                if self.wait_for_element_exist(*HoneycombDasbordLocators.HONEYCOMB_SHOW_DASHBOARD):
                    self.driver.find_element(*HoneycombDasbordLocators.HONEYCOMB_SHOW_DASHBOARD).click()
                    
                    if self.wait_for_element_exist(*self.REFRESH_BUTTON): 
                        self.report_pass('Android-App : The Hive App is successfully Logged in')
                    else:
                        self.report_fail('Android App : The Hive App is not logged in. Please check the Login credentials and re-execute test.')                
                    
                #else:
                    #self.report_fail('Android App : The Hive App is either not Launched or the Login screen is not displayed. Please check and re-execute test.')
                    
            except:
                self.report_fail('Android App : NoSuchElementException: in login_hive_app Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
                

#Page Class for Home page. Has all the methods for the Home page
class HomePage(BasePage):
    #Navigates to the Heating Home Page
    def navigate_to_heating_home_page(self): 
        if self.reporter.ActionStatus:
            try:
                if not self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper().find('HEATING') >= 0:
                    print(self.driver.find_element(*HomePageLocators.CURRENT_TITLE).text)
                    if self.currentAppVersion == 'V6':
                            time.sleep(2)   
                            self.driver.find_element(*HomePageLocators.MENU_BUTTON_SHOW).click()
                            if self.wait_for_element_exist(*HomePageLocators.HEAT_WATER_MAIN_MENU):
                                self.driver.find_element(*HomePageLocators.HEAT_WATER_MAIN_MENU).click()
                                time.sleep(2)                                
                                if self.wait_for_element_exist(*HoneycombDasbordLocators.HONEYCOMB_HEATING_ON):
                                    self.driver.find_element(*HoneycombDasbordLocators.HONEYCOMB_HEATING_ON).click()
                                elif self.wait_for_element_exist(*HoneycombDasbordLocators.HONEYCOMB_HEATING_OFF):
                                        self.driver.find_element(*HoneycombDasbordLocators.HONEYCOMB_HEATING_OFF).click()          
                                        time.sleep(2)
                    if self.wait_for_element_exist(*HeatingControlPageLocators.TARGET_TEMPERATURE_SCROLL):
                            self.report_pass('Android-App : Successfully navigated to the Heating Home Page')
                    else:
                            self.report_fail('Android App : Unable to navigate to Heating Home Page')
                               
            except:
                self.report_fail('Android App : NoSuchElementException: in navigate_to_heating_homepage Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
    
    
    #Navigates to the Hot water Home Page
    def navigate_to_hot_water_home_page(self): 
        if self.reporter.ActionStatus:
            try: 
                print("1")
                if not self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper().find('HOT WATER') >= 0:
                    print("2")
                    print(self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name'))
                    if self.currentAppVersion == 'V6':
                            print("3")
                            time.sleep(2) 
                            self.driver.find_element(*HomePageLocators.MENU_BUTTON_SHOW).click()
                            if self.wait_for_element_exist(*HomePageLocators.HEAT_WATER_MAIN_MENU):  
                                    print("4")                          
                                    self.driver.find_element(*HomePageLocators.HEAT_WATER_MAIN_MENU).click()
                                    time.sleep(2) 
                                    print("5")
                                    time.sleep(2)
                                    if self.wait_for_element_exist(*HomePageLocators.HOT_WATER_SUBMENU):
                                        self.driver.find_element(*HomePageLocators.HOT_WATER_SUBMENU).click()      
                                        time.sleep(3)
                                        if self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper().find('HOT WATER') >= 0:
                                            self.report_pass('Android-App : Successfully navigated to the Hot Water Home Page')
                    else:
                            self.report_fail('Android App : Unable to navigate to Hot Water Home Page')
                
            except:
                self.report_fail('Android App : NoSuchElementException: in navigate_to_hot_water_homepage Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
         
    """ def navigate_to_screen(self, strPageName):
        if self.reporter.ActionStatus:
            try: 
                print(self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name'))
                if self.wait_for_element_exist(*self.MENU_BUTTON):
                    self.driver.find_element(*self.MENU_BUTTON).click()
                    time.sleep(2)
                    self.driver.find_element(*HomePageLocators.SETTINGS_MAIN_MENU).click()
                    self.report_pass("Android App :")
                    if strPageName == "account details":
                        time.sleep(2)
                        self.driver.find_element(*AccountDetailsLocators.ACCOUNT_SUB_MENU).click()
                    if strPageName == "holiday mode":
                        time.sleep(2)
                        self.driver.find_element(*HomePageLocators.HOLIDAY_SUB_MENU).click()
                        time.sleep(2)
                        self.driver.find_element(*HolidayModeLocators.START_DATE_TIME).click()
                        time.sleep(2)
                        print("\n *****************************"+ time.strftime("%d")+"\n ")
                        if self.driver.wait_for_element_exist(*HolidayModeLocators.START_DATE_TIME):
                            print("\n *****************************"+ time.strftime("%d")+"\n ")
                            self.driver.find_element(*HolidayModeLocators.START_DATE_TIME).click()
                            print("\n *****************************"+ time.strftime("%d")+"\n ")
                        else:
                            print("\n *****************************"+ time.strftime("%d")+"\n ")
                            self.driver.find_element_by_id(*HolidayModeLocators.TITLE).click()
                            time.sleep(2)
                        self.driver.find_element(*HolidayModeLocators.START_DATE_TIME).click()
                        print("\n *****************************"+ time.strftime("%d")+"\n ")
                        
            except:
                self.report_fail('Android App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))   
"""
    #Log out of the Hive Mobile App
    def logout_hive_app(self):
        #self.driver.reset()
        try: 
            if not 'LOGIN' in self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper():
                if self.wait_for_element_exist(*HomePageLocators.MENU_BUTTON_SHOW):
                    self.driver.find_element(*HomePageLocators.MENU_BUTTON_SHOW).click()
                if self.wait_for_element_exist(*HomePageLocators.SETTINGS_MAIN_MENU):
                    self.driver.find_element(*HomePageLocators.SETTINGS_MAIN_MENU).click()
                    self.wait_for_element_exist(*LogoutLocators.LOGOUT_OPTION)
                    self.driver.find_element(*LogoutLocators.LOGOUT_OPTION).click()
                    time.sleep(5)
                    if 'LOGIN' in self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper():
                        print('Android-App: The Hive Android App is successfully Logged out')
                        #self.report_pass('iOS-App: The Hive iOS App is successfully Logged out')
            else: 
                self.report_pass('Android-App: The Hive Android App is already Logged out')
                
        except:
            self.report_fail('Android-App: Exception in logout_hive_app Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
     
#Page Class for Heating Home page. Has all the methods for the Heating Home page
class HeatingHomePage(BasePage):
    #Navigates to the Heating Control Page
    def navigate_to_heating_control_page(self, boolStopBoost = True): 
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HeatingHomePageLocators.TITLE_LABEL):
                    self.driver.find_element(*HeatingHomePageLocators.HEAT_CONTROL_TAB).click()
                    if self.wait_for_element_exist(*HeatingControlPageLocators.PRESET_TEMP_BUTTON):                    
                        self.driver.find_element(*HeatingControlPageLocators.PRESET_TEMP_BUTTON).click()
                        self.driver.find_element(*HeatingControlPageLocators.PRESET_TEMP_BUTTON).click()
                        self.report_pass('Android-App : Successfully navigated to the Heating Control Page')
                    else:
                        if not boolStopBoost:                                
                            self.report_pass('Android-App: Successfully navigated to the Heating Control Page -')
                            return True
                        if self.wait_for_element_exist_for_given_time(*HeatingControlPageLocators.BOOST_STOP_BUTTON):
                            self.driver.find_element(*HeatingControlPageLocators.BOOST_STOP_BUTTON).click()
                            time.sleep(3)
                        if self.wait_for_element_exist(*HeatingControlPageLocators.PRESET_TEMP_BUTTON):  
                            self.report_pass('Android-App : Successfully navigated to the Heating Control Page')
                        else:
                            self.report_fail('Android App : Unable to navigate to Heating Control Page')
                else:
                    self.report_fail("Android-App : Control not active on the Heating Home Page to Navigate to Heating Control Page")
                
            except:
                self.report_fail('Android App : NoSuchElementException: in navigate_to_heating_control_page Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
    #Navigates to the Hot water Home Page
    def navigate_to_heating_schedule_page(self): 
        if self.reporter.ActionStatus:
            try: 
                if self.wait_for_element_exist(*HeatingHomePageLocators.TITLE_LABEL):                
                    time.sleep(5)
                    self.driver.find_element(*HeatingHomePageLocators.HEAT_SCHEDULE_TAB).click()
                    if self.wait_for_element_exist(*SchedulePageLocators.START_TIME_LABEL):
                        self.report_pass('Android-App : Successfully navigated to the Heating Schedule Page')
                    else:
                        self.report_fail('Android App : Unable to navigate to Heating Schedule Page')
                else:
                    self.report_fail("Android-App : Control not active on the Heating Home Page to Navigate to Heating Schedule Page")
                
            except:
                self.report_fail('Android App : NoSuchElementException: in navigate_to_heating_schedule_page Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
                
            
    
#Page Class for Hot Water Home page. Has all the methods for the Hot Water Home page
class HotWaterHomePage(BasePage):
    #Navigates to the Hot Water Control Page
    def navigate_to_hot_water_control_page(self, boolStopBoost = True): 
        if self.reporter.ActionStatus:
            try:
                 
                if self.wait_for_element_exist(*HotWaterHomePageLocators.TITLE_LABEL):
                    self.driver.find_element(*HotWaterHomePageLocators.HOT_WATER_CONTROL_TAB).click()
                    
                    if not boolStopBoost:                                
                        self.report_pass('Android-App: Successfully navigated to the Hot Water Control Page -')
                        return True
                    
                    if self.wait_for_element_exist(*HotWaterControlPageLocators.OFF_MODE_LINK):   
                        self.report_pass('Android-App : Successfully navigated to the Hot Water Control Page')
                    else:  
                        if not boolStopBoost:                                
                            self.report_pass('iOS-App: Successfully navigated to the Hot Water Control Page -')
                            return True
                        if self.wait_for_element_exist_for_given_time(*HotWaterControlPageLocators.BOOST_STOP_BUTTON):
                            self.driver.find_element(*HotWaterControlPageLocators.BOOST_STOP_BUTTON).click()
                            time.sleep(3)
                        if self.wait_for_element_exist(*HotWaterControlPageLocators.OFF_MODE_LINK):   
                            self.report_pass('Android-App : Successfully navigated to the Hot Water Control Page')
                        else:
                            self.report_fail('Android App : Unable to navigate to Hot Water Control Page')
                else:
                    self.report_fail("Android-App : Control not active on the Hot Water Home Page to Navigate to Hot Water Control Page")
                
            except:
                self.report_fail('Android App : NoSuchElementException: in navigate_to_hot_water_control_page Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
                
    
    #Navigates to the Hot water Home Page
    def navigate_to_hot_water_schedule_page(self): 
        if self.reporter.ActionStatus:
            try: 
                if self.wait_for_element_exist(*HotWaterHomePageLocators.TITLE_LABEL):                
                    time.sleep(5)
                    self.driver.find_element(*HotWaterHomePageLocators.HOT_WATER_SCHEDULE_TAB).click()
                    if self.wait_for_element_exist(*SchedulePageLocators.START_TIME_LABEL):
                        self.report_pass('Android-App : Successfully navigated to the Hot Water Schedule Page')
                    else:
                        self.report_fail('Android App : Unable to navigate to Hot Water Schedule Page')
                else:
                    self.report_fail("Android-App : Control not active on the Hot Water Home Page to Navigate to Hot Water Schedule Page")
                
            except:
                self.report_fail('Android App : NoSuchElementException: in navigate_to_hot_water_schedule_page Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
                
                       
#Page Class for Heating Control page. Has all the methods for the Heating Control page
class HeatingControlPage(BasePage):
    #Set Heat mode
    def set_heat_mode(self, strMode, intTemperature = None, intDuration = 1): 
        if self.reporter.ActionStatus:
            try: 
                if self.wait_for_element_exist(*HeatingControlPageLocators.PRESET_TEMP_BUTTON):             
                    self.driver.find_element(*self.REFRESH_BUTTON).click()
                    time.sleep(5)
                    self.wait_for_element_exist(*self.REFRESH_BUTTON)
                    if strMode.upper() == 'AUTO': self.driver.find_element(*HeatingControlPageLocators.SCHEDULE_MODE_LINK).click()
                    elif strMode.upper() == 'MANUAL': self.driver.find_element(*HeatingControlPageLocators.MANUAL_MODE_LINK).click()
                    elif strMode.upper() == 'OFF': self.driver.find_element(*self.OFF_MODE_LINK).click()
                    elif strMode.upper() == 'BOOST': 
                        self.driver.find_element(*self.CH_BOOST_MODE_LINK).click()
                        print('intTemperature', intTemperature)
                        print('intDuration', intDuration)
                        if (self.currentAppVersion == 'V6'): 
                            #Set Boost Duration
                            if (intDuration != 1):
                                intHour = int(self.driver.find_element(*HeatingControlPageLocators.BOOST_CURRENT_HOUR).text.split(':')[0])
                                intMinute = int(self.driver.find_element(*HeatingControlPageLocators.BOOST_CURRENT_MINUTE).text.split(':')[0])
                                intCurrentDuration = utils.round_up((intHour * 60 + intMinute)/60)
                                print('intCurrentDuration', intCurrentDuration)
                                print('intDuration', intDuration)
                                intCntrIter= 0 
                                while (intCurrentDuration != intDuration) and (intCntrIter <3) : 
                                    time.sleep(2)
                                    self.set_boost_time_duration(intDuration)
                                    intHour = int(self.driver.find_element(*HeatingControlPageLocators.BOOST_CURRENT_HOUR).text.split(':')[0])
                                    intMinute = int(self.driver.find_element(*HeatingControlPageLocators.BOOST_CURRENT_MINUTE).text.split(':')[0])
                                    intCurrentDuration = utils.round_up((intHour * 60 + intMinute)/60)
                                    intCntrIter += 1
                            #Set Boost Target temperature
                            if (intTemperature != None):
                                oScrolElement = self.driver.find_element(*HeatingControlPageLocators.BOOST_TEMP_SCROLL)
                                fltCurrentTargTemp = float(oScrolElement.get_attribute('name').split()[2])
                                intCntrIter = 1
                                while (fltCurrentTargTemp != intTemperature) and (intCntrIter < 3):
                                    self.scroll_element_to_value(oScrolElement, fltCurrentTargTemp, intTemperature, 0.5, 2)
                                    fltCurrentTargTemp = float(oScrolElement.get_attribute('name').split()[2])
                                    intCntrIter =+1
                           
                    
                    time.sleep(5)
                    self.driver.find_element(*self.REFRESH_BUTTON).click()
                    time.sleep(5)
                    if self.wait_for_element_exist(*self.REFRESH_BUTTON):
                        self.report_pass('Android-App : Successfully Heat mode is set to <B>' + strMode)
                    else:
                        self.report_fail('Android App : Unable to set Heat mode to <B>' + strMode)
                else:
                    self.report_fail("Android-App : Control not active on the Heating Control Page to set the Heat Mode")
                
            except:
                self.report_fail('Android App : NoSuchElementException: in set_heat_mode Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
                
    #Set Target Temperature    
    def set_target_temperature(self, fltTargetTemperature): 
        if self.reporter.ActionStatus:
            try: 
                if self.wait_for_element_exist(*HeatingControlPageLocators.PRESET_TEMP_BUTTON):                
                    self.driver.find_element(*self.REFRESH_BUTTON).click()
                    time.sleep(5)
                    self.wait_for_element_exist(*self.REFRESH_BUTTON)
                    self.driver.find_element(*HeatingControlPageLocators.PRESET_TEMP_BUTTON).click()
                    self.driver.find_element(*HeatingControlPageLocators.PRESET_TEMP_BUTTON).click()
                    oScrolElement = self.driver.find_element(*HeatingControlPageLocators.TARGET_TEMPERATURE_SCROLL)
                    fltCurrentTargTemp = float(oScrolElement.get_attribute('name').split()[2])
                    intCntrIter = 1
                    while (fltCurrentTargTemp != fltTargetTemperature) and (intCntrIter < 3):
                        self.scroll_element_to_value(oScrolElement, fltCurrentTargTemp, fltTargetTemperature, 0.5, 2)
                        fltCurrentTargTemp = float(oScrolElement.get_attribute('name').split()[2])
                        intCntrIter =+1
                    
                    time.sleep(5)
                    self.driver.find_element(*self.REFRESH_BUTTON).click()
                    time.sleep(5)
                    self.wait_for_element_exist(*self.REFRESH_BUTTON)
                    
                    if fltCurrentTargTemp == fltTargetTemperature:
                        self.report_pass('Android-App : The Target Temperature is successfully set to : ' + str(fltTargetTemperature))
                    else:   
                        self.report_fail('Android App : Unable to set the Target Temperature to : ' + str(fltTargetTemperature))
                else:
                    self.report_fail("Android-App : Control not active on the Heating Control Page to set the Target Temperature")
                
            except:
                self.report_fail('Android App : NoSuchElementException: in set_target_temperature Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
    
    #Get Attributes for Heating Controls                
    def get_heating_attribute(self):
        if self.reporter.ActionStatus:
            try: 
                fltCurrentTargTemp = 0.0
                strRunningState = 'OFF'
                strMode = ""
                if self.wait_for_element_exist(*HeatingHomePageLocators.TITLE_LABEL):
                    print("==================first===if========\n")
                    self.driver.find_element(*HeatingHomePageLocators.HEAT_CONTROL_TAB).click()
                    if self.wait_for_element_exist(*HeatingControlPageLocators.SELECTED_MODE_LINK):
                        print("=====================if========\n")
                        strMode = self.driver.find_element(*HeatingControlPageLocators.SELECTED_MODE_LINK).text.upper()
                        print(strMode, 'strMode')
                        if 'SCHEDULE' in strMode: 
                            strMode = 'AUTO'
                        if self.wait_for_element_exist(*HeatingControlPageLocators.FLAME_ICON): strRunningState = 'ON'
                    else: 
                        strMode = 'BOOST'
                        print("===========else==================\n")
                        if self.wait_for_element_exist(*HeatingControlPageLocators.BOOST_FLAME_ICON): strRunningState = 'ON'
                        
                    oScrolElement = self.driver.find_element(*HeatingControlPageLocators.TARGET_TEMPERATURE_SCROLL)
                    fltCurrentTargTemp = float(oScrolElement.get_attribute('name').split()[2])
                else:
                    print("=====ifelse========================\n")
                    self.report_fail("Android-App : Control not active on the Heating Control Page to set the Target Temperature")
                
                self.report_done('Android App : Screenshot while getting attributes')
                if strRunningState == 'OFF': strRunningState= '0000'
                else: strRunningState = '0001'
                if fltCurrentTargTemp == 7.0: fltCurrentTargTemp = 1.0
                return strMode, strRunningState, fltCurrentTargTemp
            except:
                print("=========exception====================\n")
                self.report_fail('Android App : NoSuchElementException: in get_heating_attribute Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
               

#Page Class for Heating Schedule page. Has all the methods for the Heating Schedule page
class HeatingSchedulePage(BasePage):
    #Set Heating Schedule
    def set_heating_schedule(self, oScheduleDict): 
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*SchedulePageLocators.START_TIME_LABEL) and self.wait_for_element_exist(*self.REFRESH_BUTTON):
                    for oKey in oScheduleDict.keys():
                        print('m here')
                        print(oKey)
                        self._navigate_to_day(oKey)
                        self.wait_for_element_exist(*self.REFRESH_BUTTON)
                        oScheduleList = oSchedUtils.remove_duplicates(oScheduleDict[oKey])
                        #Get List of Options & Start Time
                        lstStartTime = self.driver.find_elements(*SchedulePageLocators.START_TIME_LABEL) 
                        intCurrentEventCount = len(lstStartTime)
                        if self.reporter.platformVersion=='V6':
                            self.add_or_remove_events(len(oScheduleList))
                        else:
                            if len(oScheduleList) > 4:
                                if not intCurrentEventCount == 6:
                                    self.driver.find_element(*SchedulePageLocators.SCHEDULE_SPINNER_MENU).click()  
                                    self.driver.find_element(*SchedulePageLocators.SIX_EVENT_SUBMENU).click()  
                            else:
                                if not intCurrentEventCount == 4:
                                    self.driver.find_element(*SchedulePageLocators.SCHEDULE_SPINNER_MENU).click()  
                                    self.driver.find_element(*SchedulePageLocators.FOUR_EVENT_SUBMENU).click()  
                         
                        lstStartTime = self.driver.find_elements(*SchedulePageLocators.START_TIME_LABEL)              
                        for intCntr in range((len(lstStartTime) -1), -1, -1):
                            strSetStartTime = oScheduleList[intCntr][0]
                            fltSetTargTemp = oScheduleList[intCntr][1]
                            if fltSetTargTemp ==1.0: fltSetTargTemp = 7.0
                            intCntrIter= 0 
                            strCurrentStartTIme = ''
                            while (strCurrentStartTIme != strSetStartTime) and (intCntrIter <3) :
                                lstStartTime[intCntr].click()
                                self.report_done('Android-App : Event number : ' + str(intCntr + 1 ) + ' before the event change')
                                print(fltSetTargTemp)
                                self.set_schedule_target_temperature(fltSetTargTemp)
                                self.set_schedule_event_hour(strSetStartTime.split(':')[0])
                                self.set_schedule_event_minute(strSetStartTime.split(':')[1])
                                intCntrIter +=1                
                                self.report_done('Android-App : Event number : ' + str(intCntr + 1 ) + ' after the event change')
                                self.driver.find_element(*EditTimeSlotPageLocators.SAVE_BUTTON).click()  
                                self.wait_for_element_exist(*self.REFRESH_BUTTON)
                                strCurrentStartTIme = lstStartTime[intCntr].get_attribute('text')
                            self.report_pass('Android-App : Main Screen after Event number : ' + str(intCntr + 1 ) + ' is changed')
                        self.report_pass('Android-App : Main Screen after all Events are changed')
                else:
                    self.report_fail("Android-App : Control not active on the Heating Schedule Page to set the Heating Schedule")
                
            except:
                self.report_fail('Android App : NoSuchElementException: in set_heating_schedule Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
                
    #Set the Even Target temperature
    def set_schedule_target_temperature(self, fltSetTargTemp): 
        if self.reporter.ActionStatus:
            try: 
                if self.wait_for_element_exist(*EditTimeSlotPageLocators.HEATING_TITLE_LABEL):
                    oScrolElement = self.driver.find_element(*EditTimeSlotPageLocators.EVENT_TARGET_TEMPERATURE_SCROLL)
                    fltCurrentTargTemp = float(oScrolElement.get_attribute('name').split()[2])
                    intCntrIter = 1
                    while (fltCurrentTargTemp != fltSetTargTemp) and (intCntrIter < 3):
                        self.scroll_element_to_value(oScrolElement, fltCurrentTargTemp, fltSetTargTemp, 0.5, 2)
                        fltCurrentTargTemp = float(oScrolElement.get_attribute('name').split()[2])
                        intCntrIter =+1
                    if fltCurrentTargTemp == fltSetTargTemp:
                        self.report_pass('Android-App : The Target Temperature is successfully set to : ' + str(fltSetTargTemp))
                    else:   
                        self.report_fail('Android App : Unable to set the Target Temperature to : ' + str(fltSetTargTemp))
                else:
                    self.report_fail("Android-App : Control not active on the Edit Time Slot for Heating schedule Page to set the Event Target Temperature")
                
            except:
                self.report_fail('Android App : NoSuchElementException: in set_schedule_target_temperature Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
                
                
   
#Page Class for Hot Water Control page. Has all the methods for the Hot Water Control page
class HotWaterControlPage(BasePage):
    #Set Heat mode
    def set_hot_water_mode(self, strMode, intDuration = 1): 
        if self.reporter.ActionStatus:
            try: 
                if self.wait_for_element_exist(*self.RUNNING_STATE_CIRCLE):             
                    self.driver.find_element(*self.REFRESH_BUTTON).click()
                    time.sleep(5)
                    self.wait_for_element_exist(*self.REFRESH_BUTTON)
                    if strMode.upper() == 'AUTO': self.driver.find_element(*HotWaterControlPageLocators.SCHEDULE_MODE_LINK).click()
                    elif strMode.upper() == 'MANUAL': self.driver.find_element(*HotWaterControlPageLocators.MANUAL_MODE_LINK).click()
                    elif strMode.upper() == 'OFF': self.driver.find_element(*HotWaterControlPageLocators.OFF_MODE_LINK).click()
                    elif strMode.upper() == 'BOOST': 
                        self.driver.find_element(*self.HW_BOOST_MODE_LINK).click()
                        print('intDuration', intDuration)
                        if (self.currentAppVersion == 'V6'): 
                            #Set Boost Duration
                            if (intDuration != 1):
                                intHour = int(self.driver.find_element(*HotWaterControlPageLocators.BOOST_CURRENT_HOUR).text.split(':')[0])
                                intMinute = int(self.driver.find_element(*HotWaterControlPageLocators.BOOST_CURRENT_MINUTE).text.split(':')[0])
                                intCurrentDuration = utils.round_up((intHour * 60 + intMinute)/60)
                                print('intCurrentDuration', intCurrentDuration)
                                print('intDuration', intDuration)
                                intCntrIter= 0 
                                while (intCurrentDuration != intDuration) and (intCntrIter <3) : 
                                    time.sleep(2)
                                    self.set_boost_time_duration(intDuration)
                                    intHour = int(self.driver.find_element(*HotWaterControlPageLocators.BOOST_CURRENT_HOUR).text.split(':')[0])
                                    intMinute = int(self.driver.find_element(*HotWaterControlPageLocators.BOOST_CURRENT_MINUTE).text.split(':')[0])
                                    intCurrentDuration = utils.round_up((intHour * 60 + intMinute)/60)
                                    intCntrIter += 1
                            
                                               
                    time.sleep(5)
                    self.driver.find_element(*self.REFRESH_BUTTON).click()
                    time.sleep(5)
                    if self.wait_for_element_exist(*self.REFRESH_BUTTON):
                        self.report_pass('Android-App : Successfully Hot Water mode is set to <B>' + strMode)
                    else:
                        self.report_fail('Android App : Unable to set Hot Water mode to <B>' + strMode)
                else:
                    self.report_fail("Android-App : Control not active on the Hot Water Control Page to set the Hot Water Mode")
                
            except:
                self.report_fail('Android App : NoSuchElementException: in set_hot_water_mode Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
                
    #Get Attributes for HotWater Controls                
    def get_hotwater_attribute(self):
        if self.reporter.ActionStatus:
            fltCurrentTargTemp = 0.0
            strRunningState = 'OFF'
            strMode = ""
            try: 
                if self.wait_for_element_exist(*self.RUNNING_STATE_CIRCLE):
                    self.refresh_page()
                    if self.wait_for_element_exist(*HotWaterControlPageLocators.SELECTED_MODE_LINK):
                        strMode = self.driver.find_element(*HotWaterControlPageLocators.SELECTED_MODE_LINK).text.upper()
                        if 'SCHEDULE' in strMode: 
                            strMode = 'AUTO'
                        if self.driver.find_element(*self.RUNNING_STATE_CIRCLE).get_attribute('name').find('ON') >= 0:
                            strRunningState = 'ON'
                    else: 
                        strMode = 'BOOST'
                        if self.driver.find_element(*HotWaterControlPageLocators.BOOST_ACTIVE).get_attribute('name').upper().find('ACTIVE') >= 0:
                            strRunningState = 'ON'
                    
                else:
                    self.report_fail("Android-App : Control not active on the Hot Water Control Page to get Heating Attributes")
                    
                self.report_done('Android App : Screenshot while getting attributes')
                if strRunningState == 'OFF': strRunningState= '0000'
                else: strRunningState = '0001'
                return strMode, strRunningState, fltCurrentTargTemp
            except:
                self.report_fail('Android App : NoSuchElementException: in get_hotwater_attribute Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))           
                
#Page Class for Hot Water Schedule page. Has all the methods for the Hot Water Schedule page
class HotWaterSchedulePage(BasePage):
    #Set Hot Water Schedule
    def set_hot_water_schedule(self, oScheduleDict): 
        if self.reporter.ActionStatus:
            try: 
                if self.wait_for_element_exist(*SchedulePageLocators.START_TIME_LABEL) and self.wait_for_element_exist(*self.REFRESH_BUTTON):
                    for oKey in oScheduleDict.keys():
                        print('m here')
                        print(oKey)
                        self._navigate_to_day(oKey)
                        self.wait_for_element_exist(*self.REFRESH_BUTTON)
                        oScheduleList = oSchedUtils.remove_duplicates(oScheduleDict[oKey])
                        #Get List of Options & Start Time
                        lstStartTime = self.driver.find_elements(*SchedulePageLocators.START_TIME_LABEL)      
                        intCurrentEventCount = len(lstStartTime)
                        if self.reporter.platformVersion=='V6':
                            self.add_or_remove_events(len(oScheduleList))
                        else:
                            if len(oScheduleList) > 4:
                                if not intCurrentEventCount == 6:
                                    self.driver.find_element(*SchedulePageLocators.SCHEDULE_SPINNER_MENU).click()  
                                    self.driver.find_element(*SchedulePageLocators.SIX_EVENT_SUBMENU).click()  
                            else:
                                if not intCurrentEventCount == 4:
                                    self.driver.find_element(*SchedulePageLocators.SCHEDULE_SPINNER_MENU).click()  
                                    self.driver.find_element(*SchedulePageLocators.FOUR_EVENT_SUBMENU).click()  
                        
                        lstStartTime = self.driver.find_elements(*SchedulePageLocators.START_TIME_LABEL)   
                        for intCntr in range((len(lstStartTime) -1), -1, -1):
                            strSetStartTime = oScheduleList[intCntr][0]
                            fltSetTargTemp = oScheduleList[intCntr][1]
                            if fltSetTargTemp ==1.0: fltSetTargTemp = 7.0
                            intCntrIter= 0 
                            strCurrentStartTIme = ''
                            while (strCurrentStartTIme != strSetStartTime) and (intCntrIter <3) :
                                lstStartTime[intCntr].click()
                                self.report_done('Android-App : Event number : ' + str(intCntr + 1 ) + ' before the event change')
                                print(fltSetTargTemp)
                                if self.driver.find_element(*EditTimeSlotPageLocators.HOT_WATER_TOGGLE_BUTTON).get_attribute('name').find('ON') >= 0:
                                    strCurrentState = 'ON'
                                else: strCurrentState = 'OFF' 
                                    
                                if (fltSetTargTemp  == 99.0 and strCurrentState == 'OFF') or (fltSetTargTemp  == 0.0 and strCurrentState == 'ON'): 
                                    self.driver.find_element(*EditTimeSlotPageLocators.HOT_WATER_TOGGLE_BUTTON).click()  
                                    
                                self.set_schedule_event_hour(strSetStartTime.split(':')[0])
                                self.set_schedule_event_minute(strSetStartTime.split(':')[1])
                                intCntrIter +=1                
                                self.report_done('Android-App : Event number : ' + str(intCntr + 1 ) + ' after the event change')
                                self.driver.find_element(*EditTimeSlotPageLocators.SAVE_BUTTON).click()  
                                time.sleep(2)
                                self.wait_for_element_exist(*self.REFRESH_BUTTON)
                                strCurrentStartTIme = lstStartTime[intCntr].get_attribute('text')
                            self.report_pass('Android-App : Main Screen after Event number : ' + str(intCntr + 1 ) + ' is changed')
                        self.report_pass('Android-App : Main Screen after all Events are changed')
                else:
                    self.report_fail("Android-App : Control not active on the Hot Water Schedule Page to set the Hot Water Schedule")
                
            except:
                self.report_fail('Android App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
                
#Page Class for account details page. Has all the methods for the account details page               
class AccountDetails(BasePage):
                    
    def open_acc_details(self, strPageName):
        if self.reporter.ActionStatus:
            try: 
                print(self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name'))
                if self.wait_for_element_exist(*self.MENU_BUTTON):
                    self.driver.find_element(*self.MENU_BUTTON).click()
                    time.sleep(2)
                    self.driver.find_element(*AccountDetailsLocators.SETTINGS_MAIN_MENU).click()
                    self.report_pass("Android App :")
                    if strPageName == "account details":
                        time.sleep(2)
                        self.driver.find_element(*AccountDetailsLocators.ACCOUNT_SUB_MENU).click()
            except:
                self.report_fail('Android App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))   


    def validate_acc_details(self,context):
        print("hi")
     
class HolidayMode(BasePage):
      
    def navigateToHoildayScreen(self,context):
        #strHolidayStart = "+2"
        #strHolidayStartTime = "+120"
        #strDuration = "120"
        print(self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name'))
        if self.wait_for_element_exist(*HomePageLocators.MENU_BUTTON_V6):
            print('\n Start \n')
            self.driver.find_element(*HomePageLocators.MENU_BUTTON_V6).click()
            time.sleep(2)
            self.driver.find_element(*HomePageLocators.SETTINGS_MAIN_MENU).click()
            time.sleep(3)
            self.driver.find_element(*HomePageLocators.HOLIDAY_SUB_MENU).click()
            print('\n done \n')
            print('Going to activate holiday mode')
            time.sleep(360)
            print('I finshed waiting for holiday mode')
            
            
    def activateHolidaymode(self):
        if self.wait_for_element_exist(*HolidayModeLocators.ACTIVATE_HOLIDAY_BUTTON):
            self.driver.find_element(*HolidayModeLocators.ACTIVATE_HOLIDAY_BUTTON).click()
            time.sleep(2)
            
        
    
    def setHoildayMode(self,context,strHolidayStart,strHolidayStartTime,strDuration):
        print("^^^^^^^^^^^"+str(datetime.now()))
        if "+" in strHolidayStart:
            dtDate = datetime.now() + timedelta(days=int(strHolidayStart.split(sep="+", maxsplit=1)[1]))
            
            strSetMonth = dtDate.strftime("%B").upper()
            strSetDate = dtDate.day
            strSetYear = dtDate.year
            if "+" in strHolidayStartTime:
                dtDate = datetime.now() + timedelta(seconds=int(strHolidayStartTime.split(sep="+", maxsplit=1)[1]))
                strSetHour = dtDate.hour
                strSetMin = dtDate.minute
            else:
                if "-" in strHolidayStartTime:
                    dtDate = datetime.now() - timedelta(seconds=int(strHolidayStartTime.split(sep="-", maxsplit=1)[1]))
                    strSetHour = dtDate.hour
                    strSetMin = dtDate.minute
        else:
            if "-" in strHolidayStart:
                dtDate = datetime.now() - timedelta(days=int(strHolidayStart.split(sep="-", maxsplit=1)[1]))
                strSetMonth = dtDate.strftime("%B").upper()
                strSetDate = dtDate.day
                strSetYear = dtDate.year
            if "+" in strHolidayStartTime:
                dtDate = datetime.now() + timedelta(seconds=int(strHolidayStartTime.split(sep="+", maxsplit=1)[1]))
                strSetHour = dtDate.hour
                strSetMin = dtDate.minute
            else:
                if "-" in strHolidayStartTime:
                    dtDate = datetime.now() - timedelta(seconds=int(strHolidayStartTime.split(sep="-", maxsplit=1)[1]))
                    strSetHour = dtDate.hour
                    strSetMin = dtDate.minute
                    
        
        dtDate = dtDate + timedelta(seconds=int(strDuration))
        strSetEndDate = dtDate.day
        strSetEndMonth = dtDate.strftime("%B").upper()
        strSetEndYear = dtDate.year
        strSetEndHour = dtDate.hour
        strSetEndMin = dtDate.minute
        self.verifyHolidayModeSettingPage("First")
        self.setHolidayTargetTemperature(9)
        time.sleep(2)
        self.setHolidayStartDate(str(strSetYear), strSetMonth, str(strSetDate),str(strSetHour),str(strSetMin))
        strSetYear = 2015
        strSetMonth = "OCTOBER"
        strSetDate = "20"
        self.setHolidayEndTime(str(strSetEndYear),strSetEndMonth,str(strSetEndDate),str(strSetEndHour),str(strSetEndMin))
        time.sleep(2)
        self.driver.find_element(*HolidayModeLocators.ACTIVATE_HOLIDAY_BUTTON).click()
    
    #Set Target temperature
    def setHolidayTargetTemperature(self,fltSetTargTemp):
        time.sleep(2)
        oScrolElement = self.driver.find_element(*HolidayModeLocators.TARGET_TEMPERATURE)
        fltCurrentTargTemp = float(oScrolElement.get_attribute('name').split()[1])
        self.setScrollValue(self.driver, oScrolElement, fltCurrentTargTemp, fltSetTargTemp, 0.5, 2)

            
    #Set Scroll Value
    ''' def setScrollValue(self,wd, oScrolElement, fltCurrentValue, fltSetValue, fltPrecision, fltScrolPrecesion):
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
                wd.swipe(intStX, intEndY, intEndX, intStY, 1000)
                time.sleep(0.5)
            time.sleep(10)
'''
   
    month_dict = {"Jan":1,"Feb":2,"Mar":3,"Apr":4, "May":5, "Jun":6, "Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12} 

    def to_dict(self,name): 
        return self.month_dict[name] 
    
    def to_if(self,name): 
        if name == "JANUARY": return 1 
        elif name == "FEBRUARY": return 2 
        elif name == "MARCH": return 3 
        elif name == "APRIL": return 4 
        elif name == "MAY": return 5 
        elif name == "JUNE": return 6 
        elif name == "JULY": return 7 
        elif name == "AUGUST": return 8 
        elif name == "SEPTEMBER": return 9 
        elif name == "OCTOBER": return 10 
        elif name == "NOVEMBER": return 11 
        elif name == "DECEMBER": return 12 
        else: raise ValueError
    
    def selectHolidayStartTime(self,strStartHour,strStartMin):
        strSetStartTime = strStartHour + ":" + strStartMin
        intCntrIter= 0 
        strCurrentStartTIme = self.driver.find_element(*HolidayModeLocators.DEPARTURE_TIME).get_attribute("text")
        self.driver.find_element(*HolidayModeLocators.DEPARTURE_TIME).get_attribute("text")
        self.driver.find_element(*HolidayModeLocators.START_DATE_TIME).click()
        time.sleep(2)
        while (strCurrentStartTIme != strSetStartTime) and (intCntrIter <3) :
            #self.set_schedule_target_temperature(fltSetTargTemp)
            self.set_schedule_event_hour(strStartHour)
            print(strStartMin,'\n')
            input('')
            self.set_schedule_event_minute(int(strStartMin), 1)
            intCntrIter +=1       
            self.driver.find_element(*EditTimeSlotPageLocators.SAVE_BUTTON).click()  
            #self.wait_for_element_exist(*self.REFRESH_BUTTON)
            strCurrentStartTIme = self.driver.find_element(*HolidayModeLocators.DEPARTURE_TIME).get_attribute("text")
            self.driver.find_element(*HolidayModeLocators.START_DATE_TIME).click()
        self.driver.find_element(*EditTimeSlotPageLocators.SAVE_BUTTON).click()  
    
    def selectHolidayEndTime(self,strEndHour,strEndMin):
        strSetEndTime = strEndHour + ":" + strEndMin
        intCntrIter= 0 
        strCurrentEndTIme = self.driver.find_element(*HolidayModeLocators.ARRIVAL_TIME).get_attribute("text")
        self.driver.find_element(*HolidayModeLocators.DEPARTURE_TIME).get_attribute("text")
        self.driver.find_element(*HolidayModeLocators.END_DATE_TIME).click()
        time.sleep(2)
        while (strCurrentEndTIme != strSetEndTime) and (intCntrIter <3) :
            #self.set_schedule_target_temperature(fltSetTargTemp)
            self.set_schedule_event_hour(strEndHour)
            self.set_schedule_event_minute(strEndMin, 1)
            intCntrIter +=1       
            self.driver.find_element(*EditTimeSlotPageLocators.SAVE_BUTTON).click()  
            #self.wait_for_element_exist(*self.REFRESH_BUTTON)
            strCurrentEndTIme = self.driver.find_element(*HolidayModeLocators.ARRIVAL_TIME).get_attribute("text")
            self.driver.find_element(*HolidayModeLocators.END_DATE_TIME).click()
        self.driver.find_element(*EditTimeSlotPageLocators.SAVE_BUTTON).click()  
       
    #Set the Even Target temperature
    
    def set_schedule_event_minute(self, intSetMinute, intPrecession = 15): 
        try: 
            if self.wait_for_element_exist(*EditTimeSlotPageLocators.MINUTE_SCROLL):
                oScrolElement = self.driver.find_element(*EditTimeSlotPageLocators.MINUTE_SCROLL)
                intSetMinute = int(intSetMinute)
                intCurrentMinute = int(oScrolElement.find_element(*EditTimeSlotPageLocators.NUMBER_INSDE_SCROLL_ITEM).get_attribute('name'))  
                self.scroll_element_to_value(oScrolElement, intCurrentMinute, intSetMinute, intPrecession, 1.4)
                
            else:
                print("Android-App : Control not active on the Edit Time Slot for Heating schedule Page to set the Event start time Minute")
            
        except:
            print('Android App : NoSuchElementException: in set_schedule_event_minute Method\n {0}'+format(traceback.format_exc().replace('File', '$~File')))
            
    '''def setHolidayYearAndMonth(self,strSetDate,strMonthName,strYearName,strSetYear,strSetMonth):
        if (int(strYearName) - int(strSetYear)) < 0:
            if (self.to_if(strSetMonth)-self.to_if(strMonthName)) > 0:
                if int(strSetYear) != int(strYearName):
                    if (12-self.to_if(strMonthName) + self.to_if(strSetMonth)) < 12 :
                        for i in range(1,(12-self.to_if(strMonthName) + self.to_if(strSetMonth))):
                            self.driver.find_element(*HolidayModeLocators.DEPARTURE_ADD_MONTH).click()
                    else:
                        if (12-self.to_if(strMonthName) + self.to_if(strSetMonth)) > 12 :
                            for i in range(0,(12+(self.to_if(strSetMonth) - self.to_if(strMonthName)))):
                                self.driver.find_element(*HolidayModeLocators.DEPARTURE_ADD_MONTH).click()
                        else:
                            for i in range(0,12):
                                self.driver.find_element(*HolidayModeLocators.DEPARTURE_ADD_MONTH).click()
                strMonthYearName = self.driver.find_element(*HolidayModeLocators.DEPARTURE_MONTH_YEAR).get_attribute("text")
                strMonthName = strMonthYearName.split(sep=" ", maxsplit=1)[0]
                if self.to_if(strSetMonth) != self.to_if(strMonthName):
                    print("\n ***********Fail")
                else:
                    print("\n ***********Pass")
                    time.sleep(2)
                    self.clickHolidayDate(strSetDate)
        else:
            if (int(strYearName) - int(strSetYear)) == 0:
                if int(self.to_if(strSetMonth)) - int(self.to_if(strMonthName)) > 0:
                    for i in range(0,(self.to_if(strSetMonth) - self.to_if(strMonthName))):
                        self.driver.find_element(*HolidayModeLocators.DEPARTURE_ADD_MONTH).click()
                else:
                    if int(self.to_if(strSetMonth)) - int(self.to_if(strMonthName)) < 0:
                        for i in range(0,(self.to_if(strMonthName) - self.to_if(strSetMonth))):
                            self.driver.find_element(*HolidayModeLocators.DEPARTURE_DEL_MONTH).click()
            else:
                if(int(strYearName) - int(strSetYear)) < 0:
                    for i in range(0,(12-self.to_if(strSetMonth) + self.to_if(strMonthName))-12+(((int(strYearName) - int(strSetYear)) * 12)-12)):
                        self.driver.find_element(*HolidayModeLocators.DEPARTURE_DEL_MONTH).click()
                else:
                    for i in range(0,12):
                        self.driver.find_element(*HolidayModeLocators.DEPARTURE_DEL_MONTH).click()
            strMonthYearName = self.driver.find_element(*HolidayModeLocators.DEPARTURE_MONTH_YEAR).get_attribute("text")
            strMonthName = strMonthYearName.split(sep=" ", maxsplit=1)[0]
            if self.to_if(strSetMonth) != self.to_if(strMonthName):
                print("\n ***********Fail")
            else:
                print("\n ***********Pass")
                time.sleep(2)
                self.clickHolidayDate(strSetDate)'''
                
    def setHolidayStartDate(self,strSetYear,strSetMonth,strSetDate,strSetHour,strSetMin):
        #self.driver.find_element(*HolidayModeLocators.START_DATE_TIME).click()
        time.sleep(2)
        self.selectHolidayStartTime(strSetHour,strSetMin)
        time.sleep(2)
        self.driver.find_element(*HolidayModeLocators.START_DATE_TIME).click()
        time.sleep(2)
        strMonthYearName = self.driver.find_element(*HolidayModeLocators.DEPARTURE_MONTH_YEAR).get_attribute("text")
        strMonthName = strMonthYearName.split(sep=" ", maxsplit=1)[0]
        strYearName = strMonthYearName.split(sep=" ",maxsplit=1)[1]
        print("@@@@@@@@@@@@@@@@@@@@"+ str(int(strSetDate)))
        if (self.to_if(strSetMonth) != self.to_if(strMonthName)) | (int(strSetYear) != int(strYearName)):
            self.setHolidayYearAndMonth(strSetDate, strMonthName, strYearName,strSetYear,strSetMonth)
        else:
            if self.to_if(strSetMonth) != self.to_if(strMonthName):
                print("\n ***********Fail")
            else:
                print("\n ***********Pass")
                time.sleep(2)
                print("HolidayModeLocators.DEPARTURE_DATE")
                self.driver.find_element(*HolidayModeLocators.DEPARTURE_SAVE).click()
                time.sleep(2)
                self.driver.find_element(*HolidayModeLocators.START_DATE_TIME).click()
                time.sleep(2)
                self.driver.find_element(*HolidayModeLocators.DEPARTURE_SAVE).click()
                time.sleep(2)
                print("\n ***********Pass")
                self.clickHolidayDate(strSetDate)                    
        self.driver.find_element(*HolidayModeLocators.DEPARTURE_SAVE).click()
        time.sleep(2)
        
    def clickHolidayDate(self,strSetDate):
        oDayElLoc = self.set_TO_property(HolidayModeLocators.DEPARTURE_DATE,"CHANGE", str(int(strSetDate)))
        self.driver.find_element(*oDayElLoc).click()
        time.sleep(2)
    
    def clickHolidayDates(self,strSetDate):
        oDayElLoc = self.set_TO_property(HolidayModeLocators.DEPARTURE_DATES,"CHANGE", str(int(strSetDate)))
        self.driver.find_element(*oDayElLoc).click()
        time.sleep(2)
        
    def setHolidayEndTime(self,strSetYear,strSetMonth,strSetDate,strSetHour,strSetMin):
        #self.driver.find_element(*HolidayModeLocators.END_DATE_TIME).click()
        self.selectHolidayEndTime(strSetHour,strSetMin)
        time.sleep(2)
        self.driver.find_element(*HolidayModeLocators.END_DATE_TIME).click()
        time.sleep(2)
        print("@@@@@@@@@@@@@@@@@@@@"+ str(int(strSetDate)))
        strMonthYearName = self.driver.find_element(*HolidayModeLocators.DEPARTURE_MONTH_YEAR).get_attribute("text")
        strMonthName = strMonthYearName.split(sep=" ", maxsplit=1)[0]
        strYearName = strMonthYearName.split(sep=" ",maxsplit=1)[1]
        if (self.to_if(strSetMonth) != self.to_if(strMonthName)) | (int(strSetYear) != int(strYearName)):
            self.setHolidayYearAndMonth(strSetDate, strMonthName, strYearName,strSetYear,strSetMonth)
        else:
            if self.to_if(strSetMonth) != self.to_if(strMonthName):
                print("\n ***********Fail")
            else:
                print("\n ***********Pass")
                time.sleep(2)
                self.clickHolidayDate(strSetDate)
            self.driver.find_element(*HolidayModeLocators.DEPARTURE_SAVE).click()
            time.sleep(2)
            #self.driver.find_element(*HolidayModeLocators.ACTIVATE_HOLIDAY_BUTTON).click()
            time.sleep(2)
           
    def verifyHolidayModeSettingPage(self,strVisitingTime):
        if str(strVisitingTime).upper() == "FIRST":
            strMonthYearName = self.driver.find_element(*HolidayModeLocators.DEPARTURE_DATE).get_attribute("text")
            strDateName = strMonthYearName.split(sep=" ", maxsplit=2)[0]
            strMonthName = strMonthYearName.split(sep=" ", maxsplit=2)[1]
            strYearName = strMonthYearName.split(sep=" ",maxsplit=2)[2]
            print('----'+ strDateName + '====' + strMonthName + '"""""""' + strYearName)
            if int(strDateName) == int(datetime.now().day):
                print("Pass")
            else:
                print("Fail")
            
            if self.to_if(strMonthName.upper()) == int(datetime.now().month):
                print("Pass")
            else:
                print("Fail")
            if int(strYearName) == int(datetime.now().year):
                print("Pass")
            else:
                print("Fail")
            strMonthYearName = self.driver.find_element(*HolidayModeLocators.ARRIVAL_DATE).get_attribute("text")
            strDateName = strMonthYearName.split(sep=" ", maxsplit=2)[0]
            strMonthName = strMonthYearName.split(sep=" ", maxsplit=2)[1]
            strYearName = strMonthYearName.split(sep=" ",maxsplit=2)[2]
            print('----'+ strDateName + '====' + strMonthName + '"""""""' + strYearName)
            dtDate = datetime.now() + timedelta(days=7)
            if int(strDateName) == int(dtDate.day):
                print("Pass")
            else:
                print("Fail")
            
            if self.to_if(strMonthName.upper()) == int(dtDate.month):
                print("Pass")
            else:
                print("Fail")
            if int(strYearName) == int(dtDate.year):
                print("Pass")
            else:
                print("Fail")
              
           
class SetChangePassword(BasePage):
                    
    def change_password_screen(self):
        if self.reporter.ActionStatus:
            try: 
                strPassword = utils.getAttribute('common', 'password')
                if self.wait_for_element_exist(*ChangePasswordLocators.OLD_PASSWORD_EDITTEXT):
                    self.driver.find_element(*ChangePasswordLocators.OLD_PASSWORD_EDITTEXT).send_keys(strPassword)
                    self.report_pass('Android APP: Change Password Screen: Old password is entered successfully')
                    time.sleep(2)
                else:
                    self.report_fail('Android APP: Change Password Screen: Old password is entered successfully')
                    
                if self.wait_for_element_exist(*ChangePasswordLocators.NEW_PASSWORD_EDITTEXT):
                    self.driver.find_element(*ChangePasswordLocators.NEW_PASSWORD_EDITTEXT).send_keys('Password1' +"a")
                    self.report_pass('Android APP: Change Password Screen: New password is entered successfully')
                    time.sleep(2)
                else:
                    self.report_fail('Android APP: Change Password Screen: New password is entered successfully')
                 
                if self.wait_for_element_exist(*ChangePasswordLocators.CONF_PASSWORD_EDITTEXT):
                    self.driver.find_element(*ChangePasswordLocators.CONF_PASSWORD_EDITTEXT).send_keys('Password1' +"a")
                    self.report_pass('Android APP: Change Password Screen: Retype password is entered successfully')
                    time.sleep(2)
                else:
                    self.report_fail('Android APP: Change Password Screen: Retype password is entered successfully')
                    
                if self.wait_for_element_exist(*ChangePasswordLocators.SAVE_PASSWORD):
                    self.driver.find_element(*ChangePasswordLocators.SAVE_PASSWORD).click()
                    self.report_pass('Android APP: Change Password Screen:  Password is set successfully')
                    time.sleep(2)
                else:
                    self.report_fail('Android APP: Change Password Screen: Password is not set ,Save button is not clicked')    
                    
                           
            except:
                self.report_fail('Android App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))   
        
    #Navigate To ChangePassword Screen
    def navigate_to_change_password(self):    
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HomePageLocators.MENU_BUTTON_V6):
                    self.driver.find_element(*HomePageLocators.MENU_BUTTON_V6).click()
                    self.report_pass('Android APP: Change Password : Navigated to Menu Successfully')
                    time.sleep(2)
                else:
                    self.report_fail('Android APP: Change Password : Menu is not selected Successfully')    
                
                
                
                if self.wait_for_element_exist(*HomePageLocators.SETTINGS_MAIN_MENU):
                    self.driver.find_element(*HomePageLocators.SETTINGS_MAIN_MENU).click()
                    self.report_pass('Android APP: Navigated to Settings Successfully')
                    time.sleep(2)
                else:
                    self.report_fail('Android APP: Change Password : Settings is selected Successfully') 
                    
                print('settings clicked')
                self.driver.swipe(200,800,220,500, 1000)
                time.sleep(2)
                if self.wait_for_element_exist(*HomePageLocators.CHANGE_PASSWORD_SUBMENU):
                    self.driver.find_element(*HomePageLocators.CHANGE_PASSWORD_SUBMENU).click()
                    self.report_pass('Android APP: Navigated to Change Password screen Successfully')
                    time.sleep(2)
                else:
                    self.report_fail('Android APP: Change Password : is not selected Successfully') 
                
            
            except:
                self.report_fail('Android App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))   
            
     
     
    
     
    def login_change_password(self):
        if self.reporter.ActionStatus:
            try:
                strUserName = utils.getAttribute('common', 'userName')
                strPassword = utils.getAttribute('common', 'password')
                
                if self.wait_for_element_exist(*LoginPageLocators.LOGIN_BUTTON):
                    print("am in")
                    self.driver.find_element(*LoginPageLocators.USERNAME_EDTBOX).send_keys(strUserName)
                    self.driver.hide_keyboard()
                    self.driver.find_element(*LoginPageLocators.PASSWORD_EDTBOX).send_keys('Password1' +"a")
                    self.driver.hide_keyboard()
                    self.driver.find_element(*LoginPageLocators.LOGIN_BUTTON).click()
                if self.driver.find_element(*HomePageLocators.MENU_BUTTON_V6): 
                    self.report_pass('Android-App: The Hive Android App is successfully Logged in with the Changed Password')
                else:
                    self.report_fail('Android-App: The Hive Android App is not logged in. Please check the Login credentials and re-execute test.')
                            
            #else:
                #self.report_fail('The Hive App is either not Launched or the Login screen is not displayed. Please check and re-execute test.')          

                self.driver.find_element(*HomePageLocators.MENU_BUTTON_V6).click()  
                if self.wait_for_element_exist(*HomePageLocators.SETTINGS_MAIN_MENU):
                    self.driver.find_element(*HomePageLocators.SETTINGS_MAIN_MENU).click()  
                    self.driver.swipe(200,800,220,500, 1000)           
                    time.sleep(2)
                self.driver.find_element(*HomePageLocators.CHANGE_PASSWORD_SUBMENU).click()
                              
                
                self.driver.find_element(*ChangePasswordLocators.OLD_PASSWORD_EDITTEXT).send_keys('Password1' +"a")
                self.driver.find_element(*ChangePasswordLocators.NEW_PASSWORD_EDITTEXT).send_keys(strPassword)
                self.driver.find_element(*ChangePasswordLocators.CONF_PASSWORD_EDITTEXT).send_keys(strPassword)
                self.driver.find_element(*ChangePasswordLocators.SAVE_PASSWORD).click()        
                #self.driver.find_element(*HomePageLocators.MENU_BUTTON_SHOW).click()
                
            except:
                self.report_fail('Android-App: Exception in login_hive_app Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
        
            
            
            
     


class TextControl(BasePage):  
           
    def textControlOptions(self,context):
        if self.reporter.ActionStatus:             
                    for oRow in context.table:
                        strusername = oRow['UserName']
                        strMobileNo = oRow['MobileNo']
                        print(strusername,strMobileNo)
                        try:
                            if self.driver.find_element(*TextControlLocators.ADD_NEW_USER_LINK).is_displayed():
                                self.driver.find_element(*TextControlLocators.ADD_NEW_USER_LINK).click()
                                self.driver.find_element(*TextControlLocators.NAME_EDTBOX).send_keys(strusername)
                                self.driver.find_element(*TextControlLocators.MOBILE_EDTBOX).send_keys(strMobileNo)
                                self.driver.find_element(*TextControlLocators.SAVE_BUTTON).click()
                                time.sleep(5)                                                       
                                try:
                                    if self.driver.find_element(*TextControlLocators.ADD_NEW_USER_LINK).is_displayed():
                                        self.report.done("Android App:Maximum user limit reached in TextControl Page")
                                                                       
                                    else:
                                        self.driver.find_element(*TextControlLocators.SAVE_BUTTON).is_displayed()
                                        self.report_fail("Android App:This number is already registered to a Hive Account")                                           
                                except:
                                    self.report_pass("Android App:User added to Text Control successfully")     
                                
                      
                        except:
                            self.report_fail("Android App:Maximum user limit reached in TextControl Options")
                
     
    def textControlValidation(self,context):   
        if self.reporter.ActionStatus:
            try:
                '''strUserCount=self.driver.find_element(*TextControlLocators.USER_TABLE).text
                intRowCount=int(strUserCount[(len(strUserCount)-1)])'''
                try:
                    
                        self.report_done("Android App:More users can be added in TextControl Page")
                except:
                    
                     
                    self.report_pass("Android App:Text Control Options reached Maximum user limits")
                else:
                    self.report_done("Android App:More users can be added in TextControl Page")
            except:
                    self.report_fail('Android App : NoSuchElementException: in textControlValidation\n {0}'.format(traceback.format_exc().replace('File', '$~File')))            
            
            
            
            
            
            
    def navigate_to_TextControl_page(self):
         
        if self.reporter.ActionStatus:
            try: 
                rowcount=1
                if(rowcount<=6):
                    if self.wait_for_element_exist(*HomePageLocators.MENU_BUTTON_V6):
                        self.driver.find_element(*HomePageLocators.MENU_BUTTON_V6).click()
                        print('finished clicking home')
                        time.sleep(2)
                        self.driver.find_element(*HomePageLocators.HELP_SUPPORT_SUBMENU).click()
                        print('clicked help menu')
                    if self.wait_for_element_exist(*TextControlLocators.TEXTCONTROL_SUBMENU):                             
                            self.driver.find_element(*TextControlLocators.TEXTCONTROL_SUBMENU).click()
                            rowcount=rowcount+1
                            time.sleep(2)
                            self.report_pass('Android-App : Successfully navigated to the Change Password Page')    
                        
                    else:
                            self.report_fail("Android-App : Control not active on the Change Password Page")
                else:
                    self.report_fail("Android-App : Control not active on the Menu Button")               
            except:
                self.report_fail('Android App : NoSuchElementException: in navigate_to_change_password_screen\n {0}'.format(traceback.format_exc().replace('File', '$~File')))   
                                    
            
            
class SaveHeatingNotification(BasePage):
    
    def naivgate_to_ZoneNotificaiton(self):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HomePageLocators.MENU_BUTTON_V6):
                    self.driver.find_element(*HomePageLocators.MENU_BUTTON_V6).click()
                    self.report_pass('Android APP :  Hive user is able access Menu successfully')
                    time.sleep(2)
                else:
                    self.report_fail('Android APP: What went wrong -> Opps! Hive user is not able to access Menu')    
                
                if self.wait_for_element_exist(*HeatingNotificationsLocators.HEATING_NOTIFICATION):  
                        self.driver.find_element(*HeatingNotificationsLocators.HEATING_NOTIFICATION).click()
                        self.report_pass('Android APP: Hive user is able to access sub menu item Heating notification successfully')
                elif self.wait_for_element_exist(*HomePageLocators.SETTINGS_MAIN_MENU):
                        self.driver.find_element(*HomePageLocators.SETTINGS_MAIN_MENU).click()
                        self.driver.find_element(*HeatingNotificationsLocators.HEATING_NOTIFICATION).click()
                        self.report_pass('Android APP: Hive user is able to access sub menu item Heating notification successfully')
                else:
                        self.report_pass('Android APP: Hive user is not able to navigate to Heating notification ')
                
            except:
                self.report_fail('Android App : NoSuchElementException: in Heating Notification Screen\n {0}'.format(traceback.format_exc().replace('File', '$~File')))        
      
      
    def setHighTemperature(self,oTargetHighTemp):
            if self.reporter.ActionStatus:
                try:                 
                    if self.wait_for_element_exist(*HeatingNotificationsLocators.HEATING_MAX_OFF): 
                        self.report_pass('Android APP: Hive user is able to navigate to Maximum temperature screen successfully')
                        time.sleep(2)
                        if self.driver.find_element(*HeatingNotificationsLocators.HEATING_MAX_OFF):
                            self.driver.find_element(*HeatingNotificationsLocators.HEATING_MAX_OFF).click()
                            time.sleep(3)
                            self.set_target_Heating_notification_temperature_high(oTargetHighTemp)
                            time.sleep(3)
                            self.driver.find_element(*HeatingNotificationsLocators.SAVE_HEATING_NOTIFICATION).click()
                            self.driver.find_element(*HeatingNotificationsLocators.SAVE_MINMAX_NOTIFICATION).click()
                        else:                          
                            self.driver.find_element(*HeatingNotificationsLocators.CANCEL_HEATING_NOTIFICATION) 
                    else:
                        self.report_pass('Android APP: Hive user had already set the Maximum Temperature')
                        
                except:
                        self.report_fail('Android APP: Exception in set_heating_schedule Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
 

    def setLowTemperature(self,oTargetLowTemp):
            if self.reporter.ActionStatus:
                try:          
                    if self.wait_for_element_exist(*HeatingNotificationsLocators.HEATING_MIN_OFF):
                        self.report_pass('Android APP: Hive user is able to navigate to Minimum temperature screen successfully')
                        time.sleep(2)
                        if self.driver.find_element(*HeatingNotificationsLocators.HEATING_MIN_OFF):
                            self.driver.find_element(*HeatingNotificationsLocators.HEATING_MIN_OFF).click()
                            time.sleep(3)
                            self.set_target_Heating_notification_temperature_low(oTargetLowTemp)
                            self.driver.find_element(*HeatingNotificationsLocators.SAVE_HEATING_NOTIFICATION).click()
                            self.driver.find_element(*HeatingNotificationsLocators.SAVE_MINMAX_NOTIFICATION).click()
                            
                        else:                          
                            self.driver.find_element(*HeatingNotificationsLocators.CANCEL_HEATING_NOTIFICATION)
                    else:
                        self.report_pass('Android APP: Hive user had already set the Minimum Temperature')
                        
                except:
                    self.report_fail('Android APP: Exception in set_heating_schedule Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
                    
                    
                    
                    
                    
    def receiveWarnings(self):
        if self.reporter.ActionStatus:
                try:
                    if self.wait_for_element_exist(*HeatingNotificationsLocators.WARNING_OFF):
                            time.sleep(2)
                            self.driver.find_element(*HeatingNotificationsLocators.WARNING_OFF).click()
                            self.driver.find_element(*HeatingNotificationsLocators.SAVE_MINMAX_NOTIFICATION).click()
                            self.report_pass('Android APP: Hive user enabled the Receive Warnings')
                    else:
                            self.report_pass('Android APP: Hive user had already enabled Receive Warnings')
                
                except:
                    self.report_fail('Android APP: Exception in set_heating_schedule Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
    

    
    def set_target_Heating_notification_temperature_high(self, fltSetTargTemp):
        if self.reporter.ActionStatus:
            try: 
                    oScrolElement = self.driver.find_element(*HeatingNotificationsLocators.TARGET_TEMPERATURE_SCROLL_MAX)
                    print("Element found")
                    oScrolElementVAlue = oScrolElement.get_attribute('name')
                   
                    if 'degrees' in oScrolElementVAlue:
                        fltCurrentTargTemp=float(oScrolElementVAlue.split(' ')[3])
                        print(fltCurrentTargTemp)
                    intCntrIter = 1
                    while (fltCurrentTargTemp != fltSetTargTemp) and (intCntrIter < 3):                      
                        oScrolElement = self.driver.find_element(*HeatingNotificationsLocators.NOTIFY_TARGET_TEMPERATURE_SCROLL)
                        oScrolElementVAlue = oScrolElement.get_attribute('name')
                        fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[3])
                        #self.scroll_element_to_value(oScrolElement, fltCurrentTargTemp, fltSetTargTemp, 0.5, 2)
                        self.scroll_element_to_value(oScrolElement, fltCurrentTargTemp, fltSetTargTemp, 0.5, 2)
                        intCntrIter =+1
                        print(fltCurrentTargTemp, fltSetTargTemp)
                        
                    if fltCurrentTargTemp == fltSetTargTemp:
                        self.report_pass('Android APP: The Target Temperature is successfully set to : ' + str(fltSetTargTemp))
                    else:   
                        self.report_fail('Android APP: Unable to set the Target Temperature to : ' + str(fltSetTargTemp))  
            except:
                self.report_fail('Android APP: Exception in set_schedule_target_temperature Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
                  
    def set_target_Heating_notification_temperature_low(self, fltSetTargTemp):
        if self.reporter.ActionStatus:
            try: 
                    oScrolElement = self.driver.find_element(*HeatingNotificationsLocators.TARGET_TEMPERATURE_SCROLL_MIN)
                    print("Element found")
                    oScrolElementVAlue = oScrolElement.get_attribute('name')
                   
                    if 'degrees' in oScrolElementVAlue:
                        fltCurrentTargTemp=float(oScrolElementVAlue.split(' ')[3])
                        print(fltCurrentTargTemp)
                    intCntrIter = 1
                    while (fltCurrentTargTemp != fltSetTargTemp) and (intCntrIter < 3):                      
                        oScrolElement = self.driver.find_element(*HeatingNotificationsLocators.TARGET_TEMPERATURE_SCROLL_MIN)
                        oScrolElementVAlue = oScrolElement.get_attribute('name')
                        fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[3])
                        #self.scroll_element_to_value(oScrolElement, fltCurrentTargTemp, fltSetTargTemp, 0.5, 2)
                        self.scroll_element_to_value(oScrolElement, fltCurrentTargTemp, fltSetTargTemp, 0.5, 2)
                        intCntrIter =+1
                        print(fltCurrentTargTemp, fltSetTargTemp)
                        
                    if fltCurrentTargTemp == fltSetTargTemp:
                        self.report_pass('Android APP: The Target Temperature is successfully set to : ' + str(fltSetTargTemp))
                    else:   
                        self.report_fail('Android APP: Unable to set the Target Temperature to : ' + str(fltSetTargTemp))  
            except:
                self.report_fail('Android APP: Exception in set_schedule_target_temperature Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
                  

    def setNotificationONtoOFF(self,strNotiState):
            if self.reporter.ActionStatus:
                try:                 
                    if self.wait_for_element_exist(*HeatingNotificationsLocators.HEATING_MAX_ON): 
                        
                        self.report_pass('Android APP: Hive user is able to navigate to Maximum temperature screen successfully')
                        time.sleep(2)
                        if strNotiState == 'OFF' :
                                self.driver.find_element(*HeatingNotificationsLocators.HEATING_MAX_ON).click()
                                time.sleep(2)
                                #self.driver.find_element(*HeatingNotificationsLocators.SAVE_HEATING_NOTIFICATION).click()
                                self.report_pass('Android APP: Hive user turn off the Maximum Temperature')
                        else:                          
                                self.driver.find_element(*HeatingNotificationsLocators.CANCEL_HEATING_NOTIFICATION)
                    if self.wait_for_element_exist(*HeatingNotificationsLocators.HEATING_MIN_ON):
                        
                        self.report_pass('Android APP: Hive user is able to navigate to Maximum temperature screen successfully')
                        time.sleep(2)
                        if strNotiState == 'OFF' :
                                self.driver.find_element(*HeatingNotificationsLocators.HEATING_MIN_ON).click()
                                time.sleep(2)
                               
                                self.report_pass('Android APP: Hive user turn off the Minimum Temperature')
                                time.sleep(5)   
                                self.driver.find_element(*HeatingNotificationsLocators.WARNING_ON).click()
                                time.sleep(2)   
                                self.driver.find_element(*HeatingNotificationsLocators.SAVE_MINMAX_NOTIFICATION).click()
                                self.report_pass('Android APP: Hive user turn off the Heating Notification')  
                    else:
                        self.report_pass('Android APP: Hive user had already set the Maximum Temperature')
                        
                except:
                        self.report_fail('Android APP: Exception in heating schedule on to off Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
                        
                        
    
class SetPinLock(BasePage):

    def navigate_to_pin_lock(self):    
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HomePageLocators.MENU_BUTTON_V6):
                    self.driver.find_element(*HomePageLocators.MENU_BUTTON_V6).click()
                    self.report_pass('Android APP :  Hive user is able access Menu successfully')
                    time.sleep(2)
                else:
                    self.report_fail('Android APP: What went wrong -> Opps! Hive user is not able to access Menu')    
                
                if self.wait_for_element_exist(*PinLock.PINLOCK_SUB_MENU):  
                        self.driver.find_element(*PinLock.PINLOCK_SUB_MENU).click()
                        self.report_pass('Android APP: Hive user is able to access sub menu item Pinlock successfully')
                elif self.wait_for_element_exist(*HomePageLocators.SETTINGS_MAIN_MENU):
                        self.driver.find_element(*HomePageLocators.SETTINGS_MAIN_MENU).click()
                        self.driver.find_element(*PinLock.PINLOCK_SUB_MENU).click()
                        self.report_pass('Android APP: Hive user is able to access sub menu item Pinlock successfully')
                else:
                        self.report_pass('Android APP: Hive user is not able to navigate to Pinlock ')
                
            except:
                self.report_fail('Android App : NoSuchElementException: in Pinlock Screen\n {0}'.format(traceback.format_exc().replace('File', '$~File')))        
      
      

    def set_pinlock(self):  
        
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*PinLock.PINLOCK_STATUS_OFF):
                    self.report_pass('Android APP: Navigated to Set Pin Lock screen Successfully')  
                    time.sleep(2) 
                    self.driver.find_element(*PinLock.PINLOCK_STATUS_OFF).click()           
                    
                elif self.wait_for_element_exist(*PinLock.PINLOCK_STATUS_ON):
                        time.sleep(2)
                        self.report_pass('Android APP: Hive user has set pin lock already')     
                else:
                    self.report_fail('Android APP: Pin Lock Screen is not selected Successfully')    
                
                if self.wait_for_element_exist(*PinLock.ENTER_NEW_PIN):
                    self.driver.find_element(*PinLock.ENTER_NEW_PIN).send_keys("1234")
                    time.sleep(2)
                    self.driver.find_element(*PinLock.REENTER_NEW_PIN).send_keys("1234")
                    time.sleep(2)
                    self.driver.find_element(*PinLock.SAVE_NEW_PIN).click()
                    self.report_pass('Android APP: Pin lock set pin is selected screen Successfully')
                else:
                    self.report_fail('Android APP: Pin Lock Not set')    
                    
            except:
                self.report_fail('IOS App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(traceback.format_exc().replace('File', '$~File'))) 



    def validate_pin(self):
        if self.reporter.ActionStatus:
            try:                
                if self.wait_for_element_exist(*PinLock.PINLOCK_CHANGE_PIN):
                        self.report_pass('Android APP: Pin lock is set successfully')
                else:
                    self.wait_for_element_exist(*PinLock.PINLOCK_STATUS_OFF)
                    self.driver.find_element(*PinLock.PINLOCK_STATUS_OFF).click()
                    self.wait_for_element_exist(*PinLock.PINLOCK_STATUS_ON)
                    self.report_pass('Android APP:Pin lock is not set successfully')
            except:
                self.report_fail('Android-App: Exception in login_hive_app Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))   
        
    def change_pin(self):  
        
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*PinLock.PINLOCK_CHANGE_PIN):
                    self.driver.find_element(*PinLock.PINLOCK_CHANGE_PIN).click()
                    self.report_pass('Android APP: Change Pin Screen is entered successfully')
                else:
                    self.report_fail('Android APP: Change Pin Screen is not entered successfully')    
                
                
                if self.wait_for_element_exist(*PinLock.ENTER_CURRENT_PIN_CHANGE):
                    self.driver.find_element(*PinLock.ENTER_CURRENT_PIN_CHANGE).send_keys("1234")
                    time.sleep(2)
                    self.driver.find_element(*PinLock.ENTER_NEW_PIN_CHANGE).send_keys("4321")
                    time.sleep(2)
                    self.driver.find_element(*PinLock.CONFIRM_NEW_PIN_CHANGE).send_keys("4321")
                    time.sleep(2)
                    self.driver.find_element(*PinLock.SAVE_CHANGE_PIN).click()
                    self.report_pass('Android APP: Old Pin is entered success')
                else:
                    self.report_fail('Android APP: Enter new pin is not entered entered')
            
            except:
                self.report_fail('Android App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(traceback.format_exc().replace('File', '$~File'))) 

    def forgot_pin_lock(self):    
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*PinLock.PINLOCK_FORGOT_PIN):
                    time.sleep(2)
                    self.driver.find_element(*PinLock.PINLOCK_FORGOT_PIN).click()
                    self.report_pass('Android APP: Forgot Pin is selected Successfully')
                    
                else:
                    self.report_fail('Android APP: Forgot Pin is not selected Successfully')    
                            
            except:
                self.report_fail('Android App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))        
    
        
    def forgot_validate_pin(self):    
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*PinLock.PINLOCK_LOGOUT):
                    self.report_pass('Android APP: Forgot PIN is selected Successfully')
                    self.driver.find_element(*PinLock.PINLOCK_CANCEL).click()
                    time.sleep(2)
                else:
                    self.report_fail('Android APP: Forgot Pin is not done Successfully')    
                            
            except:
                self.report_fail('Android App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))


class MotionSensor(BasePage):
    
    def navigate_to_motion_sensor_page(self): 
        if self.reporter.ActionStatus:
            try:
                if not self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper().find('MOTION SENSOR') >= 0:
                    print(self.driver.find_element(*HomePageLocators.CURRENT_TITLE).text)
                    if self.currentAppVersion == 'V6':
                            time.sleep(2)   
                            self.driver.find_element(*HomePageLocators.MENU_BUTTON_SHOW).click()
                            if self.wait_for_element_exist(*HomePageLocators.HEAT_WATER_MAIN_MENU):
                                self.driver.find_element(*HomePageLocators.HEAT_WATER_MAIN_MENU).click()
                                time.sleep(2)                                
                                
                                if self.wait_for_element_exist(*HoneycombDasbordLocators.HONEYCOMB_MOTION_SENSOR):
                                    self.driver.find_element(*HoneycombDasbordLocators.HONEYCOMB_MOTION_SENSOR).click()
                                    time.sleep(2)
                                    self.driver.find_element(*self.REFRESH_BUTTON).click() 
                                    print("Navigated to motion sensor page")
                                
                                elif self.wait_for_element_exist(*HomePageLocators.HEAT_WATER_MAIN_MENU):
                                    self.driver.find_element(*HomePageLocators.HEAT_WATER_MAIN_MENU).click()
                                    print("page going to scroll")
                                    time.sleep(2)                           
                                    self.driver.swipe(1300,2300,80,2300,2000)
                                    time.sleep(2) 
                                    self.driver.find_element(*HoneycombDasbordLocators.HONEYCOMB_MOTION_SENSOR).click()
                                    time.sleep(2)  
                                    self.driver.find_element(*self.REFRESH_BUTTON).click()
                                    
                                    print("Navigated to motion sensor page")
                              
                else:
                        self.report_fail("Android-App : Motion heating not found")
                
            except:
                self.report_fail('Android App : NoSuchElementException: in navigate_to_heating_homepage Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
   
   
    def navigate_to_eventlogs(self):
        if self.reporter.ActionStatus:
            try: 
                if self.wait_for_element_exist(*HoneycombDasbordLocators.HONEYCOMB_DEVICE_OFFLINE):
                    self.report_pass('Android App : The motion sensor is offline. No validations possible.')
                elif self.wait_for_element_exist(*HoneycombDasbordLocators.DEVICE_TODAYS_LOGS):
                    self.driver.find_element(*HoneycombDasbordLocators.DEVICE_TODAYS_LOGS).click()
                    print("Navigated to event logs screen successfully")
                    self.report_pass('Android App : Navigated to event logs of Motion Sensor screen')
                
                else:
                    self.report_fail('Android App : Navigation to event log failed')
                    
                if self.wait_for_element_exist(*HoneycombDasbordLocators.DEVICE_TODAYS_LOGS_CLOSE):
                    self.driver.find_element(*HoneycombDasbordLocators.DEVICE_TODAYS_LOGS_CLOSE).click()
            except:
                self.report_fail('Android App : NoSuchElementException: in navigate_to_eventlogs Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))       
    
    def verify_event_logs(self):
        if self.reporter.ActionStatus:
            try:
                if self.driver.find_element(*HoneycombDasbordLocators.HONEYCOMB_DEVICE_OFFLINE):
                    self.report_pass('Android App : The motion sensor is offline. No validations possible.')
                else:
                    if (self.wait_for_element_exist(*MotionSensorLocators.NO_MOTION_CURRENTLY)):
                        self.report_pass('Android App : Verified there are no logs present in Motion Sensor screen currently')
                    elif (self.wait_for_element_exist(*MotionSensorLocators.MOTION_DETECTED)):
                        self.report_pass('Android App : Verified there is  motion log present in Motion Sensor screen')
                    elif (self.wait_for_element_exist(*MotionSensorLocators.NO_MOTION_CURRENTLY)):
                        self.report_pass('Android App : Verified there are multiple logs present in Motion Sensor screen')
                    else:
                        self.report_fail('Android App : Unexpected logs found')
            
                if (self.wait_for_element_exist(*HoneycombDasbordLocators.DEVICE_TODAYS_LOGS_CLOSE)):
                        self.driver.find_element(*HoneycombDasbordLocators.DEVICE_TODAYS_LOGS_CLOSE).click()                
            except:
                self.report_fail('IOS App : NoSuchElementException: in verify_event_logs Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
  
    def verify_current_status(self):
        if self.reporter.ActionStatus:
            try:          
                if self.wait_for_element_exist(*HoneycombDasbordLocators.HONEYCOMB_DEVICE_OFFLINE):
                    time.sleep(1)
                    print("Device offline")
                    self.report_pass('Android App : The motion sensor is offline. No validations possible.')
                else:
                    if self.wait_for_element_exist(*MotionSensorLocators.MOTION_DETECTED):
                        print("Motion Sensor has detected motion. Call API validation")
                        self.report_pass('Android App : Current motion status verified as in motion')
                        time.sleep(5)
                    elif self.wait_for_element_exist(*MotionSensorLocators.NO_MOTION_CURRENTLY):
                        print("Motion Sensor has not detected motion. Call API validation")
                        self.report_pass('Android App : Current motion status verified as no motion')
                        time.sleep(5)
                    else:
                        self.report_fail('Android App : The given Motion Sensor does not exist in the kit')
            except:
                self.report_fail('Android App : NoSuchElementException: in verify_event_logs Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))       
    
        
class ContactSensor(BasePage):
    
    def navigate_to_contact_sensor_page(self): 
        if self.reporter.ActionStatus:
            try:
                if not self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper().find('WIN/DOOR SENSOR') >= 0:
                    print(self.driver.find_element(*HomePageLocators.CURRENT_TITLE).text)
                    if self.currentAppVersion == 'V6':
                            time.sleep(2)   
                            self.driver.find_element(*HomePageLocators.MENU_BUTTON_SHOW).click()
                            if self.wait_for_element_exist(*HomePageLocators.HEAT_WATER_MAIN_MENU):
                                self.driver.find_element(*HomePageLocators.HEAT_WATER_MAIN_MENU).click()
                                time.sleep(2)                                
                                if self.wait_for_element_exist(*HoneycombDasbordLocators.HONEYCOMB_WINDOW_SENSOR):
                                    time.sleep(1)
                                    self.driver.find_element(*HoneycombDasbordLocators.HONEYCOMB_WINDOW_SENSOR).click()
                                if not self.wait_for_element_exist(*HoneycombDasbordLocators.HONEYCOMB_WINDOW_SENSOR): 
                                    time.sleep(1)  
                                    self.driver.swipe(1300,2300,80,2300,2000)
                                    time.sleep(2)
                                    self.driver.find_element(*HoneycombDasbordLocators.HONEYCOMB_WINDOW_SENSOR).click()
                                    
                                    self.driver.find_element(*self.REFRESH_BUTTON).click()
                                                             
                                elif (HoneycombDasbordLocators.HONEYCOMB_DEVICE_OFFLINE):
                                    print("Motion sensor is offline")
                                    self.report_pass('Android App : Navigated to MOtion Sensor screen where the sensor is offline')
                                    time.sleep(3) 
                                else:
                                    self.report_fail('Android APP:Not able to find MOtion Sensor') 
                                    
                                
                                                                   
    
                                        
                else:
                        self.report_fail("Android-App : Motion heating not found")
                
            except:
                self.report_fail('Android App : NoSuchElementException: in navigate_to_heating_homepage Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
    def navigate_to_eventlogs(self):
        if self.reporter.ActionStatus:
            try: 
                if self.driver.is_element_present(*HoneycombDasbordLocators.HONEYCOMB_DEVICE_OFFLINE):
                    self.report_pass('Android App : The motion sensor is offline. No validations possible.')
                elif self.wait_for_element_exist(*HoneycombDasbordLocators.DEVICE_TODAYS_LOGS):
                    self.driver.find_element(*HoneycombDasbordLocators.DEVICE_TODAYS_LOGS).click()
                    print("Navigated to event logs screen successfully")
                    self.report_pass('Android App : Navigated to event logs of Motion Sensor screen')
                    time.sleep(5)
                else:
                    self.report_fail('Android App : Navigation to event log failed')
                    
                if self.driver.is_element_present(*HoneycombDasbordLocators.DEVICE_TODAYS_LOGS_CLOSE):
                    self.driver.find_element(*HoneycombDasbordLocators.DEVICE_TODAYS_LOGS_CLOSE).click()
            except:
                self.report_fail('Android App : NoSuchElementException: in navigate_to_eventlogs Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))       
    
    def verify_event_logs(self):
        if self.reporter.ActionStatus:
            try:
                if self.driver.is_element_present(*HoneycombDasbordLocators.HONEYCOMB_DEVICE_OFFLINE):
                    self.report_pass('Android App : The motion sensor is offline. No validations possible.')
                else:
                    if (self.wait_for_element_exist(*MotionSensorLocators.NO_MOTION_CURRENTLY)):
                        self.report_pass('Android App : Verified there are no logs present in Motion Sensor screen currently')
                    elif (self.wait_for_element_exist(*MotionSensorLocators.NO_MOTION_CURRENTLY)):
                        self.report_pass('Android App : Verified there is current motion log present in Motion Sensor screen')
                    elif (self.wait_for_element_exist(*MotionSensorLocators.NO_MOTION_CURRENTLY)):
                        self.report_pass('Android App : Verified there are multiple logs present in Motion Sensor screen')
                    else:
                        self.report_fail('Android App : Unexpected logs found')
            
                if (self.wait_for_element_exist(*HoneycombDasbordLocators.DEVICE_TODAYS_LOGS_CLOSE)):
                        self.driver.find_element(*HoneycombDasbordLocators.DEVICE_TODAYS_LOGS_CLOSE).click()                
            except:
                self.report_fail('IOS App : NoSuchElementException: in verify_event_logs Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
  
    def verify_current_status(self):
        if self.reporter.ActionStatus:
            try: 
                if self.driver.is_element_present(*HoneycombDasbordLocators.HONEYCOMB_DEVICE_OFFLINE):
                    self.report_pass('Android App : The motion sensor is offline. No validations possible.')
                else:
                    if self.wait_for_element_exist(*MotionSensorLocators.NO_MOTION_CURRENTLY):
                        print("Motion Sensor has detected motion. Call API validation")
                        self.report_pass('Android App : Current motion status verified as in motion')
                        time.sleep(5)
                    elif self.wait_for_element_exist(*MotionSensorLocators.NO_MOTION_CURRENTLY):
                        print("Motion Sensor has not detected motion. Call API validation")
                        self.report_pass('Android App : Current motion status verified as no motion')
                        time.sleep(5)
                    else:
                        self.report_fail('Android App : The given Motion Sensor does not exist in the kit')
            except:
                self.report_fail('Android App : NoSuchElementException: in verify_event_logs Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))       
    
        
