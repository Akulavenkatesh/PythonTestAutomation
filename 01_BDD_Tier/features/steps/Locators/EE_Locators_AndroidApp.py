'''
Created on 16 Jun 2015

@author: ranganathan.veluswamy
'''

from selenium.webdriver.common.by import By

class LoginPageLocators(object):
    TITLE_LABEL = (By.ID, 'title')
    USERNAME_EDTBOX = (By.ID, 'login_edit_username')
    PASSWORD_EDTBOX = (By.ID, 'login_edit_password')
    LOGIN_BUTTON = (By.ID, 'login_btn_submit')
    

class HomePageLocators(object):
    SKIP_BUTTON = (By.ID, 'textBtn')
    CURRENT_TITLE = (By.ID, 'title')
    MENU_BUTTON = (By.NAME, 'Menu button, double tap to open menu')
    MENU_BUTTON_V6 = (By.ID, 'full_product_menu_button_hide')
    MENU_BUTTON_SHOW=(By.ID,'full_product_menu_button_show')    
    HOME_MENU_SCREEN_V6 = (By.XPATH, "//*[@text='Home']")
    HEAT_WATER_MAIN_MENU = (By.ID,'icon')
    HEAT_WATER_MAIN_MENU_ICON = (By.XPATH, "//*[@text='c']")
    
    HEAT_WATER_MAIN_MENU_ARROW_UP = (By.XPATH, "//*[@text='j']")
    HEAT_WATER_MAIN_MENU_ARROW_DOWN = (By.XPATH, "//*[@text='k']")
   
    
    
    
    HEATING_SUBMENU = (By.XPATH, "//*[@text='Heating']")
    HOT_WATER_SUBMENU = (By.XPATH, "//*[@text='Hot water']")
    REFRESH_BUTTON = (By.NAME, 'Refresh button')
    REFRESH_BUTTON_V6 = (By.ID, 'refresh_button')
   
    SETTINGS_MAIN_MENU = (By.XPATH,"//*[@text='Settings']")
    ACCOUNT_SUB_MENU = (By.XPATH,"//*[@text='Account details']")
    HOLIDAY_SUB_MENU = (By.XPATH,"//*[@text='Holiday Mode']")
    CHANGE_PASSWORD_SUBMENU=(By.XPATH,"//*[@text='Change password']")
    HELP_SUPPORT_SUBMENU=(By.XPATH,"//*[@text='Help & Support']")
    
class HeatingHomePageLocators(object):
    TITLE_LABEL = (By.NAME, 'Heating')
    TITLE_LABEL1=(By.XPATH,"//[contains(text(),'Heating')]")
    
    REFRESH_BUTTON = (By.NAME, 'Refresh button')
    HEAT_CONTROL_TAB = (By.XPATH,"//*[@text='Control']")
    HEAT_SCHEDULE_TAB = (By.XPATH,"//*[@text='Schedule']")
    
class ChangePasswordLocators(object):

    

    OLD_PASSWORD_EDITTEXT=(By.ID,'oldPassword')

    NEW_PASSWORD_EDITTEXT=(By.ID,'newPassword')

    CONF_PASSWORD_EDITTEXT=(By.ID,'repeatPassword')

    SAVE_PASSWORD=(By.ID,'positiveBtn')
    
    
    
