# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.conf import settings
from django.core.cache import cache

from weixin.message.handler.message_handler import *
from weixin.message.handler.event_handler import *
from weixin.user.models import WeixinUser
from weixin.statistics.models import decrease_weixin_user_statistics, increase_weixin_user_statistics
from weixin.message.qa import cache_util
from weixin.message.qa.models import Rule
from weixin.message.material.models import News, Material

from modules.member.models import WebAppUser, MemberFollowRelation
from mall.models import Product
from account.social_account.models import SocialAccount

from weixin.message.message_handler import tasks 


"""
默认的事件处理实现，主要是对关注和取消关注事件的处理

对于关注事件：
1. 修改发送消息微信用户对接收消息的公众账号的关注状态
2. 接收消息的公众账号的每日新增粉丝数+1
3. 返回所配置的关注回复，如果没有配置那么返回空

对于取消关注事件：
1. 修改发送消息微信用户对接收消息的公众账号的关注状态
2. 接收消息的公众账号的每日新增粉丝数-1
3. 返回空消息
"""
class DefaultEventHandler(EventMessageHandler):
	def _find_follow_response_rule_for(self, user_profile):
		#rule = qa_util.find_follow_answer_for(webapp_id)
		#从缓存中获取数据  duhao  2015-03-09
		rule = cache_util.find_follow_answer_from_cache_for(user_profile)
		if rule:
			return rule
		else:
			return None

	def _move_weixin_followers_statistics_one_step(self, user_id, is_from_simulator, is_increse=True):
		if (not is_from_simulator) or (settings.DEBUG):
			#只有在下列两种情况才更新统计
			#1. settings.DEBUG为True
			#2. settings.DEBUG不为True且数据不是来自模拟器
			# if is_increse:
			# 	increase_weixin_user_statistics(user)
			# else:
			# 	decrease_weixin_user_statistics(user)
			#update by bert at 20150323
			if user_id:
				tasks.weixin_user_statistics.delay(user_id, is_increse)

	def _handle_subscribe_event(self, context, is_from_simulator):
		received_message = context.message
		user_profile = context.user_profile

		try:
			if context.weixin_user:
				from_weixin_user = context.weixin_user
				from_weixin_username = from_weixin_user.username
			else:
				from_weixin_username = received_message.fromUserName
				#from_weixin_user = WeixinUser.objects.get(username=from_weixin_username)

			tasks.update_weixin_user.delay(from_weixin_username, True)
			# from_weixin_user.is_subscribed = True
			# from_weixin_user.save()
		finally:
			self._move_weixin_followers_statistics_one_step(user_profile.user_id, is_from_simulator)
			## weshop begin
			cache_key = 'from_weshop_%s' % received_message.fromUserName
			product = cache.get(cache_key)
			# if product == None:
			# 	cache.set(cache_key, 1704, 60 * 5)
			response_rule = None

			if product:
				news = News()
				news.title = '微众商城合作商家'
				news.summary = '微众商城合作商家'
				#news.text = 'weshop text'
				news.pic_url = 'http://weizoom.b0.upaiyun.com/upload/92_20150121/1421810295068_503.jpg'
				news.url = '?module=mall&model=products&action=list&category_id=0&workspace_id=mall&webapp_owner_id=%s'\
					% (user_profile.user_id)

				material = Material()
				material.owner = user_profile.user
				news.material = material

				response_rule = Rule()
				response_rule.type = 3
				response_rule.material_id = 1

				product_set = Product.objects.filter(id=product)
				if len(product_set) == 1:
					news2 = News()
					# news2.title = '9折购买-%s' % (product_set[0].name)
					news2.title = product_set[0].name
					news2.pic_url = product_set[0].thumbnails_url
					news2.url = '?woid=%s&module=mall&model=product&action=get&rid=%s'\
						% (user_profile.user_id, product)
					news2.material = material
					response_rule.newses = [news, news2]
				else:
					print 'default_event_handler len(product_set) not 1. ', len(product_set)
					response_rule.newses = [news]
			else:
				response_rule = self._find_follow_response_rule_for(user_profile)
			## weshop end
			if response_rule:
				return self._build_response_to_weixin_user(context.user_profile, context.message, \
						response_rule, is_from_simulator)
			else:
				return None

	def _handle_unsubscribe_envent(self, context, is_from_simulator):
		received_message = context.message
		user_profile = context.user_profile

		from_weixin_username = received_message.fromUserName

		try:
			WeixinUser.objects.filter(username=from_weixin_username).update(
				is_subscribed = False
				)

			self.__handle_member_unsubscribe_event(context)
		finally:
			self._move_weixin_followers_statistics_one_step(user_profile.user_id, is_from_simulator, False)
			return None

	def __handle_member_unsubscribe_event(self, context):
		if context.member is not None:
			context.member.is_subscribed = False
			context.member.status = 0
			context.member.save()

	# def __remove_member_info(self, context, from_weixin_username):
	# 	#删除对应的会员以及关系
	# 	if context.member is not None:
	# 		member_id = context.member.id

	# 		MemberFollowRelation.objects.filter(member_id=context.member.id).delete()
	# 		MemberFollowRelation.objects.filter(follower_member_id=context.member.id).delete()
	# 		context.member.delete()

	# 		#删除会员对应的webapp user
	# 		WebAppUser.objects.filter(member_id=member_id).delete()

	# 	#删除对应的社会化账号信息
	# 	if from_weixin_username is not None:
	# 		SocialAccount.objects.filter(openid=from_weixin_username).delete()
