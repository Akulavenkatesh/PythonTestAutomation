#! /usr/bin/python3.3

# Keith Gough
# Python Module Code to build and execute AlertMe API rest calls
# Python 3.3

#import apiFilePaths
import urllib.request
import urllib.parse
import requests
import json
import ast
import time
import math
from copy import deepcopy
import FF_utils as utils
from AA_Steps_ModeChange import setTargetTemperature
# Setup some constants
debug = False

# Device Types
lampType = 'Lamp'
thermostatType = 'HeatingController'
meterReaderType = 'MeterReader'
smartplugType='SmartPlug'
binarySwitchType='GenericBinarySwitch'
# Emperor Device Types
empBoilerModule1 = 'HAHVACThermostat'
empBoilerModule2 = 'HAHVACThermostatSLR2'

empThermostat = 'HAHVACTemperatureSensor'
SLT3Thermostat = 'HAHVACTemperatureSensorSLT3'

# Dictionaries of parameters for each data channel
# Channels have various data point intervals and values that can be specified
cost_dict = {'interval':'1','operations':('average+min+max+amount')}
power_dict = {'interval':'1','operations':('average+min+max')}
energy_dict = {'interval':'1','operations':('average+min+max')}

# Min.Max and Average all contain the same values for signal,battery and temperature so only get average.
# AlertMe only have average in the battery channel
temperature_dict = {'interval':'120','operations':('average')}
signal_dict = {'interval':'120','operations':('average')}
battery_dict = {'interval':'86400','operations':('average')}
targetTemperature_dict = {'interval':'120','operations':('average')}
controllerState_dict = {'interval':'120','operations':('dataset')}
rssi_dict = {'interval':'120', 'operations':('average')}

# Dictionary of device types vs channels and query parameters
deviceChannelParameters = {thermostatType:  {'temperature':temperature_dict,
                                             'battery':battery_dict,
                                             'signal':signal_dict},
                           meterReaderType: {'cost':cost_dict,
                                             'battery':battery_dict,
                                             'temperature':temperature_dict,
                                             'power':power_dict,
                                             'signal':signal_dict},
                           empBoilerModule1:{'temperature':temperature_dict,
                                             'signal':signal_dict,
                                             'targetTemperature':targetTemperature_dict,
                                             'controllerState':controllerState_dict,
                                             'rssi':rssi_dict},
                           empBoilerModule2:{'temperature':temperature_dict,
                                             'signal':signal_dict,
                                             'targetTemperature':targetTemperature_dict,
                                             'controllerState':controllerState_dict,
                                             'rssi':rssi_dict},
                           empThermostat:   {'temperature':temperature_dict,
                                             'battery':battery_dict,
                                             'signal':signal_dict,
                                             'rssi':rssi_dict},
                           lampType:        {'signal':signal_dict},
                           binarySwitchType:{'signal':signal_dict,'rssi':rssi_dict},
                           smartplugType:   {'signal':signal_dict,
                                             'battery':battery_dict,
                                             'temperature':temperature_dict}}

# Server Information and Tokens. Modify pathToFiles from calling module to store files elsewhere.
###SERVER_FILE= apiFilePaths.tokenFilePath + 'tokens.txt'
API_CREDENTIALS = None

class apiCredentials(object):
    """ Credentials are set in two ways..
        1. server, username, password - url obtained from SERVER_FILE. cookie is obtained by a /login to the api
        2. server only                - url & supertoken cookie are retrieved from SERVER_FILE
    """
    # Class Variable
    servers = None

    # Instance Variables
    def __init__(self,\
                 apiServer,\
                 apiCaller = '', username = None, password = None):

        self.loadServers(apiServer)

        # Check that server is listed in credentials file
        if apiServer not in self.servers:
            print('Server not found in credentials file.')
            exit()

        self.apiServer = apiServer
        self.apiUrl = self.servers[apiServer]['url']
        self.apiCaller = apiCaller
        self.apiUsername = None
        self.apiPassword = None
        self.apiCookie = None
        self.platformVersion = None
        
        if 'superToken' in self.servers[apiServer]:
            # supertoken login
            self.apiCookie = {'Cookie': 'ApiToken=' + self.servers[apiServer]['superToken']}
        
        # Username login
        if username != None:
            self.apiUsername = username
        elif 'apiUsername' in self.servers[apiServer]:
            self.apiUsername = self.servers[apiServer]['apiUsername']

            # get password
        if password != None:
            self.apiPassword = password
        elif 'apiPassword' in self.servers[apiServer]:
            self.apiPassword = self.servers[apiServer]['apiPassword']
        else:
            print('No api Password in credentials file')
            exit()
        return None

    def loadServers(self, apiServer):
        """ Load tokens servers and image data from config file
        """
       
        servers={}
        serverAttributes = {}
        strCurrentServer = apiServer #utils.getAttribute('common', 'currentEnvironment')
        serverAttributes['superToken'] = utils.getAttribute('common', 'superToken', Env = strCurrentServer)
        serverAttributes['url'] = utils.getAttribute('common', 'platformAPIURL', Env = strCurrentServer)
        serverAttributes['apiUsername'] = utils.getAttribute('common', 'userName')
        serverAttributes['apiPassword'] = utils.getAttribute('common', 'password')
        
        servers[strCurrentServer] = serverAttributes
        
        '''
        tokenFile=open(myFile,mode='r')
        content=(tokenFile.read()).split('\n')
        
        
        for item in content:
            if item!='':
                row=item.split(',',2)
                server=row[0]
                if server not in servers:
                    servers[server]={}
                item=row[1]
                payload=ast.literal_eval(row[2])
                servers[server][item]=payload
        tokenFile.close()
        '''
        self.servers = servers
        return 0

class accountClass(object):
    """ Class for the parameters associated with account instances
        Initialise with build=False to create an unpopulated object (i.e. no API calls)
        This allows us to create a list of accounts that will be used later.
        
    """

    # Instance Variables
    def __init__(self, username='',build=True):

        # Parameters set by script
        self.username = username
        self.accountFound = False

        # Parameters that returned by API calls
        self.userId = None
        self.email = None
        self.hubId = 'No hub ID'
        self.hubText = None
        self.available = None
        self.availableStatus = None
        self.upgrade = None
        self.upTime = None
        self.hardwareRevision = None
        self.latestVersion = None
        self.version = None
        self.upgrading = None
        self.httpError = False

        # Device list is populated by API calls
        self.deviceList = []
        self.oldDeviceList = []

        # These are used to store current and old schedules
        self.heatSchedule = None
        self.oldHeatSchedule = None
        self.waterSchedule = None
        self.oldWaterSchedule = None
        
        # These are used to store flash status of this account as decided by the script
        # If flashDone == False then a flash is in progress (hub or attached device)
        self.flashStatus = ''
        self.flashStart = None
        self.flashDone = True
        self.flashVersion = None

        # run some methods
        #if build:
            #self.checkUserExists()
            #self.updateInstance()

        return None
    def checkUserExists(self):
        """ Check to see if account name can be found
        """
        myUser,state = getUserSearch(self.username,1)
        if state!=0:
            self.httpError = 'ERROR: Problem in checkUserExists(), {0},{1}'.format(self.username,state)
            
        if myUser['totalMatches'] != '0':
            #if (myUser['matches'][0]['username']).upper() == (self.username).upper():
            #    self.accountFound = True
            #    self.email = myUser['matches'][0]['email']
            for user in myUser['matches']:
                if user['username'].upper() == (self.username).upper():
                    self.accountFound = True
                    self.email = user['email']
                    self.userId = user['userId']
                    if user['hubs']!=None:
                        if len(user['hubs'])>0:
                            self.hubText=user['hubs'][0]['shortId']
                
                #'hubs': [{'shortId': 'KDR-356'}]
                elif 'hubs' in user:
                    if user['hubs']!=None:
                        for h in user['hubs']:
                            if h['shortId']==self.username:
                                self.username = user['username']
                                self.accountFound = True
                                self.email = user['email']
                                self.userId = user['userId']

        if self.accountFound == False:
            self.available = 'Account not found'
            self.hubId = self.available
        return 0
    def updateInstance(self):
        """ Update the account instance.
            Query the status parameters, devices and device status parameters
        """

        if self.accountFound == True:
            hubs, state = getHubs(self.username)
            if state!=0:
                self.httpError='ERROR: problem with getHubs, {0},{1}'.format(self.username,state)
                return 0
            
            # If the account has a hub installed there will be a hub ID
            # If not then assume account not installed.
            if len(hubs) == 0:
                self.hubId = 'No hub installed'
                self.available = self.hubId
            else:

                # User exists and hub is installed.
                # Get the hub ID
                self.hubId = hubs[0]['id']

                # Get status of all devices
                devicesStatus,state = getDevicesStatus(self.username, self.hubId)
                if state!=0:
                    self.httpError = 'ERROR: problem with getDeviceStatus, {0},{1}'.format(self.username,state)
                    return 0
