'''
Created on 21 Sep 2015

@author: ranganathan.veluswamy
'''
import time

import FF_loggingConfig as config
import FF_threadedSerial as AT
import FF_zigbeeClusters as zc


def main():
    myNodeId = '885E'
    AT.stopThread.clear()  
    AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False)
    AT.startAttributeListener(printStatus=False)
    AT.getInitialData(myNodeId, fastPoll=True, printStatus=True)
    
    # Setup a binding
    _, _, mySrcAddr = AT.getEUI(myNodeId, myNodeId)
    _, _, myDstAddr = AT.getEUI('0000', '0000')
    #respState, _, respValue = AT.setBinding(myNodeId, mySrcAddr, '05', '0000', myDstAddr, '01')
    respState, _, respValue = AT.setUnBind(myNodeId, mySrcAddr, '05', '0000', myDstAddr, '01')
    print(respState, respValue)
    time.sleep(5)
    print(AT.getBindings(myNodeId))
    
    AT.stopThreads()
    
    
    
if __name__ == '__main__':
    main()
    