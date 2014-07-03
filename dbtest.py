#!/usr/bin/python

import subprocess
import cqdb


ips=cqdb.ip_all()
connected = [""]
for ip in ips:
    connected.append(ip)
cqdb.printname_ip(connected)

ips=cqdb.keyip_all()
connected = [""]
for ip in ips:
    connected.append(ip)
cqdb.printname_ip(connected)

name=cqdb.ip2name(ips[3])
print "iptoname " 
print name
print "-------"

pw="iamroot"
usr="roo"

print cqdb.check_usrpw(usr,pw)
print cqdb.check_pw(pw)
print cqdb.check_usr(usr)
cqdb.db_close()

