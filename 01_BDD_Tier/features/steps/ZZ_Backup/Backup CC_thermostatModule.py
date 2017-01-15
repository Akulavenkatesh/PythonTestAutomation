'''
Created on 27 Apr 2015

@author: keith

TODO: Check if true OFF still exists in BM code
TODO: Check behaviour if FP triggered when in OFF and TRUE OFF

TODO: Test guardzone warnings
TODO: Test BOOST from BOOST (does modeExpire work correctly)
TODO: Holiday Mode Tests

- futureHolidayTest()
  Set a holiday in the future.
  Change clock time so that clock time is a few minutes before the holiday start.
  Confirm that holiday starts.
  Change clock time so that clock time is a few minutes before holiday end.
  Confirm that holiday ends.
  Have a switch on this test to either move time or use real time.

- cancelFutureHolidayTest()

- nowHolidayTest() 
  Set a holiday to start now
  Confirm that holiday starts now.
  
- cancelCurrentHolidayTest() 

- holidayTransitionsTest()
  Holiday transition tests - set an holiday from all combinations of start modes.
  Check it starts, ends and check that modes return to initial modes.
  
    - From various mode combinations
        
        Water Modes:
            OFF
            MAN
            AUTO
            BOOST (OFF)
            BOOST (MAN)
            BOOST (AUTO)
        
        Heating Modes:
        (Note each of these scenarios should also be combined with each hot water mode)
            OFF
            MAN
            AUTO
            OVERRIDE
            Single BOOST scenarios (shall return to original mode after BOOST completes)
                BOOST (OFF)
                BOOST (MAN)
                BOOST (AUTO)
                BOOST (OVERRIDE)
            Double BOOST scenarios (shall return to original mode after BOOST completes)
                OFF > BOOST > BOOST
                MAN > BOOST > BOOST
                AUTO > BOOST > BOOST
                OVERRIDE > BOOST > BOOST
        
        Store modes in list of lists.  Each item is a list.  First entry in each item is the start mode.
        Subsequent entries can be BOOSTS, e.g.
        
        [['OFF'],['OFF','BOOST','BOOST']]
            
        Test Description:
            Set wanted heat mode, set wanted water mode
            Confirm modes.
            Set a holiday of duration 1min to start in one minute
            Confirm modes switch to HOLIDAY.
            Pause for 1min
            Wait for 2mins (max) for modes to switch back to start modes.
        
- Try to change setpoint during a holiday
- Try to set a boost during holiday

TODO: Add 0.1'C hysteresis on setpoint vs runnningState check.
TODO: Add an attribute reporting check (to make sure they are all set correctly).
TODO: Add time change by ZB command
        
Attribute Truth Table:

Water, OFF,           SM=00, SH=00, SHD=0000
Water, Manual,        SM=04, SH=01, SHD=FFFF
Water, Auto,          SM=04, SH=00, SHD=0000
Water, BOOST          SM=05, SH=01, SHD=xxxx

Heat, OFF,            SM=00, SH=00, SHD=0000
Heat, Manual          SM=04, SH=01, SHD=FFFF
Heat, Auto            SM=04, SH=00, SHD=0000
Heat, BOOST           SM=05, SH=01, SHD=xxxx
Heat, Override        SM=04, SH=01, SHD=xxxx

Allowed Transition Table:

OFF      > MANUAL (Default 20'C setpoint, mode select)                        
         > MANUAL (Arbitrary setpoint, knob rotate in OFF)
         > AUTO   (Schedule setpoint, mode select)
         > BOOST  (22'C default setpoint, boost button press)
         > BOOST  (Arbitrary setpoint, boost button + knob rotate)

MANUAL   > OFF    (Heat SP=1'C, Water SP=32'C)
         > AUTO   (Schedule setpoint)  
         > BOOST  (22'C default setpoint)
         > BOOST  (Arbitrary setpoint)
        
AUTO     > OFF    (Heat SP=1'C, Water SP=32'C)
         > MANUAL (Default 20'C setpoint)
         > BOOST  (Default 22'C setpoint)
         > BOOST  (Arbitrary setpoint)

OVERRIDE > OFF    (Heat SP=1'C, Water SP=32'C)
         > MANUAL (Default 20'C setpoint)
         > AUTO   (Schedule setpoint)
         > BOOST  (22'C default setpoint)
         > BOOST  (Arbitrary setpoint)

BOOST    > BOOST_CANCEL   (Back button - return to previous mode/setpoint)
         > OFF            (Heat SP=1'C, Water SP=32'C)
         > MANUAL         (Default 20'C setpoint)
         > AUTO           (Schedule setpoint)

Water - Allowed Mode Transitions

OFF      > MANUAL
         > AUTO
         > BOOST (Default)
         > BOOST (Arbitrary)
         
MANUAL   > OFF
         > AUTO
         > BOOST (Default)
         > BOOST (Arbitrary)

AUTO     > OFF
         > MANUAL
         > BOOST (Default)
         > BOOST (Arbitrary)
         
BOOST    > BOOST_CANCEL (Back button - return to previous mode/setpoint)
         > OFF
         > MANUAL
         > AUTO
         
'''

import time
import datetime
import random
import redis

import FF_loggingConfig as config
import FF_zigbeeClusters as zcl
import FF_convertTimeTemperature as tt
import BackupFF_threadedSerial as AT

r = redis.StrictRedis(host='localhost', port=6379, db=0)
days = {'sun':'01','mon':'02','tue':'04','wed':'08','thu':'10','fri':'20','sat':'40'}
timeOffset = datetime.timedelta(seconds=0)

COMMAND_TIMEOUT = datetime.timedelta(seconds=120) # Max time to wait (in seconds) for states to resolve after sending commands
GUARDZONE = 30 # Time in seconds before and after schedule event or mode expire during which no setting (or update) operations allowed

class thermostatClass(object):
    def __init__(self,nodeId):
        self.statusOk=True
        self.statusCode={}
        
        self.heatEP = thermostatEndpoint(self,nodeId,'HEAT','05')
        self.waterEP = thermostatEndpoint(self,nodeId,'WATER','06')
        return
    def update(self):
        """ Updates the endpoint states and their respective models
            Exit immediately with an error if we are in the guard zone i.e. near the next/last event
            event in the model schedule or near a mode expire time.
            
            Otherwise update the object states/variables.
            
        """
        self.statusOk=True
        self.statusCode={}
        
        respState,respValue = self.heatEP.update()
        if not respState:
            self.statusOk=False
            self.statusCode['HEAT']=respValue
        
        respState,respValue = self.waterEP.update()
        if not respState:
            self.statusOk=False
            self.statusCode['WATER']=respValue
        
        return self.statusOk,self.statusCode

class thermostatEndpoint(object):
    """ Class object containing last known set of state variables
        for the Tstat.
        
    """
    def __init__(self,thermostat,nodeId,epType,epId):

        # Parent Tstat
        self.parentTstat = thermostat

        # ZB Address for Tstat
        self.nodeId = nodeId
        self.epId = epId
        self.type = epType

        # Setpoint constants for SLT3
        self.MANUAL_DEFAULT = 20
        self.BOOST_DEFAULT = 22
        
        # Remember there is no auto o/r for hot water.
        # Boost Cancel is the back button boost cancel on the Tstat (not actually a mode but does cause a mode transition)        
        self.allowedModes = ['OFF','MANUAL','AUTO','OVERRIDE','BOOST','BOOST_CANCEL','HOLIDAY']
        if self.type=='WATER': self.allowedModes.remove('OVERRIDE')
        self.previousModes = {'00':'OFF','01':'MANUAL','10':'AUTO'}
        self.allowedFpDefaults = [sp/2 for sp in range(10,25)]

        self.minSetpoint = 5
        self.maxSetpoint = 32
        self.allowedSetpoints = [1.0] + [sp/2 for sp in range(10,65)]
        self.maxNumEvents = 6
        
        # Status - used to indicate an error state. Invalid mode or similar.
        self.statusOk = True
        self.statusCode = []
        
        # Thermostat Mode - AUTO,MANUAL,OVERRIDE,OFF,BOOST
        self.mode = None

        # Initialisation is done by forcing a read of the given attribute.  This will update the REDIS cache.

        # Private Attributes - Used to establish mode
        self._systemMode = self._initialiseAttribute('Thermostat Cluster', 'systemMode')
        self._temperatureSetpointHold = self._initialiseAttribute('Thermostat Cluster', 'temperatureSetpointHold')
        self._temperatureSetpointHoldDuration = self._initialiseAttribute('Thermostat Cluster', 'temperatureSetpointHoldDuration')
        
        # Public Attributes
        self.thermostatRunningState = self._initialiseAttribute('Thermostat Cluster', 'thermostatRunningState')

        if self.type=='HEAT':
            self.localTemperature = self._initialiseAttribute('Thermostat Cluster', 'localTemperature')
            self.occupiedHeatingSetpoint = self._initialiseAttribute('Thermostat Cluster', 'occupiedHeatingSetpoint')            
            self.frostProtectionSetpoint = self._initialiseAttribute('BG Cluster', 'frostProtectionSetpoint')            
            # Previous modes are encoded 00=OFF, 01=MANUAL, 10=AUTO.  Use lastMode to get string mode
            self._previousHeatMode = self._initialiseAttribute('BG Cluster', 'previousHeatMode')
            self._previousWaterMode = self._initialiseAttribute('BG Cluster', 'previousWaterMode')               
            self.previousHeatSetpoint = self._initialiseAttribute('BG Cluster', 'previousHeatSetpoint')
            
            # Holiday mode attributes
            self.holidayModeEnabled = self._initialiseAttribute('BG Cluster', 'holidayModeEnabled')
            self.holidayModeActive = self._initialiseAttribute('BG Cluster', 'holidayModeActive')
            self.holidaySetpoint = self._initialiseAttribute('BG Cluster', 'holidaySetpoint')
            # These ones are private because we build mode useful datetimes from them
            self._holidayStartDate = self._initialiseAttribute('BG Cluster', 'holidayStartDate')
            self._holidayStartTime = self._initialiseAttribute('BG Cluster', 'holidayStartTime')
            self._holidayEndDate = self._initialiseAttribute('BG Cluster', 'holidayEndDate')
            self._holidayEndTime = self._initialiseAttribute('BG Cluster', 'holidayEndTime')

            # Holiday Start/End datetimes will be converted to a datetime type and stored in the following variables
            # update of Tstat object will set these to correct value (similar to mode)
            if self.holidayModeEnabled=='01':
                self.holidayStart = self._buildHolidayDatetimeUTC(self._holidayStartDate, self._holidayStartTime)
                self.holidayEnd = self._buildHolidayDatetimeUTC(self._holidayEndDate, self._holidayEndTime)
            else:
                self.holidayStart=None
                self.holidayEnd=None

        # Weekly Schedule
        self._weeklySchedule = {}
