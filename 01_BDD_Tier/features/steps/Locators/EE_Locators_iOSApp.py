'''
Created on 16 Jun 2015

@author: ranganathan.veluswamy

@author: Hitesh Sharma - 15 July 2016
@note: class HeatingNotification - Identifier for Heating Notifications screen and updated LoginPageLocators to fix login issue
'''

from selenium.webdriver.common.by import By

class LoginPageLocators(object):
    TITLE_LABEL = (By.XPATH, "//*[@name='Log in'][2]")
    USERNAME_EDTBOX = (By.XPATH, "//*[@label='Email']")
    PASSWORD_EDTBOX = (By.XPATH, "//*[@label='Password']")
    LOGIN_BUTTON = (By.XPATH, "//*[@name='Log in'][2]")
    LOG_OUT_BUTTON = (By.XPATH, "//*[@label='Log out']")
      
class HomePageLocators(object):
    
    CURRENT_TITLE = (By.XPATH, "//*[contains(@label, 'screen')]")
    MENU_BUTTON = (By.NAME, 'Menu')
    ALL_RECIPES = (By.NAME, 'All Recipes')
    MENU_TITLE = (By.NAME, 'Menu, screen')
    GOT_IT_BUTTON = (By.XPATH, "//*[@label='Got it!']")
    HEAT_CONTROL_MENU_LINK = (By.NAME, 'Heating control')
    HEAT_SCHEDULE_MENU_LINK = (By.NAME, 'Heating schedule')
    SETTINGS_MENU_LINK = (By.NAME, 'Settings')
    HOLIDAY_MODE_MENU_LINK = (By.NAME, 'Holiday mode')
    GEOLOCATION_LINK = (By.NAME, 'Geolocation')
    NOTIFICATIONS_MENU_LINK = (By.NAME, 'Notifications')
    ACCOUNT_DETAILS_MENU_LINK = (By.NAME, 'Account details')
    HOT_WATER_CONTROL_MENU_LINK = (By.NAME, 'Hot water control')
    HOT_WATER_SCHEDULE_MENU_LINK = (By.NAME, 'Hot water schedule')
    LINK_COLAPSE_BUTTON = (By.NAME, 'c')
    SETTINGS_MAIN_MENU = (By.NAME, 'Settings')
    CHANGE_PASSWORD_SUB_MENU = (By.NAME, 'Change password') 
    PINLOCK_SUB_MENU =(By.NAME,'PIN lock')
    HELP_SUPPORT_LINK= (By.XPATH,"//*[@value='Help & Support']")
    TEXT_CONTROL_LINK=(By.XPATH,"//*[@value='Text control']")
    PLUG_CONTROL_LINK=(By.NAME,'Plug control')
    PLUG_SCHEDULE_LINK=(By.NAME,'Plug schedule')
    MOTIONSENSOR_ON_LOCATOR = (By.XPATH, "//*[@label='Hall, on']")
    MOTIONSENSOR_OFF_LOCATOR = (By.XPATH, "//*[@label='Hall, off']")
    strLOCAL_ON = "//*[contains(@label,'name, on')]"
    strLOCAL_OFF = "//*[contains(@label,'name, off')]"
    strLOCAL_OFFLINE = "//*[contains(@label,'name, offline')]"
    NOTIFICATION_RECIPE_DEFAULT = "//*[contains(@label,'Notify me when 'name' detects motion')]"
    DEVICE_OFFLINE_LABEL = (By.XPATH, "//*[contains(@label,'Device offline')]")
    FLIP_TO_HONEYCOMB = (By.XPATH, "//*[@label='Flip to honeycomb dashboard']")
    PAGE_NAVIGATOR =(By.XPATH, "//*[contains(@value, 'page 1 of 2')]")
    FLIP_TO_DEVICE_LIST = (By.XPATH, "//*[@label='Flip to list']")

