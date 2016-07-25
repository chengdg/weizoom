# -*- coding: utf-8 -*-

from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
#from datetime import datetime
import json
import time
from core import emotion

from core.emojicons_util import encode_emojicons_for_html

from modules.member.models import  Member
from utils.string_util import byte_to_hex, hex_to_byte

DEFAULT_ICON = '/static/img/user-1.jpg'


#########################################################################
# Material：素材
#########################################################################
SINGLE_NEWS_TYPE = 1
MULTI_NEWS_TYPE = 2
MATERIAL_TYPES = (
	(SINGLE_NEWS_TYPE, '单图文消息'),
	(MULTI_NEWS_TYPE, '多图文消息')
)
class Material(models.Model):
	owner = models.ForeignKey(User, related_name='owned_materials')
	type = models.IntegerField(default=SINGLE_NEWS_TYPE, choices=MATERIAL_TYPES)
	created_at = models.DateTimeField(auto_now_add=True)
	is_deleted = models.BooleanField(default=False) #是否删除

	class Meta(object):
		db_table = 'material_material'
		verbose_name = '素材'
		verbose_name_plural = '素材'


#########################################################################
# News：一条图文消息
#########################################################################
class News(models.Model):
	material = models.ForeignKey(Material) #素材外键
	display_index = models.IntegerField() #显示顺序
	title = models.CharField(max_length=40) #标题
	summary = models.CharField(max_length=120) #摘要
	text = models.TextField(default='') #正文
	pic_url = models.CharField(max_length=1024) #图片url地址
	url = models.CharField(max_length=1024) #目标地址
	link_target = models.CharField(max_length=2048) #链接目标
	is_active = models.BooleanField(default=True) #是否启用
	created_at = models.DateTimeField(auto_now_add=True) #添加时间
	is_show_cover_pic = models.BooleanField(default=True, verbose_name=u"是否在详情中显示封面图片")

	class Meta(object):
		db_table = 'material_news'
		verbose_name = '图文消息'
		verbose_name_plural = '图文消息'

	@staticmethod
	def get_news_by_material_id(material_id):
		news_list = []
		for new in News.objects.filter(material_id=material_id, is_active=True):
			news_list.append(new)
		return news_list

	@property
	def user(self):
		return self.material.owner

