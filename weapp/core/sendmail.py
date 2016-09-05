#!/usr/bin/python
#coding: utf8


import sys
from datetime import datetime
#邮件部分
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.utils import parseaddr, formataddr
import smtplib
from django.conf import settings

__author__ = 'chuter'



if __name__ == '__main__':
	import os
	sys.path.insert(0, '../../')
	sys.path.insert(0, '../')
	os.environ['DJANGO_SETTINGS_MODULE'] = 'weapp.settings'



class MyMail(object ):
	def __init__ (self):
		self.account = settings.MAIL_NOTIFY_USERNAME
		self.password = settings.MAIL_NOTIFY_PASSWORD
		self.smtp_server = settings.MAIL_NOTIFY_ACCOUNT_SMTP

	def send (self, receivers, title, content, mode=None, file_path=None):
		if mode == 'test':
			receivers = receivers[0:1]
		to_addr = ';'.join(receivers)

		date = datetime.now().strftime('%Y-%m-%d')
		msg = MIMEMultipart('alternative')
		msg['From' ] = self.account
		msg['To' ] = to_addr
		msg['Subject'] = str(Header('%s' % title, 'utf-8'))
		c = MIMEText(content, _subtype='html', _charset='utf-8')
		msg.attach(c)

		#添加附件
		if file_path:
			filename = file_path.split('.')[0]
			with open(file_path ,'rb') as f:
				#设置附件的mime和文件名，这里是py类型
				mime = MIMEBase('txt', 'xlsx', filename=filename)
				#加上头信息
				mime.add_header('Content-Disposition', 'attachment', filename=file_path)
				mime.add_header('Content-ID', '<0>')
				mime.add_header('X-Attachment-Id', '0')

				#把附件的内容读进来
				mime.set_payload(f.read())

				#用Base64编码
				encoders.encode_base64(mime)

				#添加到MIMEMultipart
				msg.attach(mime)
		server = smtplib.SMTP(self.smtp_server)
		#server.docmd("EHLO server" )
		#server.starttls()
		server.login(self.account,self.password)
		server.sendmail(self.account, receivers, msg.as_string())
		server.close()


m = MyMail()
def sendmail(receivers, title, content, mode=None, file_path=None):
	if isinstance(receivers,str):
		receivers = [receivers]
	m.send(receivers, title, content, mode, file_path)

if __name__=="__main__" :
    if len(sys.argv) < 4:
		print 'Usage: %s mail_address title content' % sys.argv[0]
    else:
		sendmail(sys.argv[1], sys.argv[2], sys.argv[3])

