'''
Created on 8 Mar 2016

@author: srirudhran
'''
#from behave import *
from behave import *

import DD_Page_iOSApp as paygeiOS
import DD_Page_AndroidApp as paygeAndroid
import FF_utils as utils
strMainClient = utils.getAttribute('common', 'mainClient')



@given('The Hive product is paired to a hub and navigated to Change Password screen')
def changepassword_navigatio(context):
    print("given is launched") 
    if strMainClient=='iOS App':  
        oChangePasswordPage =paygeiOS.SetChangePassword(context.iOSDriver , context.reporter)
        oChangePasswordPage.navigate_to_change_password()
    elif strMainClient=='Android App':
        print("Call method for Android")
        oChangePasswordPage =paygeAndroid.SetChangePassword(context.AndroidDriver , context.reporter)
        oChangePasswordPage.navigate_to_change_password()
    elif strMainClient=='Web App':
        print("Call method for Web")   
    else:
        print("Problem in getting Main client") 

@when('User is changing password on the Client')
def validate_changepassword(context):
    print("When is launched\n")
    if strMainClient=='iOS App': 
        oChangePasswordPage =paygeiOS.SetChangePassword(context.iOSDriver , context.reporter)
        oChangePasswordPage.change_password_screen()
    elif strMainClient=='Android App':
        print("Call method for Android")
        oChangePasswordPage =paygeAndroid.SetChangePassword(context.AndroidDriver , context.reporter)
        oChangePasswordPage.change_password_screen()
    elif strMainClient=='Web App':
        print("Call method for Web")   
    else:
        print("Problem in getting Main client")

@then('Validate user is able to login with the password changed')
def verify_changepassword(context):
    print("Then is launched\n")
    if strMainClient=='iOS App':
        oChangePasswordPage =paygeiOS.HomePage(context.iOSDriver , context.reporter)
        oChangePasswordPage.logout_hive_app()
        oChangePasswordPage =paygeiOS.SetChangePassword(context.iOSDriver , context.reporter)
        oChangePasswordPage.login_change_password()
        oChangePasswordPage =paygeiOS.HomePage(context.iOSDriver , context.reporter)
        oChangePasswordPage.logout_hive_app()
    elif strMainClient=='Android App':
        print("Call method for Android")
        oChangePasswordPage =paygeAndroid.HomePage(context.AndroidDriver , context.reporter)
        oChangePasswordPage.logout_hive_app()
        oChangePasswordPage =paygeAndroid.SetChangePassword(context.AndroidDriver , context.reporter)
        oChangePasswordPage.login_change_password()
        oChangePasswordPage =paygeAndroid.HomePage(context.AndroidDriver , context.reporter)
        oChangePasswordPage.logout_hive_app()
    elif strMainClient=='Web App':
        print("Call method for Web")   
    else:
        print("Problem in getting Main client")