#                 if type(devicesStatus) == urllib.error.HTTPError:
#                     self.httpError = devicesStatus
#                     return 0

                # Update our copy of the hub status parameters
                # protected values start with '_' so keep those
                # Any values we have in the local object that are not
                # returned by the API are set to 'None' to ensure they don't
                # hold stale data.
                myHubStatus = devicesStatus['hub']
                for attr in self.__dict__:
                    if attr in myHubStatus:
                        setattr(self, attr, myHubStatus[attr])
                    # if the hub availability is not present in the devicesStatus response (e.g. ISOP) then
                    # do another call to get it
                if 'available' not in myHubStatus:
                    print('Debug: \'available\' not in the API responses')

                # Build a device list
                for device in devicesStatus:
                    if device != 'hub':

                        myDeviceStatus = devicesStatus[device]

                        # Select the device from the list or
                        # if device not already in the list then add it
                        newDevice = True
                        for listDevice in self.deviceList:
                            if listDevice.id == device:
                                newDevice = False
                                myDev = listDevice

                        if newDevice == True:
                            myDev = deviceClass(myDeviceStatus['type'], device)
                            self.deviceList.append(myDev)

                        # Update the device parameters
                        # Leave protected parameters intact
                        for attr in myDev.__dict__:
                            if attr in myDeviceStatus:
                                setattr(myDev, attr, myDeviceStatus[attr])
                            else:
                                # Reset these ones if they are missing from the API response
                                if attr == 'progress': setattr(myDev, attr, None)
                                if attr == 'reason' : setattr(myDev, attr, None)

                        # Round off the battery value for nicer printing
                        if myDev.battery != None: myDev.battery = round(myDev.battery,2)

        return 0
    def copyDevicesStates(self):
        """ Make a copy of any old device states e.g. prior to re-flashing
        """
        self.oldDeviceList = deepcopy(self.deviceList)
        return 0
    def checkDeviceStates(self):
        """ Check device states after e.g. a re-flash
            Confirm that all devices returned to 'Online' and confirm that the device parameters
            have updated correctly.
            If not then Return False and a list of device checks that failed.
        """
        devStates='This has not been implemented yet'

        return devStates
    def getHeatSchedule(self):
        """ Check the device list for a suitable device and then call api
            to pull the schedule data.
        """
        for device in self.deviceList:
            if device.type == empBoilerModule1 or device.type == empBoilerModule2:
                if device.presence == True:
                    self.heatSchedule = getHeatSchedule(self.username, device.id)

        return 0
    def getWaterSchedule(self):
        """ Check the device list for a suitable device and then call api
            to pull hot water schedule
        """
        for device in self.deviceList:
            if device.type == empBoilerModule2 and device.presence == True:
                self.waterSchedule = getHotWaterSchedule(self.username, self.hubId, device.id)

        return 0
    def printAccount(self):
        """ Returns a one line string for hub, devices and their status.
        """
        if self.hubId != None:
            myHubId=self.hubId
        else:
            myHubId='No Hub Id'

        if self.available == True:
            hubStatus = 'ONLINE'
        else:
            hubStatus = 'OFFLINE'

        if self.upgrading == True:
            hubString = ('{0:35},{1:19},{2},{3},{4}'.format
                         (self.username,
                          myHubId,
                          self.userId,
                          'HUB UPGRADING',
                          self.version))
        else:
            hubString = '{0:35},{1:19},{2},{3},{4}'.format(self.username,self.hubId,self.userId,hubStatus,self.version)

        myString=''

        deviceStrings={'bmStr':'',\
                       'statStr':'',\
                       'plugStr':'',\
                       'lampStr':'',\
                       'bswStr':'',\
                       'otherDevicesStr':''}

        for device in self.deviceList:

            if device.presence == True:
                deviceStatus = 'ONLINE'
            else:
                deviceStatus = 'OFFLINE'

            if device.battery == None:
                batteryString = str(device.battery)
            else:
                batteryString = '{}v'.format(device.battery)

            if device.progress == None:
                myString = ('{0},{1},{2},{3},{4},{5}'.format
                            (device.type,
                             deviceStatus,
                             device.version,
                             device.latestVersion,
                             device.signal,
                             batteryString))
            else:
                myString = ('{0},{1},{2},{3},{4},{5}'.format
                            (device.type,
                             deviceStatus,
                             device.version,
                             device.signal,
                             'Progress={0}%'.format(device.progress),
                             batteryString))

            if device.type == empBoilerModule1 or device.type == empBoilerModule2:
                deviceStrings['bmStr'] += myString
            elif device.type == thermostatType or device.type == empThermostat:
                deviceStrings['statStr'] += myString
            elif device.type == lampType:
                deviceStrings['lampStr'] += myString
            elif device.type == smartplugType:
                deviceStrings['plugStr'] += myString
            elif device.type == binarySwitchType:
                deviceStrings['bswStr'] += myString
            else:
                deviceStrings['otherDevicesStr'] += myString

        for deviceStr in deviceStrings:
            if deviceStrings[deviceStr] == '':
                deviceStrings[deviceStr] = ',,,,,'

        myString='{0},{1},{2},{3},{4},{5},{6}'.format \
                    (hubString,
                     deviceStrings['statStr'],
                     deviceStrings['bmStr'],
                     deviceStrings['lampStr'],
                     deviceStrings['bswStr'],
                     deviceStrings['plugStr'],
                     deviceStrings['otherDevicesStr'])

        return myString
class deviceClass(object):
    """ Class Type for device details
    """
    def __init__(self,\
                 myType,\
                 myId):

        self.type=myType
        self.id=myId

        self.progress = None
        self.battery = None
        self.batteryLow = False
        self.power = None
        self.presence = False
        self.version = None
        self.latestVersion = None
        self.upgrade = None
        self.upgradeStatus = None
        self.reason = None
        self.signal = None

        # These are used to store flash status of this device as decided by the script
        # If flashStart != None then a flash is in progress (hub or device)
        self.flashStatus = ''
        self.flashStart = None

        return None


def myApiCall(myApiCmd, myParams, myMethod, myNumOfRetries=1):
    """ Makes a RESTful API call and returns a tuple of JSON payload and HTTP response code
    Keyword arguments:
        myApiCmd (string)      -- The AlertMe API command to be executed
        mParams (dict)         -- POST command parameters or None.  Parameters must be encoded as byte type (utf-8)
        myMethod (string)      -- POST, GET, PUT
    """

    # Check that api credentials has been initialised
    if API_CREDENTIALS == None:
        print('DEBUG: API Credentials not initialised.  Call createCredentials() first')
        exit()
    elif API_CREDENTIALS.apiCookie == None and myApiCmd != '/login':
        print('DEBUG: API Credentials not initialised.  No Cookie')
        exit()

    # Build the full URL
    myURL = API_CREDENTIALS.apiUrl + myApiCmd
    
    #print(myURL, myParams)
    #Build the headers
    headers = API_CREDENTIALS.apiCookie
    #print(myURL, myParams, headers)
    retryCount = 0
    timeout=600
    while True:
        # Execute the required method
        if myMethod == 'POST':
            r=requests.post(myURL, data=myParams, headers=headers, timeout=timeout)
        elif myMethod == 'GET':
            r=requests.get(myURL, params=myParams, headers=headers,timeout=timeout)
        elif myMethod == 'PUT':
            r=requests.put(myURL, data=myParams, headers=headers,timeout=timeout)
        elif myMethod == 'DELETE':
            r=requests.delete(myURL, params=myParams, headers=headers,timeout=timeout)
        #print(r)
        if debug == True:
            print('API Call: ' + myMethod + ' ' + myURL, end=', ')
            print('params:' + str(myParams))
            if r.text!='':
                print('RESPONSE: {}'.format(r.json()))
            print("STATUS CODE: {}".format(r.status_code))
            #print(myAccount.apiCookie)
    
        if r.text!='':
            jsonResponse = r.json()
        else:
            jsonResponse = ''
            
        statusCode = r.status_code
        
        if statusCode in [ 200, 201, 202, 204]:
            statusCode=0
            break
        else:
            retryCount+=1
            if retryCount>myNumOfRetries:
                jsonResponse=None
                break
            
    return jsonResponse,statusCode
             