class HeatingControlPageLocators(object):
    TARGET_TEMPERATURE_SCROLL = (By.NAME, 'Temperature control')
    PRESET_TEMP_BUTTON = (By.NAME, 'Switch between the temperature control and temperature presets')
    SCHEDULE_MODE_LINK =  (By.XPATH, "//*[contains(@label, 'Schedule')]")
    MANUAL_MODE_LINK = (By.XPATH, "//*[contains(@label, 'Manual')]")
    OFF_MODE_LINK = (By.XPATH, "//*[contains(@label, 'Off, option 3 of 3,')]")
    BOOST_MODE_LINK = (By.XPATH, "//*[contains(@label, 'Boost')]")
    SELECTED_MODE_LINK = (By.XPATH, "//*[contains(@label, 'selected')]")
    FLAME_ICON = (By.XPATH, "//*[contains(@label, 'Your heating is o')]")
    BOOST_TIME_SCROLL = (By.XPATH, "//UIAScrollView[1]/UIATableView[1]/UIAPickerWheel[1]")
    BOOST_CURRENT_TIME_BUTTON = (By.XPATH, "//UIAButton[contains(@label,'0')][4]")
    BOOST_STOP = (By.NAME, 'Stop boost')
    BOOST_SAVE = (By.NAME, 'Save')
   
class HotWaterControlPageLocators(object):
    RUNNING_STATE_CIRCLE = (By.ID, 'hotWaterCircleView')
    BOOST_MODE_LINK = (By.XPATH, "//*[contains(@label, 'Boost')]")
    SCHEDULE_MODE_LINK = (By.XPATH, "//*[contains(@label, 'Hot water mode Schedule')]")
    MANUAL_MODE_LINK = (By.XPATH, "//*[contains(@label, 'Hot water mode On')]")
    OFF_MODE_LINK = (By.XPATH, "//*[contains(@label, 'Hot water mode Off')]")
    SELECTED_MODE_LINK = (By.XPATH, "//*[contains(@label, 'selected')]")
    HOT_WATER_CURRENT_STATE = (By.XPATH, "//*[contains(@label, 'Hot Water, currently')]")   
    RUNNING_STATE_ON = (By.NAME, 'On')
    RUNNING_STATE_OFF = (By.NAME, 'Off')    
    BOOST_TIME_SCROLL = (By.XPATH, "//UIAScrollView[1]/UIATableView[1]/UIAPickerWheel[1]")
    BOOST_CURRENT_TIME_BUTTON = (By.XPATH, "//*[contains(@name,'0')][1]")
    BOOST_STOP = (By.NAME, 'Stop boost')
    BOOST_SAVE = (By.NAME, 'Save')
    
class SchedulePageLocators(object):
    MON_SCHEDULE_BUTTON = (By.XPATH, "//*[contains(@label, 'Monday')]")
    TUE_SCHEDULE_BUTTON = (By.XPATH, "//*[contains(@label, 'Tuesday')]")
    WED_SCHEDULE_BUTTON = (By.XPATH, "//*[contains(@label, 'Wednesday')]")
    THU_SCHEDULE_BUTTON = (By.XPATH, "//*[contains(@label, 'Thursday')]")
    FRI_SCHEDULE_BUTTON = (By.XPATH, "//*[contains(@label, 'Friday')]")
    SAT_SCHEDULE_BUTTON = (By.XPATH, "//*[contains(@label, 'Saturday')]")
    SUN_SCHEDULE_BUTTON = (By.XPATH, "//*[contains(@label, 'Sunday')]")
    TODAY_SCHEDULE_BUTTON = (By.XPATH, "//*[contains(@label, 'today, selected')]")
    
    EVENT_LABEL = (By.XPATH, "//*[contains(@label, 'target temperature')]")
    EVENT_ARROW = (By.NAME, 'z')
    EVENT_CELL = (By.XPATH, "//UIATableCell[contains(@label, 'until')]")
    SCHEDULE_OPTIONS_BUTTON = (By.NAME, 'Schedule options')
    ADD_TIME_SLOT_SUBMENU = (By.XPATH, "//*[contains(@label, 'Add a time slot')]")

    
