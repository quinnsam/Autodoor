#!/usr/bin/env python

"""
A simple echo client
"""

import socket

host = 'mobkilla.no-ip.biz'
port = 55555
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
s.send('Hello, world')
data = s.recv(size)
s.close()
print 'Received:', data
