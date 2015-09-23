# -*- coding: utf-8 -*-

import datetime

import mongoengine as models

class SignParticipance(models.Document):
	webapp_user_id= models.LongField(default=0) #参与者id
	member_id= models.LongField(default=0) #参与者id
	belong_to = models.StringField(default="", max_length=100) #对应的活动id
	tel = models.StringField(default="", max_length=100)
	termite_data = models.DynamicField(default="") #termite数据
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
			'status_code': RETURN_STATUS_CODE['ERROR'],
		}
		nowDate = datetime.datetime.now()

		return_data['status_code'] = RETURN_STATUS_CODE['SUCCESS']
		#用户签到操作
		user_update_data = {
			'set__latest_date': nowDate,
			'inc__total_count': 1
		}
		#判断是否连续签到，否则重置为1
		latest_date = self.latest_date
		if latest_date == nowDate - datetime.timedelta(days=1):
			user_update_data['inc__serial_count'] = 1
		else:
			user_update_data['set__serial_count'] = 1
		#如果当前连续签到大于等于最高连续签到，则更新最高连续签到
		curr_serial_count = 1
		if self.serial_count >= self.top_serial_count:
			curr_serial_count = user_update_data['set__top_serial_count'] = self.serial_count + 1
		#更新prize
		daily_integral = serial_integral = 0
		daily_coupon_id = serial_coupon_id = ''
		#首先获取奖项配置
		prize_settings = sign.prize_settings
		for name in sorted(prize_settings.keys()):
			setting = prize_settings[name]
			if int(name) == 0:
				#每日奖励和达到连续签到要求的奖励
				for type, value in setting.items():
					if type == 'integral':
						daily_integral += int(value)
					elif type == 'coupon':
						daily_coupon_id = value
			if int(name) == curr_serial_count:
				#达到连续签到要求的奖励
				for type, value in setting.items():
					if type == 'integral':
						serial_integral += int(value)
					elif type == 'coupon':
						serial_coupon_id = value
		user_prize = self.prize
		user_prize['integral'] += daily_integral + serial_integral
		temp_coupon_list = user_prize['coupon'].split(',')
		if daily_coupon_id != '':
			temp_coupon_list.append(daily_coupon_id)
		if serial_coupon_id != '':
			temp_coupon_list.append(serial_coupon_id)
		user_prize['coupon'] = temp_coupon_list.join(',')
		user_update_data['set__prize'] = user_prize
		self.update(**user_update_data)
		#更新签到参与人数
		sign.update(inc__participant_count=1)

		return_data['daily_integral'] = daily_integral
		return_data['daily_coupon_id'] = daily_coupon_id
		return_data['serial_integral'] = serial_integral
		return_data['serial_coupon_id'] = serial_coupon_id

		return return_data

STATUS_NOT_START = 0
STATUS_RUNNING = 1
STATUS_STOPED = 2

RETURN_STATUS_CODE = {
	'ERROR': 0,
	'SUCCESS': 1,
	'NONE': 2
}
class Sign(models.Document):
	owner_id = models.LongField() #创建人id
	name = models.StringField(default="", max_length=100) #名称
	# start_time = models.DateTimeField() #开始时间
	# end_time = models.DateTimeField() #结束时间
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
	def get_auto_sign_data(data):
		return_data = {}
		try:
			sign = Sign.objects.get(owner_id=data.owner_id)
			if sign.status != 1:
				return_data['errMsg'] = u'签到活动未开始'
			elif data.keyword == sign.reply.keyword:
				user = SignParticipance.objects.get(member_id=data.member_id, belong_to=sign.id)
				return_data = user.do_signment(sign)
			else:
				return_data['status_code'] = RETURN_STATUS_CODE['NONE']
				return_data['errMsg'] = u'关键字不匹配'
		except Exception, e:
			print e
			return_data['status_code'] = RETURN_STATUS_CODE['ERROR']
		return return_data

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


	
