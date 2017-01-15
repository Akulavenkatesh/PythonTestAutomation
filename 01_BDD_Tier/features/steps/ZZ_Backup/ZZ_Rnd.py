'''
Created on 22 May 2015

@author: ranganathan.veluswamy

import time
from datetime import timedelta

intTCStartTime = time.monotonic()
time.sleep(3)
intTCEndTime = time.monotonic()
strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
print("<th colspan='4'>Execution Duration: " + strTCDuration + "</th>\n") #.format(strTCDuration))
'''
#from Reporter import Reporter
import json
from PIL.ImageEnhance import Brightness
'''
import features.steps.steps.scheduleTest as st
import features.steps.utilities.threadedSerial as AT
import features.steps.utilities.loggingConfig as config
import time

AT.stopThread.clear()  # Reset the threads stop flag for serial port thread and attribute listener thread.
    
# Start the serial port read/write threads and attribute listener thread
AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False)
AT.startAttributeListener(printStatus=False)
strNodeID = '380C'
strEndPoint = '05'
oThermostatEP = st.thermostatEndpoint(strNodeID, strEndPoint)
oThermostatEP.update()    


print(st.buildRandomSchedule(6, '07D0', 15))
time.sleep(5)  


#print(st.buildRandomSchedule(4,20))
'''
'''
schedule={'fri': [('13:15', 20.0), ('13:30', 29.0), ('13:45', 15.0), ('14:00', 30.0), ('14:15', 1.0), ('14:30', 10.0)]}
oThermostatEP.setSchedule(schedule)
oThermostatEP.setMode('AUTO')
'''
'''
intHour = 23
intMinute = 30
if (intHour < 0  or intHour > 23) or (intMinute< 0 or intMinute >59):
    print ('True')

    
oList = [(20.0, '13:15'), (29.0, '13:30'), (15.0, '13:45'), (30.0, '14:00'), (1.0, '14:15'), (10.0, '14:30')]

for intcntr in range(len(oList)):
    print (oList[intcntr])
       
    
strEvent = ""
for intCntr in range(1,7):
    strEvent = strEvent + 'Event ' + str(intCntr) + '$$'
strEvent = strEvent[:len(strEvent) - 2]
print(strEvent)

oScheduleList =[('13:15', 20.0), ('13:30', 29.0), ('13:45', 15.0), ('14:00', 30.0), ('14:15', 1.0), ('14:30', 10.0)]
for intCntr in range(len(oScheduleList)):
    print(str(intCntr) + + '...' +oScheduleList[intCntr][0] + '==> ' + oScheduleList[intCntr][0])

intMin =122
print('print{:02d}'.format(intMin))    

intMinute = 200

print(intMinute + (15 - intMinute%15))

import steps.AA_Steps_Schedule as stsh
oSchedule = {'mon': [('06:30', 18.0), ('08:30', 1.0), ('12:00', 1.0), ('14:00', 16.0), ('16:30', 18.0), ('22:00', 1.0)], 'wed': [('06:30', 18.0), ('08:30', 1.0), ('12:00', 1.0), ('14:00', 1.0), ('16:30', 18.0), ('22:00', 1.0)], 'sat': [('06:30', 18.0), ('08:30', 1.0), ('12:00', 1.0), ('14:00', 1.0), ('16:30', 18.0), ('22:00', 1.0)], 'tue': [('06:30', 18.0), ('08:30', 1.0), ('12:00', 1.0), ('14:00', 1.0), ('16:30', 18.0), ('22:00', 1.0)], 'sun': [('06:30', 18.0), ('08:30', 1.0), ('12:00', 1.0), ('14:00', 1.0), ('16:30', 18.0), ('22:00', 1.0)], 'thu': [('06:30', 18.0), ('08:30', 1.0), ('12:00', 1.0), ('14:00', 1.0), ('16:30', 18.0), ('22:00', 1.0)], 'fri': [('06:30', 18.0), ('08:30', 1.0), ('12:00', 1.0), ('14:00', 1.0), ('16:30', 18.0), ('22:00', 1.0)]}
print(stsh.getCurrentTempFromSchedule(oSchedule))

intRowCount = 2
for intTmp in range(6 - intRowCount):
    print("hi")

def temp():
    return 1,2

intF = temp()

print(intF)
from datetime import datetime
print(60 - int(datetime.today().strftime("%S" )))


import random
import features.steps.steps.scheduleTest as st
import steps.AA_Steps_Schedule as stSc
hd=[]
numberOfEvents =6
for i in range(0,numberOfEvents):
    hd.append(random.choice([True, False]))
    print(stSc.buildCompleteRandomSchedule(numberOfEvents,'07D0'))
print(hd)

print(st.buildRandomSchedule(6, '07D0', 15))
 

 
import steps.AA_Steps_Schedule as stSc
print(stSc.makeSixSceduleFormat([('11:45', 23.0), ('13:45', 31.5), ('16:00', 16.0), ('16:15', 9.0)]))


import random


for intCntr in range(0,100):
    print(random.randrange(2, 8, 2))
     '''
