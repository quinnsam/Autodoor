#!/usr/bin/python2.7
##################################################################
# Program : Califlower database functions
# Author : Chauncey Yan
# Date : May 16th 2014
# Revisions : 0.1
# Description : Query the database on localhost, get the val we need
#               Printing out in a nicer format.
# Updates : None
##################################################################
import subprocess
import MySQLdb

###################################################################
# Connect the db for query alter and insert.
###################################################################
# Open database connection
db = MySQLdb.connect("localhost","root","iamroot","AutoDoorClients" )
# prepare a cursor object using cursor() method
cursor = db.cursor()
###################################################################
# Retrive the IP data from the database
###################################################################
def querydb (query):
    try:
    # Execute the SQL command
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except:
        # Rollback in case there is any error
        print "Error: unable to fecth data"
        db.rollback()

###################################################################
# query the ips with function querydb
###################################################################
def keyip_all():
    ip_arr= [""]
    sql = "select IPaddr from Addr Left join Persons on Persons.ID=Owner where DeviceName='KeyPhone'"
    results = querydb(sql)
    for row in results: 
        ip_arr.append(row[0])
    # Now print fetched result
    print ", ".join(map(str, ip_arr))
    return ip_arr
###################################################################
# print out the data from the database
###################################################################
def printname_ip(ips): 
    c=0
    s="\t\t"
    for ip in ips:
        c+=1
        sql = "select FirstName as Owner from Addr Left join Persons on Persons.ID=Owner where IPaddr='" + ip + "';"
        results = querydb(sql)
        for name in results:
            nam="%10s" % name[0]
            s += nam + ","
    l="+----------"
    line="------"
    for i in range(0,c):
        line += l 
    line += "-+"
    s=s[:-1]
    print line
    print s 


###################################################################
# Disconnect form sercer
###################################################################
def db_close():
    db.close()

