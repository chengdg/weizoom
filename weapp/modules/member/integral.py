# -*- coding: utf-8 -*-

__author__ = 'chuter'

from util import *

from visit_session_util import has_visit, get_request_url_digest, get_request_url
from core.exceptionutil import unicode_full_stack

from django.http import HttpResponseRedirect

from utils.url_helper import remove_querystr_filed_from_request_url

from account.url_util import get_webappid_from_request

import member_settings
from models import *
from mall.models import Order

from watchdog.utils import watchdog_error, watchdog_fatal, watchdog_info
import module_api

from modules.member.tasks import update_member_integral, increase_intgral_for_be_member_first

"""
积分计算

"""
def _is_buyed(member):
	webapp_user = WebAppUser.from_member(member)
	
	#这种方式无法正确的判断是否购买过， 如果数据被删除则积分计算会出现问题    by bert
	# if webapp_user:
	# 	return webapp_user.has_purchased
	# else:
	# 	return False
	if webapp_user:
		return True if Order.objects.filter(webapp_user_id=webapp_user.id,status__gte=2).count() > 0 else False
	else:
		return False

def _has_visit(request, member_id, uuid):
	return has_visit(request, member_id, uuid)

is_buyed_querier = _is_buyed
has_visit_querier = _has_visit

class IntegralCaculator(object):

	def __init__(self):
		super(IntegralCaculator, self).__init__()

		from models import IntegralStrategySttings, MemberSharedUrlInfo, MemberIntegralLog, FIRST_SUBSCRIBE, FOLLOWER_CLICK_SHARED_URL, USE, RETURN_BY_SYSTEM, AWARD, BUY_AWARD, FOLLOWER_BUYED_VIA_SHARED_URL, BRING_NEW_CUSTOMER_VIA_QRCODE

	def increase_member_integral(self, member, integral_increase_count, 
			event_type, follower_member=None, webapp_user=None, to_task=True):
		if member is None:
			return
		if follower_member:
			follower_member_id = follower_member.id
		else:
			follower_member_id = 0

		if webapp_user:
			webapp_user_id = webapp_user.id
		else:
			webapp_user_id = 0
		# if to_task :
		# 	update_member_integral.delay(member.id, follower_member_id, integral_increase_count, event_type, webapp_user_id)
		# else:
		update_member_integral(member.id, follower_member_id, integral_increase_count, event_type, webapp_user_id)
		
	def _get_integral_strategy(self, request):
		if not hasattr(request, 'user_profile'):
			return None

		if request.user_profile:
			return self._get_integral_strategy_by_webappid(request.user_profile.webapp_id)
		else:
			webapp_id = get_webappid_from_request(request)
			if webapp_id:
				return self._get_integral_strategy_by_webappid(webapp_id)
			else:
				return None

	def _get_integral_strategy_by_webappid(self, webapp_id):
		try:
			return IntegralStrategySttings.objects.get(webapp_id=webapp_id)
		except:
			notify_message = u"根据webapp_id获取积分策略失败, webapp_id={}".format(webapp_id)
			watchdog_fatal(notify_message)
			return None

	def increase_for_bring_new_customer_by_qrcode(self, user_profile, member, followed_member):
		if member is None or followed_member is None or user_profile is None:
			return

		try:
			integral_strategy = self._get_integral_strategy_by_webappid(member.webapp_id)

			if integral_strategy is None:
				notify_message = u'分享二维码带来关注增加积分失败，因为获取不到对应的积分策略，会员id:{}'.format(member.id)
				watchdog_error(notify_message)
				return
			else:
				self.increase_member_integral(
					member, 
					integral_strategy.increase_integral_count_for_brring_customer_by_qrcode, 
					BRING_NEW_CUSTOMER_VIA_QRCODE,
					followed_member
				)
		except:
			notify_message = u'分享二维码带来关注增加积分失败，会员id:{}'.format(member.id)
			watchdog_error(notify_message)

	#成为会员时增加积分
	def increase_for_be_member_first(self, user_profile, member):
		if user_profile is None:
			#如果request没有user_profile信息，即不知道所访问的店铺，那么不
			#进行任何操作
			return
		self._increase_for_be_member_first(user_profile, member)

	#成为会员时增加积分
	def _increase_for_be_member_first(self, user_profile, member):
		if user_profile is None:
			#如果request没有user_profile信息，即不知道所访问的店铺，那么不
			#进行任何操作
			return

		if member is None:
			return
		

		#为首次成为会员增加积分
		increase_intgral_for_be_member_first.delay(member.id, user_profile.webapp_id, FIRST_SUBSCRIBE)
		# integral_strategy = self._get_integral_strategy_by_webappid(user_profile.webapp_id)

		# if integral_strategy is None:
		# 	notify_message = u'首次关注没有增加积分，因为获取不到对应的积分策略，会员id:{}'.format(
		# 		member.id)
		# 	watchdog_error(notify_message)
		# 	return



		#self.increase_member_integral(member, integral_strategy.be_member_increase_count, FIRST_SUBSCRIBE)

	#有人点击a用户分享的链接对a增加相应的积分
	def increase_for_click_shared_url(self, request):
		if request.user_profile is None:
			#如果request没有user_profile信息，即不知道所访问呢的店铺，那么不
			#进行任何操作
			return

		global is_buyed_querier
		global has_visit_querier

		#获取分享者信息
		followed_member_token = get_followed_member_token_from_url_querystr(request)
		if followed_member_token is None or len(followed_member_token) == 0:
			return
		followed_member = get_member_by_member_token(followed_member_token)
		if followed_member is None:
			#如果获取不到分享者信息，不进行任何操作
			return
		member = get_member(request)
		if member and member.token == followed_member_token:
			#如果自己点击自己分享的链接不进行任何计算
			return
		member_id = member.id if member else None
		uuid = get_uuid(request)
		if has_visit_querier(request, member_id, uuid):
			#如果不是第一次点击，那么不进行积分计算
			return
		#获取积分策略
		integral_strategy = self._get_integral_strategy(request)
		#判断分享者是否已经购买
		is_buyed = is_buyed_querier(followed_member)
		# if member:
		# 	watchdog_info('-----------------increase_for_click_shared_url-----member.id:%d' % member.id)
		# watchdog_info('-----------------increase_for_click_shared_url-----followed_member.id:%d' % followed_member.id)
		# watchdog_info('-----------------increase_for_click_shared_url-----is_buyed:%s' % is_buyed)
		webapp_user = request.webapp_user
		# if is_buyed:
		# 	if integral_strategy is None:
		# 		notify_message = u'分享链接被点击时，购买后的分享者没有增加积分，因为获取不到对应的积分策略，分享会员id:{}, url:{}'.format(
		# 				followed_member.id, request.get_full_path())
		# 		watchdog_error(notify_message)
		# 	else:
		# 		self.increase_member_integral(followed_member, \
		# 			integral_strategy.click_shared_url_increase_count_after_buy, FOLLOWER_CLICK_SHARED_URL, member, webapp_user) 
		# else:
		if integral_strategy is None:
			notify_message = u'分享链接被点击时，还没有购买的分享者没有增加积分，因为获取不到对应的积分策略，分享会员id:{}, url:{}'.format(
					followed_member.id, request.get_full_path())
			watchdog_error(notify_message)
		else:
			self.increase_member_integral(followed_member, \
				integral_strategy.click_shared_url_increase_count, FOLLOWER_CLICK_SHARED_URL, member, webapp_user)

	#有人通过a用户分享的链接成功购买后对a增加相应的积分
	def increase_for_buy_via_shared_url(self, request, order=None):
		if request.user_profile is None:
			#如果request没有user_profile信息，即不知道所访问呢的店铺，那么不
			#进行任何操作
			return
		member = get_member(request)
		integral_strategy = self._get_integral_strategy(request)
		if member:
			if integral_strategy is None:
				notify_message = u'购买时没有对购买者增加积分，因为获取不到对应的积分策略，会员id:{}, url:{}'.format(
						member.id, request.get_full_path())
				send_error_notify(notify_message, '')
			else:
				self.increase_member_integral(member, \
						integral_strategy.buy_award_count_for_buyer, BUY_AWARD)

				if order and order.final_price > 0:
					order_money_percentage_for_each_buy = float(integral_strategy.order_money_percentage_for_each_buy)
					increase_count_integral = int(order_money_percentage_for_each_buy * float(order.final_price))
					if increase_count_integral > 0:
						self.increase_member_integral(member, increase_count_integral, BUY_AWARD)
						
		#获取分享者信息
		followed_member_token = get_followed_member_token_from_cookie(request)
		if followed_member_token is None or len(followed_member_token) == 0:
			return			
		else:
			followed_member = get_member_by_member_token(followed_member_token)
		#获取购买者信息


		if followed_member and member and followed_member.id == member.id:
			#如果是同一人不进行任何操作
			return
		#获取积分策略
		
		#为购买者增加积分
		

		#为分享者增加积分
		if followed_member:
			if integral_strategy is None:
				notify_message = u'分享链接产生购买时对分享者没有增加积分，因为获取不到对应的积分策略，分享会员id:{}, url:{}'.format(
						followed_member.id, request.get_full_path())
				watchdog_error(notify_message)
			else:
				increase_count = integral_strategy.buy_via_shared_url_increase_count_for_author
				if increase_count > 0:
					# order_money_percentage_for_each_buy = float(integral_strategy.order_money_percentage_for_each_buy)
					# if order and order.final_price > 0 and order_money_percentage_for_each_buy > 0:
					# 	# str_a = "increase_count %s , order_money_percentage_for_each_buy%s, final_price%s" % (increase_count, order_money_percentage_for_each_buy, float(order.final_price))
					# 	# watchdog_error(str_a)
					# 	increase_count = increase_count + int(order_money_percentage_for_each_buy * float(order.final_price))

					self.increase_member_integral(followed_member, \
							increase_count, FOLLOWER_BUYED_VIA_SHARED_URL, member)
				
	def return_integral(self, member, return_count):
		if return_count <= 0:
			return

		self.increase_member_integral(member, return_count, RETURN_BY_SYSTEM)

	def use_integral_to_buy(self, member, use_count):
		if use_count <= 0:
			return 0.0

		self.increase_member_integral(member, -1*use_count, USE)

		integral_strategy = self._get_integral_strategy_by_webappid(member.webapp_id)

		if integral_strategy is None:
			notify_message = u'购买使用积分失败，因为获取不到对应的积分策略，会员id:{}, 使用数量:{}'.format(
					member.id, use_count)
			watchdog_fatal(notify_message)

			return 0.0

		money = (use_count + 0.0) / integral_strategy.integral_each_yuan
		return money

	def _record_integral_log(self, member, follower_member, integral_increase_count, event_type, webapp_user):
		if integral_increase_count == 0:
			return None
		try:
			webapp_user_id = 0
			if webapp_user:
				webapp_user_id = webapp_user.id

			return MemberIntegralLog.objects.create(
				member = member, 
				follower_member_token = follower_member.token if follower_member else '', 
				integral_count = integral_increase_count, 
				event_type = event_type,
				webapp_user_id = webapp_user_id
			)
		except:
			notify_message = u"记录积分日志失败, 会员id:{}, follower_member_token:{}, 积分增量:{}, 原由:{}\ncause:{}"\
				.format(member.id, follower_member.token if follower_member else '', integral_increase_count, event_type, unicode_full_stack())
			watchdog_fatal(notify_message)
			return None
		

