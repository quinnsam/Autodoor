#!/usr/bin/python
##################################################################
# Program : Chaucney Query database functions
# Author : Chauncey Yan
# Date : May 16th 2014
# Revisions : 0.2
# Description : Query the database on localhost, get the val we need
#               Printing out in a nicer format. 
# Updates : Added the Users and 
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
    col=[""]
    results = querydb(sql)
    for row in results: 
        col.append(row[0])
    # Now print fetched result
    #print ", ".join(map(str, col))
    return col[1:]

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
	return name[0]

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
#  checking 
###################################################################
def check_usrpw(usr,pw):
    sql = "select ID from User where Password=SHA2('" + pw + "',256) and Username='" + usr + "';"
    #print fetch_fcol(sql)
    if ( fetch_fcol(sql) == [] ):
        return 0;
    else: 
        return 1;

###################################################################
# user checking
###################################################################
def check_usr(usr):
    sql = "select ID from User where Username='" + usr + "';"
    if ( fetch_fcol(sql) == [] ):
        return 0;
    else:
        return 1;

###################################################################
# password checking 
###################################################################
def check_pw(pw):
    sql = "select ID from User where Password=SHA2('" + pw + "',256);"
    if ( fetch_fcol(sql) == [] ):
        return 0;
    else:
        return 1;
###################################################################
# Disconnect form sercer
###################################################################
def db_close():
    db.close()