#print("6.0".isnumeric())
'''
import json

oFile = open('/users/Ranganathan.veluswamy/Desktop/json.output')
oJson = json.load(oFile)

for item in oJson:
    for oKey in item.keys():
        print(oKey)
        

import steps.CC_platformAPI as pAPI

oPlatformAPI = pAPI.platformAPIClass('isopBeta')
oheat = oPlatformAPI.heatEP

oheat.update()
print('***********')
print(oheat.localTemperature)

#*******
print('MANUL sdfs'.split()[0])    

import time
print(time.time() * 1000)
import json    
strFilePath = '/Users/ranganathan.veluswamy/Desktop/Ranga/Workspace/EclipseWorkspace/HiveTestAutomation/01_Manager_Tier/EnviromentFile/GlobalVar.json'

strJson = open(strFilePath, mode='r')
oJsonDict = json.loads(strJson.read())
print(oJsonDict) 



strCurrentEnv = oJsonDict['globalVariables']['currentEnvironment']
oCurrentEnvDetailsDict = oJsonDict['globalVariables']['listOfEnvironments'][strCurrentEnv]


print(oCurrentEnvDetailsDict['iOS']['deviceName'])

#print(round(x))

round_up = lambda num: int(num + 1) if int(num) != num else int(num)

x = 1.9
x=x-0.5
print(round_up(x))

exit()

from jira.client import JIRA
options = {
'server': 'https://jira.bgchtest.info'
}
jira = JIRA(options)

projects = jira.projects()

print(len(projects))
      
   
   ''' '''

import subprocess
import time


import calendar
from datetime import datetime, timedelta
import time

import steps.FF_utils as utils


from datetime import datetime, timedelta


from datetime import datetime, timedelta


from tkinter import *



class Application(Frame):
    def say_hi(self):
        print( "hi there, everyone!")

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "left"})

        self.hi_there = Button(self)
        self.hi_there["text"] = "Hello",
        self.hi_there["command"] = self.say_hi

        self.hi_there.pack({"side": "left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
'''
'''
top = kinter.Tk()
# Code to add widgets will go here...
top.mainloop()
  '''
'''  
from datetime import datetime, timedelta
import steps.FF_convertTimeTemperature as tt
  
holidayStartOffset = 60  # Start offset from now in seconds.
#strHoldayStart = (datetime.now() + timedelta(seconds=holidayStartOffset)).replace(second=0,microsecond=0)     

print(timedelta(seconds=holidayStartOffset))
'''

'''utils.onOffTest('0671', 'ON', False)

time.sleep(10)

utils.onOffTest('0671', 'OFF', False)
'''

'''from datetime import datetime, timedelta
import calendar
d = datetime.utcnow()
unixtime = calendar.timegm(d.utctimetuple())
print(datetime.today())
print(d.strftime("%H:%M:%S" ))

intSetTempDuration = 60
holidayStartOffset = 60  # Start offset from now in seconds.
strHoldayStart = (datetime.utcnow() + timedelta(seconds=holidayStartOffset)).replace(second=0,microsecond=0)     
strHoldayEnd = (strHoldayStart + timedelta(seconds=intSetTempDuration))

print(strHoldayStart,strHoldayEnd)'''

#print (time.mktime(time.gmtime(unixtime)).strftime("%H:%M:%S" ))

'''import steps.FF_loggingConfig as config
import steps.FF_threadedSerial as AT
import steps.FF_utils as utils
import time


AT.stopThread.clear()  
AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False)
#AT.startAttributeListener(printStatus=False)
#AT.getInitialData('B672', fastPoll=True, printStatus=True)


BMID = utils.discoverNodeIDbyCluster('0201')[2]
time.sleep(3)
SPID = utils.discoverNodeIDbyCluster('0006')[2]
time.sleep(3)
NTAble = utils.getNtable('ff')[2]
boolTHfound = False
for oRow in NTAble:
    if 'RFD' in oRow:
        THID = oRow.split('|')[3].strip()
        boolTHfound = True
if not boolTHfound:
    NTAble = utils.getNtable(BMID)[2]
    for oRow in NTAble:
        if 'RFD' in oRow:
            THID = oRow.split('|')[3].strip()
            boolTHfound = True
if not boolTHfound:
    NTAble = utils.getNtable(SPID)[2]
    for oRow in NTAble:
        if 'RFD' in oRow:
            THID = oRow.split('|')[3].strip()
            boolTHfound = True
            
print('BM: ', BMID)
print('TH: ', THID)
print('SP: ', SPID)


print("@@@@@@@@@@@@@@@@@@@@")

print(utils.getAllClustersAttributes(BMID, "BM"))

utils.setBind(THID, '09',  '0020')
AT.fastPollStart(THID)
print(utils.getAllClustersAttributes(THID, "TH"))
AT.fastPollStop()
print(utils.getAllClustersAttributes(SPID,"SP"))

AT.stopThreads()'''

