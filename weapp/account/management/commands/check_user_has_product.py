# -*- coding: utf-8 -*-

import os
import subprocess

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from product.models import Product, UserHasProduct

class Command(BaseCommand):
	help = "check user's products"
	args = ''
	
	def handle(self, **options):
		all_users = [user for user in User.objects.all() if (user.username != 'admin' and user.username != 'manager')]
		id2user = dict([(user.id, user) for user in all_users])
		has_product_user_ids = [relation.owner_id for relation in UserHasProduct.objects.all()]
		all_user_ids = [user.id for user in all_users]
		no_product_user_ids = set(all_user_ids) - set(has_product_user_ids)

		print u'1. 下列用户没有Weapp Product：'
		print '\tID\tNAME'
		for user_id in no_product_user_ids:
			print '\t%d\t%s' % (user_id, id2user[user_id].username)

		print u'\n2. 系统中现有以下Weapp Product:'
		print '\tID\tNAME'
		product_ids = set()
		for product in Product.objects.all():
			print '\t%d\t%s' % (product.id, product.name)
			product_ids.add(str(product.id))

		product_id = None
		while True:
			print u'\n请输入Weapp Product的id，为没有Weapp Product的用户安装Product'
			print u'>>>',
			product_id = raw_input()
			if not product_id in product_ids:
				print u'输入的id值(%s)错误' % id
				continue
			else:
				break 

		if product_id:
			for user_id in no_product_user_ids:
				print u'为用户%s(%d)安装Weapp Product' % (id2user[user_id].username, user_id)
				UserHasProduct.objects.create(
					owner_id = user_id,
					product_id = product_id
				)

		print 'finish!'
