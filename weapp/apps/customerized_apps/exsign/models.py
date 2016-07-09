# -*- coding: utf-8 -*-

import datetime
from django.conf import settings

import mongoengine as models
from mongoengine.queryset.visitor import Q

from modules.member.module_api import get_member_by_openid

from modules.member import models as member_models
from mall.promotion.models import CouponRule
from termite import pagestore as pagestore_manager

class exSignDetails(models.Document):
	"""
	签到详情记录表
	"""
	member_id= models.LongField(default=0) #参与者id
	belong_to = models.StringField(default="", max_length=100) #对应的活动id
	created_at = models.DateTimeField() #创建时间
	prize = models.DynamicField() #奖励信息
	type = models.StringField(default=u"页面签到", max_length=20) #页面签到 or 自动签到

	meta = {
		'collection': 'exsign_exsign_details',
		'db_alias': 'apps'
	}

class exSignControl(models.Document):
	member_id= models.LongField(default=0) #参与者id
	belong_to = models.StringField(default="", max_length=100) #对应的活动id
	sign_control = models.StringField(default="", max_length=100, unique_with=['belong_to', 'member_id'])

	meta = {
		'collection': 'exsign_exsign_control',
		'db_alias': 'apps'
	}

class exSignParticipance(models.Document):
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
		'collection': 'exsign_exsign_participance',
		'db_alias': 'apps'
	}

	def do_signment(self, exsign, grade_id):
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
		if latest_date and latest_date.strftime('%Y-%m-%d') == nowDate.strftime('%Y-%m-%d') and self.serial_count != 0:
			return_data['status_code'] = RETURN_STATUS_CODE['ALREADY']
			return_data['errMsg'] = u'今日已签到'
			return return_data
		#判断是否连续签到，否则重置为1
		if latest_date and latest_date.strftime('%Y-%m-%d') == (nowDate - datetime.timedelta(days=1)).strftime('%Y-%m-%d'):
			user_update_data['inc__serial_count'] = 1
			curr_serial_count = temp_curr_serial_count = int(self.serial_count) + 1
		else:
			user_update_data['set__serial_count'] = 1
			temp_curr_serial_count = 0
			curr_serial_count = 1
		#如果当前连续签到大于等于最高连续签到，则更新最高连续签到

		if temp_curr_serial_count > int(self.top_serial_count):
			user_update_data['set__top_serial_count'] = temp_curr_serial_count
		#更新prize
		curr_prize_integral = daily_integral = serial_integral = next_serial_integral = next_serial_count = 0
		curr_prize_coupon_id = daily_coupon_id = serial_coupon_id = next_serial_coupon_id = ''
		curr_prize_coupon_name = daily_coupon_name = serial_coupon_name = next_serial_coupon_name = ''
		next_serial_coupon = []
		daily_coupon = []
		serial_coupon = []
		curr_prize_coupon = []
		#首先获取奖项配置
		prize_settings = exsign.prize_settings
		bingo = 0
		flag = False
		for name in sorted(map(lambda x: (int(x),x), prize_settings.keys())):
			setting = prize_settings[name[1]]
			name = int(name[0])
			if flag or name > curr_serial_count:
				next_serial_count = name
				for type, value in setting.items():
					if type == 'integral':
						next_serial_integral = value
					elif type == 'coupon':
						for v in value:
							if int(v['grade_id']) == grade_id:
								next_serial_coupon.append({
									"id": v["id"],
									"name": v["name"],
									"grade_id": v["grade_id"]
								})
							elif int(v['grade_id']) == 0:
								next_serial_coupon.append({
									"id": v["id"],
									"name": v["name"],
									"grade_id": v["grade_id"]
								})
				break
			if name == 0:
				#每日奖励和达到连续签到要求的奖励
				for type, value in setting.items():
					if type == 'integral':
						daily_integral = int(value)
					elif type == 'coupon':
						for v in value:
							if int(v['grade_id']) == grade_id:
								daily_coupon.append({
									"id": v["id"],
									"name": v["name"],
									"grade_id": v["grade_id"]
								})
							elif int(v['grade_id']) == 0:
								daily_coupon.append({
									"id": v["id"],
									"name": v["name"],
									"grade_id": v["grade_id"]
								})
			if name == curr_serial_count:
				#达到连续签到要求的奖励
				bingo = curr_serial_count
				flag = True
				for type, value in setting.items():
					if type == 'integral':
						serial_integral = int(value)
					elif type == 'coupon':
						for v in value:
							if int(v['grade_id']) == grade_id:
								serial_coupon.append({
									"id": v["id"],
									"name": v["name"],
									"grade_id": v["grade_id"]
								})
							elif int(v['grade_id']) == 0:
								serial_coupon.append({
									"id": v["id"],
									"name": v["name"],
									"grade_id": v["grade_id"]
								})

		user_prize = self.prize
		temp_coupon_list = user_prize['coupon'].split(',')
		temp_coupon_list = [] if temp_coupon_list == [''] else temp_coupon_list #防止出现[''].append(x)再用join时出现前置逗号的问题
		#若命中连续签到，则不奖励每日签到
		if bingo == curr_serial_count:
			user_prize['integral'] = int(user_prize['integral']) + serial_integral
			if serial_coupon:
				for s in serial_coupon:
					temp_coupon_list.append(s["name"])
				curr_prize_coupon = serial_coupon
			curr_prize_integral = serial_integral
		else:
			user_prize['integral'] = int(user_prize['integral']) + daily_integral
			if daily_coupon:
				for d in daily_coupon:
					temp_coupon_list.append(d["name"])
				curr_prize_coupon = daily_coupon
			curr_prize_integral = daily_integral

		user_prize['coupon'] = ','.join(temp_coupon_list)
		user_update_data['set__prize'] = user_prize
		# self.update(**user_update_data)
		sync_result = self.modify(
			{'__raw__': {'$or':
							[
								{'latest_date': None},
								{'latest_date': {'$lt': datetime.datetime(nowDate.year, nowDate.month, nowDate.day, 0, 0)}}
							]
						}
			},
			**user_update_data
		)
		if not sync_result:
			return_data['status_code'] = RETURN_STATUS_CODE['ALREADY']
			return_data['errMsg'] = u'每天只能签到一次'
			return return_data
		self.reload()
		#更新签到参与人数
		exsign.update(inc__participant_count=1)

		#发放奖励 积分&优惠券
		member = member_models.Member.objects.get(id=self.member_id)
		member.consume_integral(-int(curr_prize_integral), u'参与签到，积分奖项')
		if curr_prize_coupon:
			from apps.request_util import get_consume_coupon
			for c in curr_prize_coupon:
				coupon, msg, coupon_count = get_consume_coupon(exsign.owner_id,'exsign', str(exsign.id), c['id'], self.member_id)
				c["count"] = coupon_count
		else:
			curr_prize_coupon = {
				"id": 0,
				"name": "",
				"count": 0
			}
		return_data['curr_prize_integral'] = curr_prize_integral
		return_data['curr_prize_coupon'] = curr_prize_coupon
		return_data['daily_integral'] = daily_integral
		return_data['daily_coupon'] = daily_coupon
		return_data['next_serial_count'] = next_serial_count
		return_data['next_serial_integral'] = next_serial_integral
		return_data['next_serial_coupon'] = next_serial_coupon
		return_data['serial_count'] = int(self.serial_count)

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
class exSign(models.Document):
	owner_id = models.LongField() #创建人id
	name = models.StringField(default="", max_length=100) #名称
	share = models.DynamicField(default="") #分享设置
	# reply = models.DynamicField(default="") #自动回复设置
	prize_settings = models.DynamicField(default="") #签到奖项设置
	status = models.IntField(default=0) #状态
	participant_count = models.IntField(default=0) #参与者数量
	related_page_id = models.StringField(default="", max_length=100) #termite page的id
	created_at = models.DateTimeField() #创建时间
	
	meta = {
		'collection': 'exsign_exsign',
		'db_alias': 'apps'
	}

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


def get_coupon_count(coupon_rule_id):
	"""
	通过优惠券id获取其库存量
	:param coupon_rule_id: 优惠券ruleid
	:return: 库存
	"""
	if not coupon_rule_id or int(coupon_rule_id) == 0:
		return 0

	try:
		coupon = CouponRule.objects.get(id=coupon_rule_id)
		return coupon.remained_count
	except:
		return 0