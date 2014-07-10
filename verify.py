#!/usr/bin/python
# Import smtplib for the actual sending function
import smtplib
import cqdb
# Import the email modules we'll need
from email.mime.text import MIMEText

###############################################################################
# Perfomes the inital handshake between the connected socket and itself
#
# Tasks:
# 1.)   Recieve the xml message from the newly connected client
# 2.)   Send handshake back to the client
#
###############################################################################

def shake(user, pin):
	print 'Checking Credidentials'
	print 'User =', user
	try:
		if (cqdb.check_usrpw(user,pin) == 1):
			return 0
		else:
			print 'Username and Password did not match'
			return 1
	except:
		print 'Verification failed Database may be offline'
		return 1

def mailer(user, status):
	print 'Sending Email to email list'
	sender = 'comprepair3@gmail.com'
	if status == 0:
		msg = MIMEText('%s has logged in to Autodoor App' % user)
	elif status == 2:
		msg = MIMEText('%s Has connected to the network' % user)
	elif status == 3:
		msg = MIMEText('%s Has dis-connected from the network' % user)
	else:
		msg = MIMEText('%s FAILED to login to the Autodoor App' % user)
	msg['Subject'] = 'Autodoor activity'
	msg['From'] = sender
	msg['To'] = 'quinnsam1@gmail.com'
	s = smtplib.SMTP('smtp.gmail.com',587)
	s.starttls()
	s.ehlo()
	s.login(sender, cqdb.return_empw(sender))
	s.sendmail(sender, ['quinnsam1@gmail.com'], msg.as_string())
	msg['To'] = 'chaunceyyann@gmail.com'
	s.sendmail(sender, ['chaunceyyann@gmail.com'], msg.as_string())
	s.quit()
	print 'Email Sent'