#         self._scheduleLastUpdate = 0    # Timestamp of last schedule read. If it's 0 or older than 1hr
#                                         # then we'll re-synch REDIS with BM latest value.
        
        # Since schedule is only reported on change, for initialisation we provoke a REDIS update by forcing a schedule read.
        clust='0201'
        for day in days:
            respState,_,respValue = AT.getWeeklySchedule(self.nodeId, self.epId, clust, days[day])
            if not respState:
                self._setStatusCode("ERROR: getWeeklySchedule(), {}".format(respValue))
                return self.statusOk,self.statusCode
                     
        # Get latest values from REDIS and update this instance
        self._updateThermostatEp()
        
        # Create a model object
        self.model = thermostatEndpointModel(self)        
        
        return
    """ Public Methods """
    def update(self):
        """ Update the thermostat state from REDIS and do a cross check with model state

        """                
        # Reset the status variables on every update
        self.statusOk=True
        self.statusCode=[]
        
        # Update the Thermostat state and return early if in bad state
        respState, respValue = self._updateThermostatEp()
        if not respState: return respState,respValue
        # Check the model state
        self.model.checkModel()
        return self.statusOk,self.statusCode
    def createLogStrings(self):
        """ Create a string(s) containing current state variables
            
            Timestamp, stateVariables, SM, TSH, TSHD, T, OHS, TRS, FP, 
            Timestamp, schedule,sun,mon,tue,wed,thu,fri,sat
            
        """
        timestamp = time.strftime("%d/%m/%Y %H:%M:%S")
        stateVariablesStr = "{0},stateVariables,{1},{2},{3},{4},{5},{6},{7}".format(timestamp,
                                                                                    self.systemMode,
                                                                                    self.temperatureSetpointHold,
                                                                                    self.temperatureSetpointHoldDuration,
                                                                                    self.temperature,
                                                                                    self.occupiedHeatingSetpoint,
                                                                                    self.thermostatRunningState,
                                                                                    self.frostProtection)
        
        scheduleString = "{0},schedule,{1},{2},{3},{4},{5},{6},{7}".format(timestamp,
                                                                           self.sunSchedule,
                                                                           self.monSchedule,
                                                                           self.tueSchedule,
                                                                           self.wedSchedule,
                                                                           self.thuSchedule,
                                                                           self.friSchedule,
                                                                           self.satSchedule)

        return stateVariablesStr,scheduleString
    def printThermostatState(self):
        """  Print the state/schedule values in the following format
        
        States: SM, TSH, TSHD,    T,  OHS, TRS,   FP
                04,  01, FFFF, 0000, 0000,  01, 0000 
        
        Mode        = AUTO (MANUAL, OFF, BOOST, AUTO O/R, HOLIDAY)
        Temperature = xx'C
        Setpoint    = yy'C
        
        Sunday         Monday         Tuesday        Wednesday      Thursday       Friday         Saturday
        08:00, 23.5'C  08:00, 23.5'C  08:00, 23.5'C  08:00, 23.5'C  08:00, 23.5'C  08:00, 23.5'C  08:00, 23.5'C
        10:00, 22'C
        
        """
        print()
        
        # Print the raw state values        
        frost = self.parentTstat.heatEP.frostProtectionSetpoint 
        phm = self.parentTstat.heatEP._previousHeatMode
        phs = self.parentTstat.heatEP.previousHeatSetpoint
        pwm = self.parentTstat.heatEP._previousWaterMode
                
        print("States:   SM, TSH, TSHD,  TRS,   FP,  PHM,  PHS,  PWM")
        print("States: {0:>4},{1:>4},{2:>5},{3:>5},{4:>5},{5:>5},{6:>5},{7:>5}".format(self._systemMode,
                                                                         self._temperatureSetpointHold,
                                                                         self._temperatureSetpointHoldDuration,
                                                                         self.thermostatRunningState,
                                                                         frost,
                                                                         phm,
                                                                         phs,
                                                                         pwm))
        
        print("\nMode        = {}".format(self.mode))
        temperature = tt.temperatureHexStringToFloat(self.parentTstat.heatEP.localTemperature)
        setpoint = tt.temperatureHexStringToFloat(self.parentTstat.heatEP.occupiedHeatingSetpoint)
        print("Temperature = {}".format(temperature))
        print("Setpoint    = {}".format(setpoint))
        
        print()
        print('Sunday         Monday         Tuesday        Wednesday      Thursday       Friday         Saturday')
        
        dayList = ['sun','mon','tue','wed','thu','fri','sat']
        for event in range(0,6):
            eventString=''
            for day in dayList:
                # 0 8 16 (event*8)
                daySched =self._weeklySchedule[day]
                timeStr = daySched[event][0]
                tempFloat = daySched[event][1]
                dayString = "{},{:>4}'C   ".format(timeStr,tempFloat)
                eventString = eventString + dayString
            print(eventString)

        print('{}, statusOk={}\n'.format(self.statusCode,self.statusOk))
        return 0
    def lastMode(self):
        """ Returns string version of previousHeatMode or previousWaterMode
        
        """
        if self.type=='HEAT':
            return self.previousModes[self._previousHeatMode]
        if self.type=='WATER':
            return self.parentTstat.heatEP.previousModes[self.parentTstat.heatEP._previousWaterMode]
    """ Public Set Methods """   
    def setMode(self,myMode,mySetpoint=None,myDuration=1):
        """ Set the MODE of the thermostat to AUTO,MANUAL,OFF,BOOST,OVERRIDE
        
            Exit with an error if we are in the guard zone (Near to schedule event or more expire)
            
            Note: Water setpoints are always 32'C. Relay state in Auto is determines only by schedule setpoints.
            Always ON = ON
            Always OFF = OFF
            Auto on/off = Schedule setpoint (0'C or 99'C)
            BOOST = ON (for given time)
        
        """
        self.statusOk=True
        self.statusCode=[]
        
        nowTime=getTestTime(timeOffset)
        scheduleSetpoint,_,_ = self.model._eventStatus(nowTime)
        
        # Check the given mode is an allowed mode
        if myMode not in self.allowedModes:
            self._setStatus("ERROR: Mode must be one of {}".format(self.allowedModes))
            return self.statusOk, self.statusCode
        
        # Check if current mode is HOLIDAY
        if self.mode=='HOLIDAY':
            self._setStatusCode("ERROR: setMode() in HOLIDAY is not allowed. Use cancelHoliday() to exit HOLIDAY.")
            return self.statusOk,self.statusCode
        
        # If a setpoint is given for a WATER EP then raise an error.
        if self.type=='WATER' and mySetpoint!=None:
            self._setStatusCode("ERROR: Setpoint is not allowed for WATER.")
            return self.statusOk,self.statusCode 
        
        # Only transitions to BOOST can include a setpoint
        if myMode!='BOOST' and mySetpoint!=None:
            self._setStatusCode("ERROR: setpoint is not allowed with mode switch from {} to {}".format(self.mode,myMode))
            return self.statusOk, self.statusCode        
        
        # For transition to MANUAL set default MANUAL setpoint 
        if myMode=='MANUAL':
            mySetpoint=self.MANUAL_DEFAULT
        
        # For transition to BOOST set default BOOST setpoint         
        if myMode=='BOOST' and mySetpoint==None:
            mySetpoint=self.BOOST_DEFAULT
        
        # If we are currently in BOOST then we have special case where back button can cancel BOOST
        # Get the appropriate previous mode and setpoints.
        if myMode=='BOOST_CANCEL' and self.mode=='BOOST':
            myMode=self.lastMode()
            if self.type=='HEAT':
                mySetpoint=tt.temperatureHexStringToFloat(self.previousHeatSetpoint)
        
        # Set the wanted mode
        respState,_,respValue = AT.setMode(self.nodeId, self.epId, myMode, self.type, mySetpointFloat=mySetpoint, myDuration=myDuration)
        if not respState:
            self._setStatusCode("ERROR: setMode(), {}".format(respValue))
            return self.statusOk, self.statusCode
            
        # CODE FROM HERE DOWN IS TO UPDATE THE MODEL
       
        # In model - save old settings if transition is to BOOST
        if self.model.mode!='BOOST' and myMode=='BOOST':
            # If HEAT EP and mode is MANUAL then save the setpoint
            # If HEAT EP and any other mode then lastSetpoint is set to FFFF (invalid)
            # If water then don't use the lastSetpoint
            if self.type=='HEAT':
                if self.model.mode=='MANUAL':
                    self.model.lastSetpoint=self.model.occupiedHeatingSetpoint
                else:
                    self.model.lastSetpoint='FFFF'
                
            if self.model.mode=='OVERRIDE':
                self.model.lastMode='AUTO'
            else:
                self.model.lastMode=self.model.mode        
       
        # If transition is from BOOST to another mode then reset modeExpire
        if self.model.mode=='BOOST':
            self.model.modeExpire=None
       
        # Update model mode, 
        self.model.mode=myMode

        # Switch to OFF
        if myMode=='OFF' and self.type=='HEAT':
            mySetpoint=1
            self.model.occupiedHeatingSetpoint=tt.temperatureFloatToHexString(mySetpoint)
        
        # Switch to MANUAL
        elif myMode=='MANUAL' and self.type=='HEAT':
            if mySetpoint==None: mySetpoint=self.MANUAL_DEFAULT
            self.model.occupiedHeatingSetpoint=tt.temperatureFloatToHexString(mySetpoint)
        
        # Switch to AUTO sets setpoint to schedule setpoint
        # the model status check will select the correct setpoint.
        elif myMode=='AUTO' and self.type=='HEAT':
            mySetpoint=scheduleSetpoint
            self.model.occupiedHeatingSetpoint=scheduleSetpoint
        
        # Switch to BOOST sets setpoint and an expire time   
        elif myMode=='BOOST':
            if mySetpoint==None: mySetpoint=self.BOOST_DEFAULT
            if self.type=='HEAT': self.model.occupiedHeatingSetpoint=tt.temperatureFloatToHexString(mySetpoint)            
            self.model.modeExpire = nowTime + datetime.timedelta(hours=myDuration)
            # myDuration=2 means a 2 minute test boost
            if myDuration==0:
                self.model.modeExpire = nowTime + datetime.timedelta(minutes=2)
        
        # Wait for mode and setpoint to be confirmed.
        self._checkSettingsPropagated()

        return self.statusOk,self.statusCode
    def setSetpoint(self,mySetpoint):
        """ Set the setpoint for the thermostat
        
        """
        self.statusOk=True
        self.statusCode=[]
        
        nowTime=getTestTime(timeOffset)
        
        # Exit if the given setpoint is not within valid range
        if not mySetpoint in self.allowedSetpoints:
            self._setStatusCode("ERROR: Setpoint must be 1'C or in range {}-{}'C. sp={}".format(self.minSetpoint,self.maxSetpoint,mySetpoint))
            return self.statusOk,self.statusCode
        
        # Setpoint changes are not allowed in Holiday Mode
        if self.mode=='HOLIDAY':
            self._setStatusCode("ERROR: Setpoint changes in HOLIDAY MODE are not allowed")
            return self.statusOk,self.statusCode
        
        # Return if endpoint type is for WATER.  Setpoint changes for water are not valid.
        if self.type=='WATER':
            self._setStatusCode('ERROR: Setpoint change for WATER endpoint is not a valid operation')
            return self.statusOk,self.statusCode
        
        # Setting a HEAT setpoint from OFF changes the mode to MANUAL (knob rotate in OFF mode).
        if self.mode=='OFF':
            respState, respVal = self.setMode('MANUAL')
            if not respState:
                # setMode already set the fail status so just return.
                return self.statusOk,self.statusCode
            respState,_,respVal = AT.setSetpoint(self.nodeId, self.epId, mySetpoint)
            if not respState:
                self._setStatusCode("ERROR: setSetpoint() failed. {}".format(respVal))
                return self.statusOk,self.statusCode
            # Update the model
            self.model.mode='MANUAL'
            self.model.occupiedHeatingSetpoint=tt.temperatureFloatToHexString(mySetpoint)
        
        elif self.mode=='MANUAL':
            respState,_,respValue = AT.setSetpoint(self.nodeId, self.epId, mySetpoint)
            if not respState:
                self._setStatusCode("ERROR: setSetpoint() failed. {}".format(respValue))
                return self.statusOk,self.statusCode
            # Update the model
            self.model.occupiedHeatingSetpoint=tt.temperatureFloatToHexString(mySetpoint)             
        
        # If in AUTO, OVERRIDE or BOOST
        elif self.mode=='AUTO' or self.mode=='OVERRIDE' or self.mode=='BOOST':
            # Make a note of current time and then change the setpoint
            respState,_,respValue = AT.setSetpoint(self.nodeId, self.epId, mySetpoint)
            if not respState:
                self._setStatusCode("ERROR: setSetpoint() failed. {}".format(respValue))
                return self.statusOk,self.statusCode
            
            # Update the model mode (if necessary),  setpoint and mode expire time.
            # If in AUTO mode now then setting a setpoint switches to OVERRIDE.
            if self.mode=='AUTO':
                self.model.mode='OVERRIDE'            
            self.model.occupiedHeatingSetpoint = tt.temperatureFloatToHexString(mySetpoint)
            self.model.modeExpire = self.model.getNextEvent(nowTime)

        # Wait for mode and setpoint to be confirmed.
        self._checkSettingsPropagated()
                       
        return self.statusOk,self.statusCode
    def setSchedule(self,schedule, boolStandaloneMode = False):
        """ Sets the schedule for the thermostat.
            Schedule is a list of Zigbee payload strings of the form
           
            Each day may have 1-N events
           
            {'sun':[('HH:MM',sp1), ('HH:MM',sp1) ,(),(),(),()]
             'mon':[('HH:MM',sp1), ('HH:MM',sp1) ,(),(),(),()]
             .
             .
             'sat':[('HH:MM',sp1), ('HH:MM',sp1) ,(),(),(),()]
            }           
            
        """
        # Check that number of payloads does not exceed max (for 7 days).
        for d in schedule:
            if len(schedule[d])!=self.maxNumEvents:
                self._setStatusCode('ERROR: setSchedule() must have {} events per day'.format(self.maxNumEvents))
                return self.statusOk,self.statusCode
                
        # Send the new schedule to the thermostat
        for d in schedule:
            payload = self._createZigbeeSchedulePayloadDay(schedule[d])

            respState,_,respVal = AT.setWeeklySchedule(self.nodeId, self.epId, '0201', days[d], payload, boolStandaloneMode)
            if not respState:
                self._setStatusCode('ERROR: setWeeklySchedule() has failed. {}'.format(respVal))
                print("ERROR")
                return self.statusOk,self.statusCode
        
        # Update the model
        self.model.weeklySchedule=self.getSchedule()
        
        # Wait for changes to propagate
        self._checkSettingsPropagated()
        
        return self.statusOk,self.statusCode
    def setFrostProtectionDefault(self,fpSetpoint):
        """ Set the FP default attribute to the given value
        
            1. No need to check gz as no event driven FP settings occur in the device
            2. Check the given value is in the valid range
            3. Set the given FP default.
            4. Confirm ok via an update()
            
        """
        # Check the given value is in the valid range for FP setpoints
        if not fpSetpoint in self.allowedFpDefaults:
            self._setStatusCode("Frost protection default not a valid value. {}".format(fpSetpoint))
            return self.statusOk,self.statusCode

        # Set the FP Default
        attrVal = tt.temperatureFloatToHexString(fpSetpoint)
        myClust,_ = zcl.getClusterNameAndId("BG Cluster")
        attrId,_,attrType = zcl.getAttributeNameAndId("BG Cluster", "frostProtectionSetpoint")
        
        respState,_,respVal=AT.setAttribute(self.nodeId,
                                            self.epId,
                                            myClust,
                                            'server',
                                            attrId,
                                            attrType,
                                            attrVal)
        if not respState:
            self._setStatusCode("setFrostProtection() has failed. {}".format(respVal))
            return self.statusOk,self.statusCode
        
        # Update the model
        self.model.frostProtectionSetpoint=attrVal
        
        # Wait for changes to propagate
        self._checkSettingsPropagated()
        return self.statusOk,self.statusCode
    def setHoliday(self,startDatetime,endDatetime,setpoint):
        """ Sets up a holiday on the device.
        
        """
        # Check we are on the heatEP.  Holiday attributes reside on that endpoint only.
        if self.type!='HEAT':
            self._setStatusCode("Holiday mode commands only supported on HEAT endpoint.")
            return self.statusOk,self.statusCode
                
        # Not planning any other checking at present (e.g. not checking that startDate/Time is
        # before endDateTime and that all dates are in the future.
        startDateString=datetime.datetime.strftime(startDatetime,"%Y%m%d")
        startTimeString=datetime.datetime.strftime(startDatetime,"%H:%M")
        startTimeHex=tt.timeStringToHex(startTimeString)
        
        endDateString=datetime.datetime.strftime(endDatetime,"%Y%m%d")
        endTimeString=datetime.datetime.strftime(endDatetime,"%H:%M")
        endTimeHex=tt.timeStringToHex(endTimeString)        
        
        setpoint = tt.temperatureFloatToHexString(setpoint)
        
        params = {'holidayStartDate':startDateString,
                  'holidayStartTime':startTimeHex,
                  'holidayEndDate':endDateString,
                  'holidayEndTime':endTimeHex,
                  'holidaySetpoint': setpoint}
        
        # Set the individual attributes.
        clustId = 'FD00'
        
        for k in params:
            attrId,attrName,attrType = zcl.getAttributeNameAndId(clustId, k)
            attrVal = params[k]
            respState,respCode,respValue = AT.setAttribute(self.nodeId,
                                                           self.epId,
                                                           clustId,
                                                           'server',
                                                           attrId,
                                                           attrType,
                                                           attrVal)
            
            if (not respState) or (respCode!=zcl.statusCodes['SUCCESS']):
                self._setStatusCode("Not able to set Holiday Attribute {}. {}".format(attrName,respValue))
                return self.statusOk,self.statusCode
                
        # Set holiday mode enabled.
        attrId,attrName,attrType = zcl.getAttributeNameAndId(clustId, 'holidayModeEnabled')
        attrVal = '01'
        respState,respCode,respValue = AT.setAttribute(self.nodeId,
                                                       self.epId,
                                                       clustId,
                                                       'server',
                                                       attrId,
                                                       attrType,
                                                       attrVal)
        
        if not respState:
            self._setStatusCode("Not able to set holidayModeEnabled Attribute. {}".format(respValue))
            return self.statusOk,self.statusCode
        
        # Update the model parameters
        # holidayActive is infered from start/end datetimes and we allow an error to occur if our inferred answer
        # does not match the actual settings in the tstat
        self.model.holidayModeEnabled='01'
        self.model.holidayModeStart=self._buildHolidayDatetimeUTC(params['holidayStartDate'], params['holidayStartTime'])
        self.model.holidayModeEnd=self._buildHolidayDatetimeUTC(params['holidayEndDate'], params['holidayEndTime'])
        self.model.holidayModeSetpoint=params['holidaySetpoint']
        
        # Wait for mode and setpoint to be confirmed.
        self._checkSettingsPropagated()
        
        return self.statusOk,self.statusCode
    def cancelHoliday(self):
        """ Clear the holidayModeEnabled attribute to exit HOLIDAY mode and return to 
            previous heat/water mode.
        
        """
        # Check we are on the heatEP.  Holiday attributes reside on that endpoint only.
        if self.type!='HEAT':
            self._setStatusCode("Holiday mode commands only supported on HEAT endpoint.")
            return self.statusOk,self.statusCode
        
        # Check that holiday mode is enabled
        if self.parentTstat.heatEP.holidayModeEnabled != '01':
            self._setStatusCode("ERROR: Holiday mode is not enabled.")
            return self.statusOk, self.statusCode
    
        # Build and send the cancel command
        clustId='FD00'
        attrId,attrName,attrType = zcl.getAttributeNameAndId(clustId, 'HolidayModeEnabled')
        attrVal='00'
        respState,respValue = AT.setAttribute(self.nodeId,
                                              self.epId,
                                              clustId,
                                              'server',
                                              attrId,
                                              attrType,
                                              attrVal)
        
        if not respState:
            self._setStatusCode("Not able to clear holidayModeEnabled attribute {}. {}".format(attrName,respValue))
            return self.statusOk,self.statusCode
        
        # Update the model.
        self.model.mode = self.model.lastMode()
        self.model.setpoint = tt.temperatureHexStringToFloat(self.model.lastSetpoint)
        
        # Wait for mode and setpoint to be confirmed.
        self._checkSettingsPropagated()
        
        return self.statusOk,self.statusCode
        
    """ Public Get Methods """
    def getSchedule(self):
        return self._weeklySchedule
       
    """ Private Methods """
    def _checkSettingsPropagated(self):
        """ Wait for settings to propagate or timeout and warn if in guard zone.
        
        """
        startTime=getTestTime(timeOffset)
        self.update()
        while not self.statusOk:
            # If we have timeout then exit.
            nowTime = getTestTime(timeOffset)
            if nowTime>startTime+COMMAND_TIMEOUT:
                inGuardZone,remainingSeconds,eventName=self.model._guardZone(nowTime)
                myError='ERROR: Timeout. Settings have not propagated correctly. guardzone={}, eventName={}, remainingSeconds={}'.format(inGuardZone,
                                                                                                                                         eventName,
                                                                                                                                         remainingSeconds)
                self._setStatusCode(myError)
                return False
            time.sleep(1)
            
            # Update and loop round again to see if states have resolved.
            self.update()
        return True
    def _updateThermostatEp(self):
        """ Update the state variables from REDIS cache and update mode states based on those
            state variables.
            
        """
        # We get the latest value from REDIS cache
        self._systemMode = self._getAttributeFromRedis(self.epId,'Thermostat Cluster','systemMode')        
        self._temperatureSetpointHold = self._getAttributeFromRedis(self.epId,'Thermostat Cluster','temperatureSetpointHold')
        self._temperatureSetpointHoldDuration = self._getAttributeFromRedis(self.epId,'Thermostat Cluster','temperatureSetpointHoldDuration')
        self.thermostatRunningState = self._getAttributeFromRedis(self.epId,'Thermostat Cluster','thermostatRunningState')
        
        if self.type=='HEAT':
            # Update Tstat cluster attrs
            self.localTemperature = self._getAttributeFromRedis(self.epId,'Thermostat Cluster','localTemperature',)
            self.occupiedHeatingSetpoint = self._getAttributeFromRedis(self.epId,'Thermostat Cluster','occupiedHeatingSetpoint')    
            ep = self
            
        if self.type=='WATER':
            ep = self.parentTstat.heatEP

        # Force attribute reads of previous Mode attributes to update REDIS (these attrs are not reported automatically on change)
        ep._initialiseAttribute('BG Cluster', 'previousHeatMode')
        ep._initialiseAttribute('BG Cluster', 'previousWaterMode')
        ep._initialiseAttribute('BG Cluster', 'previousHeatSetpoint')
        ep._previousHeatMode = ep._getAttributeFromRedis(ep.epId,'BG Cluster', 'previousHeatMode')
        ep._previousWaterMode = ep._getAttributeFromRedis(ep.epId,'BG Cluster', 'previousWaterMode')            
        ep.previousHeatSetpoint = ep._getAttributeFromRedis(ep.epId,'BG Cluster', 'previousHeatSetpoint')
        ep.frostProtectionSetpoint = ep._getAttributeFromRedis(ep.epId,'BG Cluster','frostProtectionSetpoint')
            
        # Update holiday mode attrs and derived variables
        ep.holidayModeEnabled = ep._getAttributeFromRedis(ep.epId,'BG Cluster', 'holidayModeEnabled')
        ep.holidayModeActive = ep._getAttributeFromRedis(ep.epId,'BG Cluster', 'holidayModeActive')
        ep.holidaySetpoint = ep._getAttributeFromRedis(ep.epId,'BG Cluster', 'holidaySetpoint')            
        ep._holidayStartDate = ep._getAttributeFromRedis(ep.epId,'BG Cluster', 'holidayStartDate')
        ep._holidayStartTime = ep._getAttributeFromRedis(ep.epId,'BG Cluster', 'holidayStartTime')
        ep._holidayEndDate = ep._getAttributeFromRedis(ep.epId,'BG Cluster', 'holidayEndDate')
        ep._holidayEndTime = ep._getAttributeFromRedis(ep.epId,'BG Cluster', 'holidayEndTime')
        
        # Update the mode (AUTO, MANUAL etc)
        self._updateMode()        
        
        if ep.holidayModeEnabled=='01' and ep._holidayStartDate!='' and ep._holidayStartTime!='FFFF' and ep._holidayEndDate!='' and ep._holidayEndTime!='FFFF':
            ep.holidayStart=ep._buildHolidayDatetimeUTC(ep._holidayStartDate, ep._holidayStartTime)
            ep.holidayEnd=ep._buildHolidayDatetimeUTC(ep._holidayEndDate, ep._holidayEndTime)
        else:
            ep.holidayStart=None
            ep.holidayEnd=None
            
        # Update this schedule from REDIS
        self._getScheduleFromRedis()

        return self.statusOk,self.statusCode
    def _updateMode(self):
        """ Determine the operating mode based on the current state variables
        
        """
        # List defined states here.  Raise an error for any other combinations
        self.mode=None
        
        if self._systemMode=='04' and self._temperatureSetpointHold=='00' and self._temperatureSetpointHoldDuration=='0000':   # AUTO mode
            self.mode='AUTO'
        elif self._systemMode=='04' and self._temperatureSetpointHold=='01' and self._temperatureSetpointHoldDuration!='FFFF': # AUTO O/R mode
            self.mode='OVERRIDE'
        elif self._systemMode=='04' and self._temperatureSetpointHold=='01' and self._temperatureSetpointHoldDuration=='FFFF': # Manual Mode
            self.mode='MANUAL'
        elif self._systemMode=='05' and self._temperatureSetpointHold=='01' and self._temperatureSetpointHoldDuration!='FFFF': # BOOST Mode
            self.mode='BOOST'
        elif self._systemMode=='00' and self._temperatureSetpointHold=='00' and self._temperatureSetpointHoldDuration=='0000': # OFF MODE
            self.mode='OFF'
        else:
            self._setStatusCode("WARNING: Mode attributes invalid.  Mode not known.")
        
        # Holiday mode overrides the rest
        if self.type=='HEAT':
            if self.holidayModeActive=='01' and self._systemMode=='04' and \
               self._temperatureSetpointHold=='01' and self._temperatureSetpointHoldDuration=='FFFF':
                    self.mode='HOLIDAY'
        
        if self.type=='WATER':
            if self.parentTstat.heatEP.holidayModeActive=='01' and self._systemMode=='00' and \
               self._temperatureSetpointHold=='00' and self._temperatureSetpointHoldDuration=='0000':
                    self.mode='HOLIDAY'
        
        if self.mode==None:
            self._setStatusCode("WARNING: Mode attributes invalid.  Mode not known.")

        return
    def _initialiseAttribute(self,myClustName,myAttrName):
        """ Initialise the variable by a zigbee attribute get.
        
        """
        # Send the zigbee command to get the value
        clustId,_ = zcl.getClusterNameAndId(myClustName)
        attrId,_,_ = zcl.getAttributeNameAndId(clustId, myAttrName)
        respState,_,respVal = AT.getAttribute(self.nodeId,self.epId, clustId, attrId, 'server')
        if not respState:
            raise zigbeeError("ERROR: getAttribute() failed, {}".format(respVal))
        return respVal
    def _setStatusCode(self, myError):
        """ Add the myError string to tstat statusCode if there is an error state
            
        """
        if self.statusOk==True:
            # Set first error state
            self.statusOk=False
            self.statusCode.append("TSTAT: {}".format(myError))
        else:
            # Model already in error state so concatenate current error.
            self.statusCode.append(myError)
        return
    def _buildHolidayDatetimeUTC(self,myDate,myTime):
        """ Return a UTC datetime for the given date and time strings
        
        """
        myTime=tt.timeHexToString(myTime)
        dtString = "{} {}".format(myDate,myTime)
        myDT = datetime.datetime.strptime(dtString,'%Y%m%d %H:%M')
        myUTC = tt.getEventUtcTime(myDT)
        return myUTC
    """ REDIS Handling methods """
    def _getAttributeFromRedis(self,myEpId,myClusterName,myAttributeName):
        """ Retrieve the value for the given attribute form REDIS
         
        """
        # Build the REDIS key
        clustId,_ = zcl.getClusterNameAndId(myClusterName)
        attrId,_,_ = zcl.getAttributeNameAndId(clustId, myAttributeName)
            
        redisKey="{0},{1},{2},{3}".format(self.nodeId,myEpId,clustId,attrId)
        attrVal = r.get(redisKey)
        if attrVal == None:
            raise zigbeeError('{}, ERROR: No REDIS entry for attribute'.format(myAttributeName))
        else:
            attrVal = attrVal.decode()
        return attrVal
    def _getScheduleFromRedis(self):
        """ Retrieve REDIS schedule entries.  One for each day of week.
            Returns that in the instance _weeklySchedule object 
        
        """
        for day in days:
            dayBitmap = days[day]
            
            redisKey="{0},{1},{2},{3}".format(self.nodeId,self.epId,'0201','sched'+dayBitmap)
            schedVal = r.get(redisKey)
            if schedVal == None:
                raise zigbeeError("ERROR: No REDIS entry for schedule")
            else:
                schedVal = schedVal.decode()
                schedDay = self._parseZigbeeSchedule(schedVal)
        
            self._weeklySchedule[day] = schedDay
        return 0
    """ Zigbee schedule methods """
    def _createZigbeeSchedulePayloadDay(self,schedule):
        """ Create a string schedule object suitable for sending via setWeeklySchedule (zigbee command).
            Contains only the time/temperature pairs for one day.
            
            Schedule is a list of tuples (one tuple per event).  Tuple of the form (time,setpoint) e.g.
            ('16:15',20.5)
             
        """
        zbSchedule=''
        for event in schedule:
    
            timeHexStr = tt.timeStringToHex(event[0])
            timeHexStr = byteSwap(timeHexStr)
    
            temperature = tt.temperatureFloatToHexString(event[1])
            temperature = byteSwap(temperature)
    
            zbSchedule=zbSchedule+timeHexStr+temperature
            
        return zbSchedule
    def _createZigbeeSchedulePayloadWeek(self,schedule):
        """ Create a list of payloads (one for each day)
        
        """    
        schedPayloads = {}
        for day in schedule:
            daySched = schedule[day]
            schedPayload = self._createZigbeeSchedulePayloadDay(daySched,day)
            schedPayloads[day]=schedPayload
        return schedPayloads
    def _parseZigbeeSchedule(self,schedVal):
        """
        """
        eventList=[]
        events=splitString(schedVal, 8)
        for event in events:
            time=tt.timeHexToString(event[:4])
            temp=tt.temperatureHexStringToFloat(event[4:])
            eventList.append((time,temp))
        return eventList
