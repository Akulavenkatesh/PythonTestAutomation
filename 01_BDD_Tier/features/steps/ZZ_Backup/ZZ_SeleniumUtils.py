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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox import firefox_profile

import steps.FF_convertTimeTemperature as tt


webDayList = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

def setUpWebDriver(strURL):
    driver = webdriver.Firefox()
    driver.get('https://beta-my.hivehome.com')
    driver.maximize_window()

    return driver

def loginWeb(driver, strUserName, strPassword):
    driver.find_element_by_id('username').send_keys(strUserName)
    driver.find_element_by_id('password').send_keys(strPassword)
    driver.find_element_by_xpath("//*[@type='submit']" ).click()
    time.sleep(5)


def setHeatMode(driver, strMode, reporter):
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
        click_element_on_position(oTargTempElement, 'Top')
        click_element_on_position(oTargTempElement, 'Bottom')
        fltCurrentTargTemp = oTargTempElement.get_attribute('aria-valuenow')
    fltCurrentTargTemp = float(fltCurrentTargTemp)
    return fltCurrentTargTemp
    
def click_element_on_position(oClickElement, strPosition = 'Center'):
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
def set_target_target_temperature(oTargTempElement, fltSetTargTemp):
    if fltSetTargTemp == 1.0: fltSetTargTemp = 7.0
    fltCurrentTargTemp = oTargTempElement.get_attribute('aria-valuenow')
    
    if fltCurrentTargTemp is None:
        click_element_on_position(oTargTempElement, 'Top')
        click_element_on_position(oTargTempElement, 'Bottom')
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
                click_element_on_position(oTargTempElement, strPositionToClick)
            fltCurrentTargTemp = float(oTargTempElement.get_attribute('aria-valuenow'))
            intCntrIter += 1
    time.sleep(5)
            
def set_main_target_temperature(driver, fltSetTargTemp, reporter):   
    driver.refresh()
    time.sleep(3)
    
    TargTempEl = driver.find_element_by_xpath("//*[@throbber-throb-for='heating.temperature']")
    set_target_target_temperature(TargTempEl, fltSetTargTemp)
    
    driver.refresh()
    time.sleep(3)
    reporter.ReportEvent('Test Validation', 'Successfully Target Temperature is set to <B>' + str(fltSetTargTemp), "PASS", 'Center', True, driver)

def highlight(element):
    """Highlights (blinks) a Selenium Webdriver element"""
    driver = element._parent
    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                              element, s)
    original_style = element.get_attribute('style')
    apply_style("background: yellow; border: 2px solid red;")
    time.sleep(.3)
    apply_style(original_style)

def get_SchedRow(oSchedRowElLst, strDay):
    intDayIndexCntr = 0
    for oSchedRow in oSchedRowElLst:
        if len(oSchedRow.get_attribute('data-reactid')) == 9:
            strActDay = webDayList[intDayIndexCntr]
            if strDay == strActDay:
                return oSchedRow
            intDayIndexCntr +=1

            
    

def TempTest(driver):
    try:
        driver.find_element_by_xpath("//*[@type='submit']").click()  
    except:
        strTraceback = traceback.format_exc()
        print('Tracebacccccckc   :   "', strTraceback)
        
        
        
        
