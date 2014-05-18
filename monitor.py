#!/usr/bin/python2.7
arduino = serial.Serial('/dev/ttyUSB0', 9600, 7, 'E', 1)
print 'Arduino watcher has spawned,', os.getpid()
print arduino.readline()