def myApiCall_Old(myApiCmd, myParams, myMethod, myNumOfRetries=1):
    """ Makes a RESTful API call and returns a tuple of JSON payload and HTTP response code
    Keyword arguments:
        myApiCmd (string)      -- The AlertMe API command to be executed
        mParams (dict)         -- POST command parameters or None.  Parameters must be encoded as byte type (utf-8)
        myMethod (string)      -- POST, GET, PUT
    """
    # Note if parameters included then urllib assumes a POST is required, otherwise a GET.
    # If a PUT is required we overload the get method name with PUT.
    # If a get is required with parameters then we build the string directly

    # Check that api credentials has been initialised
    if API_CREDENTIALS == None:
        print('DEBUG: API Credentials not initialised.  Call createCredentials() first')
        exit()
    elif API_CREDENTIALS.apiCookie == None and myApiCmd != '/login':
        print('DEBUG: API Credentials not initialised.  No Cookie')
        exit()

    # Build the URL

    myURL = API_CREDENTIALS.apiUrl + myApiCmd
    myURL = urllib.parse.quote(myURL,safe=':/')

    # If 'POST' command with no parameters insert dummy string into parameters to force a POST
    # Otherwise encode them as bytes
    if myMethod == 'POST':
        if myParams == None:
            params = 'POST'.encode('utf-8')
        else:
            params=urllib.parse.urlencode(myParams).encode('utf-8') # params must be type byte (utf-8) for the api call

    # If a GET with parameters then encode and add them to the URL
    if myMethod =='GET':
        if myParams == None:
            params = None
        else:
            params = urllib.parse.urlencode(myParams)
            myURL = myURL + '?' + params
            params = None

    # If PUT with parameters then byte encode as per a POST
    if myMethod == 'PUT':
        if myParams == None:
            params = None
        else:
            params = urllib.parse.urlencode(myParams).encode('utf-8')

    if myMethod == 'DELETE':
        if myParams == None :
            params=None
        else:
            params = urllib.parse.urlencode(myParams).encode('utf-8')

    # Build the request
    # If there's a header/cookie include it the request
    if API_CREDENTIALS.apiCookie != None:
        request = urllib.request.Request(myURL, params, API_CREDENTIALS.apiCookie)
    else:
        request = urllib.request.Request(myURL, params)

    # If a 'PUT' command then override the method as PUT (Fudge due to urllib not supporting PUT)
    if myMethod=='PUT':
        request.get_method = lambda:'PUT'

    if myMethod == 'DELETE':
        request.get_method = lambda:'DELETE'

    if debug == True:
        print('API Call: ' + myMethod + ' ' + myURL, end=', ')
        print('params:' + str(params))
        #print(myAccount.apiCookie)

    # Make the REST call and use json.loads to return a dict
    # Wrap this in a retry loop with try/except to catch any network glitches.
    retryCount=0
    maxRetry=myNumOfRetries
    
    while True:
        try:
            with urllib.request.urlopen(request) as myResp:
                state = 0
                
                # Convert the response from a string to a dict
                myRespString = (myResp.read()).decode('utf-8')
                if myRespString != '':
                    jsonResponse = json.loads(myRespString)  # @UndefinedVariable
                else:
                    jsonResponse = None
                
                # Check the HTTP response code
                apiRespCode = myResp.getcode()
                if debug == True:
                    print('HTTP Return Code: ' + str(apiRespCode))
                    print('Json Response: ', jsonResponse)
            
                if apiRespCode in [ 200, 201, 202, 204]:
                    pass
                else:
                    print('Bad API Call:  ' + str(apiRespCode))
                    exit()
                
                break

        except urllib.error.URLError as e:
            # Retry a few time in case it's a temporary connectivity glitch 
            retryCount += 1    
            if retryCount>maxRetry:
                state = e
                return None, e
                break
            time.sleep(1)

    return jsonResponse, state
def createCredentials(myApiServer,myApiCaller=None, username = None, password = None):
    """ Create the apiCredentials object before calling any apis
        If no username or password them assume a supertoken
    """
    global API_CREDENTIALS
    API_CREDENTIALS = apiCredentials(apiServer = myApiServer, apiCaller = myApiCaller, username = username, password = password)

    # If a username is given then it's not a super token so we need to Login to get a cookie
    if API_CREDENTIALS.apiUsername != None:
        if API_CREDENTIALS.platformVersion == 'V5':
            loginResult = login()
            API_CREDENTIALS.apiCookie = loginResult[0]
            state = loginResult[2]
            if state!=0:
                print('ERROR: Unable to login')
                print(state)
                #exit()
        else: 
            sessionV6  = sessionObject()
            if sessionV6.statusCode != 200:
                return sessionV6.statusCode, sessionV6.response
            if sessionV6.latestSupportedApiVersion == '6': 
                API_CREDENTIALS.platformVersion = 'V6'
            else: 
                API_CREDENTIALS.platformVersion = 'V5'
                #API_CREDENTIALS.apiUrl = API_CREDENTIALS.apiUrl + '/api'
                loginResult = login()
                API_CREDENTIALS.apiCookie = loginResult[0]
                state = loginResult[2]
                if state!=0:
                    print('ERROR: Unable to login')
                    print(state)
                
    return API_CREDENTIALS.platformVersion

def login():
    """ POST /login
    Desription:
        Login to the API. Return an HTTP cookie and Hub ID.
        Creates a session and allows use of all other API methods.
        Sessions expire after 20 minutes of inactivity.
        Function returns a cookie that must be appended to most other API calls
        Caller is an identifier that gets added to the hub log on the server
        to identify the calling application.
    Keyword arguments:
        myLoginParms (dict) -- url, username, password, apicookie, hubid
    API Response:
        Cookie for API session and the hub ID.
    """
   
    myApiCmd = '/api/login'
   
    params = {'username':API_CREDENTIALS.apiUsername, \
              'password':API_CREDENTIALS.apiPassword, \
              'caller':API_CREDENTIALS.apiCaller}
    
   
    jsonResponse,state = myApiCall(myApiCmd, params, 'POST')
    if state==0:
        apiSessionValue = jsonResponse["ApiSession"]
        apiCookie = {'Cookie': 'ApiSession=' + str(apiSessionValue)}
        hubId = jsonResponse['hubIds'][0]
    else:
        apiSessionValue = None
        apiCookie = None
        hubId = None
        
    return apiCookie, hubId, state



class superUserSessionObject(object):
    
    def __init__(self):
        self.username = "ranganathan.veluswamy@bgch.co.uk"
        self.password = "password1"
        self.headers  = {'Accept':'application/vnd.alertme.zoo-6.4+json',
                         'X-AlertMe-Client':'KG',
                         'Content-Type':'application/json'}

        self.sessionId, self.userId, self.latestSupportedApiVersion, self.statusCode, self.response  = getSessionToken(self.username,self.password)
        self.headers['X-Omnia-Access-Token'] = self.sessionId
        return


class sessionObject(object):
    
    def __init__(self):
        self.username = API_CREDENTIALS.apiUsername
        self.password = API_CREDENTIALS.apiPassword
        self.headers  = {'Accept':'application/vnd.alertme.zoo-6.0+json',
                         'X-AlertMe-Client':'KG',
                         'Content-Type':'application/json'}

        self.sessionId, self.userId, self.latestSupportedApiVersion, self.statusCode, self.response  = getSessionToken(self.username,self.password)
        self.headers['X-Omnia-Access-Token'] = self.sessionId
        return

def getSessionToken(username, password):
    """ Login and get a session token for the user
        Used by the sessionObject class to get the session token
    """    
    url = API_CREDENTIALS.apiUrl + '/omnia/auth/sessions'
    payload = json.dumps({'sessions':[ {'username':username,'password':password}]})
    headers = {'Accept':'application/vnd.alertme.zoo-6.0+json',
               'X-AlertMe-Client':'KG',
               'Content-Type':'application/json'}
    
    r = requests.post(url, data=payload, headers=headers)
    #print("respose for the Login")
    #print(r.json)
    if r.status_code!=200:
        print("ERROR in getSessionToken(): ",r.status_code,r.reason,r.url,r.text)
        print(r.text)
        return "", username, "", r.status_code,r.text
    latestSupportedApiVersion = ''
    session = r.json()['sessions'][0]
    userId = session['userId']
    sessionId = session['sessionId']
    username = session['username']
    if 'latestSupportedApiVersion' in session: 
        latestSupportedApiVersion = session['latestSupportedApiVersion']
    return sessionId, userId, latestSupportedApiVersion, r.status_code,r.text

def deleteSessionV6(session):
    """ Logout from session
    """
    url = API_CREDENTIALS.apiUrl + '/omnia/auth/sessions/{}'.format(session.sessionId)
    r = requests.delete(url,headers=session.headers)
    if r.status_code!=200:
        print("ERROR in deleteSession(): ",r.status_code,r.reason,r.url,r.text)
        exit()
    return

def getNodesV6(session):
    """
    """
    url = API_CREDENTIALS.apiUrl + '/omnia/nodes/'
    r = requests.get(url, headers=session.headers)
    
    if r.status_code!=200:
        print("ERROR in getNodes(): ",r.status_code,r.reason,r.url,r.text)
        exit()
    return r.json() 

def getHubIdV6(session, username):
    """
    """
    url = API_CREDENTIALS.apiUrl + '/api/management/diagnostics/users/{}'.format(username)
    r = requests.get(url, headers=session.headers)
    
    if r.status_code!=200:
        print("ERROR in getHubIdV6(): ",r.status_code,r.reason,r.url,r.text)
        exit()
    return r.json() 

def getHubLogsV6(session, hubID):
    """
    """
    url = API_CREDENTIALS.apiUrl + '/api/management/diagnostics/hubs/{}'.format(hubID)
    r = requests.get(url, headers=session.headers)
    
    if r.status_code!=200:
        print("ERROR in getHubLogsV6(): ",r.status_code,r.reason,r.url,r.text)
        exit()
    return r.json() 

def rebootHub(session, hubID):
    """
    """
    session.headers["Accept"] = "application/json"
    username = utils.getAttribute('common', 'userName')
    payload= "power : REBOOT" #"REBOOT" #{'power':'REBOOT'}
    url = API_CREDENTIALS.apiUrl + '/api/users/{0}/hubs/{1}/power'.format(username,hubID)
    
    r = requests.put(url, headers=session.headers, data=payload)
    
    session.headers["Accept"] = 'application/vnd.alertme.zoo-6.4+json'
    if r.status_code!=200:
        print("ERROR in getHubLogsV6(): ",r.status_code,r.reason,r.url,r.text)
        exit()
    return r.json() 

