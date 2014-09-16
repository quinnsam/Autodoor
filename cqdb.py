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
import getopt
import sys

###################################################################
# Connect the db for query alter and insert.
###################################################################
# Open database connection
db = MySQLdb.connect("localhost","root","iamroot","AutoDoorClients" )
# prepare a cursor object using cursor() method
cursor = db.cursor()
def usage():
	print "Usage:"
	print "-n Name2ip"
	print "-i Lists all ips"
	print "-h Displays this message"
	print "-q query the database"
	print "-k Print key ips"

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
#  username and password checking 
###################################################################
def check_usrpw(usr,pw):
    sql = "select ID from User where Password=SHA2('" + pw + "',256) and Username='" + usr + "';"
    #print fetch_fcol(sql)
    if ( fetch_fcol(sql) == [] ):
        return 0;
    else: 
        return 1;

###################################################################
# username checking
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
def check_pw(table,pw):
    sql = "select ID from " + table + " where Password=SHA2('" + pw + "',256);"
    if ( fetch_fcol(sql) == [] ):
        return 0;
    else:
        return 1;

###################################################################
# Email and password checking 
###################################################################
def check_empw(email,pw):
    sql = "select ID from Email where Email='" + email + "';"
    if ( fetch_fcol(sql) == [] ):
        return 0;
    else:
		if ( check_pw("Email",pw) == 1 ):
			return 1;
		return 0;

###################################################################
# Email password return
###################################################################
def return_empw(email):
    sql = "select Password from Email where Email='" + email + "';"
    return fetch_fcol(sql)[0];

###################################################################
# Disconnect form sercer
###################################################################
def db_close():
    db.close()


###############################################################################
# Pareses and sets varibles from commandline arguments.
###############################################################################
try:
	opts, args = getopt.getopt(sys.argv[1:], "kn:ihq:", ["help", "ipa"])
except getopt.GetoptError as err:
	# print help information and exit:
	print str(err) # will print something like "option -a not recognized"
	usage()
	sys.exit(2)
for o, a in opts:
	if o == "-q":
		print a, '-', querydb(a)
	elif o == "-i":
		print ip_all()
	elif o == "-k":
		print keyip_all()
	elif o == "-n":
		print ip2name(a)
	elif o in ("-h", "--help"):
		usage()
		sys.exit()
	else:
		assert False, "unhandled option"