_caculator = IntegralCaculator()
increase_member_integral = _caculator.increase_member_integral
increase_for_be_member_first = _caculator.increase_for_be_member_first
increase_for_click_shared_url = _caculator.increase_for_click_shared_url
increase_for_bring_new_customer_by_qrcode = _caculator.increase_for_bring_new_customer_by_qrcode
increase_for_buy_via_shared_url = _caculator.increase_for_buy_via_shared_url
use_integral_to_buy = _caculator.use_integral_to_buy
return_integral = _caculator.return_integral

def _replace_followed_member_token_in_request_url(request, new_followed_member_token=None):
	orig_full_path = request.get_full_path()

	if new_followed_member_token is None:
		return orig_full_path

	query_parts = orig_full_path.split('&')
	for index, query_part in enumerate(query_parts):
		if query_part.find(member_settings.FOLLOWED_MEMBER_TOKEN_URL_QUERY_FIELD) >= 0:
			key_and_value = query_part.split('=')
			new_query_part = "{}={}".format(key_and_value[0], new_followed_member_token)
			query_parts[index] = new_query_part
			break

	return '&'.join(query_parts)

#===============================================================================
# process_shared_url_request : 当分享链接在点击时进行相关的
# 积分计算，如果是分享链接，那么所分享该链接的会员的token信
# 息会出现在url中
#
# 1. 如果cookie携带当前会员的session(假设为b)信息，但是和url中携带的分享会员
#    信息(假设为a)不同，那么进行跳转(url中分享者信息改为b) ，同时计算a对应会
#    员的积分且cookie中设置所关注的会员session信息
# 2. 如果cookie中携带当前会员的session(假设为a)信息，但是和url中携带的分享会
#    员信息(假设为a)相同，那么不进行任何操作;
# 3. 如果cookie中不携带当前会员的session信息，那么进行跳转(url中不携带会员信息)
#===============================================================================
def process_shared_url_request(request):
	followed_member_token = get_followed_member_token_from_url_querystr(request)
	if followed_member_token is None or len(followed_member_token) == 0:
		return None
	member = get_member(request)
	if member:
		if member.token != followed_member_token:
			#第一种情况
			try:
				increase_for_click_shared_url(request)
			except:
				notify_message = u"根据点击计算积分发生异常, url:{}, cause:\n{}".format(
						request.get_full_path(), unicode_full_stack())
				watchdog_fatal(notify_message)

			new_url = _replace_followed_member_token_in_request_url(request, member.token)
			response = HttpResponseRedirect(new_url)
			response.set_cookie(member_settings.FOLLOWED_MEMBER_TOKEN_SESSION_KEY, followed_member_token, max_age=60*60*24*365)
			return response
		else:
			#第二种情况
			return None
	else:
		#第三种情况
		new_url = remove_querystr_filed_from_request_url(request, member_settings.FOLLOWED_MEMBER_TOKEN_URL_QUERY_FIELD)
		response = HttpResponseRedirect(new_url)

		uuid = get_uuid(request)
		if uuid is None:
			uuid = generate_uuid(request)
			request.uuid = uuid
			response.set_cookie(member_settings.UUID_SESSION_KEY, uuid, max_age=60*60*24*365)

		try:
			increase_for_click_shared_url(request)
		except:
			notify_message = u"根据点击计算积分发生异常, url:{}, cause:\n{}".format(
					request.get_full_path(), unicode_full_stack())
			watchdog_fatal(notify_message)

		
		response.set_cookie(member_settings.FOLLOWED_MEMBER_TOKEN_SESSION_KEY, followed_member_token, max_age=60*60*24*365)
		return response

	#其他情况
	return None

