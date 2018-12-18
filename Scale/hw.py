# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 17:04:47 2018

@author: Colin
"""
class hw:
    
    def __init__(self):
        self.connected = False
        self.connect()
        self.read_data()
        
    def connect(self):
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if "Fio" in p[1]: # if the device is found (by name)
                #open a xbee device on the current port
                self.serial_device = serial.Serial(p[0], 9600)
                self.connected = True
            else:
                self.connected = False
                
    def close(self):
        
        # Define function for when data is recieved
    def read_data(self):
        while self.connected:
            if self.serial_device.in_waiting:
                #update the GUI with the new value
                self.load = float(self.serial_device.readline())
        self.connect()
        return
    
        #Connect the Fio
#        ports = list(serial.tools.list_ports.comports())
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            print(p[1])
            if "Fio" in p[1]: # if the device is found (by name)
                #open a xbee device on the current port
                self.serial_device = serial.Serial(p[0], 9600)

                # update the log
                self.update_log("Arduino Connected")
                #start data collection in it's own thread
                self.thread = threading.Thread(target=self.read_data)
                self.read = True
#                self.read_data()
                self.thread.start()
                return
            else:
                self.update_log("No Arduino Found")    
                print("No Arduino Found")
                return