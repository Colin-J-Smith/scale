import tkinter
from tkinter import Tk, Label, Button, Entry, DoubleVar, StringVar, END, W, E
import serial
import serial.tools.list_ports
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2TkAgg)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import time
import numpy as np
import threading


class PedalGUI:

    def __init__(self, master):
        self.master = master
        master.title("Pedal Force GUI")
        
        self.collect = False

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
        t = np.arange(0, 3, .01)
        self.fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        
        toolbar = NavigationToolbar2TkAgg(self.canvas, root)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        
        def on_key_press(event):
            print("you pressed {}".format(event.key))
            key_press_handler(event, self.canvas, toolbar)
        
        self.canvas.mpl_connect("key_press_event", on_key_press)
        
        self.label.pack()
        self.load_text.pack()
        self.start_button.pack()
        self.stop_button.pack()
        self.log_box.pack()
        self.quit_button.pack(side=tkinter.BOTTOM)
        
        #Connect the Fio
#        ports = list(serial.tools.list_ports.comports())
        ports = list(serial.tools.list_ports.comports())

        for p in ports:
            if "Fio" in p[1]: # if the device is found (by name)
                #open a xbee device on the current port
                self.serial_device = serial.Serial(p[0], 9600)

                # update the log
                self.update_log("Arduino Connected")
                self.thread = threading.Thread(target=self.collect_data)
                self.thread.start()
                return
            else:
                self.update_log("No Arduino Found")    
                print("No Arduino Found")
        
    def _quit(self):
        self.master.quit()     # stops mainloop
        self.master.destroy()  # this is necessary on Windows to prevent
                        # Fatal Python Error: PyEval_RestoreThread: NULL tstate
    def start(self):
        print('start')
        self.load_array = []
        self.time_array = []
        self.t0 = time.time()
        self.collect = True
        return

    def stop(self):
        print('stop')
        self.collect = False
        self.thread.exit()
        # SAVE DATA TO CSV
        return   

    # Define function for when data is recieved
    def collect_data(self):
        while True:
            if self.serial_device.in_waiting:
                #update the GUI with the new value
                self.load = float(self.serial_device.readline())
                self.load_var.set(self.load)
                
                if self.collect:
                    self.time_array.append(time.time() - self.t0)
                    self.load_array.append(self.load)
                    self.update_plot()
        return

    def update_plot(self):
        self.fig.subplots().plot(self.time_array, self.load_array)
        self.canvas.draw()
        return
        
    def update_log(self, message):
        old_msg = self.log_text.get()
        self.log_text.set(old_msg + '\r\n' + message)
        return


root = Tk()
my_gui = PedalGUI(root)
root.mainloop()

# Exit Script
my_gui.serial_device.close()

