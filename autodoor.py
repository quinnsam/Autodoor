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
import serial
import os
import RPi.GPIO as GPIO
import clfdb

def arduino_watcher():
    print 'Arduino watcher has spawned,', os.getpid()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.IN, pull_up_down.PUD_DOWN)
    while (1):
        if(GPIO.input(23) ==1 and running != 1):
            print 'Arduino signal recived!'
            running = 1
        
        if(GPIO.input(23) == 0 and running != 0):
            running = 0


ips=clfdb.keyip_all()

###############################################################################
# SETTING GLOBAL VARIBLES AND ENVIRONMENT.
###############################################################################
CONNECTED = ["10.0.0.1", "10.0.0.9"]
LOCK_STATUS = 0
#ARDUINO = SERIAL.SERIAL('/DEV/TTYACM0', 9600)

###############################################################################
# SENDS A LOCK REQUEST TO THE DOOR TO BE LOCKED
#
# TASKS:
# 1.)   CHECKS THE CURRENT STORED LOCK POSITION.
# 2.)   SENDS A SINGNAL TO THE ARDUINO TO LOCK THE DOOR.
# 3.)   ONLY LOCKS THE DOOR IF THE DOOR IS CLOSED USING THE MAGNETIC SENSOR.
#
###############################################################################
DEF LOCK():
    GLOBAL LOCK_STATUS
    PRINT "\N\N LOCKING -", LOCK_STATUS, " \N\N"
    #ARDUINO.WRITE('1')
    LOCK_STATUS = 1

###############################################################################
# SENDS A UNLOCK REQUEST TO THE DOOR TO BE UNLOCKED
#
# TASKS:
# 1.)   CHECKS THE CURRENT STORED LOCK POSITION.
# 2.)   SENDS A SINGNAL TO THE ARDUINO TO UNLOCK THE DOOR.
#
###############################################################################
DEF UNLOCK():
    GLOBAL LOCK_STATUS
    PRINT "\N\N UNLOCKING \N\N"
    #ARDUINO.WRITE('0')
    LOCK_STATUS = 0

###############################################################################
# THE MAIN WHILE LOOP THAT WILL CONTINUALY MONITOR FOR CLIENTS AND MANAGE
# HOUSEKEEPING PROCESS.
#
# TASKS:
# 1.)   PING THE CLIENT LIST TO SEE WHICH DEVICES ARE ALIVE OR DEAD.
# 2.)   IF A DEVICES IS ALIVE AND HAVE NOT BEEN ADDED TO THE CLIET LIST YET
#       IT WILL UNLOCK THE DOOR.
# 3.)   IF THE ALIVE DEVICE IS ALREADY BEEN ESTABLISHED THEN NO ACTION IS TAKEN.
# 4.)   AFTER 30 SECONDS OF THE DOOR BEING UNLOCKED IT WILL AUTOMATICALLY LOCK.
# 5.)   WHEN A USER IS LEAVING THE HOUSE THE PROXSIMITY SENSOR WILL TRIGGER AND
#       AUTOMATICALLY UNLOCK THE DOOR SO EXITING DOES NOT HAVE TO BE MATIC.
#
###############################################################################
WHILE 1:
    FOR IP IN IPS:

        #IF (ARDUINO.READLINE(EOL='\R') == '8'):
        #    UNLOCK()
        #    #SLEEP
        #    LOCK()

        RET = SUBPROCESS.CALL("PING -C 1 -W 1 -N %S" % IP,
                SHELL=TRUE,
                STDOUT=OPEN('/DEV/NULL', 'W'),
                STDERR=SUBPROCESS.STDOUT)

        IF RET == 0:
            IF IP IN CONNECTED:
                CONTINUE
            ELSE:
                CONNECTED.APPEND(IP)
                IF LOCK_STATUS == 1:
                    UNLOCK()
                    #SLEEP
                    LOCK()


        ELSE :
            IF IP IN CONNECTED:
                CONNECTED.REMOVE(IP)
            IF (LEN(CONNECTED) == 2 AND LOCK_STATUS == 0):
                LOCK()

    CLFDB.PRINTNAME_IP(CONNECTED)
    PRINT '[', LOCK_STATUS,'] %S' % ', '.JOIN(MAP(STR, CONNECTED))


# DISCONNETING FROM MYSQL SERVER
CLFDB.DB_CLOSE()