#########################################################################
# Rule：规则
#########################################################################
TEXT_TYPE = 1
NEWS_TYPE = 2
FOLLOW_TYPE = 3
UNMATCH_TYPE = 4
MENU_TYPE = 5
RULE_TYPES = (
	(TEXT_TYPE, '文本消息'),
	(NEWS_TYPE, '图文消息'),
	(FOLLOW_TYPE, '关注回复消息'),
	(UNMATCH_TYPE, '自动回复'),
	(MENU_TYPE, '自定义菜单回复')
)
WEEODAY2NUM = {
	"Mon": 1,
	"Tue": 2,
	"Wed": 3,
	"Thu": 4,
	"Fri": 5,
	"Sat": 6,
	"Sun": 7
}
RULE_ACTIVE_TYPE_INACTIVE = 0
RULE_ACTIVE_TYPE_ACTIVE = 1
RULE_ACTIVE_TYPE_TIMED_ACTIVE = 2
class Rule(models.Model):
	owner = models.ForeignKey(User, related_name='owned_rules')
	type = models.IntegerField(default=TEXT_TYPE, choices=RULE_TYPES)
	rule_name = models.CharField(default='', max_length=256) #关键词匹配的规则名称
	active_type = models.IntegerField(default=RULE_ACTIVE_TYPE_ACTIVE) #启用类型
	start_hour = models.CharField(default='', max_length=10) #启用时间，在active_type = RULE_ACTIVE_TYPE_TIMED_ACTIVE有用
	end_hour = models.CharField(default='', max_length=10) #禁用时间，在active_type = RULE_ACTIVE_TYPE_TIMED_ACTIVE有用
	created_at = models.DateTimeField(auto_now_add=True) #添加时间
	patterns = models.CharField(max_length=1024) #匹配词，以英文竖线'|'分隔
	answer = models.CharField(max_length=2048) #回答
	material_id = models.IntegerField(default=0) #素材id，type为NEWS_TYPE时有效
	#weapp 10.0 bert add
	is_url = models.BooleanField(default=False) #是否是url
	active_days = models.CharField(default='', max_length=150) #周几启用

	class Meta(object):
		db_table = 'qa_rule'
		verbose_name = '规则'
		verbose_name_plural = '规则'

	@property
	def is_news_type(self):
		return self.type == NEWS_TYPE or self.material_id > 0

	@property
	def is_active(self):
		if hasattr(self, '_is_active'):
			return self._is_active

		if self.active_type == RULE_ACTIVE_TYPE_ACTIVE:
			self._is_active = True
		elif self.active_type == RULE_ACTIVE_TYPE_INACTIVE:
			self._is_active = False
		else: #RULE_ACTIVE_TYPE_TIMED_ACTIVE
			cur_hour = datetime.now().hour

			#兼容旧的start_hour和end_hour，转换成时分格式
			start_hour, end_hour = _format_hour(self.start_hour, self.end_hour)
			if end_hour == '24:00':
				end_hour = '23:59'

			start_time = time.strptime(start_hour, "%H:%M")
			end_time = time.strptime(end_hour, "%H:%M")

			now_str = time.strftime("%H:%M", time.localtime())
			now_time = time.strptime(now_str, "%H:%M")

			weekday = datetime.today().weekday() + 1
			days = []
			try:
				weekday2value = json.loads(self.active_days)
				for day in weekday2value:
					if weekday2value[day]:
						days.append(WEEODAY2NUM[day])
			except:
				pass
			self._is_active = now_time >= start_time and now_time < end_time and weekday in days

		return self._is_active

	@staticmethod
	def get_keyword_reply_rule(user, is_include_menu_reply_rule=False, order_query='-id'):
		query_types = [TEXT_TYPE, NEWS_TYPE]
		if is_include_menu_reply_rule:
			query_types.append(MENU_TYPE)

		return Rule.objects.filter(owner=user, type__in=query_types).order_by(order_query)

	def format_to_dict(self):
		try:
			self.patterns = json.loads(self.patterns)
			if type(self.patterns) == int or type(self.patterns) == long or type(self.patterns) == float:
				self.patterns = str(self.patterns)
				1/0 #防止关键词是数字时引起bug，使进入except代码块
		except:
			keywords = self.patterns.split('|')
			keyword_array = []
			for keyword in keywords:
				keyword2type = {}
				keyword2type['keyword'] = keyword
				keyword2type['type'] = 0
				keyword_array.append(keyword2type)

			self.patterns = keyword_array

		#处理老的图文回复
		if self.is_news_type and self.answer == '':
			self.answer = '[{"content":" ' + str(self.material_id) + '","type":"news"}]'

		try:
			self.answer = json.loads(self.answer)
			if type(self.answer) == int or type(self.answer) == long or type(self.answer) == float or type(self.answer) == dict:
				self.answer = str(self.answer)
				1/0 #防止关键词是数字和自定义菜单字典格式内容时引起bug，使进入except代码块
		except:
			if self.answer != '':
				answer_array = []
				content2type = {}
				if self.is_news_type:
					content2type['content'] = self.material_id
					content2type['type'] = 'news'
				else:
					#content2type['content'] = emotion.change_emotion_to_img(self.answer)
					try:
						news_answer = eval(self.answer)
						content2type['content'] = emotion.change_emotion_to_img(news_answer['content'])
					except:
						content2type['content'] = emotion.change_emotion_to_img(self.answer)

					content2type['type'] = 'text'

					#answers_dict = json.loads(self.answer)
					#content2type['content_content'] = emotion.change_emotion_to_img(answers_dict.content)

				answer_array.append(content2type)

				if self.type == FOLLOW_TYPE:
					#关注后自动回复只有一条回复内容，不需要用数组封装
					self.answer = content2type
				else:
					self.answer = answer_array

		if self.type == FOLLOW_TYPE:
			answer_dict = self.answer
			_fill_answer_dict(answer_dict)
		else:
			for answer_dict in self.answer:
				_fill_answer_dict(answer_dict)

		try:
			self.active_days = json.loads(self.active_days)
		except:
			# error_message = 'parse active_days to json error:' + self.active_days
			# watchdog_error(error_message)
			# print '----------------',error_message
			self.active_days = ''

		self.created_at = self.created_at.strftime('%Y-%m-%d %H:%M:%S')
		#兼容旧的start_hour和end_hour，转换成时分格式
		start_hour, end_hour = _format_hour(self.start_hour, self.end_hour)
		self.start_hour =start_hour
		self.end_hour = end_hour
		return {
			"id": self.id,
			"owner_id": self.owner_id,
			"type": self.type,
			"rule_name": self.rule_name,
			"active_type": self.active_type,
			"start_hour": self.start_hour,
			"end_hour": self.end_hour,
			"created_at": self.created_at,
			"patterns": self.patterns,
			"answer": self.answer,
			"material_id": self.material_id,
			"is_url": self.is_url,
			"active_days": self.active_days,
			"is_news_type": self.is_news_type
		}

