# -*- coding: utf-8 -*-
#__auth__='justiing'
import logging
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db.models import Q,F

#邮件部分
from core.sendmail import sendmail


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
from tools.regional.models import *
from mall.models import *
from account.models import UserProfile
import xlsxwriter

from datetime import datetime,timedelta,date
DATE_FORMAT="%Y-%m-%d"


class Command(BaseCommand):
	help = "send product sales email"
	args = ''
	
	def handle(self,*args, **options):
			print args

			week_day = datetime.now().weekday()
			current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

			first_day = "{}-01".format(current_time.rsplit('-',1)[0])

			file_path = 'product_pool_55.xlsx'
			workbook   = xlsxwriter.Workbook(file_path)
			table = workbook.add_worksheet()
			alist = [u'未上架55分成商品', u"供货商"]
			
			pool_weapp_profile = UserProfile.objects.filter(webapp_type=2).first()
			owner_pool = User.objects.get(id=pool_weapp_profile.user_id)

			id2usr_profiles = dict([(s.id, s) for s in UserProfile.objects.filter(webapp_type = 1).filter(~Q(user_id__in=[968, 930,816, 16,529]))])
			manager_supplier_ids2name = dict([(s.id, s.name) for s in Supplier.objects.filter(owner_id=pool_weapp_profile.user_id, type = 0)])
			product_ids = Product.objects.filter(owner=owner_pool, supplier__in=manager_supplier_ids2name.keys()).values_list('id', flat=True)
			
			product_ids = ProductPool.objects.filter(status=PP_STATUS_ON_POOL, product_id__in=product_ids).filter(~Q(woid__in=[968, 930,816, 16,529])).values_list('product_id', flat=True)
			id2products =  dict([(s.id, s) for s in Product.objects.filter(id__in=product_ids)])
			woid_pids2pool = dict([(str(p.woid)+'_'+str(p.product_id), p) for p in ProductPool.objects.filter(product_id__in=product_ids).filter(~Q(woid__in=[968, 930,816, 16,529]))])
			woid_pids = woid_pids2pool.keys()
			for id, value in id2usr_profiles.items():
				alist.append(value.store_name)
			table.write_row('A1',alist)

			tmp_line = 1
			for product_id, product in id2products.items():
				tmp_line += 1
				tmp_list = [product.name, manager_supplier_ids2name[product.supplier]]

				for profile_id, profile in id2usr_profiles.items():
					current_key = str(profile.user_id) + '_' +str(product_id)
					if current_key in woid_pids:
						if woid_pids2pool[current_key].status == PP_STATUS_ON_POOL:
							tmp_list.append(u"否")
						else:
							tmp_list.append(u"是")
					else:
						tmp_list.append(u"未同步")

				table.write_row('A{}'.format(tmp_line),tmp_list)

			workbook.close()
			receivers = ['guoyucheng@weizoom.com','mengqi@weizoom.com','zhangzhiyong@weizoom.com']
			mode = ''
			if len(args) == 1:
				if args[0] == 'test':
					mode = 'test'
					receivers = ['guoyucheng@weizoom.com']
			title = u'微众自运营平台未上架55分成商品{}'.format(current_time)
			content = u'您好，微众自运营平台未上架55分成商品'

			sendmail(receivers, title, content, mode, file_path)

