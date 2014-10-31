#!/usr/bin/python
# Tkinter and GPIO together
 
from Tkinter import *
import serial
import time

def unlock():
	arduino.write('0')
	
def lock():
	arduino.write('1')
 
def stat():
	arduino.write('2')
	#buf = buf + arduino.read(arduino.inWaiting())
	buf = arduino.read(arduino.inWaiting())
	if '\n' in buf :
		#last_received = "a"
		lines = buf.split('\n') # Guaranteed to have at least 2 entries

    	if lines[-2]: 
			last_received = lines[-2]
		
	statusButton["text"] = "Status: " + last_received

def calibrate():
	arduino.write('3')

arduino = serial.Serial('/dev/ttyUSB0', 9600)

root = Tk()
root.title("Autodoor")
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w, h))

unlockButton = Button(root, text="Unlock", font=("Helvetica", 72), fg="black", bg="green", command=unlock)
unlockButton.pack(fill=BOTH, expand=1)
#unlockButton.grid(row=0,column=0)

lockButton = Button(root, text="Lock", font=("Helvetica", 72), fg="black", bg="red", command=lock)
lockButton.pack(fill=BOTH, expand=1)
#lockButton.grid(row=0,column=1)

statusButton = Button(root, text="Status", font=("Helvetica", 72), fg="white", bg="blue", command=stat)
statusButton.pack(fill=BOTH, expand=1)
#statusButton.grid(row=1,column=0)

caliButton = Button(root, text="Calibrate", font=("Helvetica", 72), fg="red", bg="yellow", command=calibrate)
caliButton.pack(fill=BOTH, expand=1)
#caliButton.grid(row=1,column=1)
 
exitButton = Button(root, text="Quit", font=("Helvetica", 72), fg="grey", bg="brown", command=exit)
exitButton.pack(fill=BOTH, expand=1)

root.mainloop()
