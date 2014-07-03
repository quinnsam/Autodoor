#!/usr/bin/python
import socket
import cgi, cgitb 

host = '0.0.0.0'
port = 5555
size = 1024
data = 'ERROR'
username = ''
password = ''
request = ''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
username = form.getvalue('username')
password  = form.getvalue('pin')
request = form.getvalue('request')
print "Content-type:text/html\r\n\r\n"
print '<html>'
print '<head>'
print '<title>Autodoor Website</title>'
print '</head>'
print '<body>'
print '<h2>Contacting Earth to unlock the door, now.</h2>'
if username != '' and password != '' and request != '':
	message = "<message><type>handshake</type><user>%s</user><pin>%s</pin></message>" % (username, password)
	s.send(message)
	data = s.recv(size)
	#print "<p>User:%s, pin:%s, Request:%s</p>" % (username, password, request)
	
	if data == '<message> <type>handshake</type> <from>earth</from> </message>':
		print "<h2>PASSED</h2>"
		message = "<message> <type>%s</type> <user>%s</user> </message>" % (request, username)
		s.send(message)
		data = s.recv(size)
	else:
		print "<h2>FAILED</h2>"
		print "<p>Invalid Username or Password.</p>"

	s.close()
else:
	print "<h2>FAILED</h2>"
	print "<p>%s: Invalid Request.</p>" % (data)
print '</body>'
print '</html>'
