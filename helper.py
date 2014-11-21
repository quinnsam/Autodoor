#!/usr/bin/python
# Import smtplib for the actual sending function
import smtplib
import hashlib
# Import the email modules we'll need
from email.mime.text import MIMEText

def process_file(file_name):

    user_names = []
    passwords = []

    try:
        file_conn = open(file_name)
        data = file_conn.readlines()

        for i in range(len(data)):
            if i%2 == 0:
                user_names.append(data[i][:-1])
            else:
                passwords.append(data[i][:-1])

        file_conn.close()
    except:
        return "", ""
    return user_names, passwords

def auth_user(user, password):

    user_names, passwords = process_file("Autodoor.pass")

    if user not in user_names:
        return -1

    user_input = hashlib.sha224(password).hexdigest()
    if user_input != passwords[user_names.index(user)]:
        print 'Incorrect Password'
        return -1
    else:
        print 'User Authenticated\n'
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
	s.login(sender, 'password')
	s.sendmail(sender, ['quinnsam1@gmail.com'], msg.as_string())
	s.quit()
	print 'Email Sent'
