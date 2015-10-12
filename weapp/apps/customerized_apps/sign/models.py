# -*- coding: utf-8 -*-

import datetime
from django.conf import settings

import mongoengine as models
from modules.member.module_api import get_member_by_openid

class SignParticipance(models.Document):
	webapp_user_id= models.LongField(default=0) #参与者id
	member_id= models.LongField(default=0) #参与者id
	belong_to = models.StringField(default="", max_length=100) #对应的活动id
	tel = models.StringField(default="", max_length=100)
	prize = models.DynamicField(default="") #活动奖励
	created_at = models.DateTimeField() #创建时间&第一次签到时间
	latest_date = models.DateTimeField() #最后一次签到时间
	total_count = models.IntField(default=0) #总签到天数
	serial_count = models.IntField(default=0) #连续签到天数
	top_serial_count = models.IntField(default=0) #最高连续签到天数

	meta = {
		'collection': 'sign_sign_participance'
	}

	def do_signment(self, sign):
		return_data = {
			'status_code': RETURN_STATUS_CODE['SUCCESS'],
		}
		nowDate = datetime.datetime.now()
		#用户签到操作
		user_update_data = {
			'set__latest_date': nowDate,
			'inc__total_count': 1
		}
		latest_date = self.latest_date
		#判断是否已签到
		if latest_date and latest_date.strftime('%Y-%m-%d') == nowDate.strftime('%Y-%m-%d'):
			return_data['status_code'] = RETURN_STATUS_CODE['ALREADY']
			return_data['errMsg'] = u'今日已签到'
			return return_data
		#判断是否连续签到，否则重置为1
		if latest_date == nowDate - datetime.timedelta(days=1):
			user_update_data['inc__serial_count'] = 1
		else:
			user_update_data['set__serial_count'] = 1
		#如果当前连续签到大于等于最高连续签到，则更新最高连续签到
		curr_serial_count = 1
		if self.serial_count >= self.top_serial_count:
			curr_serial_count = user_update_data['set__top_serial_count'] = int(self.serial_count) + 1
		#更新prize
		curr_prize_integral = daily_integral = serial_integral = next_serial_integral = next_serial_count = 0
		curr_prize_coupon_id = daily_coupon_id = serial_coupon_id = next_serial_coupon_id = ''
		curr_prize_coupon_name = daily_coupon_name = serial_coupon_name = next_serial_coupon_name = ''
		#首先获取奖项配置
		prize_settings = sign.prize_settings
		bingo = 0
		flag = False
		for name in sorted(prize_settings.keys()):
			setting = prize_settings[name]
			if flag or int(name)>curr_serial_count:
				next_serial_count = name
				for type, value in setting.items():
					if type == 'integral':
						next_serial_integral = value
					elif type == 'coupon':
						next_serial_coupon_id = value['id'] if value != '' else ''
						next_serial_coupon_name = value['name']
				break
			if int(name) == 0:
				#每日奖励和达到连续签到要求的奖励
				for type, value in setting.items():
					if type == 'integral':
						daily_integral = int(value)
					elif type == 'coupon':
						daily_coupon_id = value['id'] if value != '' else ''
						daily_coupon_name = value['name']
			if int(name) == curr_serial_count:
				#达到连续签到要求的奖励
				bingo = curr_serial_count
				flag = True
				for type, value in setting.items():
					if type == 'integral':
						serial_integral = int(value)
					elif type == 'coupon':
						serial_coupon_id = value['id'] if value != '' else ''
						serial_coupon_name = value['name']
		user_prize = self.prize
		temp_coupon_list = user_prize['coupon'].split(',')
		temp_coupon_list = [] if temp_coupon_list == [''] else temp_coupon_list #防止出现[''].append(x)再用join时出现前置逗号的问题
		#若命中连续签到，则不奖励每日签到
		if bingo == curr_serial_count:
			user_prize['integral'] = int(user_prize['integral']) + serial_integral
			if serial_coupon_name:
				temp_coupon_list.append(serial_coupon_name)
				curr_prize_coupon_id = serial_coupon_id
				curr_prize_coupon_name = serial_coupon_name
			curr_prize_integral = serial_integral
		else:
			user_prize['integral'] = int(user_prize['integral']) + daily_integral
			if daily_coupon_name:
				temp_coupon_list.append(daily_coupon_name)
				curr_prize_coupon_id = daily_coupon_id
				curr_prize_coupon_name = daily_coupon_name
			curr_prize_integral = daily_integral

		user_prize['coupon'] = ','.join(temp_coupon_list)
		user_update_data['set__prize'] = user_prize
		self.update(**user_update_data)
		self.reload()
		#更新签到参与人数
		sign.update(inc__participant_count=1)

		return_data['curr_prize_integral'] = curr_prize_integral
		return_data['curr_prize_coupon_id'] = curr_prize_coupon_id
		return_data['curr_prize_coupon_name'] = curr_prize_coupon_name
		return_data['daily_integral'] = daily_integral
		return_data['daily_coupon_id'] = daily_coupon_id
		return_data['daily_coupon_name'] = daily_coupon_name
		return_data['next_serial_count'] = next_serial_count
		return_data['next_serial_integral'] = next_serial_integral
		return_data['next_serial_coupon_id'] = next_serial_coupon_id
		return_data['next_serial_coupon_name'] = next_serial_coupon_name
		return_data['reply_content'] = sign.reply['content']
		return_data['serial_count'] = self.serial_count

		return return_data