def rebootHubV6(session, hubID):
    """
    """
    payload=json.dumps({"nodes":[{"attributes": {"powerSupply":{"targetValue":"REBOOT"}}}]})
    url = API_CREDENTIALS.apiUrl + '/omnia/nodes/{}'.format(hubID)
    
    r = requests.put(url, headers=session.headers, data=payload)
    
    if r.status_code!=200:
        print("ERROR in getHubLogsV6(): ",r.status_code,r.reason,r.url,r.text)
        exit()
    return r.json() 

def getNodesByIDV6(session, nodeId):
    """
    """
    url = API_CREDENTIALS.apiUrl + '/omnia/nodes/{}'.format(nodeId)
    r = requests.get(url, headers=session.headers)
    
    if r.status_code!=200:
        print("ERROR in getNodes(): ",r.status_code,r.reason,r.url,r.text)
        exit()
    return r.json() 

def getRulesV6(session):
    url = API_CREDENTIALS.apiUrl + '/omnia/rules/'
    r = requests.get(url, headers=session.headers)
    
    if r.status_code!=200:
        print("ERROR in getRulesV6(): ",r.status_code,r.reason,r.url,r.text)
        exit()
    return r.json() 

'''def setScheduleV6(session):
    """ Start a fw upgrade for the node
        PUT /omina/nodes/{nodeId}
        Payload = {"nodes":[{"attributes": {"softwareVersion":{"targetValue":fwTarget}]}
        200 = Success
            
    """
    success = False
    payload=json.dumps({"nodes":[{"attributes": {"softwareVersion":{"targetValue":schedule}}}]})
    url = API_CREDENTIALS.apiUrl + '/omnia/nodes/{}'.format(nodeId)
    r = requests.put(url, headers=session.headers,data=payload)
    if r.status_code==200: success=True
    return r,success'''

def firmwareUpgrade(session,nodeId,fwTargetVersion):
    """ Start a fw upgrade for the node
        PUT /omina/nodes/{nodeId}
        Payload = {"nodes":[{"attributes": {"softwareVersion":{"targetValue":fwTarget}]}
        200 = Success
            
    """
    success = False
    payload=json.dumps({"nodes":[{"attributes": {"softwareVersion":{"targetValue":fwTargetVersion}}}]})
    url = API_CREDENTIALS.apiUrl + '/omnia/nodes/{}'.format(nodeId)
    r = requests.put(url, headers=session.headers,data=payload)
    if r.status_code==200: success=True
    return r,success

def setSmartPlugState(session,nodeId,state):
    """ Start a fw upgrade for the node
        PUT /omina/nodes/{nodeId}
        Payload = {"nodes":[{"attributes": {"state":{"targetValue":fwTarget}]}
        200 = Success
            
    """
    success = False
    payload=json.dumps({"nodes":[{"attributes": {"state":{"targetValue":state}}}]})
    url = API_CREDENTIALS.apiUrl + '/omnia/nodes/{}'.format(nodeId)
    r = requests.put(url, headers=session.headers,data=payload)
    if r.status_code==200: success=True
    return r,success

def setActiveLightState(session,nodeId,state):
    """ Set On-Off on Active Bulb
        PUT /omina/nodes/{nodeId}
        Payload = {"nodes":[{"attributes": {"state":{"targetValue":state}]}
        200 = Success
            
    """
    success = False
    payload=json.dumps({"nodes":[{"attributes": {"state":{"targetValue":state}}}]})
    url = API_CREDENTIALS.apiUrl + '/omnia/nodes/{}'.format(nodeId)
    r = requests.put(url, headers=session.headers,data=payload)
    if r.status_code==200: success=True
    return r,success

def setActiveLightBrightness(session,nodeId,intBrightness):
    """ Set On-Off on Active Bulb
        PUT /omina/nodes/{nodeId}
        Payload = {"nodes":[{"attributes": {"brightness":{"targetVal                   ue":state}]}
        200 = Success
            
    """
    success = False
    payload=json.dumps({"nodes":[{"attributes": {"brightness":{"targetValue":intBrightness}}}]})
    url = API_CREDENTIALS.apiUrl + '/omnia/nodes/{}'.format(nodeId)
    r = requests.put(url, headers=session.headers, data=payload)
    if r.status_code==200: success=True
    return r,success

def setActiveLightColourTemperature(session,nodeId,intColorTemperature):
    """ Set On-Off on Active Bulb
        PUT /omina/nodes/{nodeId}
        Payload = {"nodes":[{"attributes": {"colourTemperature":{"targetVal                   ue":state}]}
        200 = Success
            
    """
    success = False
    payload=json.dumps({"nodes":[{"attributes": {"colourTemperature":{"targetValue":intColorTemperature}}}]})
    url = API_CREDENTIALS.apiUrl + '/omnia/nodes/{}'.format(nodeId)
    r = requests.put(url, headers=session.headers, data=payload)
    if r.status_code==200: success=True
 

def setScheduleSP(session,nodeId,payload):
    """ Set On-Off on Active Bulb
        PUT /omina/nodes/{nodeId}
        200 = Success
            
    """
    success = False
    url = API_CREDENTIALS.apiUrl + '/omnia/nodes/{}'.format(nodeId)
    r = requests.put(url, headers=session.headers, data=payload)
    if r.status_code==200: success=True
    print(r,success)
    return r,success

def deleteDeviceV6(session,nodeId):
    """ Delete Device
        DELETE /omina/nodes/{nodeId}
        200 = Success
            
    """
    success = False
    url = API_CREDENTIALS.apiUrl + '/omnia/nodes/{}'.format(nodeId)
    r = requests.delete(url, headers=session.headers)
    if r.status_code==200: success=True
    return r,success

def setHubStateV6(session,nodeId, hubState):
    """ Delete Device
        PUT /omina/nodes/{nodeId}
        200 = Success
            
    """
    
    strPUTJson = {"nodes":[{"attributes":{"devicesState":{"targetValue":hubState}}}]}
    success = False
    payload=json.dumps(strPUTJson)
    url = API_CREDENTIALS.apiUrl + '/omnia/nodes/{}'.format(nodeId)
    r = requests.put(url, headers=session.headers,data=payload)
    if r.status_code==200: success=True
    print(r,success)
    return r,success


def setModeV6(session,nodeId, setMode, targetHeatTemperature = None, scheduleLockDuration = 60):
    """ Set mode for the node
        PUT /omina/nodes/{nodeId}
        Payload = {"nodes":[{"attributes":{"activeHeatCoolMode":{"targetValue":"HEAT"},"activeScheduleLock":{"targetValue":false}}}]}
        200 = Success
            
    """
    setMode = setMode.upper()
    if 'MANUAL' in setMode or 'ON' in setMode:
        strPUTJson = {"nodes":[{"attributes":{"activeHeatCoolMode":{"targetValue":"HEAT"},"activeScheduleLock":{"targetValue":"true"}}}]}
    elif 'AUTO' in setMode:
        strPUTJson = {"nodes":[{"attributes":{"activeHeatCoolMode":{"targetValue":"HEAT"},"activeScheduleLock":{"targetValue":"false"}}}]}
    elif 'OFF' in setMode:
        strPUTJson = {"nodes":[{"attributes":{"activeHeatCoolMode":{"targetValue":"OFF"},"activeScheduleLock":{"targetValue":"true"}}}]}
    elif 'BOOST' in setMode:
        if targetHeatTemperature is not None:
            strPUTJson = {"nodes":[{"attributes":{"activeHeatCoolMode":{"targetValue":"BOOST"},"scheduleLockDuration":{"targetValue":scheduleLockDuration},"targetHeatTemperature":{"targetValue":targetHeatTemperature}}}]}
        else:
            strPUTJson = {"nodes":[{"attributes":{"activeHeatCoolMode":{"targetValue":"BOOST"},"scheduleLockDuration":{"targetValue":scheduleLockDuration}}}]}
    else: return 
    print(strPUTJson)
    success = False
    payload=json.dumps(strPUTJson)
    url = API_CREDENTIALS.apiUrl + '/omnia/nodes/{}'.format(nodeId)
    r = requests.put(url, headers=session.headers,data=payload)
    if r.status_code==200: success=True
    print(r,success)
    return r,success

def setTargTemperatureV6(session, nodeId, targetHeatTemperature):

    strPUTJson = {"nodes":[{"attributes":{"targetHeatTemperature":{"targetValue":targetHeatTemperature}}}]}
    success = False
    payload=json.dumps(strPUTJson)
    url = API_CREDENTIALS.apiUrl + '/omnia/nodes/{}'.format(nodeId)
    r = requests.put(url, headers=session.headers,data=payload)
    if r.status_code==200: success=True
    return r,success

def logout():
    """ POST /logout
    Description:
        Logout from the API Session
    API Response:
        Returns HTTP 204 if successful
    """
    myApiCmd = '/logout'
    jsonResponse,state = myApiCall(None, myApiCmd, None, 'POST')
    return jsonResponse,state
#
def resetPassword(myEmail):
    """ POST /passwordreset
    Description:
        Starts the password reset process and sends the confirmation email to the end user.
        Assumes that the username == email address.
    Arguments:
        email = Email address of account holder.
        ip    = (optional) IP address of the end user, used only for logging purposes.
    API Response:
        Successful requests always return:-HTTP 201
    """
    myApiCmd = '/passwordreset'
    params = {'email': myEmail}
    jsonResponse, state = myApiCall(myApiCmd, params , 'POST')
    return jsonResponse, state
    #
