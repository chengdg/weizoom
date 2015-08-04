#!/usr/bin/python
#coding: utf8


import sys
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#from email.message import Message
from email.header import Header
import smtplib 
from django.conf import settings

__author__ = 'chuter'



if __name__ == '__main__':
	import os
	sys.path.insert(0, '../../')
	sys.path.insert(0, '../')
	os.environ['DJANGO_SETTINGS_MODULE'] = 'weapp.settings'



class MyMail (object ):
    def __init__ (self):
		self.account = settings.MAIL_NOTIFY_USERNAME
		self.password = settings.MAIL_NOTIFY_PASSWORD

    def send (self, dst_mail, title, content):
		date = datetime.now().strftime('%Y-%m-%d')
		msg = MIMEMultipart('alternative')
		msg['From' ] = self.account
		msg['To' ] = dst_mail
		msg['Subject'] = str(Header('%s' % title, 'utf-8'))
		c = MIMEText(content, _subtype='html', _charset='utf-8')
		msg.attach(c)
		server = smtplib.SMTP(settings.MAIL_NOTIFY_ACCOUNT_SMTP)
		#server.docmd("EHLO server" )
		#server.starttls()
		server.login(self.account,self.password)
		server.sendmail(self.account, dst_mail.split(','), msg.as_string())
		server.close()	


m = MyMail()
def sendmail(mail_address, title, content):
    m.send(mail_address, title, content)


if __name__=="__main__" :
    if len(sys.argv) < 4:
		print 'Usage: %s mail_address title content' % sys.argv[0]
    else:
		sendmail(sys.argv[1], sys.argv[2], sys.argv[3])

