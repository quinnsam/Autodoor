#!/usr/bin/python
import socket
import cgi, cgitb

host = '0.0.0.0'
port = 5555
size = 1024
data = 'ERROR'
username = '999'
password = '999'
request = '999'

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

if request == None:
	data = 'Unsuported Browser.. for now sorry! :('


if username != '999' and password != '999' and request != '999':
    if username != '' or password != '' or request != '':
        message = "<message><type>handshake</type><user>%s</user><pin>%s</pin></message>" % (username, password)
        s.send(message)
        data = s.recv(size)
        #print "<p>User:%s, pin:%s, Request:(%s), DATA:%s</p>" % (username, password, request, data)

        if data == '<message><type>handshake</type><from>earth</from></message>':
            print "<h2>PASSED</h2>"
            message = "<message><type>%s</type><user>%s</user></message>" % (request, username)
            s.send(message)
            data = s.recv(size)
        else:
            print "<h2>FAILED</h2>"
            print "<p>Invalid Username or Password.</p>"
    else:
        print "<h2>You sneeker no this will not werk </h2>"

    s.close()
else:
	print "<h2>FAILED</h2>"
	print "<p>%s: Invalid Request.</p>" % (data)
print '</body>'
print '</html>'
