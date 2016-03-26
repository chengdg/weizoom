#coding:utf8
from celery import task
from models import *
from modules.member.models import *
from core import upyun_util
from member_list import get_member_orders
from watchdog.utils import watchdog_error
from core.exceptionutil import unicode_full_stack
import xlwt
import os
import time

@task(bind=True, max_retries=2)
def send_export_job_task(self, exportjob_id, filter_data_args, sort_attr, type, filename):

	export_jobs = ExportJob.objects.filter(id=exportjob_id)
	if type == 0:
		try:
			members = Member.objects.filter(**filter_data_args).order_by(sort_attr)
			file = xlwt.Workbook(encoding='utf-8')
			table = file.add_sheet('name',cell_overwrite_ok=True)



			members_info = [u'ID', u'昵称',u'性别',u'备注名',
				 u'姓名',u'电话',u'QQ',u'微博',u'备注',u'积分',u'经验值',u'会员等级',u'好友数',u'好友关系',
				 u'贡献数',u'贡献关系',u'来源',u'加入时间',u'分享总数',u'分享链接',u'链接点击',u'订单数',u'订单号',u'金额',u'状态',u'社交因子']
			for i in range(len(members_info)):
				table.write(0, i, members_info[i])
			member_count = members.count()
			export_jobs.update(count=member_count)
			tmp_count = 0
			for member in members:
				time.sleep(3)
				count_list = []
				id = member.id
				nike_name = member.username
				try:
					nike_name = nike_name.decode('utf8')
				except:
					nike_name = member.username_hexstr
				remarks_name = member.remarks_name
				integral = member.integral
				experience = member.experience
				grade = member.grade.name


				friend_members = MemberFollowRelation.get_follow_members_for(member.id)
				friend_count = len(friend_members)
				count_list.append(friend_count)

				fans_members  = MemberFollowRelation.get_follow_members_for(member.id, '1')
				fans_count = len(fans_members)
				count_list.append(fans_count)

				factor = member.factor
				source = member.source
				created_at = member.created_at

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
				qq_number = u''
				weibo_nickname = u''
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
					qq_number = member_info.qq_number
					weibo_nickname = member_info.weibo_nickname
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
					else:
						order_id = ''
						status = ''
						final_price = ''

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
								qq_number,
								weibo_nickname,
								member_remarks,
								integral,
								experience,
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
								factor
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
								''
							]
					tmp_count += 1
					export_jobs.update(processed_count=tmp_count)
					for i in range(len(info_list)):
						table.write(tmp_count, i, info_list[i])
					
			filename = "member_{}.xls".format(exportjob_id)
			file.save(filename)
			export_jobs.update(status=1)
			upyun_path = '/upload/excel/{}'.format(filename)
			yun_url = upyun_util.upload_audio_file(filename, upyun_path)
			print "yun_url>>>>>",yun_url
			export_jobs.update(file_path=yun_url)
			os.remove(filename)
			 
		except:
			notify_message = "导出会员任务失败,response:{}".format(unicode_full_stack())
			watchdog_error(notify_message)