def _fill_answer_dict(answer_dict):
	import re
	if answer_dict['type'] == 'news':
		answer_dict['newses'] = []
		#获取图文标题
		newses = News.get_news_by_material_id(int(answer_dict['content']))
		news_array = []
		for news in newses:
			news_dict = {}
			news_dict['id'] = news.id
			news_dict['title'] = news.title
			answer_dict['newses'].append(news_dict)
	else:
		#把除a表情外的html字符<,>转化成html对应的编码 by Eugene
		# a_pattern = re.compile(r'<a.+?href=.+?>.+?</a>')
		# all_a_html = a_pattern.findall(answer_dict['content'])
		# for html in all_a_html:
		# 	answer_dict['content'] = answer_dict['content'].replace(html, "%s")
		# answer_dict['content'] = answer_dict['content'].replace('<', "&lt;")
		# answer_dict['content'] = answer_dict['content'].replace('>', "&gt;")
		# answer_dict['content'] = answer_dict['content'] % tuple(all_a_html)
		from message.util import translate_special_characters
		answer_dict['content'] = translate_special_characters(answer_dict['content'])

		#处理表情
		answer_dict['content'] = emotion.change_emotion_to_img(answer_dict['content'])

def _format_hour(start_hour, end_hour):
	#兼容旧的start_hour和end_hour，转换成时分格式
	if len(start_hour) == 1:
		start_hour = '0%s:00' % start_hour
	elif len(start_hour) == 2:
		start_hour = '%s:00' % start_hour

	if len(end_hour) == 1:
		end_hour = '0%s:00' % end_hour
	elif len(end_hour) == 2:
		end_hour = '%s:00' % end_hour

	return start_hour, end_hour


class Tail(models.Model):
	owner = models.ForeignKey(User, related_name='owned_tails')
	tail = models.CharField(max_length=1024) #小尾巴内容
	is_active = models.BooleanField(default=False) #是否启用
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'qa_tail'
		verbose_name = '文本消息小尾巴'
		verbose_name_plural = '文本消息小尾巴'


#########################################################################
# has_duplicate_pattern：检查是否有重复的pattern
#########################################################################
def has_duplicate_pattern(user, new_patterns, ignore_rule=None):
	#处理ignore_rule
	if ignore_rule:
		ignore_rule = int(ignore_rule)
	else:
		ignore_rule = -1

	#获得关键词回复规则
	rules = Rule.get_keyword_reply_rule(user, True)

	duplicate_patterns = []
	existed_patterns = []
	#解析库中的patterns
	for rule in rules:
		if ignore_rule and rule.id == ignore_rule:
			continue

		try:
			for patterns in json.loads(rule.patterns):
				pattern = patterns['keyword']
				is_sub_match = patterns['type']

				if not pattern or pattern == '':
					continue
				existed_patterns.append(pattern.strip().lower())
		except:
			patterns = rule.patterns.split('|')
			for pattern in patterns:
				if pattern == '':
					continue
				existed_patterns.append(pattern.strip().lower())

	#处理传过来的patterns
	patterns = new_patterns.split('|')
	for pattern in patterns:
		if pattern in existed_patterns:
			duplicate_patterns.append(pattern)

	return len(duplicate_patterns) > 0, duplicate_patterns