def getUserInformation(myUsername):
    """ GET /users/:username
    Description:
        Return Information on the given user
    Keyword arguments:
        myAccount class
    Response:
        Returns user info like email, phone, address etc
    """
    myApiCmd = '/users/' + myUsername
    jsonResponse,state = myApiCall(myApiCmd, None, 'GET')
    return jsonResponse,state
#
def getUserSearch(mySearchString,myIndex,myQuantity=100):
    """ GET /users/all/search
        Description:
            Returns information about users that match the provided query argument sorted by username.
        Arguments:
            query - Term to search by (matches against beginnings of username, email address; also matches against mobile number, partnerSpecificId or hub ID).
            first -(optional) Restrict the results returned, to those starting at the specified index (1 based)
            quantity - (optional) Restrict the results to the maximum quantity specified
            fieldSet - (optional) Specify which set(s) of fields to return. Options are ("default", "user", and "hub"). Format is space separated or plus ('+') when URL encoded
        query='' returns all users
    """
    myApiCmd = '/users/all/search'
    myParams = {'query':mySearchString,'fieldSet':'default hub user','quantity':str(myQuantity),'first':str(myIndex)}
    jsonResponse,state = myApiCall(myApiCmd , myParams, 'GET')
    return jsonResponse,state
#
def getAllUsers():
    """ Special Case.  username='' or username='___' so get all users and return them in the self._hubId attribute
    """
    username = '___'
    myNames=[]
    pageSize=1000
    page = 1
    lastPage = '?'
    while True:
        index = ((page-1)*pageSize)+1
        print('Getting chunk ' + str(page) + '/' + str(lastPage))

        myUsers,state = getUserSearch(username,index)
        if state!=0: 
            print(state)
            exit()

        for user in myUsers['matches']:

            if user['hubs']!=None:
                hubId=user['hubs'][0]['shortId']
            else:
                hubId=None
            
            # 'hubCount':str(len(user['hubs'])),
            myNames.append({'username':user['username'],
                            'firstName':user['firstName'],
                            'hubId':hubId,
                            'lastName':user['lastName']})
        
        # Work out if this is the last chunk
        totalMatches = int(myUsers['totalMatches'])
        lastPage = math.ceil(totalMatches/pageSize)
        if page >= lastPage:
            break
        else:
            page += 1

    return myNames
def postTransferHub(myAccount,myHubText,myTransfer=False):
    """ POST /users/:username/hubs
        Description:
            Use this to move a hub attached to a dummy account to a specified account.
            Authorize a hub, which generates a long Hub ID for use in future calls.
            "Transfer" argument is optional.
        Arguments:
            hubText  - The text on the Hub hardware, e.g. ABC-123
            transfer - Bool, if true switches hub with provided hubText and related devices to specified username.
        Sample Response:
            For "transfer" omitted or "false"
            {
                "id": "2342340234920344"
            }
            For "transfer" = "true"
           {
               "id": "2342340234920344",
               "migrateHubResult":     "true",
               "migrateDevicesResult": "true"
           }
        Returned errors:
            404 NO_SUCH_HUB        Can't find hub with specified hubId in DB.
            401 HUB_OWNER_IS_NOT_DUMMY_USER - Hub owner is not user with username like "dummy0123456789".
            400 HUB_NOT_FOUND_FOR_AUTHORIZING - The hub is not trying to authorize (possibly yet). The user should make sure that the hub is blinking red, check the hub's network connection or wait (if the hub has just been switched on, rebooted or factory restored).
            400 INVALID_HUB_TEXT - The hubText parameter is not in ABC-123 format.
            400 USER_ALREADY_HAS_A_HUB - The user already has a hub installed (there is currently a limit of one hub per user)
            500 AUTHORISATION_FAILED - Hub authorization failed. It may be due to network problems - please try again.
    """
    myApiCmd = '/users/' + myAccount.username + '/hubs'
    params = {'hubText':myHubText, \
              'transfer':myTransfer}
    jsonResponse, state = myApiCall(myApiCmd, params, 'POST')
    return jsonResponse, state
#
def postUsers(myNewUser):
    """ POST /users
    Description:
        Create a new user
    Keyword Arguments:
        myNewUser = Dict with API parameters as below.
    API Arguments:
        username    (mandatory) if omitted, the email address will be used instead.
        password    (mandatory) password.
        firstName            First name
        lastName             Surname
        address              Street address.
        addressAdditional    Address second line.
        pin                  4 or 6 digit PIN (depending on tariff's pin length configuration).
        city                 City
        county               County/State/Province.
        postcode             Postal Code.
        country              Country
        dob                  Date of birth (DD-MM-YY).
        language             UI Language.
        phone                Landline phone number.
        email                Email address.
        mobile               Mobile phone number.
        tariff               Tariff name. Tariff ID usage instead of tariff name is allowed but deprecated now.
        partnerId            Partner ID (mandatory only for a supertoken user).
        partnerSpecificId    External userId.
        flags[flagName]      Sets a flag for the user. Permitted values are false|true and 0|1 - other values will be treated as false
    """
    myApiCmd = '/users'
    params = myNewUser
    jsonResponse,state =myApiCall(myApiCmd, params, 'POST')
    return jsonResponse,state
def postUserSettings(myAccount, myParam, myParamValue):
    """ POST /users/:username/settings
    """
    myApiCmd = '/users/{0}/settings'.format(myAccount.username)
    params = { myParam : myParamValue}
    jsonResponse,state = myApiCall(myApiCmd, params, 'POST')
    return jsonResponse,state
#
def getHubs(myUsername):
    """ GET /users/:username/hubs
    Description:
        Get list of hubs
    Response:
        Returns the list of hubs associated with :username
    """
    myApiCmd = '/users/' + myUsername + '/hubs'
    jsonResponse,state = myApiCall(myApiCmd, None, 'GET')
    return jsonResponse,state
#
def getSingleHub(myUsername, myHubId):
    """ GET /users/:username/hubs/:hubId
    Description:
        Returns details of hub
    Keyword Arguments:
    Response::
        Sample Responses:
        {
            "name":               "Joe's House",
            "available":          false,
            "hardwareRevision":   2,
            "simHistory":
              [
                 {
                    "state":      "done",
                    "start_date": "2011-11-15 17:30:00",
                    "simiccid":   "8944123456789012345",
                    "imei":       "359511111111111",
                    "provider"    "orange"
                 }
              ]
        }
        OR
        {
            "name":               "Joe's House",
            "available":          true,
            "upgrading":          false,
            "configured":         true,
            "version":            "2.10",
            "latestVersion":      "2.12",
            "upgrade":            "INELIGIBLE",
            "version":            "HUB_NOT_PRESENT",
            "powerType":          "AC",
            "connectionType":     "BROADBAND",
            "onSince":            1272387672,
            "upTime":             4168,
            "timezone":           -210,
            "daylightSaving":     "EU",
            "behaviourId":        9887,
            "behaviourType":      "HOME",
            "hardwareRevision":   2,
            "ip":                 "192.168.1.1",
            "externalIp":         "172.16.254.1",
            "simPresent":         true,
            "gprsSignalStrength": 12,
            "currentImei":        "359511111111111",
            "currentIccid":       "8944123456789012345",
            "currentSimId":       "231111111111111",
            "zigbeeNetworkInfo":  "231",
            "macAddress":         "AAA-001 (00-11-22-33-44-55)",
            "simHistory":
              [
                 {
                    "state":      "done",
                    "start_date": "2011-11-15 17:30:00",
                    "simiccid":   "8944123456789012345",
                    "imei":       "359511111111111",
                    "provider":   "orange"
                 }
              ]
        }
        Possible Values
        available        = true, false
        upgrading        = true, false
        behaviourType    = "HOME", "AWAY", "NIGHT"
        powerType        = "AC", "BATTERY"
        connectionType   = "BROADBAND", "GPRS"
        timezone         = (offset in minutes from GMT)
        hardwareRevision = integer: 1 classic, 2 starter, 3 nano, 4 mini
        ip               = IPv4, "UNAVAILABLE", "UNKNOWN"
        externalIp       = IPv4, "UNAVAILABLE", "UNKNOWN"
        gprsSignalStrength = integer number in range [0..100] or null (if SIM is not present or signal is not known)
        NOTE: You can only access hubs which belong to your user
        The "upgrade" value can be "ELIGIBLE", "INELIGIBLE", "DOWNLOADING", "PROGRAMMING".
        The "reason" value is only filled in if the "upgrade" value is "INELIGIBLE".
        The "latestRequiredVersion" value is the minimum version required for the hub to be at, for the upgrade criticality specified in the call argument. This field may be omitted if there are no such requirements.
    """
    myApiCmd = '/users/' + myUsername + '/hubs/' + myHubId
    jsonResponse,state = myApiCall(myApiCmd, None, 'GET')
    return jsonResponse,state
