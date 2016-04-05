#coding:utf8
from celery import task
from account.models import ExportJob
from modules.member.models import *
from core import upyun_util
from member_list import get_member_orders
from watchdog.utils import watchdog_error
from core.exceptionutil import unicode_full_stack
from django.conf import settings
from mall.models import Order, STATUS2TEXT,ORDER_STATUS_SUCCESSED
import xlsxwriter
import os
import time

@task(bind=True, time_limit=7200, max_retries=2)
def send_export_job_task(self, exportjob_id, filter_data_args, sort_attr, type, filename):

	export_jobs = ExportJob.objects.filter(id=exportjob_id)
	if type == 0:
		filename = "member_{}.xlsx".format(exportjob_id)
		dir_path_excel = "excel"
		dir_path = os.path.join(settings.UPLOAD_DIR, dir_path_excel)
		file_path = "{}/{}".format(dir_path,filename)
		workbook   = xlsxwriter.Workbook(file_path)
		table = workbook.add_worksheet()
		try:
			members = Member.objects.filter(**filter_data_args).order_by(sort_attr)

			members_info = [u'ID', u'昵称',u'性别',u'备注名',
				 u'姓名',u'绑定手机号',u'备注',u'积分',u'会员等级',u'好友数',u'好友关系',
				 u'贡献数',u'贡献好友',u'来源',u'加入时间',u'分享总数',u'分享链接',u'链接点击',u'订单数',u'订单号',u'金额',u'状态',u'购买次数',u'收货人',u'电话',u'地址']
			for i in range(len(members_info)):
				table.write(0, i, members_info[i])
			member_count = members.count()
			export_jobs.update(count=member_count)
			tmp_count = 0
			member_count_write = 0
			for member in members:
				count_list = []
				id = member.id
				nike_name = member.username
				try:
					nike_name = nike_name.decode('utf8')
				except:
					nike_name = member.username_hexstr
				remarks_name = member.remarks_name
				integral = member.integral
				grade = member.grade.name


				friend_members = MemberFollowRelation.get_follow_members_for(member.id)
				friend_count = len(friend_members)
				count_list.append(friend_count)

				fans_members  = MemberFollowRelation.get_follow_members_for(member.id, '1')
				fans_count = len(fans_members)
				count_list.append(fans_count)

				source = member.source
				created_at = "{}".format(member.created_at)

				if source == 0:
					source = u'直接关注'

				if source == 1:
					source = u'推广扫描'

				if source == 2:
					source = u'会员分享'

				if source == -1:
					source = u'直接关注'

				shared_url_infos = MemberSharedUrlInfo.get_member_share_url_info(member.id)
				share_urls_count = len(shared_url_infos)
				count_list.append(share_urls_count)

				member_orders = get_member_orders(member)
				pay_times = member_orders.filter(status=ORDER_STATUS_SUCCESSED).count()

				if member_orders != None:
					member_orders_count = len(member_orders)
				else:
					member_orders_count = 0
					member_orders = []
				count_list.append(member_orders_count)

				member_info =  MemberInfo.get_member_info(member.id)
				name = u''
				sex = u''
				phone_number = u''
				member_remarks = u''
				if member_info:
					name = member_info.name
					sex = member_info.sex
					if sex != -1:
						if sex == 1:
							sex = u'男'
						elif sex == 2:
							sex = u'女'
						else:
							sex = u'未知'
					else:
						sex = u'未知'
					phone_number = member_info.phone_number
					member_remarks = member_info.member_remarks

				max_count = max(count_list)
				if max_count == 0:
					max_count = 1
				for index in range(max_count):
					share_url = shared_url_infos[index] if share_urls_count > index else None
					if share_url:
						share_url_title = share_url.title
						pv = share_url.pv
					else:
						share_url_title = ''
						pv = ''

					member_order = member_orders[index] if member_orders_count > index else None
					if member_order:
						order_id = member_order.order_id
						status = STATUS2TEXT[member_order.status]
						final_price = member_order.final_price
						area = member_order.get_str_area
						ship_name = member_order.ship_name
						ship_tel = member_order.ship_tel
						ship_address = member_order.ship_address
						ship_address = "{} {}".format(area,ship_address)
					else:
						order_id = ''
						status = ''
						final_price = ''
						ship_name = ''
						ship_tel = ''
						ship_address = ''

					friend_member = friend_members[index] if friend_count > index else None
					if friend_member:
						friend_name = friend_member.username
						try:
							friend_name = friend_name.decode('utf8')
						except:
							friend_name = friend_member.username_hexstr
					else:
						friend_name = ''

					fans_member = fans_members[index] if fans_count > index else None
					if fans_member:
						fans_name = fans_member.username
						try:
							fans_name = fans_name.decode('utf8')
						except:
							fans_name = fans_member.username_hexstr
					else:
						fans_name = ''

					if index == 0:
						info_list = [ id,
								nike_name,
								sex,
								remarks_name,
								name,
								phone_number,
								member_remarks,
								integral,
								grade,
								friend_count,
								friend_name,
								fans_count,
								fans_name,
								source,
								created_at,
								share_urls_count,
								share_url_title,
								pv,
								member_orders_count,
								order_id,
								final_price,
								status,
								pay_times,
								ship_name,
								ship_tel,
								ship_address,
							]
					else:
						info_list = ['',
								'',
								'',
								'',
								'',
								'',
								'',
								'',
								'',
								'',
								friend_name,
								'',
								fans_name,
								'',
								'',
								'',
								share_url_title,
								pv,
								'',
								order_id,
								final_price,
								status,
								'',
								ship_name,
								ship_tel,
								ship_address,
							]
					tmp_count += 1
					for i in range(len(info_list)):
						table.write(tmp_count, i, info_list[i])
				member_count_write += 1
				export_jobs.update(processed_count=member_count_write,update_at=datetime.now())
			workbook.close()
			upyun_path = '/upload/excel/{}'.format(filename)
			yun_url = upyun_util.upload_image_to_upyun(file_path, upyun_path)
			export_jobs.update(status=1,file_path=yun_url,update_at=datetime.now())

			 
		except:
			notify_message = "导出会员任务失败,response:{}".format(unicode_full_stack())
			export_jobs.update(status=2,is_download=1)
			watchdog_error(notify_message)



