'''
Created on 10 Sep 2015

@author: kingston.samselwyn
'''
#import behave
import behave
import time
import steps.CC_platformAPI as oPlatform
import steps.FF_utils as utils
#from pycallgraph import PyCallGraph
'''from pycallgraph.output import GraphvizOutput
from pycallgraph import Config'''


@behave.when('I navigate to the {strPageName} screen {strClient}')
def screen_navigation(context,strPageName, strClient):
    utils.setClient(context, strClient)
    print("testing\n")
    
    '''config = Config(max_depth=1)
    graphviz = GraphvizOutput(output_file='filter_max_depth.png')'''

    

    '''with PyCallGraph(output=graphviz, config=config):
        context.rFM.navigateToScreen( context.reporter, context.oThermostatEP, strPageName)
    '''

@behave.then('I should be able to view the account details and the app version')
def verify_screen(context):
    print()
