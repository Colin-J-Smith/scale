import tkinter
from tkinter import Tk, Label, Button, DoubleVar, StringVar
import serial
import serial.tools.list_ports

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib import style

import csv
import time

style.use("ggplot")

def connect_hw():
    #Connect the Fio
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        print(p[1])
        if "USB" in p[1]: # if the device is found (by name)
            #open a xbee device on the current port
            serial_device = serial.Serial(p[0], 9600)
            # update the log
            print("Arduino Connected")
            return serial_device
        else:
            print("No Arduino Found")
            return
    
class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Digital Load Cell")
        
#        self.shared_load = load
        self.load_array = []
        self.time_array = []

        # The load
        self.load = 0.0
        # set the data type for the load readings
        self.load_var = DoubleVar()
        # assign the init values for the load.
        self.load_var.set(self.load)
        # render the load variables to the GUI
        self.load_text = Label(master, textvariable=self.load_var)
        # render the load variables text labels to the GUI
        self.label = Label(master, text="Load (lbs)")
        self.quit_button = Button(master, text="Quit", command=self._quit)
        self.start_button = Button(master, text="Start", command=self.start)
        self.stop_button = Button(master, text="Stop", command=self.stop)
        
        # Log Display
        self.log= ''
        self.log_text = StringVar()
        self.log_text.set(self.log)
        self.log_box = Label(master, textvariable=self.log_text)

        # Graph Display        
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.plot = self.fig.add_subplot(111)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        self.toolbar = NavigationToolbar2Tk(self.canvas, root)
        self.toolbar.update()
        #add graph navigation toolbar
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        def on_key_press(event):
            print("you pressed {}".format(event.key))
            key_press_handler(event, self.canvas, self.toolbar)
        self.canvas.mpl_connect("key_press_event", on_key_press)
        
        # arrange gui
        self.label.pack()
        self.load_text.pack()
        self.start_button.pack()
        self.stop_button.pack()
        self.log_box.pack()
        self.quit_button.pack(side=tkinter.BOTTOM)
                
        self.collect = False
        self.read = True
        try:
            self.serial_device = connect_hw()
        except:
            self._quit()
        self.read_data()
        return
        
    def _quit(self):
        self.read = False
        self.serial_device.close()
        print("Arduino Disconnected")
        self.master.quit()     # stops mainloop
        self.master.destroy()  # this is necessary on Windows to prevent
        return
    
    def start(self):
        self.load_array = []
        self.time_array = []
        self.t0 = time.time()
        self.collect = True
        return

    def stop(self):
        self.collect = False
        self.save()
        # SAVE DATA TO CSV
        return
    
    def save(self):
        myData = [self.time_array, self.load_array]  
        myFile = open('data.csv', 'w')  
        with myFile:  
           writer = csv.writer(myFile)
           writer.writerows(myData)
        return
        
    def read_data(self):   
        if self.read:
            try:
                if self.serial_device.in_waiting:
                    self.load =float(self.serial_device.readline())
            except():
                print("Arduino Disconnected")
            
            self.load_var.set(self.load)
            if self.collect: # if we are collecting data
                self.time_array.append(time.time() - self.t0)
                self.load_array.append(self.load)
                self.plot.clear()
                self.plot.plot(self.time_array, self.load_array)
                self.canvas.draw()
            self.master.after(50, self.read_data) #loop for next data point

root = Tk()
my_gui = GUI(root)
root.mainloop()


# Exit Script