'''striOSAppiumConnectionString = "/Applications/Appium.app/Contents/Resources/node/bin/node \
                                                /Applications/Appium.app/Contents/Resources/node_modules/appium/bin/appium.js \
                                                --address 127.0.0.1 --command-timeout \"7200\" --debug-log-spacing \
                                                --no-reset \
                                                 --native-instruments-lib --log-level \"error\""
print(striOSAppiumConnectionString)                        
'''

'''                                            
from subprocess import Popen, PIPE

stdout = Popen('adb devices', shell=True, stdout=PIPE).stdout
output = stdout.read()
print(output)'''
'''oWeekDay = ['sun','mon','tue','wed','thu','fri','sat'] 
intToday = int(datetime.today().strftime("%w" ))
intYesterday = int(datetime.today().strftime("%w" )) -1
if intYesterday == -1: intYesterday = 6
intTomorrow = int(datetime.today().strftime("%w" )) + 1
if intTomorrow == -1: intTomorrow = 0
strToday = oWeekDay[intToday]
strYesterday = oWeekDay[intYesterday]
strTomorrow = oWeekDay[intTomorrow]
print(strYesterday,strToday,strTomorrow)'''
'''import filelock

lock = filelock.BaseFileLock("/Users/ranganathan.veluswamy/Documents/VRISHU.JPG")
with lock.acquire():
    pass
print(lock.is_locked)
try:
    pass
finally:
    lock.release(True)
print(lock.is_locked)'''
'''from lockfile import LockFile
lock = LockFile("/Users/ranganathan.veluswamy/Documents/VRISHU.JPG")
lock.acquire()
print(lock.is_locked())
print(lock.path, 'is locked.')
lock.release()
print(lock.is_locked())


import subprocess, time, os
oProcess = subprocess.Popen("/Users/ranganathan.veluswamy/Desktop/Ranga/RnD/Appium/android-sdk-macosx/platform-tools/adb devices", stdout=subprocess.PIPE, shell=True)
#oProcess = subprocess.Popen("$ANDROID_HOME/platform-tools/adb devices", stdout=subprocess.PIPE, shell=True)
#oProcess = subprocess.call("./getDeviceList.sh", shell=True)
print('Test suite Triggered')
time.sleep(3)
deviceList = []
while True:
    output = oProcess.stdout.readline()
    if oProcess.poll() is not None:
        break
    if output:
        #print(output)
        if not 'DEVICES' in str(output).upper():
            if 'DEVICE' in str(output).upper():
                deviceList.append(str(output).split("\\t")[0].split("'")[1].strip())
    else:
        break
print(deviceList)
print("@@@@@@@@@@@Successfully completed", output)  '''
'''intTemp = '4321'
print(intTemp[3:])'''
'''
def getShellCommandOutput(strCmd):
    
    oProcess = subprocess.Popen(strCmd, stdout=subprocess.PIPE, shell=True)
    #oProcess = subprocess.Popen("$ANDROID_HOME/platform-tools/adb devices", stdout=subprocess.PIPE, shell=True)
    outputList = []
    while True:
        output = oProcess.stdout.readline()
        if oProcess.poll() is not None:
            break
        if output:
            outputList.append(str(output))
            #outputList.append(output)
        else:
            break
    print(outputList)
    return outputList

oKitDetList = []
#oFileList = get_connected_android_devices("ssh rpi2 \"cd /dev; ls\"")
#oFileList = getShellCommandOutput("ssh rpi2 ls /dev | grep \"USB\"")
#oFileList = getShellCommandOutput("ls /dev | grep \"USB\"")

oKitDetails = getShellCommandOutput("ssh rpi2 \"source env/bin/activate; python workspace/HiveTestAutomation/01_BDD_Tier/features/get_TG_devices_details.py\"")

for oKitDetail in oKitDetails:
    oKitDetail = oKitDetail.replace("b'", "").replace("\\n'", "")
    if 'OBMDICT' in oKitDetail.upper() or 'OTHDICT' in oKitDetail.upper():
        oKitDetList.append(oKitDetail)

print(oKitDetList)'''
'''
from win_unc import UncCredentials, UncDirectory, UncDirectoryConnection
 
# Describe your UNC path:
simple_unc = UncDirectory(r'\\path\to\remote\directory')
 
# Or provide credentials if you need them:
creds = UncCredentials('username', 'myp@ssw0rd')
authz_unc = UncDirectory(r'\\path\to\authz\directory', creds)
 
# Setup a connection handler:
conn = UncDirectoryConnection(authz_unc)
conn.connect()
 
#do something meaningful...
 
conn.disconnect()
assert(not conn.is_connected())'''
'''
import serial
port = '/dev/tty.SLAB_USBtoUART'
baud = 19200
try:
    serial_port = serial.Serial(port, baud, timeout=10)
    input("hi")
except IOError as e:
    print('Error opening port.',e)'''
