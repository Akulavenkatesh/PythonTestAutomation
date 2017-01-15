'''
Created on 11 August 2016

@authors: 
iOS        - rajeshwaran
Android    - TBD
Web        - TBD
'''

from behave import *
import DD_Page_iOSApp as paygeiOS
import FF_utils as utils

strMainClient = utils.getAttribute('common', 'mainClient')


@given(u'The {nameMotionSensor} / {nameContactSensor} / {namePlug} / {nameBulb} are paired with the hub')
def navToDevices(context,nameMotionSensor,nameContactSensor,namePlug,nameBulb):
    #utils.setClient(context, strMainClient)
    if strMainClient=='iOS App': 
            oDeviceRecipes =paygeiOS.DeviceRecipes(context.iOSDriver , context.reporter)
            oDeviceRecipes.navigate_to_device(nameMotionSensor,'MS')
            oDeviceRecipes.navigate_to_device(nameContactSensor,'CS')
            oDeviceRecipes.navigate_to_device(namePlug,'Plug')
            oDeviceRecipes.navigate_to_device(nameBulb,'Bulb')
    elif strMainClient=='Android App':
        print("Call method for Android")
    elif strMainClient=='Web App':
        print("Call method for Web")   
    else:
        print("Problem in getting Main client") 
        

@when(u'User removes all of the existing recipes')
def removeExistingRecipes(context):
    #utils.setClient(context, strMainClient)
    if strMainClient=='iOS App': 
            oDeviceRecipes =paygeiOS.DeviceRecipes(context.iOSDriver , context.reporter)
            oDeviceRecipes.navigate_to_allrecipes()
            oDeviceRecipes.remove_existing_recipes()
    elif strMainClient=='Android App':
        print("Call method for Android")
    elif strMainClient=='Web App':
        print("Call method for Web")   
    else:
        print("Problem in getting Main client") 
        
@then(u'Verify if the recipe template has all available options')
def navToAddaNewRecip(context):
    #utils.setClient(context, strMainClient)
    if strMainClient=='iOS App': 
            oDeviceRecipes =paygeiOS.DeviceRecipes(context.iOSDriver , context.reporter)
            oDeviceRecipes.verify_recipe_template()           
    elif strMainClient=='Android App':
        print("Call method for Android")
    elif strMainClient=='Web App':
        print("Call method for Web")   
    else:
        print("Problem in getting Main client") 

@when(u'User sets {TypeOf} notification recipe for {Sensor} when {SensorState} in the Client')
def setNewRecipes(context,TypeOf,Sensor,SensorState):
    if strMainClient=='iOS App': 
            oDeviceRecipes =paygeiOS.DeviceRecipes(context.iOSDriver , context.reporter)            
            oMotionSensor =paygeiOS.MotionSensor(context.iOSDriver , context.reporter)
            recipe_exists = 100
            if (('opened' in SensorState) or ('closed' in SensorState)):
                oDeviceRecipes.navigate_to_device(Sensor,'CS')
            else:
                oDeviceRecipes.navigate_to_device(Sensor,'MS')
            oMotionSensor.navigate_to_recipes()
            recipe_exists = oDeviceRecipes.verify_notification_recipe_exists(Sensor, TypeOf, SensorState)
            oDeviceRecipes.set_sensor_recipe(recipe_exists, TypeOf, Sensor, SensorState)            
    elif strMainClient=='Android App':
        print("Call method for Android")
    elif strMainClient=='Web App':
        print("Call method for Web")   
    else:
        print("Problem in getting Main client") 
        
@then(u'Verify if the {TypeOf} notification recipe is displayed for {Sensor} when {SensorState} in the device recipe screen')
def verifySavedRecipe(context,TypeOf,Sensor,SensorState):
    #utils.setClient(context, strMainClient)
    if strMainClient=='iOS App': 
            oDeviceRecipes =paygeiOS.DeviceRecipes(context.iOSDriver , context.reporter)
            oMotionSensor =paygeiOS.MotionSensor(context.iOSDriver , context.reporter)
            if oDeviceRecipes.SET_RECIPE_TRIGERRED == 1:
                recipe_exists = 100
                if (('opened' in SensorState) or ('closed' in SensorState)):
                    oDeviceRecipes.navigate_to_device(Sensor,'CS')
                else:
                    oDeviceRecipes.navigate_to_device(Sensor,'MS')
                oMotionSensor.navigate_to_recipes()
                recipe_exists = oDeviceRecipes.verify_notification_recipe_exists(Sensor, TypeOf, SensorState)
                oDeviceRecipes.report_recipe_exists(recipe_exists, TypeOf, Sensor, SensorState)            
            else:
                oDeviceRecipes.report_recipe_exists(1, TypeOf, Sensor, SensorState)
                oDeviceRecipes.SET_RECIPE_TRIGERRED = 0
    elif strMainClient=='Android App':
        print("Call method for Android")
    elif strMainClient=='Web App':
        print("Call method for Web")   
    else:
        print("Problem in getting Main client") 
