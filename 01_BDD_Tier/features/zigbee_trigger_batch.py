'''
Created on 27 Oct 2015

@author: ranganathan.veluswamy
'''

import json
import os
import subprocess
import threading
import time
from tkinter import *
from tkinter import font
from tkinter import ttk, Text
from tkinter.messagebox import showinfo


class UIClass(Frame):
    
    
    def __init__(self, parent):
        self.oKitCombinBasedOnSel = [('All')]
        self.window = parent
        parent.title("Hive Test Automation - Zigbee Batch Execution")
        parent.configure(background='#F4FFFF')
        self.position_window(parent,w=600, h=500)
        
        Frame.__init__(self, parent)
        
        self.strIconFilePath = os.path.abspath(__file__ + "/../../../") + "/02_Manager_Tier/EnviromentFile/Icons/"  
        
        #High Frame
        self.Highsupermainframe =ttk.Frame(self, padding="0 0 0 0")
        # self.mainframe.configure(style='TFrame')
        self.Highsupermainframe.grid(column=0, row=0)
        self.Highsupermainframe.columnconfigure(0, weight=1)
        self.Highsupermainframe.rowconfigure(0, weight=1)
        #Tittle Frame
        self.titleFrame = ttk.Frame(self.Highsupermainframe, padding="180 10 180 10")
        self.titleFrame.configure(style='TFrame')
        self.titleFrame.grid(column=0, row=0, sticky=(N))
        self.titleFrame.columnconfigure(0, weight=1)
        self.titleFrame.rowconfigure(0, weight=1)#Frame1
        self.titleFrame1 = ttk.Frame(self, padding="0 10 180 10")
        self.titleFrame1.configure(style='TFrame')
        self.titleFrame1.grid(column=1, row=0, sticky=(N, W))
        self.titleFrame1.columnconfigure(0, weight=1)
        self.titleFrame1.rowconfigure(0, weight=1)
        #Super main Frame
        self.supermainframe =ttk.Frame(self.Highsupermainframe, padding="0 0 0 0")
        # self.mainframe.configure(style='TFrame')
        self.supermainframe.grid(column=0, row=1, sticky=(N))
        self.supermainframe.columnconfigure(0, weight=1)
        self.supermainframe.rowconfigure(0, weight=1)
        
        #Lst box Frame
        self.KitComboFrame = ttk.Frame(self.supermainframe, padding="47 0 10 5")
        self.KitComboFrame.configure(style='TFrame')
        self.KitComboFrame.grid(column=0, row=1, sticky=(W, N))
        self.KitComboFrame.columnconfigure(0, weight=1)
        self.KitComboFrame.rowconfigure(0, weight=1)
        
        #Button Frame
        self.ButtonFrame = ttk.Frame(self.supermainframe, padding="10 50 59 28")
        self.ButtonFrame.configure(style='TFrame')
        self.ButtonFrame.grid(column=1, row=1)
        self.ButtonFrame.columnconfigure(0, weight=1)
        self.ButtonFrame.rowconfigure(0, weight=1)
        
        #Bottom Frame
        self.BottomFrame =ttk.Frame(self.Highsupermainframe, padding="0 0 0 100")
        # self.BottomFrame.configure(style='TFrame')
        self.BottomFrame.grid(column=0, row=3, sticky=(N))
        self.BottomFrame.columnconfigure(0, weight=1)
        self.BottomFrame.rowconfigure(0, weight=1)
        
        #Lst box Frame
        self.SelectedKitComboFrame = ttk.Frame(self.BottomFrame, padding="47 0 10 5")
        self.SelectedKitComboFrame.configure(style='TFrame')
        self.SelectedKitComboFrame.grid(column=0, row=1, sticky=(W, N))
        self.SelectedKitComboFrame.columnconfigure(0, weight=1)
        self.SelectedKitComboFrame.rowconfigure(0, weight=1)
        
        #Button Frame
        self.ExecuteButtonFrame = ttk.Frame(self.BottomFrame, padding="10 50 59 58")
        self.ExecuteButtonFrame.configure(style='TFrame')
        self.ExecuteButtonFrame.grid(column=1, row=1)
        self.ExecuteButtonFrame.columnconfigure(0, weight=1)
        self.ExecuteButtonFrame.rowconfigure(0, weight=1)
        
        
        self.KitJson = StringVar()
        
        
        #Main Heading
        self.appHighlightFont = font.Font(family='Helvetica', size=22, weight='bold')
        self.subHeadFont = font.Font(family='Helvetica', size=12, weight='bold')
        ttk.Label(self.titleFrame, text='Zigbee Batch Execution', font=self.appHighlightFont).grid(column=3, row=0)
        #ttk.Label(self.titleFrame1, text='Batch Execution', font=self.appHighlightFont).grid(column=3, row=0)
        
        #Kit Combination List box
        ttk.Label(self.KitComboFrame, text='Kit Combination', font=self.subHeadFont).grid(row=1,column=1)
        self.oKitCombo = Listbox(self.KitComboFrame, 
                                 exportselection = False, height=10)        
        self.oKitCombo.grid(column=1, row=2, sticky=(N,W))
        self.oKitCombo.bind('<<ListboxSelect>>', self.load_kit_json)        
        ttk.Label(self.KitComboFrame, text=' ').grid(column=2, row=1, sticky=E)
        
        #Respose and Load Scroll bars
        xscrollbar = Scrollbar(self.KitComboFrame, orient=HORIZONTAL)
        xscrollbar.grid(row=2, column=17, sticky=E+W)        
        yscrollbar = Scrollbar(self.KitComboFrame)
        yscrollbar.grid(row=2, column=17, sticky=N+S)
        self.oKitJson = Text(self.KitComboFrame, width = 22, height =11, wrap=NONE, bd=0,
                    xscrollcommand=xscrollbar.set,
                    yscrollcommand=yscrollbar.set)
        #self.oKitJson.state(['readonly'])
        self.oKitJson.pack()
        self.oKitJson.grid(column=17, row=2, sticky=W)
        xscrollbar.config(command=self.oKitJson.xview)
        yscrollbar.config(command=self.oKitJson.yview)

        #OPTION Buttons        
        self.spaceLabelFont = font.Font(family='Helvetica', size=1, weight='bold')
        self.oSelectKitIMG= PhotoImage(file=self.strIconFilePath + 'rename.gif') 
        self.oRenameIMG1= PhotoImage(file=self.strIconFilePath + 'rename.gif') 
        self.oSaveAsIMG1 = PhotoImage(file=self.strIconFilePath + 'save_as.gif') 
        self.oRemoveIMG1 = PhotoImage(file=self.strIconFilePath + 'delete.gif') 
        
        ttk.Label(self.ButtonFrame, font=self.spaceLabelFont, text='').grid(column=1, row=0, sticky=E)  
        self.oSelectKit = ttk.Button(self.ButtonFrame, command=self.add_selected_kit_to_list, text = 'Select Kit')
        self.oSelectKit.grid(column=1, row=0)
        
        ttk.Label(self.ButtonFrame, font=self.spaceLabelFont, text=' ').grid(column=1, row=1, sticky=E)    
        self.oBatchSaveAs = Button(self.ButtonFrame, image=self.oSaveAsIMG1, command=self.load_kit_json)
        self.oBatchSaveAs.grid(column=1, row=2)  
        
        ttk.Label(self.ButtonFrame, font=self.spaceLabelFont, text=' ').grid(column=1, row=5, sticky=E)
        self.oBatchRemoveKit = Button(self.ButtonFrame, image=self.oRemoveIMG1, command=self.load_kit_json)
        self.oBatchRemoveKit.grid(column=1, row=6) 
        
        
        #Selected Kit Combination List box
        ttk.Label(self.SelectedKitComboFrame, text='SelectedKit Combination', font=self.subHeadFont).grid(row=1,column=1)
        self.oSelectedKitCombo = Listbox(self.SelectedKitComboFrame, selectmode='multiple', 
                                 exportselection = False, height=10)        
        self.oSelectedKitCombo.grid(column=1, row=2, sticky=(N,W))
        self.oSelectedKitCombo.bind('<<ListboxSelect>>', self.load_kit_json)        
        ttk.Label(self.SelectedKitComboFrame, text=' ').grid(column=2, row=1, sticky=E)
        
        
        #Execute Buttons        
        self.oRenameIMG1= PhotoImage(file=self.strIconFilePath + 'rename.gif') 
        self.oSaveAsIMG1 = PhotoImage(file=self.strIconFilePath + 'save_as.gif') 
        self.oRemoveIMG1 = PhotoImage(file=self.strIconFilePath + 'delete.gif') 
        ttk.Label(self.ExecuteButtonFrame, font=self.spaceLabelFont, text=' ').grid(column=1, row=0, sticky=E)  
        self.oExecuteSelectedKit = ttk.Button(self.ExecuteButtonFrame, command=self.execute_selected_kits, text = 'Execute')
        self.oExecuteSelectedKit.grid(column=1, row=0)
        ttk.Label(self.ExecuteButtonFrame, font=self.spaceLabelFont, text=' ').grid(column=1, row=1, sticky=E)    
        self.oBatchSaveAs = Button(self.ExecuteButtonFrame, image=self.oSaveAsIMG1, command=self.load_kit_json)
        self.oBatchSaveAs.grid(column=1, row=2)  
        ttk.Label(self.ExecuteButtonFrame, font=self.spaceLabelFont, text=' ').grid(column=1, row=5, sticky=E)
        self.oBatchRemoveKit = Button(self.ExecuteButtonFrame, image=self.oRemoveIMG1, command=self.load_kit_json)
        self.oBatchRemoveKit.grid(column=1, row=6) 
        
        print("Getting the Kit details from Remote Pi's")
        #self.get_kit_details_from_remote_pi()
        #self.update_kit_list()
        
        
    #Load Json when the kit combo is selected in the listbox
    def load_kit_json(self, event):
        intIndex = 1.0
        self.oKitJson.delete(1.0, END) 
        oRpiJson = self.get_rpi_kit_details_Json()
        current_Kit_id = self.oKitCombo.curselection()
        if len(current_Kit_id)>0:
            current_Kit_id = self.oKitCombo.get(current_Kit_id[0])
            strPiID = current_Kit_id.split("=>")[0]
            for oPort in oRpiJson[strPiID]:
                self.oKitJson.insert(intIndex, json.dumps(oRpiJson[strPiID][oPort], indent=1, sort_keys=False))                 
                intIndex = intIndex + 1.0
    
    #Load selected  Kit to the Selected Kit List box  
    def add_selected_kit_to_list(self):
        current_Kit_id = self.oKitCombo.curselection()
        if len(current_Kit_id)>0:
            current_Kit_id = self.oKitCombo.get(current_Kit_id[0])
            if  not current_Kit_id in self.oSelectedKitCombo.get(0, END):
                self.oSelectedKitCombo.insert(END, current_Kit_id)  
    
    #Execute the the selected list of kits
    def execute_selected_kits(self):
        jobs = []
        oRpiJson = self.get_rpi_kit_details_Json()
        for oKit in self.oSelectedKitCombo.get(0, END):
            strPiID = oKit.split("=>")[0]
            strPort = list(oRpiJson[strPiID].keys())[0]
            strTestSuite = oRpiJson[strPiID][strPort]['Test_Suite']
            parallelExecThread = threading.Thread(target=self.trigger_test_execution_on_rpi, args=(strPiID, strTestSuite,))
            parallelExecThread.daemon = True # This kills the thread when main program exits
            parallelExecThread.start()
            parallelExecThread.name = strPiID
            jobs.append(parallelExecThread)
            time.sleep(10)
        for oJob in jobs:
            oJob.join()
            
    #Thread function to trigger the automated tests on the Rasberry Pi's
    def trigger_test_execution_on_rpi(self, strPiID, strTestSuite):
        if strTestSuite == 'BasicSmokeTest_Dual':
            strBehaveCommand = "behave --tags=BasicSmokeTest"
        elif strTestSuite == 'BasicSmokeTest_Heating':            
            strBehaveCommand = "behave --tags=BasicSmokeTest --tags=Heating"        
        elif strTestSuite == 'BasicSmokeTest_HotWater':            
            strBehaveCommand = "behave --tags=BasicSmokeTest --tags=HotWater"
        elif strTestSuite == 'ScheduleTest_Dual':
            strBehaveCommand = "behave --tags=ScheduleTest --tags=Verify"
        elif strTestSuite == 'ScheduleTest_Heating':
            strBehaveCommand = "behave --tags=ScheduleTest --tags=Verify --tags=Heating"
        elif strTestSuite == 'ScheduleTest_HotWater':
            strBehaveCommand = "behave --tags=ScheduleTest --tags=Verify --tags=HotWater"
        else: return
        oKitDetails = self.getShellCommandOutput("ssh " + strPiID + " \"source env/bin/activate; cd workspace/HiveTestAutomation/01_BDD_Tier/features; " + strBehaveCommand+"\"", strPiID, True)
        
 
    #Place Window on the center fo the screen
    def position_window(self, parent, w, h):
        # get screen width and height
        ws = parent.winfo_screenwidth()
        hs = parent.winfo_screenheight()
        # calculate position x, y
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    
    def update_kit_list(self):
        intIndex = 0
        self.oKitCombo.delete(0, END) 
        oKitDetailsDict = self.get_rpi_kit_details_Json()
        for strPi in oKitDetailsDict:
            for strPort in oKitDetailsDict[strPi]:
                strKitCombo = strPi + "=>" + oKitDetailsDict[strPi][strPort]['BM']['Name'] + "<>" + oKitDetailsDict[strPi][strPort]['TH']['Name']
              
                self.oKitCombo.insert(intIndex, strKitCombo)  
                intIndex = intIndex + 1
    
    
    def get_kit_details_from_remote_pi(self):
        oPiList = ["rpi2", "rpi3", "rpi4", "rpi5", "rpi6", "rpi7", "rpi8", "rpi9"]
        oKitDetailsDict = {}
        for strPiID in oPiList:
            print("Getting kit details from :", strPiID)
            oKitDetails = self.getShellCommandOutput("ssh " + strPiID + " \"source env/bin/activate; python workspace/HiveTestAutomation/01_BDD_Tier/features/get_TG_devices_details.py\"", strPiID)
            
            for oKitDetail in oKitDetails: 
                oKitDetail = oKitDetail.replace("b'", "").replace("\\n'", "")
                if 'TTY' in oKitDetail.upper() and 'USB' in oKitDetail.upper():
                    oDict = json.loads(oKitDetail[oKitDetail.find("{"):oKitDetail.rfind("}")+1].replace("'", "\""))
                    for strPort in oDict:
                        if oDict[strPort]['BM']['Name'] == 'SLR1':
                            oDict[strPort]['Test_Suite'] = "BasicSmokeTest_Heating"
                        else: oDict[strPort]['Test_Suite'] = "BasicSmokeTest_Dual"
                    oKitDetailsDict[strPiID] = oDict
                    print(strPiID, oDict)
        '''
        oKitDetailsDict =   {
                                    "rpi3": {
                                        "ttyUSB0": {
                                            "TH": {
                                                "Name": "SLT2",
                                                "Version": "05135300"
                                            },
                                            "BM": {
                                                "Name": "SLR2",
                                                "Version": "07144640"
                                            }
                                        }
                                    }
                                }      
        '''
        print(json.dumps(oKitDetailsDict, indent=4, sort_keys=False))
        
        self.put_rpi_kit_details_Json(oKitDetailsDict)
    
    def get_rpi_kit_details_Json(self):
        strEnvironmentFolderPAth = os.path.abspath(__file__ + "/../../../") + "/02_Manager_Tier/EnviromentFile/"        
        strNodeClustAttrPath = strEnvironmentFolderPAth + '/rpi_kit_details.json'    
        strJson = open(strNodeClustAttrPath, mode='r')
        oKitDetailsDict = json.loads(strJson.read())
        strJson.close() 
        return oKitDetailsDict

    #Update the Kit details json
    def put_rpi_kit_details_Json(self, oKitDetailsDict):
        strEnvironmentFolderPAth = os.path.abspath(__file__ + "/../../../") + "/02_Manager_Tier/EnviromentFile/"        
        strNodeClustAttrPath = os.path.abspath(strEnvironmentFolderPAth + '/rpi_kit_details.json')
        #Write back the JSON to the GlobalVar.JSON
        oJson = open(strNodeClustAttrPath, mode='w+')
        oJson.write(json.dumps(oKitDetailsDict, indent=4, sort_keys=False))
        oJson.close()
    
    #Get Shell command output
    def getShellCommandOutput(self, strCmd, strRpiID, boolPrintOutput = False):    
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
    
root = Tk()
UIClass(root).pack()
root.mainloop()