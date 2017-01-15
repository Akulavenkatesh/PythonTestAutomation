'''
Created on 29 Feb 2016

@author: Nirmalkumar.Anbu
'''



from behave import *


import DD_Page_iOSApp as paygeiOS
import FF_utils as utils

strMainClient = utils.getAttribute('common', 'mainClient')

@given('User is navigated to Text Control page')
def navigationTextControl(context):
    
    if strMainClient=='iOS App':
        oTXTCntrlPage=paygeiOS.TextControl(context.iOSDriver, context.reporter)
        oTXTCntrlPage.navigate_to_TextControl_page()
    elif strMainClient=='Android App':
        print("Call method for Android")
    elif strMainClient=='Web App':
        print("Call method for Web")   
    else:
        print("Problem in getting Main client")
        
@When ('User adds the below list of UserName and Mobile number in Text Control Page')
def textControlUseradditions(context): 
    
    if strMainClient=='iOS App':
        oTXTCntrlPage = paygeiOS.TextControl(context.iOSDriver, context.reporter)
        oTXTCntrlPage.textControlOptions(context)   
    elif strMainClient=='Android App':
        print("Call method for Android")
    elif strMainClient=='Web App':
        print("Call method for Web")   
    else:
        print("Problem in getting Main client")
    
    

@Then ('Validate maximum limit of new users for Text control options')
def validateTextControlLimit(context): 
         
    if strMainClient=='iOS App':
        oTXTCntrlPage = paygeiOS.TextControl(context.iOSDriver, context.reporter)
        oTXTCntrlPage.textControlValidation(context)  
    elif strMainClient=='Android App':
        print("Call method for Android")
    elif strMainClient=='Web App':
        print("Call method for Web")   
    else:
        print("Problem in getting Main client")
    
  

