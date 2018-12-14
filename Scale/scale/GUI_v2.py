from tkinter import Tk, Label, Button, Entry, DoubleVar, StringVar, END, W, E
from digi.xbee.devices import XBeeDevice
import serial
import serial.tools.list_ports


'''
Detect available COM ports.
Select the port with the Xbee Explorer attached
Send the initialize command to both pedal modules
Check that both pedals initialize
Wait for available serial data and report it to the GUI when it arrives.

GUI
Reset/Initialize Button
Left Pedal Load Output
Right Pedal Load Output
'''


class PedalGUI:

    def __init__(self, master):
        self.master = master
        master.title("Pedal Force GUI")

        # The load from each pedal
        self.left = 0.0
        self.right = 0.0

        # set the data type for the load readings
        self.left_load_text = DoubleVar()
        self.right_load_text = DoubleVar()

        # assign the init values for the right and left loads.
        self.left_load_text.set(self.left)
        self.right_load_text.set(self.right)

        # render the load variables to the GUI
        self.left_load = Label(master, textvariable=self.left_load_text)
        self.right_load = Label(master, textvariable=self.right_load_text)

        # render the load variables text labels to the GUI
        self.left_label = Label(master, text="Peak Left Pedal Load")
        self.right_label = Label(master, text="Peak Right Pedal Load")
        
        self.connect_button = Button(master, text="Connect Devices", command=self.connect_xbee)#lambda: self.update("connect"))

        # Log Display
        self.log= ''
        self.log_text = StringVar()
        self.log_text.set(self.log)
        self.log_box = Label(master, textvariable=self.log_text)

        
        # LAYOUT

        self.left_load.grid(row=1, column=0, sticky=W)
        self.right_load.grid(row=1, column=2, sticky=E)

        self.left_label.grid(row=0, column=0, sticky=W)
        self.right_label.grid(row=0, column=2, sticky=E)
        
        self.connect_button.grid(row=2, column=1, sticky=W+E)

        self.log_box.grid(row=3,column=1, sticky=W+E)

    def connect_xbee(self):
        # add code here to search for available devices and connect
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if "USB Serial Port" in p[1]: # if the device is found (by name)
                #open a xbee device on the current port
                self.xbee_pc = XBeeDevice(p[0], 9600)
                self.xbee_pc.open()

                # Define callback for when data is recieved
                def my_data_received_callback(xbee_message):
                    address = xbee_message.remote_device.get_64bit_addr()
                    data = xbee_message.data.decode("utf8")

                    #check if the data is coming from left or right and update the variable
                    if data[0] == 'L':
                        # update the GUI with the new peak value
                        self.left = float(data[1:])
                        self.left_load_text.set(self.left)
                    elif data[0] == 'R':
                        # update the GUI with the new peak value
                        self.right = float(data[1:])
                        self.right_load_text.set(self.right)
                    else:
                        self.update_log("Invalid data recieved.")

                # assign callback
                self.xbee_pc.add_data_received_callback(my_data_received_callback)

                # update the log
                self.update_log("Xbee Connected")
                return

        self.update_log("No Xbee Explorer Found")    
        print("No Xbee Explorer Found")
        return
        
    def update_log(self, message):
        old_msg = self.log_text.get()
        self.log_text.set(old_msg + '\r\n' + message)
        return


##    def update(self, method):
##        if method == "connect":
##            self.connect_xbee()
##        elif method == "log":
##            self.log(message)
##        return


root = Tk()
my_gui = PedalGUI(root)
root.mainloop()

# Exit Script
my_gui.xbee_pc.close()
print("Xbee connection closed")