class thermostatEndpointModel(object):
    """ Class to represent a simulated Thermostat.  Holds the current expected state of a thermostat
        mode and schedule.  Pass a thermostat object to this at initialisation so that the model can
        synchrosise states.
    
    """
    def __init__(self,thermostatEndpoint):
        
        # Store a reference to the thermostat endpoint that we are modeling
        self.parentEp = thermostatEndpoint
        
        # Thermostat Mode - AUTO,MANUAL,OVERRIDE,OFF,BOOST
        self.mode = self.parentEp.mode
        
        # Relay state
        self.thermostatRunningState = self.parentEp.thermostatRunningState

        # We don't replicate localTemperature because there is no model for that.
        # For water we dont replicate occupiedHeatingSetpoint as it's not used for water. 
        if self.parentEp.type=='HEAT':
            self.occupiedHeatingSetpoint = self.parentEp.occupiedHeatingSetpoint
        
        # Frost protection default 
        if self.parentEp.type=='HEAT':
            self.frostProtectionSetpoint = self.parentEp.frostProtectionSetpoint
            
        # Weekly Schedule
        self.weeklySchedule = dict(self.parentEp.getSchedule())
        
        # Last mode/setpoint
        self.lastMode=self.parentEp.lastMode()
        if self.parentEp.type=='HEAT':
            self.lastSetpoint=self.parentEp.previousHeatSetpoint
        
        # If already in BOOST or OVERRIDE then initialise mode expire.
        if self.mode=='BOOST' or self.mode=='OVERRIDE':
            spHoldMinutes = tt.timeHexToMinutes(self.parentEp._temperatureSetpointHoldDuration)
            self.modeExpire=getTestTime(timeOffset) + datetime.timedelta(minutes=spHoldMinutes)
        else:
            self.modeExpire = None
        
        # Holiday Attributes      
        if self.parentEp.type=='HEAT':
            ep = self.parentEp

            # Note we don't have holidayModeActive because we set mode variable to HOLIDAY.
            self.holidayModeEnabled = ep.holidayModeEnabled        
            self.holidayModeStart = ep.holidayStart
            self.holidayModeEnd = ep.holidayEnd
            self.holidayModeSetpoint = ep.holidaySetpoint

        return
    """ Public Methods """
    def checkModel(self):
        """ Check that thermostat state is consistent with the model state.
            If not then return false.
                
            Confirm mode is as expected.
                Check if BOOST, OVERRIDE or HOLIDAY have expired.
                Check if a HOLIDAY has started (save lastModes and heat setpoint if it has)
                Simple match on mode between model and actual since we update the model when we change the mode on actual.
            
            Confirm weeklySchedule is as expected.
                Simple match.
                
            Confirm frostProtectionSetpoint is as expected.
                Simple match.
                
            Confirm setpoint is as expected.
                if mode is OFF then setpoint is frostProtection
                if mode is AUTO then get setpoint from schedule
                if mode is OVERRIDE then setpoint is last given setpoint, until next event in schedule then setpoint resets to schedule
                if mode is MANUAL then setpoint is last given setpoint (persistant until mode changes)
            
            Confirm relay state is as expected.
                if temperature >= setpoint then relay OFF
                if temperature < setpoint then relay ON
            
            Confirm previousMode and previousSetpoint is as expected.
                Simple match.
            
            Confirm HOLIDAY mode is as expected.
                if holidayEnabled and holidayStart<=date<holidayEnd then
                    set model holidayActive
                    set model setpoint == model holidaySetpoint
                    
                if holidayEnabled and date>=holidayEnd then 
                    clear holidayActive and holidayEnabled.
                    if heat then:
                        set modelHeatMode = model previousHeatMode
                        set modelWaterMode = model previousWaterMode
                    if water then:
                        set modelSetpoint = model previousSetpoint
                
                Check holidayEnabled and holidayActive match.
                Check holidayStart and holidayEnd match.  << Not sure what these are set to when holiday expires.
                
        """
        # Setpoint calculations need events and times from schedule
        nowTime = getTestTime(timeOffset)
        scheduleSetpoint,_,_ = self._eventStatus(nowTime)
        
        # Check we have a valid mode     
        assert self.mode in self.parentEp.allowedModes
        
        holidayModeEnabled = self.parentEp.parentTstat.heatEP.model.holidayModeEnabled
        holidayModeStart = self.parentEp.parentTstat.heatEP.model.holidayModeStart
        holidayModeEnd = self.parentEp.parentTstat.heatEP.model.holidayModeEnd
        holidayModeSetpoint = self.parentEp.parentTstat.heatEP.model.holidayModeSetpoint

        # First check if any modes have expired.
        if ((self.mode=='BOOST' or self.mode=='OVERRIDE') and nowTime>=self.modeExpire) or \
           (self.mode=='HOLIDAY' and nowTime>=holidayModeEnd):
            # Deal with the mode
            if self.lastMode=='OVERRIDE': self.lastMode='AUTO'
            self.mode=self.lastMode
            
            # Deal with HEAT setpoints
            if self.parentEp.type=='HEAT':
                if self.lastMode=='OFF':
                    self.occupiedHeatingSetpoint=1
                elif self.lastMode=='AUTO':
                    self.occupiedHeatingSetpoint=scheduleSetpoint 
                elif self.lastMode=='MANUAL':
                    print("DEBUG: Last setpoint={}".format(self.lastSetpoint))
                    self.occupiedHeatingSetpoint=self.lastSetpoint

            # Reset the expire time
            self.modeExpire=None
            
            # Reset holidayModeEnabled
            self.parentEp.parentTstat.heatEP.model.holidayModeEnabled='00' 
          
        # Check if a holiday has started
        # Tstat EP mode changes to HOLIDAY when holidayModeActive is set.
        # The model infers when HOLIDAY should start from startDate so modes should
        # match if everything switches at Start as expected.        
        if holidayModeEnabled=='01':
            # Set an error if holidayModeStart or end is None.
            if holidayModeStart==None:
                self._setStatusCode('holidayMode enabled but holidayModeStart is None.')
            elif holidayModeEnd==None:
                self._setStatusCode('holidayMode enabled but holidayModeEnd is None.')
            elif (nowTime>=holidayModeStart) and (nowTime<holidayModeEnd):
                # Save lastMode
                # Don't save if already in Holiday/Boost/Override as we'd overwrite the wanted lastModes set by
                # entering those modes (those are not valid return modes at end of Holiday).
                # lastMode and lastSetpoint are set on entry to those modes.
                if self.mode!='HOLIDAY' and self.mode!='BOOST' and self.mode!='OVERRIDE':
                    self.lastMode=self.mode
                
                # Save last setpoint only if we are entering from MANUAL.
                # This is the only mode that has a valid historical setpoint.
                # If we are returing to OFF or AUTO we don't use the previousSetpoint value.
                if self.mode=='MANUAL' and self.parentEp.type=='HEAT':
                    self.lastSetpoint=self.occupiedHeatingSetpoint
                
                # Set Holiday Mode and setpoint
                self.mode='HOLIDAY'
                if self.parentEp.type=='HEAT': self.occupiedHeatingSetpoint=holidayModeSetpoint
        
        # Check Mode
        if self.mode!=self.parentEp.mode:
            self._setStatusCode('Mode inconsistent. mode={}, expected={}'.format(self.parentEp.mode,self.mode))
            
        # Check Schedule
        if self.weeklySchedule!=self.parentEp._weeklySchedule:
            self._setStatusCode('Schedule inconsistent')
            
        # Check Frost Protections
        if self.parentEp.type=='HEAT':
            if self.frostProtectionSetpoint!=self.parentEp.frostProtectionSetpoint:
                self._setStatusCode('Frost protection setpoint inconsistent. Expected={}'.format(self.frostProtectionSetpoint))

        # If HEAT EP then check setpoints
        if self.parentEp.type=='HEAT':
            if self.mode=='OFF':
                self.occupiedHeatingSetpoint=tt.temperatureFloatToHexString(1)
                if self.occupiedHeatingSetpoint!=self.parentEp.occupiedHeatingSetpoint:
                    self._setStatusCode('Setpoint inconsistent. Expected frostProtection')
    
            elif self.mode=='AUTO':
                self.occupiedHeatingSetpoint=tt.temperatureFloatToHexString(scheduleSetpoint)
                if self.occupiedHeatingSetpoint!=self.parentEp.occupiedHeatingSetpoint:
                    self._setStatusCode('Setpoint inconsistent. Expected schedule setpoint.')
            
            elif self.mode in ['MANUAL','OVERRIDE','BOOST']:
                if self.occupiedHeatingSetpoint!=self.parentEp.occupiedHeatingSetpoint:
                    self._setStatusCode("Setpoint inconsistent. Expected setpoint = {}'C".format(tt.temperatureHexStringToFloat(self.occupiedHeatingSetpoint)))
        
        # Check Heat Relay State
        if self.parentEp.type=='HEAT':
            if self.parentEp.localTemperature<self.occupiedHeatingSetpoint:
                self.thermostatRunningState='0001'
            else:
                self.thermostatRunningState='0000'
            if self.thermostatRunningState!=self.parentEp.thermostatRunningState:
                self._setStatusCode('Heat relay states are inconsistent. Tstat={}, model={}'.format(self.parentEp.thermostatRunningState,
                                                                                                    self.thermostatRunningState))
                
        # check water relay state
        if self.parentEp.type=='WATER':
            if self.mode in ['MANUAL','BOOST']:
                # Relays are on
                self.thermostatRunningState='0001'
            if self.mode in ['OFF','HOLIDAY']:
                # Relays are off
                self.thermostatRunningState='0000'
            if self.mode=='AUTO':
                # Relays are on if event is on.
                # Water Schedules contain 0'C and 99'C to represent on/off.
                if scheduleSetpoint==0:
                    self.thermostatRunningState='0000'
                else:
                    self.thermostatRunningState='0001'
            if self.thermostatRunningState!=self.parentEp.thermostatRunningState:
                self._setStatusCode('Water relay states are inconsistent.')
                
        # Check previousMode/setpoints
        if self.mode=='BOOST' or self.mode=='HOLIDAY':
            if self.lastMode!=self.parentEp.lastMode():
                self._setStatusCode('Previous mode is inconsistent. Expected={}'.format(self.lastMode))
            if self.parentEp.type=='HEAT':
                if self.lastSetpoint!=self.parentEp.previousHeatSetpoint:
                    self._setStatusCode('Previous setpoint is inconsistent. Expected={}'.format(tt.temperatureHexStringToFloat(self.lastSetpoint)))
        
        return 0
    def getNextEvent(self,myTimeNow):
        """ Return the start time of the next event in the module schedule
        """
        _,_,nextEventTime = self._eventStatus(myTimeNow)
        return nextEventTime

    """ Private Methods """
    def _eventStatus(self,myTimeNow):
        """ From the internal schedule state, determine the current event and return
            the start time for this event (in minutes since midnight), the setpoint for the
            current event and the start time for the next event.
             
            We build a list of datetimes for each event in the schedule.
            Datetime has todays day (or yesterday/tomorrow for edge events)
            and the local time for the event (which may be BST or GMT)
            These are then converted to UTC datetimes that can be compared against current UTC time
            to determine which event we are in and time to next/last events.
       
            If we are in event 0 then last event was event 6 of yesterday.
            If we are in event 6 then next event is event 1 of tomorrow.
       
            So we build an 8 event list:
            e1(e6 yesterday),e1,e2,e3,e4,e5,e6,e7(e1 tomorrow)
       
        """
        eventListUtc,setpointList = self._buildUtcEventList()
        
        # Now work out which event we are in
        for i in range(0,8):
            if myTimeNow>=eventListUtc[i]:
                eventNumber = i
        
        currentSetpoint = setpointList[eventNumber]
        currentEventStart = eventListUtc[eventNumber]
        nextEventStart = eventListUtc[eventNumber+1]
        
        return currentSetpoint, currentEventStart, nextEventStart
    def _buildUtcEventList(self):
        """ Build an eight event list to allow time to next event to be calculated.
            Times are converted to UTC.
            
            e1(e6 yesterday),e1,e2,e3,e4,e5,e6,e7(e1 tomorrow)       
        
        """
        eventList=[]
        setpointList=[]
        today = datetime.datetime.now()
        yesterday = today - datetime.timedelta(days=1)
        tomorrow = today + datetime.timedelta(days=1)
        
        # Get e0 i.e. e6 from yesterday
        day = yesterday.strftime("%a").lower()
        timeStr = self.weeklySchedule[day][5][0]
        eventList.append(tt.timeStringToDatetimeUTC(timeStr, yesterday))
        setpointList.append(self.weeklySchedule[day][5][1])

        # Get e1-e6 from today
        day = today.strftime("%a").lower()
        for e in self.weeklySchedule[day]:
            timeStr = e[0]
            eventList.append(tt.timeStringToDatetimeUTC(timeStr, today))
            setpointList.append(e[1])
        
        # Get e7 i.e. e1 from tomorrow
        day = tomorrow.strftime("%a").lower()
        timeStr = self.weeklySchedule[day][0][0]
        eventList.append(tt.timeStringToDatetimeUTC(timeStr, tomorrow))        
        setpointList.append(self.weeklySchedule[day][0][1])
        
        return eventList,setpointList
    def _setStatusCode(self, myError):
        """ Add the myError string to model statusCode if there is an error state
            
        """
        if self.parentEp.statusOk==True:
            # Set first error state
            self.parentEp.statusOk=False
            self.parentEp.statusCode.append("MODEL ERROR: {}".format(myError))
        else:
            # Model already in error state so concatenate current error.
            self.parentEp.statusCode.append(myError)
        return
    def _guardZone(self,nowTime=None):
        """ Check if current time is within +/- seconds of the next event in the model schedule
            or the next modeExpire (End of BOOST, HOLIDAY etc)
            Used to block changes/reads around the event transition time.
            Returns true/false,remaining guardzone time (if any) in seconds and eventName for the event we are
            close to.  None if not in guardzone.
           
        """
        # If no time provided then use current time (suspect we should use this for all calls?)
        if nowTime==None:
            nowTime=getTestTime(timeOffset)
        _,currentEventDatetime,nextEventDatetime = self._eventStatus(nowTime)
        events={'Current schedule event start':currentEventDatetime,
                'Next schedule event start':nextEventDatetime,
                'Boost or Override mode expire':self.modeExpire}
        #=======================================================================
        # events={'Current schedule event start':currentEventDatetime,
        #         'Next schedule event start':nextEventDatetime,
        #         'Boost or Override mode expire':self.modeExpire,
        #         'Holiday start':self.holidayModeStart,
        #         'Holiday end':self.holidayModeEnd
        #         }
        #=======================================================================
        
        guardZoneSeconds = 30
        inBand,remainingSeconds,eventName=tt.checkGuardZone(nowTime, events, guardZoneSeconds)
        
        return inBand,remainingSeconds,eventName

