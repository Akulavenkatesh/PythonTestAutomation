'''
Created on 18 Apr 2016

@author: sri.gunasekaran
'''
from datetime import datetime, timedelta
import time

from behave import *

import FF_ScheduleUtils as oSchdUtil
import FF_utils as utils
import DD_Page_WebApp as oPageWeb


@when(u'heating notification is set automatically for HIGH Temperature alert with Target Temperature as {strSetTemp1:.1f} and LOW Temperature alert with Target Temperature as {strSetTemp2:.1f}{strClientType}')
def setBothNotification(context,strSetTemp1,strSetTemp2,strClientType):
    utils.setClient(context, strClientType)
    #oAlertType = oPageWeb.SetNotification(context.WebDriver,context.reporter)
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Set HIGH & LOW Temperature Notification')
    if (int(strSetTemp1) >= 5 and int(strSetTemp1) <= 32) or (int(strSetTemp2) >= 5 and int(strSetTemp2) <= 32):
        print('High  & Low Temperature Alert')
        context.oThermostatEP.setHighNotification(strSetTemp1,strSetTemp2,'Yes') 
    else :
        #context.rFM.quitDrivers(context)
        return False
        context.skip.scenario()
             
@when(u'heating notification is set automatically for {strNotiTempType} alert with Target Temperature as {strSetTemp:.1f}{strClientType}')
def setNotification(context,strNotiTempType,strSetTemp,strClientType):
    utils.setClient(context, strClientType)
    #oAlertType = oPageWeb.SetNotification(context.WebDriver,context.reporter)
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Set '+ strNotiTempType+ ' Notification')
    if float(strSetTemp) >= 5 and float(strSetTemp) <= 32 :
        if strNotiTempType.upper().find('HIGH')>=0:
            print('High Temperature Alert')
            context.oThermostatEP.setHighNotification(strSetTemp)
        else :
            print('Low Temperature Alert')
            context.oThermostatEP.setLowNotification(strSetTemp)
    else :
        context.rFM.quitDrivers(context)


@when(u'heating notification is turned {strNotiState} automatically for HIGH Temperature alert and LOW Temperature alert {strClientType}')
def setNotificationOnOff(context,strNotiState,strClientType): 
    utils.setClient(context, strClientType)
    #oAlertType = oPageWeb.SetNotification(context.WebDriver,context.reporter)
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Set Notification ' + strNotiState) 
    
    context.oThermostatEP.setNotificationOnOff(strNotiState)
    #oAlertType.setNotificationOnOff(strNotiState)


@then('Automatically validate {strNotiTempType1} alert as active with Target Temperature as {strExpectedTemp1:.1f} and {strNotiTempType2} alert as active with Target Temperature as {strExpectedTemp2:.1f}')
def validateBothNotification(context,strNotiTempType1,strExpectedTemp1,strNotiTempType2,strExpectedTemp2):
    boolAutoMode = True
    if context.APIType  == 'PLATFORM': 
        boolAutoMode = False
    
    context.rFM.validateNotification(context.reporter,boolAutoMode,context.oThermostatEP,strExpectedTemp1,strNotiTempType1)
    context.rFM.validateNotification(context.reporter,boolAutoMode,context.oThermostatEP,strExpectedTemp2,strNotiTempType2)
        

@then('Automatically validate {strNotiTempType} alert as active with Target Temperature as {strExpectedTemp:.1f}')
def validateNotification(context,strNotiTempType,strExpectedTemp):
    boolAutoMode = True
    if context.APIType  == 'PLATFORM': 
        boolAutoMode = False
    
    
    context.rFM.validateNotification(context.reporter,boolAutoMode,context.oThermostatEP,strExpectedTemp,strNotiTempType)

@then('Automatically validate the alerts as turned {strExpNotiState}')
def validateNotificationOnOff(context,strExpNotiState):
    boolAutoMode = True
    if context.APIType  == 'PLATFORM': 
        boolAutoMode = False
    
    utils.setClient(context, 'mainClient') 
    #oAlertType = oPageWeb.SetNotification(context.WebDriver,context.reporter)
    strExpectedTemp = context.oThermostatEP.getNotificationTempFromUI()
     
        
    if strExpNotiState =='ON' :
        strExpectedRuleStatus = 'ACTIVE'
    else :
        strExpectedRuleStatus = 'INACTIVE'
        
    
    context.rFM.validateNotificationOnOff(context.reporter,boolAutoMode,context.oThermostatEP,strExpectedTemp[0],'HIGH',strExpectedRuleStatus)
    context.rFM.validateNotificationOnOff(context.reporter,boolAutoMode,context.oThermostatEP,strExpectedTemp[1],'LOW',strExpectedRuleStatus)
        
    
    
    
    
