#!/usr/bin/python
import socket
import cgi, cgitb 

host = '0.0.0.0'
port = 5555
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
username = form.getvalue('username')
pin  = form.getvalue('pin')

print "Content-type:text/html\r\n\r\n"
print '<html>'
print '<head>'
print '<title>Autodoor Website</title>'
print '</head>'


print '<body>'
print '<h2>Contacting Earth to unlock the door, now.</h2>'
message = "<message><type>handshake</type><user>%s</user><pin>%s</pin></message>" % (username, pin)
s.send(message)
data = s.recv(size)
if data == '<message> <type>handshake</type> <from>earth</from> </message>':
	print "<h2>PASSD</h2>"
	message = "<message> <type>unlock</type> <user>%s</user> </message>" % (username)
	s.send(message)
	data = s.recv(size)
else:
	print "<h2>FAILED</h2>"

s.close()
print "<p>%s</p>" % (data)
print '</body>'

print '</html>'