""" Custom Exception """
class zigbeeError(Exception):
    def __init__(self,value):
        self.value=value
    def __str__(self, *args, **kwargs):
        return Exception.__str__(self, *args, **kwargs)

""" Tstat Wrappers """
def wrapTstatUpdate(tstat):
    """
    """
    respStatus,respVal = tstat.update()
    if not respStatus:
        print(respStatus, respVal)
        exit()
    return
def wrapSetMode(ep,mode,setpoint=None,duration=1):
    """
    """
    respStatus, respVal = ep.setMode(mode,setpoint,duration)
    if not respStatus:
        print(respStatus, respVal)
        exit()
    return
def wrapSetSetpoint(ep,setpoint):
    """
    """
    respStatus,respVal = ep.setSetpoint(setpoint)
    if not respStatus:
        print(respStatus, respVal)
        exit()
    return
def wrapSetSchedule(ep,schedule):
    """
    """
    respStatus,respVal = ep.setSchedule(schedule)
    if not respStatus:
        print(respStatus, respVal)
        exit()
    return    
def wrapSetFrostProtection(ep,fpDefault=7):
    """ Set the frost protection default setpoint
    
    """
    respState,respVal = ep.setFrostProtectionDefault(fpDefault)
    if not respState:
        print(respVal)
        exit()
    return 

