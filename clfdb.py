#!/usr/bin/python
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
# input : A string query
# output : a nested list of string
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
# Fetch only first col from the database.
# input : A string qurey
# output : A list of string
###################################################################
def fetch_fcol(sql):
    col= [""]
    results = querydb(sql)
    for row in results: 
        col.append(row[0])
    # Now print fetched result
    #print ", ".join(map(str, col))
    return col

###################################################################
# Fetch the all ips from db
# input : None
# output : A list of ip string
###################################################################
def ip_all():
    sql = "select IPaddr from Addr"
    ip_arr=fetch_fcol(sql)
    return ip_arr

###################################################################
# Fetch all keyphone ips 
# input : None
# output : A list of key ips string
###################################################################
def keyip_all():
    sql = "select IPaddr from Addr where DeviceName='KeyPhone'"
    keyip_arr=fetch_fcol(sql)
    return keyip_arr

###################################################################
# Fetch the FirstName acording to ip
# input : A string ip
# output : A string Firstname
###################################################################
def ip2name(ip):
	sql="select FirstName from Addr right join Persons on Persons.ID=Owner where IPaddr=\"" + ip + "\";"
	name=fetch_fcol(sql)
	#print name
	return name

###################################################################
# print out the data from the database
###################################################################
def printname_ip(ips): 
    c=0
    s="     "
    for ip in ips:
        c+=1
        sql = "select FirstName as Owner from Addr Left join Persons on Persons.ID=Owner where IPaddr='" + ip + "';"
        results = querydb(sql)
        for name in results:
            nam="%10s" % name[0]
            s += nam + ","
    l="+----------"
    line="----"
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

