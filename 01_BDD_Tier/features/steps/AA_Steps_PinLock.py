'''Created on 8 Mar 2016

@author: srirudhran

'''

#from behave import *

from behave import *



import DD_Page_iOSApp as paygeiOS

import FF_utils as utils



strMainClient = utils.getAttribute('common', 'mainClient')





@given('The Hive product is paired to a hub and navigated to Pin Lock screen')

def pinlock_navigation(context): 

    if strMainClient=='iOS App':

        oPinLockPage =paygeiOS.SetPinLock(context.iOSDriver , context.reporter)

        oPinLockPage.navigate_to_pin_lock()

        print("given is launched for pin lock") 

    elif strMainClient=='Android App':

        print("Call method for Android")

    elif strMainClient=='Web App':

        print("Call method for Web")   

    else:

        print("Problem in getting Main client")    



@when('User Sets Pin Lock on the Client')

def set_pinlock(context):

    if strMainClient=='iOS App':

        oPinLockPage =paygeiOS.SetPinLock(context.iOSDriver , context.reporter)

        oPinLockPage.navigate_to_pin_lock()

        print("given is launched for pin lock") 

    elif strMainClient=='Android App':

        print("Call method for Android")

    elif strMainClient=='Web App':

        print("Call method for Web")   

    else:

        print("Problem in getting Main client")  





@then('Validate user is able to Succesfully set Pin')

def verify_setpinlock(context):

    if strMainClient=='iOS App':

        oPinLockPage =paygeiOS.SetPinLock(context.iOSDriver , context.reporter)

        oPinLockPage.validate_pin()

        print("given is launched for pin lock") 

    elif strMainClient=='Android App':

        print("Call method for Android")

    elif strMainClient=='Web App':

        print("Call method for Web")   

    else:

        print("Problem in getting Main client")  

    

@when('User Changes Pin on the Client')

def change_pinlock(context):

    if strMainClient=='iOS App':

        oPinLockPage =paygeiOS.SetPinLock(context.iOSDriver , context.reporter)

        oPinLockPage.navigate_to_pin_lock()

        print("given is launched for pin lock") 

    elif strMainClient=='Android App':

        print("Call method for Android")

    elif strMainClient=='Web App':

        print("Call method for Web")   

    else:

        print("Problem in getting Main client")  





@then('Validate the User is able to Successfully change pin')

def verify_changepin(context):

    if strMainClient=='iOS App':

        oPinLockPage =paygeiOS.SetPinLock(context.iOSDriver , context.reporter)

        oPinLockPage.validate_pin()

        print("given is launched for pin lock") 

    elif strMainClient=='Android App':

        print("Call method for Android")

    elif strMainClient=='Web App':

        print("Call method for Web")   

    else:

        print("Problem in getting Main client")  



@when('user forgot Pin on client')

def forgot_pinlock(context):

    if strMainClient=='iOS App':

        oPinLockPage =paygeiOS.SetPinLock(context.iOSDriver , context.reporter)

        oPinLockPage.forgot_pin_lock()

        print("given is launched for pin lock") 

    elif strMainClient=='Android App':

        print("Call method for Android")

    elif strMainClient=='Web App':

        print("Call method for Web")   

    else:

        print("Problem in getting Main client")  





@then('Validate user is able to logout of the app and login again')

def verify_forgotpin(context):

    if strMainClient=='iOS App':

        oPinLockPage =paygeiOS.SetPinLock(context.iOSDriver , context.reporter)

        oPinLockPage.forgot_validate_pin()()

        print("given is launched for pin lock") 

    elif strMainClient=='Android App':

        print("Call method for Android")

    elif strMainClient=='Web App':

        print("Call method for Web")   

    else:

        print("Problem in getting Main client")  