#########################################################################
# WeixinUser：微信用户
#########################################################################
class WeixinUser(models.Model):
	username = models.CharField(max_length=100, unique=True)
	webapp_id = models.CharField(max_length=16, verbose_name='对应的webapp id')
	fake_id = models.CharField(max_length=50, default="") #微信公众平台字段fakeId
	nick_name = models.CharField(max_length=256) #微信公众平台字段nickName
	weixin_user_remark_name = models.CharField(max_length=64) #微信公众平台字段remarkName,暂未使用
	weixin_user_icon = models.CharField(max_length=1024) #微信公众平台字段icon
	created_at = models.DateTimeField(auto_now_add=True)
	is_head_image_received = models.BooleanField(default=False) #是否接收到头像
	head_image_retry_count = models.IntegerField(default=0) #接收头像的重试次数
	is_subscribed = models.BooleanField(default=True) #是否关注  0 ：取消关注 ，1 ：关注

	class Meta(object):
		ordering = ['-id']
		db_table = 'app_weixin_user'
		verbose_name = '微信用户'
		verbose_name_plural = '微信用户'

	@property
	def weixin_user_nick_name(self):
		if hasattr(self, '_nick_name'):
			return self._nick_name

		self._nick_name = hex_to_byte(self.nick_name)
		return self._nick_name

	@weixin_user_nick_name.setter
	def weixin_user_nick_name(self, nick_name):
		self.nick_name = byte_to_hex(nick_name)

	@property
	def nickname_for_html(self):
		if hasattr(self, '_nickname_for_html'):
			return self._nickname_for_html

		if (self.nick_name is not None) and (len(self.nick_name) > 0):
			self._nickname_for_html = encode_emojicons_for_html(self.nick_name, is_hex_str=True)
		else:
			self._nickname_for_html = ''

		try:
			#解决用户名本身就是字节码串导致不能正常转换得问题，例如ae
			self._nickname_for_html.decode('utf-8')
		except:
			self._nickname_for_html = self.nick_name

		return self._nickname_for_html


from weixin.user.models import WeixinMpUserAccessToken, get_mpuser_access_token_for, get_system_user_binded_mpuser, WeixinMpUser


#########################################################################
# RealTimeInfo：实时信息, 和所绑定的微信公众号关联
#########################################################################
class RealTimeInfo(models.Model):
	mpuser = models.ForeignKey(WeixinMpUser, related_name='owned_realtime_infos')
	unread_count = models.IntegerField(default=0, db_index=True) #未读消息数

	class Meta(object):
		db_table = 'weixin_message_realtime_info'
		verbose_name = '微信消息实时状态信息'
		verbose_name_plural = '微信消息实时状态信息'


#########################################################################
# Session：会话抽象
#########################################################################
class Session(models.Model):
	mpuser = models.ForeignKey(WeixinMpUser, related_name='owned_sessions')
	weixin_user = models.ForeignKey(WeixinUser, to_field='username', db_column='weixin_user_username')
	latest_contact_content = models.CharField(max_length=1024) #最后一次交互消息内容
	latest_contact_created_at = models.DateTimeField(auto_now_add=True) #最后一次交互时间
	is_latest_contact_by_viper = models.BooleanField(default=False) #最后一次交互是否是客户发出的
	unread_count = models.IntegerField(default=0) #未读消息数
	is_show = models.BooleanField(default=False) #是否显示(是否填充对应的WeixinUser)
	created_at = models.DateTimeField(auto_now_add=True)
	weixin_created_at = models.CharField(max_length=50) #微信平台提供的创建时间
	retry_count = models.IntegerField(default=0) #重試次數
	#add by bert at 20.0
	message_id = models.IntegerField(default=0)
	#add by slzhu
	member_user_username = models.CharField(default='', max_length=100)
	member_message_id = models.IntegerField(default=0)
	member_latest_content = models.CharField(default='', max_length=1024) #粉丝最近一条消息
	member_latest_created_at = models.CharField(default='', max_length=50) #粉丝最近一条消息时间
	is_replied = models.BooleanField(default=False) #是否回复过

	class Meta(object):
		ordering = ['-latest_contact_created_at']
		db_table = 'weixin_message_session'


