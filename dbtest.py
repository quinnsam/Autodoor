#!/usr/bin/python2.7

import subprocess
import clfdb


ips=clfdb.keyip_all()
connected = [""]
for ip in ips:
    connected.append(ip)
clfdb.printname_ip(connected)
clfdb.db_close()