class EditTimeSlotPageLocators(object):
    TITLE_LABEL = (By.NAME, 'Edit time slot, screen')
    EVENT_TARGET_TEMPERATURE_SCROLL = (By.NAME, 'Temperature control')
    START_TIME_BUTTON = (By.ID, 'startTime')
    START_TIME_LABEL = (By.XPATH, "//*[contains(@label, 'start time')]")
    HOUR_SCROLL = (By.XPATH, "//*[contains(@value, 'clock')]")
    HOT_WATER_TOGGLE_BUTTON_SCROLL = (By.XPATH, "//*[contains(@label, 'Hot water')]")
    MINUTE_SCROLL = (By.XPATH, "//*[contains(@value, 'minutes')]")
    CANCEL_BUTTON = (By.ID, 'Cancel')
    SAVE_BUTTON = (By.NAME, 'Save')
    DELETE_EVENT_BUTTON = (By.NAME, 'Delete time slot')
    DELETE_CONFIRM_BUTTON = (By.NAME, 'Delete')
    HOT_WATER_TOGGLE_BUTTON = (By.XPATH, "//UIAButton[contains(@name, 'Hot water o')]")
    
    
class ChangePasswordLocators(object):   
    
    OLDPASSWORD_EDTBOX = (By.XPATH,"//UIASecureTextField[@label='Old Password']")
    NEWPASSWORD_EDTBOX = (By.XPATH,"//UIASecureTextField[@label='New Password']")
    RETYPEPASSWORD_EDTBOX = (By.XPATH,"//UIASecureTextField[@label='Retype Password']")
    SAVE_BUTTON =(By.NAME,'Save')
    CURRENT_TITLE = (By.XPATH, "//*[contains(@label, 'screen')]")
    
class PinLockPageLocators(object):
    
    PINLOCK_LINK = (By.NAME,'PIN lock')
    PINLOCK_SETPIN =(By.XPATH,"//UIATableCell[1][@name='PIN lock']")
    PINKEY_ONE =(By.XPATH,"//UIAKey[1][@name='1']")
    PINKEY_TWO =(By.XPATH,"//UIAKey[2][@name='2']")
    PINKEY_THREE =(By.XPATH,"//UIAKey[3][@name='3']")
    PINKEY_FOUR =(By.XPATH,"//UIAKey[4][@name='4]")
    PINSET_ON=(By.XPATH,"//*[@name='On']")
    PINLOCK_CHANGEPIN =(By.XPATH,"//UIATableCell[2][@name='Change PIN']")
    PINLOCK_FORGOTPIN=(By.XPATH,"//UIATableCell[3][@name='Forgot PIN']")
    PINLOCK_LOGOUT=(By.XPATH,"//UIAStaticText[@label='log out']")
    PINLOCK_LOGOUT_OK=(By.XPATH,)
    
class DemoChangePasswordLocators(object):
    
    OLDPASSWORD_EDTBOX = (By.XPATH,"//UIASecureTextField[@label='Old Password']")
    NEWPASSWORD_EDTBOX = (By.XPATH,"//UIASecureTextField[@label='New Password']")
    RETYPEPASSWORD_EDTBOX = (By.XPATH,"//UIASecureTextField[@label='Retype Password']")
    SAVE_BUTTON =(By.NAME,'Save')
    
class DemoHomePageLocators(object):
    
    DEMO_LINK=(By.NAME,'Demo mode')
    CURRENT_TITLE = (By.XPATH, "//*[contains(@label, 'screen')]")
    MENU_BUTTON = (By.NAME, 'Menu')
    MENU_TITLE = (By.NAME, 'Menu, screen')
    GOT_IT_BUTTON = (By.XPATH, "//*[@label='Got it!']")
    HEAT_CONTROL_MENU_LINK = (By.NAME, 'Heating control')
    HEAT_SCHEDULE_MENU_LINK = (By.NAME, 'Heating schedule')
    SETTINGS_MENU_LINK = (By.NAME, 'Settings')
    HOLIDAY_MODE_MENU_LINK = (By.NAME, 'Holiday mode')
    GEOLOCATION_LINK = (By.NAME, 'Geolocation')
    NOTIFICATIONS_MENU_LINK = (By.NAME, 'Notifications')
    ACCOUNT_DETAILS_MENU_LINK = (By.NAME, 'Account details')
    HOT_WATER_CONTROL_MENU_LINK = (By.NAME, 'Hot water control')
    HOT_WATER_SCHEDULE_MENU_LINK = (By.NAME, 'Hot water schedule')
    LINK_COLAPSE_BUTTON = (By.NAME, 'c')
    SETTINGS_MAIN_MENU = (By.NAME, 'Settings')
    CHANGE_PASSWORD_SUB_MENU = (By.NAME, 'Change password') 
    EXIT_DEMO_MODE=(By.NAME,'Exit Demo mode')