def _increase_shared_url_pv(member, shared_url_digest):
	from django.db import connection, transaction
	cursor = connection.cursor()
	cursor.execute("update member_shared_url_info set pv=pv+1 where member_id = %d and shared_url_digest = '%s'" % (member.id, shared_url_digest))
	transaction.commit_unless_managed()
	Member.update_factor(member)

def update_shared_url_pv(request):
	followed_member_token = get_followed_member_token_from_url_querystr(request)
	if followed_member_token is None or len(followed_member_token) == 0:
		return

	member = get_member(request)

	if member and followed_member_token == member.token:
		#如果自己点击自己的分享链接，不进行任何操作
		return

	try:
		followed_member = get_member_by_member_token(followed_member_token)
		if followed_member is None:
			return

		shared_url = get_request_url(request)
		shared_url_digest = get_request_url_digest(request, shared_url)
		
		shared_infos = MemberSharedUrlInfo.objects.filter(member=followed_member, shared_url_digest=shared_url_digest)
		if shared_infos.count() > 0:
			_increase_shared_url_pv(followed_member, shared_url_digest)
		else:
			#title = MemberBrowseRecord.get_title(followed_member, shared_url)
			MemberSharedUrlInfo.objects.create(
				member = followed_member,
				shared_url = shared_url,
				pv = 1,
				shared_url_digest = shared_url_digest,
				title=''
				)
			Member.update_factor(followed_member)
			# notify_message = u"更新分享链接的pvfollowed_member.id:{},member_id:{}m,event_data{}".format(followed_member.id, member.id if member else -1, request.__dict__)
			# watchdog_error(notify_message)
	except:
		notify_message = u"更新分享链接的pv失败, url:{}, cause:\n{}".format(
				request.get_full_path(), unicode_full_stack())
		watchdog_error(notify_message)

