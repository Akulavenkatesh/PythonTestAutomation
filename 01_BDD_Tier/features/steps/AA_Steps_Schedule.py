'''
Created on 26 May 2015

@author: ranganathan.veluswamy
'''
from datetime import datetime
from behave import *
import FF_ScheduleUtils as oSchdUtil
import FF_utils as utils
import FF_Platform_Utils as pUtils




@when('The below schedule is set for the whole week on the {Device} via Hub API')
def setWeekSceduleViaHUBAPI(context, Device):
    
    context.deviceType = Device
    context.oThermostatEP  = context.oThermostatClass.heatEP
    context.oThermostatEP.deviceType = Device
    
    oSchedDict = {}    
    oSchedDict.clear()
    oSchedDict = oSchdUtil.createWeekSceduleFormatFromTable(context)
    context.oSchedDict = oSchedDict
    oAllNodeList = pUtils.getNodeAndDeviceVersionID()
    
    if Device in oAllNodeList:
        
        nodeId = oAllNodeList[Device]["nodeID"]
        context.NodeID = nodeId
        SDNodeID, _ = pUtils.getDeviceSDNodeID(nodeId)
        print(nodeId, "nodeId")
        print(SDNodeID, "SDNodeID")
        #Set and report schedule
        context.rFM.setSchedule(context, oSchedDict, boolViaHub = True, nodeId = SDNodeID)
    else:
        context.boolScenarioExecStatus = False
        context.strStepFailReason = "Node is MISSING for the given device type: " + Device
        return False

@when('The below schedule is set for the whole week on the Client {mode}')
def setWeekScedule(context, mode):
    utils.setClient(context, 'Client')      
    
    for oRow in context.table:       
        strDay = oRow['Day'][:3].lower()
        
    print(strDay)
    oSchedDict = {}    
    oSchedDict.clear()
    oSchedDict = oSchdUtil.createWeekSceduleFormatFromTable(context)
    
    context.oSchedDict = oSchedDict
    
    if 'STAND' in mode.upper() and 'ALONE' in mode.upper(): boolStandaloneMode = True
    else: boolStandaloneMode = False
    
    #Set and report schedule
    #context.rFM.setSchedule(context, oSchedDict, boolStandaloneMode)
    
@when('The below {device} schedule is set for {strDay} via Hub')
def setDaySceduleViaHub(context, device, strDay):
    deviceType = device.strip()
    strDay = strDay.split()[0]
    context.oThermostatEP  = context.oThermostatClass.heatEP
    context.oThermostatEP.deviceType = deviceType
    #To identify strDay in terms of actual weekday (eg : sun , mon etc.)
    if strDay.upper() in oSchdUtil.oWeekDayDict: strDay = oSchdUtil.oWeekDayDict[strDay.upper()]    
    else: strDay = datetime.today().strftime("%a").lower() 
    print(strDay)
    oSchedDict = {}    
    oSchedDict.clear()
    oSheduleList = oSchdUtil.createSceduleFormatFromTableForHUB(context)
    
    if oSheduleList == False: return False
    oSchedDict = {strDay : oSheduleList}  
    
    context.oSchedDict = oSchedDict
    print(oSchedDict)
    oAllNodeList = pUtils.getNodeAndDeviceVersionID()
    
    if deviceType in oAllNodeList:
        
        context.deviceType = deviceType
        nodeId = oAllNodeList[deviceType]["nodeID"]
        context.NodeID = nodeId
        SDNodeID, _ = pUtils.getDeviceSDNodeID(nodeId)
        print(nodeId, "nodeId")
        print(SDNodeID, "SDNodeID")
        #Set and report schedule
        context.rFM.setSchedule(context, oSchedDict, boolViaHub = True, nodeId = SDNodeID)
    else:
        context.boolScenarioExecStatus = False
        context.strStepFailReason = "Node is MISSING for the given device type: " + deviceType
        return False
        
    
    
    
    
@when('The below schedule is set for {strDay}')
def setDayScedule(context, strDay):
    utils.setClient(context, strDay)      
    
    strDay = strDay.split()[0]

    #To identify strDay in terms of actual weekday (eg : sun , mon etc.)
    if strDay.upper() in oSchdUtil.oWeekDayDict: strDay = oSchdUtil.oWeekDayDict[strDay.upper()]    
    else: strDay = datetime.today().strftime("%a").lower() 
    print(strDay)
    oSchedDict = {}    
    oSchedDict.clear()
    if 'Start Time' in context.table.headings:
        oSheduleList = oSchdUtil.createSceduleFormatFromTable(context)
        if oSheduleList == False: return False
        oSchedDict = {strDay : oSheduleList}  
    else:
        oSheduleList = oSchdUtil.createSceduleFormatFromTableWithoutStartTime(context)
        if oSheduleList == False: return False
        oSchedDict = {strDay : oSheduleList} 
    context.oSchedDict = oSchedDict
    #print(oSchedDict)
    
    
    #Set and report schedule
    context.rFM.setSchedule(context, oSchedDict)
    

   
