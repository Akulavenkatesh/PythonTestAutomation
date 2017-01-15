'''
Created on 26 Oct 2015

@author: ranganathan.veluswamy
'''
import os
import time
import FF_utils as utils
import FF_threadedSerial as AT

def get_connected_TGS():
    oTGList = []
    for filenames in os.walk("/dev"):
        for file_list in filenames:
            for file_name in file_list:
                if 'TTY' in file_name.upper() and 'USB' in file_name.upper():
                    oTGList.append(file_name)
                    
    return oTGList
    
def getNodes():
    BMID = utils.discoverNodeIDbyCluster('0201')[2]
    time.sleep(2)
    '''SPID = utils.discoverNodeIDbyCluster('0006')[2]
    time.sleep(2)'''
    THID = ""
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
    '''if not boolTHfound:
        NTAble = utils.getNtable(SPID)[2]
        for oRow in NTAble:
            if 'RFD' in oRow:
                THID = oRow.split('|')[3].strip()
                boolTHfound = True'''
            
    return {'BM':BMID, 'TH':THID}


def get_device_name(oNode, oEP):
    """ Returns the Node ID of Related to the Cluster
    """'''
    myMsg = 'AT+READATR:{0},{1},{2},{3},{4}'.format(oNode, oEP, "0", "0000", "0005")
    print(myMsg)
    expectedResponse = ['RESPATTR:{0},{1},{2},{3}{4},(..)'.format(oNode, oEP, "0000", "0005", "00")]'''
    sendMode = '0'
    myClust = '0000'
    myAttr = '0005'
    myMsg = 'AT+READATR:{0},{1},{2},{3},{4}'.format(oNode,oEP,sendMode,myClust,myAttr)             
    
    expectedResponse=['RESPATTR:{0},{1},{2},{3},{4},(..)'.format(oNode,
                                                                      oEP,
                                                                      myClust,
                                                                      myAttr, '00')]
    # DEV:C58A,09
    
    respState, respCode, respValue = AT.sendCommand(myMsg, expectedResponse, maxAttempts=5)

    if respState:
        arrResp = respValue.split(',')
        resp = arrResp[len(arrResp)-1]
    else:
        resp = respValue    
    return respState,respCode,resp

def get_device_version(oNode, oEP):
    sendMode = '0'
    myClust = '0019'
    myAttr = '0002'
    myMsg = 'AT+READCATR:{0},{1},{2},{3},{4}'.format(oNode,oEP,sendMode,myClust,myAttr)             
    
    expectedResponse=['RESPATTR:{0},{1},{2},{3},{4},(..)'.format(oNode,
                                                                      oEP,
                                                                      myClust,
                                                                      myAttr, '00')]
    
    respState, respCode, respValue = AT.sendCommand(myMsg, expectedResponse, maxAttempts=5)

    if respState:
        arrResp = respValue.split(',')
        resp = arrResp[len(arrResp)-1]
    else:
        resp = respValue    
    return respState,respCode,resp

def main():
    oKitListDict = {}
    oTGList = get_connected_TGS()
    for oPort in oTGList:
        time.sleep(5)
        AT.stopThread.clear()  
        AT.startSerialThreads("/dev/" + oPort, "19200",  printStatus=False)
        oNodeDict = getNodes()
        #print(oNodeDict)
        AT.getInitialData(oNodeDict['BM'], fastPoll=True, printStatus=False)
        _, _, strBMName= get_device_name(oNodeDict['BM'], '05')
        _, _, strBMVersion= get_device_version(oNodeDict['BM'], '05')
        _, _, strTHName = get_device_name(oNodeDict['TH'], '09')
        _, _, strTHVersion = get_device_version(oNodeDict['TH'], '09')
        AT.stopThreads()
        oKitListDict[oPort] = {"BM":{"Name": strBMName, "Version": strBMVersion}, "TH": {"Name": strTHName, "Version": strTHVersion}}
    '''if not len(oTGList)==0:
        oBMDict = {"Name": strBMName, "Version": strBMVersion}
        oTHDict = {"Name": strTHName, "Version": strTHVersion}
        print('oBMDict', oBMDict)
        print('oTHDict', oTHDict)'''
    print(oKitListDict)
    
if __name__ == '__main__':
    main()