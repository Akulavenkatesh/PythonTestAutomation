'''
Created on 11 Jun 2015

@author: ranganathan.veluswamy
'''


from _ast import While
from datetime import datetime
import os
import sys
import time
import traceback

from appium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from steps.EE_Locators_AndroidApp import LoginPageLocators, HomePageLocators, HeatingHomePageLocators, HotWaterHomePageLocators, HeatingControlPageLocators, HotWaterControlPageLocators, SchedulePageLocators, EditTimeSlotPageLocators, EditBoostTimePageLocators , AccountDetailsLocators


import steps.FF_ScheduleUtils as oSchedutils


def setUpAndroidDriver(strAndroidPlatformVersion, strDeviceName, strAppPath):

    #success = True
    desired_caps = {}
    desired_caps['appium-version'] = '1.0'
    desired_caps['platformName'] = 'Android'
    desired_caps['platformVersion'] = strAndroidPlatformVersion
    desired_caps['deviceName'] = strDeviceName
    desired_caps['app'] = os.path.abspath(strAppPath)
    desired_caps['appPackage'] = 'uk.co.centrica.hive.v6.internalprod"'      #uk.co.centrica.hive.isopbeta'
    desired_caps['appActivity'] = 'uk.co.centrica.hive.ui.base.HiveBottomDrawerActivity'
    desired_caps['noReset'] = True
    
    oAndroidDriver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
    oAndroidDriver.implicitly_wait(60)
    
    return oAndroidDriver

def wait_for_element_exist1(driver, by, value, intWaitTime = 0):
        if intWaitTime == 0: intWaitTime =50
        try:
            wait = WebDriverWait(driver, intWaitTime)
            wait.until(EC.presence_of_element_located((by, value)))
            time.sleep(1)
            return True
        except TimeoutException:
            print(by, value, 'element not found')
            return False