""" Helper methods """
def byteSwap(myString):
    first = myString[0:2]
    last = myString[2:4]
    return last+first
def splitString(myString, length):
    return [myString[i:i+length] for i in range(0, len(myString), length)]
def getTestTime(myTimeOffset):
    """ Return a time offset from UTC by myTimeOffset
    
    """
    return datetime.datetime.utcnow() + myTimeOffset
 
""" Raw schedule methods 
    
    buildRandomSchedule - creates a sched for today with random setpoints. First event starts at next 15mins boundary.
    packSixEventScheduel - stuffs the day schedule into 6 events i.e. pads an n-event schedule to a 6 event schedule.
    buildWeeklySchedule - copies the day schedule into all 7 days. 

"""
def buildRandomSchedule(epType,numberOfEvents,currentTemperature,eventLength=15):
    """ Build a schedule for today with given numberOfEvents and eventLength.  Schedule event 1 is rounded to next 15mins.
        
        Returns a list of N datetime events and temperatures. [(dt1,sp1), (dt2,sp2), (dt3,sp3)...]
        
        Events will alternate heat demand by setting setpoints of Current temperature +/- 5'C
        Event heat demand is selected randomly true/false.
        For each HDoff event we randomly select a setpoint of either:
            currentTemp-5'C
                or..
            Frost protection
         
        First event time will be next nearest whole minute + holdoff (say 5 minutes) to allow test to be setup.
        
        Water setpoints are either 0 or 99.  Magic numbers for OFF and ON.
        
    """
    # Build a list of setpoints.
    # First make a list of the correct length with random boolean values for heat demand
    hd=[]
    for i in range(0,numberOfEvents):
        hd.append(random.choice([True, False]))
 
    # Now get current time rounded to nearest 15mins.
    currentTime = datetime.datetime.now()
    nextEventTime = tt.roundTimeUp(currentTime,15*60)
    # if time has rolled into next day then subract a day to bring it back.
    if nextEventTime.day > currentTime.day:
        nextEventTime = nextEventTime.replace(day=currentTime.day)
    
    # Now deal with the currentTemperature
    currentTemperature=round(int(currentTemperature,16)/100)  # Round to nearest degree is good enough
        
    # Now make the real setpoint list.
    setpoints = []
    fpSetpoint = 1  
    for i in range(0,numberOfEvents):
        if hd[i]:
            # Generate a random setpoint (in 0.5'C steps) where
            # (currentTemp+5) <= N <= 32
            sp = random.randint((currentTemperature+5)*2,64)/2
            # Generate a random setpoint (in 0.5'C steps) where
            # 5 <= N <= (currentTemperature-5)
            if epType=='WATER': sp=99
            setpoints.append((nextEventTime,sp))
        else:
            frost = random.choice([True, False])
            offSetpoint = random.randint(10,(currentTemperature-5))/2
            if epType=='WATER':
                offSetpoint=0
                fpSetpoint=0
            if frost:
                setpoints.append((nextEventTime,fpSetpoint))
            else:
                setpoints.append((nextEventTime,offSetpoint))
        
        # Increment nextEventTime by 15mins.
        nextEventTime = (nextEventTime + datetime.timedelta(minutes=15)).replace(day=currentTime.day)
    
    setpoints=sorted(setpoints)
    setpointsStr = [] 
    for sp in setpoints:
        setpointsStr.append(("{:02}:{:02}".format(sp[0].hour,sp[0].minute),sp[1]))

    return setpointsStr
