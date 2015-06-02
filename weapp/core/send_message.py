# -*- coding: utf-8 -*-

import sys
import random
try:
	import json
except:
	import simplejson as json
import stomp
import urllib

from optparse import OptionParser
from django.conf import settings

from watchdog.utils import watchdog_info

default_retry_times   = 3


#===============================================================================
# send_message_to_activemq : 将消息传递给ActiveMQ
#===============================================================================
def send_message_to_activemq(destination, 
				 message_str, 
				 retry_times = default_retry_times):
	"""
	send the message to specific destination
		
	\param destination		   
		the destination of the message send to.
		ex. '/queue/jms.com.wintim.service' or '/topic/jms.com.wintim.service'

	\param message_str
		the message send to the destination, it will
		be wrapped as textMessage, it must be in json type
			
	\param retry_times
		when send message failed, try 'retry_times' times again
		
	\param activeMQ_host
		this host of the activeMQ server's transportConnector, default is 'mq.wintim.com'
			
	\param activeMQ_port
		this port of the activeMQ server's transportConnector
	"""
	host = settings.MOM_HOST
	port = settings.MOM_PORT
	conn = stomp.Connection([(host, port)])
	conn.start()
	conn.connect(wait=True)
	
	print 'send message [%s] to destination %s at %s:%s' % (message_str, destination, host, port)
	watchdog_info('send message [%s] to destination %s at %s:%s' % (message_str, destination, host, port))
	try:
		conn.send(message_str, destination=destination, \
				  headers={'type':'textMessage','MessageNumber':random.randint(0,65535), 'persistent':'true'}, ack='auto')
	except Exception, e:
		print 'failed to send message, caused by ', (str)(e)
		print 'retry send message [%s] to destination %s' % (message_str, destination)
		i = 1
		while i < retry_times:
			if conn.is_connected() == False:
				conn.connect(wait=True)
			try:
				time.sleep(1)
				conn.send(message_str, destination=destination, \
					  headers={'type':'textMessage','MessageNumber':random.randint(0,65535), 'persistent':'true'}, ack='auto')
			except:
				pass
			i += 1
		
		if i >= retry_times:
			raise Exception, '[has retry %d times]' % retry_times
	finally:
		conn.disconnect()

send_message = send_message_to_activemq
	
if __name__ == '__main__':
	parser = OptionParser()
	
	parser.add_option('-D', '--dst', type = 'string', dest = 'destination',
					  help = 'The destination message to send to.')
	parser.add_option('-M', '--message', type = 'string', dest = 'message',
					  help = 'The message(in json data structure) want to send.')
	parser.add_option('-R', '--retry', type = 'int', dest = 'retry_times', default = '3',
					  help = 'The times to retry to send the message when failed.')
	parser.add_option('-H', '--host', type = 'string', dest = 'host', default = 'amq.wintim.com',
					  help = 'Hostname or IP to connect to. Defaults to dm.wintim.com if not specified.')
	parser.add_option('-P', '--port', type = int, dest = 'port', default = 61613,
					  help = 'Port providing stomp protocol connections. Defaults to 61613 if not specified.')

	(options, args) = parser.parse_args()

	if options.destination is None or options.message is None:
		print>>sys.stderr, "The destination and the message must been set.\n"
		parser.print_help(sys.stderr)
		sys.exit(1)
	
	try:
		send_message(options.destination, options.message.decode('gb18030'), options.retry_times, options.host, options.port)
		print 'Succeed to send message.'
	except Exception, e:
		try:
			send_message(options.destination, options.message.decode('utf-8'), options.retry_times, options.host, options.port)
			print 'Succeed to send message.'
		except Exception, e1:
			print>>sys.stderr, "Send message failed with", e1
			sys.exit(1)
			