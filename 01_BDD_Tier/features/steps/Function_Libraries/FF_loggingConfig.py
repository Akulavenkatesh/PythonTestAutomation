# Config file for attribute logging script
# Make sure USB is inserted and joined to the wanted network
# Enter BM node Id below.
import FF_zigbeeClusters as zbc
import os

# Logging on/off used to control scripts that are running.
# They look for the file to confirm they should continue to run.
# If no file then exit the script
loggingOn=False

# loggingOn/Off is controlled via a file.  if file exists then logging is on.
# touch the file to create it, delete it to turn logging off.
# Logging scripts shall check for this file and exit if it has been deleted.
# This provides a way to stop a running script.
ctrlFile = '/tmp/logging_on'
if loggingOn:
    open(ctrlFile,'a').close()
else:
    if os.path.isfile(ctrlFile):
        os.remove(ctrlFile)

firmwareRootFilePath = '/Users/ranganathan.veluswamy/Google Drive/firmware-release-notes/'
# firmwareRootFilePath = '/volumes/hardware/firmware-release-notes/'

# Log file used for attribute logger
#logfile = '/home/pi/google_drive/attributeLogs.txt'
logfile = '/Users/keith/Google_Drive/Python/alertme_api_logs/logs/attributeLogs.txt'

# Serial Port Parameters
#PORT = '/dev/ttyUSB0'
PORT = '/dev/tty.SLAB_USBtoUART'
BAUD = 115200

node1 = "52A3"


# nodes & endpoints 7c62
nodeList = [{'node':'25EA','ep1':'05','ep2':None}] #,
            #{'node':'DB43','ep1':'09','ep2':None}]

ATTRS = "hiveAttrs"

class hiveAttrs(object):
    def __init__(self,nodeList):
        
        self.tstat_heat_attrs =  [('0000','0001','003C'),
                                  ('0012','0001','0078'),
                                  ('001C','0001','0078'),                 
                                  ('0023','0001','0078'),
                                  ('0024','0001','0078'),
                                  ('0029','0001','0078')]
    
        self.tstat_water_attrs = [('001C','0001','0078'),
                                  ('0023','0001','0078'),
                                  ('0024','0001','0078'),
                                  ('0029','0001','0078')]
    
        self.bg_clust_attrs    = [('0020','0001','0078'),
                                  ('0021','0001','0078'),
                                  ('0022','0001','0078'),
                                  ('0023','0001','0078'),
                                  ('0024','0001','0078'),
                                  ('0025','0001','0078'),                 
                                  ('0026','0001','0078'), 
                                  ('0027','0001','0078'),                  
                                  ('0031','0001','0078')]

        # attrReports shall contain one line per node/cluster/ep combination (i.e. one row per required binding)
        self.attrReports = []        
        for n in nodeList:
            self.attrReports.append({'nodeId':n['node'],'epId':n['ep1'],'clustName':'Thermostat Cluster', 'attrs':self.tstat_heat_attrs})
            self.attrReports.append({'nodeId':n['node'],'epId':n['ep2'],'clustName':'Thermostat Cluster', 'attrs':self.tstat_water_attrs})
            self.attrReports.append({'nodeId':n['node'],'epId':n['ep1'],'clustName':'BG Cluster', 'attrs':self.bg_clust_attrs})
    
        return
class plugAttrs(object):
    def __init__(self,nodeList):
        self.pwrConfigAttrs=[('0000','0078','0078'), # mainsVoltage
                             ('0001','0078','0078')] # mainsFrequency
        
        self.deviceTempConfigAttrs=[('0000','0078','0078')] # currentTemperature
    
        self.onOffAttrs = [('0000','0078','0078')] # onOff
    
        self.meterAttrs = [('0000','0078','0078'), # currentSummationDelivered
                           ('0006','0078','0078'), # powerFactor
                           ('0400','0078','0078')] # instantaneousDemand
        
        self.attrReports = []
        for n in nodeList:
            self.attrReports.append({'nodeId':n['node'],'epId':n['ep1'],'clustName':'Power Configuration Cluster','attrs':self.pwrConfigAttrs})
            self.attrReports.append({'nodeId':n['node'],'epId':n['ep1'],'clustName':'Device Temperature Configuration Cluster','attrs':self.deviceTempConfigAttrs})
            self.attrReports.append({'nodeId':n['node'],'epId':n['ep1'],'clustName':'On/Off Cluster','attrs':self.onOffAttrs})
            self.attrReports.append({'nodeId':n['node'],'epId':n['ep1'],'clustName':'Metering Cluster','attrs':self.meterAttrs})
    
        return