'''import os
strFolderPath = 'smb://172.19.1.200/hardware'
local_dir = os.path.abspath(strFolderPath)
retcode = subprocess.call(["/sbin/mount", "-t", "smbfs", remote_dir, local_dir])
if retcode != 0:
    raise OSError("mount operation failed")

strPath = 'smb://172.19.1.200/hardware/tokens.txt'
local_dir = os.path.abspath(strPath)
oFileReader = open(strPath, 'r')
oFileReader.close()'''
'''import os
import smb
from xbmc import xbmcvfs

strPath = 'smb://ranganathan.veluswam:password-1@nas1/hardware/tokens.txt'
local_dir = os.path.abspath(strPath)
oFileReader = open(strPath, 'r')
oFileReader.close()'''
'''import tempfile
from smb.SMBConnection import SMBConnection

# There will be some mechanism to capture userID, password, client_machine_name, server_name and server_ip
# client_machine_name can be an arbitary ASCII string
# server_name should match the remote machine name, or else the connection will be rejected
userID = 'Ranganathan.Veluswam'
password = 'password-1'
client_machine_name = 'hardware'
server_name = 'nas1'
server_ip = '172.19.1.200'
conn = SMBConnection(userID, password, client_machine_name, server_name, use_ntlm_v2 = True)
assert conn.connect(server_ip, 445)

    '''
'''# Open a file
fd = open( "/volumes/Hardware/tokens.txt",  'w' )

# Write one string
fd.write("This is test")
fd.close()'''
 #Ensures the dirPath exists, if not creates the same
'''def ensure_dir(dirpath):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    return dirpath

import platform
import socket
import getpass
import time
strAPI = "Zigbee"
if 'ZIGBEE' in strAPI.upper():
    strAPIFolder = 'Device_Test_Automation'
else: strAPIFolder = 'Web-Mobile_Test_Automation'
strSystemResultFolderName = ''
if 'DARWIN' in platform.system().upper():
    if os.path.exists("/volumes/hardware"):
        strSystemResultFolderName = getpass.getuser() + "_" + socket.gethostname().split(".")[0]
        strTestResultFolder ="/volumes/hardware/" + strAPIFolder + '/Test_Results/'
        ensure_dir(strTestResultFolder + strSystemResultFolderName)
elif 'LINUX' in platform.system().upper():
    if os.path.exists("/home/pi/hardware"):
        strSystemResultFolderName = socket.gethostname().split(".")[0].split("-")[1]
        strTestResultFolder ="/home/pi/hardware/" + strAPIFolder + '/Test_Results/'
        ensure_dir(strTestResultFolder + strSystemResultFolderName)'''
'''from datetime import datetime
file = '/Users/ranganathan.veluswamy/Desktop/Ranga/Workspace/EclipseWorkspace/HiveTestAutomation/03_Results_Tier/Beta_Android_Auto_Batch_23-Oct-2015_10-47-17'

arrCreationDtTime = time.ctime(os.stat(file).st_ctime).split(" ")
strMonth = arrCreationDtTime[1]
strYear = arrCreationDtTime[4]
strDay = arrCreationDtTime[2]
print(strDay, strMonth, strYear)

timestamp = os.stat(file).st_ctime
dt_obj = datetime.fromtimestamp(os.stat(file).st_ctime)
print(datetime.strftime(dt_obj, "%b"))'''
'''import time
intStartTime = time.time()
time.sleep(5)
intEndTime = time.time()
print(int(intEndTime-intStartTime))'''
'''import fcntl
import serial


for tty in ['serial.Serial(0)']:
    try:
        port = serial.Serial(0) #serial.Serial(port=tty[0])
        if port.isOpen():
            try:
                fcntl.flock(port.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except IOError:
                print ('Port {0} is busy'.format(tty))
    except serial.SerialException as ex:
        print( 'Port {0} is unavailable: {1}'.format(tty, ex))'''
'''
import steps.FF_threadedSerial as AT
import steps.FF_loggingConfig as config
import steps.FF_utils as utils

AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False)

_,_, resp =utils.get_device_constants("FD90")
for oRow in resp.split("$$"):
    print(oRow)
AT.stopThreads()
'''
'''for intCntr in range(5):
    print(intCntr)

print(len([1,2,3]))

mySetpointFloat = 30.0

print("{:04x}".format(int(mySetpointFloat*100)))'''

from datetime import datetime
import os 
import subprocess
import time
from datetime import timedelta
import json



