'''
Created on Nov 7, 2014

@author: Keith
'''
import math
import binascii
import time
import os
import glob
from getopt import getopt
import sys
import FF_loggingConfig as config
import FF_threadedSerial as AT

AT.debug = False
deviceVersionDict ={
                                'SLT3': {'2.1' : '02100203',
                                            '2.10' : '02100203',
                                            '2.13' : '02130204'}
                                }

deviceTypes = [{'type':'SLR1','ep':'05','path':'SLR1_SLR2'},
               {'type':'SLR2','ep':'05','path':'SLR1_SLR2'},
               {'type':'SLT2','ep':'09','path':'SLT2'},
               {'type':'SLT3','ep':'09','path':'SLT3'},
               {'type':'SLB1','ep':'09','path':'SLB1'},
               {'type':'SLP2','ep':'09','path':'SLP2'},
               {'type':'CL01','ep':'01','path':'CL01'}]

otaHeader = [('upgradeFileIdentifier',4),
             ('headerVersion',2),
             ('headerLength',2),
             ('headerFieldControl',2),
             ('manufacturerCode',2),
             ('imageType',2),
             ('fileVersion',4),
             ('zigbeeStackVersion',2),
             ('headerString',32),
             ('totalImageSize',4),
             ('securityCredentialVersion',1),
             ('upgradeFileDestination',8), 
             ('minHardwareVersion',2),
             ('maxHardwareVersion',2)]

HEADER_LENGTH_POSITION = 6

"""  Block Size 0x32 i.e. 50 Bytes
Needs to be small enough to prevent buffer overflow during multi-hop upgrades
Typical header = 64Bytes + 50 Payload = 114 Bytes total
Multi-hop header is 2 bytes larger (66 Bytes)
CT default for newer devices block size of 63 bytes
So for multi-hop header of 66 + 63 Payload = 129 Bytes (1 more than buffer length)
"""
blockSize = "32"
                 
class myOtaHeader(object):
    """ header data object
    """
    def __init__(self):
        self.upgradeFileIdentifier = ''
        self.headerVersion = ''
        self.headerLength = 0
        self.headerFieldControl = ''
        self.manufacturerCode = ''
        self.imageType = ''
        self.fileVersion = ''
        self.zigbeeStackVersion = ''
        self.headerString = ''
        self.totalImageSize = 0

def selectDeviceAndFirmware():
    """ Get the user to enter nodeId, select the device type and select the
        firmware file.
    
    """
    nodeId = input("Enter your NodeId = ")
    nodeId = nodeId.upper()
    
    # Work out the device type by reading the attribute from the basic cluster
    # AT.getAttribute(nodeId, myEP, myClust, myAttr, myType)
    
    print('\nSelect your device type:')
    for i in range(0, len(deviceTypes)):
        print(i,deviceTypes[i])
    
    dt = input('> ')
    ep = deviceTypes[int(dt)]['ep']
    #dType = deviceTypes[int(dt)]['type']
    dPath = deviceTypes[int(dt)]['path']
    
    pathname = config.firmwareRootFilePath + dPath + "_Firmware/*.ota"
    
    print('\nSelect your firmware image')
    fileList = glob.glob(pathname )
    for f in fileList:
        file = f.rpartition('/')[2]
        i = fileList.index(f)
        print("{0:>2}. {1}".format(i,file))
    i = input("> ")
    filename = fileList[int(i)]
    print(filename)
    
    return nodeId, ep, filename

def swapEndian(myVal):
    myTemp=''
    for i in range(len(myVal)-2,-2,-2):
        myTemp += myVal[i:i+2]
    return(myTemp)
def readFileByte(f, byteCount):
    myBytes = binascii.hexlify(f.read(byteCount)).decode('utf-8')
    return myBytes