def get_weixinuser_sessions(weixin_user_name):
	if weixin_user_name is None:
		return []

	return Session.objects.filter(weixin_user=weixin_user_name)

def get_opid_from_session(filter_args):
	return [session.member_user_username for session in Session.objects.filter(**filter_args)]



TEXT = 'text'
IMAGE = 'image'
VOICE = 'voice'
class Message(models.Model):
	"""
	表示消息的表
	"""
	mpuser = models.ForeignKey(WeixinMpUser, related_name='owned_messages')
	session = models.ForeignKey(Session)
	weixin_message_id = models.CharField(max_length=50, default='') #消息中的id
	mp_message_id = models.CharField(max_length=50, default='') #公众平台的id
	from_weixin_user_username = models.CharField(max_length=50) #消息发出者的username
	to_weixin_user_username = models.CharField(max_length=50) #消息接收者的username
	content = models.TextField()
	content_url = models.CharField(max_length=500, default='') #微信公众平台字段contentUrl,暂未使用
	has_reply = models.BooleanField(default=False) #微信公众平台字段hasReply,暂未使用
	created_at = models.DateTimeField(auto_now_add=True) #系统创建时间
	weixin_created_at = models.DateTimeField(auto_now_add=True) #在微信平台上创建的时间
	is_checked = models.BooleanField(default=False) #是否检查过
	is_reply = models.BooleanField(default=True) #是否是系统帐号回复
	#add by bert at 20.0
	message_type = models.CharField(default=TEXT, max_length=50)
	media_id = models.CharField(max_length=255,default='')
	msg_id = models.CharField(max_length=255,default='')
	pic_url = models.TextField()
	audio_url = models.TextField()
	is_updated = models.BooleanField(default=True)
	memo = models.CharField(max_length=255, default='') # 消息加备注
	#add by duhao 2015-05-06
	material_id = models.IntegerField(default=0) #素材id

	class Meta(object):
		db_table = 'weixin_message_message'
		ordering = ['-weixin_created_at', '-id']

	@property
	def is_news_type(self):
		return self.material_id > 0


########################################################################
# CollectMessage:收藏消息
########################################################################
class CollectMessage(models.Model):
	owner = models.ForeignKey(User, related_name='owned_collect_messages')
	message_id = models.IntegerField(default=0)
	status = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True) #系统创建时间

	class Meta(object):
		db_table = 'weixin_collect_message'

	@staticmethod
	def is_collected(message_id):
		if CollectMessage.objects.filter(message_id=message_id).count() > 0:
			return CollectMessage.objects.filter(message_id=message_id)[0].status
		else:
			return False

	@staticmethod
	def get_message_ids(owner):
		return [collect_message.message_id for collect_message in CollectMessage.objects.filter(owner=owner, status=True).order_by('-created_at')]




########################################################################
# ReamrkMessage:消息备注
########################################################################
class MessageRemarkMessage(models.Model):
	owner = models.ForeignKey(User, related_name='owned_remark_messages')
	message_id = models.IntegerField(default=0)
	message_remark = models.TextField()
	status = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True) #系统创建时间

	class Meta(object):
		db_table = 'weixin_message_remark'

	@staticmethod
	def get_message_ids(owner):
		remark_messages = MessageRemarkMessage.objects.filter(owner=owner, status=True).exclude(message_remark='').order_by('-created_at')
		return [remark_message.message_id for remark_message in remark_messages]


