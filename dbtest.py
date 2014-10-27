#!/usr/bin/python

import subprocess
import cqdb


ips=cqdb.ip_all()
connected = [""]
for ip in ips:
    connected.append(ip)
#cqdb.printname_ip(connected)

ips=cqdb.keyip_all()
connected = [""]
for ip in ips:
    connected.append(ip)
#cqdb.printname_ip(connected)

#name=cqdb.ip2name(ips[3])
#print "iptoname " 
#print name
#print "-------"

pw="iamycx"
usr="cyanjin"
email="chaunceyyann@gmail.com"
email2="chaunceyyann@gmail.com"
epw="iamycx"
print cqdb.check_usrpw(usr,pw)
print cqdb.check_pw("User",pw)
print cqdb.check_usr(usr)
print cqdb.check_empw(email2,epw)
print cqdb.return_empw(email)
print cqdb.return_empw(email2)

cqdb.db_close()