def packSixEventSchedule(rawSchedule):
    """ Pack a given schedule of 1-6 events into a 6 event schedule
    
        For schedule lengths less than 6 events there are multiple ways 
        of inserting the events into the schedule.  This is done
        randomly.
         
        Returns a packed 6 event schedule.  Unused events are set to
        same start time as the next highest active event.
    
        schedule packing variations:
        
        1 event = all 6 events have same time. Event6 is the active event.
        
        2 events = Event1,6
                   Event2,6
                   Event3,6
                   Event4,6
                   Event5,6
    
        3 events = Event1,2,6
                   Event1,3,6
                   Event1,4,6
                   Event1,5,6
                   
                   Event2,3,6
                   Event2,4,6
                   Event2,5,6
                   
                   Event3,4,6
                   Event3,5,6
                   
                   Event4,5,6
                   
        4 events = Event1,2,3,6
                   Event1,2,4,6
                   Event1,2,5,6
                   
                   Event1,3,4,6
                   Event1,3,5,6
                   
                   Event1,4,5,6
                   
                   Event2,3,4,6
                   Event2,3,5,6
                   
                   Event2,4,5,6
                   
                   Event3,4,5,6
                   
        5 events = Event1,2,3,4, ,6
                   Event1,2,3, ,5,6
                   Event1,2, ,4,5,6 
                   Event1, ,3,4,5,6
                   Event ,2,3,4,5,6
                   
        Algorithm is as follows:
        
        For an n-event schedule we need to pack n-events into a 6 event ZB schedule.
        
        Last event in schedule is placed into Event6.  Copy it to all insertion positions with wanted number or lower.
        Take remaining events in reverse order.
            Randomly select an insertion position between positions..
                max=last_insertion_position-1
                min=currentEventNumber
                When inserting copy to this location and all lower numbered locations.     
        
    """   
    lastInsertionPoint = 6
    packedSchedule = [0,0,0,0,0,0]

    # Loop over rawSchedule in reverse order and insert the raw events into 
    # a 6 event schedule with padded events (if necessary)
    for rawSchedIndex, e in reversed(list(enumerate(rawSchedule))):
        
        # Calculate where to insert next event into the 6 event schedule
        if lastInsertionPoint==6:
            # This is the first one so force the insertion point to be 5
            ip = 5
        else:
            # Calculate next insertion point
            ipMax = lastInsertionPoint - 1
            ipMin = rawSchedIndex
            ip = random.randint(ipMin,ipMax)
        
        # Save the last used insertion point
        lastInsertionPoint=ip
        
        for i in range(0,ip+1):
            packedSchedule[i]=e
        
    return (packedSchedule)