class HeatingNotification(object):
    SUB_MENU_HEATING_NOTIFICATION =(By.XPATH, "//*[@name ='Heating notifications'][1]")
    MAX_TEMPRATURE =(By.XPATH, "//*[contains(@label, 'Maximum Temperature')]")
    MAX_TEMPRATURE_NOTSET = (By.XPATH,"//*[contains(@label, 'Maximum Temperature, Not set')]")
    MIN_TEMPRATURE = (By.XPATH, "//*[contains(@label, 'Minimum Temperature')]")
    MIN_TEMPRATURE_NOTSET =(By.XPATH, "//*[contains(@label, 'Minimum Temperature, Not set')]")
    RECEIVE_WARNINGS = (By.XPATH,"//*[contains(@label, 'Receive warnings')]")
    RECEIVE_WARNINGS_ON =(By.XPATH, "//*[@value = '1'][2]")
    RECEIVE_WARNINGS_OFF =(By.XPATH, "//*[@value = '0']")
    BTN_BACK =(By.XPATH, "//*[@label ='Back'][1]")
    SAVE_CHANGES =(By.XPATH, "//*[contains(@label, 'Save Changes')]")
    EMAIL_ME =(By.XPATH, "//*[contains(@label, 'Email when temperature')]")
    EMAIL_ME_OFF =(By.XPATH, "//*[@value = '0']")
    EMAIL_ME_ON =(By.XPATH, "//*[@value = '1']")
    TARGET_TEMPERATURE_SCROLL_HN = (By.NAME, 'Temperature control')
    
class SmartPlugsLocators(object):
    
    PLUG_ON_BUTTON=(By.XPATH,"//*[@name='Plug - now on']")
    PLUG_OFF_BUTTON=(By.XPATH,"//*[@name='Plug - now off']")
    PLUG_BUTTON=(By.XPATH,"//*[contains(@label,'Plug - now')]")
    PLUG_SCHEDULE=(By.XPATH,"//*[contains(@label,'Plug schedule')]")
    TITLE_LABEL = (By.NAME, 'Add holiday, screen')
    TITLE_LABEL = (By.XPATH, "//*[contains(@name, 'Holiday mode, screen')]")
    ACTIVATE_HOLIDAYMODE_BUTTON=(By.NAME,'Activate holiday mode')
    CANCEL_HOLIDAYMODE_BUTTON =(By.XPATH ,"//*[contains(@name,'Cancel holiday mode')]")
    EDIT_HOLIDAYMODE_BUTTON =(By.XPATH,"//*[@label='Edit']")
    CANCEL_HOLIDAYMODE_ALERT=(By.XPATH,"//UIAAlert[@label='Cancel holiday mode']")
    STOP_HOLIDAYMODE_BUTTON =(By.XPATH ,"//*[contains(@name,'Stop holiday mode')]")
    TARGET_TEMPERATURE_SCROLL = (By.NAME, 'Temperature control')
    YES_ALERT_BUTTON=(By.XPATH,"//UIACollectionCell[@name='Yes']")
    SET_DEPARTURE=(By.NAME,'Set departure')
    SET_RETURN=(By.NAME,'Set return')
    DAY_PICKER=(By.XPATH,"(//UIAPicker[@type='UIAPickerWheel])[1]")
    HOUR_PICKER=(By.XPATH,"(//UIAPicker[@type='UIAPickerWheel])[2]")
    MINUTE_PICKER=(By.XPATH,"(//UIAPicker[@type='UIAPickerWheel])[3]")
    DEFAULT_DDAY=(By.XPATH,"//UIATableCell[1]/UIAStaticText[2]")
    DEFAULT_DMONTH_YEAR=(By.XPATH,"//UIATableCell[1]/UIAStaticText[3]")
    DEFAULT_DTIME=(By.XPATH,"//UIATableCell[1]/UIAStaticText[4]")
    DEFAULT_RDAY=(By.XPATH,"//UIATableCell[1]/UIAStaticText[6]")
    DEFAULT_RMONTH_YEAR=(By.XPATH,"//UIATableCell[1]/UIAStaticText[7]")
    DEFAULT_RTIME=(By.XPATH,"//UIATableCell[1]/UIAStaticText[8]")
    DEFAULT_TEMP=(By.XPATH,"//UIATableCell[2]/UIAStaticText[1]")

