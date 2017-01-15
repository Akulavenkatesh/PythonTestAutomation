import copy
import json
import os
from sys import executable
from tkinter import *
from tkinter import font
from tkinter import ttk, Text
from tkinter.messagebox import showinfo
from tkinter.ttk import Style

import FF_alertmeApi as ALAPI
import FF_utils as utils


class UIClass(Frame):
    
    
    def __init__(self, parent):
        self.set_global_var()
        self.oKitCombinBasedOnSel = [('All')]
        self.window = parent
        parent.title("Hive Test Automation - KIT Manager")
        parent.configure(background='#F4FFFF')
        self.position_window(parent,w=1085, h=500)
        
        self.oKitCombinationList = [('Nano2', 'SLR2', 'SLT3'), ('Nano2', 'SLR1', 'SLT3'), ('Nano2', 'SLR2', 'SLT2'), ('Nano2', 'SLR1', 'SLT2'),
                                                   ('Nano1', 'SLR2', 'SLT3'), ('Nano1', 'SLR1', 'SLT3'), ('Nano1', 'SLR2', 'SLT2'), ('Nano1', 'SLR1', 'SLT2'),('Nano1', 'SLT1')]
        Frame.__init__(self, parent)
        
        #Frame1
        self.titleFrame = ttk.Frame(self, padding="430 10 0 10")
        self.titleFrame.configure(style='TFrame')
        self.titleFrame.grid(column=0, row=0, sticky=(N,E))
        self.titleFrame.columnconfigure(0, weight=1)
        self.titleFrame.rowconfigure(0, weight=1)#Frame1
        self.titleFrame1 = ttk.Frame(self, padding="0 10 440 10")
        self.titleFrame1.configure(style='TFrame')
        self.titleFrame1.grid(column=1, row=0, sticky=(N, W))
        self.titleFrame1.columnconfigure(0, weight=1)
        self.titleFrame1.rowconfigure(0, weight=1)
        #Frame2
        self.EnvFrame = ttk.Frame(self, padding="47 0 48 5")
        self.EnvFrame.configure(style='TFrame')
        self.EnvFrame.grid(column=0, row=1, sticky=(W, N))
        self.EnvFrame.columnconfigure(0, weight=1)
        self.EnvFrame.rowconfigure(0, weight=1)
        #Frame2
        self.selectFrame = ttk.Frame(self, padding="20 10 59 58")
        self.selectFrame.configure(style='TFrame')
        self.selectFrame.grid(column=0, row=2, sticky=(W, N))
        self.selectFrame.columnconfigure(0, weight=1)
        self.selectFrame.rowconfigure(0, weight=1)
        #Frame3
        self.resultHeadFrame = ttk.Frame(self, padding="0 10 100 0")
        self.resultHeadFrame.configure(style='TFrame')
        self.resultHeadFrame.grid(column=1, row=1, sticky=(N, W))
        self.resultHeadFrame.columnconfigure(0, weight=1)
        self.resultHeadFrame.rowconfigure(0, weight=1)
        #Frame3
        self.resultFrame = ttk.Frame(self, padding="10 10 10 10")
        self.resultFrame.configure(style='TFrame')
        self.resultFrame.grid(column=1, row=2, sticky=(N, W))
        self.resultFrame.columnconfigure(0, weight=1)
        self.resultFrame.rowconfigure(0, weight=1)
        
        #Main Heading
        self.appHighlightFont = font.Font(family='Helvetica', size=22, weight='bold')
        ttk.Label(self.titleFrame, text='Get Kit', font=self.appHighlightFont).grid(column=3, row=0)
        ttk.Label(self.titleFrame1, text='Combination', font=self.appHighlightFont).grid(column=3, row=0)
        
        #Environment        
        self.oKitCombo = None
        self.EnvironmentMW = StringVar()
        a = Radiobutton(self.EnvFrame, text='isopInternProd', padx = 15, activebackground = 'Lawn Green', highlightcolor='green', variable=self.EnvironmentMW, value='isopInternProd', indicatoron=0, command=self.load_users_env_select)
        a.grid(column=1, row=0)
        Radiobutton(self.EnvFrame, text='isopBeta', padx = 15, variable=self.EnvironmentMW, value='isopBeta', indicatoron=0, command=self.load_users_env_select).grid(column=3, row=0)
        Radiobutton(self.EnvFrame, text='isopStaging', padx = 15, variable=self.EnvironmentMW, value='isopStaging', indicatoron=0, command=self.load_users_env_select).grid(column=4, row=0)
        Radiobutton(self.EnvFrame, text='isopProd', padx = 15, variable=self.EnvironmentMW, value='isopProd', indicatoron=0, command=self.load_users_env_select).grid(column=5, row=0)
        #self.oIntProd.state(['selected'])
       
        intCombWidth = 12
        #Sub Heading         
        #ttk.Label(self.selectFrame, text=' ').grid(column=1, row=1, sticky=E)
        self.subHeadFont = font.Font(family='Helvetica', size=12, weight='bold')
        
        #HUBs
        #Nano2
        ttk.Label(self.selectFrame, text='Nano2', font=self.subHeadFont).grid(row=3,column=5)# , sticky=W)
        self.Nano2Check = StringVar()
        self.oNano2Check = Checkbutton(self.selectFrame, variable=self.Nano2Check, command = self.getKitCombination)
        self.oNano2Check.grid(row=4, column=4)
        self.oNano2Check.select()        
        
        self.Nano2FW = StringVar()
        self.oNano2FW = Listbox(self.selectFrame, listvariable=self.Nano2FW, width = intCombWidth, height =4, exportselection = False)
        self.oNano2FW.bind('<<ListboxSelect>>', self.load_users) 
        self.oNano2FW.grid(row=4, column=5)
        self.oNano2FW.insert(0, "All") 
        self.oNano2FW.insert(1, "4283") 
        self.oNano2FW.insert(2, "4302") 
        self.oNano2FW.select_set(0)
        
        #self.oNano2FW['values'] = ('All', '4283', '4253')
        #self.oNano2FW.set('All')
        ttk.Label(self.selectFrame, text='    ').grid(column=6, row=3, sticky=E)
                
        #Nano1
        ttk.Label(self.selectFrame, text='Nano1', font=self.subHeadFont).grid(row=3, column=9)
        self.Nano1Check = StringVar()
        self.oNano1Check = Checkbutton(self.selectFrame, variable=self.Nano1Check, command = self.getKitCombination)
        self.oNano1Check.grid(row=4, column=8)
        self.oNano1Check.select()
        self.Nano1FW = StringVar()
        self.oNano1FW = Listbox(self.selectFrame, listvariable=self.Nano1FW, width = intCombWidth, height =4, exportselection = False)
        self.oNano1FW.bind('<<ListboxSelect>>', self.load_users) 
        self.oNano1FW.grid(row=4, column=9)
        self.oNano1FW.insert(0, "All") 
        self.oNano1FW.insert(1, "4251") 
        self.oNano1FW.insert(2, "4283") 
        self.oNano1FW.select_set(0)
        #self.oNano1FW['values'] = ('All', '4251', '4302')
        #self.oNano1FW.set('All')
        ttk.Label(self.selectFrame, text='    ').grid(row=3, column=10, sticky=E)
        ttk.Label(self.selectFrame, text='    ').grid(row=5, column=10, sticky=E)
   
        
        
        #BMs
        #SLR2
        ttk.Label(self.selectFrame, text='SLR2', font=self.subHeadFont).grid(row=6,column=5)
        self.SLR2Check = StringVar()
        self.oSLR2Check = Checkbutton(self.selectFrame, variable=self.SLR2Check, command = self.getKitCombination)
        self.oSLR2Check.grid(row=7, column=4)
        self.oSLR2Check.select()                
        self.SLR2FW = StringVar()
        self.oSLR2FW = Listbox(self.selectFrame, listvariable=self.SLR2FW, width = intCombWidth, height =4, exportselection = False)
        self.oSLR2FW.bind('<<ListboxSelect>>', self.load_users) 
        self.oSLR2FW.grid(row=7, column=5)
        self.oSLR2FW.insert(0, "All") 
        self.oSLR2FW.insert(1, "07114640") 
        self.oSLR2FW.insert(2, "07064640") 
        self.oSLR2FW.select_set(0)
        #self.oSLR2FW['values'] = ('All', '4283', '4253')
        #self.oSLR2FW.set('All')
                
        #SLR1
        ttk.Label(self.selectFrame, text='SLR1', font=self.subHeadFont).grid(row=6, column=9)
        self.SLR1Check = StringVar()
        self.oSLR1Check = Checkbutton(self.selectFrame, variable=self.SLR1Check, command = self.getKitCombination)
        self.oSLR1Check.grid(row=7, column=8)
        self.oSLR1Check.select()
        self.SLR1FW = StringVar()
        self.oSLR1FW = Listbox(self.selectFrame, listvariable=self.SLR1FW, width = intCombWidth, height =4, exportselection = False)
        self.oSLR1FW.bind('<<ListboxSelect>>', self.load_users) 
        self.oSLR1FW.grid(row=7, column=9)
        self.oSLR1FW.insert(0, "All") 
        self.oSLR1FW.insert(1, "07114640") 
        self.oSLR1FW.insert(2, "07064640") 
        self.oSLR1FW.select_set(0)
        #self.oSLR1FW['values'] = ('All', '4251', '4302')
        #self.oSLR1FW.set('All')
        ttk.Label(self.selectFrame, text='    ').grid(row=3, column=10, sticky=E)
        ttk.Label(self.selectFrame, text='    ').grid(row=8, column=10, sticky=E)
        
        #Thermostats
        #SLT3
        ttk.Label(self.selectFrame, text='SLT3', font=self.subHeadFont).grid(row=9,column=5)
        self.SLT3Check = StringVar()
        self.oSLT3Check = Checkbutton(self.selectFrame, variable=self.SLT3Check, command = self.getKitCombination)
        self.oSLT3Check.grid(row=10, column=4)
        self.oSLT3Check.select()                
        self.SLT3FW = StringVar()
        self.oSLT3FW = Listbox(self.selectFrame, listvariable=self.SLT3FW, width = intCombWidth, height =4, exportselection = False)
        self.oSLT3FW.bind('<<ListboxSelect>>', self.load_users) 
        self.oSLT3FW.grid(row=10, column=5)
        self.oSLT3FW.insert(0, "All") 
        self.oSLT3FW.insert(1, "02100203") 
        self.oSLT3FW.insert(2, "02080203") 
        self.oSLT3FW.select_set(0)
        #self.oSLT3FW['values'] = ('All', '02100203', '02080203')
        #self.oSLT3FW.set('All')
                
        #SLT2
        ttk.Label(self.selectFrame, text='SLT2', font=self.subHeadFont).grid(row=9, column=9)
        self.SLT2Check = StringVar()
        self.oSLT2Check = Checkbutton(self.selectFrame, variable=self.SLT2Check, command = self.getKitCombination)
        self.oSLT2Check.grid(row=10, column=8)
        self.oSLT2Check.select()
        self.SLT2FW = StringVar()
        self.oSLT2FW = Listbox(self.selectFrame, listvariable=self.SLT2FW, width = intCombWidth, height =4, exportselection = False)
        self.oSLT2FW.bind('<<ListboxSelect>>', self.load_users) 
        self.oSLT2FW.grid(row=10, column=9)
        self.oSLT2FW.insert(0, "All") 
        self.oSLT2FW.insert(1, "05115300") 
        self.oSLT2FW.insert(2, "05105300") 
        self.oSLT2FW.select_set(0)
        #self.oSLT2FW['values'] = ('All', '05115300', '05105300')
        #self.oSLT2FW.set('All')
        ttk.Label(self.selectFrame, text='    ').grid(row=3, column=10, sticky=E)
        
        #SLT1
        ttk.Label(self.selectFrame, text='SLT1', font=self.subHeadFont).grid(row=9, column=13)
        self.SLT1Check = StringVar()
        self.oSLT1Check = Checkbutton(self.selectFrame, variable=self.SLT1Check, command = self.getKitCombination)
        self.oSLT1Check.grid(row=10, column=12)
        self.oSLT1Check.select()
        self.SLT1FW = StringVar()
        self.oSLT1FW = Listbox(self.selectFrame, listvariable=self.SLT1FW, width = intCombWidth, height =4, exportselection = False)
        self.oSLT1FW.bind('<<ListboxSelect>>', self.load_users) 
        self.oSLT1FW.grid(row=10, column=13)
        self.oSLT1FW.insert(0, "All") 
        self.oSLT1FW.insert(1, "4.7") 
        self.oSLT1FW.insert(2, "4.8") 
        self.oSLT1FW.select_set(0)
        #self.oSLT1FW['values'] = ('All', '4.7')
        #self.oSLT1FW.set('All')
        
        
        self.DeviceFWCheckDict = {'NANO2': self.oNano2FW, 'NANO1': self.oNano1FW,
                                             'SLR2': self.oSLR2FW, 'SLR1': self.oSLR1FW,
                                             'SLT3': self.oSLT3FW, 'SLT2': self.oSLT2FW, 'SLT1': self.oSLT1FW}
        
        #Kit Combination List box
        ttk.Label(self.resultHeadFrame, text='           Kit Combination', font=self.subHeadFont).grid(row=1,column=1)
        self.oKitCombo = Listbox(self.resultFrame, selectmode='multiple', 
                                 exportselection = False, height=23)        
        self.oKitCombo.grid(column=1, row=1, sticky=(N,W))
        self.oKitCombo.bind('<<ListboxSelect>>', self.load_users)        
        ttk.Label(self.resultFrame, text=' ').grid(column=2, row=1, sticky=E)
        
        #Matching Users List Box
        ttk.Label(self.resultHeadFrame, text='                           Matching Users', font=self.subHeadFont).grid(row=1,column=3)
        self.oMatchingUsers = Listbox(self.resultFrame, selectmode='EXTENDED', 
                                      exportselection = False, height=23)        
        self.oMatchingUsers.grid(column=3, row=1, sticky=(N,W))
        self.oMatchingUsers.bind('<<ListboxSelect>>', self.sampPrint)
        self.oMatchingUsers.insert(0, "hi")            
        
        ttk.Label(self.resultFrame, text=' ').grid(column=4, row=1, sticky=E)
        
        ttk.Label(self.resultHeadFrame, text='                                            Response', font=self.subHeadFont).grid(row=1,column=5)
        #Respose and Load Scroll bars
        xscrollbar = Scrollbar(self.resultFrame, orient=HORIZONTAL)
        xscrollbar.grid(row=1, column=5, sticky=E+W)        
        yscrollbar = Scrollbar(self.resultFrame)
        yscrollbar.grid(row=1, column=5, sticky=E+W)
        self.OutPut = Text(self.resultFrame, width = 30, height = 26, wrap=NONE, bd=0,
                    xscrollcommand=xscrollbar.set,
                    yscrollcommand=yscrollbar.set)
        self.OutPut.pack()
        self.OutPut.grid(column=5, row=1, sticky=(N,W))
        xscrollbar.config(command=self.OutPut.xview)
        yscrollbar.config(command=self.OutPut.yview)
        
        ttk.Label(self.selectFrame, text=' ').grid(column=4, row=11, sticky=E)
        oMangeUsers = ttk.Button(self.selectFrame, text='Manage Users', command=self.create_window, width=11)
        oMangeUsers.grid(column=5, row=12)
        '''
        oExecute = ttk.Button(self.resultFrame, text='Quit1', command=lambda: self.create_window(None))
        oExecute.grid(column=18, row=15, sticky=E)
        '''
        self.getKitCombination()
        
    def getKitCombination(self):
        self.oKitCombinBasedOnSel = copy.deepcopy(self.oKitCombinationList)
        #self.oKitCombinBasedOnSel = self.oKitCombinationList
        self.oKitCombo.delete(0, END)
        if self.Nano2Check.get() == '0': 
            self.unloadKitCombo('Nano2')
            self.oNano2FW.config(state=DISABLED)
        else: self.oNano2FW.config(state=NORMAL)
        
        if self.Nano1Check.get() == '0': 
            self.unloadKitCombo('Nano1')
            self.oNano1FW.config(state=DISABLED)
        else: self.oNano1FW.config(state=NORMAL)
        
        if self.SLT3Check.get() == '0': 
            self.unloadKitCombo('SLT3')
            self.oSLT3FW.config(state=DISABLED)
        else: self.oSLT3FW.config(state=NORMAL)
        
        if self.SLT2Check.get() == '0': 
            self.unloadKitCombo('SLT2')
            self.oSLT2FW.config(state=DISABLED)
        else: self.oSLT2FW.config(state=NORMAL)
        
        if self.SLR2Check.get() == '0': 
            self.unloadKitCombo('SLR2')
            self.oSLR2FW.config(state=DISABLED)
        else: self.oSLR2FW.config(state=NORMAL)
        
        if self.SLR1Check.get() == '0': 
            self.unloadKitCombo('SLR1')
            self.oSLR1FW.config(state=DISABLED)
        else: self.oSLR1FW.config(state=NORMAL)
        
        if self.SLT1Check.get() == '0': 
            self.unloadKitCombo('SLT1')
            self.oSLT1FW.config(state=DISABLED)
        else: self.oSLT1FW.config(state=NORMAL)
        
        intCntr = 1
        if len(self.oKitCombinBasedOnSel) > 1: self.oKitCombo.insert(0, 'All')
        for oKitCombo in self.oKitCombinBasedOnSel:
            if len(oKitCombo) >2:
                strComb = oKitCombo[0] + '<>' + oKitCombo[1] + '<>' + oKitCombo[2] 
            else: 
                strComb = oKitCombo[0] + '<>' + oKitCombo[1] 
            
            self.oKitCombo.insert(intCntr, strComb)
            intCntr = intCntr +1
        self.load_users(None)
        
    def unloadKitCombo(self, strDevice):
        for oKitCombo in self.oKitCombinationList:
            if strDevice in oKitCombo: 
                if oKitCombo in self.oKitCombinBasedOnSel: 
                    self.oKitCombinBasedOnSel.remove(oKitCombo)
    
    
    def sampPrint(self, event):
        print('Sample Print')
        
    def create_window(self):
        self.window.iconify()
        self.APIWindow = Toplevel(self.window)
        self.APIWindow.wm_title("Hive Test Automation - Manage Users & Kits")
        self.position_window(self.APIWindow,w=920, h=500)
        #l = ttk.Label(t, text="This is window #%s" % self.counter)
        #l.pack(side="top", fill="both", expand=True, padx=100, pady=100)
        
        Frame.__init__(self, self.APIWindow)
        
        '''
        #Style - Background color
        s = ttk.Style()
        #s.configure('.', background='black')
        
        ttk.Style().configure("TButton", padding=6, relief="flat", bg='#000000',
                fg='#b7f731',background="pale green")
        '''
        
        
        #Frame1
        self.mainframe = ttk.Frame(self.APIWindow, padding="50 10 30 255")
        self.mainframe.configure(style='TFrame')
        self.mainframe.grid(column=0, row=0, sticky=(N))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        #Frame2
        self.resposeFrame = ttk.Frame(self.APIWindow, padding="10 10 10 10")
        self.resposeFrame.configure(style='TFrame')
        self.resposeFrame.grid(column=1, row=0, sticky=(N, W, E, S))
        self.resposeFrame.columnconfigure(0, weight=1)
        self.resposeFrame.rowconfigure(0, weight=1)
        
        #Variables    
        self.Environment = StringVar()
        self.APIValidation = StringVar()
        self.UserName = StringVar()
        self.Password = StringVar()
        self.Response = StringVar()
        self.EndPoint = StringVar()
        self.Node = StringVar()
                
        self.appHighlightFont = font.Font(family='Helvetica', size=22, weight='bold')
        ttk.Label(self.mainframe, text='Get', font=self.appHighlightFont).grid(column=3, row=0, sticky=E)
        ttk.Label(self.mainframe, text='API Response', font=self.appHighlightFont).grid(column=15, row=0, sticky=W)
        
        #Environment
        ttk.Label(self.mainframe, text='Environment:    ').grid(column=3, row=1, sticky=E)
        self.oEnvironment = ttk.Combobox(self.mainframe, textvariable=self.Environment)
        self.oEnvironment['values'] = ('isopInternProd', 'isopBeta', 'isopStaging', 'isopProd')
        self.oEnvironment.state(['readonly'])
        self.oEnvironment.set('isopInternProd')
        self.oEnvironment.grid(column=15, row=1, sticky=W)
        
        #User Name
        self.lblUserName = ttk.Label(self.mainframe, text='User Name:    ')
        self.lblUserName.grid(column=3, row=3, sticky=E)
        self.oUserName = ttk.Combobox(self.mainframe, textvariable=self.UserName)
        self.oUserName['values'] = ('auto1_v6', 'tester2', 'tester4_v6')
        self.oUserName.set(utils.getAttribute('common', 'userName'))
        self.oUserName.grid(column=15, row=3, sticky=W)
        
        #Password
        self.lblPassword = ttk.Label(self.mainframe, text='Password:    ')
        self.lblPassword.grid(column=3, row=4, sticky=E)
        self.oPassword = ttk.Combobox(self.mainframe, textvariable=self.Password)
        self.oPassword['values'] = ('password1', 'Password1', 'passw0rd')
        self.oPassword.set(utils.getAttribute('common', 'password'))
        self.oPassword.grid(column=15, row=4, sticky=W)
        self.boolUserPassDestroyed = False
        
        
       
        #Respose and Load Scroll bars
        xscrollbar = Scrollbar(self.resposeFrame, orient=HORIZONTAL)
        xscrollbar.grid(row=2, column=17, sticky=E+W)        
        yscrollbar = Scrollbar(self.resposeFrame)
        yscrollbar.grid(row=2, column=17, sticky=N+S)
        self.Response = Text(self.resposeFrame, width = 70, height = 30, wrap=NONE, bd=0,
                    xscrollcommand=xscrollbar.set,
                    yscrollcommand=yscrollbar.set)
        self.Response.pack()
        self.Response.grid(column=17, row=2, sticky=W)
        xscrollbar.config(command=self.Response.xview)
        yscrollbar.config(command=self.Response.yview)
        
        #Exucute & Quit Buttons
        ttk.Label(self.mainframe, text='').grid(column=3, row=14, sticky=E)
        ttk.Label(self.mainframe, text='').grid(column=15, row=14, sticky=E)
        oExecute = ttk.Button(self.mainframe, text='Execute', command= self.load_response)
        oExecute.grid(column=3, row=15, sticky=E)       
        oExecute = ttk.Button(self.mainframe, text='Add Kit', command= self.updateGlobalVarJson)
        oExecute.grid(column=15, row=15, sticky=W)       
        oExecute = ttk.Button(self.mainframe, text='Quit', command=lambda: self.closeWidget(self.APIWindow))
        oExecute.grid(column=15, row=15, sticky=E)
        
        
    def load_response(self):
        self.Response.delete(1.0, END) 
        self.reponseJson = self.get_response()
        self.Response.insert(1.0, json.dumps(self.reponseJson, indent=4, sort_keys=False))
        if self.session.statusCode == 200:
            ALAPI.deleteSessionV6(self.session)
        
        showinfo("Hive Test Automation","User & Kit details loaded")
    
    def set_default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        raise TypeError


    def get_response(self):
        ALAPI.createCredentials(self.Environment.get(), username = self.UserName.get(), password = self.Password.get())
        self.session = ALAPI.sessionObject()
        if self.session.statusCode != 200:
            resp =self.session.response
            if isinstance(resp, str): resp = json.loads(resp)
            return resp
        if self.session.latestSupportedApiVersion != '6':
            self.platformVersion = 'V5'
            print("hello")
            self.Response.insert(1.0, 'User is V5. Retry with V6 User')
            return False
        else:
            self.platformVersion = 'V6'
            
            resp = ALAPI.getNodesV6(self.session)
           
            oDeviceVersionDict = {}
            strSLTMacID = ""
            strSLRMacID = ""
            for oNode in resp['nodes']:
                if not 'supportsHotWater'  in oNode['attributes']:
                    if 'hardwareVersion' in oNode['attributes']: 
                        intHardwareVersion = oNode['attributes']['hardwareVersion']['reportedValue']
                        intSoftwareVersion = oNode['attributes']['softwareVersion']['reportedValue']
                        if 'NANO' in  intHardwareVersion:
                            #oDeviceVersionDict['HUB'] = intHardwareVersion + '$$' + intSoftwareVersion
                            oDeviceVersionDict['HUB'] = {"model" : intHardwareVersion, "version" : intSoftwareVersion}
                    if 'zigBeeNeighbourTable' in oNode['attributes']:
                        for oDevice in oNode['attributes']['zigBeeNeighbourTable']['reportedValue']:
                            if oDevice['relationship'] == 'CHILD':
                                strSLTMacID = oDevice['neighbourAddress']
                            elif oDevice['relationship'] == 'NONE':
                                strSLRMacID = oDevice['neighbourAddress']
                                    
            for oNode in resp['nodes']:
                if not 'supportsHotWater'  in oNode['attributes']:
                    if 'model' in oNode['attributes']: 
                        strModel = oNode['attributes']['model']['reportedValue']
                        intSoftwareVersion = oNode['attributes']['softwareVersion']['reportedValue']                            
                        if 'SLT' in strModel: 
                            #oDeviceVersionDict['Thermostat'] = strModel + '$$' + intSoftwareVersion
                            oDeviceVersionDict['Thermostat'] = {"model" : strModel, "version" : intSoftwareVersion, 'mac_id': strSLTMacID}
                        elif'SLR' in strModel: 
                            #oDeviceVersionDict['Boiler Module'] = strModel + '$$' + intSoftwareVersion
                            oDeviceVersionDict['Boiler Module'] = {"model" : strModel, "version" : intSoftwareVersion, 'mac_id': strSLRMacID}
            oDeviceVersionDict['credentials'] = {"username": self.UserName.get(), "password":self.Password.get()}
            return oDeviceVersionDict
        
        
    def get_selected_value_from_Listbox(self, oListBox): 
        oSelectCombList = oListBox.curselection()
        if len(oSelectCombList)>0:
            if oListBox.get(oSelectCombList[0]).upper() == 'ALL':
                oSelectCombList = oListBox.get(1, END)
            else:
                oSelectKitList = []
                for oIndex in oSelectCombList:
                    oSelectKitList.append(oListBox.get(oIndex))
                oSelectCombList = oSelectKitList
        return oSelectCombList
    
    def load_users_env_select(self):
        self.load_users(None)
    
    def load_users(self, event):        
        #print(self.oNano2FW.(1))
        if self.oKitCombo is None: return
        self.oMatchingUsers.delete(0, END)
        oSelectCombList = self.get_selected_value_from_Listbox(self.oKitCombo)
        if len(oSelectCombList)>0:
            '''
            if self.oKitCombo.get(oSelectCombList[0]).upper() == 'ALL':
                oSelectCombList = self.oKitCombo.get(1, END)
            else:
                oSelectKitList = []
                for oIndex in oSelectCombList:
                    oSelectKitList.append(self.oKitCombo.get(oIndex))
                oSelectCombList = oSelectKitList
            print(oSelectCombList)
            '''
            
            strEnvironmentFolderPAth = os.path.abspath(__file__ + "/../../../") + "/02_Manager_Tier/EnviromentFile/"        
            strKitDetailsFilePath = strEnvironmentFolderPAth + '/kits_detail.json'    
            strJson = open(strKitDetailsFilePath, mode='r')
            oJsonDict = json.loads(strJson.read())
            strJson.close()
            
            print(self.EnvironmentMW.get())
            if self.EnvironmentMW.get() == '':
                
                showinfo("Hive Test Automation - KIT Manager", 'Please select the environment')
                print('Please select the environment')
                self.oKitCombo.selection_clear(0, END)
                return
            #get list of kits/users for the selected environment
            oDeviceListJson = oJsonDict['listOfEnvironments'][self.EnvironmentMW.get()]['DeviceList']
            
            for oKitComb in oSelectCombList:
                oHubFWList = []
                oBMFWList = []
                oTHFWList = []
                strHubType = ""
                strBMType = ""
                strTHFWType = ''
                oDeviceList = oKitComb.split("<>")
                strHubType = oDeviceList[0].upper()
                oHubFWList =  self.get_selected_value_from_Listbox(self.DeviceFWCheckDict[strHubType])                
                if len(oDeviceList) >2: 
                    strBMType = oDeviceList[1].upper()
                    strTHFWType = oDeviceList[2].upper()                 
                else: 
                    strTHFWType = oDeviceList[1].upper()                
                if not strBMType == '':
                    oBMFWList =  self.get_selected_value_from_Listbox(self.DeviceFWCheckDict[strBMType])      
                          
                oTHFWList =  self.get_selected_value_from_Listbox(self.DeviceFWCheckDict[strTHFWType]) 
                print(strHubType, strBMType, strTHFWType)
                
                #print(oHubFWList, oBMFWList, oTHFWList)
                oMatchingUsers = []
                for oUserKey in oDeviceListJson:
                    oUser = oDeviceListJson[oUserKey]
                    if not 'errors' in oUser:
                        print(oUser['credentials']['username'])
                        boolUserMatching = True 
                        boolUserHUbMatching =False 
                        boolUserTHMatching = False 
                        boolUserBMMatching = False     
                        #print(oUser)    
                        if 'HUB' in oUser:               
                            if oUser['HUB']['model'] == strHubType:
                                for oHUBFW in oHubFWList:
                                    if oHUBFW in oUser['HUB']['version']:
                                        boolUserHUbMatching = True                                
                                if oUser['Thermostat']['model'] == strTHFWType:
                                    for oTHFW in oTHFWList:
                                        if oTHFW in oUser['Thermostat']['version']:
                                            boolUserTHMatching = True
                                            
                                    if not ((strBMType == '') and ('Boiler Module' not in  oUser)): 
                                        if ((strBMType == '') and ('Boiler Module' in  oUser)) or ((strBMType != '') and ('Boiler Module' not in  oUser)): 
                                            boolUserMatching = False
                                        elif oUser['Boiler Module']['model'] == strBMType:
                                            for oBMFW in oBMFWList:
                                                if oBMFW in oUser['Boiler Module']['version']:
                                                    boolUserBMMatching = True
                                        else : boolUserMatching = False
                                else : boolUserMatching = False
                            else : boolUserMatching = False
                        else : boolUserMatching = False
                        
                        #print(boolUserMatching, boolUserHUbMatching,boolUserBMMatching, boolUserTHMatching )
                        if boolUserMatching and boolUserHUbMatching and boolUserTHMatching and boolUserBMMatching: oMatchingUsers.append(oUserKey)
                #print(oMatchingUsers, 'oMatchingUsers')
                for oUser in oMatchingUsers:
                    self.oMatchingUsers.insert(END, oUser)
            
                
    #Place Window on the center fo the screen
    def position_window(self, parent, w, h):
        # get screen width and height
        ws = parent.winfo_screenwidth()
        hs = parent.winfo_screenheight()
        # calculate position x, y
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        parent.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
          
    def create_combobox(self, intRow, strLabel, oStringVar, oValueList, strDefaultValue, boolReadOnly):                
        oLabel = ttk.Label(self.mainframe, text=strLabel)
        oLabel.grid(column=3, row=intRow, sticky=E)
        oCombobox = ttk.Combobox(self.mainframe, textvariable=oStringVar)
        oCombobox['values'] = oValueList
        oCombobox.set(strDefaultValue)                
        if boolReadOnly: oCombobox.state(['readonly'])
        oCombobox.grid(column=15, row=intRow, sticky=W)
        return oLabel, oCombobox
   
    def closeWidget(self, oWindow):
        #Tk().clipboard_append(self.Response.get())
        self.APIWindow.destroy()
        self.APIWindow = None
        
    def updateGlobalVarJson(self):
        #Reading all data from GlobalVar.Json
        self.load_response()
        print()
        strEnvironmentFolderPAth = os.path.abspath(__file__ + "/../../../") + "/02_Manager_Tier/EnviromentFile/"        
        strKitDetailsFilePath = strEnvironmentFolderPAth + '/kits_detail.json'    
        strJson = open(strKitDetailsFilePath, mode='r')
        oJsonDict = json.loads(strJson.read())
        strJson.close()
        
        oEnvListDict = oJsonDict['listOfEnvironments']
        strEnvironment = self.Environment.get()
        if not strEnvironment in oEnvListDict.keys():
            oEnvListDict[strEnvironment] = {}
            oEnvListDict[strEnvironment]['DeviceList'] = {}
        
        oDeviceList = oEnvListDict[strEnvironment]['DeviceList']
        
        oDeviceList[self.UserName.get()] = self.reponseJson
        
        oEnvListDict[strEnvironment]['DeviceList'] = oDeviceList
        oJsonDict['listOfEnvironments']= oEnvListDict
        
        #Write back the JSON to the GlobalVar.JSON
        strJson = open(strKitDetailsFilePath, mode='w+')
        #strDict = json.dumps(oJsonDict, indent=4, sort_keys=True)
        #print(str(strDict))
        strJson.write(json.dumps(oJsonDict, indent=4, sort_keys=True))
        strJson.close()
        
    def set_global_var(self):
        strEnvironmentFolderPAth = os.path.abspath(__file__ + "/../../../") + "/02_Manager_Tier/EnviromentFile"        
        strGlobVarFilePath = strEnvironmentFolderPAth + '/GlobalVar.json'    
        strJson = open(strGlobVarFilePath, mode='r')
        oJsonDict = json.loads(strJson.read())
        strJson.close()    
        utils.oJsonDict = oJsonDict

        
root = Tk()
UIClass(root).pack()
root.mainloop()
