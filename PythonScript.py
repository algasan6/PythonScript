import json
import keyboard
import datetime

from Interfaces.Ethernet.EthernetConfig import EthernetParams
from Interfaces.Ethernet.IPConnection import IPConnection
from Interfaces.Ethernet.Commands import IPCommands

import ConfigClasses as cfgCl
import matplotlib.pyplot as plt
import numpy as np
from time import time, sleep, mktime

# import paho.mqtt.client as mqttClient
import random

# from ConfigClasses import HtParams

class Main():

    def __init__(self):
        
        self.hwParams = cfgCl.HwParams()
        self.sysParams = cfgCl.SysParams()
        self.htParams = cfgCl.HtParams()
        
        self.FD_Data = cfgCl.FD_Data()
        self.TD_Data = cfgCl.TD_Data()
        self.HT_Targets = cfgCl.HtTargets()
        
        self.etherParams = EthernetParams()
        self.etherParams.ip = "192.168.0.2"
        self.etherParams.port = 1024
        self.myInterface = None
        self.interface = None
        self.connected = False
        self.error = False

    def Connect(self, interface=None):

        if interface == None:   
            self.error = True
            return

        if interface == "Ethernet":
            self.myInterface = IPConnection(self)
            
            if not self.myInterface.connect():
                print ("")
                print ("Connection to "+self.etherParams.ip+":"+str(self.etherParams.port)+" failed.")
                self.error = True
                return
            
            self.cmd = IPCommands(connection=self.myInterface, main_win=self)
        
        self.interface = interface
        self.connected = True
            
    def GetHwParams(self):

        if not self.connected or self.error:
            return
        
        try:
            self.cmd.execute_cmd("CMDID_SEND_INFO")
        except:
            print ("Error in receiving hardware parameters.")
            self.error = True
            return
        
    def GetSysParams(self):

        if not self.connected or self.error:
            return
        
        try:
            self.cmd.execute_cmd("CMDID_SEND_PARAMS")
        except:
            print ("Error in receiving system parameters.")
            self.error = True
            return
                
    def SetSysParams(self):

        if not self.connected or self.error:
            return
        
        try:
            self.cmd.execute_cmd("CMDID_SETUP")
        except:
            print ("Error in setting system parameters.")
            self.error = True
            return
            
    def GetHtParams(self):

        if not self.connected or self.error:
            return
        
        try:
            self.cmd.execute_cmd("CMDID_SEND_HT_PARAMS")
        except:
            print ("Error in receiving Human Tracker parameters.")
            self.error = True
            return

    def SetHtParams(self):

        if not self.connected or self.error:
            return
        
        try:
            self.cmd.execute_cmd("CMDID_HT_PARAMS")
        except:
            print ("Error in setting Human Tracker parameters.")
            self.error = True
            return
    
    def HtMeasurement(self):

        if not self.connected or self.error:
            return
        
        try:
            self.cmd.execute_cmd("CMDID_DO_HT")            
        except:
            print ("Error in receiving Human Tracker data.")
            self.error = True
            return
            
    def Disconnect(self):

        if not self.connected:
           return
        if self.interface == "Ethernet":
           self.myInterface.disconnect()
            
        self.connected = False

# ------------------------------------------------------ #

random = random.randint(0, 1000)

def on_connect(client, userdata, flags, rc):

        if rc == 0:
            global Connected
            Connected = True
        else:
            print("Connection failed")

# MQTT Server 

# Connected = False   
# broker_address= ""
# port = 
# user = ""
# password = ""

# print('')
# client_name = "Python" + str(random)
# print "Client name: ", client_name
# client = mqttClient.Client(client_name)
# client.username_pw_set(user, password = password)
# client.on_connect= on_connect
# client.connect(broker_address, port = port)
# client.loop_start()

# ------------------------------------------------------ #

main = Main()
interface = "Ethernet"
main.Connect(interface)

main.GetHwParams()
print ""
print "Please, wait. Measurements are about to start."
print "Radar Module: ", main.hwParams.radarNumber

print ""
print "========================="
print "Radar System Parameters"
print "========================="
print ""

main.sysParams.minFreq = 24008
main.sysParams.manualBW = 230
main.sysParams.SC_Enabled = True
main.sysParams.atten = 0
main.sysParams.band = 3
main.sysParams.t_ramp = 1
main.sysParams.zero_pad = 1
main.sysParams.norm = 0
main.sysParams.FFT_data_type = 1
main.sysParams.frontendEn = 1
main.sysParams.powerSaveEn = 0
main.sysParams.active_RX_ch = 10

