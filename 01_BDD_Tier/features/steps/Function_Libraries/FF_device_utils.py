'''
Created on 14 Oct 2015

@author: ranganathan.veluswamy
'''


import json
import subprocess, time, os
import FF_utils as utils
import FF_threadedSerial as AT
import FF_loggingConfig as config
import platform
import serial
import sys

strAppiumConnectionString = "/Applications/Appium.app/Contents/Resources/node/bin/node " + \
                                                "/Applications/Appium.app/Contents/Resources/node_modules/appium/bin/appium.js  --log-level error"
                                                
strAppiumConnectionString = "/Applications/Appium.app/Contents/Resources/node/bin/node " + \
                                                "/Applications/Appium.app/Contents/Resources/node_modules/appium/bin/appium.js " + \
                                                "--address 127.0.0.1 --command-timeout  \"7200\"  --debug-log-spacing " + \
                                                "--no-reset " + \
                                                 "--native-instruments-lib --log-level error"
                                                 


strAndroidAppFilePath = '/Users/ranganathan.veluswamy/Downloads/Hive-productV6Internalprod-release-1.2.0.47.apk'
strADBPath = '/Users/ranganathan.veluswamy/Desktop/Ranga/RnD/Appium/android-sdk-macosx/platform-tools/'

strEnvironmentFolderPAth = os.path.abspath(__file__ + "/../../../../../02_Manager_Tier/EnviromentFile/")
def get_connected_android_devices():
    oProcess = subprocess.Popen(strADBPath + "adb devices", stdout=subprocess.PIPE, shell=True)
    #oProcess = subprocess.Popen("$ANDROID_HOME/platform-tools/adb devices", stdout=subprocess.PIPE, shell=True)
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
    return deviceList

def install_app_android_device(strAndroidAppFilePath):
    strAppPakage = utils.getAttribute('android', 'appPackage')
    print(strAppPakage)
    oDeviceList = get_connected_android_devices()
    for strDeviceID in oDeviceList:
        #Uninstall the existing App
        subprocess.call(strADBPath + "adb -s " +  strDeviceID +" uninstall " + strAppPakage, shell=True)
        #Install the App
        subprocess.call(strADBPath + "adb -s " +  strDeviceID +" install -rg " + strAndroidAppFilePath, shell=True)
    
def create_android_device_json():
    killall_nodes()
    intPort = 4723
    intBootStrap = 4724
    oDeviceList = get_connected_android_devices()
    if len(oDeviceList) == 0:
        oDeviceList = get_connected_android_devices()
        
    oADLJsonDict = getAndroidDeviceListJson()
    oADLJsonDict['android_devicelist'] = {}
    intIndex = 1
    for oDevice in oDeviceList:
        strPort = str(intPort)
        strBootStrap = str(intBootStrap)
        strDeviceNode = 'device' + str(intIndex)
        oADLJsonDict['android_devicelist'][strDeviceNode] = {}
        oADLJsonDict['android_devicelist'][strDeviceNode]['device_id'] = oDevice
        oADLJsonDict['android_devicelist'][strDeviceNode]['port'] = strPort
        oADLJsonDict['android_devicelist'][strDeviceNode]['bootstrap'] = strBootStrap
        # + ' --address 127.0.0.' + strPort[3:] 
        strDeviceAppiumConnectionString = strAppiumConnectionString + ' -p ' + strPort + ' -bp ' + strBootStrap #+ ' -U ' + oDevice
        oADLJsonDict['android_devicelist'][strDeviceNode]['appium_connection_string'] = strDeviceAppiumConnectionString
        launch_appium_server(strDeviceAppiumConnectionString)
        oADLJsonDict['android_devicelist'][strDeviceNode]['status'] = 'Not Started'
        oADLJsonDict['android_devicelist'][strDeviceNode]['execution_start_time'] = ""
        intIndex = intIndex + 1
        intPort = intPort + 2
        intBootStrap = intBootStrap + 2
        
    putAndroidDeviceListJson(oADLJsonDict)