class ANDROID_UI(object):  
    def setUp(self):
    
    
    
        success = True
        desired_caps = {}
        desired_caps["browserName"] = ""
        desired_caps["appium-version"] = "1.4.0"
        desired_caps["platformName"] = "Android"
        desired_caps["platformVersion"] = "5.1"
        desired_caps["deviceName"] = "Nexus 6"
        desired_caps["udid"] = "ZX1G42BJHK"
        desired_caps["app"] = os.path.abspath("/Users/ranganathan.veluswamy/Downloads/Hive-productV6BetaInternalTesters-release-1.2.0.47.apk")
        desired_caps["appPackage"] = "uk.co.centrica.hive.v6.beta.internaltesters"      #uk.co.centrica.hive.isopbeta"
        desired_caps["appActivity"] = "uk.co.centrica.hive.ui.base.HiveBottomDrawerActivity"
        desired_caps["noReset"] = True
        
        wd = webdriver.Remote('http://127.0.0.1:4725/wd/hub', desired_caps)
        wd.implicitly_wait(60)
    
        input('Ji')
        wd.quit()
        exit()
    
    
    
    
    
    
        desired_caps = {}
        desired_caps['browserName'] = ""
        desired_caps['appiumVersion'] = "1.4.13"
        desired_caps['deviceName'] = "LG Nexus 4 Emulator"
        desired_caps['deviceOrientation'] = "portrait"
        desired_caps['platformVersion'] = "4.4"
        desired_caps['platformName'] = "Android"
        desired_caps['app'] = "sauce-storage:test.apk"
        '''desired_caps["browserName"] = ""
        desired_caps["appium-version"] = "1.4.0"
        desired_caps["platformName"] = "Android"
        desired_caps["platformVersion"] = "4.4"
        desired_caps["deviceName"] = "LG Nexus 4 Emulator 4.4"
        desired_caps["app"] = "sauce-storage:test.apk"
        desired_caps["appPackage"] = "uk.co.centrica.hive.v6.internalprod" 
        desired_caps["appActivity"] = "uk.co.centrica.hive.ui.base.HiveBottomDrawerActivity"'''
        desired_caps["noReset"] = True
    
        wd = webdriver.Remote(command_executor="http://BGCHIS:3c0fd44d-951a-48b4-aa77-80fe20904233@ondemand.saucelabs.com:80/wd/hub", desired_capabilities = desired_caps)
        wd.implicitly_wait(60)
    
        input('Ji')
        wd.quit()
        exit()
    
    
    
    
        success = True
        desired_caps = {}
        desired_caps["browserName"] = ""
        desired_caps["appium-version"] = "1.4.0"
        desired_caps["platformName"] = "Android"
        desired_caps["platformVersion"] = "5.1"
        desired_caps["deviceName"] = "Nexus 6"
        #desired_caps["app"] = os.path.abspath("/Users/ranganathan.veluswamy/Desktop/Ranga/Workspace/EclipseWorkspace/HiveTestAutomation/02_Manager_Tier/EnviromentFile/Apps/Android/isopInternProd/Hive-productV6Internalprod-release-1.2.0.46.apk")
        desired_caps["app"] = "sauce-storage:test.apk"
        desired_caps["appPackage"] = "uk.co.centrica.hive.v6.internalprod"      #uk.co.centrica.hive.isopbeta"
        desired_caps["appActivity"] = "uk.co.centrica.hive.ui.base.HiveBottomDrawerActivity"
        desired_caps["noReset"] = True
        
        #wd = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        #wd = webdriver.Remote('http://127.0.0.1:4490/wd/hub', desired_caps)
        '''print(desired_caps)
        
        
        
        
        caps = {}
        caps['browserName'] = ""
        caps['appiumVersion'] = "1.4.11"
        caps['deviceName'] = "LG Nexus 4 Emulator"
        caps['deviceOrientation'] = "portrait"
        caps['platformVersion'] = "4.4"
        caps['platformName'] = "Android"'''
        
        
        
        
        
        wd = webdriver.Remote(command_executor="http://BGCHIS:a0614862-ec6d-4de2-b9bb-41a10a2d37c8@ondemand.saucelabs.com:80/wd/hub", desired_capabilities = desired_caps)
        wd.implicitly_wait(60)
        self.driver = wd
        def is_alert_present(wd):
            try:
                wd.switch_to_alert().text
                return True
            except:
                return False
        
        try:
            
            
            
            
            
            '''self.driver.find_element_by_id('boost_timer').click()
            print(wd.find_element_by_id('boostTimeIntervalList').is_displayed())'''
            
            
            input('Ji')
            wd.quit()
            exit()
            
            #android.widget.ProgressBar[1]
            print(datetime.today().strftime("%H:%M:%S" ))
            wd.find_element_by_name("Refresh button").click()
            wait_for_element_exist1(wd, By.NAME, 'Refresh button')
            print(datetime.today().strftime("%H:%M:%S" ))
            input('Ji')
            wd.quit()
            exit()
            #Login
            loginAndroidApp(wd, "flashtest4@yopmail.com", "password1")
            START_TIME_LABEL = (By.ID, 'textViewFromTime')
            wait_for_element_exist(wd, *START_TIME_LABEL)
            wd.find_element_by_name("Refresh button").click()      
            wd.find_element_by_xpath("//*[@text='heating control']").click()  
            print(datetime.today().strftime("%H:%M:%S" )) 
            wait = WebDriverWait(wd, 20)
            wait.until(EC.presence_of_element_located((By.NAME,'Refresh button')))
            print(datetime.today().strftime("%H:%M:%S" ))
            
            
            exit()
            '''
            wd.find_element_by_name("Refresh button").click()        
            print(datetime.today().strftime("%H:%M:%S" )) 
            wait = WebDriverWait(wd, 20)
            wait.until(EC.presence_of_element_located((By.NAME,'Refresh button')))
            print(datetime.today().strftime("%H:%M:%S" ))
            wd.find_element_by_name("Refresh button").click()        
            print(datetime.today().strftime("%H:%M:%S" )) 
            wait = WebDriverWait(wd, 20)
            wait.until(EC.presence_of_element_located((By.NAME,'Refresh button')))
            print(datetime.today().strftime("%H:%M:%S" ))
            wd.find_element_by_name("Refresh button").click()        
            print(datetime.today().strftime("%H:%M:%S" )) 
            wait = WebDriverWait(wd, 20)
            wait.until(EC.presence_of_element_located((By.NAME,'Refresh button')))
            print(datetime.today().strftime("%H:%M:%S" ))
            wd.find_element_by_name("Refresh button").click()        
            print(datetime.today().strftime("%H:%M:%S" )) 
            wait = WebDriverWait(wd, 20)
            wait.until(EC.presence_of_element_located((By.NAME,'Refresh button')))
            print(datetime.today().strftime("%H:%M:%S" ))
            wd.find_element_by_name("Refresh button").click()        
            print(datetime.today().strftime("%H:%M:%S" )) 
            wait = WebDriverWait(wd, 20)
            wait.until(EC.presence_of_element_located((By.NAME,'Refresh button')))
            print(datetime.today().strftime("%H:%M:%S" ))
            '''
            '''
            boolWaitForElementToDisappaear = True
            while boolWaitForElementToDisappaear:
                try:
                    boolWaitForElementToDisappaear = wd.find_element_by_id('toast_progress_bar').is_displayed()
                except:
                    boolWaitForElementToDisappaear = False
                  
            wait = WebDriverWait(wd, 20)
            wait.until(EC.presence_of_element_located((By.NAME,'Refresh button')))
            print(datetime.today().strftime("%H:%M:%S" ))
            exit()
            print(wd.find_element_by_id('toast_progress_bar').is_displayed())
            print(wd.find_element_by_id('toast_progress_bar').is_enabled())
            print(wd.find_element_by_id('toast_progress_bar').is_selected())
            
            print(EC.presence_of_element_located((By.ID,'toast_progress_bar')))
            
            print(datetime.today().strftime("%H:%M" ))
            testExpectedConditionInvisiblityOfElementLocated(wd)
            wait = WebDriverWait(wd, 20)
            wait.until(EC.presence_of_element_located((By.ID,'toast_progress_bar')))
            print(datetime.today().strftime("%H:%M" ))
            
            exit()
            
            exit()
            '''  
            #Navigate to Heating Control Page To Set Mode
            wd.find_element_by_xpath("//*[@text='heating control']").click()
            setHeatMode(wd, 'Manual')    
            
            #Navigate to Heating Control Page To Set Target Temperature
            wd.find_element_by_xpath("//*[@text='heating control']").click()
            setTargetTemperature(wd, 17.0)   
            
            
            #Navigate to Heating Schedule Page
            wd.find_element_by_xpath("//*[@text='heating schedule']").click()
            oSchedList ={ 'mon' :[('06:30', 20.0), ('08:30', 1.0), ('12:00', 1.0), ('14:00', 1.0), ('16:30', 20.0)] ,
                                    'tue' :[('06:30', 20.0), ('08:30', 1.0), ('12:00', 1.0), ('14:00', 1.0), ('16:30', 20.0)]
                                    }#, ('22:00', 1.0)]
            setSchedule(wd, oSchedList)
            
            #Navigate to Heating Control Page To Set Auto Mode
            wd.find_element_by_xpath("//*[@text='heating control']").click()
            setHeatMode(wd, 'Schedule')    
        
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            '''
            #print(exc_type, exc_value, exc_traceback)
            print ("*** print_tb:")
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
            print ("*** print_exception:")
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                                      limit=2, file=sys.stdout)
            print ("*** print_exc:")
            traceback.print_exc()
            print ("*** format_exc, first and last line:")
            formatted_lines = traceback.format_exc().splitlines()
            print (formatted_lines[0])
            print (formatted_lines[-1])
            print ("*** format_exception:")
            print( repr(traceback.format_exception(exc_type, exc_value,
                                                  exc_traceback)))
            print ("*** extract_tb:")
            print (repr(traceback.extract_tb(exc_traceback)))
            print ("*** format_tb:")
            print (repr(traceback.format_tb(exc_traceback)))
            '''
            print( "*** tb_lineno:", exc_traceback.tb_lineno)
            print("££££", exc_type, exc_value)
        finally:
            wd.quit()
            if not success:
                raise Exception("Test failed.")