main.sysParams.advanced = 0
main.sysParams.freq_points = 150
main.sysParams.tic = 0
main.sysParams.doppler = 0
main.sysParams.freq_bin = 0

print "minFreq [MHz]: ", main.sysParams.minFreq
print "manualBW [MHz]: ", main.sysParams.manualBW
print "SC_Enabled: ", main.sysParams.SC_Enabled
print "atten [dB]: ", 10*np.log10(main.sysParams.atten)
print "band: ", main.sysParams.band
print "t_ramp [ms]: ", main.sysParams.t_ramp
print "zero_pad: ", main.sysParams.zero_pad
print "norm: ", main.sysParams.norm
print "FFT_data_type: ", main.sysParams.FFT_data_type
print "frontendEn: ", main.sysParams.frontendEn
print "powerSaveEn: ", main.sysParams.powerSaveEn
print "active_RX_ch: ", main.sysParams.active_RX_ch

print "advanced: ", main.sysParams.advanced
print "freq_points [fft bins]: ", main.sysParams.freq_points
print "tic [um]: ", main.sysParams.tic
print "doppler [um/s]: ", main.sysParams.doppler
print "freq_bin [Hz]: ", main.sysParams.freq_bin

main.SetSysParams()

print ""
print "========================="
print "Human Tracker Parameters"
print "========================="
print ""

main.htParams.nRefPulses = 20
main.htParams.timeInterval = 100
main.htParams.nTargets = 1
main.htParams.overThreshold = 30
main.htParams.threshFilter = 100
main.htParams.backgrFilter = 32
main.htParams.minSeparation = 1
main.htParams.maxRangeShift = 1
main.htParams.maxLostDetect = 2
main.htParams.minDistance = 0
main.htParams.enableTracker = 0

print "nRefPulses: ", main.htParams.nRefPulses
print "timeInterval [ms]: ", main.htParams.timeInterval
print "nTargets: ", main.htParams.nTargets
print "overThreshold: ", main.htParams.overThreshold
print "threshFilter: ", main.htParams.threshFilter
print "backgrFilter: ", main.htParams.backgrFilter
print "minSeparation [bins]: ", main.htParams.minSeparation
print "maxRangeShift: ", main.htParams.maxRangeShift
print "maxLostDetect: ", main.htParams.maxLostDetect
print "minDistance [m]: ", main.htParams.minDistance
print "enableTracker: ", main.htParams.enableTracker

main.SetHtParams()

if 1:
    
    HTM = 1

    timestamp_file_name = datetime.datetime.now()
    timestamp_file_name_str = str(timestamp_file_name)
    timestamp_file_name_str = timestamp_file_name_str.replace(":","_")

    while True:

        t_start = time()
        timestamp = time()
        main.HtMeasurement()
        dt = time()-t_start

        print ("")
        print ("==================")
        print ("Measurement %d"%(HTM))
        HTM = HTM+1
        print ("Targets found: %d"%main.HT_Targets.nTargets)
        print ("")
           
        radar = {}
        radar['info'] ={
            'id': main.hwParams.radarNumber,
            'timestamp': "{:.3f}".format((timestamp)),
            'tPreMeas': main.HT_Targets.tPreMeas, 
            'tPostMeas': main.HT_Targets.tPostMeas,
            'tPreProc': main.HT_Targets.tPreProc, 
            'tPostProc': main.HT_Targets.tPostProc}

        target = []
        radar['targetvalues'] = []
        
        if main.HT_Targets.nTargets != 0:

            for m in range(main.HT_Targets.nTargets):

                target_temp = {}
                target_temp['distance'] = main.HT_Targets.dist[m]
                target_temp['angle'] =  main.HT_Targets.angle[m]
                target_temp['level'] = 20*np.log10(main.HT_Targets.level[m]/2.**21)
                target.append(target_temp)

            radar['targetvalues'] = target

        # client.publish("input/Radar/" + str(main.hwParams.radarNumber), json.dumps(radar), qos=2, retain=False)
        print(json.dumps(radar))

        with open(timestamp_file_name_str + '.json','a') as file:
            json.dump(radar,file,indent=4)

        time_interval_value = 1000

        if dt < time_interval_value:
            sleep((time_interval_value-dt)/1000.)

main.Disconnect()
print ("Ended process.")
print('')