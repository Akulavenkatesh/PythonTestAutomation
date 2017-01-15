'''
Created on 16 Jun 2015

@author: ranganathan.veluswamy

@author: Hitesh Sharma 15 July 2016
@note:
1. naivgate_to_ZoneNotificaiton function is used to navigate to Heating notification screen
2. setHighTemperature and setLowTemperature functions enables navigation to Maximum Temperature screen and Minimum Temperature respectively to validate that all elements are present correctly on screen
3. receiveWarnings function enable to set ON/OFF warnings.
4. setNotificationONtoOFF function reset the High and Low Target temperature and disable heating notification (warnings)
5. set_target_Heating_notification_temperature set the the desired temperature(Min and Max)
'''

#from element import BasePageElement
from datetime import datetime, timedelta
import os
import time
import traceback
import math
#import FF_alertmeApi as ALAPI

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from EE_Locators_iOSApp import DashboardPageLocators, RecipeScreenLocators
from EE_Locators_iOSApp import DashboardTutorialPageLocators
from EE_Locators_iOSApp import ChangePasswordLocators
from EE_Locators_iOSApp import EditTimeSlotPageLocators, TextControlLocators, HolidayModePageLocators
from selenium.webdriver.common.by import By
from EE_Locators_iOSApp import HeatingControlPageLocators
from EE_Locators_iOSApp import HeatingNotification
from EE_Locators_iOSApp import HomePageLocators
from EE_Locators_iOSApp import HotWaterControlPageLocators
from EE_Locators_iOSApp import LoginPageLocators
from EE_Locators_iOSApp import PinLockPageLocators
from EE_Locators_iOSApp import SchedulePageLocators
from EE_Locators_iOSApp import MotionSensorPageLocators
from EE_Locators_iOSApp import BulbScreenLocators

import FF_Platform_Utils as oAPIValidations
import FF_ScheduleUtils as oSchedUtils
import FF_utils as utils
from EE_Locators_iOSApp import ContactSensorLocators


