#!/usr/bin/python2.7
##################################################################
# Program	: Chaucney Query database functions
# Author 	: Chauncey Yan
# Date 		: May 16th 2014
# Revisions : 0.2
# Description : Query the database on localhost, get the val we need
#               Printing out in a nicer format. 
# Updates 	: Added the Users and 
##################################################################
import subprocess
import MySQLdb
import getopt
import sys

###################################################################
# Config	:  
###################################################################

db_host="localhost" # host name, usually localhost
db_user="root" # database username
db_pw="iamroot" # database user password
db_name="Autodoor" # name of the data base

###################################################################
# Init		:
###################################################################
#check dependency
# Connect the db for query alter and insert.
db = MySQLdb.connect(db_host, db_user, db_pw)

# prepare a cursor object using cursor() method
cursor = db.cursor()

# create database if it is not exsits
cursor.execute("use " + db_name)

###################################################################
# Function	:
###################################################################
def usage():
	print "Usage:"
	print "-n <name> Return ip for specified name"
	print "-l Lists all ips"
	print "-h Displays this message"
	print "-q Directly query the database with sql language"
	print "-k Print key ips"

###################################################################
# Function	:
###################################################################
def init_setup():
	db_command("create database IF NOT EXISTS " + db_name)
	# create the tables for information storage
	db_command("create table if not exists Persons(ID int not null AUTO_INCREMENT, LastName varchar(255), FirstName varchar(255), FullName varchar(255) unique, Sex(6), primary key(ID)  );")
	db_command("create table if not exists Addr(ID int not null AUTO_INCREMENT, DeviceName varchar(24), Owner int(11), IPaddr varchar(12), MacAddr varchar(18), primary key(ID)  );")
	db_command("create table if not exists User(ID int(11) not null AUTO_INCREMENT, Owener(11), Username VARCHAR(16), Password VARCHAR(32), primary key(ID) );")

###################################################################
# Function 	: Retrive the IP data from the database
# input 	: A string query
# output 	: a nested list of string
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
        #db.rollback()

###################################################################
# Function	: Fetch only first col from the database.
# input 	: A string qurey
# output 	: A list of string
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
# Function	: Fetch the all ips from db
# input 	: None
# output 	: A list of ip string
###################################################################
def ip_all():
    sql = "select IPaddr from Addr"
    ip_arr=fetch_fcol(sql)
    return ip_arr

###################################################################
# Function	: Fetch all keyphone ips 
# input 	: None
# output 	: A list of key ips string
###################################################################
def keyip_all():
    sql = "select IPaddr from Addr where DeviceType='Key'"
    keyip_arr=fetch_fcol(sql)
    return keyip_arr

###################################################################
# Function	: Fetch the FirstName acording to ip
# input 	: A string ip
# output 	: A string Firstname
###################################################################
def ip2name(ip):
	sql="select FirstName from Addr right join Person on Person.ID=Owner where IPaddr=\"" + ip + "\";"
	name=fetch_fcol(sql)
	#print name
	return name[0]

###################################################################
# print out the name from the database with a weird format
###################################################################
def printname_ip(ips): 
    c=0
    s="     "
    for ip in ips:
        c+=1
        sql = "select FirstName as Owner from Addr Left join Person on Person.ID=Owner where IPaddr='" + ip + "';"
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

###################################################################
# execute the command in database
###################################################################
def db_command(sql):
	try:
		cursor.execute(sql)
	except:
		# Rollback in case there is any error
		print "Error: unable to execute the command"
		#db.rollback()

###################################################################
# insert information into database
###################################################################
def db_insert(user, pw, first, last, sex, deviceName, ipAddr, macAddr):
	fullName=first + last
	db_command("INSERT into Persons(LastName, FirstName, Gender) values(%s,%s,%s,%s);" % (last, first, fullName, sex))
	# detemine the owen of this 
	owner=fetch_fcol("select ID from Person where LastName=", last, " and FirstName=", first)
	db_command("INSERT into User(Username, Password, Owner) values(",user, ",", pw, ",", owner, ");")
	db_command("INSERT into Addr(DeviceName, Owner, IPaddr, MacAddr) values(", deviceName, ",", owner, ",", ipAddr, ",", macAddr, ");")


###################################################################
# Pareses and sets varibles from commandline arguments.
###################################################################
if (len(sys.argv) >= 2):
	try:
		opts, args = getopt.getopt(sys.argv[1:], "kn:lhq:", ["help", "ipa"])
	except getopt.GetoptError as err:
		# print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		usage()
		sys.exit(2)
	for o, a in opts:
		if o == "-q":
			print a, '-', querydb(a)
		elif o == "-l":
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
	



