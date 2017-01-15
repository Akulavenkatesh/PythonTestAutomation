''''''
# Created on 5 Jul 2016

# @author: ranganathan.veluswamy
'''

if __name__ == '__main__':
    #intCreditCardNum = 9795526789839145
    
    
    
    
    #Retrieving the input for No Of Credit card to validate
    intNoOfCrdtCrdNum = int(input())
    
    #Validating the input constaints
    if not (intNoOfCrdtCrdNum >= 1 and intNoOfCrdtCrdNum <= 100):
        print("Please enter No of Credit card between 1 and 100.")
        exit()
    
    #Retrieving the input for credit card numbers
    oCrdtCrdNumLst = []
    for intInputCntr in range(intNoOfCrdtCrdNum):
        oCrdtCrdNumLst.append(int(input()))
    
    #Iterating the input credit cards and validating the Check Sum
    for intCreditCardNum in oCrdtCrdNumLst:
        #Reversing the Credit Card Number
        strRevCrdtCrdNum = str(intCreditCardNum)[::-1]
        
        intCntr = 1
        intOddTotal = 0
        intEvenTotal = 0
        for strDigt in strRevCrdtCrdNum:
            intDigit = int(strDigt)
            #Pick Odd digits and sum them
            if intCntr % 2 == 1:
                intOddTotal = intOddTotal + intDigit
            else: 
                #Pick Even digits and Multiply by 2 and add the digits if >1 and sum all the numbers
                intDigit = intDigit * 2
                if len(str(intDigit))>1: intDigit = sum(map(int,str(intDigit)))
                intEvenTotal = intEvenTotal + intDigit
            intCntr = intCntr + 1
        
        #Sum Even digits and Odd digits
        intTotal = intOddTotal + intEvenTotal
        
        #Validate if the total is a multiple of 10
        if intTotal % 10 == 0: print("Yes")
        else: print("No")'''