@when('{strEvent} event Random schedule is generated and set for {strDay}')
def setRandomDaySchedule(context, strEvent, strDay):
    utils.setClient(context, strDay)      
    
    strDay = strDay.split()[0]
    oSchedDict = {}    
    oSchedDict.clear()
    if strDay.upper() == 'TODAY': strDay = datetime.today().strftime("%a").lower() 
    if strDay.upper() in oSchdUtil.oWeekDayDict: strDay = oSchdUtil.oWeekDayDict[strDay.upper()]    
    context.strDay = strDay
    
    if strEvent.isnumeric(): intEvent = int(strEvent) 
    else:  intEvent = 0
    
    if not context.table is None:
        context.ScheduleTable = context.table
        if 'Start Time' in context.table.headings:
            oSheduleList = oSchdUtil.createRandomSceduleFormatFromTable(context, 'Start Time', len(context.table.rows))
            if oSheduleList == False: return False
            oSchedDict = {strDay : oSheduleList}  
        elif 'Target Temperature' in context.table.headings:
            oSheduleList = oSchdUtil.createRandomSceduleFormatFromTable(context, 'Target Temperature', len(context.table.rows))
            if oSheduleList == False: return False
            oSchedDict = {strDay : oSheduleList}  
        elif 'Hot Water State' in context.table.headings:
            oSheduleList = oSchdUtil.createRandomSceduleFormatFromTable(context, 'Hot Water State', len(context.table.rows))
            if oSheduleList == False: return False
            oSchedDict = {strDay : oSheduleList} 
        else:
            oSheduleList = oSchdUtil.createRandomSceduleFormatFromTable(context, '', intEvent)
            if oSheduleList == False: return False
            oSchedDict = {strDay : oSheduleList} 
    else:
        oSheduleList = oSchdUtil.createRandomSceduleFormatFromTable(context, '', intEvent)
        if oSheduleList == False: return False
        oSchedDict = {strDay : oSheduleList} 
    context.oSchedDict = oSchedDict
    
    print(oSchedDict)
    
    #Set and report schedule
    context.rFM.setSchedule(context, oSchedDict)
    
    
@when('The schedule for below \'{strEvenValueHeader}\' is set with current time lying on the {strEventPosition} event, for {strDay}')
def setScheduleWithEventPosition(context, strEventPosition, strDay, strEvenValueHeader):
    utils.setClient(context, strDay)      
    
    strDay = strDay.split()[0]
    strDay = datetime.today().strftime("%a").lower() 
    if strDay.upper() in oSchdUtil.oWeekDayDict: strDay = oSchdUtil.oWeekDayDict[strDay.upper()]    
    oSchedDict = {}    
    oSchedDict.clear()
    context.ScheduleTable = context.table
    if 'Target Temperature' in context.table.headings or 'Hot Water State' in context.table.headings:
        oSheduleList = oSchdUtil.createSceduleFormatFromTableWithEventPosition(context, strEventPosition)
        if oSheduleList == False: return False
        oSchedDict = {strDay : oSheduleList}  
    context.oSchedDict = oSchedDict
    
   
    #Set and report schedule
    context.rFM.setSchedule(context, oSchedDict)
    
@then('Verify if the Schedule is set')
def verifyDaySchedule(context):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Verifying if the Schedule is set')
    for oKey in context.oSchedDict.keys():
        if oKey in context.WeeklyScheduleAfter.keys():
            strReportSchedule, boolCompStatus = oSchdUtil.getScheduleForReportWithComparison(oSchdUtil.remove_duplicates(context.oSchedDict[oKey]), oSchdUtil.remove_duplicates(context.WeeklyScheduleAfter[oKey]), oKey)
            context.reporter.ReportEvent('TestValidation', strReportSchedule, boolCompStatus, 'Center')

@then('Validate the schedule that is set')
def ValidateDaySchedule(context):
    oWeekDay = ['sun','mon','tue','wed','thu','fri','sat'] 
    strDay = oWeekDay[int(datetime.today().strftime("%w" ))]
    if strDay in context.oSchedDict:
        oScheduleList = context.oSchedDict[strDay]
        oScheduleList = oSchdUtil.remove_duplicates(oScheduleList)
        oSchdUtil.runValidationForSchedule(context, oSchdUtil.getRemainingDaySchedule(oScheduleList))

@then('Validate if the Schedule is set for the whole week')
def ValidateWeekSchedule(context):
    oSchdUtil.runValidationForWeekSchedule(context)
    

@then(u'Validate if the Schedule is set for the whole week on the {device}')
def ValidateWeekScheduleForDevice(context, device):
    oSchdUtil.runValidationForWeekScheduleForDevice(context)