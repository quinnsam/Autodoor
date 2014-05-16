#!/usr/bin/python2.7
###############################################################################
# This program automates a door for keyless unlocking                         #
# Developed by: Sam Quinn, Chauncey Yan, Ashley Greenacre, and Chris Harper.  #
# 05/13/2014                                                                  #
###############################################################################

from threading import Thread
from time import gmtime, strftime, sleep
import subprocess
#import datetime
#import serial
import os
import RPi.GPIO as GPIO
import clfdb

def arduino_watcher():
    print 'Arduino watcher has spawned,', os.getpid()
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(23, GPIO.IN, pull_up_down.PUD_DOWN)
    while (1):
        if(GPIO.input(23) ==1):
            print 'Arduino signal recived!'


def handler(signum, frame):
    switch signum 
        case 8:
            unlock()
            #sleep
            lock()
        case 7:
            # Poll form the arduino for what the new lock state is.
    

ips=clfdb.keyip_all()

###############################################################################
# Setting Global varibles and environment.
###############################################################################
SAM = '10.0.0.111'
ASHLEY = '10.0.0.54'

connected = ["10.0.0.1", "10.0.0.9"]
lock_status = 0
night_lock = 0
#current_time = int(strftime("%H", gmtime()))
#arduino = serial.Serial('/dev/ttyACM0', 9600)

###############################################################################
# Sends a lock request to the door to be locked
#
# Tasks:
# 1.)   Checks the current stored lock position.
# 2.)   Sends a singnal to the arduino to lock the door.
# 3.)   Only locks the door if the door is closed using the magnetic sensor.
#
###############################################################################
def lock():
    global lock_status
    print "\n\n LOCKING -", lock_status, " \n\n"
    #arduino.write('1')
    lock_status = 1

###############################################################################
# Sends a unlock request to the door to be unlocked
#
# Tasks:
# 1.)   Checks the current stored lock position.
# 2.)   Sends a singnal to the arduino to unlock the door.
#
###############################################################################
def unlock():
    global lock_status
    print "\n\n UNLOCKING \n\n"
    #arduino.write('0')
    lock_status = 0

###############################################################################
# The main while loop that will continualy monitor for clients and manage
# housekeeping process.
#
# Tasks:
# 1.)   Ping the client list to see which devices are alive or dead.
# 2.)   If a devices is alive and have not been added to the cliet list yet
#       it will unlock the door.
# 3.)   If the alive device is already been established then no action is taken.
# 4.)   After 30 seconds of the door being unlocked it will automatically lock.
# 5.)   When a user is leaving the house the proxsimity sensor will trigger and
#       automatically unlock the door so exiting does not have to be matic.
#
###############################################################################
while 1:
    #current_time = int(strftime("%H", gmtime()))
    for ip in ips:

        # If the arduino proximity sensor is triggered
        if (arduino.readline(eol='\r') == '8'):
            unlock()
            #sleep
            lock()

        ret = subprocess.call("ping -c 1 -w 1 -n %s" % ip,
                shell=True,
                stdout=open('/dev/null', 'w'),
                stderr=subprocess.STDOUT)

        if ret == 0:
            if ip in connected:
                continue
            else:
                connected.append(ip)
                if lock_status == 1:
                    unlock()
                    #sleep
                    lock()


        else :
            if ip in connected:
                connected.remove(ip)
            if (len(connected) == 2 and lock_status == 0):
                lock()

    clfdb.printname_ip(connected)
    print current_time, '[', lock_status,'] %s' % ', '.join(map(str, connected))


# Disconneting from mysql server
clfdb.db_close()

