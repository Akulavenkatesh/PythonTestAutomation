'''
Created on 16 July 2016

@authors: 
iOS        - rajeshwaran
Android    - TBD
Web        - TBD
'''

from behave import *
import DD_Page_iOSApp as paygeiOS
import DD_Page_AndroidApp as paygeAndroid
import FF_utils as utils


strMainClient = utils.getAttribute('common', 'mainClient')


#@given(u'The Hive product is paired and setup for Motion Sensor with API Validation')
@given(u'The {nameMotionSensor} is paired with the hub')
def navToScreen(context,nameMotionSensor):
    #utils.setClient(context, strMainClient)
    print("given is launched") 
    if strMainClient=='iOS App': 
            oMotionSensor =paygeiOS.MotionSensor(context.iOSDriver , context.reporter)
            oMotionSensor.navigate_to_motionsensor(nameMotionSensor)
    elif strMainClient=='Android App':
        oMotionSensor =paygeAndroid.MotionSensor(context.AndroidDriver , context.reporter)
        oMotionSensor.navigate_to_motion_sensor_page()
    elif strMainClient=='Web App':
        print("Call method for Web")   
    else:
        print("Problem in getting Main client") 

@when(u'User navigates to the {nameMotionSensor} screen in the Client')
def navToControlScreen(context, nameMotionSensor):
    #utils.setClient(context, strMainClient)
    print("given is launched") 
    if strMainClient=='iOS App': 
            oMotionSensor =paygeiOS.MotionSensor(context.iOSDriver , context.reporter)
            oMotionSensor.navigate_to_motionsensor(nameMotionSensor)
    elif strMainClient=='Android App':
        print("Call method for Android")
        oMotionSensor =paygeAndroid.MotionSensor(context.AndroidDriver , context.reporter)
        oMotionSensor.verify_current_status()
    elif strMainClient=='Web App':
        print("Call method for Web")   
    else:
        print("Problem in getting Main client") 

@when(u'User navigates to the event logs in the Client')
def navigateEventLogs(context):
    #utils.setClient(context, strMainClient)
    print("when is launched") 
    if strMainClient=='iOS App': 
            oMotionSensor =paygeiOS.MotionSensor(context.iOSDriver , context.reporter)
            oMotionSensor.navigate_to_eventlogs()
    elif strMainClient=='Android App':
            print("Call method for Android")
            oMotionSensor =paygeAndroid.MotionSensor(context.AndroidDriver , context.reporter)
            oMotionSensor.navigate_to_eventlogs()
    elif strMainClient=='Web App':
        print("Call method for Web")   
    else:
        print("Problem in getting Main client") 
    
@then(u'Validate the motion logs are displayed')
def verifyEventLogs(context):
    #utils.setClient(context, strMainClient)
    print("then is launched") 
    if strMainClient=='iOS App': 
            oMotionSensor =paygeiOS.MotionSensor(context.iOSDriver , context.reporter)
            oMotionSensor.verify_event_logs()
    elif strMainClient=='Android App':
        print("Call method for Android")
        oMotionSensor =paygeAndroid.MotionSensor(context.AndroidDriver , context.reporter)
        oMotionSensor.navigate_to_eventlogs()
        oMotionSensor.verify_event_logs()
    elif strMainClient=='Web App':
        print("Call method for Web")   
    else:
        print("Problem in getting Main client") 

   
@then(u'Validate the current status of the {nameMotionSensor}')
def verifyCurrentStatus(context, nameMotionSensor):
    #utils.setClient(context, strMainClient)
    print("then is launched") 
    print('Get the current status of the sensor : ', nameMotionSensor)
    if strMainClient=='iOS App': 
            oMotionSensor =paygeiOS.MotionSensor(context.iOSDriver , context.reporter)
            oMotionSensor.verify_current_status(nameMotionSensor)
    elif strMainClient=='Android App':
        print("Call method for Android")
        oMotionSensor =paygeAndroid.MotionSensor(context.AndroidDriver , context.reporter)
        oMotionSensor.verify_current_status()
    elif strMainClient=='Web App':
        print("Call method for Web")   
    else:
        print("Problem in getting Main client") 

@when(u'User views {intNumberOf} days back in the event logs in the Client')
def verifyGivenDayLog(context, intNumberOf):
    print("when is launched") 
    if strMainClient=='iOS App': 
            oMotionSensor =paygeiOS.MotionSensor(context.iOSDriver , context.reporter)
            oMotionSensor.navigate_to_eventlogs()
            oMotionSensor.navigate_to_selected_day_log(intNumberOf)
    elif strMainClient=='Android App':
        print("Call method for Android")
        #yet to be done as we have locators to be changed by dev
    elif strMainClient=='Web App':
        print("Call method for Web")   
    else:
        print("Problem in getting Main client") 

@then(u'Validate the motion event logs are displayed')
def verifyEventLog(context):
    print("then is launched") 
    if strMainClient=='iOS App': 
            oMotionSensor =paygeiOS.MotionSensor(context.iOSDriver , context.reporter)
            oMotionSensor.verify_event_logs()
    elif strMainClient=='Android App':
        print("Call method for Android")
        
    elif strMainClient=='Web App':
        print("Call method for Web")   
    else:
        print("Problem in getting Main client") 


@when(u'User navigates to the Recipes of the motion sensor in the Client')
def navigateToRecipes(context):
    print("then is launched") 
    if strMainClient=='iOS App': 
            oMotionSensor =paygeiOS.MotionSensor(context.iOSDriver , context.reporter)
            oMotionSensor.navigate_to_recipes()
    elif strMainClient=='Android App':
        print("Call method for Android")
        #yet to be done as we have locators to be changed by dev
    elif strMainClient=='Web App':
        print("Call method for Web")   
    else:
        print("Problem in getting Main client") 


@then(u'Validate the current status of Recipes of the {nameMotionSensor}')
def verifyRecipes(context, nameMotionSensor):
    print("then is launched") 
    if strMainClient=='iOS App': 
            oMotionSensor =paygeiOS.MotionSensor(context.iOSDriver , context.reporter)
            oMotionSensor.verify_recipes(nameMotionSensor)
    elif strMainClient=='Android App':
        print("Call method for Android")
        #yet to be done as we have locators to be changed by dev
    elif strMainClient=='Web App':
        print("Call method for Web")   
    else:
        print("Problem in getting Main client") 

