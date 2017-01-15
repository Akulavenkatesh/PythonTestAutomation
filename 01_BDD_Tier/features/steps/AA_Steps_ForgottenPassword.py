'''
Created on 8 Mar 2016

@author: sri.gunasekaran
'''

from behave import *

import DD_Page_WebApp as pageWebApp

import FF_ScheduleUtils as oSchdUtil
import FF_utils as utils

@given(u'The Hive product is paired and forgotten password screen is displayed on the Client')
def navToScreen(context):
    #utils.setClient(context, strClientType)
    oForgottenPasswordpage = pageWebApp.ForgottenPassword(context.WebDriver,context.reporter)
    oHeatingDashboardpage = pageWebApp.HeatingDashboardPage(context.WebDriver,context.reporter)
    oHeatingDashboardpage.logout()
    oForgottenPasswordpage.set_screen(context) 
    
@when(u'{strUsername} is automatically entered and submitted on the Client')
def setEmailaddr(context,strUsername):
    
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Set Email address') 
    #utils.setClient(context, strClientType)
    strEmailAddr=strUsername+'@yopmail.com'
    oForgottenPasswordpage = pageWebApp.ForgottenPassword(context.WebDriver,context.reporter)
    oForgottenPasswordpage.submit_username(strEmailAddr)
    
@then(u'Validate if {strNewPassword} can be set for the {strUsername} and login is successful using {strNewPassword}')
def setPassword(context,strNewPassword,strUsername):
    oForgottenPasswordpage = pageWebApp.ForgottenPassword(context.WebDriver,context.reporter)
    oForgottenPasswordpage.set_new_password(strUsername,strNewPassword) 
    oLoginPage = pageWebApp.LoginPage(context.WebDriver,context.reporter)
    #login_hive_app(self, strUsername, strNewPassword)(context.WebDriver,context.reporter)
    oLoginPage.login_hive_app(strUsername, strNewPassword)

    