class PinLock(object):
    PINLOCK_SUB_MENU=(By.XPATH, "//*[@text='Pin lock']")
    PINLOCK_STATUS_OFF=(By.ID,'on_off_switch')
    PINLOCK_STATUS_ON=(By.XPATH, "//*[contains(@content-desc,'Pin Lock  is currently ON. Double tap to change.')]")
    PINLOCK_CHANGE_PIN=(By.XPATH, "//*[@text='Change PIN']")
    PINLOCK_FORGOT_PIN=(By.XPATH, "//*[@text='Forgotten pin']")
    PINLOCK_CANCEL=(By.XPATH, "//*[@text='Cancel']")
    ENTER_CURRENT_PIN_CHANGE=(By.ID,'pin_text_0')
    ENTER_NEW_PIN_CHANGE=(By.ID,'pin_text_1')
    CONFIRM_NEW_PIN_CHANGE=(By.ID,'pin_text_2')
    SAVE_CHANGE_PIN=(By.XPATH, "//*[@text='Save']")
    CANCEL_CHANGE_PIN=(By.XPATH, "//*[@text='Cancel']")
    ENTER_REMOVE_PIN=(By.XPATH, "//*[contains(@content-desc,'Enter PIN')]")
    SAVE_REMOVE_PIN=(By.XPATH, "//*[@text='Save']")
    PIN_TITLE=(By.XPATH, "//*[@text='PIN Lock']")
    ENTER_NEW_PIN=(By.XPATH, "//*[contains(@content-desc,'Enter PIN')]")
    REENTER_NEW_PIN=(By.ID,'pin_text_1')
    SAVE_NEW_PIN=(By.XPATH, "//*[@text='Save']")
    PINLOCK_LOGOUT= (By.ID,'text_information_view')
    
    
    
    
    
class TextControlLocators(object):
    ADD_NEW_USER_LINK=(By.ID,'plusSign')
    NAME_EDTBOX=(By.ID,'usernameEditText')
    MOBILE_EDTBOX=(By.ID,'numberEditText')
    SAVE_BUTTON=(By.ID,'positiveBtn')
    TEXTCONTROL_SUBMENU = (By.XPATH, "//*[@text='Text control']")
    
    

    
class LogoutLocators(object):
    LOGOUT_OPTION=(By.XPATH,"//*[@text='Logout']")

    
    
class HotWaterHomePageLocators(object):
    TITLE_LABEL = (By.XPATH, "//*[@text='Hot water']")
    REFRESH_BUTTON = (By.NAME, 'Refresh button')
    HOT_WATER_CONTROL_TAB = (By.XPATH,"//*[@text='Control']")
    HOT_WATER_SCHEDULE_TAB = (By.XPATH,"//*[@text='Schedule']")
    

class HoneycombDasbordLocators(object):
    HONEYCOMB_SHOW_DASHBOARD=(By.ID, 'btnGetStarted')
    HONEYCOMB_HOTWATER_ON=(By.XPATH, "//*[@text='l']")
    HONEYCOMB_HOTWATER_OFF=(By.XPATH, "//*[@text='k']")
    HONEYCOMB_HEATING_ON=(By.XPATH, "//*[@text='j']")
    HONEYCOMB_HEATING_OFF=(By.XPATH, "//*[@text='i']")
    HONEYCOMB_PLUG_ICON_OFF=(By.XPATH, "//*[@text='o']")
    HONEYCOMB_PLUG_ICON_ON=(By.XPATH, "//*[@text='p']")
    HONEYCOMB_MOTION_OFF=(By.XPATH, "//*[@text='q']")
    HONEYCOMB_MOTION_ON=(By.XPATH, "//*[@text='r']")
    HONEYCOMB_MOTION_SENSOR=(By.XPATH, "//*[@text='Motion Sensor']")
    HONEYCOMB_WINDOW_SENSOR=(By.XPATH, "//*[@text='Win/door sensor']")
    HONEYCOMB_DEVICE_OFFLINE=(By.XPATH, "//*[@text='Device offline!']")
    DEVICE_TODAYS_LOGS=(By.ID, "logButton")
    DEVICE_TODAYS_LOGS_CLOSE=(By.ID, "full_product_menu_button_close")
    HONEYCOMB_MOTION_SENSOR_1=(By.XPATH, "//*[@text='Motion Sensor1']")
    
    
    HONEYCOMB_LIGHT_ON=(By.XPATH, "//*[@text='v']")
    HONEYCOMB_LIGHT_OFF=(By.XPATH, "//*[@text='u']")
    HONEYCOMB_WINDOW_OFF=(By.XPATH, "//*[@text='s']")
    HONEYCOMB_WINDOW_ON=(By.XPATH, "//*[@text='t']")
    HONEYCOMB_INTRO=(By.XPATH, "//*[@text='Show me my dashboard']")
    HONEY_DASHBOARD_HOME_BUTTON=(By.ID, "dashboardHomeButton")
    DASHBOARD_VIEWFLIPPER=(By.ID, "dashboardViewFlipperButtonContainer")
    HONEY_DASHBOARD_TITLE=(By.XPATH, "//*[@text='Dashboard']")
    
    