attrClassDict = {"hiveAttrs":hiveAttrs(nodeList),
                 "plugAttrs":plugAttrs(nodeList)}

ATTRS = attrClassDict[ATTRS]

""" Helper methods """
def buildChangeRep(myClust,myAttr):
    """ Build the word for minimum reportable change.
        Digital Attrs -> None
        Analogue Attrs -> One zero per nibble e.g. 1byte = 00
        
    """
    _,_,attrType = zbc.getAttributeNameAndId(myClust, myAttr)
    AorD = zbc.dataTypes[attrType]['type']
    bits = zbc.dataTypes[attrType]['bits']
    if AorD == 'A':
        changeRep='0' * int(bits/4)
    elif AorD == 'D':
        changeRep= ''
    return changeRep
    
# Main Program Starts

if __name__ == "__main__":
    
    # Only import this if we are the main module (to prevent circular reference)
    import FF_threadedSerial as AT
    myWantedAttrs = ATTRS

    print("**** Logging Configuration")
    print("")
    print("LoggingOn = {}".format(loggingOn))
    print("Port      = {}".format(PORT))
    print("Baud      = {}".format(BAUD))
    print("Firmware  = {}".format(firmwareRootFilePath))
    print("")

    # Print the nodes/endpoints/clusters/attributes and reporting configuration
    # Build a list of dicts containing the details for each attribute report config
    configList = []
    for node in ATTRS.attrReports:
        myNode = node['nodeId']
        myEp = node['epId']
        myClust=node['clustName']
        
        print("NodeId={0}, EP={1}, Clust={2}".format(myNode,myEp,myClust))

        attrs = node['attrs']
        # Print the clusters/attributes
        for attr in attrs:
            attrId = attr[0]
            minRep = attr[1]
            maxRep = attr[2]            
            changeRep = buildChangeRep(myClust, attrId)
            _,attrName,_ = zbc.getAttributeNameAndId(myClust,attrId)
            print('    {},{:35},{},{},{}'.format(attrId,attrName,minRep,maxRep,changeRep))
            
            #nodeId, epId, clustId, attr, minRep, maxRep, changeRep
            clustId,_ = zbc.getClusterNameAndId(myClust)
            configList.append({'nodeId':myNode,
                               'epId':myEp,
                               'clustId':clustId,
                               'attrId':attrId,
                               'minRep':minRep,
                               'maxRep':maxRep,
                               'changeRep':changeRep})
        
        print("")
    
    # Setup bindings and attribute reporting
    i = input("Do you want to setup bindings and attribute reporting on these attributes? y/n ")
    if i.upper()=='Y':
        
        AT.startSerialThreads(PORT, BAUD, printStatus=False, rxQ=True, listenerQ=False)
        AT.debug=True
        #AT.getInitialData(node1,ep1,fastPoll=True, printStatus=True)
 
        print('Starting binding/reporting setup:')
        
        # Set required bindings
        for node in ATTRS.attrReports:
            nodeId = node['nodeId']
            epId = node['epId']
            clustId,_ = zbc.getClusterNameAndId(node['clustName'])
            print('Setting binding on {0},{1},{2}'.format(nodeId,epId,clustId))
            
            # Setup a binding
            _, _, mySrcAddr = AT.getEUI(nodeId, nodeId)
            _, _, myDstAddr = AT.getEUI('0000', '0000')
            respState, _, respValue = AT.setBinding(nodeId, mySrcAddr, epId, clustId, myDstAddr, '01')
            if respState==False:
                print('Binding failed: ',respState,respValue)

        # Set attribute reporting on each attribute
        for attr in configList:
            respState,_,respValue = AT.setAttributeReporting(attr['nodeId'],
                                                             attr['epId'],
                                                             attr['clustId'],
                                                             attr['attrId'],
                                                             attr['minRep'],
                                                             attr['maxRep'],
                                                             attr['changeRep'])
            if respState==False:
                print('Setting attribute reporting failed: ',respState,respValue)
                
    print('All Done') 