def readHeader(myHeader,myFile):
    """ Read the header parameters from an OTA file and populate
        the header class instance.
        Print the header variables
    """
    lengthCount = 0
    
    myFile.seek(HEADER_LENGTH_POSITION)
    myHeader.headerLength = readFileByte(myFile,2)
    headerLengthInt = int(myHeader.headerLength,16)
    
    myFile.seek(0)
    
    for item in otaHeader:
        lengthCount += item[1]
        myVal = readFileByte(myFile, item[1])
        myVal = swapEndian(myVal)
        
        if item[0] == 'headerString':
            myVal = swapEndian(myVal)
            # Convert hex to binary then decode that as UTF-8
            
            #myVal = binascii.unhexlify(myVal).decode('utf-8')
            # Alternative to above line which may work in older python versions
            myVal = bytearray.fromhex(myVal).decode()
            
        setattr(myHeader,item[0],myVal)
        
        if lengthCount >= headerLengthInt: break
        
    # Print the header fields    
    for item in otaHeader:
        if hasattr(myHeader,item[0]):
            print('{0:25}= {1}'.format(item[0], getattr(myHeader, item[0])))
    
    print()
    print('Image Size (hex) = {0}'.format(myHeader.totalImageSize))
    
    return 0
def readArguments():
    """ Read command line parameters 
        Use them if provided.
    """
    helpString = "\n*** OTA Module\n\n" +\
                 "Use these command line options to select the node and firmware file:\n\n" +\
                 "-h Print this help\n" +\
                 "-n node        Node ID of target node\n" +\
                 "-e endpoint    Endpoint for target node\n" +\
                 "-f firmware    Path to firmware file\n" +\
                 "-p port        /dev/portId"

    myNodeId = ''
    myEp = ''
    myFullPath = ''
    myPort = ''

    opts = getopt(sys.argv[1:], "hn:e:f:p:")[0]
    
    for opt, arg in opts:
        #print(opt, arg)
        if opt == '-h':
            print(helpString)
            exit()
        if opt == '-n':
            myNodeId = arg.upper()
        if opt == '-e':
            myEp = arg
        if opt == '-f':
            myFullPath = arg
            if os.path.isfile(myFullPath):
                pass
            else:
                print('File not found: {}'.format(arg))
                exit()
        if opt == '-p':
            myPort = arg
    
    return myNodeId, myEp, myFullPath, myPort