class MotionSensorLocators(object):
    NO_MOTION_CURRENTLY = (By.XPATH, "//*[@text='No Motion']")

    MOTION_DETECTED= (By.XPATH, "//*[@text='Motion']")
   
    
class ActivePlugLocator(object):
    PLUG_STATUS=(By.XPATH, "//*[@text='on']")
    PLUG_STATUS=(By.XPATH, "//*[@text='off']")
    PLUG_MODE=(By.ID, 'button_mode_status')
    PLUG_MODE_RIGHT_ARROW=(By.ID, 'button_mode_right')
    PLUG_MODECHANGE_RIGHT=(By.ID, "dashboardHomeButton")
    PLUG_CONTROL_TAB=(By.XPATH, "//*[contains(@content-desc,'Control tab.')]")
    PLUG_SCHEDULE_TAB=(By.XPATH, "//*[contains(@content-desc,'Schedule tab.')]")
    PLUG_SCHEDULE_STATUS=(By.XPATH, "//*[@text='Schedule active']")
    



    
class ActiveplugControlPageLocators(object):
    PLUG_ICON_ON=(By.XPATH, "//*[@text='p']")
    PLUG_ICON_OFF=(By.XPATH, "//*[@text='o']")

class HeatingControlPageLocators(object):
    TARGET_TEMPERATURE_SCROLL = (By.ID, 'heatingControlTempControlView')
    PRESET_TEMP_BUTTON = (By.NAME, 'Preset temperature button')
    SCHEDULE_MODE_LINK = (By.XPATH, "//*[@text='Schedule']")
    MANUAL_MODE_LINK = (By.XPATH, "//*[@text='Manual']")
    OFF_MODE_LINK = (By.XPATH, "//*[@text='Off']")
    OFF_MODE_LINK_V6 = (By.XPATH, "//*[contains(@content-desc,'heating Off mode')]" )
    SELECTED_MODE_LINK = (By.XPATH, "//*[contains(@content-desc,'currently active')]")
    FLAME_ICON = (By.ID, "flame")
    BOOST_FLAME_ICON = (By.ID, "boost_flame")
    
    
    BOOST_MODE_LINK = (By.XPATH, "//*[@text='Boost']")
    BOOST_MODE_LINK_V6 = (By.ID, "heating_boost")
    BOOST_STOP_BUTTON = (By.ID, "boost_btn_stop")
    BOOST_TIMER = (By.ID, 'boost_timer')
    BOOST_CURRENT_HOUR = (By.ID, "boost_timer_hour")
    BOOST_CURRENT_MINUTE = (By.ID, "boost_timer_mins")
    BOOST_CURRENT_SECOND = (By.ID, "boost_timer_secs")
    BOOST_TEMP_SCROLL = (By.ID, "heatingControlTempControlView")

class EditBoostTimePageLocators(object):
    EDIT_BOOST_TIME_SCREEN = (By.XPATH, "//*[@text='Edit Boost Time']")
    BOOST_TIME_SCROLL = (By.ID, 'boostTimeIntervalList')
    NUMBER_INSDE_SCROLL_ITEM = (By.ID, 'numberpicker_input')
    CANCEL_BUTTON = (By.XPATH, "//*[@text='Cancel']")
    SAVE_BUTTON = (By.XPATH, "//*[@text='Save']")