#
def getHubVersion(myUsername, myHubId):
    """ GET /users/:username/hubs/:hubId/version
    Description:
        Returns the details of a hub's upgrade status. This can be used to establish
        if the hub is eligible for upgrades of a certain criticality.
    API Arguments:
        criticality - high/medium/low
        high   -- (default) The most critical upgrades, regarded as compulsory for all users, and required at install time
        medium -- Upgrades of medium criticality; depending on the configuration they may be applied automatically overnight
        low    -- All other upgrades
        If the criticality level is not specified in the request, it defaults to "high".
    Sample Response:
        {
            "upgrade":               "INELIGIBLE",
            "reason":                "HUB_NOT_PRESENT",
            "version":               "2.01r16",
            "latestVersion":         "2.01r17",
            "latestRequiredVersion": "2.01r17"
        }
        The "upgrade" value can be "ELIGIBLE", "INELIGIBLE", "DOWNLOADING", "PROGRAMMING".
        The "reason" value is only filled in if the "upgrade" value is "INELIGIBLE".
        The "latestRequiredVersion" value is the minimum version required for the hub to be at,
        for the upgrade criticality specified in the call argument.
        This field may be omitted if there are no such requirements.
    """
    myApiCmd = '/users/' + myUsername + '/hubs/' + myHubId + '/version'
    # myParams = {'criticality': 'high'}
    jsonResponse,state = myApiCall(myApiCmd, None, 'GET')
    return jsonResponse,state
#
def putHubVersion(myUsername, myHubId):
    """ PUT /users/:username/hubs/:hubId/version
    Description:
        Instructs the hub to upgrade it's firmware to the latest version.
    Arguments:
        version -- LATEST
    Sample Response:
        HTTP 202
        {
            "result":  "HUB_UPGRADE_REQUESTED"
        }
        Returned errors:
            400 MISSING_PARAMETER -- Version parameter is missing.
            400 INVALID_PARAMETER -- Version parameter is invalid (only valid value in current API version is LATEST).
    """
    myApiCmd = '/users/' + myUsername + '/hubs/' + myHubId + '/version'
    myParams = {'version':'LATEST'}
    jsonResponse,state = myApiCall(myApiCmd, myParams, 'PUT')
    return jsonResponse,state
    #
def postHubImageGroupId(myUsername, myHubId, myGroupName):
    """/users/:username/hubs/:hubId/imagegroupid?groupName=3.7r58
    Description:
        Change the hub group (FW version that will installed on next upgrade)
        The group name need to be identified from available groupnames in the version management part
        of the staff site for the specific server.
        So to automate the upgrade script :
            1) Set Groupname you want to update to on specific account using above API
            2) Upgrade using API ( same  as you use today )
    Arguments:
        groupName = 3.7r58 (or the version you looked up on staffsite)
        Note: The groupName string does not always match the version returned by getHubVersion so
        when cehcking you need to know both.  Typical values are...
        latestVersion == '2.52r07' and groupId == '2.52r7 for test'
        latestVersion == '2.52r08' and groupId == '2.52r8'
    Sample Response:
    """
    myApiCmd = '/users/' + myUsername + '/hubs/' + myHubId + '/imagegroupid'
    myParams = {'groupName':myGroupName}
    jsonResponse,state = myApiCall(myApiCmd, myParams, 'POST')
    return jsonResponse,state
    #
def factoryRestoreHub(myUsername, myHubId):
    """ /users/:username/hubs/:hubId
    Description:
    Factory restore the account/hub. This can take up to 5mins to complete.
    """
    myApiCmd = '/users/' + myUsername + '/hubs/' + myHubId
    jsonResponse,state = myApiCall(myApiCmd, None, 'POST')
    return jsonResponse,state
    #
def putRebootHub(myUsername, myHubId):
    """ PUT /users/:username/hubs/:hubId/power
    Description:
    Changes the power state of a hub - currently this is limited to rebooting the hub
    Arguments:
    power = REBOOT
    Sample Response:
    HTTP 204 Rebooting
    """
    myApiCmd = '/users/' + myUsername + '/hubs/' + myHubId + '/power'
    myParams = {'power':'REBOOT'}
    jsonResponse,state = myApiCall(myApiCmd, myParams, 'PUT')
    return jsonResponse,state

def getColdAlert(myUsername, myHubId, myDevice):
    '''GET /users/:userid/hubs/:hubid/devices/all/:deviceId/events/TooCold/behaviours/ALL
    Description:
        Returns a list of all configured events for the low temperature warning.
        NIGHT:{'actions': [{'type': 'SendEmail', 'message': '[template:tooCold]?temp=10.0&deviceName=Your Receiver', 'to': 'me'}], 'temperature': 10}
        AWAY:{'actions': [{'type': 'SendEmail', 'message': '[template:tooCold]?temp=10.0&deviceName=Your Receiver', 'to': 'me'}], 'temperature': 10}
        HOME:{'actions': [{'type': 'SendEmail', 'message': '[template:tooCold]?temp=10.0&deviceName=Your Receiver', 'to': 'me'}], 'temperature': 10}
    '''
    myApiCmd = '/users/{0}/hubs/{1}/devices/all/{2}/events/TooCold/behaviors/ALL'.format(myUsername, myHubId, myDevice.id)
    jsonResponse,state = myApiCall(myApiCmd, None, 'GET')
    return jsonResponse,state
def getHotAlert(myUsername, myHubId, myDevice):
    ''' GET /users/:userid/hubs/:hubid/devices/all/:deviceId/events/TooHot/behaviours/ALL
    '''
    myApiCmd = '/users/{0}/hubs/{1}/devices/all/{2}/events/TooHot/behaviors/ALL'.format(myUsername, myHubId, myDevice.id)
    jsonResponse,state = myApiCall(myApiCmd, None, 'GET')
    return jsonResponse,state

def getDevices(myUsername, myHubId):
    """ GET /users/:username/hubs/:hubId
    Description:
        Returns a list of devices attached to the given hub
    Response:
        Returns a list of all devices associated with this hub
    """
    myApiCmd = '/api/users/' + myUsername + '/hubs/' + myHubId + '/devices'
    jsonResponse,state = myApiCall(myApiCmd, None, 'GET')
    return jsonResponse,state
    #
def getDevicesStatus(myUsername, myHubId):
    """ GET /users/{username}/hubs/{hubId}/services/support/devicesStatus
    Description:
        Returns a list of all devices (including the hub) and their current status.
    """
    myApiCmd = '/users/' + myUsername + '/hubs/' + myHubId + '/services/support/devicesStatus'
    jsonResponse,state = myApiCall(myApiCmd, None, 'GET',myNumOfRetries=0)
    return jsonResponse,state
    #
def getDeviceSingle(myUsername, myHubId, myDeviceType, myDeviceId ):
    """ GET / users/:username/hubs/:hubid/devices/:devicetype/:deviceid
    """
    myApiCmd = '/users/{0}/hubs/{1}/devices/{2}/{3}'.format(myUsername, myHubId, myDeviceType, myDeviceId)
    jsonResponse,state = myApiCall(myApiCmd, None, 'GET')
    return jsonResponse,state
def getDevicesOnly(myUsername, myHubId, myDeviceType):
    """ GET /users/:username/hubs/:hubId/devices/:deviceType/only
    Description:
        Shortcut for all calls beginning with /devices/:deviceType/:deviceId
        Available when only one device of :deviceType (including special value of "all") is installed on the hub.
    Response:
    Returned errors:
        404 NO_SUCH_DEVICE       - There is no device of :deviceType installed on the hub.
        400 MORE_THAN_ONE_DEVICE - There are more than one device of :deviceType installed on the hub.
    """
    myApiCmd = '/users/' + myUsername + '/hubs/' + myHubId + '/devices/' + myDeviceType + '/only'
    jsonResponse,state = myApiCall(myApiCmd, None, 'GET')
    return jsonResponse,state
    #
def getDeviceStatus(myUsername, myHubId, myDeviceType, myDeviceId):
    """ GET  /devices/:deviceType/:deviceId/status
    Description:
        Return status information for the device
    Keyword Arguments:
        myDeviceType (string) -- Device type
        myDeviceId (string)   -- Device ID
    Response:
        Sample Response:
        {
           "battery": 95,
           "batteryLow": false,
           "power": 100,
           "signal": 100,
           "presence": true,
           "temperature": null,
           "version": "2.01r16"
        }
    """
    myApiCmd = '/users/' + myUsername + '/hubs/' + myHubId + \
               '/devices/' + myDeviceType + '/' + myDeviceId + '/status'
    jsonResponse,state = myApiCall(myApiCmd, None, 'GET')
    return jsonResponse,state
    #
def getDeviceVersion(myUsername, myHubId, myDeviceType, myDeviceId):
    """ GET /users/:username/hubs/:hubId/devices/:deviceType/:deviceId/version
    Description:
        Returns the details of a device's upgrade status.  Can be used to establish
        if the device is eligible for upgrades.
    Keyword Arguments:
        myDeviceType (string) -- Target device type
        myDeviceId (string)   -- Target device id
    API Arguments:
        criticality - high/medium/low
    Sample Response:
    """
    myApiCmd = '/users/' + myUsername + '/hubs/' + myHubId + \
               '/devices/' + myDeviceType + '/' + myDeviceId + '/version'
    #myParams = {'criticality': 'high'}
    jsonResponse,state = myApiCall(myApiCmd, None, 'GET')
    return jsonResponse,state
    #
