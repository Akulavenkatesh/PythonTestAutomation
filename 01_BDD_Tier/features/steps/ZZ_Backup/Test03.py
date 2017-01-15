'''
Created on 5 Jul 2016

@author: ranganathan.veluswamy
'''
'''from sympy.physics.quantum.tests.test_sho1d import kf

if __name__ == '__main__':
    strInputData = "lk;asdlfkjlskdfj;alskj sldfkj;slkjfdcsdfjslkdjflskjfal;skjdfl;k<script = sdfdsdf>1234455</script>asdfasfdafsafs &&&&&& <script = sdfdsdf>1234455</script>XXXXXXX"
    
    print(strInputData)

    
    strOutputData = ""
    strStartSearch = "<script"
    strEndSearch = "</script>"
    if strStartSearch in strInputData:
        while True:
            if strStartSearch in strInputData:
                strOutputData = strOutputData + strInputData.split(strStartSearch)[0]
                strInputData = strInputData[strInputData.find(strStartSearch)+len(strStartSearch):]
                
            if strEndSearch in strInputData:
                strInputData = strInputData[strInputData.find(strEndSearch)+len(strEndSearch):]
            else: 
                strOutputData = strOutputData + strInputData
                break
            
    else: strOutputData = strInputData
    
    print(strOutputData)
        
    strInputData = ""
    
try:
    while True:
        strInput = input()
        if strInput == "": break
        strInputData = strInputData + strInput
except: pass
    '''