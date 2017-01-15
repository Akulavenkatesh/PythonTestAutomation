import datetime
import json
import ntpath
import os
import shutil
import subprocess
from sys import executable
import threading
import time
from tkinter import *
from tkinter import font
from tkinter import simpledialog
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import *
from tkinter.messagebox import showinfo
from tkinter.ttk import Style
import traceback
import webbrowser

import pymsgbox

import FF_alertmeApi as ALAPI
import FF_utils as utils


UDID = "8d25ba7d4a8f82f1a32cc35d907ad2a928b6e808"
DEVICE_NAME = "iPhone"

striOSAppiumConnectionString = "/Applications/Appium.app/Contents/Resources/node/bin/node \
                                                /Applications/Appium.app/Contents/Resources/node_modules/appium/bin/appium.js \
                                                --address 127.0.0.1 --command-timeout \"7200\" --debug-log-spacing \
                                                --no-reset \
                                                 --native-instruments-lib --log-level \"error\""



class UIClass(Frame):
    
        
    
    def __init__(self, parent):
        self.set_global_var()
        self.window = parent
        self.intCommonWidth = 1056
        parent.title("Hive Test Automation - Batch Execution Configuration")
        s = ttk.Style()
        bg = s.lookup('TFrame', 'background')
        parent.configure(background = bg)
        #parent.tk_setPalette(background='#40E0D0', foreground='black',
        #activeBackground='black')#, activeForeground=mycolor2)
        parent.configure(background='light blue')
        self.position_window(parent,w=self.intCommonWidth, h=560)
        Frame.__init__(self, parent, pady=3,padx=3)
        
        #Style - Background color
        ''' s = ttk.Style()
        s.configure('.', background='black')
        ttk.Style().configure("TButton", padding=6, relief="flat", bg='#000000',
                fg='#b7f731',background="pale green")
        '''
        s.map('TButton', 
        background=[('disabled','#d9d9d9'), ('active','#ececec')],
        foreground=[('disabled','#a3a3a3')],
        relief=[('!disabled', 'FLAT')])
        #Frame
        self.Highsupermainframe =ttk.Frame(self, padding="0 0 0 0")
        # self.mainframe.configure(style='TFrame')
        self.Highsupermainframe.grid(column=0, row=0)
        self.Highsupermainframe.columnconfigure(0, weight=1)
        self.Highsupermainframe.rowconfigure(0, weight=1)
        
        #Frame
        self.supermainframe =ttk.Frame(self.Highsupermainframe, padding="0 0 0 0")
        # self.mainframe.configure(style='TFrame')
        self.supermainframe.grid(column=0, row=0, sticky=(N))
        self.supermainframe.columnconfigure(0, weight=1)
        self.supermainframe.rowconfigure(0, weight=1)
        
        #Frame
        self.mainframe =ttk.Frame(self.supermainframe, padding="30 30 30 0")
        # self.mainframe.configure(style='TFrame')
        self.mainframe.grid(column=4, row=0, sticky=(N, W, E))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        
        #Frame3
        self.batchlistbuttonFrame = ttk.Frame(self.supermainframe, padding="30 80 10 20")
        self.batchlistbuttonFrame.configure(style='TFrame')
        self.batchlistbuttonFrame.grid(column=1, row=0, sticky=(N, W, E))
        self.batchlistbuttonFrame.columnconfigure(0, weight=1)
        self.batchlistbuttonFrame.rowconfigure(0, weight=1)
        
        #Frame2
        self.kitFrame = ttk.Frame(self.supermainframe, relief=FLAT, padding="0 50 10 25")
        self.kitFrame.configure(style='TFrame')
        self.kitFrame.grid(column=2, row=0, sticky=(N, W, E))
        self.kitFrame.columnconfigure(0, weight=1)
        self.kitFrame.rowconfigure(0, weight=1)
        
        #Frame3
        self.listbuttonFrame = ttk.Frame(self.supermainframe, padding="0 80 30 20")
        self.listbuttonFrame.configure(style='TFrame')
        self.listbuttonFrame.grid(column=3, row=0, sticky=(N, W, E))
        self.listbuttonFrame.columnconfigure(0, weight=1)
        self.listbuttonFrame.rowconfigure(0, weight=1)
        
        #Frame3
        self.mainbuttonFrame = ttk.Frame(self.Highsupermainframe, padding="70 0 0 0")
        self.mainbuttonFrame.configure(style='TFrame')
        self.mainbuttonFrame.grid(column=0, row=1, sticky=(N, W))
        self.mainbuttonFrame.columnconfigure(0, weight=1)
        self.mainbuttonFrame.rowconfigure(0, weight=1)
        
        #Frame3
        self.executebuttonFrame = ttk.Frame(self.Highsupermainframe, padding="0 10 0 30")
        self.executebuttonFrame.configure(style='TFrame')
        self.executebuttonFrame.grid(column=0, row=2, sticky=(N))
        self.executebuttonFrame.columnconfigure(0, weight=1)
        self.executebuttonFrame.rowconfigure(0, weight=1)
        
        
        #Variables
        self.Environment = StringVar()
        self.APIValidation = StringVar()
        self.MainClient = StringVar()
        self.UserName = StringVar()
        self.Password = StringVar()
        self.TestSuite = StringVar()
        self.AppVersion = StringVar()
        self.ATNode = StringVar()
        self.OSVersion = StringVar()
        self.AppFilePath = StringVar()
        self.DeviceName = StringVar()
        self.UDID = StringVar()
        self.BrowserName = StringVar()
        self.URL = StringVar()
        
        self.boolAppFieldDestroyed = True
        self.boolUDIDFieldDestroyed = True
        self.boolZigbeeFieldDestroyed = True
        self.boolUserPassDestroyed = True
        self.boolWebFieldDestroyed = True
        
        self.strIconFilePath = os.path.abspath(__file__ + "/../../../") + "/02_Manager_Tier/EnviromentFile/Icons/"  
        self.appHighlightFont = font.Font(family='Helvetica', size=22, weight='bold')
        ttk.Label(self.mainframe, text='Hive Device /', font=self.appHighlightFont).grid(column=3, row=0, sticky=E)
        ttk.Label(self.mainframe, text='Client Test Automation', font=self.appHighlightFont).grid(column=15, row=0, sticky=W)
        
        #Environment
        ttk.Label(self.mainframe, text='Environment:    ').grid(column=3, row=1, sticky=E)
        self.oEnvironment = ttk.Combobox(self.mainframe, textvariable=self.Environment)
        self.oEnvironment['values'] = ('isopInternProd', 'isopBeta', 'isopStaging', 'isopProd')
        self.oEnvironment.bind('<<ComboboxSelected>>', self.api_selected_item_event)
        self.oEnvironment.state(['readonly'])
        self.oEnvironment.set(utils.getAttribute('common', 'currentEnvironment'))
        self.oEnvironment.grid(column=15, row=1, sticky=W)
        
        #API Validation
        ttk.Label(self.mainframe, text='API Validation:    ').grid(column=3, row=2, sticky=E)
        self.oAPIValidation = ttk.Combobox(self.mainframe, textvariable=self.APIValidation)
        self.oAPIValidation['values'] = ('Platform API', 'Zigbee API')
        self.oAPIValidation.bind('<<ComboboxSelected>>', self.api_selected_item_event)
        self.oAPIValidation.state(['readonly'])
        self.oAPIValidation.set(utils.getAttribute('common', 'apiValidationType'))
        self.oAPIValidation.grid(column=15, row=2, sticky=W)
        
        #Main & Second Client Validation
        self.SelectedClientRadioButton= StringVar()
        self.oMainClinetRD = Radiobutton(self.mainframe, text='Main Client', padx = 3,  variable=self.SelectedClientRadioButton, value='Main Client', command=self.set_main_or_second_client)
        self.oMainClinetRD.grid(column=3, row=3, sticky=E)
        self.oSecondClinetRD = Radiobutton(self.mainframe, text='Second Client', padx = 3, variable=self.SelectedClientRadioButton, value='Second Client', command=self.set_main_or_second_client)
        self.oSecondClinetRD.grid(column=15, row=3, sticky=W)
        self.oMainClinetRD.select()
        self.SecondClientFlag = StringVar()
        self.oSecondClientFlag = Checkbutton(self.mainframe, variable=self.SecondClientFlag, command = self.set_second_client_flag)
        self.oSecondClientFlag.grid(row=3, column=17, sticky=W)
        
        '''self.lblAppversion = ttk.Label(self.mainframe, text='App Version:    ')
        self.lblAppversion.grid(column=3, row=3, sticky=E)
        self.oAppVersion = ttk.Combobox(self.mainframe, textvariable=self.AppVersion)
        self.oAppVersion.bind('<<ComboboxSelected>>', self.load_app_details)
        self.oAppVersion['values'] = ('V6', 'V5')
        self.oAppVersion.state(['readonly'])
        self.oAppVersion.set(utils.getAttribute('common', 'currentAppVersion'))
        self.oAppVersion.grid(column=15, row=3, sticky=W)'''
                
        #Main Client
        self.lblMainClient = ttk.Label(self.mainframe, text='Main Client:    ')
        self.lblMainClient.grid(column=3, row=4, sticky=E)
        self.oMainClient = ttk.Combobox(self.mainframe, textvariable=self.MainClient)
        self.oMainClient['values'] = ('Android App', 'iOS App', 'Web App')
        self.oMainClient.bind('<<ComboboxSelected>>', self.load_app_details)
        self.oMainClient.state(['readonly'])
        self.oMainClient.set(utils.getAttribute('common', 'mainClient'))
        self.oMainClient.grid(column=15, row=4, sticky=W)
        
        
        
        #if 'Platform' in self.APIValidation.get(): 
        #self.load_platformAPI_controls()
        self.api_selected_item_event(None)
        #TestSuite
        '''
        oTestSuiteList = []
        strFeatureFolder = os.path.abspath(__file__ + "/../") 
        for strFile in os.listdir(strFeatureFolder):    
            if 'TS_' in strFile:
                oTestSuiteList.append(strFile)
        oTestSuiteList = tuple(oTestSuiteList)     
        '''   
        oTestSuiteList = ('BasicSmokeTest_Dual', 'BasicSmokeTest_Heating', 'BasicSmokeTest_HotWater', 'ScheduleTest_Dual', 'ScheduleTest_Heating', 'ScheduleTest_HotWater', 'Test_Batch')
        ttk.Label(self.mainframe, text='Test Suite:    ').grid(column=3, row=13, sticky=E)
        self.oTestSuite= ttk.Combobox(self.mainframe, textvariable=self.TestSuite, width = 30)
        self.oTestSuite['values'] = oTestSuiteList
        if len(oTestSuiteList) > 0: self.oTestSuite.set(oTestSuiteList[0])
        self.oTestSuite.grid(column=15, row=13, sticky=W)        
        ttk.Label(self.mainframe, text='', width = 7).grid(column=17, row=15, sticky=E)
        
        #Execute, Result & Quit Button
        ttk.Label(self.mainbuttonFrame, text='', width = 42).grid(column=3, row=1)
        self.oExecuteIMG = PhotoImage(file=self.strIconFilePath + 'execute.gif') 
        oExecute = Button(self.mainbuttonFrame, image=self.oExecuteIMG, command=self.trigger_batch_execution)
        oExecute.grid(column=4, row=1, sticky=W)       
        ttk.Label(self.mainbuttonFrame, text='', width = 5).grid(column=6, row=1)
        self.oResultIMG= PhotoImage(file=self.strIconFilePath + 'result.gif') 
        oResult = Button(self.mainbuttonFrame, image=self.oResultIMG, command=self.showResults)
        oResult.grid(column=7, row=1)
        ttk.Label(self.mainbuttonFrame, text='', width = 35).grid(column=8, row=1)
        self.oQuitIMG= PhotoImage(file=self.strIconFilePath + 'quit.gif') 
        oQuit= Button(self.mainbuttonFrame, image=self.oQuitIMG, command=self.closeWidget)
        oQuit.grid(column=9, row=1, sticky=E)
        
        
        oDisFont = font.Font(family='Helvetica', size=15, weight='bold')
        self.oMessLabel = ttk.Label(self.executebuttonFrame, font=oDisFont, text='')
        self.oMessLabel.grid(column=1, row=2)
        self.oProgressbar = ttk.Progressbar(self.executebuttonFrame,orient ="horizontal",length = 200, mode ="indeterminate")
        self.oProgressbar.grid(column=1, row=3)
        
        self.subHeadFont = font.Font(family='Helvetica', size=17, weight='bold')
        #Kit BAtch ID
        ttk.Label(self.kitFrame, text='Kit-Batch IDs', font=self.subHeadFont).grid(row=0,column=3)
        self.oKitBatchID = Listbox(self.kitFrame, selectmode='EXTENDED', 
                                      exportselection = False, height=17)        
        self.oKitBatchID.grid(column=3, row=1, sticky=(N,W))
        self.oKitBatchID.bind('<<ListboxSelect>>', self.load_kits_to_list)
        self.update_listbox_colour(self.oKitBatchID)
        
        
        
        #Label for space
        ttk.Label(self.kitFrame, text=' ', width=3).grid(column=4, row=1, sticky=E)
        #Kit BAtch ID
        ttk.Label(self.kitFrame, text='Kit IDs', font=self.subHeadFont).grid(row=0,column=6)
        self.oKitID = Listbox(self.kitFrame, selectmode='EXTENDED', 
                                      exportselection = False, height=17)        
        self.oKitID.grid(column=6, row=1, sticky=(N,W))
        self.oKitID.bind('<<ListboxSelect>>', self.load_kit_details)
        
        #Batch Kit List buttons            
        self.spaceLabelFont = font.Font(family='Helvetica', size=1, weight='bold')
        self.oRenameIMG1= PhotoImage(file=self.strIconFilePath + 'rename.gif') 
        self.oSaveAsIMG1 = PhotoImage(file=self.strIconFilePath + 'save_as.gif') 
        self.oRemoveIMG1 = PhotoImage(file=self.strIconFilePath + 'delete.gif') 
        self.oBatchRenameKit = Button(self.batchlistbuttonFrame, image=self.oRenameIMG1, command=self.rename_batch)
        self.oBatchRenameKit.grid(column=1, row=0)
        ttk.Label(self.batchlistbuttonFrame, font=self.spaceLabelFont, text=' ').grid(column=1, row=1, sticky=E)    
        self.oBatchSaveAs = Button(self.batchlistbuttonFrame, image=self.oSaveAsIMG1, command=self.save_as_batch)
        self.oBatchSaveAs.grid(column=1, row=2)  
        ttk.Label(self.batchlistbuttonFrame, font=self.spaceLabelFont, text=' ').grid(column=1, row=5, sticky=E)
        self.oBatchRemoveKit = Button(self.batchlistbuttonFrame, image=self.oRemoveIMG1, command=self.remove_batch_from_list)
        self.oBatchRemoveKit.grid(column=1, row=6) 
        
        #Kit List buttons           
        self.oSaveIMG2 = PhotoImage(file=self.strIconFilePath + 'save.gif') 
        self.oSaveAsIMG2 = PhotoImage(file=self.strIconFilePath + 'save_as.gif') 
        self.oRenameIMG= PhotoImage(file=self.strIconFilePath + 'rename.gif') 
        self.oUpIMG = PhotoImage(file=self.strIconFilePath + 'up.gif') 
        self.oDownIMG = PhotoImage(file=self.strIconFilePath + 'down.gif') 
        self.oRemoveIMG = PhotoImage(file=self.strIconFilePath + 'delete.gif')  
        self.oRenameKit = Button(self.listbuttonFrame, image=self.oRenameIMG, command=self.rename_kit)
        self.oRenameKit.grid(column=1, row=1)
        ttk.Label(self.listbuttonFrame, font=self.spaceLabelFont, text=' ').grid(column=1, row=2, sticky=E)   
        self.oAddKit = Button(self.listbuttonFrame, image=self.oSaveAsIMG2, command=self.add_new_kit)
        self.oAddKit.grid(column=1, row=3)
        ttk.Label(self.listbuttonFrame, font=self.spaceLabelFont, text=' ').grid(column=1, row=4, sticky=E)  
        self.oUpdateKit = Button(self.listbuttonFrame, image=self.oSaveIMG2, command=self.update_kit_details)
        self.oUpdateKit.grid(column=1, row=5)
        ttk.Label(self.listbuttonFrame, font=self.spaceLabelFont, text=' ').grid(column=1, row=6, sticky=E)   
        self.oMoveUp = Button(self.listbuttonFrame, image=self.oUpIMG, command=self.move_up_priority)
        self.oMoveUp.grid(column=1, row=7)    
        ttk.Label(self.listbuttonFrame, font=self.spaceLabelFont, text=' ').grid(column=1, row=8, sticky=E)
        self.oMoveDown = Button(self.listbuttonFrame, image=self.oDownIMG, command=self.move_down_priority)
        self.oMoveDown.grid(column=1, row=9)
        ttk.Label(self.listbuttonFrame, font=self.spaceLabelFont, text=' ').grid(column=1, row=10, sticky=E)
        self.oRemoveKit = Button(self.listbuttonFrame, image=self.oRemoveIMG, command=self.remove_kit_from_list)
        self.oRemoveKit.grid(column=1, row=11) 
        
        #Load the Batch and kit to the lists
        self.load_batch_and_kitlist()
        
        
        #Create the Message window
        self.create_message_sub("")
        
        #self.oProgressbar.start()
        #self.oProgressbar.stop()
        
        self.focus_force()
        
    #Loads the list of batches and the Kits to the corresponding list boxes
    def load_batch_and_kitlist(self, boolSelectDefaultItem = True):
        oJsonDict = self.get_kit_batch_json()
        
        self.current_batch_id = oJsonDict["kit_batch"]['current_batch_id']        
        oBatchList = oJsonDict["kit_batch"]['list_of_batches']
        intIndex = 0
        self.oKitBatchID.delete(0, END) 
        for oBatch in oBatchList:
            self.oKitBatchID.insert(intIndex, oBatch)  
            intIndex = intIndex + 1
        self.update_listbox_colour(self.oKitBatchID)        
        if boolSelectDefaultItem: self.oKitBatchID.select_set(0)    
        self.load_kits_to_list(None)
       
            
    #Loads the list of Kits for the selected batch
    def load_kits_to_list(self, event, boolSelectDefaultItem = True):
        oJsonDict = self.get_kit_batch_json()
        
        current_batch_id = self.oKitBatchID.curselection()
        if len(current_batch_id)>0:
            current_batch_id = self.oKitBatchID.get(current_batch_id[0])
            print(current_batch_id, '\n')
            oKitList = oJsonDict["kit_batch"]['list_of_batches'][current_batch_id]['list_of_kits']
            self.oKitID.delete(0, END) 
            oKitListDict = {}
            for oKit in oKitList:
                intPriority = int(oKitList[oKit]['priority'])
                oKitListDict[intPriority] = oKit
            for oKey in sorted(oKitListDict):                
                self.oKitID.insert(oKey, oKitListDict[oKey])    
            self.update_listbox_colour(self.oKitID)  
            if len(self.oKitID.curselection()) == 0 and boolSelectDefaultItem: 
                #if len(self.oKitID.get(first, last))
                self.oKitID.select_set(0)    
            self.load_kit_details(None)
    
    #Loads the kit details 
    def load_kit_details(self, event):
        current_batch_id, current_kit_id = self.get_selected_batch_kit()
        if current_batch_id != "" and current_kit_id != "":
            oJsonDict = self.get_kit_batch_json()
            oKitDetails = oJsonDict["kit_batch"]['list_of_batches'][current_batch_id]['list_of_kits'][current_kit_id]
            self.oEnvironment.set(oKitDetails['currentEnvironment'])
            self.oAPIValidation.set(oKitDetails['apiValidationType']) 
            self.api_selected_item_event(None)
            self.oUserName.set(oKitDetails['userName'])
            self.oPassword.set(oKitDetails['password'])
            self.oTestSuite.set(oKitDetails['test_suite'])
            
            #self.oAppVersion.set('V6')
            #oKitDetails['resultFolderLabel'] = "" # self.Environment.get()
            
            if 'MAIN' in self.lblMainClient.cget("text").upper(): strClientKey = 'mainClient'
            else: strClientKey = 'secondClient'
            self.oMainClient.set(oKitDetails[strClientKey]['name'])
            self.load_app_details(None)
            if 'IOS' in oKitDetails[strClientKey]['name'].upper():
                self.oAppFilePath.set(oKitDetails[strClientKey]['appFileName'])
                self.oDeviceName.set(oKitDetails[strClientKey]['deviceName'])
                self.oUDID.set(oKitDetails[strClientKey]['udid'])
                self.oOSVersion.set(oKitDetails[strClientKey]['platformVersion'])
            elif 'ANDROID' in oKitDetails[strClientKey]['name'].upper():
                self.oAppFilePath.set(oKitDetails[strClientKey]['appFileName'])
                self.oDeviceName.set(oKitDetails[strClientKey]['deviceName'])
                self.oOSVersion.set(oKitDetails[strClientKey]['platformVersion'])
            elif 'WEB' in oKitDetails[strClientKey]['name'].upper():
                self.oBrowserName.set(oKitDetails[strClientKey]['browserName'])
                self.oURL.set(oKitDetails[strClientKey]['loginURL'])
            
            
            ALAPI.createCredentials(oKitDetails['currentEnvironment'], username = oKitDetails['userName'], password = oKitDetails['password'])
            self.session = ALAPI.sessionObject()
            if self.session.statusCode != 200:
                resp =self.session.response
                if isinstance(resp, str): resp = json.loads(resp)
                self.update()
                showinfo('ERROR', resp)
            else:
                ALAPI.deleteSessionV6(self.session)
                
    
    #def Rename batch
    def rename_batch(self):
        boolNameAlreadyExists = True
        while boolNameAlreadyExists:
            current_batch_id, current_kit_id = self.get_selected_batch_kit()
            if current_batch_id == "": return False, None
            if current_batch_id.upper() == 'TEMP_BATCH':
                self.display_message("Can't Rename 'TEMP_BATCH'", 0)
                return False
            strNewBatchName = simpledialog.askstring('Batch - New Name', 'Enter the Name of the Batch', parent = self.window, initialvalue = current_batch_id)
            if strNewBatchName is None: return False, None
            if current_batch_id.upper() == strNewBatchName.upper(): print()
            current_batch_index = self.oKitBatchID.curselection()[0]
            intIndex = 0
            boolNameAlreadyExists = False
            for strBatchName in self.oKitBatchID.get(0, END):
                if strBatchName.upper() == strNewBatchName.upper():
                    boolNameAlreadyExists = True
                    self.display_message("The Entered Name already exist. Please enter another name", 0)
                    break
                intIndex = intIndex + 1
                
        oJsonDict = self.get_kit_batch_json()
        oJsonDict["kit_batch"]['list_of_batches'][strNewBatchName] = oJsonDict["kit_batch"]['list_of_batches'].pop(current_batch_id)
        self.put_kit_batch_json(oJsonDict)
        self.oKitBatchID.delete(current_batch_index)
        self.oKitBatchID.insert(current_batch_index, strNewBatchName)
        self.oKitBatchID.select_set(current_batch_index)
        self.load_kits_to_list(None, False)
        self.display_message("The Batch is renamed successfully", 1)
        self.focus_force()
        return True, strNewBatchName
    
    #Rename the Kit
    def rename_kit(self):
        boolNameAlreadyExists = True
        while boolNameAlreadyExists:
            current_batch_id, current_kit_id = self.get_selected_batch_kit()
            if current_kit_id == "": return False, None
            strNewKitName = simpledialog.askstring('Kit - New Name', 'Enter the Name of the Kit', parent = self.window, initialvalue = current_kit_id)
            if strNewKitName is None: return False, None
            if current_kit_id.upper() == strNewKitName.upper(): print()
            current_kit_index = self.oKitID.curselection()[0]
            intIndex = 0
            boolNameAlreadyExists = False
            for strKitName in self.oKitID.get(0, END):
                if strKitName.upper() == strNewKitName.upper():
                    boolNameAlreadyExists = True
                    self.display_message("The Entered Name already exist. Please enter another name", 0)
                    break
                intIndex = intIndex + 1
        oJsonDict = self.get_kit_batch_json()
        oJsonDict["kit_batch"]['list_of_batches'][current_batch_id]['list_of_kits'][strNewKitName] = oJsonDict["kit_batch"]['list_of_batches'][current_batch_id]['list_of_kits'].pop(current_kit_id)
        self.put_kit_batch_json(oJsonDict)
        self.load_kits_to_list(None, False)
        self.oKitID.select_set(current_kit_index)
        self.display_message("The Kit is renamed successfully", 1)
        self.focus_force()
        return True, strNewKitName
   
   
    #Save as new Batch
    def save_as_batch(self):
        intBatchIndex = self.oKitBatchID.curselection()[0] + 1
        strTimeStamp = datetime.datetime.today().strftime("%d-%b-%Y_%H-%M-%S")        
        current_batch_id, current_kit_id = self.get_selected_batch_kit()
        self.oKitBatchID.insert(intBatchIndex,strTimeStamp)
        self.oKitBatchID.select_clear(0, END)
        self.oKitBatchID.select_set(intBatchIndex)
        
        oJsonDict = self.get_kit_batch_json()
        oJsonDict["kit_batch"]['list_of_batches'][strTimeStamp]= oJsonDict["kit_batch"]['list_of_batches'][current_batch_id]
        self.put_kit_batch_json(oJsonDict)
        
        oNewName = self.rename_batch()
        if not oNewName[0]:
            self.oKitBatchID.delete(intBatchIndex)            
            del oJsonDict["kit_batch"]['list_of_batches'][strTimeStamp]
            self.put_kit_batch_json(oJsonDict)
            self.oKitBatchID.select_set(intBatchIndex-1)  
            self.display_message("The New Batch was not created as the Name was not entered correctly", 0)
        else:            
            self.load_kits_to_list(None)
            self.display_message("The New Batch was created successfully", 1)
       
    #Remove Batch from list
    def remove_batch_from_list(self):
        
        current_batch_id, current_kit_id = self.get_selected_batch_kit()
        if current_batch_id == "": return False, None
        if current_batch_id.upper() == 'TEMP_BATCH':
            self.display_message("Can't Delete 'TEMP_BATCH'", 0)
            return False
        oJsonDict = self.get_kit_batch_json()
        intBatchIndex = self.oKitBatchID.curselection()[0]
        current_batch_id, current_kit_id = self.get_selected_batch_kit()
        strClickedButton = askquestion('Remove Batch','Are you sure you want to remove the selected Batch: ' + current_batch_id, parent = self, default = NO, icon = WARNING)
        
        if 'YES' in strClickedButton.upper():
            del oJsonDict["kit_batch"]['list_of_batches'][current_batch_id]              
            self.put_kit_batch_json(oJsonDict)
            self.oKitBatchID.delete(intBatchIndex)
            if not intBatchIndex == 0: intBatchIndex = intBatchIndex - 1
            self.oKitBatchID.select_set(intBatchIndex)  
            self.load_kits_to_list(None)    
            #if len(self.oKitID.get(0, END)) == intBatchIndex: intBatchIndex = intBatchIndex - 1
            self.display_message('The Batch: ' + current_batch_id + ' is removed successfully.', 1)  
            self.focus_force()

        
    #Add new Kit
    def add_new_kit(self):
        ALAPI.createCredentials(self.Environment.get(), username = self.UserName.get(), password = self.Password.get())
        self.session = ALAPI.sessionObject()
        if self.session.statusCode != 200:
            resp =self.session.response
            if isinstance(resp, str): resp = json.loads(resp)
            self.update()
            showinfo('ERROR', resp)
            self.display_message("User Name or Password Error. Kit not Updated", 0)
        else:
            ALAPI.deleteSessionV6(self.session)
            intPiority = len(self.oKitID.get(0, END))
               
            strTimeStamp = datetime.datetime.today().strftime("%d-%b-%Y_%H-%M-%S"  )
            
            current_batch_id, current_kit_id = self.get_selected_batch_kit()
            oJsonDict = self.get_kit_batch_json()
            
            oJsonDict["kit_batch"]['list_of_batches'][current_batch_id]['list_of_kits'][strTimeStamp] = {"priority": str(intPiority)}
            self.put_kit_batch_json(oJsonDict)
            
            self.oKitID.insert(END,strTimeStamp)
            self.oKitID.select_clear(0, END)
            self.oKitID.select_set(END)
            oNewName = self.rename_kit()
            if not oNewName[0]:
                self.oKitID.delete(intPiority)            
                del oJsonDict["kit_batch"]['list_of_batches'][current_batch_id]['list_of_kits'][strTimeStamp]
                self.put_kit_batch_json(oJsonDict)
                self.display_message("The New Kit was not created as the Name was not entered correctly", 0)
            else:
                self.update_kit_details()
    
        
    #Updates the existing Kit details
    def update_kit_details(self, boolValidateLoginCred = True):
        current_batch_id, current_kit_id = self.get_selected_batch_kit()
        
        if not (current_batch_id == "" and current_kit_id == ""):
            if boolValidateLoginCred:
                ALAPI.createCredentials(self.Environment.get(), username = self.UserName.get(), password = self.Password.get())
                self.session = ALAPI.sessionObject()
                if self.session.statusCode != 200:
                    resp =self.session.response
                    if isinstance(resp, str): resp = json.loads(resp)
                    self.update()
                    showinfo('ERROR', resp)
                    self.display_message("User Name or Password Error. Kit not added", 0)
                else: 
                    ALAPI.deleteSessionV6(self.session)
                    
            oJsonDict = self.get_kit_batch_json()
            intCurrentKitPriority = int(oJsonDict["kit_batch"]['list_of_batches'][current_batch_id]['list_of_kits'][current_kit_id]['priority'])
            oKitDetails = oJsonDict["kit_batch"]['list_of_batches'][current_batch_id]['list_of_kits'][current_kit_id]
            oDictMainClient = oKitDetails['mainClient']
            oDictSecondClient = oKitDetails['secondClient']
            oKitDetails = {}
            oKitDetails['currentEnvironment'] = self.Environment.get()
            oKitDetails['currentAppVersion'] = 'V6' #self.AppVersion.get()
            oKitDetails['apiValidationType'] = self.APIValidation.get()
            oKitDetails['userName'] = self.UserName.get()
            oKitDetails['password'] = self.Password.get()
            oKitDetails['resultFolderLabel'] = "" # self.Environment.get()
            oKitDetails['priority'] = str(intCurrentKitPriority)
            oKitDetails['test_suite'] = self.TestSuite.get()
            if self.SecondClientFlag.get() == '1': oKitDetails['secondClientValidateFlag'] = 'YES'
            else: oKitDetails['secondClientValidateFlag'] = 'NO'
            
            if 'MAIN' in self.lblMainClient.cget("text").upper(): 
                strClientKey = 'mainClient'
                oKitDetails['secondClient'] =oDictSecondClient
            else: 
                strClientKey = 'secondClient'
                oKitDetails['mainClient'] = oDictMainClient
                
            oKitDetails[strClientKey] = {}
            if 'IOS' in self.MainClient.get().upper():
                oKitDetails[strClientKey]['appFileName'] = self.AppFilePath.get()
                oKitDetails[strClientKey]['deviceName'] = self.DeviceName.get()
                oKitDetails[strClientKey]['name'] = self.MainClient.get()
                oKitDetails[strClientKey]['udid'] = self.UDID.get()
                oKitDetails[strClientKey]['platformVersion'] = self.OSVersion.get()
            elif 'ANDROID' in self.MainClient.get().upper():
                oKitDetails[strClientKey]['appFileName'] = self.AppFilePath.get()
                oKitDetails[strClientKey]['deviceName'] = self.DeviceName.get()
                oKitDetails[strClientKey]['name'] = self.MainClient.get()
                oKitDetails[strClientKey]['platformVersion'] = self.OSVersion.get()
            elif 'WEB' in self.MainClient.get().upper():
                oKitDetails[strClientKey]['name'] = self.MainClient.get()
                oKitDetails[strClientKey]['browserName'] = self.BrowserName.get()
                oKitDetails[strClientKey]['loginURL'] = self.URL.get()
            
            print(oKitDetails)
            oJsonDict["kit_batch"]['list_of_batches'][current_batch_id]['list_of_kits'][current_kit_id] = oKitDetails
            self.put_kit_batch_json(oJsonDict)
            self.display_message('The Kit: ' + current_kit_id + ' is Updated Successfully.', 1)
            
    #Display message
    def display_message(self, strMessage, intColorIndex):
        strFontColor = 'black'
        if intColorIndex == 0: strFontColor = 'red'
        if intColorIndex == 1: strFontColor = 'dark green'
        if intColorIndex == 2: strFontColor = 'orange'
        self.oMessLabel.configure(text = strMessage, compound = CENTER, foreground = strFontColor)
        self.update()
        time.sleep(2)
        self.oMessLabel.configure(text = "")
        self.update()
        
        return
        '''
        self.position_window(self.oMessageWindow,w=500, h=100)
        self.messagelabel.configure(text=strMessage, width = len(strMessage))
        self.messagelabel.pack()
        self.oMessageWindow.deiconify()
        time.sleep(10)
        #self.position_window(self.oMessageWindow,w=0, h=0)
        self.oMessageWindow.iconify()'''
        
    #Display message
    def create_message_sub(self, strMessage):
        print(strMessage)
        self.oMessageWindow = Toplevel()
        self.oMessageWindow.wm_title("Hive Test Automation - Message")
        
        #Frame.__init__(self, self.oMessageWindow)
        #Frame1
        self.messageframe = ttk.Frame(self.oMessageWindow, padding="100 30 100 300")
        self.messageframe.configure(style='TFrame')
        self.messageframe.grid(column=0, row=0, sticky=(N))
        self.messageframe.columnconfigure(0, weight=1)
        self.messageframe.rowconfigure(0, weight=1)
        
        self.messagelabel = ttk.Label(self.messageframe, text=strMessage)
        self.messagelabel.grid(column=1, row=1, sticky=(N))
        self.messagelabel.pack()
        self.position_window(self.oMessageWindow,w=500, h=100)
        self.oMessageWindow.iconify()
        #self.oMessageWindow.mainloop()
        
    #Gets the selacted Batch and Kit combo
    def get_selected_batch_kit(self):
        current_kit_id = ""
        current_batch_id = self.oKitBatchID.curselection()
        if len(current_batch_id)>0:
            current_batch_id = self.oKitBatchID.get(current_batch_id[0])
            current_kit_id = self.oKitID.curselection()
            print(current_kit_id)
            if len(current_kit_id)>0:
                current_kit_id = self.oKitID.get(current_kit_id[0])
            else: current_kit_id = ""
        else: current_batch_id = ""
        return current_batch_id, current_kit_id
    
    #move the kits priority higher       
    def move_up_priority(self):
        #print(pymsgbox.confirm('Nuke the site from orbit?', 'Confirm nuke', ["Yes, I'm sure.", 'Cancel']))
        #Message([self.window], title="[title]", message="[message]")
        
        oJsonDict = self.get_kit_batch_json()
        
        current_batch_id = self.oKitBatchID.curselection()
        if len(current_batch_id)>0:
            current_batch_id = self.oKitBatchID.get(current_batch_id[0])
            current_kit_id = self.oKitID.curselection()
            print(current_kit_id)
            if len(current_kit_id)>0:
                current_kit_id = self.oKitID.get(current_kit_id[0])
                print(current_batch_id, current_kit_id)
                intCurrentKitPriority = int(oJsonDict["kit_batch"]['list_of_batches'][current_batch_id]['list_of_kits'][current_kit_id]['priority'])
        
                if intCurrentKitPriority == 0: return
                intSetPriorityTo = intCurrentKitPriority - 1
                
                
                oKitList = oJsonDict["kit_batch"]['list_of_batches'][current_batch_id]['list_of_kits']
                for oKit in oKitList:
                    intPriority = int(oKitList[oKit]['priority'])
                    if intPriority == intSetPriorityTo:
                        oJsonDict["kit_batch"]['list_of_batches'][current_batch_id]['list_of_kits'][oKit]['priority'] = str(intCurrentKitPriority)
                oJsonDict["kit_batch"]['list_of_batches'][current_batch_id]['list_of_kits'][current_kit_id]['priority'] = str(intSetPriorityTo)
                self.put_kit_batch_json(oJsonDict)
                self.load_kits_to_list(None, False)      
                self.oKitID.select_set(intSetPriorityTo)    
                
    #move the kits priority higher       
    def move_down_priority(self):
        oJsonDict = self.get_kit_batch_json()
        
        current_batch_id = self.oKitBatchID.curselection()
        if len(current_batch_id)>0:
            current_batch_id = self.oKitBatchID.get(current_batch_id[0])
            current_kit_id = self.oKitID.curselection()
            print(current_kit_id)
            if len(current_kit_id)>0:
                current_kit_id = self.oKitID.get(current_kit_id[0])
                print(current_batch_id, current_kit_id)
                intCurrentKitPriority = int(oJsonDict["kit_batch"]['list_of_batches'][current_batch_id]['list_of_kits'][current_kit_id]['priority'])
                intListCount = len(oJsonDict["kit_batch"]['list_of_batches'][current_batch_id]['list_of_kits']) -1
                if intCurrentKitPriority == intListCount: return
                intSetPriorityTo = intCurrentKitPriority + 1
                
                
                oKitList = oJsonDict["kit_batch"]['list_of_batches'][current_batch_id]['list_of_kits']
                for oKit in oKitList:
                    intPriority = int(oKitList[oKit]['priority'])
                    if intPriority == intSetPriorityTo:
                        oJsonDict["kit_batch"]['list_of_batches'][current_batch_id]['list_of_kits'][oKit]['priority'] = str(intCurrentKitPriority)
                        oJsonDict["kit_batch"]['list_of_batches'][current_batch_id]['list_of_kits'][current_kit_id]['priority'] = intSetPriorityTo
                self.put_kit_batch_json(oJsonDict)
                self.load_kits_to_list(None, False)      
                self.oKitID.select_set(intSetPriorityTo)    
    
    
    def testPrint(self):
        while True:
            time.sleep(3)
            print('Hiiii')
            
    #Remove the kit from the list
    def remove_kit_from_list(self):
        oJsonDict = self.get_kit_batch_json()
        
        current_batch_id = self.oKitBatchID.curselection()
        if len(current_batch_id)>0:
            current_batch_id = self.oKitBatchID.get(current_batch_id[0])
            current_kit_id = self.oKitID.curselection()
            print(current_kit_id)
            if len(current_kit_id)>0:
                intSelectedIndex = current_kit_id[0]
                current_kit_id = self.oKitID.get(current_kit_id[0])
                strClickedButton = askquestion('Remove Kit','Are you sure you want to remove the selected Kit: ' + current_kit_id, parent = self, default = NO, icon = WARNING)
                print(strClickedButton)
                if 'YES' in strClickedButton.upper():
                    oKitList = oJsonDict["kit_batch"]['list_of_batches'][current_batch_id]['list_of_kits']
                    del oKitList[current_kit_id]                
                    oJsonDict["kit_batch"]['list_of_batches'][current_batch_id]['list_of_kits'] = oKitList
                    self.put_kit_batch_json(oJsonDict)
                    self.load_kits_to_list(None, None)    
                    if len(self.oKitID.get(0, END)) == intSelectedIndex: intSelectedIndex = intSelectedIndex - 1
                    self.oKitID.select_set(intSelectedIndex)  
                    self.display_message('The Kit: ' + current_kit_id + ' is removed successfully.', 1)  
                    self.focus_force()
                
    #Write back the JSON to the kit_batch.JSON
    def put_kit_batch_json(self, oJsonDict):
        strEnvironmentFolderPAth = os.path.abspath(__file__ + "/../../../") + "/02_Manager_Tier/EnviromentFile/"        
        strGlobVarFilePath = strEnvironmentFolderPAth + '/kit_batch.json'       
        strJson = open(strGlobVarFilePath, mode='w+')
        strJson.write(json.dumps(oJsonDict, indent=4, sort_keys=True))
        strJson.close()

    #Get the kit batch json as dictionary object
    def get_kit_batch_json(self):
        strEnvironmentFolderPAth = os.path.abspath(__file__ + "/../../../") + "/02_Manager_Tier/EnviromentFile/"        
        strGlobVarFilePath = strEnvironmentFolderPAth + '/kit_batch.json'    
        strJson = open(strGlobVarFilePath, mode='r')
        oJsonDict = json.loads(strJson.read())
        strJson.close()
        return oJsonDict
        
    #Updates the Listbox items to dual colours
    def update_listbox_colour(self, oListbox):
        oItemList = oListbox.get(0, END)
        for intIndex in range(0, len(oItemList)):
            if intIndex % 2 == 0:
                oListbox.itemconfig(intIndex, bg='WhiteSmoke')
        
    #Launch the Result Summary HTML
    def showResults(self):           
        try:
            strTempFile = os.path.abspath(__file__ + "/../../../") + "/02_Manager_Tier/EnviromentFile/scripts/Temp.txt" 
            oReader = open(strTempFile, 'r')
            oHTMLSummaryPath = 'file://' + oReader.read()
            webbrowser.open(oHTMLSummaryPath,new=2)
        except: print(traceback.format_exc())
        
    #Place Window on the center fo the screen
    def position_window(self, parent, w, h):
        # get screen width and height
        ws = parent.winfo_screenwidth()
        hs = parent.winfo_screenheight()
        # calculate position x, y
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        parent.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
    def load_platformAPI_controls(self):
        if 'Platform' in self.APIValidation.get():
            #self.position_window(self.window, w=self.intCommonWidth, h=330)
            try:
                self.lblZigbeeEPNOde.destroy()
                self.oATNode.destroy()
                self.boolZigbeeFieldDestroyed = True
            except: pass
            
            
           
            oPlatClientTuple = ('Android App', 'iOS App', 'Web App')
            self.oMainClient['values'] = oPlatClientTuple
            strMainClient = utils.getAttribute('common', 'mainClient')
            if strMainClient not in oPlatClientTuple: 
                strMainClient = 'Android App'
                self.oMainClient.set(strMainClient)
                self.load_app_details(None)
            else: self.oMainClient.set(strMainClient)
            if self.boolUserPassDestroyed: 
                ''' #App Version
                self.lblAppversion = ttk.Label(self.mainframe, text='App Version:    ')
                self.lblAppversion.grid(column=3, row=4, sticky=E)
                self.oAppVersion = ttk.Combobox(self.mainframe, textvariable=self.AppVersion)
                self.oAppVersion.bind('<<ComboboxSelected>>', self.load_app_details)
                self.oAppVersion['values'] = ('V6', 'V5')
                self.oAppVersion.state(['readonly'])
                self.oAppVersion.set(utils.getAttribute('common', 'currentAppVersion'))
                self.oAppVersion.grid(column=15, row=4, sticky=W)'''
                
                #User Name
                self.lblUserName = ttk.Label(self.mainframe, text='User Name:    ')
                self.lblUserName.grid(column=3, row=11, sticky=E)
                self.oUserName = ttk.Combobox(self.mainframe, textvariable=self.UserName)
                self.oUserName['values'] = ('auto1_v6', 'tester2', 'tester4_v6')
                self.oUserName.set(utils.getAttribute('common', 'userName'))
                self.oUserName.grid(column=15, row=11, sticky=W)
                
                #Password
                self.lblPassword = ttk.Label(self.mainframe, text='Password:    ')
                self.lblPassword.grid(column=3, row=12, sticky=E)
                self.oPassword = ttk.Combobox(self.mainframe, textvariable=self.Password)
                self.oPassword['values'] = ('password1', 'Password1', 'passw0rd')
                self.oPassword.set(utils.getAttribute('common', 'password'))
                self.oPassword.grid(column=15, row=12, sticky=W)
                self.boolUserPassDestroyed = False
        else:
            #Set Main client for ZigBee API validation
            self.oMainClient['values'] = ('Thermostat')
            self.oMainClient.set('Thermostat')
            #Destroy platform API fields
            try:
                self.oBrowse.destroy()
                #self.lblAppversion.destroy()
                self.lblUserName.destroy()
                self.lblPassword.destroy()
                #self.oAppVersion.destroy()
                self.oAppFilePath.destroy()
                self.oOSVersion.destroy()
                self.oDeviceName.destroy()
                self.oUDID.destroy()
                self.lblAppFileName.destroy()
                self.lblOSVersion.destroy()
                self.lblDeviceName.destroy()
                self.lblUDID.destroy()
                self.boolAppFieldDestroyed = True                
                self.boolUDIDFieldDestroyed = True
                self.boolUserPassDestroyed = True
                self.boolWebFieldDestroyed = True
                self.oUserName.destroy()
                self.oPassword.destroy()
                self.lblURL.destroy()
                self.oURL.destroy()
                self.lblBrowserName.destroy()
                self.oBrowserName.destroy()
            except: pass
            
            #Zigbee EP Node ID
            if self.boolZigbeeFieldDestroyed:
                self.lblZigbeeEPNOde = ttk.Label(self.mainframe, text='End-Point  \n Node ID:    ')
                self.lblZigbeeEPNOde.grid(column=3, row=4, sticky=E)
                self.oATNode = ttk.Combobox(self.mainframe, textvariable=self.ATNode)
                self.oATNode.set(utils.getAttribute('common', 'atZigbeeNode'))
                self.oATNode.grid(column=15, row=4, sticky=W)
                #self.position_window(self.window, w=490, h=290)
                self.boolZigbeeFieldDestroyed = False
    
    def set_main_or_second_client(self):
        if 'SECOND' in self.SelectedClientRadioButton.get().upper(): 
            self.update_kit_details(False)
            self.lblMainClient.config(text='Second Client:    ')
            if 'ANDROID' in self.MainClient.get().upper() or 'IOS' in self.MainClient.get().upper():
                self.oMainClient['values'] = ('Web App')
                self.oMainClient.set('Web App')
                self.load_app_details(None)
                self.update_kit_details(False)
            else: 
                self.load_kit_details(None)
                self.oMainClient['values'] = ('Android App', 'iOS App', 'Web App')
        else: 
            self.update_kit_details(False)
            self.lblMainClient.config(text='Main Client:    ')
            self.load_kit_details(None)
            self.oMainClient['values'] = ('Android App', 'iOS App', 'Web App')
            
            
            #self.oNano2FW.config(state=DISABLED)
        
        #self.oMainClient.set('Web App')
        #self.load_app_details(None)
        
    def set_second_client_flag(self):
        if self.SecondClientFlag.get()=='0':
            self.oSecondClinetRD.config(state=DISABLED)
            self.oMainClinetRD.config(state=DISABLED)
            self.oMainClinetRD.select()
            self.set_main_or_second_client()
        else:
            self.oSecondClinetRD.config(state='!DISABLED')
            self.oMainClinetRD.config(state='!DISABLED')
            self.oSecondClinetRD.select()
            self.set_main_or_second_client()
        
    def load_app_details(self, event):
        if not 'Platform' in self.APIValidation.get(): return False
        print(self.MainClient.get().upper())
        #if self.AppVersion.get() is '': 
        strAppVer = utils.getAttribute('common', 'currentAppVersion')
        #else: strAppVer = self.AppVersion.get()
        if 'WEB' in self.MainClient.get().upper():
            #self.position_window(self.window, w=490, h=380)
            print('im in')
            try:
                self.oBrowse.destroy()
                self.oAppFilePath.destroy()
                self.oOSVersion.destroy()
                self.oDeviceName.destroy()
                self.oUDID.destroy()
                self.lblAppFileName.destroy()
                self.lblOSVersion.destroy()
                self.lblDeviceName.destroy()
                self.lblUDID.destroy()
                self.boolAppFieldDestroyed = True                
                self.boolUDIDFieldDestroyed = True
                print('Killed for web')
            except: pass
            if self.boolWebFieldDestroyed:
                #Browser Name
                self.lblBrowserName, self.oBrowserName = self.create_combobox(5, '     Browser Name:    ', self.BrowserName, (), "", False)    
                self.oBrowserName['values'] = ('Firefox', 'Chrome', 'Safari')
                self.oBrowserName.set(utils.getAttribute('web', 'browserName', strAppVer))
                #URL
                self.lblURL, self.oURL = self.create_combobox(6, 'Web URL:    ', self.URL, (), "", False)
                self.oURL.set(utils.getAttribute('web', 'loginURL', strAppVer))
                self.boolWebFieldDestroyed = False
        else:    
            try:
                self.lblURL.destroy()
                self.oURL.destroy()
                self.lblBrowserName.destroy()
                self.oBrowserName.destroy()
                self.boolWebFieldDestroyed = True
            except: pass
            
            if self.boolAppFieldDestroyed:
                #AppFilePath
                self.lblAppFileName, self.oAppFilePath = self.create_combobox(5, 'App File Name:    ', self.AppFilePath, (), "", False)  
                self.oAppFilePath.configure(width = 30)
                self.oBrowseIMG = PhotoImage(file=self.strIconFilePath + 'browse.gif') 
                self.oBrowse = Button(self.mainframe, image=self.oBrowseIMG, command=self.browse_app_file)
                self.oBrowse.grid(column=17, row=5, sticky=W)          
                #OS platform version
                self.lblOSVersion, self.oOSVersion = self.create_combobox(6, 'Mobile OS Version:    ', self.OSVersion, (), "", False)        
                #Device Name             
                self.lblDeviceName, self.oDeviceName = self.create_combobox(7, 'Device Name:    ', self.DeviceName, (), "", False)  
                self.boolAppFieldDestroyed = False
            
            if self.boolUDIDFieldDestroyed:      
                #UDID
                self.lblUDID, self.oUDID = self.create_combobox(9, 'UDID:    ', self.UDID, (), "", False)
                self.oUDID.configure(width = 30)
                self.boolUDIDFieldDestroyed = False
            if 'IOS' in self.MainClient.get().upper():
                #self.position_window(self.window, w=self.intCommonWidth, h=430)
                strFilePath = utils.getAttribute(self.MainClient.get().split()[0], 'appFileName')
                self.load_app_filename(strFilePath)
                self.oOSVersion['values'] = ('9.0', '8.4', '8.2', '8.3', '8.1')
                self.oOSVersion.set(utils.getAttribute('iOS', 'platformVersion', strAppVer))
                self.oDeviceName.set(utils.getAttribute('iOS', 'deviceName', strAppVer))
                self.oUDID.set(utils.getAttribute('iOS', 'udid'))
                
            elif 'ANDROID' in self.MainClient.get().upper():
                print('hee')
                #self.position_window(self.window, w=self.intCommonWidth, h=410)
                strFilePath = utils.getAttribute(self.MainClient.get().split()[0].lower(), 'appFileName')
                self.load_app_filename(strFilePath)
                self.oOSVersion['values'] = ('5.1', '5.0', '4.4', '4.3')
                self.oOSVersion.set(utils.getAttribute('android', 'platformVersion', strAppVer))
                self.oDeviceName.set(utils.getAttribute('android', 'deviceName', strAppVer))
                self.oUDID.destroy()
                self.lblUDID.destroy()                
                self.boolUDIDFieldDestroyed = True
            
        
    def load_app_filename(self, strFilePath):    
        if self.MainClient.get().split()[0] == 'Android' : oAppExt = ("APK", "*.apk")
        else: oAppExt = ("IPA", "*.ipa")
        strAPPFolderPAth = os.path.abspath(__file__ + "/../../../") + "/02_Manager_Tier/EnviromentFile/Apps/" + self.MainClient.get().split()[0] + '/' + self.Environment.get().split()[0]
        
        strFileName = ntpath.split(strFilePath)[1]
        oAppFileList = []
        oAllFileList = os.listdir(strAPPFolderPAth)
        for strFile in oAllFileList:    
            if os.path.splitext(strFile)[1].upper() == '.' + oAppExt[0]:
                oAppFileList.append(strFile)
        oAppFileTuple = tuple(oAppFileList)
        self.oAppFilePath['value'] = oAppFileTuple
        self.oAppFilePath.set(strFileName)
            
    def create_combobox(self, intRow, strLabel, oStringVar, oValueList, strDefaultValue, boolReadOnly):                
        oLabel = ttk.Label(self.mainframe, text=strLabel)
        oLabel.grid(column=3, row=intRow, sticky=E)
        oCombobox = ttk.Combobox(self.mainframe, textvariable=oStringVar)
        oCombobox['values'] = oValueList
        oCombobox.set(strDefaultValue)                
        if boolReadOnly: oCombobox.state(['readonly'])
        oCombobox.grid(column=15, row=intRow, sticky=W)
        return oLabel, oCombobox
   
    def closeWidget(self):
        strClickedButton = askquestion('Quit','Are you sure you want to Quit?', parent = self, default = NO, icon = WARNING)
        
        if 'YES' in strClickedButton.upper():
            exit()
        else: self.window.focus_set()
        '''about_message =' suuper'
        top = Toplevel()
        top.title("View Test Results")
        self.position_window(top,w=200, h=330)
        msg = Message(top, text=about_message)
        msg.pack()
        
        button = Button(top, text="Dismiss", command=top.destroy)
        button.pack()'''
    
    def updateGlobalVarJson(self):
        #Reading all data from GlobalVar.Json
        strClickedButton = askquestion('Execute','Are you sure you want to Execute the selected Batch : '  + self.get_selected_batch_kit()[0], parent = self, default = YES, icon = WARNING)
    
        if 'NO' in strClickedButton.upper():
            self.window.focus_set()
            return
        
        self.validate_kit_login()
        return
        ALAPI.createCredentials(self.Environment.get(), username = self.UserName.get(), password = self.Password.get())
        self.session = ALAPI.sessionObject()
        if self.session.statusCode != 200:
            resp =self.session.response
            if isinstance(resp, str): resp = json.loads(resp)
            showinfo('ERROR', resp)
            return
        
        strEnvironmentFolderPAth = os.path.abspath(__file__ + "/../../../") + "/02_Manager_Tier/EnviromentFile/"        
        strGlobVarFilePath = strEnvironmentFolderPAth + '/GlobalVar.json'    
        strJson = open(strGlobVarFilePath, mode='r')
        oJsonDict = json.loads(strJson.read())
        strJson.close()
        
        oGlobalDict = oJsonDict['globalVariables']
        #updating the json Dictionary based on the the input parameter selected on the GUI
        oGlobalDict['currentEnvironment'] = self.Environment.get()
        oGlobalDict['apiValidationType'] = self.APIValidation.get()
        oGlobalDict['mainClient'] = self.MainClient.get()
        
        oCurrentEnvDict = oGlobalDict['listOfEnvironments'][self.Environment.get()]
        if 'ZIGBEE' in self.APIValidation.get().upper():
            oGlobalDict['atZigbeeNode'] = self.ATNode.get()
        else:
            strAppVer = 'V6' #self.AppVersion.get()
            oGlobalDict['currentAppVersion']= 'V6' #self.AppVersion.get()
            oGlobalDict['userName']= self.UserName.get()
            oGlobalDict['password']= self.Password.get()
            
            if 'IOS' in self.MainClient.get().upper():
                oCurrentEnvDict['iOS' + strAppVer]['appFileName'] = self.AppFilePath.get()
                oCurrentEnvDict['iOS' + strAppVer]['platformVersion'] = self.OSVersion.get()
                oCurrentEnvDict['iOS' + strAppVer]['deviceName'] = self.DeviceName.get()
                oCurrentEnvDict['iOS' + strAppVer]['udid'] = self.UDID.get()
            elif 'ANDROID' in self.MainClient.get().upper():                
                oCurrentEnvDict['android' + strAppVer]['appFileName'] = self.AppFilePath.get()
                oCurrentEnvDict['android' + strAppVer]['platformVersion'] = self.OSVersion.get()
                oCurrentEnvDict['android' + strAppVer]['deviceName'] = self.DeviceName.get()
            elif 'WEB' in self.MainClient.get().upper():                
                oCurrentEnvDict['web' + strAppVer]['browserName'] = self.BrowserName.get()
                oCurrentEnvDict['web' + strAppVer]['loginURL'] = self.URL.get()
            
        oGlobalDict['listOfEnvironments'][self.Environment.get()] = oCurrentEnvDict
        oJsonDict['globalVariables'] = oGlobalDict
        
        #Write back the JSON to the GlobalVar.JSON
        strJson = open(strGlobVarFilePath, mode='w+')
        #strDict = json.dumps(oJsonDict, indent=4, sort_keys=True)
        #print(str(strDict))
        strJson.write(json.dumps(oJsonDict, indent=4, sort_keys=True))
        strJson.close()
        
        if not ('ZIGBEE' in self.APIValidation.get().upper() or 'WEB' in self.MainClient.get().upper()):
            subprocess.call('killall node', shell=True)               
            subprocess.Popen(striOSAppiumConnectionString, shell=True)
            
        if 'ANDROID' in self.MainClient.get().upper():
            #subprocess.call('adb kill-server', shell=True)
            #subprocess.call('adb start-server', shell=True) 
            print()
        time.sleep(5)
        
        if self.TestSuite.get() == 'BasicSmokeTest_Dual':
            self.ExecutionThread = threading.Thread(target=self.trigger_test_run)
            self.ExecutionThread.daemon = True # This kills the thread when main program exits
            self.ExecutionThread.start()
                    
        elif self.TestSuite.get() == 'BasicSmokeTest_Heating':            
            subprocess.Popen("behave --tags=BasicSmokeTest --tags=Heating", shell=True)        
        elif self.TestSuite.get() == 'BasicSmokeTest_HotWater':            
            subprocess.Popen("behave --tags=BasicSmokeTest --tags=HotWater", shell=True)
        elif self.TestSuite.get() == 'ScheduleTest_Dual':
            subprocess.Popen("behave --tags=ScheduleTest --tags=Verify", shell=True)
        elif self.TestSuite.get() == 'ScheduleTest_Heating':
            subprocess.Popen("behave --tags=ScheduleTest --tags=Verify --tags=Heating", shell=True)
        elif self.TestSuite.get() == 'ScheduleTest_HotWater':
            subprocess.Popen("behave --tags=ScheduleTest --tags=Verify --tags=HotWater", shell=True)
        print('Test suite Triggered')
    
    #triggers the test run for a selected kit
    def trigger_test_run(self):
        if not ('ZIGBEE' in self.APIValidation.get().upper() or 'WEB' in self.MainClient.get().upper()):
            subprocess.call('killall node', shell=True)               
            subprocess.Popen(striOSAppiumConnectionString, shell=True)
            
        if 'ANDROID' in self.MainClient.get().upper():
            subprocess.call('adb kill-server', shell=True)
            subprocess.call('adb start-server', shell=True) 
            print()
        time.sleep(5)
        strTestSuite = utils.getAttribute("common", 'test_suite')
        if strTestSuite == 'BasicSmokeTest_Dual':
            oProcess = subprocess.Popen("behave --tags=BasicSmokeTest", stdout=subprocess.PIPE, shell=True) 
        elif strTestSuite == 'BasicSmokeTest_Heating':            
            oProcess = subprocess.Popen("behave --tags=BasicSmokeTest --tags=Heating", stdout=subprocess.PIPE, shell=True)        
        elif strTestSuite == 'BasicSmokeTest_HotWater':            
            oProcess = subprocess.Popen("behave --tags=BasicSmokeTest --tags=HotWater", stdout=subprocess.PIPE, shell=True)
        elif strTestSuite == 'ScheduleTest_Dual':
            oProcess = subprocess.Popen("behave --tags=ScheduleTest --tags=Verify", stdout=subprocess.PIPE, shell=True)
        elif strTestSuite == 'ScheduleTest_Heating':
            oProcess = subprocess.Popen("behave --tags=ScheduleTest --tags=Verify --tags=Heating", stdout=subprocess.PIPE, shell=True)
        elif strTestSuite == 'ScheduleTest_HotWater':
            oProcess = subprocess.Popen("behave --tags=ScheduleTest --tags=Verify --tags=HotWater", stdout=subprocess.PIPE, shell=True)
        elif strTestSuite == 'Test_Batch':
            oProcess = subprocess.Popen("behave --tags=Test_Batch", stdout=subprocess.PIPE, shell=True)
        print('Test suite Triggered')
        while True:
            output = oProcess.stdout.readline()
            if oProcess.poll() is not None:
                break
            if output:
                print(output)
        print("@@@@@@@@@@@Successfully completed", output)  
    
    def set_global_var(self):
        strEnvironmentFolderPAth = os.path.abspath(__file__ + "/../../../") + "/02_Manager_Tier/EnviromentFile"        
        strGlobVarFilePath = strEnvironmentFolderPAth + '/GlobalVar.json'    
        strJson = open(strGlobVarFilePath, mode='r')
        oJsonDict = json.loads(strJson.read())
        strJson.close()    
        utils.oJsonDict = oJsonDict
    
    def validate_kit_login(self):
        intKitIndex = 0
        for oKit in self.oKitID.get(0, END): 
            current_batch_id, current_kit_id = self.get_selected_batch_kit()
            oJsonDict = self.get_kit_batch_json()
            oKitDict = oJsonDict["kit_batch"]['list_of_batches'][current_batch_id]['list_of_kits'][oKit]
            
            if 'userName' in oKitDict and 'password' in oKitDict:
                strEnvironment = oKitDict['currentEnvironment']
                strUserName = oKitDict['userName']
                strPassword = oKitDict['password']
                ALAPI.createCredentials(strEnvironment, username = strUserName, password = strPassword)
                self.session = ALAPI.sessionObject()
                if self.session.statusCode != 200:
                    resp =self.session.response
                    if isinstance(resp, str): resp = json.loads(resp)
                    self.oKitID.itemconfig(intKitIndex, {'fg':'red'})
                else:
                    self.oKitID.itemconfig(intKitIndex, {'fg':'green'})
            intKitIndex = intKitIndex + 1
            
    #BatchExecutioin 
    def trigger_batch_execution(self):
        self.current_batch_id, self.current_kit_id = self.get_selected_batch_kit()
        self.current_batch_id_index = self.oKitBatchID.curselection()[0]
        self.validate_kit_login()
        self.update()
        #Reading all data from GlobalVar.Json
        strClickedButton = askquestion('Execute','Are you sure you want to Execute the selected Batch : '  + self.get_selected_batch_kit()[0], parent = self, default = YES, icon = WARNING)    
        if 'NO' in strClickedButton.upper():
            self.window.focus_set()
            return       
        
        #start main thread
        self.ExecuteBatchMainThread = threading.Thread(target=self.thread_execute_kitlist)
        self.ExecuteBatchMainThread.daemon = True # This kills the thread when main program exits
        self.ExecuteBatchMainThread.start()
         
        
    #Thread that iterates through the list of kits and triggers the execution for that kit
    def thread_execute_kitlist(self):
        intKitIndex = 0
        for oKit in self.oKitID.get(0, END):
            self.oKitBatchID.select_set(self.current_batch_id_index)
            self.load_kits_to_list(None, False)
            self.oKitID.select_set(intKitIndex)
            self.load_kit_details(None)
            self.update_gloabalVar_json()
            #Trigger the test execution for the Kit
            self.trigger_test_run()
            
            intKitIndex = intKitIndex + 1
            
            
    #Sub thread to trigger the execution 
    def thread_execute_selected_kit(self):
        print()
    
    #Function to execute the batch kits for the Build Pipeline
    def build_execute_kitlist(self):        
        oBKitJsonDict = self.get_kit_batch_json()
        current_batch_id = oBKitJsonDict["kit_batch"]['current_batch_id']
        oKitList = oBKitJsonDict["kit_batch"]['list_of_batches'][current_batch_id]['list_of_kits']
        for current_kit_id in oKitList:
            self.update_gloabalVar_json()
            #Trigger the test execution for the Kit
            self.trigger_test_run()
            
        
        
    #Updated the GlobalVarJson According to the Selected Kit
    def update_gloabalVar_json(self, current_batch_id = None, current_kit_id = None):
        strEnvironmentFolderPAth = os.path.abspath(__file__ + "/../../../") + "/02_Manager_Tier/EnviromentFile/"        
        strGlobVarFilePath = strEnvironmentFolderPAth + '/GlobalVar.json'
        strJson = open(strGlobVarFilePath, mode='r')
        oGBVJsonDict = json.loads(strJson.read())
        strJson.close()
        
        oGlobalDict = oGBVJsonDict['globalVariables']
        if current_batch_id == None or current_kit_id == None: current_batch_id, current_kit_id = self.get_selected_batch_kit()
        
        if current_batch_id != "" and current_kit_id != "":
            oJsonDict = self.get_kit_batch_json()
            oKitDetails = oJsonDict["kit_batch"]['list_of_batches'][current_batch_id]['list_of_kits'][current_kit_id]
            oGlobalDict['currentEnvironment'] = oKitDetails['currentEnvironment']
            oGlobalDict['apiValidationType'] = oKitDetails['apiValidationType']
            oGlobalDict['mainClient'] = oKitDetails['mainClient']['name']
            strAppVer = oKitDetails['currentAppVersion']
            oGlobalDict['currentAppVersion'] = strAppVer
            oGlobalDict['userName'] = oKitDetails['userName']
            oGlobalDict['password'] = oKitDetails['password']
            #oKitDetails['resultFolderLabel'] = "" # self.Environment.get()
            oCurrentEnvDict = oGlobalDict['listOfEnvironments'][oKitDetails['currentEnvironment']]
            
            if 'IOS' in oKitDetails['mainClient']['name'].upper():
                oCurrentEnvDict['iOS' + strAppVer]['appFileName'] = oKitDetails['mainClient']['appFileName']
                oCurrentEnvDict['iOS' + strAppVer]['deviceName'] = oKitDetails['mainClient']['deviceName']
                oCurrentEnvDict['iOS' + strAppVer]['udid'] = oKitDetails['mainClient']['udid']
                oCurrentEnvDict['iOS' + strAppVer]['platformVersion'] = oKitDetails['mainClient']['platformVersion']
            elif 'ANDROID' in oKitDetails['mainClient']['name'].upper():
                oCurrentEnvDict['android' + strAppVer]['appFileName'] = oKitDetails['mainClient']['appFileName']
                oCurrentEnvDict['android' + strAppVer]['deviceName'] = oKitDetails['mainClient']['deviceName']
                oCurrentEnvDict['android' + strAppVer]['platformVersion'] = oKitDetails['mainClient']['platformVersion']
            elif 'WEB' in oKitDetails['mainClient']['name'].upper():
                oCurrentEnvDict['web' + strAppVer]['browserName'] = oKitDetails['mainClient']['browserName']
                oCurrentEnvDict['web' + strAppVer]['loginURL'] = oKitDetails['mainClient']['loginURL']
            
            '''oKitDetails['secondClient'] = {}
            oKitDetails['secondClient']['name'] = self.MainClient.get()
            oKitDetails['secondClient']['browserName'] = ""
            oKitDetails['secondClient']['loginURL'] = ""
            '''
            oGlobalDict['listOfEnvironments'][self.Environment.get()] = oCurrentEnvDict
            oGBVJsonDict['globalVariables'] = oGlobalDict
            
            oGlobalDict['test_suite'] = oKitDetails['test_suite']
            #Write back the JSON to the GlobalVar.JSON
            oJson = open(strGlobVarFilePath, mode='w+')
            oJson.write(json.dumps(oGBVJsonDict, indent=4, sort_keys=True))
            oJson.close()
        
    def browse_app_file(self):
        if self.MainClient.get().split()[0] == 'Android' : oAppExt = ("APK", "*.apk")
        else: oAppExt = ("IPA", "*.ipa")
        strAPPFolderPAth = os.path.abspath(__file__ + "/../../../") + "/02_Manager_Tier/EnviromentFile/Apps/" + self.MainClient.get().split()[0] + '/' + self.Environment.get().split()[0]
        strFilePath = askopenfilename(filetypes=[oAppExt], initialdir=strAPPFolderPAth, title="Select the Android APK file")        
        strFileName = ntpath.split(strFilePath)[1]
        if not strFileName is "":
            oAppFileList = []
            oAllFileList = os.listdir(strAPPFolderPAth)
            #if strFileName not in oAllFileList:
            if ntpath.split(strFilePath)[0] != strAPPFolderPAth:
                shutil.copy(strFilePath, strAPPFolderPAth)
            for strFile in oAllFileList:    
                if os.path.splitext(strFile)[1].upper() == '.' + oAppExt[0]:
                    oAppFileList.append(strFile)
            oAppFileTuple = tuple(oAppFileList)
            self.oAppFilePath['value'] = oAppFileTuple
            self.oAppFilePath.set(strFileName)
        self.focus_force()
            
    def api_selected_item_event(self, event):
        print(self.APIValidation.get())
        self.load_platformAPI_controls()    
        self.load_app_details(None)
    

            
        
root = Tk()
UIClass(root).pack()
root.mainloop()
