#!/usr/bin/python

import subprocess
import clfdb


ips=clfdb.ip_all()
connected = [""]
for ip in ips:
    connected.append(ip)
clfdb.printname_ip(connected)

ips=clfdb.keyip_all()
connected = [""]
for ip in ips:
    connected.append(ip)
clfdb.printname_ip(connected)

name=clfdb.ip2name(ips[2])
print name



clfdb.db_close()

