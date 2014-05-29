#!/usr/bin/python2.7
###############################################################################
# This program automates a door for keyless unlocking                         #
# Developed by: Sam Quinn, Chauncey Yan, Ashley Greenacre, and Chris Harper.  #
# 05/19/2014                                                                  #
###############################################################################

import os
import socket
import select
from xml.dom import minidom

host = ''       # sets the server to use the address of the current machine.
port = 5555    #My port
backlog = 5     #Number of clients can wait
size = 1024     #Max size of socket read and write


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Prevent socket from being left in TIME_WAIT state
server.bind((host, port))
server.listen(backlog)
connected = [server]  # Number of connected sockets

def handshake(client):
    raw = client.recv(size)
    raw = raw.strip()
    #XML parse message
    xmldoc = minidom.parse(raw)
    itemlist = xmldoc.getElementsByTagName('message')
    host, port = client.getpeername()
    if itemlist[0].attributes['type'].value == 'handshake':
        client.send('<message type=\"handshake\" from=\"earth\"</message>')


while True:
    readable, writeable, error = select.select(connected, [], [])
    for socket in readable:
        if(socket == server):   # New client connected
            new_client, address = server.accept()
            handshake(new_client)
        else:   # Existing client
            data = socket.recv(size)
            data = data.strip()
            data = data.Split('\n')

            for message in data:
                if message != '':
                    #XML parse message
                    xmldoc = minidom.parse(raw)
                    itemlist = xmldoc.getElementsByTagName('message')
                    request = itemlist[0].attributes['type'].value
                    if (request == 'status'):
                        # Call get status from autodoor.py
                        
                    elif (request == 'lock'):
                        # Send lock signal to autodoor.py
                    elif (request == 'unlock'):
                        # Send unlock signal to autodoor.py
                    else:
                        socket.send('ERROR: unrecognized command', request)
                else:   # Client left the session
                    socket.close()
                    connected.remove(socket)

