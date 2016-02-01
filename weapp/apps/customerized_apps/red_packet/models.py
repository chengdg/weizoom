# -*- coding: utf-8 -*-

from datetime import datetime

import mongoengine as models

STATUS_NOT_START = 0
STATUS_RUNNING = 1
STATUS_STOPED = 2
class RedPacket(models.Document):
	owner_id = models.LongField() #创建人id
	name = models.StringField(default="", max_length=100) #名称
	start_time = models.DateTimeField() #开始时间
	end_time = models.DateTimeField() #结束时间
	status = models.IntField(default=0) #状态
	related_page_id = models.StringField(default="", max_length=100) #termite page的id
	timing = models.BooleanField(default=True) #是否显示倒计时
	type = models.StringField(default="random", max_length=10) #红包方式,默认为拼手气红包
	random_total_money = models.StringField(default="", max_length=10) #拼手气红包总金额
	random_packets_number = models.StringField(default="", max_length=10) #拼手气红包红包个数
	random_random_number_list = models.ListField() #随机正负金额List
	regular_packets_number = models.StringField(default="", max_length=10) #普通红包红包个数
	regular_per_money = models.StringField(default="", max_length=10) #普通红包单个金额
	money_range = models.StringField(default="", max_length=50) #好友贡献金额区间
	reply_content = models.StringField(default="", max_length=50) #参与活动回复语
	material_image = models.StringField(default="", max_length=1024) #分享的图片链接
	share_description = models.StringField(default="", max_length=1024) #分享描述
	wishing = models.StringField(default="", max_length=50) #开现金红包文字
	qrcode = models.DynamicField() #带参数二维码ticket,name
	created_at = models.DateTimeField() #创建时间
	
	meta = {
		'collection': 'red_packet_red_packet'
	}
	
	@property
	def status_text(self):
		if self.status == STATUS_NOT_START:
			return u'未开始'
		elif self.status == STATUS_RUNNING:
			now = datetime.today()
			if now >= self.end_time:
				return u'已结束'
			else:
				return u'进行中'
		elif self.status == STATUS_STOPED:
			return u'已结束'
		else:
			return u'未知'
	
	@property
	def is_finished(self):
		status_text = self.status_text
		if status_text == u'已结束':
			return True
		else:
			return False

class RedPacketParticipance(models.Document):
	member_id= models.LongField(default=0) #参与者id
	belong_to = models.StringField(default="", max_length=100) #对应的活动id
	created_at = models.DateTimeField() #创建时间
	has_join = models.BooleanField(default=False) #是否已经参与拼红包
	red_packet_money = models.FloatField(default=0) #拼红包目标金额
	current_money = models.FloatField(default=0) #已获取金额
	red_packet_status = models.BooleanField(default=False) #红包状态
	is_already_paid = models.BooleanField(default=False) #红包发放状态
	is_valid = models.BooleanField(default=True) #该条记录是否有效(针对取关后再次关注的情况)
	helped_member_ids = models.ListField(models.LongField()) #帮他拼红包的会员id list
	finished_time = models.DateTimeField() #完成时间

	#存储api状态和结果
	msg_api_status = models.BooleanField(default=False) #模板消息是否已成功发送
	msg_api_failed_members_info = models.DynamicField() #模板消息发送失败的会员信息

	meta = {
		'collection': 'red_packet_red_packet_participance'
	}

class RedPacketLog(models.Document):
	belong_to = models.StringField(default="", max_length=100) #对应的活动id
	helper_member_id = models.LongField() #帮助者id
	help_money = models.FloatField(default=0) #帮助金额
	be_helped_member_id = models.LongField() #被帮助者id
	created_at = models.DateTimeField(default=datetime.now()) #创建时间

	meta = {
		'collection': 'red_packet_red_packet_log'
	}

class RedPacketDetail(models.Document):
	"""
	拼红包详情表
	"""
	belong_to = models.StringField(default="", max_length=100) #对应的活动id
	owner_id = models.LongField() #被帮助者id
	helper_member_id = models.LongField() #帮助者id
	helper_member_name = models.StringField(default='', max_length=1024) #帮助者昵称
	help_money = models.FloatField(default=0) #帮助金额
	has_helped = models.BooleanField(default=False) #是否已帮助(针对未关注用户)
	is_valid = models.BooleanField(default=True) #该条记录是否有效(针对取关后再次关注的情况)
	created_at = models.DateTimeField() #创建时间

	meta = {
		'collection': 'red_packet_red_packet_detail'
	}

class RedPacketControl(models.Document):
	"""
	控制一个用户同时并发给人点赞的情况
	"""
	member_id= models.LongField(default=0) #参与者id
	helped_member_id = models.LongField(default=0) #被帮助者id
	belong_to = models.StringField(default="", max_length=100) #对应的活动id
	red_packet_control = models.StringField(default="", max_length=100, unique_with=['belong_to', 'member_id', 'helped_member_id'])

	meta = {
		'collection': 'red_packet_red_packet_control'
	}

class RedPacketCertSettings(models.Document):
	"""
	存储每个帐号的证书文件地址
	"""
	owner_id = models.StringField(default=0) #活动所有者
	cert_path = models.StringField(default="", max_length=1024) #证书
	key_path = models.StringField(default="", max_length=1024) #证书key


class RedPacketAmountControl(models.Document):
	"""
	控制多个用户并发领取红包会超量的情况
	"""
	belong_to = models.StringField(default="", max_length=100) #对应的活动id
	red_packet_amount = models.IntField(default=0,unique_with=['belong_to']) #可领取的红包总量

	meta = {
		'collection': 'red_packet_red_packet_amount_control'
	}