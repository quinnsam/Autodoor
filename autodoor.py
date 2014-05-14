#!/usr/bin/python2.7

# This program automates a door for keyless unlocking.
# Developed by: Sam Quinn, Chauncey Yan, Ashley Greenacre
# 05/13/2014
# Code Referenced: 'Noah Gift's Creating Agile Commandline Tools With Python'

from threading import Thread
import subprocess

ips = ["10.0.0.1", "10.0.0.9", "10.0.0.113", "10.0.0.111"]
connected = []
devices = 0
lock_status = 0

while 1:

    for ip in ips:
        ret = subprocess.call("ping -c 1 -w 1 -n %s" % ip,
                shell=True,
                stdout=open('/dev/null', 'w'),
                stderr=subprocess.STDOUT)

        if ret == 0:
            if ip in connected:
                continue
            else:
                ++devices
                connected.append(ip)
                print "\n\n UNLOCKING \n\n"
                lock_status = 0

        else :
            if ip in connected:
                connected.remove(ip)
            if (len(connected) == 2 and lock_status == 0):
                print "\n\n LOCKING \n\n"
                lock_status = 1

    print '%s' % ', '.join(map(str, connected))