'''oSchedule = []
oState = ["ON", "OFF"]
for intDayIndex in range(1,8):
    oTransitions = []
    intStateIndexCntr = intDayIndex
    for intDeltaminutes in range(0, 1440, 240):
        oDayStartTime = datetime.strptime('01Jan2016', '%d%b%Y')
        strTime = oDayStartTime + timedelta(minutes = intDeltaminutes)
        intStateIndex = intStateIndexCntr%2
        print(strTime.strftime("%H:%M" ), oState[intStateIndex])
        oTransitions.append({"time": strTime.strftime("%H:%M" ), "action":{"state":oState[intStateIndex]}})
        intStateIndexCntr = intStateIndexCntr + 1
    oSchedule.append({"dayIndex":intDayIndex,"transitions":oTransitions})

oScheduleDict = {
                            "nodes":[
                                {
                                    "attributes":{
                                       "syntheticDeviceConfiguration":{
                                           "targetValue":{
                                              "enabled":"true",
                                               "schedule":oSchedule
                                            }
                                        }
                                    }
                                 }
                            ]
                        }
print(oScheduleDict)
print(json.dumps(oScheduleDict))'''






'''    nodeId = "7416"
    ep = "09"
    intTCStartTime = time.monotonic()
    respState,_,resp = utils.check_device_back_after_restart(nodeId, ep)
    intTCEndTime = time.monotonic()
    strTCDuration = str(timedelta(seconds=intTCEndTime - intTCStartTime))
    strTCDuration = utils.getDuration(strTCDuration)
    print(resp)
    input("hhh")
    return'''


'''lightSensorCalibration = {0: (500, 800),
                                         20:(1100, 1400),
                                         40:(2800, 3200),
                                         60:(4800, 5200),
                                         80:(7500, 8000),
                                         100:(10300, 11100)}


intBrightness = 20
intLowLimit = lightSensorCalibration[intBrightness][0]
intHighLimit = lightSensorCalibration[intBrightness][1]

print(intLowLimit)'''


'''import steps.FF_alertmeApi as ALAPI 
import steps.FF_utils as utils

ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
session =ALAPI.superUserSessionObject()

hubIDResp = ALAPI.getHubIdV6(session, "tester9_v6")
hubID = hubIDResp[0]["internalHubState"]["id"]
strModel = "SLP2"

strUpgradeStatus = ""
fltProgress = 0.0
intCntr = 1
intPercentagePrintCntr = 1.0
while strUpgradeStatus!="COMPLETE":
    time.sleep(2)
    hubLogJson = ALAPI.getHubLogsV6(session, hubID)
    for oDict in hubLogJson["internalNodeStates"]:
        if 'model' in oDict:
            if strModel == oDict["model"]:
                if "upgradeState" in oDict:
                    strUpgradeStatus = oDict["upgradeState"]["status"]
                    print(strUpgradeStatus)
                    if "progress" in oDict["upgradeState"]:
                        fltProgress = float(oDict["upgradeState"]["progress"])
                else: 
                    print("Upgrade not happenning")
                    break
        else: 
            print("Device Node is missing")
            break  
    
    if fltProgress >= intPercentagePrintCntr * 10.0:
        print(intCntr, strUpgradeStatus, fltProgress)
        intPercentagePrintCntr = intPercentagePrintCntr + 1.0
    
    intCntr = intCntr + 1
    if intCntr > 3600:
        break


ALAPI.deleteSessionV6(session)'''


'''import steps.FF_alertmeApi as ALAPI 
import steps.FF_utils as utils

ALAPI.createCredentials(utils.getAttribute('common', 'currentEnvironment'))
session =ALAPI.sessionObject()
hubID = "649b7236-0a8f-4ac4-b2e0-54258c3e8302"

ALAPI.rebootHubV6(session, hubID)

ALAPI.deleteSessionV6(session)'''

'''myDuration = 100
transitionDuration = '{:02x}'.format(int(myDuration*2.55))
print(transitionDuration)   
    '''


'''import steps.FF_Platform_Utils as pUtils

deviceType = "FWBULB01_1"
currentDeviceNodeId = pUtils.getDeviceNodeID(deviceType)
mode, CurrentDeviceState, activeLightBrightness = pUtils.getLightAttributes(currentDeviceNodeId)

print(mode, CurrentDeviceState, activeLightBrightness)

print(pUtils.getDeviceScheduleInStandardFormat(deviceType))
'''
'''if __name__ == '__main__':
    print("ksdhfkjhaslkjfdfhalskjhfkjas")
    exit()'''