def main():
    
    #oschedDict = {'fri': [('4:30', '10'), ('6:30', '17'), ('8:0', '17'), ('12:0', '7'), ('16:30', '10'), ('22:0', '7')]} #, 'tue': [('2:15', '16.5'), ('23:30', '20')], 'mon': [('2:30', '15.5'), ('23:30', '16'), ('23:45', '7')], 'thu': [('8:30', '29'), ('12:0', '7'), ('14:0', '30'), ('16:30', '7')], 'sat': [('6:30', '32'), ('8:30', '7'), ('12:0', '7'), ('14:0', '7'), ('16:30', '20'), ('21:45', '31.5')], 'sun': [('6:30', '20'), ('8:30', '7'), ('12:0', '7'), ('14:0', '7'), ('16:30', '20')], 'wed': [('6:30', '15'), ('8:30', '29'), ('12:0', '7'), ('14:0', '30'), ('16:30', '7'), ('22:0', '23')]}

    
    oschedDict = {'fri':  [('4:30', '10'), ('6:30', '17'), ('8:0', '7'), ('12:0', '17'), ('16:30', '12.0')], 'tue': [('2:15', '6.5'), ('23:30', '10')], 'mon': [('2:30', '5.5'), ('23:30', '6'), ('23:45', '17')], 'thu': [('8:30', '9'), ('12:0', '7'), ('14:0', '30'), ('16:30', '17')], 'sat': [('6:30', '32'), ('8:30', '7'), ('12:0', '17'), ('14:0', '17'), ('16:30', '20'), ('21:45', '11.5')], 'sun': [('6:30', '20'), ('8:30', '7'), ('12:0', '7'), ('14:0', '7'), ('16:30', '20')], 'wed': [('6:30', '15'), ('8:30', '29'), ('12:0', '7'), ('14:0', '30'), ('16:30', '7'), ('22:0', '23')]}
    
    oschedDict = {'tue':  [('08:30', 29.0), ('12:00', 1.0), ('14:00', 30.0), ('16:30', 1.0), ('18:30', 21.0), ('22:30', 1.0)]}
    desired_cap = {
    "platform": "Windows 10",
    "browserName": "internet explorer",
    "version": "11"
    }
    driver = webdriver.Remote(
       command_executor='http://rangawillb4u:2f69f940-28e9-4cae-ac75-b5f0c430f339@ondemand.saucelabs.com:80/wd/hub',
       desired_capabilities=desired_cap)
    #driver = webdriver.Firefox()    
    '''
    driver.get(' https://beta-my.hivehome.com')
    driver.maximize_window()
    #print(driver.find_element_by_xpath("//*[@name='loginForm']" ).text)   
    driver.find_element_by_id('username').send_keys('flashtest4@yopmail.com')
    driver.find_element_by_id('password').send_keys('password1')    
    '''
    
    driver.get('https://intprod-my.hivehome.net')
    #driver.get('https://intprod-my.hivehome.net/dashboard')
    driver.maximize_window()
    #print(driver.find_element_by_xpath("//*[@name='loginForm']" ).text)   
    driver.find_element_by_id('username').send_keys('auto1_v6')
    driver.find_element_by_id('password').send_keys('password1')    
    
    
    driver.find_element_by_xpath("//*[@type='submit']").click()    
    time.sleep(5)
    
    
    
    '''oMainEL = driver.find_element_by_xpath("//*[@ng-controller='HotWaterControlController as hotWaterController']")
    
    highlight(oMainEL)
    '''
    '''if driver.find_element_by_xpath("//*[@ng-controller='HotWaterControlController as hotWaterController']//*[@class='boost-off']").is_displayed() : print('Boost Active')
    time.sleep(5)
    print(oMainEL.find_element_by_link_text('Schedule').get_attribute('class'), 'Schedule')
    time.sleep(5)
    print(oMainEL.find_element_by_link_text('On').get_attribute('class'), 'On')
    #oMainEL.find_element_by_link_text('On').click()
    time.sleep(5)
    print(oMainEL.find_element_by_link_text('Off').get_attribute('class'), 'Off')
    #oMainEL.find_element_by_link_text('Off').click()
    time.sleep(5)
    #oMainEL.find_elements_by_xpath("//*[@class='boost-on']")[1].click()
    time.sleep(5)'''
    
    
    
    
    time.sleep(5)
    
    
    driver.quit()
    exit()
    
    
    driver.find_element_by_xpath("//*[@class='boost-off']").click()
    
    driver.refresh()
    time.sleep(5)
    
    driver.find_element_by_xpath("//*[@class='boost-on']").click()
    time.sleep(3)
    print(driver.find_element_by_xpath("//*[@class='hours-minutes']").text)
 
    #oHourMinEL = driver.find_element_by_xpath("//*[@set-option='setBoostDuration']")
    oHourMinEL = driver.find_element_by_xpath("//*[@data-reactid='.3.0']")
    highlight(oHourMinEL)
    click_element_on_position(oHourMinEL, 'Bottom')
    click_element_on_position(oHourMinEL, 'Bottom')
    click_element_on_position(oHourMinEL, 'Bottom')
    click_element_on_position(oHourMinEL, 'Bottom')
    
    
    time.sleep(3)
    print(driver.find_element_by_xpath("//*[@class='hours-minutes']").text)
    
    
    input("ff")
    driver.quit()
    exit()
    
    
    
    oClickElement = driver.find_element_by_xpath("//*[@data-reactid='.0.2.0.0']")
    print(oClickElement.rect)
    highlight(oClickElement)
    action = ActionChains(oClickElement.parent)
    action.move_to_element_with_offset(oClickElement, oClickElement.location['width']/5, oClickElement.location['hieght']/7)
    action.click()
    action.perform()
    time.sleep(0.2)

    input("ff")
    driver.quit()
    exit()
    
    oEl =  driver.find_element_by_xpath("//*[@data-reactid='.0.2.0.1:$=11:0.$=10=2$0:0']")
    #oEl.click()
    #input("ff")
    #oEl =  driver.find_element_by_xpath("//*[@data-reactid='.0.2']")  
    
    #oLEList = driver.find_elements_by_tag_name('noscript')
    
    oLEList =  driver.find_elements_by_xpath("//*[contains(@data-reactid,'.0')]")  
    print(len(oLEList))
    for oel in oLEList:
        if not oel.location['x'] == 0:
            print(oel.get_attribute('data-reactid'), oel.location, oel.is_displayed(), oel.size, oel.rect, oel.text)
            #oel.click()
            #highlight(oel)
            action = ActionChains(driver)
            action.click(oel).perform()
    
    
    driver.quit()
    exit()
    #Get S    tartX int15MinLen
    TimeScaleStartEl = driver.find_element_by_xpath("//*[@data-reactid='.0.0.0.$0']")    
    TimeScaleEndEl = driver.find_element_by_xpath("//*[@data-reactid='.0.0.0.$24']")   
    startX = TimeScaleStartEl.location['x']
    int15MinLen = (TimeScaleEndEl.location['x'] - startX) / (24 * 4)
    
    
    
    #Set Schedule
    
    #Heating Schedule Table
    oSchedTableEl = driver.find_element_by_xpath("//*[@data-reactid='.0.0.1']")  
    oSchedRowElLst = oSchedTableEl.find_elements_by_tag_name('li')
    
    for strDay in oschedDict.keys():
        #strDay = 'fri'
        oSchedList = oschedDict[strDay]
        oSchedRow = get_SchedRow(oSchedRowElLst, strDay)
        highlight(oSchedRow)
        eventLst = oSchedRow.find_elements_by_tag_name('li')    
        strLstEvntStTime = oSchedList[len(oSchedList) - 1][0]
        intLstEvntXPos = startX + (tt.timeStringToMinutes(strLstEvntStTime)/15) * int15MinLen
        print(startX, int15MinLen)
        print(intLstEvntXPos, strLstEvntStTime)
        #First Set all event to Last one
        for intC in range(len(eventLst)-1, 0, -1):
            print(intC)
            evnt = eventLst[intC]
            if not evnt.get_attribute('class') == 'desktop-event-container event-overlap':
                evntTempEl = evnt.find_elements_by_tag_name('div')[0]
                evntDotEl = evnt.find_elements_by_tag_name('div')[1]
            else: evntDotEl = evnt
            highlight(evntDotEl)
            #time.sleep(3)
            offsetX = intLstEvntXPos - evntDotEl.location['x'] 
            #if not float(offsetX) == 0.0:
            print(evntDotEl.location['x'] , offsetX)
            action = ActionChains(driver)
            action.drag_and_drop_by_offset(evntDotEl, offsetX, 5).perform()
            
            #evntTempEl.click()
            evnt.click()
            
        eventLst = oSchedRow.find_elements_by_tag_name('li') 
        for intC in range(0, len(oSchedList)):
            evnt = eventLst[intC+1]
            intCurEvntXPos = startX + (tt.timeStringToMinutes(oSchedList[intC][0])/15) * int15MinLen
            offSetVal = intLstEvntXPos - intCurEvntXPos
            print(intC, offSetVal)
            if not offSetVal == 0.0:
                action = ActionChains(driver)
                action.drag_and_drop_by_offset(evnt, -offSetVal, 5).perform()
                evnt.click()
        time.sleep(2)
        
        eventLst = oSchedRow.find_elements_by_tag_name('li')    
        oNewSchedList = []
        for intC in range(0, len(oSchedList)):
            evntCntr = intC+1
            if intC == len(oSchedList) - 1:
                evntCntr = 6
            fltSetTargTemp = float(oSchedList[intC][1])
            evnt = eventLst[evntCntr]
            if not evnt.get_attribute('class') == 'desktop-event-container event-overlap':
                evntTempEl = evnt.find_elements_by_tag_name('div')[0]
                fltTargTemp = float(evntTempEl.get_attribute('class').split('temp')[1].replace('-', '.'))
                if not fltSetTargTemp == fltTargTemp:
                    evntTempEl.click()
                    time.sleep(1)
                    oTargTempElement = driver.find_elements_by_xpath("//*[@role='spinbutton']")
                    set_target_target_temperature(oTargTempElement[1], fltSetTargTemp)
    
    
    
    
    time.sleep(5)
    driver.find_element_by_xpath("//*[@ng-click='isChanged ? saveNow() : null']" ).click()
    
    
    
    
    
    time.sleep(5)
    driver.quit()
    exit()
    
    #GetSchedule
    oSchedDict = {}
    #Heating Schedule Table
    oSchedTableEl = driver.find_element_by_xpath("//*[@data-reactid='.0.0.1']")  
    oSchedRowElLst = oSchedTableEl.find_elements_by_tag_name('li')
    print(len(oSchedRowElLst))
    intDayIndexCntr = 0
    for oSchedRow in oSchedRowElLst:
        if len(oSchedRow.get_attribute('data-reactid')) == 9:
            strDay = webDayList[intDayIndexCntr]
            
            eventLst = oSchedRow.find_elements_by_tag_name('li')    
            oNewSchedList = []
            for intC in range(1, len(eventLst)):
                evnt = eventLst[intC]
                #print(evnt.get_attribute('class'), evnt.get_attribute('data-reactid'))
                if not evnt.get_attribute('class') == 'desktop-event-container event-overlap':
                    evntTempEl = evnt.find_elements_by_tag_name('div')[0]
                    evntDotEl = evnt.find_elements_by_tag_name('div')[1]
                    #print(evntDotEl.location)
                    noOf15 = (evntDotEl.location['x'] - startX) / int15MinLen
                    #print(noOf15)
                    noOf15 = int(noOf15)
                    hour = noOf15//4
                    min = noOf15 % 4
                    strStartTime = str(hour) + ':' + str(min * 15)
                    fltTargTemp = evntTempEl.get_attribute('class').split('temp')[1].replace('-', '.')
                    oNewSchedList.append((strStartTime, fltTargTemp))
            #print(oNewSchedList)
            oSchedDict[strDay] = oNewSchedList
            intDayIndexCntr += 1
    print(oSchedDict) 
            
            
    driver.quit()
    exit()
    
    
    
    
    
    #timeEl = driver.find_elements_by_xpath("//*[@class='time-scale']" )[1]
    timeEl = driver.find_element_by_xpath("//*[@ng-controller='HotWaterScheduleController as hotWaterScheduler']" )
    #timeEl = driver.find_element_by_xpath("//*[@ng-controller='HeatingScheduleController as heatingScheduler']" )
    print(timeEl.size)
    print(timeEl.location)
    
    
    #oEventTimeElList = timeEl.find_elements_by_xpath("//*[@class='time-scale-label']" )
    
    oEventTimeElList = timeEl.find_elements_by_xpath("//*[contains(@data-reactid,'.0.0.0.$')]" )
    #oEventTimeElList = timeEl.find_elements_by_xpath("//*[contains(@data-reactid,'.0.0')]" )
    
    for el in oEventTimeElList:
        print(el.text, el.location, el.size, el.get_attribute('data-reactid'))
        #highlight(el)
    '''
    litdot = driver.find_element_by_xpath("//*[@data-reactid='.0.0.1.$0.1.0.$1.1']" )
    print(litdot.text, litdot.location, litdot.size)
    '''
    litdot = driver.find_element_by_xpath("//*[@data-reactid='.0.0.1.$1.1.0.$1.1']" )
    print(litdot.text, litdot.location, litdot.size)
    action = ActionChains(driver)
    action.drag_and_drop_by_offset(litdot, 1128, 0).perform()
    time.sleep(3)
    lstEven = driver.find_element_by_xpath("//*[@data-reactid='.0.0.1.$1.1.0.$6.1']" )
    #lstEven.click()
    action = ActionChains(driver)
    action.drag_and_drop_by_offset(lstEven, -1000, 0).perform()
    time.sleep(3)
    driver.find_element_by_xpath("//*[@ng-click='isChanged ? saveNow() : null']" ).click()
    #ng-click="isChanged ? saveNow() : null"
    time.sleep(10)
    
    #driver.quit()
    exit()
    
    ModeGroupElement =  driver.find_element_by_xpath("//*[@active-item='local.mode']")
    strMode = driver.find_element_by_xpath("//*[@active-item='local.mode']").find_element_by_xpath("//*[@class='ng-binding active']" ).text
    print(strMode)
    
    driver.find_element_by_xpath("//*[@active-item='local.mode']").find_element_by_xpath("//*[a='manual']").click()
    ModeGroupElement.find_element_by_link_text('Schedule').click()
    strMode = driver.find_element_by_xpath("//*[@active-item='local.mode']").find_element_by_xpath("//*[@class='ng-binding active']" ).text
    print(strMode)
    time.sleep(5)
    
    
    
    
    
    driver.refresh()
    time.sleep(3)
    
    TargTempEl = driver.find_element_by_xpath("//*[@throbber-throb-for='heating.temperature']")
    set_target_target_temperature(TargTempEl, 21.0)
    
    print(TargTempEl.get_attribute('name'))
    print(TargTempEl.text)
    print(TargTempEl.get_attribute('aria-valuenow'))
    print(TargTempEl.size)
   
    for intCntr in range(0,10):  
        action = ActionChains(driver)
        action.move_to_element_with_offset(TargTempEl, 130, 15)
        action.click()
        action.perform()
        time.sleep(0.2)
    
    print(TargTempEl.get_attribute('aria-valuenow'))
    time.sleep(6)
    
    for intCntr in range(0,10): 
        action = ActionChains(driver)
        action.move_to_element_with_offset(TargTempEl, 130, 195)
        action.click()
        action.perform()
        time.sleep(0.2)
        
    
    print(TargTempEl.get_attribute('aria-valuenow'))
    time.sleep(10)
    driver.quit()
    exit()
    strMode = 'schedule'
    
    lstModeElem = driver.find_element_by_xpath("//*[@active-item='local.mode']").find_element_by_xpath("//*[contains(@aria-label, 'activate " + strMode + "')]")
    lstModeElem.click()
  
    
   
    
    
    print(driver.find_element_by_xpath("//div[@class='content']/div/div/span[contains(@style,'font')]").text)
   
    lstEl = driver.find_element_by_xpath("//*[@throbber-throb-for='heating.temperature']").find_elements_by_tag_name('span')
    #lstEl = driver.find_elements_by_tag_name('div')
    #print(driver.find_element_by_xpath("//*[@throbber-throb-for='heating.temperature']").text())
    #ApTest.setSchedule(wd, oSchedList)
    targTempEl =driver.find_element_by_xpath("//*[@throbber-throb-for='heating.temperature']")
    print(len(lstEl))
    #ApTest.setScrollValue(driver, targTempEl, 20.0, 27.0, 0.5, 2)
    for el in lstEl:
        print(el.text)
        if not el.text == '':
            for intCntr in range(0,5):
                el.click()
                time.sleep(1)
        '''
        #print(el.get_attribute('style'))
        print(el.get_attribute('text'))
        if el.get_attribute('text') =='manual':
            el.click()
        '''
    driver.quit()
    exit()
    driver.find_element_by_name('Manual').click()
    driver.find_element_by_xpath("//*[@text='Manual']" ).click()
    input('click')
    driver.switch_to_default_content()
    driver.switch_to_frame(3)
    driver.find_element_by_name("iframe")
    input('click')
    driver.find_element_by_xpath("//*[button='Save']").click()
    
    driver.switch_to_default_content()
    #frame = driver.find_element_by_tag_name('iframe')
    driver.switch_to_frame('iframe')
    
    driver.find_element_by_css_selector(".targetTemp-container .active .up").click()
    
    '''
    driver.switch_to_frame(0)
    frame = driver.find_element_by_tag_name('iframe')
    driver.switch_to_frame(frame)
    driver.find_element_by_xpath("html/body/div[1]/div[2]/div/section[1]/div/div[1]/div/section[1]/div[1]/div[2]/switch-menu/nav/ul/li[2]/a" ).click()

    #driver.find_element_by_xpath("//*[@data-reactid='.0.0.1.$0.1.0.$1.0']").click()
'''
'''
    oElementList  = driver.find_elements_by_tag_name('div')
    for oElement in oElementList:
        print(oElement.text())
'''
    
def get_firefox_app_data_dir():
    """Return the path to the firefox application data."""
    if platform.system() == "Windows":
        app_data_dir = os.path.join(
            os.getenv("APPDATA"), "Mozilla", "Firefox")
    elif platform.system() == "Darwin":
        app_data_dir = os.path.join(
            os.getenv("HOME"), "Library", "Application Support", "Firefox")
    else: # unix
        home = os.getenv("HOME")
        sudo_user = os.getenv("SUDO_USER")
        user = os.getenv("USER")
        if sudo_user and sudo_user !=  user:
            process = Popen(["getent passwd ${USER} | cut -f6 -d:"], stdout=PIPE, shell=True)
            sudo_home = process.communicate()[0].strip()

            if os.path.exists(sudo_home):
                home = sudo_home

        app_data_dir = os.path.join(home, ".mozilla", "firefox")
'''
def get_profile_ini():
    app_data_dir = get_firefox_app_data_dir()
    profile_ini = ConfigParser.SafeConfigParser()
    profile_ini.read(os.path.join(app_data_dir, "profiles.ini"))
    return profile_ini
''' 
if __name__ == '__main__':
    main()
    
    