class MotionSensorPageLocators(object):
    
    TABBAR_CONTROL = (By.NAME, '3')
    TABBAR_RECIPES = (By.NAME, 'm')
    MOTIONSENSOR_TITLE = (By.NAME,'screen')
    MOTION_LABEL = (By.XPATH,"//*[@label='motion']")
    NOMOTION_LABEL = (By.XPATH,"//*[@label='no motion']")
    EVENTLOG_BUTTON= (By.XPATH, "//*[@label='A']")
    CLOSE_LOG_BUTTON = (By.XPATH, "//*[@label='Close']")
    NO_MOTION_LOG = (By.XPATH, "//*[contains(@label,'No motion detected')]")
    INTERRUPTED_MOTION_LOG = (By.XPATH, "//*[contains(@label,'Motion')]")
    CURRENT_MOTION_LOG = (By.XPATH, "//*[contains(@label,'Motion detected')]")
    RECIPE_SCREEN_HEADER = (By.XPATH, "//*[contains(@label,'Here you can set up your recipes to make your home work for you')]")
    SET_RECIPE_BUTTON = (By.XPATH, "//*[@label='z']")
    RECIPE_ALWAYS_ON = (By.XPATH, "//*[contains(@label,'Your notifications are set to always on')]")
    RECIPE_SCHEDULED = (By.XPATH, "//*[contains(@label,'Your notifications are scheduled')]")
    CANCEL_RECIPE = (By.XPATH, "//*[@label='Cancel']")          

    SENSOR_RECIPE = (By.XPATH,"//*[contains(@label,'detects motion')]")
    ADD_RECIPE = (By.XPATH,"//*[contains(@label,'Add a new recipe')]")
    RECIPE_SCREEN_HEADER_NEW = (By.XPATH, "//*[contains(@label,'Select from the recipes below and define which settings and devices you want to connect')]")
    DAY1_LOG = (By.XPATH, "//UIAApplication[1]/UIAWindow[1]/UIAStaticText[16]") #6
    DAY2_LOG = (By.XPATH, "//UIAApplication[1]/UIAWindow[1]/UIAStaticText[18]") #5
    DAY3_LOG = (By.XPATH, "//UIAApplication[1]/UIAWindow[1]/UIAStaticText[20]") #4
    DAY4_LOG = (By.XPATH, "//UIAApplication[1]/UIAWindow[1]/UIAStaticText[22]") #3
    DAY5_LOG = (By.XPATH, "//UIAApplication[1]/UIAWindow[1]/UIAStaticText[24]") #2
    DAY6_LOG = (By.XPATH, "//UIAApplication[1]/UIAWindow[1]/UIAStaticText[26]") #1
    DAY7_LOG = (By.XPATH, "//UIAApplication[1]/UIAWindow[1]/UIAStaticText[28]")


class TextControlLocators(object):   
    
    ADD_NEW_USER_LINK = (By.XPATH,"//UIATableCell[contains(@label,'User, Add a new user,')]")  
    NAME_EDTBOX = (By.XPATH,"//*[@value='Name']")
    MOBILE_EDTBOX = (By.XPATH,"//*[@value='Mobile']")
    SAVE_BUTTON =(By.XPATH,"//*[@label='Save']")   
    DELETE_BUTTON=(By.NAME,'Delete')
    USER_TABLE=(By.XPATH,"//UIAWindow[2]/UIATableView[1]")
    CLEAR_TEXT_BUTTON=(By.NAME,'Clear text')
    ERROR_MESSAGE=(By.XPATH,"//UIATableView[1]/UIATableCell[1]")
    