def wait_for_element_exist(wd, by, value):
    try:
        wait = WebDriverWait(wd, 20)
        wait.until(EC.presence_of_element_located((by, value)))
        return True
    except TimeoutException:
        return False
        
def testExpectedConditionInvisiblityOfElementLocated(driver):
        #driver.execute_script("delayedShowHide(0, true)")
        try:
            WebDriverWait(driver, 0.7).until(EC.invisibility_of_element_located((By.ID, 'toast_progress_bar')))
            #fail("Expected TimeoutException to have been thrown")
        except TimeoutException as e:
            pass    
        #driver.execute_script("delayedShowHide(200, false)")
        WebDriverWait(driver, 0.7).until(EC.invisibility_of_element_located((By.ID, 'toast_progress_bar')))
        print(driver.find_element_by_id('toast_progress_bar').is_displayed())

#Login
def loginAndroidApp(wd, strUsername, strPassword):
    wd.reset()
    time.sleep(2)
    wd.find_element_by_name("enter your username").send_keys(strUsername)
    wd.hide_keyboard()
    wd.find_element_by_name("password").send_keys(strPassword)
    wd.hide_keyboard()
    wd.find_element_by_name("login").click()
    print(datetime.today().strftime("%H:%M" ))
    wait = WebDriverWait(wd, 20)
    wait.until(EC.invisibility_of_element_located((By.ID,'toast_progress_bar')))
    
    print(datetime.today().strftime("%H:%M" ))
    wd.find_element_by_name("Refresh button").click()
    print(datetime.today().strftime("%H:%M" ))
    wait = WebDriverWait(wd, 20)
    wait.until(EC.presence_of_element_located((By.ID,'toast_progress_bar')))
    
    print(datetime.today().strftime("%H:%M" ))
    wd.find_element_by_name('Preset temperature button').click()
    time.sleep(1)
    wd.find_element_by_name('Preset temperature button').click()      
     
