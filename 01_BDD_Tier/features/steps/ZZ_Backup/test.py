''''''
# Created on 19 Apr 2016

# @author: ranganathan.veluswamy
'''
def testtt():
    strInput = "this is a string"
    
    lstInput = strInput.split(" ")
    
    strOutput = "-".join(lstInput)
    
    print(strOutput)
    
        
    import itertools
    
    strInput = "BANANA"
    
    lstVoWels = "AEIOU"
    
    intStuatPoint = 0
    intKevinPoint = 0
    lstInput = []
    lstoutput = []
    for cAlph in strInput:
        lstInput.append(cAlph)
    
    for intComb in range(1, len(strInput)+1):
        oComblist = []
        oComblist = list(itertools.permutations(lstInput,intComb))
        
        for oComb in oComblist:
            print(oComb)
            if  not oComb in  lstoutput: 
                lstoutput.append(oComb)
    
    print(len(lstoutput))
    print(lstoutput)
    for oWord in lstoutput:
        strSub =""
        for oChar in oWord:
            if not oChar == "":
                strSub = strSub + oChar
        strSub = strSub[::-1]
        if strSub in strInput: 
            intPoint = strInput.find(strSub)
            #if intPoint == 0: intPoint =1
            print(intPoint,strSub)
            strFirstLetter = strSub[:1]
            if strFirstLetter in  lstVoWels:
                intKevinPoint = intKevinPoint + intPoint
            else: 
                intStuatPoint = intStuatPoint + intPoint
            
    if intStuatPoint>intKevinPoint:
        print("Stuart", intStuatPoint)
    else: print("Kevin", intKevinPoint)
        
def get_all_substrings(string):
    length = len(string)+1
    return [string[x:y] for x in range(length) for y in range(length) if string[x:y]]


def olpcount(string,pattern,casesensitive=True):
    if casesensitive != True:
        string  = string.lower()
        pattern = string.lower()
    l = len(pattern)
    ct = 0
    for c in range(0,len(string)):
        if string[c:c+l] == pattern:
            ct += 1
    return ct

def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output

    
if __name__ == '__main__':
    strInput = "BANANA"
    
    lstVoWels = "AEIOU"
    
    intStuatPoint = 0
    intKevinPoint = 0
    lstInput = []
    lstoutput = []
    
    lstSubStrings =get_all_substrings(strInput)
    lstSubStrings = remove_duplicates(lstSubStrings)
    for strSub in lstSubStrings:
        if strSub in strInput: 
            #intPoint = strInput.count(strSub, 0,len(strInput)+1)
            intPoint = olpcount(strInput,strSub)
            #intPoint = strInput.find(strSub)
            if intPoint == 0: intPoint =1
            print(intPoint,strSub)
            strFirstLetter = strSub[:1]
            if strFirstLetter in  lstVoWels:
                intKevinPoint = intKevinPoint + intPoint
            else: 
                intStuatPoint = intStuatPoint + intPoint
            
    if intStuatPoint>intKevinPoint:
        print("Stuart", intStuatPoint)
    else: print("Kevin", intKevinPoint)'''