class HotWaterControlPageLocators(object):
    RUNNING_STATE_CIRCLE = (By.ID, 'hotWaterCircleView')
    RUNNING_STATE_CIRCLE_V6 = (By.ID, 'hotWaterImage')
    SCHEDULE_MODE_LINK = (By.XPATH, "//*[@text='Schedule']")
    MANUAL_MODE_LINK = (By.XPATH, "//*[@text='On']")
    OFF_MODE_LINK = (By.XPATH, "//*[@text='Off']")
    BOOST_ACTIVE = (By.ID, 'hwText')
    SELECTED_MODE_LINK = (By.XPATH, "//*[contains(@content-desc,'currently active')]")
    BOOST_MODE_LINK = (By.XPATH, "//*[@text='Boost']")
    BOOST_MODE_LINK_V6 = (By.ID, "hot_water_boost")
    BOOST_STOP_BUTTON = (By.ID, "boost_btn_stop")
    BOOST_TIMER = (By.ID, 'boost_timer')
    BOOST_CURRENT_HOUR = (By.ID, "boost_timer_hour")
    BOOST_CURRENT_MINUTE = (By.ID, "boost_timer_mins")
    BOOST_CURRENT_SECOND = (By.ID, "boost_timer_secs")
    
class SchedulePageLocators(object):
    MON_SCHEDULE_BUTTON = (By.ID, 'mon_single_weekday')
    TUE_SCHEDULE_BUTTON = (By.ID, 'tue_single_weekday')
    WED_SCHEDULE_BUTTON = (By.ID, 'wed_single_weekday')
    THU_SCHEDULE_BUTTON = (By.ID, 'thu_single_weekday')
    FRI_SCHEDULE_BUTTON = (By.ID, 'fri_single_weekday')
    SAT_SCHEDULE_BUTTON = (By.ID, 'sat_single_weekday')
    SUN_SCHEDULE_BUTTON = (By.ID, 'sun_single_weekday')
    
    START_TIME_LABEL = (By.ID, 'textViewFromTime')
    EVENT_OPTIONS_BUTTON = (By.NAME, 'More options' )
    DELETE_EVENT_SUBMENU = (By.XPATH, "//*[@text='Delete']")
    EDIT_TIME_SLOT_SUBMENU = (By.XPATH, "//*[@text='Edit time slot']")
    SCHEDULE_OPTIONS_BUTTON = (By.ID, 'schedule_fab')
    #ADD_TIME_SLOT_SUBMENU = (By.ID, 'add_a_time_slot')
    ADD_TIME_SLOT_SUBMENU = (By.XPATH, "//*[@text='Add a time slot']")
    SCHEDULE_SPINNER_MENU = (By.ID, 'schedule_spinner')
    SIX_EVENT_SUBMENU = (By.XPATH, "//*[@text='6 time slot schedule']")
    FOUR_EVENT_SUBMENU = (By.XPATH, "//*[@text='4 time slot schedule']")
   
class EditTimeSlotPageLocators(object):
    HEATING_TITLE_LABEL = (By.NAME, 'Edit event for Heating Schedule')
    HOT_WATER_TITLE_LABEL = (By.NAME, 'Edit event for Hot Water Schedule')
    EVENT_TARGET_TEMPERATURE_SCROLL = (By.ID, 'editHeatingScheduleTempControlView')
    HOT_WATER_TOGGLE_BUTTON = (By.ID, 'edit_schedule_item_hot_water_toggle_button')
    START_TIME_BUTTON = (By.ID, 'startTime')
    HOUR_SCROLL = (By.ID, 'hour')
    NUMBER_INSDE_SCROLL_ITEM = (By.ID, 'numberpicker_input')
    MINUTE_SCROLL = (By.ID, 'minute')
    CANCEL_BUTTON = (By.XPATH, "//*[@text='Cancel']")
    #SAVE_BUTTON = (By.ID, 'button_save')
    SAVE_BUTTON = (By.XPATH, "//*[@text='Save']")
    ADD_BUTTON = (By.XPATH, "//*[@text='Save']")
    ADD_BUTTON_V6 = (By.XPATH, "//*[@text='Add']")
    
