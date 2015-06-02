# -*- coding: utf-8 -*-
__author__ = 'liupeiyu'
import os
import subprocess

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from webapp.modules.mall.models import *
import webapp.modules.mall.module_api as mall_api

class Command(BaseCommand):
	help = "update product postage and pay"
	args = ''
	
	def handler_product(self):
		users = User.objects.all()
		for user in users:
			print u'---------------- {}'.format(user.username)
			# 获取默认的运费
			postage = mall_api.get_default_postage_by_owner_id(owner_id=user.id)
			if postage:
				print u'处理该用户下的所有商品, 运费id={}'.format(postage.id)
				# 修改该用户下的所有商品的运费
				Product.objects.filter(owner_id=user.id).update(postage_id=postage.id)

			# 是否有货到付款支付方式
			pay_interface = mall_api.get_pay_interface_cod_by_owner_id(owner_id=user.id)
			if pay_interface:
				# 修改该用户下的所有商品都支持货到付款
				print u'处理该用户下的所有商品, 支持货到付款'
				Product.objects.filter(owner_id=user.id).update(is_use_cod_pay_interface=True)

	def handle(self, **options):
		print 'start handler product postage and pay'
		self.handler_product()
		print 'end handler product postage and pay'