#SetSchedule 
def setSchedule(wd, oSchedDict, context):
    
    print(oSchedDict)
    wd.find_element_by_xpath("//*[@text='heating schedule']").click()
    for oKey in oSchedDict.keys():   
        
        oSchedList = oSchedutils.remove_duplicates(oSchedDict[oKey])    
        wd.find_element_by_name("Refresh button").click()
        time.sleep(7)
        context.reporter.ReportEvent("Test Validation", 'ScreenShot of existing schedule', "DONE", 'Center', True, wd)
        #Get Event Count
        lstMoreOptions = wd.find_elements_by_name("More options")
        intActualCount = len(lstMoreOptions)
        intExpectedCount  = len(oSchedList)
        print(intActualCount, intExpectedCount)
        if intActualCount > intExpectedCount:
            #Delete Event
            for intCntr in range((intActualCount -1), intExpectedCount-1, -1):
                lstMoreOptions[intCntr].click()
                context.reporter.ReportEvent("Test Validation", 'Deleting additional event', "DONE", 'Center', True, wd)
                wd.find_element_by_xpath("//*[@text='Delete']").click()   
                time.sleep(7)
        elif intActualCount < intExpectedCount:
            #Add Event
            for intCntr in range((intExpectedCount - 1), intActualCount - 1, -1):
                wd.find_element_by_id('schedule_fab').click()
                wd.find_element_by_id('add_a_time_slot').click()
                context.reporter.ReportEvent("Test Validation", 'Adding Additional Event', "DONE", 'Center', True, wd)
                wd.find_element_by_id('button_save').click()
                time.sleep(7)
        context.reporter.ReportEvent("Test Validation", 'ScreenShot after all additional events are added/removed', "DONE", 'Center', True, wd)
        #Get List of Options & Start Time
        lstStartTime = wd.find_elements_by_id("textViewFromTime")        
        for intCntr in range((len(lstStartTime) -1), -1, -1):
            strSetStartTime = oSchedList[intCntr][0]
            fltSetTargTemp = oSchedList[intCntr][1]
            if fltSetTargTemp ==1.0: fltSetTargTemp = 7.0
            intCntrIter= 0 
            strCurrentStartTIme = ''
            while (strCurrentStartTIme != strSetStartTime) and (intCntrIter <3) :
                lstStartTime[intCntr].click()
                context.reporter.ReportEvent("Test Validation", 'Event number : ' + str(intCntr + 1 ) + ' before the event change', "DONE", 'Center', True, wd)
                setScheduleTargetTemperature(wd, fltSetTargTemp)
                setEventHour(wd, strSetStartTime.split(':')[0])
                setEventMinute(wd, strSetStartTime.split(':')[1])
                time.sleep(2)
                intCntrIter +=1                
                context.reporter.ReportEvent("Test Validation", 'Event number : ' + str(intCntr + 1 ) + ' after the event change', "DONE", 'Center', True, wd)
                wd.find_element_by_xpath("//*[@text='Save']").click()  
                time.sleep(10)
                strCurrentStartTIme = lstStartTime[intCntr].get_attribute('text')
            context.reporter.ReportEvent("Test Validation", 'Main Screen after Event number : ' + str(intCntr + 1 ) + ' is changed', "DONE", 'Center', True, wd)
        context.reporter.ReportEvent("Test Validation", 'Main Screen after all Events are changed', "DONE", 'Center', True, wd)
     
    wd.find_element_by_name("Refresh button").click()
    time.sleep(7)        
           
