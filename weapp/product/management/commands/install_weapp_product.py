# -*- coding: utf-8 -*-

import os
import subprocess

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from product import module_api as weapp_product_api
from product.models import Product

class Command(BaseCommand):
	help = "install product for user"
	args = '[username] [product name]'
	
	def handle(self, username, product_name, **options):
		user = User.objects.get(username=username)
		product = Product.objects.get(name=product_name)

		weapp_product_api.install_product_for_user(user, product.id)