class BasePage(object):

    #Contructor for BasePage
    def __init__(self, driver, reporter):
        self.driver = driver
        self.reporter = reporter 
        self.currentAppVersion = utils.getAttribute('common', 'currentAppVersion').upper()
        self.EXPLICIT_WAIT_TIME = 25
        self.stopBoost = True
    
    #Waits for the given element exists for EXPLICIT_WAIT_TIME 
    def wait_for_element_exist(self, by, value, intWaitTime = 0):
        if intWaitTime == 0: intWaitTime = self.EXPLICIT_WAIT_TIME
        try:
            wait = WebDriverWait(self.driver, intWaitTime)
            wait.until(EC.presence_of_element_located((by, value)))
            time.sleep(1)
            return True
        except TimeoutException:
            return False
        print(by, value, 'element not found')
        
    #Initializes the Appium Android Web Driver
    def setup_ios_driver(self, strDeviceName, strAppPath):
        try:
            desired_caps = {}
            desired_caps['appium-version'] = '1.0'
            desired_caps['platformName'] = 'iOS'
            desired_caps['platformVersion'] = utils.getAttribute('iOS', 'platformVersion')
            desired_caps['udid'] = utils.getAttribute('iOS', 'udid')
            desired_caps['deviceName'] = strDeviceName
            desired_caps['app'] = os.path.abspath(strAppPath)
            desired_caps['noReset'] = True
            
            iOSDriver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
            iOSDriver.implicitly_wait(30)
            
            return iOSDriver
        except: 
            self.report_fail('Exception in setup_ios_driver Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))

            
    
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
    def scroll_element_to_value(self, oScrolElement, fltCurrentValue, fltSetValue, fltPrecision, fltScrolPrecesion):
        intLeftX = oScrolElement.location['x']
        intUpperY = oScrolElement.location['y']
        intWidth = oScrolElement.size['width']
        intHieght = oScrolElement.size['height']
        intStX = intLeftX + intWidth/2
        intEndX = intStX
        intEndY = intUpperY + fltScrolPrecesion* (intHieght/4)
        intStY = intUpperY + 3*(intHieght/4)
        intScrolTime = 500
        if fltPrecision != 0.5:
            intEndY = intUpperY + 2.2* (intHieght/4)
            intStY = intUpperY + 1.8*(intHieght/4)
            intScrolTime = 500
        if not fltSetValue==fltCurrentValue:
            if fltSetValue < fltCurrentValue:
                intTemp = intEndY
                intEndY = intStY
                intStY = intTemp
            intIterCount = int(abs(fltSetValue-fltCurrentValue)/fltPrecision)
            for intCnt in range(intIterCount):
                self.driver.swipe(intStX, intEndY, intEndX, intStY, intScrolTime)
    
  
    #Scrolls on the Scrollable element to set the specific value passed for HolidayMode Page 
    def scroll_element_to_value_date(self, oScrolElement, fltCurrentValue, fltSetValue, fltPrecision):
        intLeftX = oScrolElement.location['x']
        intUpperY = oScrolElement.location['y']
        intWidth = oScrolElement.size['width']
        intHieght = oScrolElement.size['height']
        intStX = intLeftX + intWidth/2
        intStY = intUpperY +(intHieght/4)
        intEndX = intStX
        intEndY = intUpperY + (intHieght/8)
        intSize=len(fltSetValue)     
        if intSize>2:
            fltdate=fltSetValue.split(' ')[1]
            while not fltdate in fltCurrentValue:
                self.iOSDriver.swipe(intStX, intStY, intEndX, intEndY, 1000)
                fltCurrentValue=int(oScrolElement.get_attribute('value').split(' ')[0])      
        else:
            if not fltSetValue==fltCurrentValue:
                intIterCount = int(abs(fltSetValue-fltCurrentValue)/fltPrecision)
                for intCnt in range(intIterCount):
                    print(intCnt)
                    self.iOSDriver.swipe(intStX, intStY, intEndX, intEndY, 1000)
                    time.sleep(0.5)
    
    #Method for Skipping Dashboard Tutorial
    def skip_Dashboard_tutorial(self):       
        try:
            
            self.driver.find_element(*DashboardTutorialPageLocators.NEXT_BUTTON).click()
            time.sleep(2)
            self.driver.find_element(*DashboardTutorialPageLocators.TAP_GOTO_DEVICE).click()
            time.sleep(2)
            self.driver.find_element(*DashboardTutorialPageLocators.TAP_GOTO_DEVICE_LIST).click()
            time.sleep(2)
            self.driver.find_element(*DashboardTutorialPageLocators.DONE_BTN).click()
            
            if self.driver.find_element(*HomePageLocators.MENU_BUTTON): 
                self.report_pass('iOS-App: The Hive iOS App is successfully Logged in') 
                
        except:
            self.report_fail('iOS-App: Exception in skip_Dashboard_tutorial\n {0}'.format(traceback.format_exc().replace('File', '$~File')))

    def is_element_present(self, by,value=None):        
    #Return a boolean value for an  element presence
        try: 
            self.find_element(by,value)
        
        except NoSuchElementException as e: return False
        return True       
    #Refresh Page
    def refresh_page(self):     
        self.driver.swipe(200, 200, 200, 500, 500)
        time.sleep(3)
        
    #Add/Delete Events to match the expected count
    def add_or_remove_events(self, intExpectedEventCount):
        self.report_done('iOS APP: ScreenShot of existing schedule')
        #Get Event Count
        lstEvent = self.driver.find_elements(*SchedulePageLocators.EVENT_ARROW)
        intActualCount = len(lstEvent)
        print(intActualCount, intExpectedEventCount)
        if intActualCount > intExpectedEventCount:
            #Delete Event
            self.report_step('Deleting additional events')
            for intCntr in range((intActualCount -1), intExpectedEventCount-1, -1):
                lstEvent[intCntr].click()
                self.report_done('iOS APP: Deleting additional event number : ' + str(intCntr + 1))
                self.driver.find_element(*EditTimeSlotPageLocators.DELETE_EVENT_BUTTON).click()  
                self.driver.find_element(*EditTimeSlotPageLocators.DELETE_CONFIRM_BUTTON).click()  
                time.sleep(1)
                self.wait_for_element_exist(*SchedulePageLocators.TODAY_SCHEDULE_BUTTON)
        elif intActualCount < intExpectedEventCount:
            #Add Event
            self.report_step('Adding additional events')
            for intCntr in range((intExpectedEventCount - 1), intActualCount - 1, -1):
                self.driver.find_element(*SchedulePageLocators.SCHEDULE_OPTIONS_BUTTON).click() 
                self.wait_for_element_exist(*SchedulePageLocators.ADD_TIME_SLOT_SUBMENU)
                self.driver.find_element(*SchedulePageLocators.ADD_TIME_SLOT_SUBMENU).click() 
                self.report_done('iOS APP: Adding additional event number : ' + str(intCntr + 1))
                self.driver.find_element(*EditTimeSlotPageLocators.SAVE_BUTTON).click()  
                self.wait_for_element_exist(*SchedulePageLocators.TODAY_SCHEDULE_BUTTON)
        
        self.refresh_page()
        self.report_pass('ScreenShot after all additional events are added/removed')

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
                
                self.refresh_page()            
            except:
                self.report_fail('Exception in _navigate_to_day Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))

    #Set the Even Target temperature
    def set_schedule_event_hour(self, intSetHour):
        if self.reporter.ActionStatus:
            try: 
                if self.wait_for_element_exist(*EditTimeSlotPageLocators.TITLE_LABEL):
                    oScrolElement = self.driver.find_element(*EditTimeSlotPageLocators.HOUR_SCROLL)
                    intSetHour = int(intSetHour)
                    intCurrentHour = int(oScrolElement.get_attribute('value').split(' ')[0])  
                    intCntrIter = 1
                    while (intCurrentHour != intSetHour) and (intCntrIter < 3):
                        self.scroll_element_to_value(oScrolElement, intCurrentHour, intSetHour, 1, 3)
                        intCurrentHour = int(oScrolElement.get_attribute('value').split(' ')[0])  
                        intCntrIter =+1
                    if intCurrentHour == intSetHour:
                        self.report_pass('The start time Hour is successfully set to : ' + str(intSetHour))
                    else:   
                        self.report_fail('Unable to set the start time Hour to : ' + str(intSetHour))
                    
                else:
                    self.report_fail("iOS APP: Control not active on the Edit Time Slot for Heating schedule Page to set the Event start time Hour")
                
            except:
                self.report_fail('iOS APP: Exception in set_schedule_event_hour Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
    
    #Set the Even Target temperature
    def set_schedule_event_minute(self, intSetMinute):
        if self.reporter.ActionStatus:
            try: 
                if self.wait_for_element_exist(*EditTimeSlotPageLocators.TITLE_LABEL):
                    oScrolElement = self.driver.find_element(*EditTimeSlotPageLocators.MINUTE_SCROLL)
                    intSetMinute = int(intSetMinute)
                    intCurrentMinute = int(oScrolElement.get_attribute('value').split(' ')[0])  
                    intCntrIter = 1
                    while (intCurrentMinute != intSetMinute) and (intCntrIter < 3):
                        self.scroll_element_to_value(oScrolElement, intCurrentMinute, intSetMinute, 15, 3.4)
                        intCurrentMinute = int(oScrolElement.get_attribute('value').split(' ')[0])  
                        intCntrIter =+1
                    if intCurrentMinute == intSetMinute:
                        self.report_pass('iOS APP: The start time minute is successfully set to : ' + str(intSetMinute))
                    else:   
                        self.report_fail('iOS APP: Unable to set the start time minute to : ' + str(intSetMinute))
                else:
                    self.report_fail("iOS APP: Control not active on the Edit Time Slot for Heating schedule Page to set the Event start time Minute")
                
            except:
                self.report_fail('iOS APP: Exception in set_schedule_event_minute Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))


        
    #Click Element via TouchAction
    def click_element(self, by, value = None):
        if value == None: oElement = by
        else: oElement = self.driver.find_element(by, value)
        action = TouchAction(oElement.parent)
        action.press(oElement).perform()
        

#Page Class for Login page. Has all the methods for the Login page
class LoginPage(BasePage):
    #Log in to the Hive Mobile App
    def login_hive_app(self, strUserName, strPassword):
        #self.driver.reset()
        try:
            if self.driver.is_element_present(*DashboardTutorialPageLocators.RHCDASHBOARD_IMAGE):
                print("Skipping Dashboard Tutorial")
                self.skip_Dashboard_tutorial() 
    
            if  self.driver.is_element_present(*LoginPageLocators.TITLE_LABEL):               
                self.driver.find_element(*LoginPageLocators.USERNAME_EDTBOX).send_keys(strUserName)
                self.driver.find_element(*LoginPageLocators.PASSWORD_EDTBOX).send_keys(strPassword)
                time.sleep(2)
                self.driver.find_element(*LoginPageLocators.LOGIN_BUTTON).click()
        
                if self.driver.is_element_present(*DashboardTutorialPageLocators.RHCDASHBOARD_IMAGE):
                    self.skip_Dashboard_tutorial()
                
                elif self.driver.find_element(*HomePageLocators.MENU_BUTTON):
                    self.report_pass('iOS-App: The Hive iOS App is successfully Logged in')       

                else:
                    self.report_fail('iOS-App: The Hive iOS App is not logged in. Please check the Login credentials and re-execute test.')                            
            else:
                    self.report_fail('iOS-App: The Hive iOS App is not logged in. Please check the Login credentials and re-execute test.')
                               
        except:
            self.report_fail('iOS-App: Exception in login_hive_app Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))

    

#Page Class for Home page. Has all the methods for the Home page
class HomePage(BasePage):
    #Navigates to the Heating control Page
    def navigate_to_heating_control_page(self, boolStopBoost = True):
        if self.reporter.ActionStatus:
            try:
                if not self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper().find('HEATING CONTROL') >= 0:
                    print(self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name'))
                    
                    if self.wait_for_element_exist(*DashboardPageLocators.HONEYCOMB_DASHBOARD_BUTTON):
                        self.driver.find_element(*DashboardPageLocators.HONEYCOMB_DASHBOARD_BUTTON).click()
                        time.sleep(2)                      
                        self.driver.find_element(*DashboardPageLocators.HEAT_CONTROL_DASHBOARD).click()
                        
                    elif self.wait_for_element_exist(*DashboardPageLocators.DEVICE_LIST_BUTTON):
                        self.driver.find_element(*DashboardPageLocators.HEAT_CONTROL_DASHBOARD).click()
                        time.sleep(2)
                        
                    print(self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name'))
                    if self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper().find('HEATING BOOST') >= 0:
                        if not boolStopBoost:                                
                            self.report_pass('iOS-App: Successfully navigated to the Heat BOOST Control Page -' )
                            return True
                        if self.driver.is_element_present(*HeatingControlPageLocators.BOOST_STOP):
                            self.driver.find_element(*HeatingControlPageLocators.BOOST_STOP).click()
                            time.sleep(2)
                            if self.driver.is_element_present(*HeatingControlPageLocators.TARGET_TEMPERATURE_SCROLL):
                                self.report_pass('iOS-App: Successfully navigated to the Heating Control Page')
                            else:
                                self.report_fail('iOS-App: Unable to navigate to Heating Control Page')    
                                       
                    elif self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper().find('HEATING') >= 0:
                        self.report_pass('iOS-App: Successfully navigated to the Heating Control Page')
                    else:
                        self.report_fail("iOS-App: Control not active on the Main Home Page to Navigate to Heating Control Page")
                
            except:
                self.report_fail('iOS-App: Exception in navigate_to_heating_conrtol_page Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))

    #Navigates to the Heating Schedule Page
    def navigate_to_heating_schedule_page(self):
        if self.reporter.ActionStatus:
            try:
                if not self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper().find('HEATING SCHEDULE') >= 0:
                    print(self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name'))
                    if self.wait_for_element_exist(*DashboardPageLocators.HONEYCOMB_DASHBOARD_BUTTON):
                        self.driver.find_element(*DashboardPageLocators.HONEYCOMB_DASHBOARD_BUTTON).click()
                        time.sleep(2)                      
                    
                    elif self.wait_for_element_exist(*DashboardPageLocators.DEVICE_LIST_BUTTON):
                        self.driver.find_element(*DashboardPageLocators.HEAT_CONTROL_DASHBOARD).click()
                        time.sleep(2)
                        self.driver.find_element(*DashboardPageLocators.TAB_BAR_SCHEDULE_BUTTON).click()
                        time.sleep(2)
                        if self.wait_for_element_exist(*SchedulePageLocators.TODAY_SCHEDULE_BUTTON):
                            self.report_pass('iOS-App: Successfully navigated to the Heating Schedule Page')
                        else:
                            self.report_fail('iOS-App: Unable to navigate to Heating Schedule Page')
                    else:
                        self.report_fail("iOS-App: Control not active on the Main Home Page to Navigate to Heating Schedule Page")
                
            except:
                self.report_fail('iOS-App: Exception in navigate_to_heating_schedule_page Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))

    #Navigates to the Hot water Home Page
    def navigate_to_hot_water_control_page(self, boolStopBoost = True):
        if self.reporter.ActionStatus:
            try: 
                self.refresh_page()
                if not self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper().find('HOT WATER CONTROL') >= 0:    
                                
                    if self.driver.is_element_present(*DashboardPageLocators.HONEYCOMB_DASHBOARD_BUTTON):
                        self.driver.find_element(*DashboardPageLocators.HONEYCOMB_DASHBOARD_BUTTON).click()
                        time.sleep(2)
                        self.driver.find_element(*DashboardPageLocators.HOT_WATER_CONTROL_DASHBOARD).click()
                        
                    elif self.driver.is_element_present(*DashboardPageLocators.DEVICE_LIST_BUTTON):
                        self.driver.find_element(*DashboardPageLocators.HOT_WATER_CONTROL_DASHBOARD).click()
                        time.sleep(2)
                    print(self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name'))
                    if self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper().find('HOT WATER BOOST') >= 0:
                        if not boolStopBoost:                                
                            self.report_pass('iOS-App: Successfully navigated to the Hot Water Control Page -')
                            return True
                        if self.driver.is_element_present(*HotWaterControlPageLocators.BOOST_STOP):
                            self.driver.find_element(*HotWaterControlPageLocators.BOOST_STOP).click()
                            time.sleep(2)
                        if self.wait_for_element_exist(*HotWaterControlPageLocators.BOOST_MODE_LINK):
                            self.report_pass('iOS-App: Successfully navigated to the Hot Water Control Page')
                        else:
                            self.report_fail('iOS-App: Unable to navigate to Hot Water Control Page')
                    elif self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper().find('HOT WATER CONTROL') >= 0:
                        self.report_pass('iOS-App: Successfully navigated to the Hot Water Control Page -')
                    else:
                        self.report_fail("iOS-App: Control not active on the Main Home Page to Navigate to Hot Water Control Page")
            except:
                self.report_fail('iOS-App: Exception in navigate_to_hot_water_control_page Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))

    #Navigates to the Hot water schedule Home Page
    def navigate_to_hot_water_schedule_page(self):
        
        if self.reporter.ActionStatus:
            try: 
                if not self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper().find('HOT WATER SCHEDULE') >= 0:                

                    if self.driver.is_element_present(*DashboardPageLocators.HONEYCOMB_DASHBOARD_BUTTON):
                        self.driver.find_element(*DashboardPageLocators.HONEYCOMB_DASHBOARD_BUTTON).click()
                        time.sleep(2)
                        self.driver.find_element(*DashboardPageLocators.HOT_WATER_CONTROL_DASHBOARD).click()
                        time.sleep(2)
                        self.driver.find_element(*DashboardPageLocators.TAB_BAR_SCHEDULE_BUTTON).click()
                        
                    elif self.driver.is_element_present(*DashboardPageLocators.DEVICE_LIST_BUTTON):
                        self.driver.find_element(*DashboardPageLocators.HOT_WATER_CONTROL_DASHBOARD).click()
                        time.sleep(2)
                        self.driver.find_element(*DashboardPageLocators.TAB_BAR_SCHEDULE_BUTTON).click()
                        time.sleep(2)
                    strTitile = self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name')
                    if self.driver.is_element_present(*SchedulePageLocators.TODAY_SCHEDULE_BUTTON) and  strTitile.upper().find('HOT WATER SCHEDULE') >=0:
                        self.report_pass('iOS-App: Successfully navigated to the Hot Water Schedule Page')
                    else:
                        self.report_fail('iOS-App: Unable to navigate to Hot Water Schedule Page')
                
                elif self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name').upper().find('HOT WATER SCHEDULE') >= 0:
                    self.report_pass("iOS-App: Successfully navigated to the Hot Water Schedule Page")                
                else:
                    self.report_fail("iOS-App: Control not active on the Main Home Page to Navigate to Hot Water Schedule Page")
            except:
                self.report_fail('iOS-App: Exception in navigate_to_hot_water_control_page Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))

    #Log out of the Hive Mobile App
    
    def logout_hive_app(self):
        #self.driver.reset()
        try: 
            
            if self.driver.is_element_present(*DashboardTutorialPageLocators.RHCDASHBOARD_IMAGE):
                self.skip_Dashboard_tutorial() 
                
            if self.driver.is_element_present(*LoginPageLocators.LOGIN_BUTTON):
                self.report_pass('iOS-App: The Hive iOS App is already Logged out')
                    
            elif self.driver.is_element_present(*HomePageLocators.MENU_BUTTON):
                self.driver.find_element(*HomePageLocators.MENU_BUTTON).click()
                self.driver.swipe(200, 500, 200, 200, 500) 
                self.wait_for_element_exist(*LoginPageLocators.LOG_OUT_BUTTON)
                self.driver.find_element(*LoginPageLocators.LOG_OUT_BUTTON).click()
                
            elif self.wait_for_element_exist(*DashboardPageLocators.HONEYCOMB_DASHBOARD_BUTTON):
                self.driver.find_element(*DashboardPageLocators.HONEYCOMB_DASHBOARD_BUTTON).click()
                self.driver.find_element(*HomePageLocators.MENU_BUTTON).click()
                self.driver.swipe(200, 500, 200, 200, 500) 
                self.wait_for_element_exist(*LoginPageLocators.LOG_OUT_BUTTON)
                self.driver.find_element(*LoginPageLocators.LOG_OUT_BUTTON).click()
            if self.driver.find_element(*LoginPageLocators.LOGIN_BUTTON):
                print('iOS-App: The Hive iOS App is successfully Logged out')
                        #self.report_pass('iOS-App: The Hive iOS App is successfully Logged out')
            else: 
                self.report_fail('iOS-App: Not able to Logout the Hive iOS App ')
                
        except:
            self.report_fail('iOS-App: Exception in logout_hive_app Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))                

    #Navigate To ChangePassword Screen
    def navigate_to_screen(self,strPageName):
        
        if self.reporter.ActionStatus:
            try: 
                
                if self.wait_for_element_exist(*HomePageLocators.MENU_BUTTON):
                    self.driver.find_element(*HomePageLocators.MENU_BUTTON).click()
                    time.sleep(2)
                    self.driver.find_element(*HomePageLocators.SETTINGS_MAIN_MENU).click()
                    if 'PASSWORD' in strPageName.upper():
                        if self.wait_for_element_exist(*HomePageLocators.CHANGE_PASSWORD_SUB_MENU):                             
                            self.driver.find_element(*HomePageLocators.CHANGE_PASSWORD_SUB_MENU).click()
                            time.sleep(2)
                            self.report_pass('iOS-App: Successfully navigated to the Change Password Page')
                        else:
                            self.report_fail("IOS-App : Control not active on the Change Password Page")
                    else:                         
                        self.driver.find_element(*HomePageLocators.MENU_BUTTON).click()
                else:
                    self.report_fail("IOS-App : Control not active on the Menu Button")               
            except:
                self.report_fail('IOS App : NoSuchElementException: in navigate_to_change_password_screen\n {0}'.format(traceback.format_exc().replace('File', '$~File')))   
            
  
#Page Class for Heating Control page. Has all the methods for the Heating Control page
class HeatingControlPage(BasePage):
    #Set Heat mode
    def set_heat_mode(self, strMode, intTemperature = None, intDuration = 1):
        if self.reporter.ActionStatus:
            try: 
                if self.wait_for_element_exist(*HeatingControlPageLocators.TARGET_TEMPERATURE_SCROLL):             
                    self.refresh_page()
                    #self.wait_for_element_exist(*HeatingHomePageLocators.REFRESH_BUTTON)
                    if strMode.upper() == 'AUTO': self.click_element(*HeatingControlPageLocators.SCHEDULE_MODE_LINK)
                    elif strMode.upper() == 'MANUAL': self.click_element(*HeatingControlPageLocators.MANUAL_MODE_LINK)
                    elif strMode.upper() == 'OFF': self.click_element(*HeatingControlPageLocators.OFF_MODE_LINK)
                    elif strMode.upper() == 'BOOST': 
                        self.driver.find_element(*HeatingControlPageLocators.BOOST_MODE_LINK).click()
                        print('intDuration', intDuration)
                        if (self.currentAppVersion == 'V6'): 
                            #Set Boost Duration
                            if (intDuration != 1):                                
                                intCurrentDuration = int(self.driver.find_element(*HeatingControlPageLocators.BOOST_TIME_SCROLL).get_attribute('value').split(' ')[0])
                                print('intCurrentDuration', intCurrentDuration)
                                print('intDuration', intDuration)
                                intCntrIter= 1
                                while (intCurrentDuration != intDuration) and (intCntrIter <3) : 
                                    time.sleep(2)
                                    self.set_boost_time_duration(intDuration)
                                    intCurrentDuration = int(self.driver.find_element(*HeatingControlPageLocators.BOOST_TIME_SCROLL).get_attribute('value').split(' ')[0])
                                    intCntrIter += 1
                            #Set Boost Target temperature
                            if (intTemperature != None):
                                oScrolElement = self.driver.find_element(*HeatingControlPageLocators.TARGET_TEMPERATURE_SCROLL)
                                oScrolElementVAlue = oScrolElement.get_attribute('value')
                                if 'point' in oScrolElementVAlue: fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[0] + '.' + oScrolElementVAlue.split(' ')[2])
                                else: fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[0])
                                intCntrIter = 1
                                while (fltCurrentTargTemp != intTemperature) and (intCntrIter < 3):
                                    self.scroll_element_to_value(oScrolElement, fltCurrentTargTemp, intTemperature, 0.5, 1)
                                    oScrolElementVAlue = oScrolElement.get_attribute('value')
                                    if 'point' in oScrolElementVAlue: fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[0] + '.' + oScrolElementVAlue.split(' ')[2])
                                    else: fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[0])
                                    intCntrIter =+1
                    time.sleep(5)
                    self.refresh_page()
                    time.sleep(5)
                    if self.wait_for_element_exist(*HeatingControlPageLocators.TARGET_TEMPERATURE_SCROLL):
                        self.report_pass('iOS-App: Successfully Heat mode is set to <B>' + strMode)
                    else:
                        self.report_fail('iOS-App: Unable to set Heat mode to <B>' + strMode)
                else:
                    self.report_fail("iOS-App: Control not active on the Heating Control Page to set the Heat Mode")
                
            except:
                self.report_fail('iOS-App: Exception in set_heat_mode Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
                
                
    #Set Target Temperature    
    def set_target_temperature(self, fltTargetTemperature):
        if self.reporter.ActionStatus:
            try: 
                if self.wait_for_element_exist(*HeatingControlPageLocators.PRESET_TEMP_BUTTON):  
                    self.refresh_page()
                    self.driver.find_element(*HeatingControlPageLocators.PRESET_TEMP_BUTTON).click()
                    self.driver.find_element(*HeatingControlPageLocators.PRESET_TEMP_BUTTON).click()
                    oScrolElement = self.driver.find_element(*HeatingControlPageLocators.TARGET_TEMPERATURE_SCROLL)
                    oScrolElementVAlue = oScrolElement.get_attribute('value')
                    if 'point' in oScrolElementVAlue: fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[0] + '.' + oScrolElementVAlue.split(' ')[2])
                    else: fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[0])
                    intCntrIter = 1
                    while (fltCurrentTargTemp != fltTargetTemperature) and (intCntrIter < 3):
                        self.scroll_element_to_value(oScrolElement, fltCurrentTargTemp, fltTargetTemperature, 0.5, 1)
                        oScrolElementVAlue = oScrolElement.get_attribute('value')
                        if 'point' in oScrolElementVAlue: fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[0] + '.' + oScrolElementVAlue.split(' ')[2])
                        else: fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[0])
                        intCntrIter =+1
                    time.sleep(5)
                    self.refresh_page()
                    
                    if fltCurrentTargTemp == fltTargetTemperature:
                        self.report_pass('iOS-App: The Target Temperature is successfully set to : ' + str(fltTargetTemperature))
                    else:   
                        self.report_fail('iOS-App: Unable to set the Target Temperature to : ' + str(fltTargetTemperature))
                else:
                    self.report_fail("iOS-App: Control not active on the Heating Control Page to set the Target Temperature")
                
            except:
                self.report_fail('iOS-App: Exception in set_target_temperature Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
                
    #Get Attributes for Heating Controls                
    def get_heating_attribute(self):
        if self.reporter.ActionStatus:
            strMode = strRunningState = fltCurrentTargTemp = None
            try: 
                self.refresh_page()
                if self.wait_for_element_exist(*HeatingControlPageLocators.PRESET_TEMP_BUTTON):
                    strScreenName = self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name')
                    if 'HEATING BOOST' in strScreenName.upper():
                        strMode = 'BOOST'
                    else: 
                        strSelectedModeLabel = self.driver.find_element(*HeatingControlPageLocators.SELECTED_MODE_LINK).text.upper()
                        print(strSelectedModeLabel)
                        if 'HEATING MODE SCHEDULE' in strSelectedModeLabel: 
                            strMode = 'AUTO'
                        elif 'HEATING MODE MANUAL' in strSelectedModeLabel: 
                            strMode = 'MANUAL'
                        elif 'HEATING MODE OFF' in strSelectedModeLabel: 
                            strMode = 'OFF'
                            
                    oScrolElement = self.driver.find_element(*HeatingControlPageLocators.TARGET_TEMPERATURE_SCROLL)
                    oScrolElementVAlue = oScrolElement.get_attribute('value')
                    if 'point' in oScrolElementVAlue: fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[0] + '.' + oScrolElementVAlue.split(' ')[2])
                    else: fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[0])
                    
                    strFlameLabel = self.driver.find_element(*HeatingControlPageLocators.FLAME_ICON).text.upper()
                    print(strFlameLabel)
                    if 'ON' in strFlameLabel: strRunningState = 'ON'
                    elif 'OFF' in strFlameLabel: strRunningState = 'OFF'
                    
                   
                else:
                    self.report_fail("iOS-App : Control not active on the Heating Control Page to get Heating Attributes")
                
                self.report_done('iOS App : Screenshot while getting attributes')
                if strRunningState == 'OFF': strRunningState= '0000'
                else: strRunningState = '0001'
                if fltCurrentTargTemp == 7.0: fltCurrentTargTemp = 1.0
                return strMode, strRunningState, fltCurrentTargTemp
            except:
                self.report_fail('iOS App : NoSuchElementException: in get_heating_attribute Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
               
#Page Class for Heating Schedule page. Has all the methods for the Heating Schedule page
class HeatingSchedulePage(BasePage):
    #Set Heating Schedule
    def set_heating_schedule(self, oScheduleDict):
        if self.reporter.ActionStatus:
            try: 
                if self.wait_for_element_exist(*SchedulePageLocators.TODAY_SCHEDULE_BUTTON):
                    print('m here')
                    for oKey in oScheduleDict.keys():
                        self._navigate_to_day(oKey)
                        oScheduleList = oSchedUtils.remove_duplicates(oScheduleDict[oKey])
                        self.add_or_remove_events(len(oScheduleList))
                        #Get List of Options & Start Time
                        lstStartTime = self.driver.find_elements(*SchedulePageLocators.EVENT_ARROW)       
                        for intCntr in range((len(lstStartTime) -1), -1, -1):
                            strSetStartTime = oScheduleList[intCntr][0]
                            fltSetTargTemp = oScheduleList[intCntr][1]
                            if fltSetTargTemp ==1.0: fltSetTargTemp = 7.0
                            lstStartTime[intCntr].click()
                            self.report_done('iOS APP: Event number : ' + str(intCntr + 1 ) + ' before the event change')
                            print(fltSetTargTemp)
                            self.set_schedule_target_temperature(fltSetTargTemp)                                
                            self.set_schedule_event_hour(strSetStartTime.split(':')[0])
                            self.set_schedule_event_minute(strSetStartTime.split(':')[1])
                            self.report_done('iOS APP: Event number : ' + str(intCntr + 1 ) + ' after the event change')
                            self.driver.find_element(*EditTimeSlotPageLocators.SAVE_BUTTON).click()  
                            self.wait_for_element_exist(*SchedulePageLocators.TODAY_SCHEDULE_BUTTON)
                            self.report_pass('iOS APP: Main Screen after Event number : ' + str(intCntr + 1 ) + ' is changed')
                        self.report_pass('iOS APP: Main Screen after all Events are changed')
                else:
                    self.report_fail("iOS APP: Control not active on the Heating Schedule Page to set the Heating Schedule")
                
            except:
                self.report_fail('iOS APP: Exception in set_heating_schedule Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
               
                
    #Set the Even Target temperature
    def set_schedule_target_temperature(self, fltSetTargTemp):
        if self.reporter.ActionStatus:
            try: 
                if self.wait_for_element_exist(*EditTimeSlotPageLocators.TITLE_LABEL):
                    oScrolElement = self.driver.find_element(*EditTimeSlotPageLocators.EVENT_TARGET_TEMPERATURE_SCROLL)
                    oScrolElementVAlue = oScrolElement.get_attribute('value')
                    if 'point' in oScrolElementVAlue: fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[0] + '.' + oScrolElementVAlue.split(' ')[2])
                    else: fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[0])
                    intCntrIter = 1
                    while (fltCurrentTargTemp != fltSetTargTemp) and (intCntrIter < 3):
                        self.scroll_element_to_value(oScrolElement, fltCurrentTargTemp, fltSetTargTemp, 0.5, 1)
                        oScrolElementVAlue = oScrolElement.get_attribute('value')
                        if 'point' in oScrolElementVAlue: fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[0] + '.' + oScrolElementVAlue.split(' ')[2])
                        else: fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[0])
                        intCntrIter =+1
                        print(fltCurrentTargTemp, fltSetTargTemp)
                    if fltCurrentTargTemp == fltSetTargTemp:
                        self.report_pass('iOS APP: The Target Temperature is successfully set to : ' + str(fltSetTargTemp))
                    else:   
                        self.report_fail('iOS APP: Unable to set the Target Temperature to : ' + str(fltSetTargTemp))
                else:
                    self.report_fail("iOS APP: Control not active on the Edit Time Slot for Heating schedule Page to set the Event Target Temperature")
                
            except:
                self.report_fail('iOS APP: Exception in set_schedule_target_temperature Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
          
#Page Class for Heating Control page. Has all the methods for the Heating Control page
class HotWaterControlPage(BasePage):
    #Set Heat mode
    def set_hot_water_mode(self, strMode, intDuration = 1): 
        if self.reporter.ActionStatus:
            try: 
                if self.wait_for_element_exist(*HotWaterControlPageLocators.BOOST_MODE_LINK):             
                    self.refresh_page()
                    time.sleep(5)
                    print('im here 1')
                    if strMode.upper() == 'AUTO': self.click_element(*HotWaterControlPageLocators.SCHEDULE_MODE_LINK)
                    elif strMode.upper() == 'MANUAL': self.click_element(*HotWaterControlPageLocators.MANUAL_MODE_LINK)
                    elif strMode.upper() == 'OFF': self.click_element(*HotWaterControlPageLocators.OFF_MODE_LINK)
                    elif strMode.upper() == 'BOOST': 
                        self.driver.find_element(*HotWaterControlPageLocators.BOOST_MODE_LINK).click()
                        print('intDuration', intDuration)
                        if (self.currentAppVersion == 'V6'): 
                            #Set Boost Duration
                            if (intDuration != 1):
                                
                                intCurrentDuration = int(self.driver.find_element(*HotWaterControlPageLocators.BOOST_TIME_SCROLL).get_attribute('value').split(' ')[0])
                                print('intCurrentDuration', intCurrentDuration)
                                print('intDuration', intDuration)
                                intCntrIter= 0 
                                while (intCurrentDuration != intDuration) and (intCntrIter <3) : 
                                    time.sleep(2)
                                    self.set_boost_time_duration(intDuration)
                                    intCurrentDuration = int(self.driver.find_element(*HotWaterControlPageLocators.BOOST_TIME_SCROLL).get_attribute('value').split(' ')[0])
                                    intCntrIter += 1
                            
                    time.sleep(5)
                    self.refresh_page()
                    time.sleep(5)
                    intCurrentDuration=1
                    if intCurrentDuration == intDuration:
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
            strMode = strRunningState = fltCurrentTargTemp = None
            try: 
                self.refresh_page()
                if self.wait_for_element_exist(*HeatingControlPageLocators.BOOST_MODE_LINK):
                    strScreenName = self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name')
                    print(strScreenName)
                    if 'HOT WATER BOOST' in strScreenName.upper():
                        strMode = 'BOOST'
                        if self.wait_for_element_exist(*HotWaterControlPageLocators.RUNNING_STATE_ON): strRunningState = 'ON'
                        else: strRunningState = 'OFF'
                    else: 
                        strSelectedModeLabel = self.driver.find_element(*HotWaterControlPageLocators.SELECTED_MODE_LINK).text.upper()
                        print(strSelectedModeLabel)
                        if 'HOT WATER MODE SCHEDULE' in strSelectedModeLabel: 
                            strMode = 'AUTO'
                            if self.wait_for_element_exist(*HotWaterControlPageLocators.RUNNING_STATE_ON): strRunningState = 'ON'
                            else: strRunningState = 'OFF'
                        elif 'HOT WATER MODE ON' in strSelectedModeLabel: 
                            strMode = 'Always ON'
                            if self.wait_for_element_exist(*HotWaterControlPageLocators.RUNNING_STATE_ON): strRunningState = 'ON'
                            else: strRunningState = 'OFF'
                        elif 'HOT WATER MODE OFF' in strSelectedModeLabel: 
                            strMode = 'Always OFF'
                            if self.wait_for_element_exist(*HotWaterControlPageLocators.RUNNING_STATE_OFF): strRunningState = 'OFF'
                            else: strRunningState = 'ON'
                
                else:
                    self.report_fail("iOS-App : Control not active on the Hot Water Control Page to get Heating Attributes")
                    
                self.report_done('iOS App : Screenshot while getting attributes')
                if strRunningState == 'OFF': strRunningState= '0000'
                else: strRunningState = '0001'
                return strMode, strRunningState, fltCurrentTargTemp
            except:
                self.report_fail('iOS App : NoSuchElementException: in get_hotwater_attribute Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))           
                
#Page Class for Hot Water Schedule page. Has all the methods for the Hot Water Schedule page
class HotWaterSchedulePage(BasePage):
    #Set Hot Water Schedule
    def set_hot_water_schedule(self, oScheduleDict):
        if self.reporter.ActionStatus:
            try: 
                if self.wait_for_element_exist(*SchedulePageLocators.TODAY_SCHEDULE_BUTTON):
                    print('m here')
                    for oKey in oScheduleDict.keys():
                        self._navigate_to_day(oKey)
                        oScheduleList = oSchedUtils.remove_duplicates(oScheduleDict[oKey])
                        self.add_or_remove_events(len(oScheduleList))
                        #Get List of Options & Start Time
                        lstStartTime = self.driver.find_elements(*SchedulePageLocators.EVENT_ARROW)       
                        for intCntr in range((len(lstStartTime) -1), -1, -1):
                            strSetStartTime = oScheduleList[intCntr][0]
                            fltSetTargTemp = oScheduleList[intCntr][1]
                            if fltSetTargTemp ==1.0: fltSetTargTemp = 7.0
                            lstStartTime[intCntr].click()
                            self.report_done('iOS APP: Event number : ' + str(intCntr + 1 ) + ' before the event change')
                            print(self.driver.find_element(*EditTimeSlotPageLocators.HOT_WATER_TOGGLE_BUTTON).get_attribute('name').upper())
                            #input(prompt)
                            if self.driver.find_element(*EditTimeSlotPageLocators.HOT_WATER_TOGGLE_BUTTON).get_attribute('name').upper().find('ON') >= 0:
                                    strCurrentState = 'ON'
                            else: strCurrentState = 'OFF' 
                                    
                            if (fltSetTargTemp  == 99.0 and strCurrentState == 'OFF') or (fltSetTargTemp  == 0.0 and strCurrentState == 'ON'): 
                                print('Clicking Toggle')
                                self.driver.find_element(*EditTimeSlotPageLocators.HOT_WATER_TOGGLE_BUTTON).click()  
                                    
                            self.set_schedule_event_hour(strSetStartTime.split(':')[0])
                            self.set_schedule_event_minute(strSetStartTime.split(':')[1])
                            self.report_done('iOS APP: Event number : ' + str(intCntr + 1 ) + ' after the event change')
                            self.driver.find_element(*EditTimeSlotPageLocators.SAVE_BUTTON).click()  
                            self.wait_for_element_exist(*SchedulePageLocators.TODAY_SCHEDULE_BUTTON)
                            self.report_pass('iOS APP: Main Screen after Event number : ' + str(intCntr + 1 ) + ' is changed')
                        self.report_pass('iOS APP: Main Screen after all Events are changed')
                else:
                    self.report_fail("iOS APP: Control not active on the Heating Schedule Page to set the Heating Schedule")
                
            except:
                self.report_fail('iOS APP: Exception in set_heating_schedule Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
               
class SetChangePassword(BasePage):
                    
    def change_password_screen(self):
        if self.reporter.ActionStatus:
            try: 
                strPassword = utils.getAttribute('common', 'password')
                if self.wait_for_element_exist(*ChangePasswordLocators.OLDPASSWORD_EDTBOX):
                    self.driver.find_element(*ChangePasswordLocators.OLDPASSWORD_EDTBOX).send_keys(strPassword)
                    self.report_pass('iOS APP: Change Password Screen: Old password is entered successfully')
                    time.sleep(2)
                else:
                    self.report_fail('iOS APP: Change Password Screen: Old password is entered successfully')
                    
                if self.wait_for_element_exist(*ChangePasswordLocators.NEWPASSWORD_EDTBOX):
                    self.driver.find_element(*ChangePasswordLocators.NEWPASSWORD_EDTBOX).send_keys('Password1' +"a")
                    self.report_pass('iOS APP: Change Password Screen: New password is entered successfully')
                    time.sleep(2)
                else:
                    self.report_fail('iOS APP: Change Password Screen: New password is entered successfully')
                 
                if self.wait_for_element_exist(*ChangePasswordLocators.RETYPEPASSWORD_EDTBOX):
                    self.driver.find_element(*ChangePasswordLocators.RETYPEPASSWORD_EDTBOX).send_keys('Password1' +"a")
                    self.report_pass('iOS APP: Change Password Screen: Retype password is entered successfully')
                    time.sleep(2)
                else:
                    self.report_fail('iOS APP: Change Password Screen: Retype password is entered successfully')
                    
                if self.wait_for_element_exist(*ChangePasswordLocators.SAVE_BUTTON):
                    self.driver.find_element(*ChangePasswordLocators.SAVE_BUTTON).click()
                    self.report_pass('iOS APP: Change Password Screen:  Password is set successfully')
                    time.sleep(2)
                else:
                    self.report_fail('iOS APP: Change Password Screen: Password is not set ,Save button is not clicked')    
                    
                           
            except:
                self.report_fail('IOS App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))   
            
        
    def navigate_to_change_password(self):    
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HomePageLocators.MENU_BUTTON):
                    self.driver.find_element(*HomePageLocators.MENU_BUTTON).click()
                    self.report_pass('iOS APP: Change Password : Navigated to Menu Successfully')
                    time.sleep(2)
                else:
                    self.report_fail('iOS APP: Change Password : Menu is not selected Successfully')    
                
                self.driver.swipe(287, 477, 285, 140, 500)
                
                if self.wait_for_element_exist(*HomePageLocators.SETTINGS_MAIN_MENU):
                    self.driver.find_element(*HomePageLocators.SETTINGS_MAIN_MENU).click()
                    self.report_pass('iOS APP: Navigated to Settings Successfully')
                    time.sleep(2)
                else:
                    self.report_fail('iOS APP: Change Password : Settings is selected Successfully') 
                    
                print('settings clicked')
                
                if self.wait_for_element_exist(*HomePageLocators.CHANGE_PASSWORD_SUB_MENU):
                    self.driver.find_element(*HomePageLocators.CHANGE_PASSWORD_SUB_MENU).click()
                    self.report_pass('iOS APP: Navigated to Change Password screen Successfully')
                    time.sleep(2)
                else:
                    self.report_fail('iOS APP: Change Password : is not selected Successfully') 
                
            
            except:
                self.report_fail('IOS App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))   
            
            
    
        
    def login_change_password(self):
        if self.reporter.ActionStatus:
            try:
                strUserName = utils.getAttribute('common', 'userName')
                strPassword = utils.getAttribute('common', 'password')
                
                if self.wait_for_element_exist(*LoginPageLocators.TITLE_LABEL):
                    self.driver.find_element(*LoginPageLocators.USERNAME_EDTBOX).set_value(strUserName)
                    self.driver.find_element(*LoginPageLocators.PASSWORD_EDTBOX).send_keys('Password1' +"a")
                    self.driver.find_element(*LoginPageLocators.LOGIN_BUTTON).click()
                if self.driver.find_element(*HomePageLocators.MENU_BUTTON): 
                    self.report_pass('iOS-App: The Hive iOS App is successfully Logged in with the Changed Password')
                else:
                    self.report_fail('iOS-App: The Hive iOS App is not logged in. Please check the Login credentials and re-execute test.')
                            
            #else:
                #self.report_fail('The Hive App is either not Launched or the Login screen is not displayed. Please check and re-execute test.')          

                self.driver.find_element(*HomePageLocators.MENU_BUTTON).click()               
                self.driver.swipe(287, 477, 285, 140, 500)
                self.driver.find_element(*HomePageLocators.CHANGE_PASSWORD_SUB_MENU).click()
                              
                
                self.driver.find_element(*ChangePasswordLocators.OLDPASSWORD_EDTBOX).send_keys('Password1' +"a")
                self.driver.find_element(*ChangePasswordLocators.NEWPASSWORD_EDTBOX).send_keys(strPassword)
                self.driver.find_element(*ChangePasswordLocators.RETYPEPASSWORD_EDTBOX).send_keys(strPassword)
                self.driver.find_element(*ChangePasswordLocators.SAVE_BUTTON).click()        
                self.driver.find_element(*HomePageLocators.MENU_BUTTON).click()
                
            except:
                self.report_fail('iOS-App: Exception in login_hive_app Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
                
  

class SaveHeatingNotification(BasePage):
    
    def naivgate_to_ZoneNotificaiton(self):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HomePageLocators.MENU_BUTTON):
                    self.driver.find_element(*HomePageLocators.MENU_BUTTON).click()
                    self.report_pass('iOS APP :  Hive user is able access Menu successfully')
                    time.sleep(2)
                else:
                    self.report_fail('iOS APP: What went wrong -> Opps! Hive user is not able to access Menu')    
                
                self.driver.swipe(287, 477, 285, 140, 500)
                
                if self.wait_for_element_exist(*HomePageLocators.SETTINGS_MAIN_MENU):
                    self.driver.find_element(*HomePageLocators.SETTINGS_MAIN_MENU).click()
                    self.report_pass('iOS APP: Hive user is able to access sub menu item Settings successfully')
                    time.sleep(2)
                else:
                    self.report_fail('iOS APP: What went wrong -> Opps! Hive user is not able to access sub menu Setting') 
                    
                if self.wait_for_element_exist(*HeatingNotification.SUB_MENU_HEATING_NOTIFICATION):
                    self.driver.find_element(*HeatingNotification.SUB_MENU_HEATING_NOTIFICATION).click()
                    self.report_pass('iOS APP: Hive user is able to navigate to Heating Notification screen successfully')
                    time.sleep(2)
                else:
                    self.report_fail('iOS APP: What went wrong -> Hive user is not able to navigate to Heating Notifications screen')
             
            except:
                self.report_fail('IOS App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))        
      
       
    def setHighTemperature(self,oTargetHighTemp):
            if self.reporter.ActionStatus:
                try:                 
                    if self.wait_for_element_exist(*HeatingNotification.MAX_TEMPRATURE_NOTSET): 
                        self.driver.find_element(*HeatingNotification.MAX_TEMPRATURE).click()
                        self.report_pass('iOS APP: Hive user is able to navigate to Maximum temperature screen successfully')
                        time.sleep(2)
                        if self.driver.find_element(*HeatingNotification.EMAIL_ME_OFF):
                            self.driver.find_element(*HeatingNotification.EMAIL_ME).click()
                            time.sleep(3)
                            self.set_target_Heating_notification_temperature(oTargetHighTemp)
                            time.sleep(3)
                            self.driver.find_element(*HeatingNotification.SAVE_CHANGES).click()
                        else:                          
                            self.driver.find_element(*HeatingNotification.BTN_BACK) 
                    else:
                        self.report_pass('iOS APP: Hive user had already set the Maximum Temperature')
                        
                except:
                        self.report_fail('iOS APP: Exception in set_heating_schedule Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
 

    def setLowTemperature(self,oTargetLowTemp):
            if self.reporter.ActionStatus:
                try:          
                    if self.wait_for_element_exist(*HeatingNotification.MIN_TEMPRATURE_NOTSET):
                        self.driver.find_element(*HeatingNotification.MIN_TEMPRATURE).click()
                        self.report_pass('iOS APP: Hive user is able to navigate to Minimum temperature screen successfully')
                        time.sleep(2)
                        if self.driver.find_element(*HeatingNotification.EMAIL_ME_OFF):
                            self.driver.find_element(*HeatingNotification.EMAIL_ME).click()
                            time.sleep(3)
                            self.set_target_Heating_notification_temperature(oTargetLowTemp)
                            self.driver.find_element(*HeatingNotification.SAVE_CHANGES).click()
                        else:                          
                            self.driver.find_element(*HeatingNotification.BTN_BACK)
                    else:
                        self.report_pass('iOS APP: Hive user had already set the Minimum Temperature')
                        
                except:
                    self.report_fail('iOS APP: Exception in set_heating_schedule Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))

                   
    def receiveWarnings(self):
        if self.reporter.ActionStatus:
                try:
                    if self.wait_for_element_exist(*HeatingNotification.RECEIVE_WARNINGS_OFF):
                            self.driver.find_element(*HeatingNotification.RECEIVE_WARNINGS).click()
                            self.report_pass('iOS APP: Hive user enabled the Receive Warnings')
                    else:
                            self.report_pass('iOS APP: Hive user had already enabled Receive Warnings')
                
                except:
                    self.report_fail('iOS APP: Exception in set_heating_schedule Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
    

    
    def set_target_Heating_notification_temperature(self, fltSetTargTemp):
        if self.reporter.ActionStatus:
            try: 
                    oScrolElement = self.driver.find_element(*HeatingNotification.TARGET_TEMPERATURE_SCROLL_HN)
                    oScrolElementVAlue = oScrolElement.get_attribute('value')
                    if 'point' in oScrolElementVAlue: fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[0] + '.' + oScrolElementVAlue.split(' ')[2])
                    else: fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[0])
                    intCntrIter = 1
                    while (fltCurrentTargTemp != fltSetTargTemp) and (intCntrIter < 3):
                        self.scroll_element_to_value(oScrolElement, fltCurrentTargTemp, fltSetTargTemp, 0.5, 1)
                        oScrolElementVAlue = oScrolElement.get_attribute('value')
                        if 'point' in oScrolElementVAlue: fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[0] + '.' + oScrolElementVAlue.split(' ')[2])
                        else: fltCurrentTargTemp = float(oScrolElementVAlue.split(' ')[0])
                        intCntrIter =+1
                        print(fltCurrentTargTemp, fltSetTargTemp)
                    if fltCurrentTargTemp == fltSetTargTemp:
                        self.report_pass('iOS APP: The Target Temperature is successfully set to : ' + str(fltSetTargTemp))
                    else:   
                        self.report_fail('iOS APP: Unable to set the Target Temperature to : ' + str(fltSetTargTemp))  
            except:
                self.report_fail('iOS APP: Exception in set_schedule_target_temperature Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
                  

    def setNotificationONtoOFF(self,strNotiState):
            if self.reporter.ActionStatus:
                try:                 
                    if self.wait_for_element_exist(*HeatingNotification.MAX_TEMPRATURE): 
                        self.driver.find_element(*HeatingNotification.MAX_TEMPRATURE).click()
                        self.report_pass('iOS APP: Hive user is able to navigate to Maximum temperature screen successfully')
                        time.sleep(2)
                        if strNotiState == 'OFF' :
                                self.driver.find_element(*HeatingNotification.EMAIL_ME).click()
                                time.sleep(2)
                                self.driver.find_element(*HeatingNotification.SAVE_CHANGES).click()
                                self.report_pass('iOS APP: Hive user turn off the Maximum Temperature')
                        else:                          
                                self.driver.find_element(*HeatingNotification.BTN_BACK)
                    if self.wait_for_element_exist(*HeatingNotification.MIN_TEMPRATURE):
                        self.driver.find_element(*HeatingNotification.MIN_TEMPRATURE).click()
                        self.report_pass('iOS APP: Hive user is able to navigate to Maximum temperature screen successfully')
                        time.sleep(2)
                        if strNotiState == 'OFF' :
                                self.driver.find_element(*HeatingNotification.EMAIL_ME).click()
                                time.sleep(2)
                                self.driver.find_element(*HeatingNotification.SAVE_CHANGES).click()
                                self.report_pass('iOS APP: Hive user turn off the Minimum Temperature')
                                time.sleep(2)   
                                self.driver.find_element(*HeatingNotification.RECEIVE_WARNINGS).click()
                                self.report_pass('iOS APP: Hive user turn off the Heating Notification')  
                    else:
                        self.report_pass('iOS APP: Hive user had already set the Maximum Temperature')
                        
                except:
                        self.report_fail('iOS APP: Exception in set_heating_schedule Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
                        
                        
class SetPinLock(BasePage):

    def navigate_to_pin_lock(self):    
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HomePageLocators.MENU_BUTTON):
                    self.driver.find_element(*HomePageLocators.MENU_BUTTON).click()
                    self.report_pass('iOS APP: Pin Lock : Navigated to Menu Successfully')
                    time.sleep(2)
                else:
                    self.report_fail('iOS APP: Pin Lock : Menu is not selected Successfully')    
                
                self.driver.swipe(287, 477, 285, 140, 500)
                
                if self.wait_for_element_exist(*HomePageLocators.SETTINGS_MAIN_MENU):
                    self.driver.find_element(*HomePageLocators.SETTINGS_MAIN_MENU).click()
                    self.report_pass('iOS APP: Navigated to Settings Successfully')
                    time.sleep(2)
                else:
                    self.report_fail('iOS APP: Pin Lock : Settings is selected Successfully') 
                    
                print('settings clicked')
                
                if self.wait_for_element_exist(*HomePageLocators.PINLOCK_SUB_MENU):
                    self.driver.find_element(*HomePageLocators.PINLOCK_SUB_MENU).click()
                    self.report_pass('iOS APP: Navigated to Pin Lock screen Successfully')
                    time.sleep(2)
                else:
                    self.report_fail('iOS APP: Pin Lock: is not selected Successfully') 
                
            
            except:
                self.report_fail('IOS App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(traceback.format_exc().replace('File', '$~File'))) 


    def set_pinlock(self):  
        
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*HomePageLocators.CURRENT_TITLE):
                    strScreenName = self.wait_for_element_exist(*HomePageLocators.CURRENT_TITLE).get_attribute('name')
                    print(strScreenName)
                    if 'PIN LOCK' in strScreenName.upper():
                        self.report_pass('iOS APP: Navigated to Set Pin Lock screen Successfully')
                    else:
                        self.report_pass('iOS APP: Navigated to Set Pin Lock screen is not Successfull')              
                    time.sleep(2)
                else:
                    self.report_fail('iOS APP: Pin Lock Screen is not selected Successfully')    
                
                if self.wait_for_element_exist(*PinLockPageLocators.PINLOCK_SETPIN):
                    self.driver.find_element(*PinLockPageLocators.PINLOCK_SETPIN).click()
                    self.report_pass('iOS APP: Pin lock set pin is selected screen Successfully')
                    time.sleep(2)
                else:
                    self.report_fail('iOS APP: Pin lock set pin is not selected screen Successfully') 
                
                if self.wait_for_element_exist(*PinLockPageLocators.PINKEY_ONE):
                    self.driver.find_element(*PinLockPageLocators.PINKEY_ONE).click()
                    time.sleep(2)
                    self.driver.find_element(*PinLockPageLocators.PINKEY_TWO).click()
                    time.sleep(2)
                    self.driver.find_element(*PinLockPageLocators.PINKEY_THREE).click()
                    time.sleep(2)
                    self.driver.find_element(*PinLockPageLocators.PINKEY_FOUR).click()
                    time.sleep(3)
                    self.report_pass('iOS APP: Enter new pin is selected success')
                else:
                    self.report_fail('iOS APP: Enter new pin is not successfully entered')
                    
                    
                if self.wait_for_element_exist(*PinLockPageLocators.PINKEY_ONE):
                    self.driver.find_element(*PinLockPageLocators.PINKEY_ONE).click()
                    time.sleep(2)
                    self.driver.find_element(*PinLockPageLocators.PINKEY_TWO).click()
                    time.sleep(2)
                    self.driver.find_element(*PinLockPageLocators.PINKEY_THREE).click()
                    time.sleep(2)
                    self.driver.find_element(*PinLockPageLocators.PINKEY_FOUR).click()
                    time.sleep(2)
                    self.report_pass('iOS APP: Re Enter  pin is selected success')
                else:
                    self.report_fail('iOS APP: Re Enter new pin is not successfully entered')
            
            except:
                self.report_fail('IOS App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(traceback.format_exc().replace('File', '$~File'))) 



    def validate_pin(self):
        if self.reporter.ActionStatus:
            try:                
                if self.wait_for_element_exist(*PinLockPageLocators.PINSET_ON):
                    strPinLock=self.wait_for_element_exist(*PinLockPageLocators.PINSET_ON).get_attribute('name')                  
                    if 'PIN LOCK' in strPinLock.upper():
                        self.report_pass('iOS APP: Pin lock is set successfully')
                    else:
                        self.report_fail('iOS APP: Pin lock is not set successfully')
                else:
                    self.report_fail('iOS APP:Pin lock is not set successfully')
            except:
                self.report_fail('iOS-App: Exception in login_hive_app Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))   
        
    def change_pin(self):  
        
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*PinLockPageLocators.PINLOCK_CHANGEPIN):
                    self.driver.find_element(*PinLockPageLocators.PINLOCK_CHANGEPIN).click()
                    self.report_pass('iOS APP: Change Pin Screen is entered successfully')
                else:
                    self.report_fail('iOS APP: Change Pin Screen is not entered successfully')    
                
                
                if self.wait_for_element_exist(*PinLockPageLocators.PINKEY_ONE):
                    self.driver.find_element(*PinLockPageLocators.PINKEY_ONE).click()
                    time.sleep(2)
                    self.driver.find_element(*PinLockPageLocators.PINKEY_TWO).click()
                    time.sleep(2)
                    self.driver.find_element(*PinLockPageLocators.PINKEY_THREE).click()
                    time.sleep(2)
                    self.driver.find_element(*PinLockPageLocators.PINKEY_FOUR).click()
                    time.sleep(3)
                    self.report_pass('iOS APP: Old Pin is entered success')
                else:
                    self.report_fail('iOS APP: Enter new pin is not entered entered')
                    
                    
                if self.wait_for_element_exist(*PinLockPageLocators.PINKEY_ONE):
                    self.driver.find_element(*PinLockPageLocators.PINKEY_ONE).click()
                    time.sleep(2)
                    self.driver.find_element(*PinLockPageLocators.PINKEY_ONE).click()
                    time.sleep(2)
                    self.driver.find_element(*PinLockPageLocators.PINKEY_ONE).click()
                    time.sleep(2)
                    self.driver.find_element(*PinLockPageLocators.PINKEY_ONE).click()
                    time.sleep(2)
                    self.report_pass('iOS APP: Entered new  pin is success')
                else:
                    self.report_fail('iOS APP: Entered new  pin is not success')
                    
                    
                if self.wait_for_element_exist(*PinLockPageLocators.PINKEY_ONE):
                    self.driver.find_element(*PinLockPageLocators.PINKEY_ONE).click()
                    time.sleep(2)
                    self.driver.find_element(*PinLockPageLocators.PINKEY_ONE).click()
                    time.sleep(2)
                    self.driver.find_element(*PinLockPageLocators.PINKEY_ONE).click()
                    time.sleep(2)
                    self.driver.find_element(*PinLockPageLocators.PINKEY_ONE).click()
                    time.sleep(2)
                    self.report_pass('iOS APP: Re Enter new pin is success')
                else:
                    self.report_fail('iOS APP: Re Enter new pin is not success')
            
            except:
                self.report_fail('IOS App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(traceback.format_exc().replace('File', '$~File'))) 

    def forgot_pin_lock(self):    
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*PinLockPageLocators.PINLOCK_FORGOTPIN):
                    self.driver.find_element(*PinLockPageLocators.PINLOCK_FORGOTPIN).click()
                    self.report_pass('iOS APP: Forgot Pin is selected Successfully')
                    time.sleep(2)
                else:
                    self.report_fail('iOS APP: Forgot Pin is not selected Successfully')    
                            
            except:
                self.report_fail('IOS App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))        
    
        
    def forgot_validate_pin(self):    
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*PinLockPageLocators.PINLOCK_LOGOUT):
                    self.driver.find_element(*PinLockPageLocators.PINLOCK_LOGOUT).click()
                    self.report_pass('iOS APP: Logout is selected Successfully')
                    time.sleep(2)
                    self.driver.find_element(*PinLockPageLocators.PINLOCK_LOGOUT_OK).click()
                else:
                    self.report_fail('iOS APP: Forgot Pin is not done Successfully')    
                            
            except:
                self.report_fail('IOS App : NoSuchElementException: in set_hot_water_schedule Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))

class TextControl(BasePage):         
      
    def navigate_to_TextControl_page(self):
        
        if self.reporter.ActionStatus:         
            try:
                strScreenName = self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name')
                print(strScreenName)
                self.driver.find_element(*HomePageLocators.MENU_BUTTON).click()
                time.sleep(2)
                
                if self.driver.find_element(*HomePageLocators.HELP_SUPPORT_LINK).is_displayed():
                    self.driver.find_element(*HomePageLocators.HELP_SUPPORT_LINK).click()
                    time.sleep(2)
                    self.driver.find_element(*HomePageLocators.TEXT_CONTROL_LINK).click()
                    strScreenName = self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name') 
                    print(strScreenName)
                    strUserCount=self.driver.find_element(*TextControlLocators.USER_TABLE).text
                    intRowCount=int(strUserCount[(len(strUserCount)-1)])-1            
                    print(intRowCount)
                else:
                    self.driver.swipe(340,571,344,100, 2000)
                    self.driver.find_element(*HomePageLocators.HELP_SUPPORT_LINK).click()
                    self.driver.find_element(*HomePageLocators.TEXT_CONTROL_LINK).click()
                    strScreenName = self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name')
                    print(strScreenName)
                if strScreenName =="Text control, screen":
                    self.report_pass("iOS APP :Successfully navigated to Text Control Page")
                else:
                    self.report.fail("iOS APP :Not able to navigate to Text Control Page")    
                
            except:
                self.report_fail('iOS App : NoSuchElementException: in navigate_to_TextControl_page\n {0}'.format(traceback.format_exc().replace('File', '$~File')))         
    
    def textControlOptions(self,context):
        print("Adding user")
        if self.reporter.ActionStatus:         
            
                strUserCount=self.driver.find_element(*TextControlLocators.USER_TABLE).text
                intRowCount=int(strUserCount[(len(strUserCount)-1)])
                print(intRowCount)
                if intRowCount<=6:
                    print(intRowCount)
                    for oRow in context.table:
                        strusername = oRow['UserName']
                        strMobileNo = oRow['MobileNo']
                        print(strusername,strMobileNo)
                        try:
                            if self.driver.find_element(*TextControlLocators.ADD_NEW_USER_LINK).is_displayed():
                                self.driver.find_element(*TextControlLocators.ADD_NEW_USER_LINK).click()
                                self.report_done("iOS App: Adding new user :   " + str(intRowCount) +"  " +"for Text Control Options")
                                self.driver.find_element(*TextControlLocators.NAME_EDTBOX).send_keys(strusername)
                                self.driver.find_element(*TextControlLocators.MOBILE_EDTBOX).send_keys(strMobileNo)
                                self.driver.find_element(*TextControlLocators.SAVE_BUTTON).click()
                                time.sleep(5)                                                       
                                try:
                                    if self.driver.find_element(*TextControlLocators.ADD_NEW_USER_LINK).is_displayed():
                                        self.report.done("iOS App:More users can be added for Text Control options")
                                        print(intRowCount)                                
                                    else:
                                        self.driver.find_element(*TextControlLocators.SAVE_BUTTON).is_displayed()
                                        self.report_fail("iOS App:This number is already registered to a Hive Account")                                           
                                except:
                                    self.report_pass("iOS App:User added to Text Control successfully")     
                                intRowCount=intRowCount+1
                      
                        except:
                            self.report_fail("iOS App:Maximum user limit reached in TextControl Options")
                else:
                    self.report_fail("iOS App:Maximum user limit reached in TextControl Options")         
                     
    
    def textControlValidation(self,context):   
        if self.reporter.ActionStatus:
            try:
                strUserCount=self.driver.find_element(*TextControlLocators.USER_TABLE).text
                intRowCount=int(strUserCount[(len(strUserCount)-1)])
                try:
                    if intRowCount==6 and self.driver.find_element(*TextControlLocators.ADD_NEW_USER_LINK).is_displayed()==False:
                        self.report_done("iOS App:More users can be added in TextControl Page")
                except:
                    intRowCount=intRowCount+1
                    self.report_done("iOS App: Adding New user"+ str(intRowCount) + "for Text Control Options")
                    self.report_pass("iOS App:Text Control Options reached Maximum user limits")
                else:
                    self.report_done("iOS App:More users can be added in TextControl Page")
            except:
                    self.report_fail('iOS App : NoSuchElementException: in textControlValidation\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
                    
class HolidayMode(BasePage):
    
    def navigate_To_HolidayScreen(self,context):       
        if self.reporter.ActionStatus:
            try: 
        
                if self.driver.find_element(*HomePageLocators.MENU_BUTTON).is_displayed():
                    strScreenName = self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name')
                    self.driver.find_element(*HomePageLocators.MENU_BUTTON).click()
                    self.driver.swipe(340,571,344,100, 2000)          
                    self.driver.find_element(*HomePageLocators.SETTINGS_MENU_LINK).click()   
                    time.sleep(2)
                    self.driver.find_element(*HomePageLocators.HOLIDAY_MODE_MENU_LINK).click()
                    strScreenName = self.driver.find_element(*HomePageLocators.CURRENT_TITLE).get_attribute('name')
                
                    if strScreenName=="Holiday mode, screen":
                        self.report_done("iOS App :User successfully navigated to Holiday Mode screen")
                    else:
                        self.report_fail("iOS App:User navigation to Holiday Mode Screen failed ")
                        self.driver.find_element(*HolidayModePageLocators.SET_DEPARTURE).click()
                        self.set_depart_hour(16)
            except:
                self.report_fail('iOS App : NoSuchElementException: in navigate_To_HolidayScreen\n {0}'.format(traceback.format_exc().replace('File', '$~File'))) 
    
    def set_Holiday_Mode(self,context,strHolidayStartDate,strHolidayStartTime,strHolidayEndDate,strHolidayEndTime,strClientType):
        if self.reporter.ActionStatus:
            try:
                if "DEFAULT" in strHolidayStartDate.upper():
                    
                    if self.wait_for_element_exist(*HolidayModePageLocators.ACTIVATE_HOLIDAYMODE_BUTTON):
                        self.driver.findelement(*HolidayModePageLocators.ACTIVATE_HOLIDAYMODE_BUTTON).click
                        
                        #Getting values for Holiday mode start Date & Time
                        strDday=self.driver.findelement(*HolidayModePageLocators.DEFAULT_DDAY).text
                        strDmonth_Year=self.driver.findelement(*HolidayModePageLocators.DEFAULT_DMONTH_YEAR).text
                        strHolidayStartDate=strDday+" "+strDmonth_Year
                        strHolidayStartTime=self.driver.findelement(*HolidayModePageLocators.DEFAULT_DTIME).text
                        
                        #Getting values for Holiday mode End Date & Time
                        strRday=self.driver.findelement(*HolidayModePageLocators.DEFAULT_RDAY).text
                        strRmonth_Year=self.driver.findelement(*HolidayModePageLocators.DEFAULT_RMONTH_YEAR).text
                        strHolidayEndDate=strRday+" "+strRmonth_Year
                        strHolidayEndTime=self.driver.findelement(*HolidayModePageLocators.DEFAULT_RTIME).text
                        
                        strTemp=self.driver.findelement(*HolidayModePageLocators.DEFAULT_TEMP).getAttribute('value')
                        if strTemp=='#':
                            strHolidayTemp='1'    
                        else:
                            strHolidayTemp=strTemp
                        return strHolidayStartDate,strHolidayStartTime,strHolidayEndDate,strHolidayEndTime,strHolidayTemp
                        
                    else:
                        self.report_fail("Ios App:Holiday Mode Activation failed")
                       
                elif "FUTURE" in strHolidayStartDate.upper():
                    
                        'Setting Return time for Holiday Mode'    
                        try:
                            modTime=(datetime.now() +timedelta(days=7,hours=1,minutes=5))
                            strStartHoliday=(modTime.strftime("%c"))
                            intDDate=(strStartHoliday.split(' ')[1]) +' '+ (strStartHoliday.split(' ')[2])
                            strDtime=(strStartHoliday.split(' ')[3])  
                            intDSetHour=(strDtime.split(':')[0]) 
                            intDSetMin=(strDtime.split(':')[1]) 
                         
                            self.driver.find_element(*HolidayModePageLocators.SET_DEPARTURE).click()
                   
                            #Setting Day in Holiday mode
                            oScrolElement = self.driver.find_element(*HolidayModePageLocators.DAY_PICKER)
                            fltCurrentValue=int(oScrolElement.get_attribute('value').split(' ')[0])
                            self.scroll_element_to_value_date(oScrolElement, fltCurrentValue, intDDate,1)
                            self.report_pass('The start time Hour is successfully set to : ' + str(intDDate))
                    
                            #Setting Hour in Holiday mode
                            oScrolElement = self.driver.find_element(*HolidayModePageLocators.HOUR_PICKER)
                            fltCurrentValue=int(oScrolElement.get_attribute('value').split(' ')[0])
                            self.scroll_element_to_value_date(oScrolElement, fltCurrentValue, intDSetHour,1)
                            self.report_pass('The start time Hour is successfully set to : ' + str(intDSetHour))
                    
                            #Setting Minutes in Holiday Mode
                            oScrolElement=self.driver.find_element(*HolidayModePageLocators.MINUTE_PICKER)
                            fltCurrentValue=int(oScrolElement.get_attribute('value').split(' ')[0])
                            self.scroll_element_to_value_date(oScrolElement, fltCurrentValue, intDSetMin,1)                         
                            self.report_pass('The start time Hour is successfully set to : ' + str(intDSetMin))
                                               
                            'Setting Return time for Holiday Mode'
                   
                            modTime1=(modTime+timedelta(days=7,hours=1,minutes=5))
                            strStopHoliday=(modTime1.strftime("%c"))
                            intRDate=(strStopHoliday.split(' ')[1]) +' '+ (strStopHoliday.split(' ')[2])
                            strRtime=(strStopHoliday.split(' ')[3])  
                            intRSetHour=(strRtime.split(':')[0]) 
                            intRSetMin=(strRtime.split(':')[1]) 
                         
                                    
                            self.driver.find_element(*HolidayModePageLocators.SET_RETURN).click()
                            #Setting Day in Holiday mode
                            oScrolElement = self.driver.find_element(*HolidayModePageLocators.DAY_PICKER)
                            fltCurrentValue=int(oScrolElement.get_attribute('value').split(' ')[0])
                            self.scroll_element_to_value_date(oScrolElement, fltCurrentValue, intRDate,1)
                            self.report_pass('The start time Hour is successfully set to : ' + str(intRDate))
                    
                            #Setting Hour in Holiday mode
                            oScrolElement = self.driver.find_element(*HolidayModePageLocators.HOUR_PICKER)
                            fltCurrentValue=int(oScrolElement.get_attribute('value').split(' ')[0])
                            self.scroll_element_to_value_date(oScrolElement, fltCurrentValue, intRSetHour,1)
                            self.report_pass('The start time Hour is successfully set to : ' + str(intRSetHour))
                    
                            #Setting Minutes in Holiday Mode
                            oScrolElement=self.driver.find_element(*HolidayModePageLocators.MINUTE_PICKER)
                            fltCurrentValue=int(oScrolElement.get_attribute('value').split(' ')[0])
                            self.scroll_element_to_value_date(oScrolElement, fltCurrentValue, intRSetMin,1)                         
                            self.report_pass('The start time Hour is successfully set to : ' + str(intRSetMin))
                    
                        except:
                            self.report_fail('iOS APP: Exception in setting Holiday Mode Time {0}'.format(traceback.format_exc().replace('File', '$~File')))
                        
                else:
                    self.report_pass("strPassDescription")
            except:
                self.report_fail('iOS APP: Exception in setting Holiday Mode Time {0}'.format(traceback.format_exc().replace('File', '$~File'))) 
               
class MotionSensor(BasePage):
     
    def navigate_to_motionsensor(self,nameMotionSensor):     
        Motion_off=str(HomePageLocators.strLOCAL_OFF)
        Motion_On=str(HomePageLocators.strLOCAL_ON)
        Motion_Offline = str(HomePageLocators.strLOCAL_OFFLINE)
               
        M_OFF1=Motion_off.replace("name", nameMotionSensor)
        M_ON1=Motion_On.replace("name", nameMotionSensor) 
        M_OFFLINE1=Motion_Offline.replace("name", nameMotionSensor)
                
        if self.reporter.ActionStatus:
            try: 
                if self.wait_for_element_exist(*HomePageLocators.FLIP_TO_HONEYCOMB):
                    self.driver.find_element(*HomePageLocators.FLIP_TO_HONEYCOMB).click()                
                
                if self.driver.is_element_present(By.XPATH,M_ON1):
                    self.driver.find_element(By.XPATH,M_ON1).click()
                    self.report_pass('IOS App : Navigated to device ' +nameMotionSensor+ ' screen')
                    time.sleep(3)
                elif ('offline' in M_OFFLINE1) & self.driver.is_element_present(By.XPATH,M_OFFLINE1):
                    print("Motion sensor is offline")
                    self.driver.find_element(By.XPATH,M_OFFLINE1).click()
                    self.report_pass('IOS App : Navigated to ' +nameMotionSensor+ ' screen where the sensor is offline')
                    time.sleep(3)                   
                    #if self.driver.is_element_present(*HomePageLocators.DEVICE_OFFLINE_LABEL):
                        #self.report_pass('IOS App : Navigated to ' +nameMotionSensor+ ' screen')
                        
                elif self.driver.is_element_present(By.XPATH,M_OFF1):
                    print("Motion is not enabled")
                    self.driver.find_element(By.XPATH,M_OFF1).click()
                    self.report_pass('IOS App : Navigated to device screen ' +nameMotionSensor+ ' screen')
                    time.sleep(3)   
                else:
                    self.report_fail('IOS App : The given device does not exist in the kit')
            except:
                self.report_fail('IOS App : NoSuchElementException: in navigate_to_motionsensor Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))   

    def navigate_to_eventlogs(self):
        if self.reporter.ActionStatus:
            try: 
                if self.driver.is_element_present(*HomePageLocators.DEVICE_OFFLINE_LABEL):
                    self.report_pass('IOS App : The motion sensor is offline. No validations possible.')
                elif self.wait_for_element_exist(*MotionSensorPageLocators.EVENTLOG_BUTTON):
                    self.driver.find_element(*MotionSensorPageLocators.EVENTLOG_BUTTON).click()
                    print("Navigated to event logs screen successfully")
                    self.report_pass('IOS App : Navigated to event logs of Motion Sensor screen')
                    time.sleep(5)
                else:
                    self.report_fail('IOS App : Navigation to event log failed')
            except:
                self.report_fail('IOS App : NoSuchElementException: in navigate_to_eventlogs Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))       
    def verify_event_logs(self):
        if self.reporter.ActionStatus:
            try:
                if self.driver.is_element_present(*HomePageLocators.DEVICE_OFFLINE_LABEL):
                    self.report_pass('IOS App : The motion sensor is offline. No validations possible.')
                else:
                    if (self.wait_for_element_exist(*MotionSensorPageLocators.NO_MOTION_LOG)):
                        print("There is no motion. Call API Validation") 
                        self.report_pass('IOS App : Verified there are no logs present in Motion Sensor screen')
                    elif (self.wait_for_element_exist(*MotionSensorPageLocators.CURRENT_MOTION_LOG)):
                        print("There is current motion. Call API Validation")
                        self.report_pass('IOS App : Verified there is current motion log present in Motion Sensor screen')
                    elif (self.wait_for_element_exist(*MotionSensorPageLocators.INTERRUPTED_MOTION_LOG)):
                        print("Multiple motions were detected for today. Call API Validation")
                        self.report_pass('IOS App : Verified there are multiple logs present in Motion Sensor screen')
                    else:
                        self.report_fail('IOS App : Unexpected logs found')
                print("The event logs are verified successfully")
                #self.report_pass('IOS App : Verified the event logs for current day in Motion Sensor screen')
                if (self.wait_for_element_exist(*MotionSensorPageLocators.CLOSE_LOG_BUTTON)):
                        self.driver.find_element(*MotionSensorPageLocators.CLOSE_LOG_BUTTON).click()                
            except:
                self.report_fail('IOS App : NoSuchElementException: in verify_event_logs Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
    
    def verify_current_status(self, nameMotionSensor):
        if self.reporter.ActionStatus:
            try: 
                if self.driver.is_element_present(*HomePageLocators.DEVICE_OFFLINE_LABEL):
                    self.report_pass('IOS App : The motion sensor is offline. No validations possible.')
                else:
                    if self.wait_for_element_exist(*MotionSensorPageLocators.MOTION_LABEL):
                        print("Motion Sensor has detected motion. Call API validation")
                        self.report_pass('IOS App : Current motion status verified as in motion')
                        time.sleep(5)
                    elif self.wait_for_element_exist(*MotionSensorPageLocators.NOMOTION_LABEL):
                        print("Motion Sensor has not detected motion. Call API validation")
                        self.report_pass('IOS App : Current motion status verified as no motion')
                        time.sleep(5)
                    else:
                        self.report_fail('IOS App : The given Motion Sensor does not exist in the kit')
            except:
                self.report_fail('IOS App : NoSuchElementException: in verify_event_logs Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))       
    
    def navigate_to_selected_day_log(self, intNumberOf):
        if self.reporter.ActionStatus:
            try: 
                if self.driver.is_element_present(*HomePageLocators.DEVICE_OFFLINE_LABEL):
                    self.report_pass('IOS App : The motion sensor is offline. No validations possible.')
                else:
                    counter = int(intNumberOf)
                    if ((counter == 6) & (self.wait_for_element_exist(*MotionSensorPageLocators.DAY1_LOG))):
                        self.driver.find_element(*MotionSensorPageLocators.DAY1_LOG).click() 
                        self.report_pass('IOS App : Navigated to event logs for given day of Motion Sensor screen')
                    elif ((counter == 5) & (self.wait_for_element_exist(*MotionSensorPageLocators.DAY2_LOG))):
                        self.driver.find_element(*MotionSensorPageLocators.DAY2_LOG).click() 
                        self.report_pass('IOS App : Navigated to event logs for given day of Motion Sensor screen')
                    elif ((counter == 4) & (self.wait_for_element_exist(*MotionSensorPageLocators.DAY3_LOG))):
                        self.driver.find_element(*MotionSensorPageLocators.DAY3_LOG).click() 
                        self.report_pass('IOS App : Navigated to event logs for given day of Motion Sensor screen')
                    elif ((counter == 3) & (self.wait_for_element_exist(*MotionSensorPageLocators.DAY4_LOG))):
                        self.driver.find_element(*MotionSensorPageLocators.DAY4_LOG).click() 
                        self.report_pass('IOS App : Navigated to event logs for given day of Motion Sensor screen')
                    elif ((counter == 2) & (self.wait_for_element_exist(*MotionSensorPageLocators.DAY5_LOG))):
                        self.driver.find_element(*MotionSensorPageLocators.DAY5_LOG).click() 
                        self.report_pass('IOS App : Navigated to event logs for given day of Motion Sensor screen')
                    elif ((counter == 1) & (self.wait_for_element_exist(*MotionSensorPageLocators.DAY6_LOG))):
                        self.driver.find_element(*MotionSensorPageLocators.DAY6_LOG).click() 
                        self.report_pass('IOS App : Navigated to event logs for given day of Motion Sensor screen')
                    else:
                        self.report_fail('IOS App : Invalid number of days')
            except:
                self.report_fail('IOS App : NoSuchElementException: in verify_event_logs Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))       
    def navigate_to_recipes(self):
        if self.reporter.ActionStatus:
            try: 
                if self.driver.is_element_present(*HomePageLocators.DEVICE_OFFLINE_LABEL):
                    self.report_pass('IOS App : The motion sensor is offline. No validations possible.')
                else:
                    if self.wait_for_element_exist(*MotionSensorPageLocators.TABBAR_RECIPES):
                        self.driver.find_element(*MotionSensorPageLocators.TABBAR_RECIPES).click()
                    if self.wait_for_element_exist(*MotionSensorPageLocators.RECIPE_SCREEN_HEADER):
                        self.report_pass('IOS App : Navigated to Recipes screen for the Sensor')
                    else:
                        self.report_fail('IOS App : Navigation to Recipes screen failed')
            except:
                self.report_fail('IOS App : NoSuchElementException: in navigate_to_recipes Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))       

    def verify_recipes(self, nameMotionSensor):
        if self.reporter.ActionStatus:
            try: 
                if self.driver.is_element_present(*HomePageLocators.DEVICE_OFFLINE_LABEL):
                    self.report_pass('IOS App : The motion sensor is offline. No validations possible.')
                else:
                    if self.driver.is_element_present(*MotionSensorPageLocators.ADD_RECIPE):
                        self.driver.find_element(*MotionSensorPageLocators.ADD_RECIPE).click()
                        if ((self.driver.is_element_present(*MotionSensorPageLocators.RECIPE_SCREEN_HEADER_NEW)) & (self.driver.is_element_present(*MotionSensorPageLocators.CANCEL_RECIPE))):
                            self.driver.find_element(*MotionSensorPageLocators.CANCEL_RECIPE).click()
                            self.report_done("Additional Recipes can be added to the sensor")
                        else:
                            self.report_done("All possible recipes has been added for the sensor")
                        LIST_OF_RECIPES=self.driver.find_elements_by_xpath("//*[contains(@label,'detects motion')]")
                        TOTAL_NUMBER_OF_RECIPES = len(LIST_OF_RECIPES)/2
                        RECIPE_DETAILS = ""
                        for counter in range(0,int(TOTAL_NUMBER_OF_RECIPES)):
                            IntY=225+counter*72
                            self.driver.tap([(150,IntY)])    
                            if(self.driver.is_element_present(*MotionSensorPageLocators.SENSOR_RECIPE)):
                                RECIPE_TEMP = self.driver.find_element(*MotionSensorPageLocators.SENSOR_RECIPE).get_attribute('label')
                                RECIPE_DETAILS+=RECIPE_TEMP
                                RECIPE_DETAILS+="\n"
                            if(self.driver.is_element_present(*MotionSensorPageLocators.CANCEL_RECIPE)):
                                self.driver.find_element(*MotionSensorPageLocators.CANCEL_RECIPE).click()
                        self.report_pass('IOS App : The following recipes has been set for the sensor: \n'+RECIPE_DETAILS+'')
                    else:
                        self.report_fail("Recipes screens validation not completed")

            except:
                self.report_fail('IOS App : NoSuchElementException: in navigate_to_recipes Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))       
                self.report_fail('IOS App : NoSuchElementException: in verify_recipes Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))       

class DeviceRecipes(BasePage):
    MS_AVAILABLE = 1
    CS_AVAILABLE = 1
    PLUG_AVAILABLE = 1
    BULB_AVAILABLE = 1 
    SET_RECIPE_TRIGERRED = 0
    
    def swipe_control(self, TypeOf):
        if self.reporter.ActionStatus:
            try: 
                oScrolElement = self.driver.find_element(*RecipeScreenLocators.NOTIFICATION_PICKER)
                intLeftX = oScrolElement.location['x']
                intUpperY = oScrolElement.location['y']
                intWidth = oScrolElement.size['width']
                intHieght = oScrolElement.size['height']                    
                intStX = intLeftX + intWidth/2
                intStY = intUpperY +(intHieght/4)
                intEndX = intStX
                intEndY = intUpperY + (intHieght/8)
                intEndRY = intEndY+15
                intStRY = intStY+15
                
                self.driver.swipe(intStX, intEndRY, intEndX, intStRY)
                self.driver.swipe(intStX, intEndRY, intEndX, intStRY)
                if (("Push" in TypeOf) & ("Email" not in TypeOf)):
                    self.report_done('Push notification is set') 
                elif (("Push" in TypeOf) & ("Email" in TypeOf)):
                    self.driver.swipe(intStX, intStY, intEndX, intEndY)
                    self.report_done('Push & Email notification is set')
                elif (("Push" not in TypeOf) & ("Email" in TypeOf)):
                    self.driver.swipe(intStX, intStY, intEndX, intEndY)
                    self.driver.swipe(intStX, intStY, intEndX, intEndY)
                    self.report_done('Email notification is set')                                                    
            except:
                self.report_fail('IOS App : NoSuchElementException: in navigate_to_device Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))   
    
    def navigate_to_device(self,nameDevice,typeDevice):
        print('Device to navigate :', nameDevice)
        Device_off=str(HomePageLocators.strLOCAL_OFF)
        Device_On=str(HomePageLocators.strLOCAL_ON)
        Device_Offline = str(HomePageLocators.strLOCAL_OFFLINE)
               
        D_OFF1=Device_off.replace("name", nameDevice)
        D_ON1=Device_On.replace("name", nameDevice) 
        D_OFFLINE1=Device_Offline.replace("name", nameDevice)

        if self.reporter.ActionStatus:
            try: 
                if self.driver.is_element_present(*HomePageLocators.FLIP_TO_HONEYCOMB):
                    self.driver.find_element(*HomePageLocators.FLIP_TO_HONEYCOMB).click()                
                if self.driver.is_element_present(By.XPATH,D_ON1):
                    self.driver.find_element(By.XPATH,D_ON1).click()
                    self.report_pass('IOS App : ' +nameDevice+ ' is paired with the hub as expected')
                    time.sleep(3)
                elif ('offline' in D_OFFLINE1) & self.driver.is_element_present(By.XPATH,D_OFFLINE1):
                    self.driver.find_element(By.XPATH,D_OFFLINE1).click()
                    self.report_pass('IOS App : ' +nameDevice+ ' is paired with the hub and is offline')
                    time.sleep(3)                   
                elif self.driver.is_element_present(By.XPATH,D_OFF1):
                    self.driver.find_element(By.XPATH,D_OFF1).click()
                    self.report_pass('IOS App : ' +nameDevice+ ' is paired with the hub as expected')
                    time.sleep(3)   
                else:
                    self.report_fail('IOS App : The given device is not paired with the hub')
                    if ('MS' in typeDevice):
                        DeviceRecipes.MS_AVAILABLE = 0
                    elif ('CS' in typeDevice):
                        DeviceRecipes.CS_AVAILABLE = 0
                    elif ('Plug' in typeDevice):
                        DeviceRecipes.PLUG_AVAILABLE = 0
                    elif ('Bulb' in typeDevice):
                        DeviceRecipes.BULB_AVAILABLE = 0

            except:
                self.report_fail('IOS App : NoSuchElementException: in navigate_to_device Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))   

    def navigate_to_allrecipes(self):
        if self.reporter.ActionStatus:
            try: 
                if self.driver.is_element_present(*HomePageLocators.MENU_BUTTON):
                    self.driver.find_element(*HomePageLocators.MENU_BUTTON).click()
                    if self.driver.is_element_present(*HomePageLocators.ALL_RECIPES):
                        self.driver.find_element(*HomePageLocators.ALL_RECIPES).click()
                        if self.driver.is_element_present(*RecipeScreenLocators.RECIPE_SCREEN_HEADER):
                            self.report_pass('IOS App : Navigated to All Recipes screen successfully')
                        else:
                            self.report_fail('IOS App : All Recipes header is not as expected')
                    else:
                        self.report_fail('IOS App : All Recipes option is not displayed')
                else:
                    self.report_fail('IOS App : Menu button is not displayed')                
            except:
                self.report_fail('IOS App : NoSuchElementException: in navigate_to_device Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))   
            
     
    def remove_existing_recipes(self):
        if self.reporter.ActionStatus:
            try: 
                if self.driver.is_element_present(*RecipeScreenLocators.ADD_RECIPE):
                    COUNT_OF_RECIPES = 100
                    while (COUNT_OF_RECIPES !=0):
                        MS_DISPLAYED = self.driver.find_elements(*RecipeScreenLocators.MS_RECIPE)
                        CSO_DISPLAYED = self.driver.find_elements(*RecipeScreenLocators.CSO_RECIPE)
                        CSC_DISPLAYED = self.driver.find_elements(*RecipeScreenLocators.CSC_RECIPE)
                        COUNT_OF_RECIPES = len(MS_DISPLAYED) + len(CSO_DISPLAYED) + len (CSC_DISPLAYED)
                        print(COUNT_OF_RECIPES)
                        self.driver.tap([(150,225)])
                        if (self.driver.is_element_present(*RecipeScreenLocators.REMOVE_RECIPE)):
                            if self.driver.is_element_present(*RecipeScreenLocators.MS_RECIPE):
                                CURRENT_RECIPE = self.driver.find_element(*RecipeScreenLocators.MS_RECIPE).get_attribute('label')
                            if self.driver.is_element_present(*RecipeScreenLocators.CSO_RECIPE):
                                CURRENT_RECIPE = self.driver.find_element(*RecipeScreenLocators.CSO_RECIPE).get_attribute('label')
                            if self.driver.is_element_present(*RecipeScreenLocators.CSC_RECIPE):
                                CURRENT_RECIPE = self.driver.find_element(*RecipeScreenLocators.CSC_RECIPE).get_attribute('label')
                            self.driver.find_element(*RecipeScreenLocators.REMOVE_RECIPE).click()
                            self.report_done('Remove Recipe clicked')
                            if (self.driver.is_element_present(*RecipeScreenLocators.REMOVE_POPUP)):
                                self.driver.find_element(*RecipeScreenLocators.REMOVE_POPUP).click()
                                self.report_done('Remove in pop up clicked')
                                if self.driver.is_element_present(*RecipeScreenLocators.RECIPE_SCREEN_HEADER):
                                    self.report_done('Recipe : ' +CURRENT_RECIPE+' has been removed successfully')
                                else:
                                    self.report_done('Issue in removing recipe')
                            else:
                                self.report_done('Issue in remove recipe pop up')
                        else:
                            continue
                                                
                    if self.driver.is_element_present(*RecipeScreenLocators.ADD_RECIPE):
                        self.driver.find_element(*RecipeScreenLocators.ADD_RECIPE).click()
                        if ((self.driver.is_element_present(*RecipeScreenLocators.ADD_A_NEW_RECIPE)) & (self.driver.is_element_present(*RecipeScreenLocators.CANCEL_BUTTON))):
                            self.driver.find_element(*MotionSensorPageLocators.CANCEL_RECIPE).click()
                            self.report_pass('IOS App : All recipes set for the user has been removed')
                else:
                    self.report_fail('IOS App : All recipes set for the user was not removed')
            except:
                self.report_fail('IOS App : NoSuchElementException: in remove_existing_recipes Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))   
          

    def verify_recipe_template(self):
        if self.reporter.ActionStatus:
            try: 
                if self.driver.is_element_present(*HomePageLocators.FLIP_TO_HONEYCOMB):
                    self.driver.find_element(*HomePageLocators.FLIP_TO_HONEYCOMB).click()
                if self.driver.is_element_present(*HomePageLocators.MENU_BUTTON):
                    self.driver.find_element(*HomePageLocators.MENU_BUTTON).click()
                    if self.driver.is_element_present(*HomePageLocators.ALL_RECIPES):
                        self.driver.find_element(*HomePageLocators.ALL_RECIPES).click()
                        if self.driver.is_element_present(*RecipeScreenLocators.RECIPE_SCREEN_HEADER):
                            if self.driver.is_element_present(*RecipeScreenLocators.ADD_RECIPE):
                                self.driver.find_element(*RecipeScreenLocators.ADD_RECIPE).click()
                                if ((self.driver.is_element_present(*RecipeScreenLocators.ADD_A_NEW_RECIPE)) & (self.driver.is_element_present(*RecipeScreenLocators.CANCEL_BUTTON))):
                                    self.report_pass('IOS App : Navigated to recipe template screen successfully')
                                    if (DeviceRecipes.MS_AVAILABLE != 0):
                                        MS_RECIPES=self.driver.find_elements_by_xpath("//*[contains(@label,'detects motion')]")
                                        if (len(MS_RECIPES) == 1 & DeviceRecipes.PLUG_AVAILABLE == 0 & DeviceRecipes.BULB_AVAILABLE == 0):
                                            self.report_pass('IOS App : As Plug and Bulb are not paired to the Hub, we have only notification recipe for the motion sensor')
                                        elif(len(MS_RECIPES) == 2):
                                            if (DeviceRecipes.PLUG_AVAILABLE == 0):
                                                self.report_pass('IOS App : As Plug is not paired to the Hub, we have multiple recipes for the motion sensor.')
                                            else:
                                                self.report_pass('IOS App : As Bulb is not paired to the Hub, we have multiple recipes for the motion sensor.')
                                        elif(len(MS_RECIPES) == 3):
                                            self.report_pass('IOS App : All applicable recipes for the motion sensor are displayed as expected.')
                                        else:
                                            self.report_fail('IOS App : The recipe template for motion sensor is incorrect.')
                                    if (DeviceRecipes.CS_AVAILABLE !=0):    
                                        CSO_RECIPES=self.driver.find_elements_by_xpath("//*[contains(@label,'is opened')]")
                                        CSC_RECIPES=self.driver.find_elements_by_xpath("//*[contains(@label,'is closed')]")
                                        if (len(CSO_RECIPES) == len (CSC_RECIPES)):
                                            if (len(CSO_RECIPES) == 1 & DeviceRecipes.PLUG_AVAILABLE == 0 & DeviceRecipes.BULB_AVAILABLE == 0):
                                                self.report_pass('IOS App : As Plug and Bulb are not paired to the Hub, we have only notification recipe for the contact sensor.')
                                            elif(len(CSO_RECIPES) == 2):
                                                if (DeviceRecipes.PLUG_AVAILABLE == 0):
                                                    self.report_pass('IOS App : As Plug is not paired to the Hub, we have multiple recipes for the contact sensor.')
                                                else:
                                                    self.report_pass('IOS App : As Bulb is not paired to the Hub, we have multiple recipes for the contact sensor.')
                                            elif(len(CSO_RECIPES) == 3):
                                                self.report_pass('IOS App : All applicable recipes for the contact sensor are displayed as expected.')
                                            else:
                                                self.report_fail('IOS App : The recipe template for contact sensor is incorrect.')
                                        else:
                                            self.report_fail('IOS App : The recipe template for contact sensor is incorrect.')
                            if ((self.driver.is_element_present(*RecipeScreenLocators.ADD_A_NEW_RECIPE)) & (self.driver.is_element_present(*RecipeScreenLocators.CANCEL_BUTTON))):
                                self.driver.find_element(*MotionSensorPageLocators.CANCEL_RECIPE).click()

                                    
            except:
                self.report_fail('IOS App : NoSuchElementException: in remove_existing_recipes Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))   
  
    def set_sensor_recipe(self, recipe_exists, TypeOf,Sensor, SensorState):   
        if self.reporter.ActionStatus:
            try:
                if recipe_exists == 1:
                    self.report_pass(""+TypeOf+" notification recipe already exists when "+Sensor+" "+SensorState+"")
                else:
                    if (recipe_exists == 2):
                        self.report_pass("Edit existing recipe fas "+TypeOf+" notification recipe when "+Sensor+" "+SensorState+"")
                    else:
                        self.report_pass("Create recipe as "+TypeOf+" notification recipe when "+Sensor+" "+SensorState+"")
                    DeviceRecipes.create_new_recipe(self, recipe_exists, TypeOf, Sensor, SensorState)
                    DeviceRecipes.SET_RECIPE_TRIGERRED = 1
            except:
                self.report_fail('IOS App : NoSuchElementException: in set_sensor_recipe Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))   

    def report_recipe_exists(self, recipe_exists, TypeOf, Sensor, SensorState):   
        if self.reporter.ActionStatus:
            try:
                if recipe_exists == 1:
                    self.report_pass(""+TypeOf+" notification recipe displayed in device recipe screen for "+Sensor+" when "+SensorState+"")
                else:
                    self.report_fail(""+TypeOf+" notification recipe was not displayed in device recipe screen for "+Sensor+" when "+SensorState+"")
            except:
                self.report_fail('IOS App : NoSuchElementException: in set_sensor_recipe Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))   

    def create_new_recipe(self, recipe_exists, TypeOf, Sensor, SensorState):
        if self.reporter.ActionStatus:
            try:
                if self.driver.is_element_present(*HomePageLocators.FLIP_TO_HONEYCOMB):
                    self.driver.find_element(*HomePageLocators.FLIP_TO_HONEYCOMB).click()
                if self.driver.is_element_present(*HomePageLocators.MENU_BUTTON):
                    self.driver.find_element(*HomePageLocators.MENU_BUTTON).click()
                    if self.driver.is_element_present(*HomePageLocators.ALL_RECIPES):
                        self.driver.find_element(*HomePageLocators.ALL_RECIPES).click()
                        if self.driver.is_element_present(*RecipeScreenLocators.RECIPE_SCREEN_HEADER):
                            if (recipe_exists == 2):
                                print('Navigate to existing Recipe')
                                MS_RECIPES=self.driver.find_elements_by_xpath("//*[contains(@label,'detects motion')]")
                                CSO_RECIPES=self.driver.find_elements_by_xpath("//*[contains(@label,'is opened')]")
                                CSC_RECIPES=self.driver.find_elements_by_xpath("//*[contains(@label,'is closed')]")
                                
                                TOTAL_NUMBER_OF_RECIPES = (len(MS_RECIPES) + len(CSO_RECIPES) + len(CSC_RECIPES))/2
                                for counter in range(0,int(TOTAL_NUMBER_OF_RECIPES)):
                                    IntY=225+counter*72
                                    self.driver.tap([(150,IntY)])    
                                    if(self.driver.is_element_present(*RecipeScreenLocators.THEN_EXIST)):
                                        if (self.driver.is_element_present(*RecipeScreenLocators.MS_RECIPE)):
                                            EXISTING_RECIPE = self.driver.find_element(*RecipeScreenLocators.MS_RECIPE).get_attribute('label')
                                        elif (self.driver.is_element_present(*RecipeScreenLocators.CSO_RECIPE)):
                                            EXISTING_RECIPE = self.driver.find_element(*RecipeScreenLocators.CSO_RECIPE).get_attribute('label')
                                        elif (self.driver.is_element_present(*RecipeScreenLocators.CSC_RECIPE)):
                                            EXISTING_RECIPE = self.driver.find_element(*RecipeScreenLocators.CSC_RECIPE).get_attribute('label')
                                        if ((Sensor in EXISTING_RECIPE) & (SensorState in EXISTING_RECIPE)):
                                            break
                                        else:
                                            if(self.driver.is_element_present(*RecipeScreenLocators.CANCEL_BUTTON)):
                                                self.driver.find_element(*RecipeScreenLocators.CANCEL_BUTTON).click()
                            else:
                                if self.driver.is_element_present(*RecipeScreenLocators.ADD_RECIPE):
                                    self.driver.find_element(*RecipeScreenLocators.ADD_RECIPE).click()
                                    if ((self.driver.is_element_present(*RecipeScreenLocators.CANCEL_BUTTON))):
                                        if ('detects motion' in SensorState):
                                            self.driver.find_element(*RecipeScreenLocators.MS_NOT_RECIPE).click()
                                        elif ('opened' in SensorState):
                                            self.driver.find_element(*RecipeScreenLocators.CSO_NOT_RECIPE).click()
                                        elif ('closed' in SensorState):
                                            self.driver.find_element(*RecipeScreenLocators.CSC_NOT_RECIPE).click()
                                        else:
                                            self.report_fail('IOS App : Navigation to Sensor recipe screen failed')
                                    else:
                                        self.report_fail('IOS App : Navigation to Recipe template failed')
                                else:
                                    self.report_fail('IOS App : Add a new recipe failed')
                            if(self.driver.is_element_present(*RecipeScreenLocators.THEN_EXIST)):
                                self.driver.find_element(*RecipeScreenLocators.THEN_EXIST).click()   
                            else:
                                self.report_fail('IOS App : Navigation to Then screen failed') 
                            DeviceRecipes.swipe_control(self, TypeOf)                                        
                            if (self.driver.is_element_present(*RecipeScreenLocators.THEN_DONE)):
                                self.driver.find_element(*RecipeScreenLocators.THEN_DONE).click()
                                if(self.driver.is_element_present(*RecipeScreenLocators.SAVE_BUTTON)):
                                    self.driver.find_element(*RecipeScreenLocators.SAVE_BUTTON).click()
                                    self.report_pass('IOS App : Recipe Saved successfully')                            
                                else:
                                    self.report_fail('IOS App : Recipe save failed')
                            else:
                                self.report_fail('IOS App : Setting Then failed')      
                                
                        else:
                            self.report_fail('IOS App : Recipe screen failed')
                        
                        

            except:
                self.report_fail('IOS App : NoSuchElementException: in create_new_recipe Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))   
                

    def verify_notification_recipe_exists(self, Sensor, TypeOf, SensorState):
        if self.reporter.ActionStatus:
            try: 
                if self.driver.is_element_present(*HomePageLocators.DEVICE_OFFLINE_LABEL):
                    self.report_pass('IOS App : The sensor is offline. No validations possible.')
                else:
                    if self.driver.is_element_present(*MotionSensorPageLocators.ADD_RECIPE):
                        LIST_OF_RECIPES=self.driver.find_elements_by_xpath("//*[contains(@label,'Notify me')]")
                        TOTAL_NUMBER_OF_RECIPES = len(LIST_OF_RECIPES)/2
                        if (TOTAL_NUMBER_OF_RECIPES == 0):
                            return 100
                        else:
                            for counter in range(0,int(TOTAL_NUMBER_OF_RECIPES)):
                                IntY=225+counter*72
                                self.driver.tap([(150,IntY)])    
                                if(self.driver.is_element_present(*RecipeScreenLocators.THEN_EXIST)):
                                    if (self.driver.is_element_present(*RecipeScreenLocators.MS_RECIPE)):
                                        EXISTING_RECIPE = self.driver.find_element(*RecipeScreenLocators.MS_RECIPE).get_attribute('label')
                                    elif (self.driver.is_element_present(*RecipeScreenLocators.CSO_RECIPE)):
                                        EXISTING_RECIPE = self.driver.find_element(*RecipeScreenLocators.CSO_RECIPE).get_attribute('label')
                                    elif (self.driver.is_element_present(*RecipeScreenLocators.CSC_RECIPE)):
                                        EXISTING_RECIPE = self.driver.find_element(*RecipeScreenLocators.CSC_RECIPE).get_attribute('label')
                                    EXISTING_NOTIFICATION = self.driver.find_element(*RecipeScreenLocators.THEN_EXIST).get_attribute('label')
                                    if(self.driver.is_element_present(*RecipeScreenLocators.CANCEL_BUTTON)):
                                        self.driver.find_element(*RecipeScreenLocators.CANCEL_BUTTON).click()
                                    if ((Sensor in EXISTING_RECIPE) & (SensorState in EXISTING_RECIPE)):
                                        RECIPE_EXISTS = 2
                                        if (("Push" in TypeOf) & ("Email" not in TypeOf) & ("Push" in EXISTING_NOTIFICATION)):
                                            RECIPE_EXISTS = 1
                                        elif (("Push" in TypeOf) & ("Email" in TypeOf) & ("Push" in EXISTING_NOTIFICATION) & ("Email" in EXISTING_NOTIFICATION) ):
                                            RECIPE_EXISTS = 1
                                        elif (("Push" not in TypeOf) & ("Email" in TypeOf) & ("Email" in EXISTING_NOTIFICATION)):
                                            RECIPE_EXISTS = 1
                                        break
                                    else:
                                        RECIPE_EXISTS = 0
                            return RECIPE_EXISTS

                    else:
                        self.report_fail("Recipes screens validation not completed")

            except:
                self.report_fail('IOS App : NoSuchElementException: in verify_notification_recipe_exists Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))      
                
class ContactSensors(BasePage):
    
    def navigate_to_contact_sensor(self,nameContactSensor):
        print('Contact sensor :', nameContactSensor)
        
        Motion_off=str(HomePageLocators.strLOCAL_OFF)
        Motion_On=str(HomePageLocators.strLOCAL_ON)
        Motion_Offline = str(HomePageLocators.strLOCAL_OFFLINE)
       
        M_OFF1=Motion_off.replace("name", nameContactSensor)
        M_ON1=Motion_On.replace("name", nameContactSensor) 
        M_OFFLINE1=Motion_Offline.replace("name", nameContactSensor)

        if self.reporter.ActionStatus:
            try: 
                if self.wait_for_element_exist(*HomePageLocators.FLIP_TO_HONEYCOMB):
                    self.driver.find_element(*HomePageLocators.FLIP_TO_HONEYCOMB).click()
                    time.sleep(1)
                    if self.driver.find_element(By.XPATH,M_ON1):
                        self.driver.find_element(By.XPATH,M_ON1).click()
                        self.report_pass('Hive user navigated to ' +nameContactSensor+ ' screen successfully')
                        time.sleep(2)
                    elif self.driver.find_element(By.XPATH,M_OFF1):
                        self.driver.find_element(By.XPATH,M_OFF1).click()
                        self.report_pass('Hive user navigated to ' +nameContactSensor+ ' screen successfully')
                        time.sleep(2)
                                  
                elif  self.wait_for_element_exist(*HomePageLocators.FLIP_TO_DEVICE_LIST): 
                    if self.driver.is_element_present(By.XPATH,M_ON1): 
                        self.driver.find_element(By.XPATH,M_ON1).click()
                        self.report_pass('Hive user navigated to ' +nameContactSensor+ ' screen successfully')
                        time.sleep(2)
                    elif self.driver.find_element(By.XPATH,M_OFF1):
                        self.driver.find_element(By.XPATH,M_OFF1).click()
                        time.sleep(2)
                        self.report_pass('Hive user navigated to ' +nameContactSensor+ ' screen successfully')
                   
                else:
                    self.report_fail('IOS App : The given Contact Sensor does not exist in the kit')
            except:
                self.report_fail('IOS App : NoSuchElementException: in navigate_to_contact_sensor Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
    '''
    def navigate_to_contact_sensor(self, nameContactSensor):
        
        Motion_off=str(HomePageLocators.strLOCAL_OFF)
        Motion_On=str(HomePageLocators.strLOCAL_ON)
        Motion_Offline = str(HomePageLocators.strLOCAL_OFFLINE)
       
        M_OFF1=Motion_off.replace("name", nameContactSensor)
        M_ON1=Motion_On.replace("name", nameContactSensor) 
        M_OFFLINE1=Motion_Offline.replace("name", nameContactSensor)

        if self.reporter.ActionStatus:
            try: 
                if self.wait_for_element_exist(*HomePageLocators.PAGE_NAVIGATOR):
                    if self.driver.is_element_present(By.XPATH,M_ON1):
                        self.driver.find_element(By.XPATH,M_ON1).click()
                        self.report_pass('IOS App : Navigated to ' +nameContactSensor+ ' screen')
                    elif  self.is_element_present(By.XPATH,M_OFF1):
                        self.driver.find_element(By.XPATH,M_OFF1).click()
                        self.report_pass('IOS App : Navigated to ' +nameContactSensor+ ' screen')
                    elif self.is_element_present(By.XPATH,M_OFFLINE1):
                        self.report_fail('IOS App : Given device ' +nameContactSensor+ ' is offline')
                    
                    elif self.wait_for_element_exist(*HomePageLocators.PAGE_NAVIGATOR):
                        self.driver.find_element(*HomePageLocators.PAGE_NAVIGATOR).click()
                        if self.is_element_present(By.XPATH,M_ON1):
                            self.driver.find_element(By.XPATH,M_ON1).click()
                            self.report_pass('IOS App : Navigated to ' +nameContactSensor+ ' screen')
                        elif self.is_element_present(By.XPATH,M_OFF1):
                            self.driver.find_element(By.XPATH,M_OFF1).click()
                            self.report_pass('IOS App : Navigated to ' +nameContactSensor+ ' screen')
                        elif self.is_element_present(By.XPATH,M_OFFLINE1):
                            self.report_fail('IOS App : Given device ' +nameContactSensor+ ' is offline')
                        
                    elif not self.driver.wait_for_element_exist(*HomePageLocators.PAGE_NAVIGATOR):
                        self.wait_for_element_exist(*HomePageLocators.FLIP_TO_HONEYCOMB)
                        self.report_pass('IOS App : Hive user is at Dash board List view screen')
                        self.driver.find_element(*HomePageLocators.FLIP_TO_HONEYCOMB).click()
                        self.report_pass('IOS App : Hive user is at Dash board screen')
                        
                        if self.driver.is_element_present(By.XPATH,M_ON1):
                         self.driver.find_element(By.XPATH,M_ON1).click()
                        self.report_pass('IOS App : Navigated to ' +nameContactSensor+ ' screen')
                    elif  self.is_element_present(By.XPATH,M_OFF1):
                        self.driver.find_element(By.XPATH,M_OFF1).click()
                        self.report_pass('IOS App : Navigated to ' +nameContactSensor+ ' screen')
                    elif self.is_element_present(By.XPATH,M_OFFLINE1):
                        self.report_fail('IOS App : Given device ' +nameContactSensor+ ' is offline')
                    
                    elif self.wait_for_element_exist(*HomePageLocators.PAGE_NAVIGATOR):
                        self.driver.find_element(*HomePageLocators.PAGE_NAVIGATOR).click()
                        if self.is_element_present(By.XPATH,M_ON1):
                            self.driver.find_element(By.XPATH,M_ON1).click()
                            self.report_pass('IOS App : Navigated to ' +nameContactSensor+ ' screen')
                        elif self.is_element_present(By.XPATH,M_OFF1):
                            self.driver.find_element(By.XPATH,M_OFF1).click()
                            self.report_pass('IOS App : Navigated to ' +nameContactSensor+ ' screen')
                        elif self.is_element_present(By.XPATH,M_OFFLINE1):
                            self.report_fail('IOS App : Given device ' +nameContactSensor+ ' is offline')
            
                else:
                    self.report_fail('IOS App : The given Contact Sensor does not exist in the kit')
            except:
                self.report_fail('IOS App : NoSuchElementException: in navigate_to_contact_sensor Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
    '''

    def contactSensorCurrentStatus(self,nameContactSensor):
        if self.reporter.ActionStatus:
            try:
                if self.wait_for_element_exist(*ContactSensorLocators.CS_STATUS_OPEN):
                    currentStatus = self.driver.find_element(*ContactSensorLocators.CS_STATUS_OPEN).get_attribute('value')
                    print(currentStatus)
                    self.report_pass('iOS APP: Captured the current status of device successfully')
                else: 
                    currentStatus = self.driver.find_element(*ContactSensorLocators.CS_STATUS_CLOSED).get_attribute('value')
                    print(currentStatus)
                    self.report_pass('iOS APP: Captured the current status of device successfully')
                    return currentStatus
                                    
            except:
                self.report_fail('IOS App : NoSuchElementException: in contactSensorCurrentStatus Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
                
    def todaysLog(self):
        if self.reporter.ActionStatus:
            try:
                if self.driver.is_element_present(*HomePageLocators.DEVICE_OFFLINE_LABEL):
                    self.report_pass('IOS App : The Contact sensor is offline. No validations possible.')
                elif self.wait_for_element_exist(*ContactSensorLocators.LOGS):
                    self.driver.find_element(*ContactSensorLocators.LOGS).click()
                    self.report_pass('iOS APP: Hive user is able to see the Todays log screen')
                    time.sleep(3)
                else:
                    self.report_fail('iOS APP: Hive user is not able to see the Todays log screen')
            except:
                self.report_fail('IOS App : NoSuchElementException: in todaysLog Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
    
    def navigate_to_selected_weekday_log(self, selectWeekDay):
        if self.reporter.ActionStatus:
            try: 
                if self.driver.is_element_present(*HomePageLocators.DEVICE_OFFLINE_LABEL):
                    self.report_pass('IOS App : The Contact sensor is offline. No validations possible.')
                else:
                    counter = int(selectWeekDay)
                    if ((counter == 6) & (self.wait_for_element_exist(*MotionSensorPageLocators.DAY1_LOG))):
                        self.driver.find_element(*MotionSensorPageLocators.DAY1_LOG).click()
                        time.sleep(1)  
                        self.report_pass('IOS App : Navigated to event logs for given day of Contact Sensor screen')
                    elif ((counter == 5) & (self.wait_for_element_exist(*MotionSensorPageLocators.DAY2_LOG))):
                        self.driver.find_element(*MotionSensorPageLocators.DAY2_LOG).click()
                        time.sleep(1)  
                        self.report_pass('IOS App : Navigated to event logs for given day of Contact Sensor screen')
                    elif ((counter == 4) & (self.wait_for_element_exist(*MotionSensorPageLocators.DAY3_LOG))):
                        self.driver.find_element(*MotionSensorPageLocators.DAY3_LOG).click() 
                        time.sleep(1) 
                        self.report_pass('IOS App : Navigated to event logs for given day of Contact Sensor screen')
                    elif ((counter == 3) & (self.wait_for_element_exist(*MotionSensorPageLocators.DAY4_LOG))):
                        self.driver.find_element(*MotionSensorPageLocators.DAY4_LOG).click()
                        time.sleep(1) 
                        self.report_pass('IOS App : Navigated to event logs for given day of Contact Sensor screen')
                    elif ((counter == 2) & (self.wait_for_element_exist(*MotionSensorPageLocators.DAY5_LOG))):
                        self.driver.find_element(*MotionSensorPageLocators.DAY5_LOG).click()
                        time.sleep(1)  
                        self.report_pass('IOS App : Navigated to event logs for given day of Contact Sensor screen')
                    elif ((counter == 1) & (self.wait_for_element_exist(*MotionSensorPageLocators.DAY6_LOG))):
                        self.driver.find_element(*MotionSensorPageLocators.DAY6_LOG).click() 
                        time.sleep(1) 
                        self.report_pass('IOS App : Navigated to event logs for given day of Contact Sensor screen')
                    else:
                        self.report_fail('IOS App : Invalid number of days')
            except:
                self.report_fail('IOS App : NoSuchElementException: in verify_event_logs Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))                   


    def verify_todayevent_logs(self):
        if self.reporter.ActionStatus:
            try:
                if self.driver.is_element_present(*HomePageLocators.DEVICE_OFFLINE_LABEL):
                    self.report_pass('IOS App : The contact sensor is offline. No validations possible.')
                else:
                    if (self.wait_for_element_exist(*ContactSensorLocators.OPEN_ALL_DAY)):
                        self.report_pass('IOS App : Verified that contact sensor opened all day')
                    elif (self.wait_for_element_exist(*ContactSensorLocators.OPEN_CURRENT_LOG)):

                        self.report_pass('IOS App : Verified that contact sensor is opened now')
                    elif (self.wait_for_element_exist(*ContactSensorLocators.OPEN_MUTLIPE_LOG)):
                     
                        self.report_pass('IOS App : Verified that contact sensor is open multiple times')
                    else:
                        self.report_fail('IOS App : Unexpected logs found')
                        
                if (self.wait_for_element_exist(*MotionSensorPageLocators.CLOSE_LOG_BUTTON)):
                        self.driver.find_element(*MotionSensorPageLocators.CLOSE_LOG_BUTTON).click()                
            except:
                self.report_fail('IOS App : NoSuchElementException: in verify_event_logs Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
                

class ColourLights(BasePage):
    SETTINGS_LOCAL = ""
    VALUE_LOCAL = ""
    SWITCH_ON = 0

    def setValues(self,Settings,Value):
        ColourLights.SETTINGS_LOCAL = Settings
        ColourLights.VALUE_LOCAL = Value

    def navigateToSettings(self,Settings):
        if self.reporter.ActionStatus:
            try:
                BULB_STATUS = self.driver.find_element(*BulbScreenLocators.BULB).get_attribute('value')
                if ("off" in BULB_STATUS):
                    self.driver.tap([(158,236)]) 
                    ColourLights.SWITCH_ON = 1
                if ("tone" in Settings):
                    if (self.driver.is_element_present(*BulbScreenLocators.COLOUR_BUTTON)):
                        self.driver.find_element(*BulbScreenLocators.COLOUR_BUTTON).click()
                    if (self.driver.is_element_present(*BulbScreenLocators.TONE_BUTTON)):
                        self.driver.find_element(*BulbScreenLocators.TONE_BUTTON).click()                  
                    else:
                        print("")
                elif ("brightness" in Settings):
                    if (self.driver.is_element_present(*BulbScreenLocators.DIMMER_BUTTON)):
                        self.driver.find_element(*BulbScreenLocators.DIMMER_BUTTON).click()
                    else:
                        print("")
                elif ("colour" in Settings):
                    if (self.driver.is_element_present(*BulbScreenLocators.TONE_BUTTON)):
                        self.driver.find_element(*BulbScreenLocators.TONE_BUTTON).click()
                    if (self.driver.is_element_present(*BulbScreenLocators.COLOUR_BUTTON)):
                        self.driver.find_element(*BulbScreenLocators.COLOUR_BUTTON).click()
                    else:
                        print("")
            except:
                self.report_fail('IOS App : NoSuchElementException: in navigateToSettings Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))      

        

    def setValueForBulb(self,Settings,verifyValue): 
        if self.reporter.ActionStatus:
            try:
                angleStep = 0
                if ("tone" in Settings):
                    if (self.driver.is_element_present(*BulbScreenLocators.BULB_TONE)):
                        oBulb = self.driver.find_element(*BulbScreenLocators.BULB_TONE)
                        angleStep = 20
                    else:
                        self.report_step('IOS App : Tone settings was not displayed')
                elif ("brightness" in Settings):
                    if (self.driver.is_element_present(*BulbScreenLocators.BULB_BRIGHTNESS)):
                        oBulb = self.driver.find_element(*BulbScreenLocators.BULB_BRIGHTNESS)
                        angleStep = 10
                    else:
                        self.report_step('IOS App : Brightness settings was not displayed')
                elif ("colour" in Settings):
                    if (self.driver.is_element_present(*BulbScreenLocators.BULB_COLOUR)):
                        oBulb = self.driver.find_element(*BulbScreenLocators.BULB_COLOUR)
                        angleStep = 10
                    else:
                        self.report_step('IOS App : Colour settings was not displayed')
                             
                intLeftX = oBulb.location['x']
                intUpperY = oBulb.location['y']
                intSide = oBulb.size['width']
                intSideT = (intSide / 2)
                intCenterX = intLeftX + intSideT
                intCenterY = intUpperY + intSideT      
                intRadius = intCenterX - 32
                intTempStartX = intCenterX + intRadius* math.cos (180)
                intTempStartY = intCenterY + intRadius* math.sin (180)

                for angle in range (165,375,angleStep):
                    intTempNewStartX = intCenterX + intRadius* math.cos (angle * math.pi / 180)
                    intTempNewStartY = intCenterY + intRadius* math.sin (angle * math.pi / 180)
                    intTempNewStartX = int(intTempNewStartX)
                    intTempNewStartY = int(intTempNewStartY)
                    if (intTempNewStartY <= 288):
                        self.driver.swipe(intTempStartX,intTempStartY,intTempNewStartX,intTempNewStartY)
                    time.sleep(5)

                    if ("tone" in Settings):
                        currentValue = self.driver.find_element(*BulbScreenLocators.BULB_TONE).get_attribute('value')
                        if (verifyValue in currentValue):
                            self.report_pass('IOS App : Value set for bulb '+Settings+' as ' +currentValue)
                            break
                        
                    elif ("brightness" in Settings):
                        currentValue = self.driver.find_element(*BulbScreenLocators.BULB_BRIGHTNESS).get_attribute('value')
                        if (verifyValue in currentValue):
                            self.report_pass('IOS App : Value set for bulb '+Settings+' as ' +currentValue)
                            break
                    elif ("colour" in Settings):
                        currentValue = self.driver.find_element(*BulbScreenLocators.BULB_COLOUR).get_attribute('value')
                        if (verifyValue == currentValue):
                            self.report_pass('IOS App : Value set for bulb '+Settings+' as ' +currentValue)
                            break
                    intTempStartX = intTempNewStartX
                    intTempStartY = intTempNewStartY                        
            except:
                self.report_fail('IOS App : NoSuchElementException: in setValueForBulb Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))      


    def verifyAPI(self,nodeID): 
        if self.reporter.ActionStatus:
            try:
                attributeVerify = ""
                attributeName = ""
                if ("tone" in ColourLights.SETTINGS_LOCAL):
                    attributeVerify = "colourTemperature"
                    attributeName = "reportedValue"
                elif ("colour" in ColourLights.SETTINGS_LOCAL):
                    attributeVerify ="hsvHue"
                    attributeName = "targetValue"
                elif ("brightness" in ColourLights.SETTINGS_LOCAL):
                    attributeVerify = "brightness"
                    attributeName = "targetValue"
                attributeValue = oAPIValidations.getColourBulbValues(nodeID,attributeVerify,attributeName)
                attributeValue = int(attributeValue)
                if (attributeValue != ""):
                    if ("tone" in ColourLights.SETTINGS_LOCAL):
                        if ("coolest white" in ColourLights.VALUE_LOCAL):
                            if (attributeValue >= 5471 & attributeValue <= 6535):
                                attributeValue = str(attributeValue)
                                self.report_pass('IOS App : The value for tone is updated in the API as ' +attributeValue+' for given tone '+ColourLights.VALUE_LOCAL)
                        elif ("cool white" in ColourLights.VALUE_LOCAL):
                            if (attributeValue >= 4981 & attributeValue <= 5740):
                                attributeValue = str(attributeValue)
                                self.report_pass('IOS App : The value for tone is updated in the API as ' +attributeValue+' for given tone '+ColourLights.VALUE_LOCAL)
                        elif ("mid white" in ColourLights.VALUE_LOCAL):
                            if (attributeValue >= 4221 & attributeValue <= 4980):
                                attributeValue = str(attributeValue)
                                self.report_pass('IOS App : The value for tone is updated in the API as ' +attributeValue+' for given tone '+ColourLights.VALUE_LOCAL)
                        elif ("warm white" in ColourLights.VALUE_LOCAL):
                            if (attributeValue >= 3461 & attributeValue <= 4220):
                                attributeValue = str(attributeValue)
                                self.report_pass('IOS App : The value for tone is updated in the API as ' +attributeValue+' for given tone '+ColourLights.VALUE_LOCAL)
                        elif ("warmest white" in ColourLights.VALUE_LOCAL):
                            if (attributeValue >= 2700 & attributeValue <= 3460):
                                attributeValue = str(attributeValue)
                                self.report_pass('IOS App : The value for tone is updated in the API as ' +attributeValue+' for given tone '+ColourLights.VALUE_LOCAL)
                        else:
                            attributeValue = str(attributeValue)
                            self.report_fail('IOS App : The value for tone is updated in the API as ' +attributeValue+' for given tone '+ColourLights.VALUE_LOCAL)
                    elif ("colour" in ColourLights.SETTINGS_LOCAL):
                        if (ColourLights.VALUE_LOCAL == "Red"):
                            if (attributeValue <= 6):
                                attributeValue = str(attributeValue)
                                self.report_pass('IOS App : The value for colour is updated in the API as ' +attributeValue+' for given colour '+ColourLights.VALUE_LOCAL)
                        elif (ColourLights.VALUE_LOCAL == "Red Orange"):
                            if (attributeValue >= 11 & attributeValue <= 20):
                                attributeValue = str(attributeValue)
                                self.report_pass('IOS App : The value for colour is updated in the API as ' +attributeValue+' for given colour '+ColourLights.VALUE_LOCAL)
                        elif (ColourLights.VALUE_LOCAL == "Orange"):
                            if (attributeValue >= 21 & attributeValue <= 40):
                                attributeValue = str(attributeValue)
                                self.report_pass('IOS App : The value for colour is updated in the API as ' +attributeValue+' for given colour '+ColourLights.VALUE_LOCAL)
                        elif (ColourLights.VALUE_LOCAL == "Orange Yellow"):
                            if (attributeValue >= 41 & attributeValue <= 50):
                                attributeValue = str(attributeValue)
                                self.report_pass('IOS App : The value for colour is updated in the API as ' +attributeValue+' for given colour '+ColourLights.VALUE_LOCAL)
                        elif (ColourLights.VALUE_LOCAL == "Yellow"):
                            if (attributeValue >= 51 & attributeValue <= 60):
                                attributeValue = str(attributeValue)
                                self.report_pass('IOS App : The value for colour is updated in the API as ' +attributeValue+' for given colour '+ColourLights.VALUE_LOCAL)
                        elif (ColourLights.VALUE_LOCAL == "Yellow Green"):
                            if (attributeValue >= 61 & attributeValue <= 80):
                                attributeValue = str(attributeValue)
                                self.report_pass('IOS App : The value for colour is updated in the API as ' +attributeValue+' for given colour '+ColourLights.VALUE_LOCAL)
                        elif (ColourLights.VALUE_LOCAL == "Green"):
                            if (attributeValue >= 81 & attributeValue <= 140):
                                attributeValue = str(attributeValue)
                                self.report_pass('IOS App : The value for colour is updated in the API as ' +attributeValue+' for given colour '+ColourLights.VALUE_LOCAL)
                        elif (ColourLights.VALUE_LOCAL == "Green Cyan"):
                            if (attributeValue >= 141 & attributeValue <= 169):
                                attributeValue = str(attributeValue)
                                self.report_pass('IOS App : The value for colour is updated in the API as ' +attributeValue+' for given colour '+ColourLights.VALUE_LOCAL)
                        elif (ColourLights.VALUE_LOCAL == "Cyan"):
                            if (attributeValue >= 170 & attributeValue <= 200):
                                attributeValue = str(attributeValue)
                                self.report_pass('IOS App : The value for colour is updated in the API as ' +attributeValue+' for given colour '+ColourLights.VALUE_LOCAL)
                        elif (ColourLights.VALUE_LOCAL == "Cyan Blue"):
                            if (attributeValue >= 201 & attributeValue <= 220):
                                attributeValue = str(attributeValue)
                                self.report_pass('IOS App : The value for colour is updated in the API as ' +attributeValue+' for given colour '+ColourLights.VALUE_LOCAL)
                        elif (ColourLights.VALUE_LOCAL == "Blue"):
                            if (attributeValue >= 221 & attributeValue <= 240):
                                attributeValue = str(attributeValue)
                                self.report_pass('IOS App : The value for colour is updated in the API as ' +attributeValue+' for given colour '+ColourLights.VALUE_LOCAL)
                        elif (ColourLights.VALUE_LOCAL == "Blue Magenta"):
                            if (attributeValue >= 241 & attributeValue <= 280):
                                attributeValue = str(attributeValue)
                                self.report_pass('IOS App : The value for colour is updated in the API as ' +attributeValue+' for given colour '+ColourLights.VALUE_LOCAL)
                        elif (ColourLights.VALUE_LOCAL == "Magenta"):
                            if (attributeValue >= 281 & attributeValue <= 320):
                                attributeValue = str(attributeValue)
                                self.report_pass('IOS App : The value for colour is updated in the API as ' +attributeValue+' for given colour '+ColourLights.VALUE_LOCAL)
                        elif (ColourLights.VALUE_LOCAL == "Magenta Pink"):
                            if (attributeValue >= 321 & attributeValue <= 330):
                                attributeValue = str(attributeValue)
                                self.report_pass('IOS App : The value for colour is updated in the API as ' +attributeValue+' for given colour '+ColourLights.VALUE_LOCAL)
                        elif (ColourLights.VALUE_LOCAL == "Pink"):
                            if (attributeValue >= 331 & attributeValue <= 345):
                                attributeValue = str(attributeValue)
                                self.report_pass('IOS App : The value for colour is updated in the API as ' +attributeValue+' for given colour '+ColourLights.VALUE_LOCAL)
                        elif (ColourLights.VALUE_LOCAL == "Pink Red"):
                            if (attributeValue >= 346 & attributeValue <= 355):
                                attributeValue = str(attributeValue)
                                self.report_pass('IOS App : The value for colour is updated in the API as ' +attributeValue+' for given colour '+ColourLights.VALUE_LOCAL)
                    elif ("brightness" in ColourLights.SETTINGS_LOCAL):
                        if (int(ColourLights.VALUE_LOCAL) == attributeValue):
                                attributeValue = str(attributeValue)
                                self.report_pass('IOS App : The value for brightness is updated in the API as ' +attributeValue+' for given brightness '+ColourLights.VALUE_LOCAL)
                        else:
                            attributeValue = str(attributeValue)
                            self.report_fail('IOS App : The value for brightness is updated in the API as ' +attributeValue+' for given brightness '+ColourLights.VALUE_LOCAL)
                else:
                    self.report_fail('IOS App : API validation failed for '+ColourLights.SETTINGS_LOCAL)
                
                if (ColourLights.SWITCH_ON == 1):
                    self.driver.tap([(158,236)]) 
                    ColourLights.SWITCH_ON = 0
                
            except:
                self.report_fail('IOS App : NoSuchElementException: in verifyAPI Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))      