# -*- coding: utf-8 -*-
__author__ = 'liupeiyu'

from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
import xlwt

"""
导出盛景数据，包括 手机号、姓名、公司
"""

class Command(BaseCommand):
	help = "start export shengjing data ..."
	args = ''

	def get_shengjing_data(self):
		from apps.customerized_apps.shengjing import models as shengjing_models

		bindings = shengjing_models.ShengjingBindingMember.objects.exclude(member_id=0).order_by('-created_at')
		binding_ids = [b.id for b in bindings]
		member_infos = shengjing_models.ShengjingBindingMemberInfo.objects.filter(binding__in=binding_ids)
		member_companys = shengjing_models.ShengjingBindingMemberHasCompanys.objects.filter(binding__in=binding_ids)

		print 'count =',bindings.count()

		info2binding_id = dict([(i.binding_id, i) for i in member_infos])
		for index,binding in enumerate(bindings):
			info_name = ''
			if info2binding_id.has_key(binding.id):
				info_name = info2binding_id[binding.id].name
			binding.info_name = info_name

			company_names = []
			companys = member_companys.filter(binding_id=binding.id)
			for company in companys:
				company_names.append(company.name)
			binding.company_name = ','.join(company_names)
			# print binding.company_name
			if index%30==0:
				print '*',

		print ''		
		return bindings


	def create_xml_file(self, data):
		file_name = "shengjing-{}.xls".format(datetime.now().strftime("%Y%m%d_%H%M%S"))
		wb = xlwt.Workbook(encoding = 'utf-8')
		ws = wb.add_sheet(u'盛景学员', cell_overwrite_ok=False)

		font = xlwt.Font()
		font.name = 'Times New Roman'
		font.bold = True
		font.height = 0x00c9
		font.shadow = True
		style = xlwt.XFStyle()
		style.font = font


		index = 0
		ws.write(index, 0, u'id', style)
		ws.write(index, 1, u'注册时间', style)
		ws.write(index, 2, u'手机号码', style)
		ws.write(index, 3, u'姓名', style)
		ws.write(index, 4, u'公司', style)
		ws.col(1).width = 256 * 22 
		ws.col(2).width = 256 * 20
		ws.col(4).width = 256 * 40

		for item in data:
			if item.info_name is '' or item.info_name is None:
				continue

			index = index + 1
			ws.write(index, 0, item.id)
			ws.write(index, 1, item.created_at.strftime("%Y-%m-%d %H:%M:%S"))			
			ws.write(index, 2, item.phone_number)
			ws.write(index, 3, item.info_name)
			ws.write(index, 4, item.company_name)

			if index%30==0:
				print '.',

		print ''
		print '---- file name: {}'.format(file_name)
		wb.save(file_name);

	def handle(self, **options):
		"""
		重新发送未成功的快递订阅请求service
		"""

		print "----------------start export shengjing data ..."

		# 获取数据
		datas = self.get_shengjing_data()

		# 生成xml
		self.create_xml_file(datas)

		print '... end'
