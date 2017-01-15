'''
Created on 5 May 2016

@author: ranganathan.veluswamy
'''
from _datetime import timedelta
import time

from behave import *

import AttributeReportTest as SP
import FF_alertmeApi as ALAPI
import FF_threadedSerial as AT
import FF_utils as utils

@given(u'Test attributes')
def step_impl(context):
    SP.__name__ = "main"
    SP.initialize()
    SP.ReadAttributes()
    SP.returnBaseState()
