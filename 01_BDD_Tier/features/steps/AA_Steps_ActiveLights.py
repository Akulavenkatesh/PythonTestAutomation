'''
Created on 11 August 2016

@authors: 
iOS        - rajeshwaran
Android    - TBD
Web        - TBD
'''

from behave import *
import FF_utils as utils
import FF_Platform_Utils as pUtils

strMainClient = utils.getAttribute('common', 'mainClient')

@given(u'The {lightType} light {deviceName} is paired with the hub and navigate to {strClientType}')
def navigateColourLight(context,lightType,deviceName, strClientType):
    oSensorEP = context.oThermostatClass.heatEP
    oSensorEP.reporter = context.reporter
    oSensorEP.iOSDriver = context.iOSDriver
    context.reporter.ActionStatus = True
    context.oThermostatEP = oSensorEP
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Verify if the '+deviceName+' is paired with the kit')
    utils.setClient(context, strClientType)
    context.oThermostatEP.navigateToDeviceScreen(deviceName)
       


@when(u'User sets the {Settings} as {Value} on the {strClientType}')
def setValueForBulb(context,Settings,Value,strClientType):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('User sets the '+Settings+' as '+Value)
    utils.setClient(context, strClientType)
    context.oThermostatEP.setLocalValues(Settings,Value)
    context.oThermostatEP.navigateToDesiredSettings(Settings)
    context.oThermostatEP.setValueForBulbBySwiping(Settings,Value)
        
        
@then(u'Verify if the {Settings} is set as expected in API for {deviceType}')
def verifyAPISettings(context,Settings,deviceType):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Verify if the '+Settings+' is updated in API')
    buldNodeID = pUtils.getDeviceNodeID(deviceType);
    context.oThermostatEP.verifyValueInAPI(buldNodeID)
    context.oThermostatEP.setLocalValues("","")
    
    
    