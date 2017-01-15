'''
Created on 17 Jun 2015

@author: ranganathan.veluswamy
'''

from selenium.webdriver.common.by import By

class LoginPageLocators(object):
    TITLE_LABEL = (By.XPATH, "//*[@name='loginForm']" )
    USERNAME_EDTBOX = (By.ID, 'username')
    PASSWORD_EDTBOX = (By.ID, 'password')
    LOGIN_BUTTON = (By.XPATH, "//*[@type='submit']" )
    FORGOTTEN_PASSWORD_LINK = (By.PARTIAL_LINK_TEXT, 'Forgot your password' )
    
class HeatingPageLocators(object):
    TITLE_LABEL = (By.XPATH, "//*[@name='loginForm']" )
    MY_HIVE_LINK = (By.LINK_TEXT, 'My Hive')
    MY_HIVE_MENU = (By.XPATH,"//*[@data-icon='b']")
    MY_HIVE_LINK_UNDER_MENU = (By.XPATH,"//*[@href='/dashboard']")
    USERNAME_DISPLAY = (By.XPATH,"//*[@ng-if='identity.name']")
    HEAT_MODE_GROUP = (By.XPATH, "//*[@active-item='local.mode']")
    CURRENT_MODE_ITEM = (By.XPATH, "//*[@class='ng-binding active']" )
    SCHEDULE_MODE_LINK = (By.LINK_TEXT, 'Schedule')
    MANUAL_MODE_LINK = (By.LINK_TEXT, 'Manual')
    OFF_MODE_LINK =  (By.LINK_TEXT, 'Off')
    BOOST_MODE_LINK =  (By.XPATH, "//*[@class='boost-on']")
    STOP_BOOST_BUTTON = (By.XPATH, "//*[@class='boost-off']")
    BOOST_TIME_LABE = (By.XPATH, "//*[@class='hours-minutes']")
    SET_BOOST_SCROLL = (By.XPATH, "//*[@data-reactid='.3.0']")
    TARGET_TEMPERATURE_SCROLL = (By.XPATH, "//*[@throbber-throb-for='heating.temperature']")
    
    SCHEDULE_TARGET_TEMPERATURE_SCROLL = (By.XPATH, "//*[@role='spinbutton']")
    SCHEDULE_TARGET_TEMPERATURE_SCROLLV6 = (By.XPATH, "//*[@ng-model='currentTemp']")
    TIME_SCALE_FIRST = (By.XPATH, "//*[@data-reactid='.0.0.0.$0']")
    TIME_SCALE_LAST = (By.XPATH, "//*[@data-reactid='.0.0.0.$24']")
    HEATING_SCHEDULE_TABLE = (By.XPATH, "//*[@data-reactid='.1.2.0.0']//*[canvas[4]]")
    HEATING_SCHEDULE_MAIN = (By.XPATH, "//*[@data-reactid='.1.2.0.0']//*[canvas[4]]")
    SAVE_BUTTON = (By.XPATH, "//*[@ng-click='isChanged ? saveNow() : null']")
    SAVE_BUTTONV6 = (By.XPATH, "//*[@data-reactid='.1.3.1']")
    RUNNING_STATE_FLAME_ICON = (By.XPATH, "//*[@ng-show='flameOn']")
    
    