class DashboardPageLocators(object):
    
    DEVICE_LIST_BUTTON=(By.XPATH,"//*[@name='Flip to list']")
    HOT_WATER_CONTROL_DASHBOARD=(By.XPATH,"//*[contains(@label,'Hot water')]")
    HEAT_CONTROL_DASHBOARD=(By.XPATH,"//*[contains(@label,'Heating')]")
    HONEYCOMB_DASHBOARD_BUTTON=(By.XPATH,"//*[@name='Flip to honeycomb dashboard']") 
    TAB_BAR_CONTROL_BUTTON=(By.XPATH,"//*[@name='3']")
    TAB_BAR_SCHEDULE_BUTTON=(By.XPATH,"//*[@name='1']")
    TAB_BAR_RECIPES_BUTTON=(By.XPATH,"//*[@name='m']")

class DashboardTutorialPageLocators(object):
    
    RHCDASHBOARD_IMAGE=(By.XPATH,"//*[@name='rhc_dashboard']")
    NEXT_BUTTON = (By.XPATH, "//*[@name='next']")
    TAP_GOTO_DEVICE = (By.XPATH,"//*[@name ='Tap to go to your device']")
    TAP_GOTO_DEVICE_LIST = (By.XPATH,"//*[@name ='Tap to view all your devices in a list']")
    TAP_MENU = (By.XPATH,"//*[@name ='Tap to get to your menu']")
    DONE_BTN =(By.XPATH,"//*[@name ='done']")
    
class HolidayModePageLocators(object):
  
    TITLE_LABEL = (By.XPATH, "//*[contains(@name, 'Holiday mode, screen')]")
    ACTIVATE_HOLIDAYMODE_BUTTON=(By.NAME,'Activate holiday mode')
    CANCEL_HOLIDAYMODE_BUTTON =(By.XPATH ,"//*[contains(@name,'Cancel holiday mode')]")
    EDIT_HOLIDAYMODE_BUTTON =(By.XPATH,"//*[@label='Edit']")
    CANCEL_HOLIDAYMODE_ALERT=(By.XPATH,"//UIAAlert[@label='Cancel holiday mode']")
    STOP_HOLIDAYMODE_BUTTON =(By.XPATH ,"//*[contains(@name,'Stop holiday mode')]")
    TARGET_TEMPERATURE_SCROLL = (By.NAME, 'Temperature control')
    YES_ALERT_BUTTON=(By.XPATH,"//UIACollectionCell[@name='Yes']")
    SET_DEPARTURE=(By.NAME,'Set departure')
    SET_RETURN=(By.NAME,'Set return')
    DAY_PICKER=(By.XPATH,"(//UIAPicker[@type='UIAPickerWheel])[1]")
    HOUR_PICKER=(By.XPATH,"(//UIAPicker[@type='UIAPickerWheel])[2]")
    MINUTE_PICKER=(By.XPATH,"(//UIAPicker[@type='UIAPickerWheel])[3]")
    DEFAULT_DDAY=(By.XPATH,"//UIATableCell[1]/UIAStaticText[2]")
    DEFAULT_DMONTH_YEAR=(By.XPATH,"//UIATableCell[1]/UIAStaticText[3]")
    DEFAULT_DTIME=(By.XPATH,"//UIATableCell[1]/UIAStaticText[4]")
    DEFAULT_RDAY=(By.XPATH,"//UIATableCell[1]/UIAStaticText[6]")
    DEFAULT_RMONTH_YEAR=(By.XPATH,"//UIATableCell[1]/UIAStaticText[7]")
    DEFAULT_RTIME=(By.XPATH,"//UIATableCell[1]/UIAStaticText[8]")
    DEFAULT_TEMP=(By.XPATH,"//UIATableCell[2]/UIAStaticText[1]")
    
