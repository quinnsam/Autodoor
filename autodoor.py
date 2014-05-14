#!/usr/bin/python2.7

# This program automates a door for keyless unlocking.
# Developed by: Sam Quinn, Chauncey Yan, Ashley Greenacre
# 05/13/2014
# Code Referenced: 'Noah Gift's Creating Agile Commandline Tools With Python'

from threading import Thread
from time import gmtime, strftime, sleep
import subprocess

SAM = '10.0.0.111'
CHAUNCEY = '10.0.0.72'
ASHLEY = '10.0.0.55'

ips = ["10.0.0.1", "10.0.0.9", "10.0.0.113", "10.0.0.111", "10.0.0.72", "10.0.0.55"]
connected = ["10.0.0.1", "10.0.0.9"]
lock_status = 0
night_lock = 0
current_time = int(strftime("%H", gmtime()))

def lock():
    global lock_status
    print "\n\n LOCKING -", lock_status, " \n\n"
    lock_status = 1

def unlock():
    global lock_status
    print "\n\n UNLOCKING \n\n"
    lock_status = 0

def ashley():
    unlock()
    time.sleep(6)
    lock()

while 1:
    #current_time = int(strftime("%H", gmtime()))
    for ip in ips:
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
                    if ip == ASHLEY:
                        worker = Thread(target=ashley)
                        worker.setDaemon(True)
                        worker.start()
                    else:
                        unlock()


        else :
            if ip in connected:
                connected.remove(ip)
            if (len(connected) == 2 and lock_status == 0):
                lock()

    # Testing auto lock feature
    if current_time > 24:
        current_time = 0

    if current_time >= 20:
        if night_lock != 1:
            print "System locking for the night. Time:", current_time
            if lock_status == 0:
                lock()
            night_lock = 1
    elif current_time >= 7:
        if night_lock != 0:
            print "The time is:", current_time
            night_lock = 0
    # Test auto lock feature
    current_time += 1


    print '[', lock_status,'] %s' % ', '.join(map(str, connected))