def putDeviceVersion(myUsername, myHubId, myDeviceType, myDeviceId):
    """ PUT /users/:username/hubs/:hubId/devices/:deviceType/:deviceId/version
    Description:
        Instructs the device to upgrade to the latest version.
    Arguments:
        version -- LATEST
    Sample Response:
        HTTP 202
        {
            "result":  "HUB_UPGRADE_REQUESTED"
        }
        Returned errors:
            400 MISSING_PARAMETER -- Version parameter is missing.
            400 INVALID_PARAMETER -- Version parameter is invalid (only valid value in current API version is LATEST).
    """
    myApiCmd = '/users/' + myUsername + '/hubs/' + myHubId + \
               '/devices/' + myDeviceType + '/' + myDeviceId + '/version'
    myParams = {'version':'LATEST'}
    jsonResponse,state = myApiCall(myApiCmd, myParams, 'PUT')
    return jsonResponse,state
    #
def getTopology(myUsername, myHubId):
    """ GET /users/:u/hubs/:h/devices/topology
    """
    myApiCmd = '/users/' + myUsername + '/hubs/' + myHubId + '/topology'
    jsonResponse,state = myApiCall(myApiCmd, None, 'GET')
    return jsonResponse,state
    #
def getHomeStatus(myUsername):
    """ GET /users/{username}/widgets/homestatus
    """
    myApiCmd = '/users/{0}/widgets/homestatus'.format(myUsername)
    myParams = {'detail':'hub devices'}
    jsonResponse,state = myApiCall(myApiCmd, myParams, 'GET')
    return jsonResponse,state
    #
def getChannels(myUsername, myHubId, myDeviceType, myDeviceId):
    """ GET /users/:username/hubs/:hubId/devices/:deviceType/:deviceId/channels
    Description:
        Get the supported channel list for the specified device
        Channels represent the data available from each device.
        For example presence, power, temperature.
    Keyword arguments:
        myDeviceType (string) -- 'Lamp' = Hub, 'HeatingController' = Thermostat
        myDeviceId (string)   -- Device ID
    Response:
        List of channels for given device
    """
    myApiCmd = '/users/' + myUsername + '/hubs/' + myHubId + '/devices/' + \
                myDeviceType + '/' + myDeviceId + '/channels'
    jsonResponse,state = myApiCall(myApiCmd, None, 'GET')
    return jsonResponse,state
    #
def getChan(myUsername, myHubId, myDeviceType, myDeviceId, myChannel, myStart, myEnd, myInterval, myOperations):
    """ GET /users/:username/hubs/:hubId/devices/:deviceType/:deviceId/channels/:channel
    Description:
        Get device data from a single channel of a given device.
        When called without any arguments, it returns the current channel value for given device, if available.
        When the following arguments are passed, it returns the historical channel data.
    Keyword arguments:
        myDeviceType (string) -- 'Lamp' = Hub, 'HeatingController' = Thermostat
        myDeviceId (string)   -- Device ID   Keyword arguments:
        myChannel (String)    -- Data Channel
        myStart (integer)     -- UTC Unix Timestamp
        myEnd (integer)       -- UTC Unix Timestamp
        myInterval(string)    -- Sample interval in seconds (120,3600,86400 as of 3/3/2013)
                                 The power channel has additional intervals of 1, 30 and 60 for Meter Readers, and 30 and 60 for SmartPlugs.
                                 The cost channel only supports intervals of 300, 3600 and 86400.
        myOperations (string) -- average, min, max, amount. e.g. 'averageminmax'
                                 As of 3/3/2013, amount is the sole operation available for the cost channel.
    Response:
        {
            "start":1262199600,
            "end": 1262199900,
            "interval": 60,
            "values":
            {
                "average": [1544, 1546, 1344, 1544, 1546, 1344],
                "min": [1543, 1545, 1342, 1543, 1545, 1342],
                "max": [1545, 1547, 1345, 1545, 1547, 1345],
                "amount": 123
            }
        }
        Brief explanation of returned fields:
        start - The time of the first returned sample and therefore may not match with the provided start argument
        end   - The time of the last returned sample and therefore may not match with the provided end argument
        interval - The real sampling interval. May not match provided interval argument (e.g. if interval=1 is provided for a device other
                   than a Meter Reader, then the interval will be changed to the minimum interval available for that device);
                   if the only operation requested is "amount" then this field will not be in the response
        values - is an associative array, containing one entry (array or value) per requested operation; each entry is named after the operation itself
    """
    # Build the API Call URI
    myApiCmd = '/users/' + myUsername + '/hubs/' + myHubId + '/devices/' + \
               myDeviceType + '/' + myDeviceId + '/channels/' + myChannel

    # Build the parameters
    myParams = {'start': str(myStart),\
                'end': str(myEnd),\
                'interval': str(myInterval),\
                'operation': myOperations}

    # Make the API call
    jsonResponse,state = myApiCall(myApiCmd, myParams, 'GET')
    return jsonResponse,state
    #
def getDeviceData(myUsername, myHubId, myDeviceList, myStartTime, myEndTime):
    """ Retrieves data from devices and channels as listed in wantedDevices and
        wantedChannels (at top of this module), for given time period.
    Description:
        A list of all devices are retrieved.
        For each device in the wantedDevice list get the channel data as listed in the wantedChannel
        list (at the top of this module). An API call is made for each channel to get the data.
        Data is printed to the screen.
    Keyword Arguments:
        myDevices (dict)      -- Target devices (response from getDevices method)
        myStartTime (integer)  -- UTC Unix Timestamp
        myEndTime (integer)   -- UTC Unix Timestamp
    """

    # This needs to be re-factored to:
    #
    #   Get channel data (from wantedDeviceChannels) - Think there is no need to check channels first - assume it is available.
    #   Loop for channels and devices
    #
    #   Also refactor the wantedDevice and wantedChannelParameters dictionaries to make a single
    #   dict and then use the keys from that as the iteration parameter

    myDataList=[]
    for device in myDeviceList:
        if device.type in deviceChannelParameters:
            # Get the names of the available data channels
            channels,state = getChannels(myUsername, myHubId, device.type, device.id)
            if state!=0:
                print('ERROR: getChannels, {}'.format(state))
            
            for myChan in channels:
                if myChan['name'] in deviceChannelParameters[device.type]:
                    interval = deviceChannelParameters[device.type][myChan['name']]['interval']
                    operations = deviceChannelParameters[device.type][myChan['name']]['operations']
                    myData,state = getChan(myUsername,
                                     myHubId,
                                     device.type,
                                     device.id,
                                     myChan['name'],
                                     myStartTime,
                                     myEndTime,
                                     interval,
                                     operations)
                    if state==0:
                        myDataList.append((device.type,myChan['name'],myData))
                    else:
                        print('ERROR: Error with get data, {}',format(state))
    return myDataList
def getTargetTempHistory(myUsername, myHubId, myDeviceId, myYear, myMonth, myDay, myHour):
    """ GET /climate/:deviceId/targetTemperature/history
    Description:
        Returns the temperature setpoint history for a given period.  Currently restricted in resolution.
    Attributes:
        Period       Required parameters                                            Interval      Date format
        custom       year_from, month_from, day_from, year_to, month_to, day_to     1 day         2011-02-15
        thisHour                                                                    15 minutes    2011-02-15 9:45
        today                                                                       30 minutes    2011-02-15 9:30
        yesterday                                                                   30 minutes    2011-02-15 9:30
        thisWeek                                                                    1 day         2011-02-15
        thisMonth                                                                   1 day         2011-02-15
        thisYear                                                                    1 month       2011
        hourView     year, month, day, hour                                         15 minutes    2011-02-15 9:45
        hourView     year, month, day, hour                                         30 minutes    2011-02-15 9:30
        weekView     year, week                                                     1 day         2011-02-15
        monthView    year, month                                                    1 day         2011-02-15
        yearView     year                                                           1 month       2011
        /climate/:deviceId/targetTemperature/history?period=hourView&year=2010&month=11&day=23&hour=15
    """
    myApiCmd = '/users/' + myUsername + '/hubs/' + myHubId + '/climate/' + \
               myDeviceId + '/targetTemperature/history'

    myParams = {'period':'hourView','year':myYear,'month':myMonth,'day':myDay,'hour':myHour}
    jsonResponse,state = myApiCall(myApiCmd, myParams, 'GET')
    return jsonResponse,state
def getHotWaterStatus(myUsername, myHubId, myDeviceId):
    """ GET /users/:username/hubs/:hubId/devices/HotWaterController/:deviceId
    """
    myApiCmd = '/users/' + myUsername + '/hubs/' + myHubId + '/devices/HotWaterController/' + myDeviceId
    jsonResponse,state = myApiCall(myApiCmd, None, 'GET')
    return jsonResponse,state
def getHotWaterScheduleOld(myUsername, myDeviceId):
    """ GET /users/:username/widgets/hotwater/:deviceId/controls/schedule
    Description:
        Returns the current schedule and other information for schedule mechanism.
    """
    myApiCmd = '/users/' + myUsername + '/widgets/hotwater/' + myDeviceId + '/controls/schedule'
    jsonResponse,state = myApiCall(myApiCmd, None, 'GET')
    return jsonResponse,state
def getHotWaterSchedule(myUsername, myHubId, myDeviceId):
    """ GET /users/:username/hubs/:hubId/devices/HotWaterController/:deviceId/controls/schedule
    Description:
        Returns the current hot water schedule and other information.
    """
    myApiCmd = '/api/users/' + myUsername + '/hubs/' + myHubId + \
               '/devices/HotWaterController/' + myDeviceId + '/controls/schedule'
    myParams={'precision':0.5}
    jsonResponse,state = myApiCall(myApiCmd, myParams, 'GET')
    return jsonResponse,state

