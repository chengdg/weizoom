# -*- coding: utf-8 -*-

import os
import subprocess
from datetime import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from django.dispatch import Signal
from django.dispatch.dispatcher import receiver

check_order_related_resource = Signal(providing_args=["params"])
consume_order_related_resource = Signal(providing_args=["params"])
post_save_order = Signal(providing_args=["order"])

class Request(object):
		def __init__(self):
			pass

class Order(object):
	def __init__(self, id):
		self.id = id

class Mall(object):
	def save_order(self, request):
		responses = check_order_related_resource.send(sender=Mall, params=request.GET)
		failed_response = filter(lambda response: True if not response[1]['success'] else False, responses)
		if failed_response:
			print '[Mall:save_order]: ', failed_response[0][1]['error_msg']
			return

		order = Order("order1")
		post_save_order.send(sender=Mall, order=order)


@receiver(check_order_related_resource, sender=Mall)
def check_order_coupon(params, **kwargs):
	print '[coupon]: check order coupon ', params['coupon']
	if params['coupon'] < 0:
		return {
			'success': False, 
			'error_msg': 'invalid coupon'
		}
	else:
		return {
			'success': True
		}

@receiver(check_order_related_resource, sender=Mall)
def check_order_integral(params, **kwargs):
	print '[integral]: check order integral ', params['integral']
	return {
		'success': True
	}

@receiver(post_save_order, sender=Mall)
def order_logger(order, **kwargs):
	print '[order_logger]: successfully save order ', order.id


class Command(BaseCommand):
	help = "change market tool to app"
	args = ''
	
	def handle(self, **options):
		mall = Mall()
		request = Request()
		request.GET = {
			'coupon': 20,
			'integral': 3
		}
		print '===== save 1 ====='
		mall.save_order(request)

		print '===== save 2 ====='
		request.GET = {
			'coupon': -20,
			'integral': 3
		}
		mall.save_order(request)