'''import numpy as np
import pylab

import colour
from colour.plotting import *'''
'''
# Conversion from RGB to chromaticity coordinates.
# Defining RGB values for reference.
RGB_r = np.array([1, 0, 0])
RGB_g = np.array([0, 1, 0])

# We assume they are encoded in *sRGB* colourspace.
XYZ_r =  sRGB_to_XYZ(RGB_r, apply_EOCF=False)
XYZ_g = colour.sRGB_to_XYZ(RGB_g, apply_EOCF=False)

# Conversion to chromaticity coordinates.
xy_r = colour.XYZ_to_xy(XYZ_r)
print(xy_r)
# [ 0.64  0.33]

xy_g = colour.XYZ_to_xy(XYZ_g) 
print(xy_g)
# [ 0.3  0.6]


# Conversion to CIE xyY in order to maintain Luminance ratios.
# Using sRGB Luminance ratios, second row of the NPM.
xyY_r = [0.64, 0.33, colour.sRGB_COLOURSPACE.RGB_to_XYZ_matrix[1, 0]]
xyY_g = [0.3, 0.6, colour.sRGB_COLOURSPACE.RGB_to_XYZ_matrix[1, 1]]

xy_s = colour.XYZ_to_xy(
    colour.sRGB_to_XYZ(
        colour.XYZ_to_sRGB(colour.xyY_to_XYZ(xyY_r), apply_OECF=False) +
        colour.XYZ_to_sRGB(colour.xyY_to_XYZ(xyY_g), apply_OECF=False)))
print(xy_s)
# [ 0.41930366  0.50525886]

# Plotting.
RGB_colourspaces_CIE_1931_chromaticity_diagram_plot(
    ('sRGB', ),
    bounding_box=(-0.1, 0.9, -0.1, 0.9), 
    standalone=False)

pylab.plot(xy_r[0], xy_r[1], 'o', markersize=15, color=RGB_r)
pylab.plot(xy_g[0], xy_g[1], 'o', markersize=15, color=RGB_g)
pylab.plot(xy_s[0], xy_s[1], 'o', markersize=15, color=RGB_s)
'''


''' 
import time

print (time.monotonic())
time.sleep(5)

print (time.monotonic())


'''






import steps.FF_threadedSerial as AT

AT.debug = True

pass


def moveToHueAndSat(myNodeId,myEp,hue,sat,myDuration='0000'):
    
    sendMode=1
    myMsg='AT+CCMVTOHUS:{},{},{},{},{},{}'.format(myNodeId,myEp,sendMode,hue,sat,myDuration)
    #expectedResponses=['DFTREP:0EE1,01,0300,0A,00']
    expectedResponses=['DFTREP:{},{},{},(..)'.format(myNodeId,myEp,'0300')]
    expectedResponses = ['OK']
    respState,respCode,respValue=AT.sendCommand(myMsg, expectedResponses)
    return respState,respCode,respValue

def moveToHue(myNodeId,myEp,hue,myDuration='0000'):
    
    sendMode=0
    hexdirection = '05'
    myMsg='AT+CCMVTOHUE:{},{},{},{},{},{}'.format(myNodeId,myEp,sendMode,hue,hexdirection,myDuration)
    #expectedResponses=['DFTREP:0EE1,01,0300,0A,00']
    expectedResponses=['DFTREP:{},{},{},(..)'.format(myNodeId,myEp,'0300')]
    respState,respCode,respValue=AT.sendCommand(myMsg, expectedResponses)
    print(respState,respCode,respValue)
    return respState,respCode,respValue


'''

PORT = '/dev/tty.SLAB_USBtoUART'
BAUD = 115200

AT.debug = True


AT.stopThread.clear()  
# Start the serial port read/write threads and attribute listener thread
AT.startSerialThreads(PORT, BAUD, printStatus=False, rxQ=True, listenerQ=True)

myNodeId = '157C'
myNodeId = '496E'
myNodeId = '0001'

myEp = '01'
sat = 'Fe'




for intHue in range(0,255):
    hexHue = '{:02x}'.format(intHue)
    print(hexHue)
    moveToHueAndSat(myNodeId,myEp,hexHue,sat,myDuration='0000')
    #moveToHue(myNodeId,myEp,hexHue,myDuration='0000')
    time.sleep(2)


'''



lstBrightness = [10,20,30,40,50,60,70,80,90,100]
myColourTemp = 2700