def firmwareUpgrade(header, nodeId, ep, f):
    """  Execute the FW message exchanges
    
        Expected message exchanges are:
        
        Co-ordinator      Device
        
                      <<  IMGQuery (queryNextImage) - Device uses response to this to set it's FW server
        AT+IMGNOTIFY  >>  Tell the device that Co-ord is the FW server
        .
        .
        AT+IMGNOTIFY  >>  Tell the device that an Image is available for it.
                      <<  IMGQUERY- queryNextImage Request
        AT+QIMGRSP    >>  (queryNextImage Response)
                      <<  IMGBREQ = ImageBlock Request
        AT+IMGBRSP    >>  (ImageBlockRequest Response)
                      ..
                      <<  IMGBREQ = ImageBlock Request
        AT+IMGBRSP    >>  (ImageBlockRequest Response)
                      ..
                      <<  UPGRADEREQ = UpgradeEnd Request
        AT+UPGRADE    >>  UpgradeEnd Response (Upgrade with a time. Typically upgrade now)
        
        For the purposes of this script we ignore the initial queryNextImage exchange and simply send imageNotify
        continuously until we get either...
        a) a response to the imageNotify or,
        b) a scheduled QNI from the device.
        
        In either case we respond with a QNIR and then continue with the exchange. 
    
    """
    #AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False)
    # AT.initialiseSerialComms(config.PORT, config.BAUD) 
    
    # Send the image notify command.  Wait for queryNextImage
    print("Image Notify Start: {}".format(time.strftime("%H:%M:%S", time.gmtime())))
    sendMode = '0'                          # 0=Direct, 1=Group, 6=Broadcast (if using broadcast the nodeId must
                                            # be a broadcast address e.g. FFFC
              
    payloadType = '03'                      # 0x03 = jitter, manuf code, image type and new file version included
    queryJitter = '64'
    manufCode = header.manufacturerCode
    imageType = 'FFFF'                      # 0xFFFF = All image types
    fileVersion = 'FFFFFFFF'                # 0xFFFFFFFF = All file versions

    print('\nSending Image notify: {}'.format(time.strftime("%H:%M:%S", time.gmtime())))
    respState, respCode, respValue, seqNum = AT.imageNotify(nodeId,
                                                            ep,
                                                            sendMode,
                                                            payloadType,
                                                            queryJitter,
                                                            manufCode,
                                                            imageType,
                                                            fileVersion,
                                                            timeout=700)

    if respState==False:
        print("ERROR: queryNextImage has not been received")
        print(respValue)
        exit()
    
    print('Image notify response received: {}'.format(time.strftime("%H:%M:%S", time.gmtime())))

    # Send queryNextImageResponse.  Wait for first block request.
    status = '00'
    imageType = header.imageType
    fileVersion = header.fileVersion
    imageSize = header.totalImageSize
    print('\nSending queryNextImageResponse: {}'.format(time.strftime("%H:%M:%S", time.gmtime())))
    
    sendMode='0'    
    respState,respCode,respValue,seqNum,offset,_ = AT.queryNextImageResponse(nodeId,
                                                                        ep,
                                                                        sendMode,
                                                                        status,
                                                                        manufCode,
                                                                        imageType,
                                                                        fileVersion,
                                                                        imageSize,
                                                                        seqNum)

    # We ignore the returned blocksize as it is sometimes too large see notes at the top of this file.
    blockSize='32'
    
    if respState==False:
        print('\nERROR: imageBlockRequest not received.')
        print(respValue)
        exit()
    
    # First block request received. Start sending blocks
    print('\nFirst block request received: {}'.format(time.strftime("%H:%M:%S", time.gmtime())))
    imageSizeInt = int(header.totalImageSize,16)
    blockSizeInt = int(blockSize,16)
    
    numberOfBlocks = math.ceil(imageSizeInt/blockSizeInt)
    print('\nDownload started. Number of Blocks = ',numberOfBlocks)
    print(' 0%')

    #offset='00000000'    
    percentageDone = 0

    while True:
        
        # Shorten blocksize for final block
        chunkLeftInt = imageSizeInt - f.tell()
        if chunkLeftInt < blockSizeInt:
            blockSize = "%02X" % chunkLeftInt
        
        # Read the block from the file
        f.seek(int(offset,16))
        payload = readFileByte(f,blockSizeInt)

        blockNumber = round(1 + (int(offset,16)/blockSizeInt))
            
        percentageInstant = round(blockNumber/numberOfBlocks * 100)
        if percentageInstant >= (percentageDone + 10):
            percentageDone = percentageInstant
            print("{0}% {1}".format(percentageDone,time.strftime("%H:%M:%S", time.gmtime()))) 
      
        # Send the block
        respState, respCode, respValue, seqNum, offset, done = AT.imageBlockResponse(nodeId,
                                                                                     ep,
                                                                                     sendMode,
                                                                                     status,
                                                                                     manufCode,
                                                                                     imageType,
                                                                                     fileVersion,
                                                                                     offset,
                                                                                     blockSize,
                                                                                     payload,
                                                                                     seqNum)

        if done: break    
    
    return respState,respCode,respValue

""" Code starts here """
if __name__ == "__main__":
  
    # Check if any command line arguments provided
    args = readArguments()
    for arg in args:
        if arg=='':
            nodeId, ep, fullPath = selectDeviceAndFirmware()
            port = config.PORT
            break
    else:
        nodeId = args[0]
        ep = args[1]
        fullPath = args[2]
        port = args[3]
    
    print(nodeId,ep,fullPath,port)

    # Open the image file
    if os.path.isfile(fullPath):
        f = open(fullPath, "rb")
    else:
        print("File not found {}".format(fullPath))
        exit()

    print('FW File = {0}\r\n'.format(fullPath))

    # Read header from the file
    header = myOtaHeader()
    readHeader(header,f)
    
    firmwareUpgrade(header, nodeId,ep,f)
    
    f.close()
    print('All Done. {}'.format(time.strftime("%H:%M:%S", time.gmtime())))