class ContactSensorLocators(object):
    CS_STATUS_OPEN =(By.XPATH, "//*[@label='open']")
    CS_STATUS_CLOSED =(By.XPATH, "//*[@label='closed']")
    LOGS = (By.XPATH, "//*[@label='A']")
    OPEN_ALL_DAY= (By.XPATH, "//*[contains(@label,'Open all day')]")
    OPEN_MUTLIPE_LOG = (By.XPATH, "//*[contains(@label,'Open')]")
    OPEN_CURRENT_LOG = (By.XPATH, "//*[contains(@label,'Opened')]")

class RecipeScreenLocators(object):
    REMOVE_RECIPE = (By.XPATH, "//*[contains(@label,'Remove recipe')]")
    RECIPE_SCREEN_HEADER = (By.XPATH, "//*[contains(@label,'Here you can set up your recipes to make your home work for you')]")
    ADD_RECIPE = (By.XPATH,"//*[contains(@label,'Add a new recipe')]")
    ADD_A_NEW_RECIPE = (By.XPATH, "//*[contains(@label,'Select from the recipes below and define which settings and devices you want to connect')]")
    CANCEL_BUTTON = (By.XPATH, "//*[@label='Cancel']") 
    REMOVE_RECIPE = (By.XPATH, "//*[@label='Remove recipe']") 
    REMOVE_POPUP = (By.XPATH, "//*[@label='Remove']")
    MS_RECIPE = (By.XPATH,"//*[contains(@label,'detects motion')]")
    CSO_RECIPE = (By.XPATH,"//*[contains(@label,'is opened')]")
    CSC_RECIPE = (By.XPATH,"//*[contains(@label,'is closed')]")   
    MENU_BUTTON = (By.NAME, 'Close menu')  
    NOTIFICATION_RECIPE = (By.XPATH,"//*[contains(@label,'Notify me')]")
    TYPE_OF_NOTIFICATION = (By.XPATH,"//*[contains(@label,'Notify me By')]")
    THEN_EXIST = (By.XPATH,"//*[contains(@label,'By')]")
    THEN_NOTIFICATION = (By.XPATH,"//*[contains(@label,'Notify me by')]")
    THEN_DONE = (By.XPATH, "//*[@label='Done']") 
    SAVE_BUTTON = (By.NAME, 'Save')
    
    #Recipe Template objects
    MS_NOT_RECIPE = (By.XPATH,"//*[contains(@label,'Notify me when a motion sensor detects motion')]")
    CSO_NOT_RECIPE = (By.XPATH,"//*[contains(@label,'Notify me when a window or door sensor is opened')]")
    CSC_NOT_RECIPE = (By.XPATH,"//*[contains(@label,'Notify me when a window or door sensor is closed')]")
    MS_PL_RECIPE = (By.XPATH,"//*[contains(@label,'Turn a plug ON or OFF when a motion sensor detects motion')]")
    CSO_PL_RECIPE = (By.XPATH,"//*[contains(@label,'Turn a plug ON or OFF when a window or door sensor is opened')]")
    CSC_PL_RECIPE = (By.XPATH,"//*[contains(@label,'Turn a plug ON or OFF when a window or door sensor is closed')]")
    MS_BU_RECIPE = (By.XPATH,"//*[contains(@label,'Turn a light ON or OFF when a motion sensor detects motion')]")
    CSO_BU_RECIPE = (By.XPATH,"//*[contains(@label,'Turn a light ON or OFF when a window or door sensor is opened')]")
    CSC_BU_RECIPE = (By.XPATH,"//*[contains(@label,'Turn a light ON or OFF when a window or door sensor is closed')]")
    NOTIFICATION_PICKER = (By.XPATH,"//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[5]/UIAPicker[1]/UIAPickerWheel[1]")

class BulbScreenLocators(object):
    BULB_TONE = (By.XPATH,"//*[contains(@label,'Bulb tone')]")
    BULB_COLOUR = (By.XPATH,"//*[contains(@label,'Bulb colour')]")
    BULB_BRIGHTNESS = (By.XPATH,"//*[contains(@label,'Bulb brightness')]")
    BULB = (By.NAME, 'Bulb')
    
    TONE_BUTTON = (By.NAME, 'white')
    COLOUR_BUTTON = (By.NAME, 'colour')
    DIMMER_BUTTON = (By.NAME, 'dimmer')

    
    
    