'''
for intBrightness in lstBrightness:
    AT.moveToLevel(myNodeId, myEp, 0, 100, 1)
    time.sleep(1)
    #AT.colourTemperature(myNodeId, myEp, 0, 2700, 10)
    time.sleep(1)
    AT.moveToLevel(myNodeId, myEp, 0, intBrightness, 100)
    for intT in range(0,10):
        time.sleep(1)        
        respState, respCode, respValue = AT.getAttribute(myNodeId, myEp, '0008', '0000', 'server')        
        expHexBrightness = intBrightness
        actHexBrightness = int((int(respValue, 16)*100)/255)
        print(intT, expHexBrightness, actHexBrightness)
    AT.onOff(myNodeId, myEp, 0, 0)
    time.sleep(3)
    AT.onOff(myNodeId, myEp, 0, 1)
    time.sleep(3)
    
    respState, respCode, respValue = AT.getAttribute(myNodeId, myEp, '0008', '0000', 'server')
    
    expHexBrightness = intBrightness
    actHexBrightness = int((int(respValue, 16)*100)/255)
    print(expHexBrightness, actHexBrightness)
#AT.colourTemperature(myNodeId, myEp, 0, 6500, 10)

'''
'''

moveToHueAndSat(myNodeId,myEp,'00',sat,myDuration='0000')
#moveToHue(myNodeId,myEp,'CC',myDuration='0000')
for intBrightness in lstBrightness:
    AT.moveToLevel(myNodeId, myEp, 0, 100, 1)
    time.sleep(1)
    #AT.colourTemperature(myNodeId, myEp, 0, 2700, 10)
    
    if (intBrightness/10) % 2 == 0:
        hexHue = 'CC'
    else: hexHue = '00'
    #moveToHueAndSat(myNodeId,myEp,hexHue,sat,myDuration='012C')
    moveToHue(myNodeId,myEp,hexHue,myDuration='012C')
    time.sleep(1)
    #AT.moveToLevel(myNodeId, myEp, 0, intBrightness, 300)
    
    
    for intT in range(0,35):
        time.sleep(1)        
        respState, respCode, respValue = AT.getAttribute(myNodeId, myEp, '0008', '0000', 'server')        
        expHexBrightness = intBrightness
        actHexBrightness = int((int(respValue, 16)*100)/255)
        print(intT, expHexBrightness, actHexBrightness, 'Brightness')
        
        respState, respCode, respValue = AT.getAttribute(myNodeId, myEp, '0300', '0000', 'server') 
        
        print(intT, hexHue, respValue, 'HUE')
        
    AT.onOff(myNodeId, myEp, 0, 0)
    time.sleep(3)
    AT.onOff(myNodeId, myEp, 0, 1)
    time.sleep(3)
    
    respState, respCode, respValue = AT.getAttribute(myNodeId, myEp, '0008', '0000', 'server')
    
    expHexBrightness = intBrightness
    actHexBrightness = int((int(respValue, 16)*100)/255)
    print(intT, expHexBrightness, actHexBrightness, 'Brightness')


    respState, respCode, respValue = AT.getAttribute(myNodeId, myEp, '0300', '0000', 'server') 
    
    print(intT, hexHue, respValue, 'HUE')
        
#AT.colourTemperature(myNodeId, myEp, 0, 6500, 10)



AT.stopThreads()

print("done")



'''







import steps.FF_threadedSerial as AT
import steps.FF_utils as utils

