#!/usr/bin/python

import serial

arduino = serial.Serial('/dev/ttyUSB0',9600)
arduino.write('0')