def increase_shared_url_followers(member, shared_url_digest):
	from django.db import connection, transaction
	cursor = connection.cursor()
	cursor.execute("update member_shared_url_info set followers=followers+1 where member_id = %d and shared_url_digest = '%s'" % (member.id, shared_url_digest))
	transaction.commit_unless_managed()
	Member.update_factor(member)


################################################################################
#increase_father_member_integral_by_child_member_buyed:购买者为贡献者增加积分
################################################################################
def increase_father_member_integral_by_child_member_buyed(order, webapp_id):
	webapp_user_id = order.webapp_user_id
	integral_settings = IntegralStrategySttings.objects.filter(webapp_id=webapp_id)
	member = WebAppUser.get_member_by_webapp_user_id(webapp_user_id)
	if integral_settings.count() > 0 and member:
		father_member = MemberFollowRelation.get_father_member(member.id)
		if father_member and integral_settings[0].buy_via_offline_increase_count_for_author != 0:
			increase_member_integral(father_member, integral_settings[0].buy_via_offline_increase_count_for_author, u'好友奖励')
			if order.final_price > 0 and integral_settings[0].buy_via_offline_increase_count_percentage_for_author:
				try:
					buy_via_offline_increase_count_percentage_for_author = float(integral_settings[0].buy_via_offline_increase_count_percentage_for_author)
					integral_count = int(order.final_price * buy_via_offline_increase_count_percentage_for_author)
					increase_member_integral(father_member, integral_count, u'好友奖励')
				except:
					notify_message = u"increase_father_member_integral_by_child_member_buyed cause:\n{}".format(unicode_full_stack())
					watchdog_error(notify_message)