'''PORT = '/dev/tty.SLAB_USBtoUART'
BAUD = 115200

AT.debug = False

AT.stopThread.clear()  
# Start the serial port read/write threads and attribute listener thread
AT.startSerialThreads(PORT, BAUD, printStatus=False, rxQ=True, listenerQ=True)

myNodeId = 'CA6B'

#utils.createBaselineDeviceAttrbDumpJson(myNodeId)



AT.stopThreads()'''
'''
from steps.FF_Reporter import Reporter
reporter = Reporter()  
strExecSummaryHTMLFilePath = reporter.HTML_Execution_Summary_Initialize()
reporter.strCurrentScenarioID = "Test"
reporter.HTML_TestCase_Initialize(reporter.strCurrentScenarioID )
reporter.HTML_Execution_Summary_TCAddLink()
reporter.HTML_TC_Iteration_Initialize(1)

baselineDumpFile = "/Users/ranganathan.veluswamy/Desktop/Ranga/Workspace/EclipseWorkspace/HiveTestAutomation/02_Manager_Tier/EnviromentFile/Device_Attribute_Dumps/TWBulb01UK_Baseline_Dump.json"
latestDumpFile = "/Users/ranganathan.veluswamy/Desktop/Ranga/Workspace/EclipseWorkspace/HiveTestAutomation/02_Manager_Tier/EnviromentFile/Device_Attribute_Dumps/Latest_Attribute_Dump/TWBulb01UK_11140002_Dump.json"


oJson = open(baselineDumpFile, mode='r')
oBSDumpJson = json.loads(oJson.read())
oJson.close() 

oJson = open(latestDumpFile, mode='r')
oLatestDumpJson = json.loads(oJson.read())
oJson.close() 


print(oBSDumpJson["DeviceVersion"])


strHeader = "Cluster$$"  + "Attribute ID$$" + "Attribute Name$$" + "Attribute Type$$" +"Default Value$$" + " ReportableConfigState$$" + "@@@"
strLog = ""   

for ep in sorted(oBSDumpJson["ListOfEndPoints"].keys()):
    oEP = oBSDumpJson["ListOfEndPoints"][ep]
    strExpEndPoint = oEP["EndPoint"]
    for oClust in sorted(oEP["ListOfClusters"].keys()):
        oClust = oEP["ListOfClusters"][oClust]
        strExpClusterID = oClust["ClusterID"]
        strExpClusterName = oClust["ClusterName"]
        strExpClusterTYpe = oClust["ClusterType"]
        if strExpClusterID + "_" + strExpClusterName in oLatestDumpJson["ListOfEndPoints"][ep]["ListOfClusters"]: 
            oActClust = oLatestDumpJson["ListOfEndPoints"][ep]["ListOfClusters"][strExpClusterID + "_" + strExpClusterName]            
            strActClusterID = oActClust["ClusterID"]
            strActClusterName = oActClust["ClusterName"]
            strActClusterTYpe = oActClust["ClusterType"]
        else:
            oActClust = oClust
            strExpClusterID = "||" + strExpClusterID
            if strExpClusterTYpe != strActClusterTYpe:
                strExpClusterTYpe = "||" + strExpClusterTYpe +" ==> " + strActClusterTYpe
            
            boolFirstAttr = True
            for oAttr in sorted(oClust["ListOfAttributes"].keys()):
                oAttr = oClust["ListOfAttributes"][oAttr]
                strExpAttrID = oAttr["AttributeID"]
                strExpAttrName = oAttr["AttributeName"]
                strExpAttrType = oAttr["AttributeType"]
                strExpAttrValue = oAttr["DefaultValue"]
                strExpAttrRCS = oAttr["ReportableConfigState"]
                if strExpAttrID + "_" + strExpAttrName in oActClust["ListOfAttributes"]:
                    oActAttr = oActClust["ListOfAttributes"][strExpAttrID + "_" + strExpAttrName]                    
                    strActAttrName = oActAttr["AttributeName"]
                    strActAttrType = oActAttr["AttributeType"]
                    strActAttrValue = oActAttr["DefaultValue"]
                    strActAttrRCS = oActAttr["ReportableConfigState"]
                    
                    if strExpAttrType != strActAttrType:
                        strExpAttrType =  "||" + strExpAttrType +" ==> " + strActAttrType
                    if strExpAttrValue != strActAttrValue:
                        strExpAttrValue =  "||" + strExpAttrValue +" ==> " + strActAttrValue
                    if strExpAttrRCS != strActAttrRCS:
                        strExpAttrRCS =  "||" + strExpAttrRCS +" ==> " + strActAttrRCS
                    
                    if boolFirstAttr: 
                        strLog = strLog + "$~" +  strExpClusterID + "_" + strExpClusterName + '&R&'+str(len(oClust["ListOfAttributes"])) + "$$" + strExpAttrID + "$$" + strExpAttrName + "$$" + strExpAttrType + "$$" + strExpAttrValue + "$$" + strExpAttrRCS
                    else: 
                        strLog = strLog + "$~" + strExpAttrID + "$$" + strExpAttrName + "$$" + strExpAttrType + "$$" + strExpAttrValue + "$$" + strExpAttrRCS
                    #strLog = strLog + "$~" + strExpClusterID + "_" + strExpClusterName + "$$" + strExpAttrID + "$$" + strActAttrName + "$$" + strExpAttrType + "$$" + strExpAttrValue + "$$" + strExpAttrRCS
                    boolFirstAttr = False
                    
                    
reporter.ReportEvent('Test Validation', strHeader + strLog, 'Done')           
print(strHeader + strLog)         
exit()
print("done")



'''













'''myDuration = 1
durationHex="{:04x}".format(myDuration*60)  

print(durationHex)


'''

'''
import steps.FF_device_utils as utils

print(utils.getNodes())

'''

fileList = ["HAS01UK_01015730_OTA.ota", "HAS01UK_02025730_OTA.ota"]
'''strLower = ""
strUpper = ''
strLowerFileName = ""
strUpperFileName = ""
for f in fileList:                    
    file = f.rpartition('/')[2]
    if ".OTA" in str(file).upper():
        print(str(file) + "\n")
        i = fileList.index(f)
        if strUpper == "":
            strUpper = str(file).split("_")[1]
            strUpperFileName = fileList[int(fileList.index(f))]
        else:
            intUpper = int(strUpper)
            intLower = int(str(file).split("_")[1])
            if intLower == intUpper:
#                 context.reporter.ReportEvent("Test Validation","The folder contains same OTA Files","Fail")
                exit()
            elif intUpper > intLower:
                strLower = str(intLower)
                strLowerFileName = fileList[int(fileList.index(f))]
            else:
                strLowerTemp = strLower
                strLower = strUpper
                strLowerFileName = strUpperFileName
                strUpper = strLowerTemp
                strUpperFileName = fileList[int(fileList.index(f))]
        print("{0:>2}. {1}".format(i,file))

'''
'''oDictOTAFiles = {}
strLower = ""
strUpper = ''
strLowerFileName = ""
strUpperFileName = ""
for f in fileList:                    
    file = f.rpartition('/')[2]
    if ".OTA" in str(file).upper():
        print(str(file) + "\n")
        strUpper = str(file).split("_")[1]
        strUpperFileName = f
        oDictOTAFiles[strUpper] = strUpperFileName
oSortedFileVersions = sorted(oDictOTAFiles)
DeviceVersion1 = oSortedFileVersions[0]
DeviceVersion2 =  oSortedFileVersions[1]
print("1 ="+DeviceVersion1)
print("\n 2 ="+DeviceVersion2)'''