def killall_nodes():
    subprocess.Popen("killall node", shell=True)
    time.sleep(5)
    '''subprocess.call('adb kill-server', shell=True)
    time.sleep(10)'''
    subprocess.call('adb start-server', shell=True) 
    time.sleep(10)
def getPort():
    #Set Network Path
    networkBasePath = ""
    PORT = ""
    if 'DARWIN' in platform.system().upper():
        networkBasePath = '/volumes/hardware/'
        PORT = '/dev/tty.SLAB_USBtoUART'
    elif 'LINUX' in platform.system().upper():        
        networkBasePath = '/home/pi/hardware/'
        PORT = '/dev/ttyUSB0'
    elif sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
        result = []
        FinalPort = ""
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
                FinalPort = port
            except (OSError, serial.SerialException):
                pass
        print(result)
        networkBasePath = "\\\\nas1\Hardware\\"
        PORT = FinalPort
        print('Windows '+FinalPort+'\n')
    else:
        networkBasePath = ""
        PORT = config.PORT
        print('I should not be hereeeee \n')
    return PORT
def launch_appium_server(strAppiumConString):
    print(strAppiumConString)
    subprocess.Popen(strAppiumConString, shell=True)

def getAndroidDeviceListJson():
    strAndroidDeviceListPath = strEnvironmentFolderPAth + '/android_device_list.json'    
    strJson = open(strAndroidDeviceListPath, mode='r')
    oADLJsonDict = json.loads(strJson.read())
    strJson.close() 
    return oADLJsonDict

def putAndroidDeviceListJson(oADLJsonDict):
    strNodeClustAttrPath = strEnvironmentFolderPAth + '/android_device_list.json'    
    #Write back the JSON to the GlobalVar.JSON
    oJson = open(strNodeClustAttrPath, mode='w+')
    oJson.write(json.dumps(oADLJsonDict, indent=4, sort_keys=False))
    oJson.close()
    
def getNodes(boolATStarted = True):
    if not boolATStarted: 
        AT.stopThread.clear()  
        
        status, statusMessage = AT.startSerialThreads(getPort(), config.BAUD, printStatus=False, rxQ=True, listenerQ=True)
        if not status:             
            putZigbeeDevicesJson({})
            return {}
    intListCounter = 1
    NodeList,oAllNodes = initiateNodeList()
    intCounter = 0
    boolFlag = True
    while boolFlag:
        boolFlag = False
        for oNode in NodeList:
            myNodeId = oNode[1]
            myType = oNode[2]
            myModelName = oNode[4]
            mychildNodeList = []
            if myType != "RFD" and oNode[0] != "ID":
                _, _, rows = utils.getNtable(myNodeId) 
                intCounter = 0
                for oRow in rows:
                    mytype = ""
                    intInnerCounter = 0
                    if intCounter > 0:
                        oItems = oRow.split("|")
                        if "No" not in oItems[0]:
                            for oItem in oItems:
                                'Get Device Type'
                                if intInnerCounter == 1:
                                    mytype = oItem.replace(" ","")
                                
                                'Get Device Mac Address'
                                if intInnerCounter == 2:
                                    macID = oItem.replace(" ","")
                                
                                'Get Device Model, End Point, Name and append to the list'
                                if intInnerCounter == 3:
                                    if not any(oItem.replace(" ","") == e[1] for e in NodeList):
                                        strModel = utils.getDeviceModeId(oItem.replace(" ",""))
                                        NodeList.append([])
                                                     
                                        'Naming the devices'
                                        strModelTemp = strModel
                                        strModel = namingDevices(strModelTemp,oAllNodes)
                                        oAllNodes[strModel] = {}
                                        NodeList[intListCounter].append(macID)
                                        NodeList[intListCounter].append(oItem.replace(" ","")) #NodeID
                                        NodeList[intListCounter].append(mytype)
                                        _, _, endPoints = AT.discEndpoints(oItem.replace(" ",""))
                                        NodeList[intListCounter].append(endPoints) #EndPoints
                                        NodeList[intListCounter].append(strModel) #name  
                                        mychildNodeList.append(oItem.replace(" ",""))
                                        NodeList[intListCounter].append([])
                                        intListCounter += 1
                                        boolFlag = True
                                        
                                        'Add to dictionary'
                                        oAllNodes[strModel]["nodeID"] = oItem.replace(" ","")
                                        oAllNodes[strModel]["type"] = mytype
                                        oAllNodes[strModel]["macID"] = macID
                                        oAllNodes[strModel]["name"] = strModelTemp
                                        oAllNodes[strModel]["endPoints"] = endPoints
                                intInnerCounter += 1
                    intCounter += 1
                    
                    'Add child Nodes'
                    if len(mychildNodeList) > 0:
                        for oNode in NodeList:
                            oAllNodes[myModelName]["childNodes"] = mychildNodeList
                    elif 'childNodes' not in oAllNodes[myModelName]:
                        oAllNodes[myModelName]["childNodes"] = []
    if not boolATStarted: 
        AT.stopThreads()
    putZigbeeDevicesJson(oAllNodes)
    return oAllNodes

