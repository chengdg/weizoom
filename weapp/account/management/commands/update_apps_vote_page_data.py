# -*- coding: utf-8 -*-

import time
import re

from django.core.management.base import BaseCommand, CommandError

from termite import pagestore as pagestore_manager
from apps.customerized_apps.vote import models as app_models


class Command(BaseCommand):
	help = 'update vote page'
	args = ''
	
	def handle(self, **options):
		print 'update vote page start...'
		try:
			#从page中取出数据
			pagestore = pagestore_manager.get_pagestore('mongo')
			for vote in app_models.vote.objects.all():
				related_page_id = vote.related_page_id

				page = pagestore.get_page(related_page_id, 1)
				components = page['component']
				print 'get components', type(components)
				components_str = str(components)
				#替换内容
				print 'replace appkit.selection'
				components_str = components_str.replace('appkit.selection', 'appkit.textselection')
				print 'replace appkit.selectionitem'
				components_str = components_str.replace('appkit.selectitem', 'appkit.textselectionitem')
				components = eval(components_str)

				#保存page
				pagestore.save_page(related_page_id, 1, components)
			print 'update vote page end...'
		except Exception, e:
			print 'update vote page fail...', e