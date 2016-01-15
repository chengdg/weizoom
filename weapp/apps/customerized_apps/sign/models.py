# -*- coding: utf-8 -*-

import datetime
from django.conf import settings

import mongoengine as models
from modules.member.module_api import get_member_by_openid

from modules.member import models as member_models
from mall.promotion.models import CouponRule
from termite import pagestore as pagestore_manager

class SignDetails(models.Document):
	"""
	签到详情记录表
	"""
	member_id= models.LongField(default=0) #参与者id
	belong_to = models.StringField(default="", max_length=100) #对应的活动id
	created_at = models.DateTimeField() #创建时间
	prize = models.DynamicField() #奖励信息
	type = models.StringField(default=u"页面签到", max_length=20) #页面签到 or 自动签到

	meta = {
		'collection': 'sign_sign_details'
	}

class SignControl(models.Document):
	member_id= models.LongField(default=0) #参与者id
	belong_to = models.StringField(default="", max_length=100) #对应的活动id
	sign_control = models.StringField(default="", max_length=100, unique_with=['belong_to', 'member_id'])

	meta = {
		'collection': 'sign_sign_control'
	}

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
		#首先获取奖项配置
		prize_settings = sign.prize_settings
		bingo = 0
		flag = False
		for name in sorted(map(lambda x: (int(x),x), prize_settings.keys())):
			setting = prize_settings[name[1]]
			name = int(name[0])
			if flag or name>curr_serial_count:
				next_serial_count = name
				for type, value in setting.items():
					if type == 'integral':
						next_serial_integral = value
					elif type == 'coupon':
						next_serial_coupon_id = value['id'] if value != '' else ''
						next_serial_coupon_name = value['name']
				break
			if name == 0:
				#每日奖励和达到连续签到要求的奖励
				for type, value in setting.items():
					if type == 'integral':
						daily_integral = int(value)
					elif type == 'coupon':
						daily_coupon_id = value['id'] if value != '' else ''
						daily_coupon_name = value['name']
			if name == curr_serial_count:
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
		sync_result = self.modify(
			query={'latest_date__lt': nowDate.date()},
			**user_update_data
		)
		if not sync_result:
			return_data['status_code'] = RETURN_STATUS_CODE['ERROR']
			return_data['errMsg'] = u'操作过于频繁'
			return return_data
		self.reload()
		#更新签到参与人数
		sign.update(inc__participant_count=1)

		#发放奖励 积分&优惠券
		member = member_models.Member.objects.get(id=self.member_id)
		member.consume_integral(-int(curr_prize_integral), u'参与签到，积分奖项')
		curr_prize_coupon_count = 0
		if curr_prize_coupon_id != '':
			from apps.request_util import get_consume_coupon
			coupon, msg, coupon_count = get_consume_coupon(sign.owner_id,'sign', str(sign.id), curr_prize_coupon_id, self.member_id)
			curr_prize_coupon_count = coupon_count
		return_data['curr_prize_integral'] = curr_prize_integral
		return_data['curr_prize_coupon_count'] = curr_prize_coupon_count
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
		sign_description=""
		host = settings.DOMAIN
		try:
			sign = Sign.objects.get(owner_id=data['webapp_owner_id'])
			checking_result = check_matched_keyword(data['keyword'], sign.reply['keyword'])
			if checking_result:
				if sign.status != 1:
					return_html.append(u'签到活动未开始')
				else:
					# add by bert  增加获取会员代码
					member = get_member_by_openid(data['openid'], data['webapp_id'])
					if not member:
						return None
					#设置的最大连续签到天数
					max_setting_count = sorted(map(lambda x: int(x), sign.prize_settings.keys()), reverse=True)[0]

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

					#如果已达到最大设置天数则重置签到
					if (signer.serial_count == max_setting_count and signer.latest_date and signer.latest_date.strftime('%Y-%m-%d') != datetime.datetime.now().strftime('%Y-%m-%d')) or (max_setting_count !=0 and signer.serial_count > max_setting_count):
						signer.update(set__serial_count=0, set__latest_date=datetime.datetime.today())
						signer.reload()

					pagestore = pagestore_manager.get_pagestore('mongo')
					page = pagestore.get_page(sign.related_page_id, 1)
					sign_description = page['component']['components'][0]['model']['description']

					return_data = signer.do_signment(sign)

					detail_dict = {
						'belong_to': str(sign.id),
						'member_id': member.id,
						'created_at': datetime.datetime.today(),
						'type': u'自动签到',
						'prize': {
							'integral': 0,
							'coupon': {
								'id': 0,
								'name': ''
							}
						}
					}

					if return_data['status_code'] == RETURN_STATUS_CODE['ALREADY']:
						return_html.append(u'亲，今天您已经签到过了哦，\n明天再来吧！')
					if return_data['status_code'] == RETURN_STATUS_CODE['SUCCESS']:
						detail_prize_dict = {
							'integral': 0,
							'coupon': {
								'id': 0,
								'name': ''
							}
						}
						return_html.append(u'签到成功！\n已连续签到%s天。\n本次签到获得以下奖励:\n' % return_data['serial_count'])
						return_html.append(str(return_data['curr_prize_integral']))
						return_html.append(u'积分')
						detail_prize_dict['integral'] = str(return_data['curr_prize_integral'])
						if return_data['curr_prize_coupon_name'] != '' and return_data['curr_prize_coupon_count'] >= 0:
							if return_data['curr_prize_coupon_count']>0:
								return_html.append('\n'+str(return_data['curr_prize_coupon_name']))
								return_html.append(u'\n<a href="http://%s/termite/workbench/jqm/preview/?module=market_tool:coupon&model=usage&action=get&workspace_id=market_tool:coupon&webapp_owner_id=%s&project_id=0">点击查看</a>' % (host, data['webapp_owner_id']))
								detail_prize_dict['coupon'] = {
									'id': return_data['curr_prize_coupon_id'],
									'name': str(return_data['curr_prize_coupon_name'])
								}
							else:
								return_html.append(u'\n奖励已领完,请联系客服补发')
								detail_prize_dict['coupon'] = {
									'id': return_data['curr_prize_coupon_id'],
									'name': u'优惠券已领完,请联系客服补发'
								}
						return_html.append(u'\n签到说明：%s\n'%sign_description)
						return_html.append(str(return_data['reply_content']))
						detail_dict['prize'] = detail_prize_dict
						#记录签到历史
						details = SignDetails(**detail_dict)
						details.save()
					return_html.append(u'\n<a href="http://%s/m/apps/sign/m_sign/?webapp_owner_id=%s"> >>点击查看详情</a>' % (host, data['webapp_owner_id']))
			else:
				return None
		except Exception,e:
			print e
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

def check_matched_keyword(remote_keyword, setting_keywords_dict):
	"""
	匹配关键字 ，精确匹配和模糊匹配
	:param remote_keyword: 微信端传递的关键字
	:param setting_keywords_dict: 系统配置的关键字集合
	:return: 是否命中
	"""
	result = False
	for key, mode in setting_keywords_dict.items():
		if 'accurate' == mode and remote_keyword == key:
			result = True
			break
		elif 'blur' == mode and key in remote_keyword:
			result = True
			break
	return result