def namingDevices(strModelTemp,oAllNodes):
    intDeviceCntr = 0
    strModel = strModelTemp
    while True:                                            
        intDeviceCntr = intDeviceCntr + 1
        strModel = strModelTemp + "_" + str(intDeviceCntr)
        if strModel in oAllNodes: continue
        else: break
    return strModel

def initiateNodeList():
    _, _, rows = utils.getNtable('0000')
    NodeList = []
    NodeList.append([])
    _, _, myDstAddr = AT.getEUI('0000', '0000')
    NodeList[0].append(myDstAddr)
    NodeList[0].append("0000")
    NodeList[0].append("COO")
    NodeList[0].append("--")
    NodeList[0].append("TGStick")
    NodeList[0].append([])
    
    oAllNodes = {}
    oAllNodes["TGStick"] = {}
    oAllNodes["TGStick"]["nodeID"] = "0000"
    oAllNodes["TGStick"]["type"] = "COO"
    oAllNodes["TGStick"]["macID"] = myDstAddr
    oAllNodes["TGStick"]["name"] = "TGStick"
    oAllNodes["TGStick"]["endPoints"] = []
    return NodeList,oAllNodes

def getNodeIDbyDeciveID(deviceID, boolATStarted = True):
    oNodeList = getZigbeeDevicesJson()
    nodeID = ""
    if deviceID in oNodeList: nodeID = oNodeList[deviceID]['nodeID']
    return nodeID

def getDeviceNode(deviceID, boolATStarted = True):
    oNodeList = getZigbeeDevicesJson()
    Node = ""
    if deviceID in oNodeList: Node = oNodeList[deviceID]
    return Node

def putZigbeeDevicesJson(oADLJsonDict):
    strNodeClustAttrPath = strEnvironmentFolderPAth + '/zigbeeDevices.json'    
    #Write back the JSON to the GlobalVar.JSON
    oJson = open(strNodeClustAttrPath, mode='w+')
    oJson.write(json.dumps(oADLJsonDict, indent=4, sort_keys=False))
    oJson.close()

def getZigbeeDevicesJson():
    strAndroidDeviceListPath = strEnvironmentFolderPAth + '/zigbeeDevices.json'    
    strJson = open(strAndroidDeviceListPath, mode='r')
    oZDLJsonDict = json.loads(strJson.read())
    strJson.close() 
    return oZDLJsonDict

    #return NodeList
if __name__ == '__main__':
    '''create_android_device_json()
    install_app_android_device(strAndroidAppFilePath)'''
    pass