class AccountDetailsLocators(object):
    SETTINGS_MAIN_MENU = (By.XPATH,"//*[@text='Settings']")
    ACCOUNT_SUB_MENU = (By.XPATH,"//*[@text='Account details']")
    
    
class HolidayModeLocators(object):
    START_DATE_TIME = (By.ID,'button_holiday_mode_departure')
    END_DATE_TIME = (By.ID,'button_holiday_mode_return')
    ACTIVATE_HOLIDAY_BUTTON = (By.ID,'button_start_holiday_mode')
    TITLE = (By.ID,'title')
    DEPARTURE_SAVE = (By.ID,'positiveBtn')
    DEPARTURE_MONTH_YEAR = (By.ID,'calendar_month_year_textview')
    DEPARTURE_ADD_MONTH = (By.ID,'calendar_right_arrow')
    DEPARTURE_DEL_MONTH = (By.ID,'calendar_left_arrow')
    DEPARTURE_DATES = (By.XPATH,"//*[@Id = 'calendar_tv' AND @text='CHANGE']")
    DEPARTURE_DEL_MONTH = (By.ID,'calendar_left_arrow')
    DEPARTURE_TIME = (By.ID,'edit_holiday_mode_set_departure_time')
    ARRIVAL_TIME = (By.ID,'edit_holiday_mode_set_return_time')
    TARGET_TEMPERATURE = (By.ID,'tempControlView')
    DEPARTURE_DATE = (By.ID,'holiday_mode_status_data_day_of_month')
    ARRIVAL_DATE = (By.ID,'edit_holiday_mode_set_return_date')
    
    
    
    
class HeatingNotificationsLocators(object):
    HEATING_NOTIFICATION=(By.XPATH, "//*[@text='Heating notifications']")
    HEATING_MAX_ON=(By.XPATH, "//*[contains(@content-desc,'Email me for Maximum Temperature  is currently ON. Double tap to change.')]") 
    HEATING_MAX_OFF=(By.XPATH, "//*[contains(@content-desc,'Email me for Maximum Temperature  is currently OFF. Double tap to change.')]")
    HEATING_MIN_ON=(By.XPATH, "//*[contains(@content-desc,'Email me for Minimum Temperature  is currently ON. Double tap to change.')]")
    HEATING_MIN_OFF=(By.XPATH, "//*[contains(@content-desc,'Email me for Minimum Temperature  is currently OFF. Double tap to change.')]")
    WARNING_OFF=(By.XPATH, "//*[contains(@content-desc,'Email me warnings  is currently OFF. Double tap to change')]")
    WARNING_ON=(By.XPATH, "//*[contains(@content-desc,'Email me warnings  is currently ON. Double tap to change')]")
    SAVE_HEATING_NOTIFICATION=(By.ID, 'Save')
    SAVE_MINMAX_NOTIFICATION=(By.ID, 'Save')
    CANCEL_HEATING_NOTIFICATION=(By.ID, 'negativeBtn')
    HEATING_NOTI_TITLE=(By.XPATH, "//*[contains(@content-desc,'Notifications')]" )
    #TARGET_TEMPERATURE_SCROLL_HN=(By.ID, 'tab_outer_circle')
    TARGET_TEMPERATURE_SCROLL_MIN= (By.XPATH,"//android.widget.RelativeLayout[2]/android.widget.RelativeLayout[1]/android.widget.TextView[1]")
    TARGET_TEMPERATURE_SCROLL_MAX= (By.XPATH,"//android.widget.RelativeLayout[1]/android.widget.RelativeLayout[1]/android.widget.TextView[1]")
    NOTIFY_TARGET_TEMPERATURE_SCROLL =(By.XPATH,"//*[contains(@content-desc,'Maximum temperature Notification')]")
    