def getHeatScheduleOld(myUsername):
    """ GET /users/:username/widgets/heating/detail
    Description:
        Returns the current schedule and other information for schedule mechanism.
    """
    myApiCmd = '/users/' + myUsername + '/widgets/heating/detail'
    jsonResponse,state = myApiCall(myApiCmd, None, 'GET')
    return jsonResponse,state
def getHeatSchedule(myAccount, myDeviceId):
    """ GET /users/:username/widgets/climate/:deviceId/controls/schedule
    Description:
        Returns the current schedule and other information for heating.
    """
    myApiCmd = '/api/users/' + myAccount.username + '/widgets/climate/' + \
               myDeviceId + '/controls/schedule'
    # Build the parameters
    myParams = {'precision':0.5}
    jsonResponse,state = myApiCall(myApiCmd, myParams,'GET')
    return jsonResponse,state
def postHeatSchedule(myAccount, myDeviceId, mySched, myNumOfEvents):
    """ POST /users/:username/widgets/climate/:deviceId/controls/schedule
    Description:
        Sets the controller's schedule
    Attributes:
        mode=HEAT
        temperatureUnit=C
        numberOfSetPoints=4
        days[monday][0][time] = 12:35
        days[monday][0][temperature] = 12
    """
    # Build the parameter set
    myParams={}
    myParams['mode']='HEAT'
    myParams['temperatureUnit']='C'
    myParams['numberOfSetpoints']=str(myNumOfEvents)

    daysOfWeek=['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    for day in daysOfWeek:
        for event in range(0,myNumOfEvents):
            timeArgument='days[' + day + '][' + str(event) + ']' + '[time]'
            tempArgument='days[' + day + '][' + str(event) + ']' + '[temperature]'
            myParams[timeArgument]=mySched[day][event]['time']
            myParams[tempArgument]=mySched[day][event]['temperature']

    myApiCmd = '/users/' + myAccount.username + '/widgets/climate/' + \
               myDeviceId + '/controls/schedule'
    jsonResponse,state = myApiCall(myApiCmd, myParams, 'POST')
    return jsonResponse,state
    #

def getHeatMode(myAccount, myDeviceId):
    username = 'flashtest4@yopmail.com'
    """GET /users/:username/widgets/climate/:deviceId
    """
    myApiCmd = '/users/' + username + '/widgets/climate/' + myDeviceId
    jsonResponse,state = myApiCall(myApiCmd, None, 'GET')
    return jsonResponse,state
#
def putHeatMode(myUsername,myDeviceId,myMode):
    """PUT/climate/:deviceId/control
    Description: Change the heat mode to OFF, MANUAL or AUTO/SCHEDULE
    Parameters:
        control = MANUAL, SCHEDULE, OFF
    """
    myApiCmd = '/users/' + myUsername + '/widgets/climate/' + myDeviceId + '/control'
    myParams = {'control':myMode}
    jsonResponse,state = myApiCall(myApiCmd,myParams,'PUT')
    return jsonResponse,state
#
def putTargetTemperature(myUsername,myDeviceId,myTemperature):
    """PUT /users/:username/widgets/climate/:deviceId/targetTemperature
    Description:
        Sends the new temperature target to the TStat
        If in Schedule/Auto mode this will result in TStat entering Override mode
    Arguments:
        temperatureUnit=C
        temperature=25
    """
    myApiCmd = '/users/' + myUsername + '/widgets/climate/' + myDeviceId + \
               '/targetTemperature'
    myParams = {'temperatureUnit':'C','temperature':myTemperature}
    jsonResponse,state = myApiCall(myApiCmd,myParams,'PUT')
    return jsonResponse,state
def getTargetTemperature(username):
    """GET /users/:username/widgets/climate/targetTemperature
    Description:
        Sends the new temperature target to the TStat
        If in Schedule/Auto mode this will result in TStat entering Override mode
    Arguments:
        temperatureUnit=C
        temperature=25
    """
    myApiCmd = '/api/users/' + username + '/widgets/climate/targetTemperature'
    myParams = None
    jsonResponse,state = myApiCall(myApiCmd,myParams,'GET')
    return jsonResponse,state
def getControlMode(username):
    """GET /users/{username}/widgets/climate/control
    
    """
    myApiCmd = '/users/{0}/widgets/climate/control'.format(username)
    myParams = None
    jsonResponse,state = myApiCall(myApiCmd,myParams,'GET')
    return jsonResponse,state    

def getLocalTemperature(username):
    """GET /users/{username}/widgets/climate/control
    
    """
    myApiCmd = '/api/users/{0}/widgets/temperature'.format(username)
    myParams = None
    jsonResponse,state = myApiCall(myApiCmd,myParams,'GET')
    return jsonResponse,state   

def getHeatDetails(username):
    """GET /users/{username}/widgets/climate
    
    """
    myApiCmd = '/api/users/{0}/widgets/climate'.format(username)
    myParams = None
    jsonResponse,state = myApiCall(myApiCmd,myParams,'GET')
    return jsonResponse,state 

def getHeatModeNew(username):
    """GET /users/{username}/widgets/climate/control
    
    """
    myApiCmd = '/api/users/{0}/widgets/climate/control'.format(username)
    myParams = None
    jsonResponse,state = myApiCall(myApiCmd,myParams,'GET')
    return jsonResponse,state 

def getHotWaterModeAndRunState(username, myDeviceId):
    """GET /users/{username}/widgets/Hotwater/DeviceID
    
    """
    myApiCmd = '/api/users/' + username + '/widgets/hotwater/' + myDeviceId 
    myParams = None
    jsonResponse,state = myApiCall(myApiCmd,myParams,'GET')
    return jsonResponse,state 

def getNodes():
    """GET /users/{username}/widgets/Hotwater/DeviceID
    
    """
    myApiCmd = '/nodes'
    myParams = None
    jsonResponse,state = myApiCall(myApiCmd,myParams,'GET')
    return jsonResponse,state 


  
def postWaterSchedule(myUsername, myDeviceId, mySched, myNumOfEvents):
    """ POST /users/:username/widgets/hotwater/:deviceId/controls/schedule
        Description:
            Sets the controllers hot water schedule
        Attributes:
            numberOfEvents         4
            temperatureUnit        C
            days[monday][0][time]  06:00
            days[monday][0][op]    ON
            days[monday][1][time]  09:00
            days[monday][1][op]    ON
            ...
            OR
            numberOfEvents             4
            temperatureUnit            C
            days[weekdays][0][time]    06:00
            days[weekdays][0][op]      ON
            days[weekdays][1][time]    09:00
            days[weekdays][1][op]      ON
            ...
    """
    # Build the parameter set
    myParams={}
    myParams['temperature']='C'
    myParams['numberOfEvents']=str(myNumOfEvents)

    daysOfWeek=['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    for day in daysOfWeek:
        for event in range(0,myNumOfEvents):
            timeArgument='days[' + day + '][' + str(event) + ']' + '[time]'
            opArgument='days[' + day + '][' + str(event) + ']' + '[op]'
            myParams[timeArgument]=mySched[day][event]['time']
            myParams[opArgument]=mySched[day][event]['op']

    myApiCmd = '/users/' + myUsername + '/widgets/hotwater/' + \
               myDeviceId + '/controls/schedule'
    jsonResponse,state = myApiCall(myApiCmd, myParams, 'POST')
    return jsonResponse,state
def deleteUser(myUsername, confirmationRequired=True):
    """ DELETE /users/:username
    """
    print("")
    print("*********  WARNING ************")
    print(" ABOUT TO DELETE = ",myUsername)
    print("*******************************")
    
    proceed = False
    if confirmationRequired==False:
        proceed = True
    elif input("Continue Y/n?") == 'Y':
        proceed = True
    
    if proceed:
        #myApiCmd = '/users/' + myUsername
        #myParams = None
        myApiCmd = '/users'
        myParams = {'username':myUsername, 'ignoreExistingHubs':'true'}
        jsonResponse,state = myApiCall(myApiCmd, myParams, 'DELETE')
    else:
        jsonResponse = "Delete Aborted."
        state = 0
        print("Delete Aborted.")
        print()
    return jsonResponse, state

def getExportUserData(myUsername):
    """ GET /users/:username/widgets/climate/:deviceId/controls/schedule
    Description:
        Returns the current schedule and other information for heating.
    """
    myApiCmd = '/users/{0}/exportUserData'.format(myUsername)
    # Build the parameters
    myParams = {'hubRequired':'true'}
    jsonResponse,state = myApiCall(myApiCmd, myParams,'GET')
    return jsonResponse,state

def postUserGroup(myGroupName):
    """ POST /userGroups
        Create a new user group
    """
    myApiCmd = '/userGroups'
    myParams = {'name' : myGroupName}
    jsonResponse,state = myApiCall(myApiCmd, myParams, 'POST')
    return jsonResponse,state

def getDiagnostics(myUserName):
    """ GET /management/diagnostics/users/{username}
    
    """
    myApiCmd = '/management/diagnostics/users/{}'.format(myUserName)
    myParams = None
    jsonResponse,state = myApiCall(myApiCmd, myParams, 'GET')
    return jsonResponse,state