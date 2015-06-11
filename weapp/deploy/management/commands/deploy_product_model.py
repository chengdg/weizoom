# -*- coding: utf-8 -*-

import os
import subprocess

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from mall.models import ProductModel, Product

class Command(BaseCommand):
	help = "create standard product model for existed product if necessary"
	args = ''
	
	def handle(self, **options):
		counter = 0
		for product in Product.objects.all():
			if ProductModel.objects.filter(product=product, name='standard').count() != 0:
				pass

			ProductModel.objects.create(
				owner = product.owner,
				product = product,
				name = 'standard',
				is_standard = True,
				price = product.price,
				weight = product.weight,
				stock_type = product.stock_type,
				stocks = product.stocks
			)
			counter += 1

		print 'create %d standard models' % counter