class FanCategory(models.Model):
	"""
	表示粉丝(会员)的分组

	@note 类似MemberTag。粉丝表示微信关注的用户。会员(member)表示在微商城购买过产品的用户。

	@see MemberTag

	@todo 账号初始化时，增加一个"未分组"？
	"""
	webapp_id = models.CharField(max_length=16, db_index=True)
	name = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'weixin_fan_category'
		verbose_name = '粉丝分组'
		verbose_name_plural = '粉丝分组'
		# 唯一性索引
		unique_together = (('webapp_id', 'name'),)

	@staticmethod
	def get_fan_categorys(webapp_id):
		if webapp_id:
			return list(FanCategory.objects.filter(webapp_id=webapp_id))
		else:
			return []


class FanHasCategory(models.Model):
	"""
	表示粉丝的分组情况

	@note 粉丝表示微信关注的用户。会员(member)表示在微商城购买过产品的用户。

	@see MemberHasTag

	@todo 按照产品设计，fan只能有一个category。
	"""
	fan = models.ForeignKey(Member)
	category = models.ForeignKey(FanCategory)

	class Meta(object):
		db_table = 'weixin_fan_has_category'
		verbose_name = '粉丝所属分组'
		verbose_name_plural = '粉丝所属分组信息'
		# 唯一性索引
		unique_together = (('category', 'fan'),)

	@staticmethod
	def get_fans_list_by_category_id(category_id):
		if category_id:
			fans = []
			for fans_has_category in FanHasCategory.objects.filter(category_id=category_id):
				fans.append(fans_has_category.fan)
			return fans
		else:
			return []

	@staticmethod
	def get_fan_id_list_by_category_id(category_id):
		if category_id:
			id_list = []
			for fans_has_category in FanHasCategory.objects.filter(category_id=category_id):
				id_list.append(fans_has_category.fan_id)
			return id_list
		else:
			return []


STATUS_OPEN = 1
STATUS_STOP = 0
class CustomerMenuStatus(models.Model):
	"""
	自定义菜单状态
	"""
	owner = models.ForeignKey(User, related_name='owned_menu_status')
	status = models.SmallIntegerField(default=1)
	created_at = models.DateTimeField(auto_now_add=True) #添加时间

	class Meta(object):
		db_table = 'weixin_menu_status'
		verbose_name = '自定义菜单状态'
		verbose_name_plural = '自定义菜单状态'


# SEX_TYPE_MEN = 1
# SEX_TYPE_WOMEN = 2
# SEX_TYPE_UNKOWN = 0
# SEX_TYPES = (
# 	(SEX_TYPE_MEN, '男'),
# 	(SEX_TYPE_WOMEN, '女'),
# 	(SEX_TYPE_UNKOWN, '未知')
# 	)

# class MemberInfo(models.Model):
# 	member = models.ForeignKey(Member, related_name='owner_member')
# 	name = models.CharField(max_length=300, default='', verbose_name='会员姓名')
# 	sex = models.IntegerField(choices=SEX_TYPES, verbose_name='性别')
# 	age = models.IntegerField(default=-1, verbose_name='年龄')
# 	address = models.CharField(max_length=32, blank=True, null=True, verbose_name='地址')
# 	phone_number = models.CharField(max_length=11, blank=True)
# 	qq_number = models.CharField(max_length=13, blank=True)
# 	weibo_nickname = models.CharField(max_length=16, verbose_name='微博昵称')
# 	member_remarks = models.TextField(max_length=1024, blank=True)
# 	#new add by bert
# 	is_binded = models.BooleanField(default=False)
# 	session_id = models.CharField(max_length=1024, blank=True)
# 	captcha = models.CharField(max_length=11, blank=True) #验证码
# 	is_passed = models.BooleanField(default=False)

# 	class Meta(object):
# 		db_table = 'member_info'
# 		verbose_name = '会员详细资料'
# 		verbose_name_plural = '会员详细资料'

# 	@staticmethod
# 	def get_member_info(member_id):
# 		if member_id is None or member_id <= 0:
# 			return None

# 		return MemberInfo.objects.filter(member_id=member_id)[0] if MemberInfo.objects.filter(member_id=member_id).count() > 0 else None


