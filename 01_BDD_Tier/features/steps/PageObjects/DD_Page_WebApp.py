'''
Created on 16 Jun 2015

@author: ranganathan.veluswamy
'''

#from element import BasePageElement
import os
import time
import traceback

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from EE_Locators_WebApp import LoginPageLocators, HeatingPageLocators, HotWaterPageLocators,ForgottenPasswordPageLocators,HeatingDashboardLocators, HeatingNotificationLocators, DashboardLocators

import FF_ScheduleUtils as oSchedUtils
import FF_convertTimeTemperature as tt
from _decimal import Context
from lib2to3.pgen2.driver import Driver


class BasePage(object):

    #Contructor for BasePage
    def __init__(self, driver, reporter):
        self.driver = driver
        self.reporter = reporter 
        
        self.webDayList = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        self.EXPLICIT_WAIT_TIME = 15
    
    #Waits for the given element exists for EXPLICIT_WAIT_TIME 
    def wait_for_element_exist(self, by, value, intWaitTime = 0):
        if intWaitTime == 0: intWaitTime = self.EXPLICIT_WAIT_TIME
        try:
            wait = WebDriverWait(self.driver, intWaitTime)
            wait.until(EC.presence_of_element_located((by, value)))
            return True
        except TimeoutException:
            return False
            print(by, value, 'element not found')
        
    #Initializes the  Selenium Web Driver
    def setup_Selenium_driver(self, strBrowserName, strURL):
        if strBrowserName.upper() == 'FIREFOX':
            '''desired_cap = {
            "platform": "Windows 10",
            "browserName": "internet explorer",
            "version": "11"
            }
            driver = webdriver.Remote(
               command_executor='http://rangawillb4u:2f69f940-28e9-4cae-ac75-b5f0c430f339@ondemand.saucelabs.com:80/wd/hub',
               desired_capabilities=desired_cap)'''
            driver = webdriver.Firefox()
            driver.get(strURL)
            driver.maximize_window()
            driver.implicitly_wait(60)
            return driver
    
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
    
    def refresh_page(self):
        self.driver.refresh()
        time.sleep(3)
     
    def click_element_on_position(self, oClickElement, strPosition = 'Center'):
        intWidth = oClickElement.size['width']
        intHieght = oClickElement.size['height']
        intX = intWidth/2
        
        if strPosition.upper() == 'TOP':
            intY = intHieght/4
        elif strPosition.upper() == 'BOTTOM':
            intY = (intHieght/4) * 3
        else: intY = intHieght/2
        
        action = ActionChains(oClickElement.parent)
        action.move_to_element_with_offset(oClickElement, intX, intY)
        action.click()
        action.perform()
        time.sleep(0.2)
    
    #Clicks on the Scrollable element to set the specific value passed 
    def _set_target_temperature(self, oTargTempElement, fltSetTargTemp):
        if fltSetTargTemp == 1.0: fltSetTargTemp = 7.0
        fltCurrentTargTemp = oTargTempElement.get_attribute('aria-valuenow')
        
        if fltCurrentTargTemp is None:
            self.click_element_on_position(oTargTempElement, 'Top')
            self.click_element_on_position(oTargTempElement, 'Bottom')
            fltCurrentTargTemp = oTargTempElement.get_attribute('aria-valuenow')
        fltCurrentTargTemp = float(fltCurrentTargTemp)
        
        print(fltCurrentTargTemp)
        print(fltSetTargTemp)
        if not fltSetTargTemp==fltCurrentTargTemp:
            intCntrIter = 1
            while (fltCurrentTargTemp != fltSetTargTemp) and (intCntrIter < 3):
                strPositionToClick = 'Top'
                if fltSetTargTemp < fltCurrentTargTemp: strPositionToClick = 'Bottom'
                intIterCount = int(abs(fltSetTargTemp-fltCurrentTargTemp)/0.5)
                for intCnt in range(intIterCount):
                    self.click_element_on_position(oTargTempElement, strPositionToClick)
                fltCurrentTargTemp = float(oTargTempElement.get_attribute('aria-valuenow'))
                intCntrIter += 1
        time.sleep(5) 
        if  fltSetTargTemp==fltCurrentTargTemp: return True
        else: return False
        
    #Highlight Element on the webpafe
    def highlight(self, element):
        """Highlights (blinks) a Selenium Webdriver element"""
        driver = element._parent
        def apply_style(s):
            driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                  element, s)
        original_style = element.get_attribute('style')
        apply_style("background: yellow; border: 2px solid red;")
        time.sleep(.3)
        apply_style(original_style)
        
    #The Schedule Row on the Table on Web Application for the  given Day
    def get_SchedRow(self, oSchedRowElLst, strDay):
        intDayIndexCntr = 0
        for oSchedRow in oSchedRowElLst:
            if len(oSchedRow.get_attribute('data-reactid')) == 9:
                strActDay = self.webDayList[intDayIndexCntr]
                if strDay == strActDay:
                    return oSchedRow
                intDayIndexCntr +=1
    
    #Get StartX int15MinLen
    def get_15min_Xlen(self):
        oTimeScaleStartEl = self.driver.find_element(*HeatingPageLocators.TIME_SCALE_FIRST) 
        oTimeScaleEndEl = self.driver.find_element(*HeatingPageLocators.TIME_SCALE_LAST) 
        fltStartX = oTimeScaleStartEl.location['x']
        flt15MinLen = (oTimeScaleEndEl.location['x'] - fltStartX) / (24 * 4)
        return flt15MinLen, fltStartX
    
    #First Set all event to Last one
    def set_all_events_to_last(self, oEventList, intLstEvntXPos):
        for intC in range(len(oEventList)-1, 0, -1):
            evnt = oEventList[intC]
            if not evnt.get_attribute('class') == 'desktop-event-container event-overlap':
                evntDotEl = evnt.find_elements_by_tag_name('div')[1]
            else: evntDotEl = evnt
            self.highlight(evntDotEl)
            #time.sleep(3)
            offsetX = intLstEvntXPos - evntDotEl.location['x'] 
            #if not float(offsetX) == 0.0:
            action = ActionChains(self.driver)
            action.drag_and_drop_by_offset(evntDotEl, offsetX, 5).perform()
            evnt.click()
            
    #Remove events
    def remove_events(self, intDelEventCount):
        intButtonCenterY = 27
        intEventMinusButtonX = 190
        intSchedBtnBtnX = 60
        #Click Schedule Options button
        action = ActionChains(self.oSchedTableEL.parent)
        action.move_to_element_with_offset(self.oSchedTableEL, intSchedBtnBtnX, intButtonCenterY).click().perform()
        time.sleep(1)     
        #Click Minus button
        action = ActionChains(self.oSchedTableEL.parent)
        action.move_to_element_with_offset(self.oSchedTableEL, intEventMinusButtonX, intButtonCenterY).click().perform()
        time.sleep(1)
        
        #Deleting Event
        for intCntr in range(0, intDelEventCount):
            print(intCntr)
            oCurEvent = self.oSourceSchedList[intCntr]
            print(oCurEvent)            
            intCurrentEventStartPosition = self.intWidthLeftPad + (tt.timeStringToMinutes(oCurEvent[0])/15) * self.intWidthOf15Min
            if intCntr == len(self.oSourceSchedList) - 1:
                intNextEventStartPosition = self.intWidthLeftPad + 24 * 4 * self.intWidthOf15Min
            else:
                intNextEventStartPosition =self.intWidthLeftPad + (tt.timeStringToMinutes(self.oSourceSchedList[intCntr+1][0])/15) * self.intWidthOf15Min
            intCurrEventMid = (intNextEventStartPosition - intCurrentEventStartPosition)/2
            intCurEvntClickPos = intCurrentEventStartPosition + intCurrEventMid
            #Click on events that needs to be deleted
            action = ActionChains(self.oSchedTableEL.parent)
            action.move_to_element_with_offset(self.oSchedTableEL, intCurEvntClickPos, self.intYDay).click().perform()
            time.sleep(1)
            self.oSourceSchedList.remove(oCurEvent)
        
        #Click Schedule Options Cancel button
        action = ActionChains(self.oSchedTableEL.parent)
        action.move_to_element_with_offset(self.oSchedTableEL, intSchedBtnBtnX, intButtonCenterY).click().perform()
        time.sleep(2)     
        
    #Add events
    def add_events(self, intEventsToAdd):
        #Get schedule option button details
        intButtonCenterY = 27
        intSchedBtnBtnX = 60
        intEventAddButtonX = 110
        
        #Click Schedule Options button
        action = ActionChains(self.oSchedTableEL.parent)
        action.move_to_element_with_offset(self.oSchedTableEL, intSchedBtnBtnX, intButtonCenterY).click().perform()
        
        #Click Add button
        action = ActionChains(self.oSchedTableEL.parent)
        action.move_to_element_with_offset(self.oSchedTableEL, intEventAddButtonX, intButtonCenterY).click().perform()
        
        #Load Event Positions to List
        oSourceEventPosList = [self.intWidthLeftPad] 
        for oEvent in self.oSourceSchedList:
            intCurrentEventStartPosition = self.intWidthLeftPad + (tt.timeStringToMinutes(oEvent[0])/15) * self.intWidthOf15Min
            oSourceEventPosList.append(intCurrentEventStartPosition)    
        print(oSourceEventPosList)
        
        #Get Event Positions to add
        oEventToAddPosList  = []
        intStartPosToClick = oSourceEventPosList[1]
        intEventIndexCntr = 0
        while True:
            intStartPosToClick = intStartPosToClick + self.intWidthOf15Min
            if not intStartPosToClick in oSourceEventPosList:
                oEventToAddPosList.append(intStartPosToClick)
                if self.oSourceSchedList[intEventIndexCntr][1] == 99.0: fltNewTargTemp = 0.0
                else: fltNewTargTemp = 99.0
                print(intEventIndexCntr, intStartPosToClick, float(self.oSourceSchedList[intEventIndexCntr][1]), fltNewTargTemp)
                self.oSourceSchedList.insert(intEventIndexCntr+1, (intStartPosToClick,fltNewTargTemp))
                intEventIndexCntr = intEventIndexCntr +1
            else:intEventIndexCntr = intEventIndexCntr +1
            if len(oEventToAddPosList) >= intEventsToAdd:
                break
        print(self.oSourceSchedList)
        
        #Click on new event Position to add
        for oPos in oEventToAddPosList:        
            action = ActionChains(self.oSchedTableEL.parent)
            print(oPos)
            action.move_to_element_with_offset(self.oSchedTableEL, oPos, self.intYDay).click_and_hold().release().perform()
            time.sleep(2)
            
        #Click Schedule Options Cancel button
        action = ActionChains(self.oSchedTableEL.parent)
        action.move_to_element_with_offset(self.oSchedTableEL, intSchedBtnBtnX, intButtonCenterY).click().perform()
        time.sleep(2)
            
    #Set Schedule Start times for the given schedule for the day
    def set_event_start_times(self, oEventListEL, oSchedList, intLstEvntXPos):
        for intC in range(0, len(oSchedList)):
            evnt = oEventListEL[intC+1]
            int15MinLen = self.get_15min_Xlen()
            fltStartX = int15MinLen[1]
            int15MinLen = int15MinLen[0]
            intCurEvntXPos = fltStartX + (tt.timeStringToMinutes(oSchedList[intC][0])/15) * int15MinLen
            offSetVal = intLstEvntXPos - intCurEvntXPos
            if not offSetVal == 0.0:
                action = ActionChains(self.driver)
                action.drag_and_drop_by_offset(evnt, -offSetVal, 5).perform()
                evnt.click()
                time.sleep(1)
        time.sleep(2)
        
      
    def navigate_to_settingScreen(self, strPageName):
        if self.reporter.ActionStatus:
            try:
                if (strPageName == 'NOTIFICATION'):
                    landingPage = self.driver.find_element(*HeatingDashboardLocators.NOTIFICATION_LINK)
                #if (strPageName == 'Manage Device') :
                    #landingPage = self.driver.find_element(*HeatingDashboardLocators.MANAGE_DEVICE_LINK)
                #if (strPageName == 'Install Device') :
                    #landingPage = self.driver.find_element(*HeatingDashboardLocators.INSTALL_DEVICE_LINK)
                #if (strPageName == 'Change Password') :
                    #landingPage = self.driver.find_element(*HeatingDashboardLocators.CHANGE_PASSWORD_LINK)
                #if (strPageName == 'Text Control') :
                    #landingPage = self.driver.find_element(*HeatingDashboardLocators.TEXT_CONTROL_LINK)      
                #if (strPageName == 'Holiday Mode') :
                    #landingPage = self.driver.find_element(*HeatingDashboardLocators.HOLIDAY_MODE_LINK)
        
        
                if self.wait_for_element_exist(*HeatingDashboardLocators.SETTINGS_MENU) :
                    oMoveToSettings = self.driver.find_element(*HeatingDashboardLocators.SETTINGS_MENU)      
                    action = ActionChains(self.driver).move_to_element(oMoveToSettings)
                    action.perform()
                time.sleep(2)
            
                try : 
                    landingPage.click()
                    if self.wait_for_element_exist(*HeatingNotificationLocators.TITLE_LABEL):
                        time.sleep(1)
                        self.report_done('Web App : Navigation to Notification screen is successful')
            
                except NoSuchElementException as z :
                    self.report_fail('Web App : No Such link exists in Settings menu')
            except:  
                self.report_fail('Web App : NoSuchElementException: in get_heating_attribute Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))   
    
                   
#Page Class for Login page. Has all the methods for the Login page
class LoginPage(BasePage):
    #Log in to the Hive Mobile App
    
    def login_hive_app(self, strUserName, strPassword):
        try: 
            if self.wait_for_element_exist(*LoginPageLocators.TITLE_LABEL):
                self.driver.find_element(*LoginPageLocators.USERNAME_EDTBOX).send_keys(strUserName)
                self.driver.find_element(*LoginPageLocators.PASSWORD_EDTBOX).send_keys(strPassword)
                self.driver.find_element(*LoginPageLocators.LOGIN_BUTTON).click()
                if self.wait_for_element_exist(*HeatingPageLocators.USERNAME_DISPLAY):   
                    self.report_pass('Web App : The Hive Desktop Application is successfully Logged in')   
                #if self.wait_for_element_exist(*HeatingPageLocators.MY_HIVE_LINK):   
                    #self.report_pass('Web App : The Hive Desktop Application is successfully Logged in')                   
                    
                #elif self.wait_for_element_exist(*HeatingPageLocators.MY_HIVE_MENU):
                    #self.report_pass('Web App : The Hive Desktop Application is successfully Logged in')
                    
                else:
                    self.report_fail('Web App : The Hive Desktop Application is not logged in. Please check the Login credentials and re-execute test.')                
            else:
                self.report_fail('Web App : The Hive Desktop Application is either not Launched or the Login screen is not displayed. Please check and re-execute test.')
                
        except NoSuchElementException as e:
            self.report_fail('Web App : NoSuchElementException: {0} in login_hive_app Method'.format(e))

class HoneycombDashboardPage(BasePage):
    
    def navigate_to_heating_product_page(self):
        if self.reporter.ActionStatus:
            try :
                if self.wait_for_element_exist(*DashboardLocators.HEATING_THUMBNAIL):  
                    if self.wait_for_element_exist(*DashboardLocators.HEATING_THUMBNAIL_OFFLINE): 
                        self.report_fail('Web App : Device is Offline ')
                    else:
                        self.driver.find_element(*DashboardLocators.HEATING_THUMBNAIL).click()
                        self.report_pass('Web App : Successfully navigated to the Heating product page')
            except:
                self.report_fail('Web App : NoSuchElementException: in navigate_to_heating_product_page Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
    
    def navigate_to_hot_water_product_page(self):
        if self.reporter.ActionStatus:
            try :
                if self.wait_for_element_exist(*DashboardLocators.HOTWATER_THUMBNAIL):  
                    if self.wait_for_element_exist(*DashboardLocators.HOTWATER_THUMBNAIL_OFFLINE): 
                        self.report_fail('Web App : Device is Offline ')
                    else:
                        self.driver.find_element(*DashboardLocators.HOTWATER_THUMBNAIL).click()
                        self.report_pass('Web App : Successfully navigated to the Hotwater product page')
            except:
                self.report_fail('Web App : NoSuchElementException: in navigate_to_hot_water_product_page Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
                

class HeatingDashboardPage(BasePage):
    
    def logout(self):
        #if self.reporter.ActionStatus:
            try:
                oMoveToSettings = self.driver.find_element(*HeatingDashboardLocators.SETTINGS_MENU)      
                action = ActionChains(self.driver).move_to_element(oMoveToSettings)
                action.perform()
                self.driver.find_element(*HeatingDashboardLocators.LOGOUT_LINK).click()
        
            except NoSuchElementException as z :
                self.report_fail('Web App : NoSuchElementException: {0} in logout method'.format(z.strerror))
  

#Page Class for Heating page. Has all the methods for the Heating page
class HeatingPage(BasePage):
    #Set Heat mode
    def set_heat_mode(self, strMode):
        try: 
            
            if self.wait_for_element_exist(*HeatingPageLocators.HEAT_MODE_GROUP):             
                self.driver.refresh()
                time.sleep(5)
                if self.wait_for_element_exist(*HeatingPageLocators.STOP_BOOST_BUTTON):
                    if self.driver.find_element(*HeatingPageLocators.STOP_BOOST_BUTTON).is_displayed():
                        self.driver.find_element(*HeatingPageLocators.STOP_BOOST_BUTTON).click()
                        time.sleep(5)
                        self.driver.refresh()
                        time.sleep(5)
                self.wait_for_element_exist(*HeatingPageLocators.TARGET_TEMPERATURE_SCROLL)
                if strMode.upper() == 'AUTO': self.driver.find_element(*HeatingPageLocators.SCHEDULE_MODE_LINK).click()
                elif strMode.upper() == 'MANUAL': self.driver.find_element(*HeatingPageLocators.MANUAL_MODE_LINK).click()
                elif strMode.upper() == 'OFF': self.driver.find_element(*HeatingPageLocators.OFF_MODE_LINK).click()  
                elif strMode.upper() == 'BOOST': self.driver.find_element(*HeatingPageLocators.BOOST_MODE_LINK).click()  
                time.sleep(5)
                self.driver.refresh()
                if self.wait_for_element_exist(*HeatingPageLocators.TARGET_TEMPERATURE_SCROLL):
                    self.report_pass('Web App : Successfully Heat mode is set to <B>' + strMode)
                    '''
                    oTargTempElement = self.driver.find_element(*HeatingPageLocators.TARGET_TEMPERATURE_SCROLL)
                    fltCurrentTargTemp = oTargTempElement.get_attribute('aria-valuenow')
                    if fltCurrentTargTemp is None and strMode == 'MANUAL':
                        self.click_element_on_position(oTargTempElement, 'Top')
                        self.click_element_on_position(oTargTempElement, 'Bottom')
                        fltCurrentTargTemp = oTargTempElement.get_attribute('aria-valuenow')
                    if not fltCurrentTargTemp is None: fltCurrentTargTemp = float(fltCurrentTargTemp)
                    '''
                    return None
                else:
                    self.report_fail('Web App : Unable to set Heat mode to <B>' + strMode)
            else:
                self.report_fail("Web App : Control not active on the Heating Page to set the Heat Mode")
            
        except NoSuchElementException as e:
            self.report_fail('Web App : NoSuchElementException: {0} in set_heat_mode Method'.format(e.strerror))
        
    #Set Target Temperature    
    def set_target_temperature(self, fltTargetTemperature):
        try: 
            if self.wait_for_element_exist(*HeatingPageLocators.TARGET_TEMPERATURE_SCROLL):                
                self.driver.refresh()
                self.wait_for_element_exist(*HeatingPageLocators.TARGET_TEMPERATURE_SCROLL)
                oTargTempEL = self.driver.find_element(*HeatingPageLocators.TARGET_TEMPERATURE_SCROLL)
                boolSetTargTemp = self._set_target_temperature(oTargTempEL, fltTargetTemperature)
                
                self.driver.refresh()
                self.wait_for_element_exist(*HeatingPageLocators.TARGET_TEMPERATURE_SCROLL)
                
                if boolSetTargTemp:
                    self.report_pass('Web App : The Target Temperature is successfully set to : ' + str(fltTargetTemperature))
                else:   
                    self.report_fail('Web App : Unable to set the Target Temperature to : ' + str(fltTargetTemperature))
            else:
                self.report_fail("Web App : Control not active on the Heating Page to set the Target Temperature")
            
        except NoSuchElementException as e:
            self.report_fail('Web App : NoSuchElementException: {0} in set_target_temperature Method'.format(e.strerror))
            
    #Set Heating Schedule
    def set_heating_schedule(self, oSourceSchedDict, oDestSchedDict):
        try: 
            if self.wait_for_element_exist(*HeatingPageLocators.HEATING_SCHEDULE_MAIN):
                oWeekDayList = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
                #Get StartX int15MinLen
                self.oSchedTableEL =  self.driver.find_element(*HeatingPageLocators.HEATING_SCHEDULE_MAIN)  
                
                #Setup Initial Configs
                self.intWidthLeftPad = 60
                intWidthRightPad = 30
                intWidthOfCavas = self.oSchedTableEL.size['width']
                intWidthSchedule = intWidthOfCavas - (self.intWidthLeftPad + intWidthRightPad)
                self.intWidthOf15Min = (intWidthSchedule/24)/4
                print(self.intWidthOf15Min)
                
                for strDay in oDestSchedDict.keys():
                    #Get the DestScedList
                    self.oDestSchedList = oSchedUtils.remove_duplicates(oDestSchedDict[strDay])
                    self.oSourceSchedList = oSchedUtils.remove_duplicates(oSourceSchedDict[strDay])
                    self.intYDay = 100 + 40* (oWeekDayList.index(strDay))
                    
                    intSourceListCount = len(self.oSourceSchedList)
                    intDestListCount = len(self.oDestSchedList)
                    if intSourceListCount > intDestListCount:
                        self.remove_events(intSourceListCount - intDestListCount)
                    elif intSourceListCount < intDestListCount:
                        self.add_events(intDestListCount - intSourceListCount)
                    print(intSourceListCount, intDestListCount)
                   
                    self.report_done('Web App : For Day  : ' + strDay + ' Before all events are Merged to last')
                    #Get Last events position
                    strLstEvntStTime = self.oSourceSchedList[len(self.oSourceSchedList) - 1][0]
                    intLstEvntXPos = self.intWidthLeftPad + (tt.timeStringToMinutes(strLstEvntStTime)/15) * self.intWidthOf15Min
                    intLastEventMoveToPosition = len(self.oSourceSchedList) * self.intWidthOf15Min    
                    intLastEventInitialOffset = - (intLstEvntXPos - intLastEventMoveToPosition)
                    #And move all the events to the beginning
                    action = ActionChains(self.oSchedTableEL.parent)
                    action.move_to_element_with_offset(self.oSchedTableEL, intLstEvntXPos, self.intYDay).click_and_hold().move_by_offset(intLastEventInitialOffset, 0).release().perform()
                    time.sleep(2)                    
                    self.report_done('Web App : For Day  : ' + strDay + ' After all events are Merged to last')
                    
                    #Set Dest Schedule Start times
                    for intCntr in range(len(self.oDestSchedList)-1, -1, -1):
                        oCurEvent = self.oDestSchedList[intCntr]
                        intCurEvntDestPos = self.intWidthLeftPad + (tt.timeStringToMinutes(oCurEvent[0])/15) * self.intWidthOf15Min
                        intCurEvntSourcePos = self.intWidthLeftPad + (intCntr * self.intWidthOf15Min)
                        intCurOffsetPos = intCurEvntDestPos - intCurEvntSourcePos
                        #And move the event to the Dest Position
                        action = ActionChains(self.oSchedTableEL.parent)
                        action.move_to_element_with_offset(self.oSchedTableEL, intCurEvntSourcePos, self.intYDay).click_and_hold().move_by_offset(intCurOffsetPos, 0).release().perform()
                        #time.sleep(2)
                    self.report_pass('Web App : For Day  : ' + strDay + ' After all events Start Times are set')
                    
                    #Set Target temperature to for all events of the day
                    for intCntr in range(0, len(self.oDestSchedList)):
                        print(intCntr)
                        oCurEvent = self.oDestSchedList[intCntr]
                        print(oCurEvent)            
                        intCurrentEventStartPosition = self.intWidthLeftPad + (tt.timeStringToMinutes(oCurEvent[0])/15) * self.intWidthOf15Min
                        if intCntr == len(self.oDestSchedList) - 1:
                            intNextEventStartPosition = self.intWidthLeftPad + 24 * 4 * self.intWidthOf15Min
                        else:
                            intNextEventStartPosition =self.intWidthLeftPad + (tt.timeStringToMinutes(self.oDestSchedList[intCntr+1][0])/15) * self.intWidthOf15Min
                        intCurrEventMid = (intNextEventStartPosition - intCurrentEventStartPosition)/2
                        intCurEvntClickPos = intCurrentEventStartPosition + intCurrEventMid
                        #And move the event to the Dest Position
                        action = ActionChains(self.oSchedTableEL.parent)
                        action.move_to_element_with_offset(self.oSchedTableEL, intCurEvntClickPos, self.intYDay).click().perform()
                        time.sleep(2)
                        self.report_pass('Web App : For Day  : ' + strDay + ' Before Target Temperatures for Event number ' + str(intCntr+1) + ' is set') 
                        fltSetTargTemp = float(oCurEvent[1])
                        if self.wait_for_element_exist(*HeatingPageLocators.SCHEDULE_TARGET_TEMPERATURE_SCROLLV6):
                            oSchedTargTemScrollEL = self.driver.find_element(*HeatingPageLocators.SCHEDULE_TARGET_TEMPERATURE_SCROLLV6) 
                            self._set_target_temperature(oSchedTargTemScrollEL, fltSetTargTemp)
                            self.report_pass('Web App : For Day  : ' + strDay + ' After Target Temperatures for Event number ' + str(intCntr+1) + ' is set')     
                        else:
                            self.report_fail('Web App : For Day  : ' + strDay + ' Target Temperatures Object for Event number ' + str(intCntr+1) + ' is not displayed')
                    
                    self.report_pass('Web App : For Day  : ' + strDay + ' After all events Target Temperatures are set')                           
                     
                self.driver.find_element(*HeatingPageLocators.SAVE_BUTTONV6).click()                
                self.report_pass('Web App : Heating Schedule Screen after all the New Schedule is Set')
            else:
                self.report_fail("Web App : Control not active on the Heating Page to set the Heating Schedule")
            
        except:
            self.report_fail('iOS APP: Exception in set_heating_schedule Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))

            
    #Set Heating Schedule
    def set_heating_scheduleV5(self, oScheduleDict):
        try: 
            if self.wait_for_element_exist(*HeatingPageLocators.HEATING_SCHEDULE_TABLE):
                #Get StartX int15MinLen
                int15MinLen = self.get_15min_Xlen()
                fltStartX = int15MinLen[1]
                int15MinLen = int15MinLen[0]
                
                #Heating Schedule Table
                oSchedTableEl = self.driver.find_element(*HeatingPageLocators.HEATING_SCHEDULE_TABLE)
                oSchedRowElLst = oSchedTableEl.find_elements_by_tag_name('li')
                
                for strDay in oScheduleDict.keys():
                    #strDay = 'fri'
                    oSchedList = oScheduleDict[strDay]
                    oSchedList = oSchedUtils.remove_duplicates(oSchedList)
                    oSchedRow = self.get_SchedRow(oSchedRowElLst, strDay)
                    self.highlight(oSchedRow)
                    oEventList = oSchedRow.find_elements_by_tag_name('li')    
                    strLstEvntStTime = oSchedList[len(oSchedList) - 1][0]
                    intLstEvntXPos = fltStartX + (tt.timeStringToMinutes(strLstEvntStTime)/15) * int15MinLen
                    print(fltStartX, int15MinLen)
                    print(intLstEvntXPos, strLstEvntStTime)
                    self.report_done('Web App : For Day  : ' + strDay + ' Before all events are Merged to last')
                    
                    #First Set all event to Last one
                    self.set_all_events_to_last(oEventList, intLstEvntXPos)
                    self.report_done('Web App : For Day  : ' + strDay + ' After all events are Merged to last')
                
                    #Set all events start time
                    self.report_done('Web App : For Day  : ' + strDay + ' Before all events Start Times are set')
                    oEventListEL = oSchedRow.find_elements_by_tag_name('li')  
                    self.set_event_start_times(oEventListEL, oSchedList, intLstEvntXPos)
                    self.report_pass('Web App : For Day  : ' + strDay + ' After all events Start Times are set')
                    
                    #Set all events Target Temperature
                    self.report_done('Web App : For Day  : ' + strDay + ' Before all events Target Temperatures are set')
                    oEventListEL = oSchedRow.find_elements_by_tag_name('li')    
                    for intC in range(0, len(oSchedList)):
                        intEvntCntr = intC+1
                        if intC == len(oSchedList) - 1:
                            intEvntCntr = 6
                        fltSetTargTemp = float(oSchedList[intC][1])
                        oEvent = oEventListEL[intEvntCntr]
                        if not oEvent.get_attribute('class') == 'desktop-event-container event-overlap':
                            evntTempEl = oEvent.find_elements_by_tag_name('div')[0]
                            fltTargTemp = float(evntTempEl.get_attribute('class').split('temp')[1].replace('-', '.'))
                            if not fltSetTargTemp == fltTargTemp:
                                evntTempEl.click()
                                time.sleep(1)
                                oTargTempElement = self.driver.find_elements(*HeatingPageLocators.SCHEDULE_TARGET_TEMPERATURE_SCROLL)
                                self.set_target_temperature(oTargTempElement[1], fltSetTargTemp)   
                    self.report_pass('Web App : For Day  : ' + strDay + ' After all events Target Temperatures are set')                           
                     
                self.driver.find_element(*HeatingPageLocators.SAVE_BUTTON).click()                
                self.report_pass('Web App : Heating Schedule Screen after all the New Schedule is Set')
            else:
                self.report_fail("Web App : Control not active on the Heating Page to set the Heating Schedule")
            
        except NoSuchElementException as e:
            self.report_fail('Web App : NoSuchElementException: {0} in set_heating_schedule Method'.format(e.strerror))
            
    #Get Attributes for Heating Controls                
    def get_heating_attribute(self):
        if self.reporter.ActionStatus:
            strMode = 'OFF'
            strRunningState = '0000'
            fltCurrentTargTemp = 0.0
            try: 
                self.refresh_page()
                if self.wait_for_element_exist(*HeatingPageLocators.HEAT_MODE_GROUP):                    
                    oHMGEL = self.driver.find_element(*HeatingPageLocators.HEAT_MODE_GROUP)
                    print(oHMGEL.find_element(*HeatingPageLocators.STOP_BOOST_BUTTON).is_displayed())
                    if oHMGEL.find_element(*HeatingPageLocators.STOP_BOOST_BUTTON).is_displayed(): strMode = 'BOOST'
                    else:
                        strMode =oHMGEL.find_element(*HeatingPageLocators.CURRENT_MODE_ITEM).text.upper()
                        if 'SCHEDULE' in strMode: strMode = 'AUTO'
                        
                    oTargTempElement = self.driver.find_element(*HeatingPageLocators.TARGET_TEMPERATURE_SCROLL)
                    fltCurrentTargTemp = oTargTempElement.get_attribute('aria-valuenow')
                    if fltCurrentTargTemp is None:
                        self.click_element_on_position(oTargTempElement, 'Top')
                        self.click_element_on_position(oTargTempElement, 'Bottom')
                        fltCurrentTargTemp = oTargTempElement.get_attribute('aria-valuenow')
                    fltCurrentTargTemp = float(fltCurrentTargTemp)
                    
                    if oHMGEL.find_element(*HeatingPageLocators.RUNNING_STATE_FLAME_ICON).is_displayed(): strRunningState = '0001'
                    print(strMode, fltCurrentTargTemp, strRunningState)
    
                else:
                    self.report_fail("Web-App : Control not active on the Heating Page to get Heating Attributes")
                
                self.report_done('Web App : Screenshot while getting attributes')
                if fltCurrentTargTemp == 7.0: fltCurrentTargTemp = 1.0
                return strMode, strRunningState, fltCurrentTargTemp
            except:
                self.report_fail('Web App : NoSuchElementException: in get_heating_attribute Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
               
   
#Page Class for Hot Water page. Has all the methods for the Hot Water page
class HotWaterPage(BasePage):
    #Set Hot Water mode
    def set_hot_water_mode(self, strMode):
        try: 
            if self.wait_for_element_exist(*HotWaterPageLocators.HOT_WATER_CONTROLER_GROUP):    
                if self.driver.find_element(*HotWaterPageLocators.STOP_BOOST_BUTTON).is_displayed():
                    self.driver.find_element(*HotWaterPageLocators.STOP_BOOST_BUTTON).click()
                    time.sleep(5)
                    self.driver.refresh()
                oHotWaterMenuEl = self.driver.find_element(*HotWaterPageLocators.HOT_WATER_CONTROLER_GROUP)  
                self.wait_for_element_exist(*HotWaterPageLocators.HOT_WATER_CONTROLER_GROUP)
                if strMode.upper() == 'AUTO': oHotWaterMenuEl.find_element(*HotWaterPageLocators.SCHEDULE_MODE_LINK).click()
                elif strMode.upper() == 'MANUAL': oHotWaterMenuEl.find_element(*HotWaterPageLocators.MANUAL_MODE_LINK).click()
                elif strMode.upper() == 'OFF': oHotWaterMenuEl.find_element(*HotWaterPageLocators.OFF_MODE_LINK).click()           
                elif strMode.upper() == 'BOOST': 
                    oHotWaterMenuEl.find_element(*HotWaterPageLocators.BOOST_MODE_LINK).click()
                time.sleep(5)
                self.driver.refresh()
                if self.wait_for_element_exist(*HotWaterPageLocators.HOT_WATER_CONTROLER_GROUP):
                    self.report_pass('Web APP : Successfully Hot Water Mode mode is set to <B>' + strMode)
                else:
                    self.report_fail('Web APP : Unable to set Hot Water mode to <B>' + strMode)
            else:
                self.report_fail("Web App : Control not active on the Hot Water Page to set the Hot Water Mode")
            
        except NoSuchElementException as e:
            self.report_fail('Web App : NoSuchElementException: {0} in set_Hot Water_mode Method'.format(e.strerror))
   
    #Set Hot water Schedule
    def set_hot_water_schedule(self, oSourceSchedDict, oDestSchedDict):
        try: 
            if self.wait_for_element_exist(*HotWaterPageLocators.HOT_WATER_SCHEDULE_MAIN):
                oWeekDayList = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
                #Get StartX int15MinLen
                self.oSchedTableEL =  self.driver.find_element(*HotWaterPageLocators.HOT_WATER_SCHEDULE_MAIN)
                
                #Setup Initial Configs
                self.intWidthLeftPad = 60
                intWidthRightPad = 30
                intWidthOfCavas = self.oSchedTableEL.size['width']
                intWidthSchedule = intWidthOfCavas - (self.intWidthLeftPad + intWidthRightPad)
                self.intWidthOf15Min = (intWidthSchedule/24)/4
                print(self.intWidthOf15Min)
                
                for strDay in oDestSchedDict.keys():
                    #Get the DestScedList
                    self.oDestSchedList = oSchedUtils.remove_duplicates(oDestSchedDict[strDay])
                    self.oSourceSchedList = oSchedUtils.remove_duplicates(oSourceSchedDict[strDay])
                    self.intYDay = 100 + 40* (oWeekDayList.index(strDay))
                    
                    intSourceListCount = len(self.oSourceSchedList)
                    intDestListCount = len(self.oDestSchedList)
                    if intSourceListCount > intDestListCount:
                        self.remove_events(intSourceListCount - intDestListCount)
                    elif intSourceListCount < intDestListCount:
                        self.add_events(intDestListCount - intSourceListCount)
                    print(intSourceListCount, intDestListCount)
                    self.report_done('Web App : For Day  : ' + strDay + ' Before all events are Merged to last')
                    #Get Last events position
                    strLstEvntStTime = self.oSourceSchedList[len(self.oSourceSchedList) - 1][0]
                    intLstEvntXPos = self.intWidthLeftPad + (tt.timeStringToMinutes(strLstEvntStTime)/15) * self.intWidthOf15Min
                    intLastEventMoveToPosition = len(self.oSourceSchedList) * self.intWidthOf15Min    
                    intLastEventInitialOffset = - (intLstEvntXPos - intLastEventMoveToPosition)
                    #And move all the events to the beginning
                    action = ActionChains(self.oSchedTableEL.parent)
                    action.move_to_element_with_offset(self.oSchedTableEL, intLstEvntXPos, self.intYDay).click_and_hold().move_by_offset(intLastEventInitialOffset, 0).release().perform()
                    time.sleep(2)                    
                    self.report_done('Web App : For Day  : ' + strDay + ' After all events are Merged to last')
                    
                    #Set Dest Schedule Start times
                    for intCntr in range(len(self.oDestSchedList)-1, -1, -1):
                        oCurEvent = self.oDestSchedList[intCntr]
                        intCurEvntDestPos = self.intWidthLeftPad + (tt.timeStringToMinutes(oCurEvent[0])/15) * self.intWidthOf15Min
                        intCurEvntSourcePos = self.intWidthLeftPad + (intCntr * self.intWidthOf15Min)
                        intCurOffsetPos = intCurEvntDestPos - intCurEvntSourcePos
                        #And move the event to the Dest Position
                        action = ActionChains(self.oSchedTableEL.parent)
                        action.move_to_element_with_offset(self.oSchedTableEL, intCurEvntSourcePos, self.intYDay).click_and_hold().move_by_offset(intCurOffsetPos, 0).release().perform()
                        #time.sleep(2)
                    self.report_pass('Web App : For Day  : ' + strDay + ' After all events Start Times are set')
                    
                    #Set Running State for all events of the day
                    for intCntr in range(0, len(self.oDestSchedList)):
                        print(intCntr)
                        oCurEvent = self.oDestSchedList[intCntr]
                        print(oCurEvent)            
                        intCurrentEventStartPosition = self.intWidthLeftPad + (tt.timeStringToMinutes(oCurEvent[0])/15) * self.intWidthOf15Min
                        if intCntr == len(self.oDestSchedList) - 1:
                            intNextEventStartPosition = self.intWidthLeftPad + 24 * 4 * self.intWidthOf15Min
                        else:
                            intNextEventStartPosition =self.intWidthLeftPad + (tt.timeStringToMinutes(self.oDestSchedList[intCntr+1][0])/15) * self.intWidthOf15Min
                        intCurrEventMid = (intNextEventStartPosition - intCurrentEventStartPosition)/2
                        intCurEvntClickPos = intCurrentEventStartPosition + intCurrEventMid
                        
                        self.report_pass('Web App : For Day  : ' + strDay + ' Before Running State for Event number ' + str(intCntr+1) + ' is set') 
                        if oCurEvent[1] != self.oSourceSchedList[intCntr][1]:
                            action = ActionChains(self.oSchedTableEL.parent)
                            action.move_to_element_with_offset(self.oSchedTableEL, intCurEvntClickPos, self.intYDay).click().perform()
                            time.sleep(2)
                            self.report_pass('Web App : For Day  : ' + strDay + ' After Running State for Event number ' + str(intCntr+1) + ' is set')   
                    
                    self.report_pass('Web App : For Day  : ' + strDay + ' After all events Running State are set')                           
                     
                self.driver.find_element(*HotWaterPageLocators.SAVE_BUTTONV6).click()                
                self.report_pass('Web App : Hot Water Schedule Screen after all the New Schedule is Set')
            else:
                self.report_fail("Web App : Control not active on the Hot Water Page to set the Heating Schedule")
            
        except:
            self.report_fail('iOS APP: Exception in set_heating_schedule Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))

    #Set Hot Water Schedule
    def set_hot_water_scheduleV5(self, oScheduleDict):
        try: 
            if self.wait_for_element_exist(*HotWaterPageLocators.HOT_WATER_SCHEDULE_TABLE):
                #Get StartX int15MinLen
                int15MinLen = self.get_15min_Xlen()
                fltStartX = int15MinLen[1]
                int15MinLen = int15MinLen[0]
                
                #Heating Schedule Table
                oSchedTableEl = self.driver.find_element(*HotWaterPageLocators.HOT_WATER_SCHEDULE_TABLE)
                oSchedRowElLst = oSchedTableEl.find_elements_by_tag_name('li')
                
                for strDay in oScheduleDict.keys():
                    #strDay = 'fri'
                    oSchedList = oScheduleDict[strDay]
                    oSchedList = oSchedUtils.remove_duplicates(oSchedList)
                    oSchedRow = self.get_SchedRow(oSchedRowElLst, strDay)
                    self.highlight(oSchedRow)
                    oEventList = oSchedRow.find_elements_by_tag_name('li')    
                    strLstEvntStTime = oSchedList[len(oSchedList) - 1][0]
                    intLstEvntXPos = fltStartX + (tt.timeStringToMinutes(strLstEvntStTime)/15) * int15MinLen
                    print(fltStartX, int15MinLen)
                    print(intLstEvntXPos, strLstEvntStTime)
                    self.report_done('Web App : For Day  : ' + strDay + ' Before all events are Merged to last')
                    
                    #First Set all event to Last one
                    self.set_all_events_to_last(oEventList, intLstEvntXPos)
                    self.report_done('Web App : For Day  : ' + strDay + ' After all events are Merged to last')
                
                    #Set all events start time
                    self.report_done('Web App : For Day  : ' + strDay + ' Before all events Start Times are set')
                    oEventListEL = oSchedRow.find_elements_by_tag_name('li')  
                    self.set_event_start_times(oEventListEL, oSchedList, intLstEvntXPos)
                    self.report_pass('Web App : For Day  : ' + strDay + ' After all events Start Times are set')
                    
                    #Set all events Target Temperature
                    self.report_done('Web App : For Day  : ' + strDay + ' Before all events Modes are set')
                    oEventListEL = oSchedRow.find_elements_by_tag_name('li')    
                    for intC in range(0, len(oSchedList)):
                        intEvntCntr = intC+1
                        if intC == len(oSchedList) - 1:
                            intEvntCntr = 6
                        fltSetTargTemp = float(oSchedList[intC][1])
                        if fltSetTargTemp == 99.0: strExpectMode = 'ON'
                        else: strExpectMode = 'OFF'
                        oEvent = oEventListEL[intEvntCntr]
                        if not oEvent.get_attribute('class') == 'desktop-event-container event-overlap':
                            evntModeEl = oEvent.find_elements_by_tag_name('div')[0]
                            strActualMode = evntModeEl.text
                            if not strExpectMode == strActualMode.upper():
                                evntModeEl.click() 
                    self.report_pass('Web App : For Day  : ' + strDay + ' After all events Target Modes are set')                           
                oSchedGroupEL = self.driver.find_element(*HotWaterPageLocators.HOT_WATER_SCHEDULE_GROUP)
                oSchedGroupEL.find_element(*HotWaterPageLocators.SAVE_BUTTON).click()                
                self.report_pass('Web App : Hot Water Schedule Screen after all the New Schedule is Set')
            else:
                self.report_fail("Web App : Control not active on the Hot Water Page to set the Hot Water Schedule")
            
        except NoSuchElementException as e:
            self.report_fail('Web App : NoSuchElementException: {0} in set_hot_water_schedule Method'.format(e.strerror))
            
            
    #Get Attributes for Heating Controls                
    def get_hotwater_attribute(self):
        if self.reporter.ActionStatus:
            strMode = 'OFF'
            strRunningState = '0000'
            fltCurrentTargTemp = 0.0
            try: 
                self.refresh_page()
                if self.wait_for_element_exist(*HotWaterPageLocators.HOT_WATER_CONTROLER_GROUP):                    
                    oHWMGEL = self.driver.find_element(*HotWaterPageLocators.HOT_WATER_CONTROLER_GROUP)
                    print(oHWMGEL.find_element(*HotWaterPageLocators.STOP_BOOST_BUTTON).is_displayed())
                    if oHWMGEL.find_element(*HotWaterPageLocators.STOP_BOOST_BUTTON).is_displayed(): strMode = 'BOOST'
                    else:
                        strMode =oHWMGEL.find_element(*HotWaterPageLocators.CURRENT_MODE_ITEM).text.upper()
                        if 'SCHEDULE' in strMode: strMode = 'AUTO'
                        elif 'ON' in strMode: strMode = 'Always ON'
                        elif 'OFF' in strMode: strMode = 'Always OFF'
                    if oHWMGEL.find_element(*HotWaterPageLocators.HOT_WATER_RUNNING_STATE).get_attribute('aria-hidden').upper() == 'TRUE': strRunningState = '0001'
                else:
                    self.report_fail("Web-App : Control not active on the Hot Water Page to get Heating Attributes")
                
                self.report_done('Web App : Screenshot while getting attributes')
                return strMode, strRunningState, fltCurrentTargTemp
            except:
                self.report_fail('Web App : NoSuchElementException: in get_hot_water_attribute Method\n {0}'.format(traceback.format_exc().replace('File', '$~File')))
               
            


class ForgottenPassword(BasePage):              
    def set_screen(self,strScreenName):
        if self.reporter.ActionStatus:
            try :
                if self.wait_for_element_exist(*LoginPageLocators.FORGOTTEN_PASSWORD_LINK):
                    self.driver.find_element(*LoginPageLocators.FORGOTTEN_PASSWORD_LINK).click()
                    self.report_pass('Web App : Forgotten Password link clicked successfully')
                    if self.wait_for_element_exist(*ForgottenPasswordPageLocators.TITLE_LABEL):
                       self.report_pass('Web App : Forgotten Password screen loaded successfully') 
                    else :
                        self.report_fail('Web App : Forgotten Password screen does not exist')
                    
                else :
                    self.report_fail('Web App : Forgotten Password link is not working') 
            except NoSuchElementException as z :
                self.report_fail('Web App : NoSuchElementException: {0} in set_screen method'.format(z.strerror))
            
    def submit_username(self,strEmailAddr):
        if self.reporter.ActionStatus:
            try : 
                if self.wait_for_element_exist(*ForgottenPasswordPageLocators.TITLE_LABEL):
                    self.driver.find_element(*ForgottenPasswordPageLocators.EMAIL_ADDR_FIELD).send_keys(strEmailAddr)
                    self.driver.find_element(*ForgottenPasswordPageLocators.SUBMIT_BUTTON).click()
                    time.sleep(4)
                    if self.wait_for_element_exist(*ForgottenPasswordPageLocators.REMINDER_MESSAGE):
                        self.report_pass('Web App : Password reset email is sent successfully')
                        time.sleep(5)
            except NoSuchElementException as z :
                        self.report_fail('Web App : NoSuchElementException: {0} in submit_username method'.format(z.strerror))
            
    def set_new_password(self,strUsername,strNewPassword): 
        yopmailURL = 'http://www.yopmail.com/en/'   
        if self.reporter.ActionStatus:
            try :
                self.driver.get(yopmailURL)
                self.driver.find_element(*ForgottenPasswordPageLocators.YOPMAIL_EMAIL_ADDR_FIELD).clear()
                self.driver.find_element(*ForgottenPasswordPageLocators.YOPMAIL_EMAIL_ADDR_FIELD).send_keys(strUsername)
                self.driver.find_element(*ForgottenPasswordPageLocators.YOPMAIL_CHECK_INBOX).click()
                time.sleep(5)
                
                self.driver.switch_to_frame(self.driver.find_element(*ForgottenPasswordPageLocators.FRAME_REF))
                
                time.sleep(4)
                #if self.wait_for_element_exist(*ForgottenPasswordPageLocators.YOPMAIL_HREF_LINK):
                reset_link = self.driver.find_element(*ForgottenPasswordPageLocators.YOPMAIL_HREF_LINK).get_attribute('href')
                self.driver.switch_to_default_content()
                self.report_pass('Web App : Password reset email received')
                self.driver.get(reset_link)
                
                if self.wait_for_element_exist(*ForgottenPasswordPageLocators.PASSWORD_RESET_LABEL):
                    self.driver.find_element(*ForgottenPasswordPageLocators.NEW_PASSWORD).send_keys(strNewPassword)
                    self.driver.find_element(*ForgottenPasswordPageLocators.CONFIRM_PASSWORD).send_keys(strNewPassword)
                    self.driver.find_element(*ForgottenPasswordPageLocators.SUBMIT_BUTTON).click()
                    
                if self.wait_for_element_exist(*ForgottenPasswordPageLocators.SUCCESS_MESSAGE) :
                    self.report_pass('Web App : Password reset successful')
                else :
                    self.report_fail('Web App : Password reset failed') 
                
                self.driver.find_element(*ForgottenPasswordPageLocators.LOGIN_BUTTON).click()         
            
            except NoSuchElementException as z :
                self.report_fail('Web App : NoSuchElementException: {0} in forgotten_password method'.format(z.strerror))
            

class SetNotification(BasePage):    
    def click_element(self,oCheckboxElem,xCoordinator,yCoordinator):
        self.oLoc = oCheckboxElem
        oAction = ActionChains(self.oLoc.parent)
        oAction.move_to_element_with_offset(self.oLoc,xCoordinator,yCoordinator).click().perform()
        return True
        
    def iteration_count(self,oTargetTemp,oCurrentTemp):
        if oTargetTemp!= oCurrentTemp:
            itrCount = int(abs(oTargetTemp-oCurrentTemp)/0.5)
            return itrCount
        else:
            return 0
    
    def upDown_decider(self,oTargetTemp,oCurrentTemp,num_iteration,tempUpDown):
        if oTargetTemp > oCurrentTemp :
            for itrCount in range(num_iteration):
                self.click_element(tempUpDown,51,15)
        elif oTargetTemp < oCurrentTemp :
            for itrCount in range(num_iteration):
                self.click_element(tempUpDown,51,25)
        else :
            print() 
                                               
        
    def set_high_temperature(self,oTargetHighTemp,oTargetLowTemp='',oBothAlert='No'):
        if oBothAlert == 'Yes':
            self.driver.refresh()
        
        if self.reporter.ActionStatus:
            if self.wait_for_element_exist(*HeatingNotificationLocators.TITLE_LABEL) :
                try:
                    if not self.driver.find_element(*HeatingNotificationLocators.HIGH_TEMP_CHKBOX).is_selected()==True :
                        self.driver.find_element(*HeatingNotificationLocators.HIGH_TEMP_CHKBOX).click()
                    tempUpDown=self.driver.find_element(*HeatingNotificationLocators.HIGH_TEMP_TT)
                    oCurrentTemp = tempUpDown.get_attribute('value')
                    oCurrentTemp = float(oCurrentTemp)
                    time.sleep(1)
                    num_iteration=self.iteration_count(oTargetHighTemp, oCurrentTemp)
                    self.upDown_decider(oTargetHighTemp, oCurrentTemp, num_iteration,tempUpDown) 
                    #self.driver.find_element(*HeatingNotificationLocators.HIGH_TEMP_TT).clear()
                    #self.driver.find_element(*HeatingNotificationLocators.HIGH_TEMP_TT).send_keys(temp)
                    time.sleep(2)
                    
                    self.report_done('Web App : Target Temperature for High temperature Alert has been set to ' + str(oTargetHighTemp))
                    if oBothAlert == 'Yes' :
                        self.set_low_temperature(oTargetLowTemp,oBothAlert)
                    else :
                        self.driver.find_element(*HeatingNotificationLocators.SAVE_BUTTON).click()
                        time.sleep(3)
                        self.report_pass('Web App : High Notification Alert has been successfully set')
                        self.driver.refresh()

                except NoSuchElementException as z :
                    self.report_fail('Web App : NoSuchElementException: {0} in set_high_temperature method'.format(z.strerror))  
        else:
            self.report_fail("Web App : Control not active on the Notification Page to set the notification")
    
    
    def set_low_temperature(self,oTargetLowTemp,oBothAlert='No'):
        if self.reporter.ActionStatus:
            if self.wait_for_element_exist(*HeatingNotificationLocators.TITLE_LABEL) :
                try:
                    if not self.driver.find_element(*HeatingNotificationLocators.LOW_TEMP_CHKBOX).is_selected()==True :
                        self.driver.find_element(*HeatingNotificationLocators.LOW_TEMP_CHKBOX).click()
                    tempUpDown=self.driver.find_element(*HeatingNotificationLocators.LOW_TEMP_TT)
                    oCurrentTemp = tempUpDown.get_attribute('value')
                    oCurrentTemp = float(oCurrentTemp)
                    time.sleep(1)
                    num_iteration=self.iteration_count(oTargetLowTemp, oCurrentTemp) 
                    self.upDown_decider(oTargetLowTemp, oCurrentTemp, num_iteration,tempUpDown)
                    time.sleep(2)   
                    self.report_done('Web App : Target Temperature for Low temperature Alert has been set to ' + str(oTargetLowTemp))
                    time.sleep(1)  
                    self.driver.find_element(*HeatingNotificationLocators.SAVE_BUTTON).click()
                    time.sleep(3)
                    if oBothAlert == 'Yes' :
                        self.report_pass('Web App : High Notification & Low Notification Alert has been successfully set')
                    else :
                        self.report_pass('Web App : Low Notification Alert has been successfully set')
                    self.driver.refresh()
                
                except NoSuchElementException as z :
                        self.report_fail('Web App : NoSuchElementException: {0} in set_low_temperature method'.format(z.strerror))  
                             
            else:
                self.report_fail("Web App : Control not active on the Notification Page to set the notification")
                                                
    def setNotificationOnOff(self,strNotiState,strNotiType='Both'):  
        if self.reporter.ActionStatus:
            if self.wait_for_element_exist(*HeatingNotificationLocators.TITLE_LABEL) :
                try:
                    if strNotiType =='Both' or strNotiType == 'High' :
                        if strNotiState == 'OFF' :
                            self.driver.find_element(*HeatingNotificationLocators.HIGH_TEMP_CHKBOX).click() 
                            time.sleep(1) 
                    
                    if strNotiType =='Both' or strNotiType == 'Low' :
                        if strNotiState == 'OFF' :
                            self.driver.find_element(*HeatingNotificationLocators.LOW_TEMP_CHKBOX).click()
                            time.sleep(1)
                    self.driver.find_element(*HeatingNotificationLocators.SAVE_BUTTON).click()
                    time.sleep(1)
                    self.report_pass('Web App : Notification Alerts has been turned '+strNotiState+' successfully')
                    
                except NoSuchElementException as z :
                        self.report_fail('Web App : NoSuchElementException: {0} in set_low_temperature method'.format(z.strerror))  
                             
            else:
                self.report_fail("Web App : Control not active on the Notification Page to set the notification")    
    
    def getNotificationTempFromUI(self,strNotiType='Both'):    
        if strNotiType=='Both' or strNotiType=='High':
            tempHighUpDown=self.driver.find_element(*HeatingNotificationLocators.HIGH_TEMP_TT)
            oCurrentHighTemp = tempHighUpDown.get_attribute('value')
            oCurrentHighTemp = float(oCurrentHighTemp)
                    
        if strNotiType=='Both' or strNotiType=='Low':
            tempLowUpDown=self.driver.find_element(*HeatingNotificationLocators.LOW_TEMP_TT)
            oCurrentLowTemp = tempLowUpDown.get_attribute('value')
            oCurrentLowTemp = float(oCurrentLowTemp)
         
        return oCurrentHighTemp,oCurrentLowTemp   