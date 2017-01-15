'''
Created on 10 Jun 2015

@author: ranganathan.veluswamy
'''

#from ConfigParser import configParser
import os
import platform
from subprocess import Popen, PIPE
import time
import traceback

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox import firefox_profile
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait

from EE_Locators_WebApp import HotWaterPageLocators, HeatingPageLocators, LoginPageLocators
import FF_convertTimeTemperature as tt


webDayList = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

class WEB(object):
        
    def setUpWebDriver(self, strURL):
        driver = webdriver.Firefox()
        driver.get('https://beta-my.hivehome.com')
        driver.maximize_window()
    
        return driver
    
    def loginWeb(self, driver, strUserName, strPassword):
        driver.find_element_by_id('username').send_keys(strUserName)
        driver.find_element_by_id('password').send_keys(strPassword)
        driver.find_element_by_xpath("//*[@type='submit']" ).click()
        time.sleep(5)
    
    
    def setHeatMode(self, driver, strMode, reporter):
        driver.refresh()
        time.sleep(5)
        modes = {'OFF' : 'off', 'AUTO': 'schedule', 'MANUAL': 'manual'}
        lstModeElem = driver.find_element_by_xpath("//*[@active-item='local.mode']").find_element_by_xpath("//*[contains(@aria-label, 'activate " + modes[strMode.upper()] + "')]")
        lstModeElem.click()
        time.sleep(2)
        driver.refresh()
        time.sleep(3)
        reporter.ReportEvent('Test Validation', 'Successfully Heat mode is set to <B>' + strMode, "PASS", 'Center', True, driver)
        
        oTargTempElement = driver.find_element_by_xpath("//*[@throbber-throb-for='heating.temperature']")
        fltCurrentTargTemp = oTargTempElement.get_attribute('aria-valuenow')
        
        if fltCurrentTargTemp is None:
            self.click_element_on_position(oTargTempElement, 'Top')
            self.click_element_on_position(oTargTempElement, 'Bottom')
            fltCurrentTargTemp = oTargTempElement.get_attribute('aria-valuenow')
        fltCurrentTargTemp = float(fltCurrentTargTemp)
        return fltCurrentTargTemp
        
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
    def set_target_target_temperature(self, oTargTempElement, fltSetTargTemp):
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
                
    def set_main_target_temperature(self, driver, fltSetTargTemp, reporter):   
        driver.refresh()
        time.sleep(3)
        
        TargTempEl = driver.find_element_by_xpath("//*[@throbber-throb-for='heating.temperature']")
        self.set_target_target_temperature(TargTempEl, fltSetTargTemp)
        
        driver.refresh()
        time.sleep(3)
        reporter.ReportEvent('Test Validation', 'Successfully Target Temperature is set to <B>' + str(fltSetTargTemp), "PASS", 'Center', True, driver)
    
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
    
    def get_SchedRow(self, oSchedRowElLst, strDay):
        intDayIndexCntr = 0
        for oSchedRow in oSchedRowElLst:
            if len(oSchedRow.get_attribute('data-reactid')) == 9:
                strActDay = webDayList[intDayIndexCntr]
                if strDay == strActDay:
                    return oSchedRow
                intDayIndexCntr +=1
    
                
        
    
    def TempTest(self, driver):
        try:
            driver.find_element_by_xpath("//*[@type='submit']").click()  
        except:
            strTraceback = traceback.format_exc()
            print('Tracebacccccckc   :   "', strTraceback)
            
            
    
    
    #Waits for the given element exists for EXPLICIT_WAIT_TIME 
    def wait_for_element_exist(self, by, value, intWaitTime = 0):
        if intWaitTime == 0: intWaitTime = 15
        try:
            wait = WebDriverWait(self.driver, intWaitTime)
            wait.until(EC.presence_of_element_located((by, value)))
            return True
        except TimeoutException:
            return False
            print(by, value, 'element not found')
            
    def main(self):
        
    
        driver = webdriver.Firefox()   
        self.driver = driver
        driver.get('https://intprod-my.hivehome.net')
        #driver.get('https://intprod-my.hivehome.net/dashboard')
        driver.maximize_window()
        #print(driver.find_element_by_xpath("//*[@name='loginForm']" ).text)
           
        self.driver.find_element(*LoginPageLocators.USERNAME_EDTBOX).send_keys('auto1_v6')
        self.driver.find_element(*LoginPageLocators.PASSWORD_EDTBOX).send_keys('password1')          
        self.driver.find_element(*LoginPageLocators.LOGIN_BUTTON).click()    
        time.sleep(5)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        driver.quit()
        exit()
    
    
if __name__ == '__main__':
    oWeb = WEB()
    oWeb.main()
    
    