class MessageAnalysis(models.Model):
	"""
	消息统计
	"""
	owner_id = models.IntegerField(default=0)
	receive_count = models.IntegerField(default=0, verbose_name='接收消息数')
	send_count = models.IntegerField(default=0, verbose_name='发送消息数')
	interaction_user_count = models.IntegerField(default=0, verbose_name='互动人数')
	interaction_count = models.IntegerField(default=0, verbose_name='互动次数')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
	date_time = models.DateField(verbose_name='日期') # 2014-12-07

	class Meta(object):
		db_table = 'message_analysis'
		verbose_name = '消息统计'
		verbose_name_plural = '消息统计'


class KeywordHistory(models.Model):
	"""
	关键词历史记录
	"""
	owner = models.ForeignKey(User, related_name='owned_keyword_history')
	keyword = models.CharField(max_length=30, default='', verbose_name='关键词')
	date = models.DateField(verbose_name='日期') # 2014-12-07

	class Meta(object):
		db_table = 'weixin_keyword_history'
		verbose_name = '关键词历史记录'
		verbose_name_plural = '关键词历史记录'


class KeywordCount(models.Model):
	"""
	关键词统计
	"""
	owner = models.ForeignKey(User, related_name='owned_keyword_count')
	keyword = models.CharField(max_length=30, default='', verbose_name='关键词')
	count = models.IntegerField(default=0, verbose_name='关键词次数')
	date = models.DateField(verbose_name='日期') # 2014-12-07

	class Meta(object):
		db_table = 'weixin_keyword_count'
		verbose_name = '关键词统计'
		verbose_name_plural = '关键词统计'





class UserHasTemplateMessages(models.Model):
	"""
	商家在公众平台上配置的模板消息
	"""
	owner_id = models.IntegerField() #所属商家
	template_id = models.CharField(max_length=512) #模板id
	title = models.CharField(max_length=256) #模板标题
	primary_industry = models.CharField(max_length=64) #一级行业
	deputy_industry = models.CharField(max_length=64) #二级行业
	content = models.CharField(max_length=2048) #模板内容
	example = models.CharField(max_length=2048) #模板示例

	class Meta(object):
		db_table = 'weixin_user_has_templates'
		verbose_name = '我的模版'
		verbose_name_plural = '我的模版'


#模版用途
WEIXIN_TEMPLATE_USAGE = {
	'APPS_RED_PACKET': 0, #百宝箱拼红包
	'APPS_GROUP_SUCCESS': 1, #百宝箱团购成功
	'APPS_GROUP_FAIL': 2, #百宝箱团购失败

}
WEIXIN_TEMPLATE_TITLE2USAGE = {
	u'拼团成功通知': 1,
	u'拼团退款提醒': 2,
	u'商品发货通知': 3,
	u'订单标记发货通知': 4,
	u'购买成功通知': 5,
	u'付款成功通知': 6,
	u'积分变动通知': 7
}

class UserTemplateSettings(models.Model):
	"""
	商家各功能所配置的模板消息
	"""
	owner_id = models.IntegerField() #所属商家
	usage = models.IntegerField() #模版用途
	template_id = models.CharField(max_length=512) #模板id
	first = models.CharField(max_length=1024, default='') #模版开头语
	remark = models.CharField(max_length=1024, default='') #模版最后的注释
	status = models.BooleanField(default=False) #配置状态，是否启用

	class Meta(object):
		db_table = 'weixin_template_settings'
		verbose_name = '模版设置'
		verbose_name_plural = '模版设置'


class TemplateMessageLogs(models.Model):
	"""
	模版消息记录
	"""
	owner_id = models.IntegerField() #所属商家
	usage = models.IntegerField() #模版用途
	reason = models.CharField(max_length=1024, default='') #使用模版的场景描述
	template_id = models.CharField(max_length=512) #模板id
	content = models.TextField() #消息内容
	status = models.CharField(max_length=64, default='') #状态
	error_msg = models.CharField(max_length=2048, default='') #错误信息
	resp_msgid = models.CharField(max_length=128, default='') #发送的消息id
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'weixin_template_message_logs'
		verbose_name = '模版消息记录'
		verbose_name_plural = '模版消息记录'