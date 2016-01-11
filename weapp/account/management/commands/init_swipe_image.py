# -*- coding: utf-8 -*-

import os
import subprocess

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from mall.models import Product, ProductSwipeImage

class Command(BaseCommand):
	help = "init mall counter for all user"
	args = ''
	
	def handle(self, **options):
		for product in Product.objects.all():
			if ProductSwipeImage.objects.filter(product=product).count() > 0:
				continue

			print 'create swipe image for product: ', product.name
			ProductSwipeImage.objects.create(
				product = product,
				url = product.pic_url
			)