def is_integral_detail_used(webapp_id):
	if IntegralStrategySttingsDetail.objects.filter(webapp_id=webapp_id).count() > 0:
		return IntegralStrategySttingsDetail.objects.filter(webapp_id=webapp_id)[0].is_used
	else:
		return None

################################################################################
#increase_detail_integral_for_after_buy:购买后为自己加分（详情加分项）
################################################################################
def increase_detail_integral_for_after_buy(webapp_user_id, webapp_id, final_price):
		integral_settings_detail =	module_api.get_integral_detail(webapp_id)

		if integral_settings_detail:
			member = WebAppUser.get_member_by_webapp_user_id(webapp_user_id)
			if member:
				if integral_settings_detail.increase_count_after_buy > 0:
					increase_count = float(integral_settings_detail.increase_count_after_buy) * final_price
					if (increase_count - int(increase_count)) > 0:
						increase_count = int(increase_count) + 1
					increase_member_integral(member, increase_count, u'购买奖励')

def increase_detail_father_member_integral_by_child_member_buyed(webapp_user_id, webapp_id, final_price):
	integral_settings_detail =	module_api.get_integral_detail(webapp_id)

	if integral_settings_detail:
		member = WebAppUser.get_member_by_webapp_user_id(webapp_user_id)
		if member:
			father_member = MemberFollowRelation.get_father_member(member.id)
			if father_member and integral_settings_detail.buy_increase_count_for_father != 0:
				increase_count = float(integral_settings_detail.buy_increase_count_for_father) * final_price
				if (increase_count - int(increase_count)) > 0:
					increase_count = int(increase_count) + 1

				increase_member_integral(father_member, increase_count, u'好友奖励')

def increase_detail_integral(webapp_user_id, webapp_id, final_price):
	if is_integral_detail_used(webapp_id):
		increase_detail_integral_for_after_buy(webapp_user_id, webapp_id, final_price)
		increase_detail_father_member_integral_by_child_member_buyed(webapp_user_id, webapp_id, final_price)