def buildScheduleWeek(packedSchedule):
    """ Create a dict with a 7 day schedule, all days with same schedule
    
    """
    schedule={}
    days = ['sun','mon','tue','wed','thu','fri','sat']
    for day in days:
        schedule[day]=packedSchedule
    return schedule

""" Use this method to create a weekly schedue that can be sent to the device """
def createSchedule(epType,numberOfEvents,currentTemperatureHex,eventLength):
    """ Use schedule methods to create a 7 day schedule (same events on each day)
        Returns a DICT of the form:
        
        {'sun':[('HH:MM',sp1), ('HH:MM',sp1) ,(),(),(),()]
         'mon':[('HH:MM',sp1), ('HH:MM',sp1) ,(),(),(),()]
         .
         .
         'sat':[('HH:MM',sp1), ('HH:MM',sp1) ,(),(),(),()]
        }
    """
    rawSched = buildRandomSchedule(epType,numberOfEvents, currentTemperatureHex, eventLength)
    pack = packSixEventSchedule(rawSched)
    weekSched = buildScheduleWeek(pack)
            
    return weekSched

""" Initialise the serial Threads"""
def serialInit():
    """
    
    """
    # Reset the stop threads flag
    AT.stopThread.clear()  # Reset the threads stop flag for serial port thread and attribute listener thread.
    
    # Start the serial port read/write threads and attribute listener thread
    AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False)    
    AT.startAttributeListener(printStatus=False)
    AT.getInitialData(config.node1, fastPoll=True, printStatus=True)
    
    return

""" Test Methods """
def stateLoggingTest(tstat):
    """ Start logging attributes to REDIS.
        Print the state on the screen every 5s
        Make a random schedule change
             
    """
    while True:
        tstat.update()
        print("*********")
        print("HEAT EP:")      
        tstat.heatEP.printThermostatState()
        print("WATER EP:")
        tstat.waterEP.printThermostatState()
        time.sleep(5)
    return
def testSetSchedule(tstat):
    """ set a random Heat and Water schedule
    
    """
    sched=createSchedule('HEAT',6, tstat.heatEP.localTemperature, 15)
    tstat.heatEP.setSchedule(sched)
    tstat.heatEP.printThermostatState()

    sched=createSchedule('WATER',6, tstat.heatEP.localTemperature, 15)
    tstat.waterEP.setSchedule(sched)
    tstat.waterEP.printThermostatState()

    return 0

""" Heat Mode Tests - Use heatModeTest(), setpointChangeTest() """
def heatModeChangeTest(tstat,modeList, startMode, startSetpoint=None):
    for mode in modeList:
        #if tstat.heatEP.mode!=startMode:
        tstat.heatEP.setMode(startMode)
        if startSetpoint!=None:
            tstat.heatEP.setSetpoint(startSetpoint)
        print('Start Mode = {}, startSetpoint={}'.format(tstat.heatEP.mode,
                                                         tt.temperatureHexStringToFloat(tstat.heatEP.occupiedHeatingSetpoint)))    
        
        print('Sending mode={}, setpoint={}'.format(mode[0],mode[1]))
        
        wrapSetMode(tstat.heatEP, mode[0], mode[1])

        tstat.update()
        tstat.heatEP.printThermostatState()
    return
def heatBoostSetDurationsTest(tstatMethodTests):
    """
    """
    return
def heatModeTest(tstat):
    
    # Switch from each Mode to all other modes and if possible set a setpoint
    startMode = 'OFF'
    modeList = [('MANUAL',None),
                ('AUTO',None),
                ('BOOST',None),
                ('BOOST',29.5)]
         
    heatModeChangeTest(tstat, modeList, startMode)
    
    startMode = 'MANUAL'
    modeList = [('OFF',None),
                ('AUTO',None),
                ('BOOST',None),
                ('BOOST',27.0)]
    heatModeChangeTest(tstat, modeList, startMode)
  
    startMode = 'AUTO'
    modeList=[('OFF',None),
              ('MANUAL',None),
              ('BOOST',None),
              ('BOOST',25.5)]
    heatModeChangeTest(tstat, modeList, startMode)
  
    # OVERRIDE TEST - We set OVERRIDE by setting AUTO then a setpoint
    startMode = 'AUTO'
    startSetpoint = 25
    modeList=[('OFF',None),
              ('MANUAL',None),
              ('AUTO',None),
              ('BOOST',None),
              ('BOOST',25.5)]
    heatModeChangeTest(tstat, modeList, startMode, startSetpoint)
      
    # BOOST Mode Transitions
    startMode='BOOST'
    startSetpoint=None
    modeList=[('OFF',None),
              ('MANUAL',None),
              ('AUTO',None)]
    heatModeChangeTest(tstat, modeList, startMode, startSetpoint)
  
    # BOOST_CANCEL Transitions
    # OFF > BOOST > OFF
    # MANUAL > BOOST > MANUAL
    # OVERRIDE > BOOST > AUTO
    # AUTO > BOOST > AUTO
    time.sleep(5)
    
    print("\n**** OFF>>BOOST>>OFF")
    wrapSetMode(tstat.heatEP, 'OFF')
    #tstat.heatEP.setMode('OFF')
    tstat.heatEP.printThermostatState()
    wrapSetMode(tstat.heatEP, 'BOOST')
    tstat.heatEP.printThermostatState()    
    wrapSetMode(tstat.heatEP, 'BOOST_CANCEL')
    tstat.heatEP.printThermostatState()
 
    print("\n**** MANUAL 27 >> BOOST >> MANUAL 27")
    wrapSetMode(tstat.heatEP, 'MANUAL')
    wrapSetSetpoint(tstat.heatEP, 27)
    tstat.heatEP.printThermostatState()
    wrapSetMode(tstat.heatEP, 'BOOST',30)
    tstat.heatEP.printThermostatState()    
    wrapSetMode(tstat.heatEP, 'BOOST_CANCEL')
    tstat.heatEP.printThermostatState()
 
    print("\n**** AUTO >> BOOST >> AUTO")
    wrapSetMode(tstat.heatEP, 'AUTO')
    tstat.heatEP.printThermostatState()
    wrapSetMode(tstat.heatEP, 'BOOST',30)
    tstat.heatEP.printThermostatState()    
    wrapSetMode(tstat.heatEP, 'BOOST_CANCEL')
    tstat.heatEP.printThermostatState()

    print("\n**** OVERRIDE >> BOOST >> AUTO")
    wrapSetMode(tstat.heatEP, 'AUTO')
    wrapSetSetpoint(tstat.heatEP,27)
    tstat.heatEP.printThermostatState()
    wrapSetMode(tstat.heatEP, 'BOOST',30)
    tstat.heatEP.printThermostatState()    
    wrapSetMode(tstat.heatEP, 'BOOST_CANCEL')
    tstat.heatEP.printThermostatState()

    return 0
def setpointChangeTest(tstat):
    """ Step through all setpoints with a 1s delay between each.
             
    """
    tstat.heatEP.setMode("OFF")

    for sp in range(10,65):
        tstat.heatEP.setSetpoint(sp/2)
        tstat.heatEP.printThermostatState()
        time.sleep(1)
    return

def modeExpireTest(tstat):
    """ Set mode to BOOST, 32'C
        0 durarion is a 2 min test BOOST.
             
    """
    tstat.setMode('BOOST', 32, 0)
    startTime = getTestTime(timeOffset)   
    print("BOOST Start = {}".format(startTime))
    print("Previous Mode: {}".format(tstat.model.lastMode))
    print()
    
    testTime=getTestTime(timeOffset)
    while testTime<=startTime+datetime.timedelta(seconds=2.5*60):
        time.sleep(10)
        tstat.update()
        testTime=getTestTime(timeOffset)
        print(testTime)
        print("{},{},{},{},{},{}".format(tstat.model.modeExpire,
                                         tstat.model.mode,
                                         tstat.model.lastMode,
                                         tstat.mode,
                                         tstat.model.statusOk,
                                         tstat.model.statusCode))
        print()
    return

""" Water Mode Tests - use waterTest() (others are helper methods)"""
def waterBoostExpire(myStat,startMode):
    """ Boost for given duration from given startMode
        Timeout is 150s i.e. 2mins + 30s
    """
    wrapSetMode(myStat.waterEP, startMode)
    wrapSetMode(myStat.waterEP,'BOOST',None,0)
    
    print("*************")
    print('2min BOOST expire from BOOST>{}'.format(startMode))
    print('BOOST Start {}'.format(datetime.datetime.utcnow()))    
    
    time.sleep(130)
    timeout=datetime.datetime.utcnow() + datetime.timedelta(seconds=120)    
    myStat.update()
    while myStat.waterEP.mode=='BOOST' and datetime.datetime.utcnow()<timeout:
        time.sleep(1)
        myStat.update()
        print(myStat.statusCode)
    
    if myStat.waterEP.mode=='BOOST':
        print("TEST ERROR: Water did not exit BOOST mode.")
        exit()
    
    print('BOOST End {}'.format(datetime.datetime.utcnow()))
    print(myStat.statusOk,myStat.statusCode)
    print()
    
    return
def waterModeChangeTest(tstat,modeList, startMode):
    for mode in modeList:

        wrapSetMode(tstat.waterEP, startMode)

        print('Start Mode = {}'.format(tstat.heatEP.mode))    
        print('Sending mode={}'.format(mode))
        
        wrapSetMode(tstat.waterEP, mode)
        tstat.update()
        tstat.waterEP.printThermostatState()
    return
def waterTest(tstat):
    
    # Check we can switch to all modes
    startMode='OFF'
    modeList=['MANUAL','AUTO','BOOST','OFF']
    waterModeChangeTest(tstat, modeList, startMode)
    
