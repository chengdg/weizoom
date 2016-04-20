# -*- coding: utf-8 -*-

__author__ = 'bert'

import json, logging
from kafka import KafkaProducer


class KafkaProducerClient(object):
	"""docstring for KafkaProducerClient"""
	def __init__(self, bootstrap_servers=['localhost:9092'], retries=3):
		logging.info("init KafkaProducerClient")
		super(KafkaProducerClient, self).__init__()
		try:
			self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers, retries=retries)
		except Exception, e:
			logging.error(e)
	
	def send_message(self, topic, message, partition=None):
		#try:
		self.producer.send(topic, json.dumps(message), partition=partition)
		#except Exception, e:
		#	raise e
		
kafkaProducerClient = KafkaProducerClient()

def send_message(topic, message, partition=None):
	#TODO :异常收集
	#try:
	kafkaProducerClient.send_message(topic, message, partition)
	#except Exception, e:
	#	raise e
