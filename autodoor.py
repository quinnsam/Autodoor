#!/usr/bin/python2.7

# This program automates a door for keyless unlocking.
# Developed by: Sam Quinn, Chauncey Yan, Ashley Greenacre
# 05/13/2014
# Code Referenced: 'Noah Gift's Creating Agile Commandline Tools With Python'

from threading import Thread
from time import gmtime, strftime, sleep
import subprocess
#import datetime
import MySQLdb
#import serial

###################################################################
# Retrive the IP data from the database
###################################################################
def querydb (query):
    # Open database connection
    db = MySQLdb.connect("localhost","root","iamroot","AutoDoorClients" )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Set the sql to query
    sql = query
    try:
    # Execute the SQL command
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
    except:
        # Rollback in case there is any error
        print "Error: unable to fecth data"
        db.rollback()


###################################################################
# query the ips with function querydb
###################################################################

ip_arr=["10.0.0.1", "10.0.0.9"]
sql = "select FirstName as Owner, IPaddr, MacAddr from Addr Left join Persons on Persons.ID=Owner where DeviceName='Phone'"
results = querydb(sql)
for row in results:
    owner = row[0]
    ipaddr = row[1]
    macaddr = row[2]
    ip_arr.append(row[1])
    # Now print fetched result
    print "owner=%s,ip=%s,mac=%s" %(owner, ipaddr, macaddr)


print ip_arr
ips=ip_arr
###################################################################
#
###################################################################

SAM = '10.0.0.111'
ASHLEY = '10.0.0.54'

#ips = ["10.0.0.1", "10.0.0.9", "10.0.0.113", "10.0.0.111", "10.0.0.72", "10.0.0.54"]
connected = ["10.0.0.1", "10.0.0.9"]
lock_status = 0
night_lock = 0
#current_time = int(strftime("%H", gmtime()))
#arduino = serial.Serial('/dev/ttyACM0', 9600)

def lock():
    global lock_status
    print "\n\n LOCKING -", lock_status, " \n\n"
    #arduino.write('1')
    lock_status = 1

def unlock():
    global lock_status
    print "\n\n UNLOCKING \n\n"
    #arduino.write('0')
    lock_status = 0

def ashley():
    unlock()
    time.sleep(6)
    lock()

while 1:
    current_time = int(strftime("%H", gmtime()))
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
                    if 0:
                    #if ip == ASHLEY:
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
    #if current_time > 24:
    #    current_time = 0

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
    ###################################################################
    # print out the data from the database
    ###################################################################
    for ip in connected:
        sql = "select FirstName as Owner from Addr Left join Persons on Persons.ID=Owner where IPaddr='" + ip + "';"
        results = querydb(sql)
        print results
    
    print current_time, '[', lock_status,'] %s' % ', '.join(map(str, connected))

# disconnect from server
db.close()