#     Check BOOST CANCEL from all modes.
#     OFF > BOOST > OFF
#     MANUAL > BOOST > OFF
#     AUTO > BOOST > OFF
#     BOOST > BOOST (Should just reset the duration)

    print('************')
    print('BOOST CANCEL. OFF>BOOST>OFF')
    wrapSetMode(tstat.waterEP, 'OFF')
    wrapSetMode(tstat.waterEP, 'BOOST')
    wrapSetMode(tstat.waterEP, 'BOOST_CANCEL')
    tstat.waterEP.printThermostatState()
  
    print('************')
    print('BOOST CANCEL. MANUAL>BOOST>MANUAL')
    wrapSetMode(tstat.waterEP, 'MANUAL')
    wrapSetMode(tstat.waterEP, 'BOOST')
    wrapSetMode(tstat.waterEP, 'BOOST_CANCEL')
    tstat.waterEP.printThermostatState()
      
          
    print('************')
    print('BOOST CANCEL. AUTO>BOOST>AUTO')
    wrapSetMode(tstat.waterEP, 'AUTO')
    wrapSetMode(tstat.waterEP, 'BOOST')
    wrapSetMode(tstat.waterEP, 'BOOST_CANCEL')
    tstat.waterEP.printThermostatState()
    
    # Test BOOST expire from various start modes
    for mode in ['OFF','MANUAL','AUTO','BOOST']:
        waterBoostExpire(tstat, mode)

    return

def thrashTest(tstat):
    """
    """
    while True:
        tstat.heatEP.setMode('AUTO')
        tstat.heatEP.setMode('BOOST',30)

""" Frost Protection Setpoint Test """
def frostTest(tstat):
    """
    """
    ep = tstat.heatEP
    
    # Set through all allowed FP setpoints
    fp_set = [sp/2 for sp in range(10,25)]
    for fp in fp_set:
        print("Setting FP to {}'C".format(fp))
        wrapSetFrostProtection(ep, fp)
        input("Any key to continue")
    
    return

""" Holiday Mode Tests """

def tsPrint(myString,offset):
    """
    """
    timeFormat = '%d/%m/%Y %H:%M:%S'
    timeString = datetime.datetime.strftime(datetime.datetime.now(),timeFormat)
    
    levelOffset = ' '*offset*4
    print('{}{}:  {}'.format(levelOffset,timeString,myString))
    return

def holidayTransitionsTest(tstat,simulateTime=False):
    """ Holiday transition tests - set a holiday from all combinations of start modes.
        Check it starts, ends and check that modes return to initial modes.
          
            - From various mode combinations
                
                Water Modes:
                    OFF
                    MAN
                    AUTO
                    BOOST (OFF)
                    BOOST (MAN)
                    BOOST (AUTO)
                
                Heating Modes:
                (Note each of these scenarios should also be combined with each hot water mode)
                    OFF
                    MAN
                    AUTO
                    OVERRIDE
                    Single BOOST scenarios (shall return to original mode after BOOST completes)
                        BOOST (OFF)
                        BOOST (MAN)
                        BOOST (AUTO)
                        BOOST (OVERRIDE)
                    Double BOOST scenarios (shall return to original mode after BOOST completes)
                        OFF > BOOST > BOOST
                        MAN > BOOST > BOOST
                        AUTO > BOOST > BOOST
                        OVERRIDE > BOOST > BOOST
                
                Store modes in list of lists.  Each item is a list.  First entry in each item is the start mode.
                Subsequent entries can be BOOSTS, e.g.
                
                [['OFF'],['OFF','BOOST','BOOST']]
                    
                Test Description:
                    Set wanted heat mode, set wanted water mode
                    Confirm modes.
                    Set a holiday of duration 1min to start in one minute
                    Confirm modes switch to HOLIDAY.
                    Pause for 1min
                    Wait for 2mins (max) for modes to switch back to start modes.
    """
    waterModes=[['OFF'],
                ['MANUAL'],
                ['AUTO'],
                ['OFF','BOOST'],
                ['MANUAL','BOOST'],
                ['AUTO','BOOST']]
    
    heatModes=[['OFF'],
               ['MANUAL'],
               ['AUTO'],
               ['AUTO','OVERRIDE'],
               ['OFF','BOOST'],
               ['MANUAL','BOOST'],
               ['AUTO','BOOST'],
               ['AUTO','OVERRIDE','BOOST'],
               ['OFF','BOOST','BOOST'],
               ['MANUAL','BOOST','BOOST'],        
               ['AUTO','BOOST','BOOST'],
               ['AUTO','BOOST','BOOST']]

    print('*** Holiday mode transition checks - confirm tstat returns to correct mode after a holiday')
    print('')

    for hm in heatModes:
        for wm in waterModes:
            hStart = hm[0]
            wStart = wm[0]
           
            print('HEAT={}, WATER={}'.format(hm,wm))
            
            # Set the wanted heat mode.
            # If BOOST scenarios then set through the list (we want to check the system will return to the original state)
            for h in hm:
                if h=='OVERRIDE':
                    wrapSetMode(tstat.heatEP, 'AUTO')
                    wrapSetSetpoint(tstat.heatEP, 32)
                else:
                    wrapSetMode(tstat.heatEP,h)
                print('    HEAT={}'.format(tstat.heatEP.mode))
                
            # Set the wanted water mode
            for w in wm:
                wrapSetMode(tstat.waterEP,w)
                print('    WATER={}'.format(tstat.waterEP.mode))
            print()
            
            holidayDuration = 60  # Seconds
            holidayStartOffset = 60  # Start offset from now in seconds.
            holidayStart = (datetime.datetime.now() + datetime.timedelta(seconds=holidayStartOffset)).replace(second=0,microsecond=0)     
            holidayEnd = (holidayStart + datetime.timedelta(seconds=holidayDuration))
            holidaySetpoint=10

            tstat.heatEP.setHoliday(holidayStart,holidayEnd,holidaySetpoint)
            
            if tstat.heatEP.statusOk:
                tstat.update()
                tsPrint('Holiday Set. HEAT Mode={}, WATER Mode={}, Holiday Start={}, Holiday End={}'.format(tstat.heatEP.mode,tstat.waterEP.mode,holidayStart,holidayEnd),1)
            else:
                print(tstat.heatEP.statusOk,tstat.heatEP.statusCode)

            # Wait for holiday to start
            timeout = holidayStart + datetime.timedelta(seconds=60)
            holiday=False
            while not holiday:
                tstat.update()
                print('DEBUG: heatStatusOk ={},{}'.format(tstat.heatEP.statusOk,tstat.heatEP.statusCode))
                print('DEBUG: waterStatusOk={},{}'.format(tstat.waterEP.statusOk,tstat.waterEP.statusCode))
                if tstat.heatEP.mode=='HOLIDAY' and tstat.waterEP.mode=='HOLIDAY' and \
                   tstat.heatEP.statusOk and tstat.waterEP.statusOk:
                    holiday=True             
                if datetime.datetime.now()>timeout:
                    tsPrint('TIMEOUT: Holiday has not started',1)
                    tsPrint('HEAT Mode={}, WATER Mode={}'.format(tstat.heatEP.mode,tstat.waterEP.mode),1)
                    tsPrint('*** STOP',1)
                    exit()
                if not holiday:
                    time.sleep(10)
            
            tsPrint('Holiday started. HEAT Mode={}, WATER Mode={}'.format(tstat.heatEP.mode,tstat.waterEP.mode),1)
            
            # Check for early expire
            holiday=True
            timeout = holidayEnd - datetime.timedelta(seconds=60)
            while holiday and datetime.datetime.now()<=timeout:
                tstat.update()
                if tstat.heatEP.mode!='HOLIDAY' or tstat.waterEP.mode!='HOLIDAY':
                    tsPrint('ERROR: Holiday has ended early. HEAT={}, WATER={}'.format(tstat.heatEP.mode,tstat.waterEP.mode), 1)
                    exit()
                time.sleep(10)
            
            # Wait for holiday to expire
            timeout = holidayEnd + datetime.timedelta(seconds=60)
            holiday=True
            while holiday:
                tstat.update()
                print('DEBUG: heatStatusOk ={},{}'.format(tstat.heatEP.statusOk,tstat.heatEP.statusCode))
                print('DEBUG: waterStatusOk={},{}'.format(tstat.waterEP.statusOk,tstat.waterEP.statusCode))
                if tstat.heatEP.mode==hStart and tstat.waterEP.mode==wStart and \
                   tstat.heatEP.statusOk and tstat.waterEP.statusOk:
                    holiday=False
                if datetime.datetime.now()>timeout:                   
                    tsPrint('TIMEOUT: Holiday has not finished',1)
                    tsPrint('HEAT Mode={}, WATER Mode={}'.format(tstat.heatEP.mode,tstat.waterEP.mode),1)
                    tsPrint('*** STOP',1)
                    exit()
                if holiday:
                    time.sleep(10)
                    
            # Print end of test state                
            tsPrint('HEAT Mode={}, WATER Mode={}'.format(tstat.heatEP.mode,tstat.waterEP.mode),1)                
            tsPrint('Holiday completed correctly',1)
            print()
def main():
    
    # Initialise the serial threads
    serialInit()
    # Get Device address info
    nodeId=config.node1

    r.flushdb()

    # Create a thermostatEndpoint class instance
    print('\nBuilding thermostat object...')
    tstat = thermostatClass(nodeId)
                
    # Set a new schedule
#     sched=createSchedule('HEAT', 6, tt.temperatureFloatToHexString(25), 15) 
#     tstat.heatEP.setSchedule(sched)
    
    # Print the state to confirm
    tstat.heatEP.printThermostatState()
    tstat.waterEP.printThermostatState()
#     time.sleep(5)
#     tstat.waterEP.cancelHoliday()
#     tstat.waterEP.printThermostatState()
#     exit()
   
    """ Call the wanted test methods here """
    
    """ Holiday Mode Tests """ 
    holidayTransitionsTest(tstat, simulateTime=False)
    exit()
    
    """ Frost Protection Test """
    #frostTest(tstat)
    
    """ setSchedule() test"""
    #testSetSchedule(tstat)
    
    """ Simple state logging - watch mode change as you edit on Tstat directly. """
    #stateLoggingTest(tstat)
    
    """ Heat mode tests """
    #setpointChangeTest(tstat)
    
    #heatModeTest(tstat)
    
    """ Water mode tests """
    waterTest(tstat)
    
    # Stop all the threads. Set the stop flag for the serial port thread
    AT.stopThread.set()
    # flush out the redis cache to prevent stale data affecting any re-runs
    r.flushdb()
    
    print('All done.')
    return

if __name__ == "__main__":
    main()