#Set the Heat Mode
def setHeatMode(wd, strMode):      
    wd.find_element_by_name("Refresh button").click()
    #time.sleep(7)
    modes = {'OFF' : 'Off', 'AUTO': 'Schedule', 'MANUAL': 'Manual'}
    wd.find_element_by_xpath("//*[@text='heating control']").click()
    wd.find_element_by_xpath("//*[@text='" + modes[strMode.upper()] + "']").click()
    
    wd.find_element_by_name("Refresh button").click()
    #time.sleep(7)
#Set Target temperature
def setTargetTemperature(wd, fltSetTargTemp):
    wd.find_element_by_name("Refresh button").click()
    time.sleep(7)
    oScrolElement = wd.find_element_by_id('heatingControlTempControlView')
    fltCurrentTargTemp = float(oScrolElement.get_attribute('name').split()[2])
    setScrollValue(wd, oScrolElement, fltCurrentTargTemp, fltSetTargTemp, 0.5, 2)
    
    wd.find_element_by_name("Refresh button").click()
    #time.sleep(7)

#Set Schedule Target temperature
def setScheduleTargetTemperature(wd, fltSetTargTemp):
    oScrolElement = wd.find_element_by_id('editHeatingScheduleTempControlView')
    fltCurrentTargTemp = float(oScrolElement.get_attribute('name').split()[2])
    setScrollValue(wd, oScrolElement, fltCurrentTargTemp, fltSetTargTemp, 0.5, 2)

#Set Event Hour
def setEventHour(wd, fltSetValue):
    oScrolElement = wd.find_element_by_id('hour')
    fltSetValue = int(fltSetValue)
    fltCurrentValue = int(oScrolElement.find_element_by_id('numberpicker_input').get_attribute('name'))   
    setScrollValue(wd, oScrolElement, fltCurrentValue, fltSetValue, 1, 1.4)
    
#Set Event Minute
def setEventMinute(wd, fltSetValue):
    oScrolElement = wd.find_element_by_id('minute')
    fltSetValue = int(fltSetValue)
    fltCurrentValue = int(oScrolElement.find_element_by_id('numberpicker_input').get_attribute('name'))   
    setScrollValue(wd, oScrolElement, fltCurrentValue, fltSetValue, 15, 1.4)
    
    
        
#Set Scroll Value
def setScrollValue(wd, oScrolElement, fltCurrentValue, fltSetValue, fltPrecision, fltScrolPrecesion):
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

    

if __name__ == '__main__':
    oANd = ANDROID_UI()
    oANd.setUp()
    
    

'''

wd.find_element_by_id('tab_schedule_circle_view')
        print(wd.find_element_by_id('tab_schedule_circle_view').get_attribute('text'))
        
        time.sleep(5)
        wd.find_element_by_name("Refresh button").click()        
        time.sleep(10)
        
        

    elList = wd.find_elements_by_xpath("//*[@text='']")
    oTargTempElement = None
    for el in elList:
        if el.get_attribute('name').find("Scroll to change")>=0:
            oTargTempElement = el
            break
    
        #elList = wd.find_elements_by_xpath("//*[contains(@tag_name, 'LinearLayout')]")
                #wd.execute_script("mobile: tap", {"tapCount": 1, "touchCount": 1, "duration": 1.25703125, "x": 518, "y": 1302 })

        
        #content-desc: Target temperature 7 degrees. Scroll to change.

        
        time.sleep(5)
        wd.swipe(540, 970, 520, 1177, 0.6222265625)
        #element = WebDriverWait(wd, 10).until(EC.invisibility_of_element_located((By.XPATH, "//*[@text='Refreshing']")))
        #wd.execute_script("mobile: swipe", {"touchCount": 1 , "startX": 540, "startY": 970, "endX": 520, "endY": 1177, "duration": 0.6222265625 })
        time.sleep(5)
        
        #wd.find_element_by_name("More options").click()
        #wd.find_element_by_xpath("//*[@text='Demo']").click()
        #time.sleep(10)
#wd.tap(positions, duration)
position = (intStX, intEndY)
print(position)
wd.tap([position], 1000)
#wd.scroll(el, el)
'''