STATUS_NOT_START = 0
STATUS_RUNNING = 1
STATUS_STOPED = 2

RETURN_STATUS_CODE = {
	'ERROR': 0,
	'SUCCESS': 1,
	'NONE': 2,
	'ALREADY': 3
}
class Sign(models.Document):
	owner_id = models.LongField() #创建人id
	name = models.StringField(default="", max_length=100) #名称
	share = models.DynamicField(default="") #分享设置
	reply = models.DynamicField(default="") #自动回复设置
	prize_settings = models.DynamicField(default="") #签到奖项设置
	status = models.IntField(default=0) #状态
	participant_count = models.IntField(default=0) #参与者数量
	related_page_id = models.StringField(default="", max_length=100) #termite page的id
	created_at = models.DateTimeField() #创建时间
	
	meta = {
		'collection': 'sign_sign'
	}


	@staticmethod
	def do_auto_signment(data):
		"""
		回复关键字自动签到
		:param data: 字典 :包含 webapp_owner_id, openid, keyword, webapp_id
		:return: html片段
		"""
		return_html = []
		host = settings.DOMAIN
		try:
			sign = Sign.objects.get(owner_id=data['webapp_owner_id'])
			print data['keyword'], sign.reply['keyword']
			if sign.status != 1:
				return_html.append(u'签到活动未开始')
			elif data['keyword'] == sign.reply['keyword']:
				# add by bert  增加获取会员代码
				member = get_member_by_openid(data['openid'], data['webapp_id'])
				if not member:
					return None
				signer = SignParticipance.objects(member_id=member.id, belong_to=str(sign.id))
				if signer.count() == 0:
					signer = SignParticipance(
						belong_to = str(sign.id),
						member_id = member.id,
						prize = {
							'integral': 0,
							'coupon': ''
						},
						created_at= datetime.datetime.today()
					)
					signer.save()
				else:
					signer = signer[0]
				return_data = signer.do_signment(sign)
				if return_data['status_code'] == RETURN_STATUS_CODE['ALREADY']:
					return_html.append(u'亲，今天您已经签到过了哦，明天再来吧！\n')
				if return_data['status_code'] == RETURN_STATUS_CODE['SUCCESS']:
					return_html.append(u'签到成功！\n已连续签到%s天\n本次签到获得以下奖励：' % return_data['serial_count'])
					return_html.append(str(return_data['curr_prize_integral']))
					return_html.append(u'积分\n')
					if return_data['curr_prize_coupon_name'] != '':
						return_html.append(return_data['curr_prize_coupon_name'])
						return_html.append(u'\n<a href="http://%s/termite/workbench/jqm/preview/?module=user_center&model=user_info&action=get&workspace_id=mall&webapp_owner_id=%s">点击查看</a>\n' % (host, data['webapp_owner_id']))
					return_html.append(u'签到说明：签到有礼！\n')
					return_html.append(return_data['reply_content'])
				return_html.append(u'\n<a href="http://%s/m/apps/sign/m_sign/?webapp_owner_id=%s"> 点击查看详情</a>' % (host, data['webapp_owner_id']))
			else:
				return None
		except:
			return None
		return ''.join(return_html)

	@property
	def status_text(self):
		return (u'未开始', u'进行中', u'已结束')[int(self.status)]

	@property
	def is_finished(self):
		status_text = self.status_text
		if status_text == u'已结束':
			return True
		else:
			return False


	