class HotWaterPageLocators(object):
    TITLE_LABEL = (By.XPATH, "//*[@name='loginForm']" )
    HOT_WATER_MODE_GROUP = (By.XPATH, "//*[@active-item='hotwater.mode']")
    
    CURRENT_MODE_ITEM = (By.XPATH, ".//*[@class='ng-binding active']" )
    SCHEDULE_MODE_LINK = (By.LINK_TEXT, 'Schedule')
    MANUAL_MODE_LINK = (By.LINK_TEXT, 'On')
    OFF_MODE_LINK =  (By.LINK_TEXT, 'Off')
    BOOST_MODE_LINK =  (By.XPATH, "//*[@ng-controller='HotWaterControlController as hotWaterController']//*[@class='boost-on']")
    STOP_BOOST_BUTTON = (By.XPATH, "//*[@ng-controller='HotWaterControlController as hotWaterController']//*[@class='boost-off']")
    BOOST_TIME_LABE = (By.XPATH, "//*[@class='hours-minutes']")
    SET_BOOST_SCROLL = (By.XPATH, "//*[@data-reactid='.3.0']")
    #BOOST_MODE_LINK =  (By.LINK_TEXT, 'BOOST')
    HOT_WATER_SCHEDULE_TABLE = (By.XPATH, "//*[@data-reactid='.1.0.1']")
    HOT_WATER_SCHEDULE_MAIN = (By.XPATH, "//*[@data-reactid='.3.2.0.0']//*[canvas[4]]")
    SAVE_BUTTON = (By.XPATH, "//*[@ng-click='isChanged ? saveNow() : null']")
    SAVE_BUTTONV6 = (By.XPATH, "//*[@data-reactid='.3.3.1']")
    HOT_WATER_SWITCH = (By.XPATH, "//*[@class='hot-water-switch']")
    HOT_WATER_MODE_MENU = (By.XPATH, "//*[@active-item='hotwater.mode']")
    HOT_WATER_SCHEDULE_GROUP = (By.XPATH, "//*[@ng-controller='HotWaterScheduleController as hotWaterScheduler']")
    HOT_WATER_CONTROLER_GROUP = (By.XPATH, "//*[@ng-controller='HotWaterControlController as hotWaterController']")
    HOT_WATER_RUNNING_STATE = (By.XPATH, "//*[contains(@class,'hot-water-off')]")

class ForgottenPasswordPageLocators(object):
    TITLE_LABEL = (By.XPATH, "//*[@ng-controller='ForgottenPasswordController']")
    EMAIL_ADDR_FIELD = (By.XPATH, "//input[@name='email']")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(.,'Submit')]")
    REMINDER_MESSAGE=(By.XPATH, "//*[@ng-bind-html='message']")
    YOPMAIL_EMAIL_ADDR_FIELD = (By.ID, "login")
    YOPMAIL_CHECK_INBOX = (By.XPATH, "//input[@title='Check inbox @yopmail.com']")
    YOPMAIL_HREF_LINK = (By.LINK_TEXT, 'here')
    PASSWORD_RESET_LABEL = (By.XPATH,"//*[@ng-controller='ResetPasswordController']")
    SUCCESS_MESSAGE = (By.XPATH, '//p[contains(.,"Your password has been updated successfully, you may now login.")]')
    NEW_PASSWORD = (By.ID, "password")
    CONFIRM_PASSWORD = (By.ID, "password2")
    LOGIN_BUTTON = (By.XPATH, '//a[@href="/login"]')
    FRAME_REF=(By.ID,"ifmail")
    
class HeatingDashboardLocators(object):
    SETTINGS_MENU = (By.XPATH, "//*[@data-icon='i']")
    LOGOUT_LINK = (By.XPATH, "//a[@href='/logout']")
    NOTIFICATION_LINK = (By.XPATH, "//a[@href='/notifications']")
    
class HeatingNotificationLocators(object):
    TITLE_LABEL = (By.XPATH,'//*[@ng-controller="NotificationsController"]//h2')
    HIGH_TEMP_CHKBOX = (By.XPATH, '//input[@name="aboveActive"]')
    HIGH_TEMP_TT = (By.XPATH, '//*[@name="above"]')
    LOW_TEMP_CHKBOX = (By.XPATH, '//input[@name="belowActive"]')
    LOW_TEMP_TT = (By.XPATH, '//*[@name="below"]')
    WARNINGS_CHKBOX = (By.XPATH, '//*[@ng-model="formData.warningsEmail"]')
    SAVE_BUTTON = (By.XPATH, '//button[contains(.,"Save")]')
    
class DashboardLocators(object):
    HEATING_THUMBNAIL = (By.XPATH,'//*[@class="product heating text-center"]')
    HEATING_THUMBNAIL_OFFLINE = (By.XPATH, '//*[@class="product heating text-center offl"]')
    HOTWATER_THUMBNAIL = (By.XPATH,'//*[@class="product hotwater text-center"]')
    HOTWATER_THUMBNAIL_OFFLINE = (By.XPATH, '//*[@class="product hotwater text-center offl"]')
    ACTIVEPLUG_THUMBNAIL = (By.XPATH, '//*[@class="product activeplug text-center"]')
    WARMWHITE_THUMBNAIL = (By.XPATH,'//*[@class="product activelight text-center"]')

    
    
