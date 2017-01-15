'''
Created on 9 Nov 2015

@author: ranganathan.veluswamy
'''
import json
import subprocess


def get_kit_details_from_remote_pi():
    oPiList = ["rpi2", "rpi3", "rpi4", "rpi5", "rpi6", "rpi7", "rpi8", "rpi9"]
    oPiList = ["rpi2", "rpi3", "rpi4", "rpi5", "rpi6", "rpi7", "rpi8", "rpi9"]
    for strPiID in oPiList:
        print("git pull on :", strPiID)
        getShellCommandOutput("ssh " + strPiID + " \"cd workspace/HiveTestAutomation;git config --global user.email 'rangawillb4u@gmail.com';git config --global user.name 'rangawillb4u';git stash; git pull 'https://rangawillb4u:ranga123@github.com/ConnectedHomes/HiveTestAutomation.git' master; git stash pop\"", strPiID)
        
                
#Get Shell command output
def getShellCommandOutput(strCmd, strRpiID, boolPrintOutput = False):    
    oProcess = subprocess.Popen(strCmd, stdout=subprocess.PIPE, shell=True)
    outputList = []
    while True:
        output = oProcess.stdout.readline()
        if oProcess.poll() is not None:
            break
        if output:
            if boolPrintOutput: print(strRpiID, output)
            outputList.append(str(output))
        else:
            break
        return outputList

if __name__ == '__main__':
    get_kit_details_from_remote_pi()                                                                                                                                                                                      