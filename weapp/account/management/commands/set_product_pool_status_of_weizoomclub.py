# -*- coding: utf-8 -*-
__author__ = 'zph'


import json
import math
import os
import random
import time
import datetime
import requests
from collections import OrderedDict
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from mall import models as mall_models

import xlrd
import sys

#####################################
#清除商品过期促销标题
#####################################
class Command(BaseCommand):
	def handle(self, **options):
		woid = User.objects.get(username = 'weizoomclub').id
		data = xlrd.open_workbook(u'./account/management/weizoomclub批量上架的商品清单.xlsx')
		table = data.sheet_by_index(0)
		nrows = table.nrows
		names = []
		for row in range(1,nrows):
			name = table.cell(row,0).value
			names.append(name)

		products = mall_models.Product.objects.filter(name__in = names,owner_id = woid)
		product_ids = [product.id for product in products]
		
		mall_models.ProductPool.objects.filter(woid = woid).update(status =0)
		for product_id in product_ids:
			mall_models.ProductPool.objects.filter(woid = woid,product_id = product_id).update(status =1)