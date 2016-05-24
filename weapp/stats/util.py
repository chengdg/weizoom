# -*- coding: utf-8 -*-

__author__ = 'robert'

from datetime import datetime, timedelta
from core import dateutil
import calendar
from django.db.models.query_utils import Q

from core import dateutil
from core import paginator
from modules.member.models import Member, MemberSharedUrlInfo, MemberInfo, WebAppUser, SOURCE_BY_URL, SOURCE_MEMBER_QRCODE, CANCEL_SUBSCRIBED, SUBSCRIBED
from market_tools.tools.member_qrcode.models import MemberQrcode, MemberQrcodeLog
from mall.models import Order, belong_to, ORDER_STATUS_PAYED_SUCCESSED, ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED, ORDER_SOURCE_OWN
from mall.models import OrderHasProduct, Product, PRODUCT_SHELVE_TYPE_ON


RECORDS_PER_PAGE = 10
def get_date_range_for_data(request, start_date = None, end_date = None):
	"""
	获取数据的时间区域
	
	需要request.GET中出现下列参数：

	 * date_interval: 可选，指定时间范围，格式为2014.12.01-2014.12.03
	 * aggregation_type: 数据聚合类型，可选{"day", "week", "month", "year"}, 默认为day
	 * page: 当前页数, 默认为1
	 *  count_per_page：每页数据个数，默认为10
	
	@retval 返回：
	(low_bound, high_bound, dates)三元组，指定需要从数据库中获取的数据的时间范围

	"""
	if start_date and end_date:
		low_bound = datetime.strptime(start_date, '%Y-%m-%d')
		high_bound = datetime.strptime('%s 23:59:59' % end_date, '%Y-%m-%d %H:%M:%S')
		return low_bound, high_bound, dateutil.get_date_range_list(low_bound, high_bound)
	else:
		type2count = {
			'day': 1,
			'week': 7,
			'month': 30,
			'year':365
		}
		aggregation_type = request.GET.get('aggregation_type', 'day')
		day_per_item = type2count[aggregation_type]

		today = datetime.today()
		if aggregation_type == 'day':
			start_date = today
		elif aggregation_type == 'week':
			start_date = today + timedelta(6-today.weekday()) #next sunday
		elif aggregation_type == 'month':
			monthrange = calendar.monthrange(today.year, today.month)
			last_day_of_month = '%s-%s-%s' % (today.year, today.month, monthrange[1])
			start_date = datetime.strptime(last_day_of_month, '%Y-%m-%d')
		else:
			last_day_of_year = '%s-%s-%s' % (today.year, '12', '31')
			start_date = datetime.strptime(last_day_of_year, '%Y-%m-%d')

		cur_page = int(request.GET.get('page', '1'))
		count_per_page = int(request.GET.get('count_per_page', RECORDS_PER_PAGE))
		
		if aggregation_type == 'month':
			#根据当前页码和每页记录个数计算截止日期
			high_bound_date = dateutil.get_month_before((cur_page - 1) * count_per_page + 1)
			
			#根据截止日期往前推count_per_page个月
			low_bound_date = dateutil.get_month_before_of_date(high_bound_date, count_per_page)
			low_bound = '%d-%d-%s 00:00:00' % (low_bound_date.year, low_bound_date.month, '01')
			
			last_day_of_high_bound_month = calendar.monthrange(high_bound_date.year, high_bound_date.month)[1]
			high_bound = '%d-%d-%d 23:59:59' % (high_bound_date.year, high_bound_date.month, last_day_of_high_bound_month)
		elif aggregation_type == 'year':
			#根据当前页码和每页记录个数计算截止日期
			high_bound_year = datetime.now().year - (cur_page - 1) * count_per_page
			high_bound = '%d-%s-%s 23:59:59' % (high_bound_year, '12', '31')
			
			low_bound_year = high_bound_year - count_per_page + 1
			low_bound = '%d-%s-%s 00:00:00' % (low_bound_year, '01', '01')
		else:
			low_bound = '%s 00:00:00' % (start_date - timedelta(cur_page * count_per_page * day_per_item - 1)).strftime('%Y-%m-%d')
			high_bound = '%s 23:59:59' % (start_date - timedelta((cur_page-1) * count_per_page * day_per_item)).strftime('%Y-%m-%d')
			
		low_bound = datetime.strptime(low_bound, '%Y-%m-%d %H:%M:%S')
		high_bound = datetime.strptime(high_bound, '%Y-%m-%d %H:%M:%S')

		return low_bound, high_bound, dateutil.get_date_range_list(low_bound, high_bound)


def get_date_range(request):
	"""
	获取时间范围，如果没有start_date和end_date参数，则默认显示最近7天的日期
	"""
	start_date = request.GET.get('start_date', None)
	end_date = request.GET.get('end_date', None)

	if not end_date:
		#默认显示最近7天的日期
		end_date = dateutil.get_today()

	if not start_date:
		start_date = dateutil.get_previous_date(end_date, 6) #获取7天前日期

	return get_date_range_for_data(request, start_date, end_date)


def daily_formatter(date):
	"""
	用于数据聚合的时间formatter

	 * day: 返回如“12.01”的日期格式
	"""
	# return date.strftime("%m.%d")
	return date.strftime("%Y-%m-%d")


def weekly_formatter(date):
	"""
	用于数据聚合的时间formatter

	 * week: 返回如"12.01-12.07"这样的日期格式
	"""
	weekday = date.weekday()
	monday = date - timedelta(weekday)
	sunday = date + timedelta(6-weekday)
	return '%s-%s' % (monday.strftime("%m.%d"), sunday.strftime('%m.%d'))


def monthly_formatter(date):
	"""
	用于数据聚合的时间formatter

	 * month: 返回如"2014.12"这样的月份格式
	"""
	return date.strftime("%Y.%m")

def yearly_formatter(date):
	return date.strftime("%Y")


def hourly_formatter(date):
	temp = '%s:00-%s:00' % (date.strftime("%H"),(date+timedelta(hours=1)).strftime("%H"))
	if temp == '23:00-00:00':
		return '23:00-24:00'
	return temp


TYPE2FORMATTER = {
	'day': daily_formatter,
	'week': weekly_formatter,
	'month': monthly_formatter,
	'year': yearly_formatter,
	'hour': hourly_formatter
}


def get_formatted_date_list(date_range, date_formatter):
	"""
	获取格式化后的日期列表
	"""
	formatted_date_list = []
	passed_date_dict = {}  #已处理过的日期字典
	
	for date in date_range:
		date = date_formatter(date)
		if passed_date_dict.has_key(date):  #如果处理过该日期则pass
			continue
		
		formatted_date_list.append(date)
		passed_date_dict[date] = 1  #把该日期加入已处理过的日期字典
	
	return formatted_date_list

# 微众商城代码
# #根据webapp_id判断是否是微众商城的订单
# WEISHOP_WEBAPP_ID = '3394'
# OLD_WEISHOP_WEBAPP_ID = '3194'
# def is_weizoom_mall_order(webapp_id):
# 	if webapp_id == WEISHOP_WEBAPP_ID or webapp_id == OLD_WEISHOP_WEBAPP_ID:
# 		return True
#
# 	return False


def get_date2new_member_count(webapp_id, low_date, high_date, date_formatter = None):
	"""
	会员统计相关函数

	@author duhao
	"""
	if not date_formatter:
		date_formatter = TYPE2FORMATTER['day']

	members = Member.objects.filter(
					webapp_id = webapp_id, 
					# is_subscribed = True, 
					#is_for_buy_test = False, 
					is_for_test = False, 
					created_at__range=(low_date, high_date), 
					status__in = (CANCEL_SUBSCRIBED, SUBSCRIBED)
				)
	#初始化数据
	date2new_member_count = {}
	#收集数据
	for member in members:
		date = date_formatter(member.created_at)
		if not date2new_member_count.has_key(date):
			date2new_member_count[date] = 0
		
		date2new_member_count[date] += 1

	return date2new_member_count


def get_new_member_count(webapp_id, low_date, high_date, date_formatter = None):
	"""
	统计新增会员数
	"""
	if not date_formatter:
		date_formatter = TYPE2FORMATTER['day']

	date2new_member_count = get_date2new_member_count(webapp_id, low_date, high_date, date_formatter)
	new_member_count = 0
	for date in date2new_member_count:
		new_member_count += date2new_member_count[date]

	return new_member_count


def get_total_member_count(webapp_id, end_time = None):
	"""
	获取会员总数，包含已取消的人数
	"""
	if end_time:
		total_count = Member.objects.filter(
						webapp_id = webapp_id, 
						# is_subscribed = True, 
						#is_for_buy_test = False, 
						is_for_test = False,
						created_at__lte = end_time, 
						status__in = (CANCEL_SUBSCRIBED, SUBSCRIBED)
					).count()
	else:
		total_count = Member.objects.filter(
						webapp_id = webapp_id, 
						# is_subscribed = True, 
						#is_for_buy_test = False, 
						is_for_test = False, 
						status__in = (CANCEL_SUBSCRIBED, SUBSCRIBED)
					).count()
	return total_count


def get_unsubscribed_member_count(webapp_id):
	"""
	获取取消关注会员总数
	"""
	unsubscribed_member_count = Member.objects.filter(
									webapp_id = webapp_id, 
									is_subscribed = False, 
									#is_for_buy_test = False, 
									is_for_test = False, 
									status__in = (CANCEL_SUBSCRIBED, SUBSCRIBED)
								).count()
	return unsubscribed_member_count


def get_subscribed_member_count(webapp_id):
	"""
	获取关注会员总数
	"""
	subscribed_member_count = Member.objects.filter(
									webapp_id = webapp_id, 
									is_subscribed = True, 
									#is_for_buy_test = False, 
									is_for_test = False
								).count()
	return subscribed_member_count


def get_date2bought_member_count(webapp_id, low_date, high_date, date_formatter = None):
	"""
	统计各个日期的下单会员数
	"""
	if not date_formatter:
		date_formatter = TYPE2FORMATTER['day']

	orders = Order.by_webapp_id(webapp_id).filter(
				order_source=ORDER_SOURCE_OWN, 
				status__in=(ORDER_STATUS_PAYED_SUCCESSED, ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED), 
				created_at__range=(low_date, high_date)
			)

	date2member_set = {}
	for order in orders:
		if order.type == 'test':
			continue
		if order.webapp_user_id != -1 and order.webapp_user_id != 0:
			# webapp_users = WebAppUser.objects.filter(id=order.webapp_user_id)
			# if webapp_users.count() > 0:
			# 	webapp_user = webapp_users[0]
			# 	member = WebAppUser.get_member_by_webapp_user_id(webapp_user.id)
			# 	if member and member.is_for_test is False:
			date = date_formatter(order.created_at)
			if not date2member_set.has_key(date):
				date2member_set[date] = set()
			date2member_set[date].add(order.webapp_user_id)

	date2bought_member_count = {}

	for date in date2member_set:
		date2bought_member_count[date] = len(date2member_set[date])

	return date2bought_member_count


def get_bought_member_count(webapp_id, low_date, high_date):
	"""
	统计下单会员数
	"""
	#这里不能像其他数据一样调用get_date2bought_member_count然后进行加和获取数据
	#要考虑会员滤重问题
	orders = Order.by_webapp_id(webapp_id).filter(
				order_source=ORDER_SOURCE_OWN, 
				status__in=(ORDER_STATUS_PAYED_SUCCESSED, ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED), 
				created_at__range=(low_date, high_date)
			)

	member_set = set()
	for order in orders:
		if order.type == 'test':
			continue
		if order.webapp_user_id != -1 and order.webapp_user_id != 0:
			# webapp_users = WebAppUser.objects.filter(id=order.webapp_user_id)
			# if webapp_users.count() > 0:
			# 	webapp_user = webapp_users[0]
			# member = WebAppUser.get_member_by_webapp_user_id(order.webapp_user_id)
			# if member and member.is_for_test is False:
			member_set.add(order.webapp_user_id)
	
	return len(member_set)


def get_date2share_url_member_count(webapp_id, low_date, high_date, date_formatter = None):
	"""
	统计各个日期发起线上分享的会员数
	"""
	if not date_formatter:
		date_formatter = TYPE2FORMATTER['day']

	share_url_members = MemberSharedUrlInfo.objects.filter(
							member__webapp_id=webapp_id,
							# member__is_subscribed=True, 
							member__is_for_test=False,
							created_at__range=(low_date, high_date)
						)
	
	#收集数据
	date2share_url_member_set = {}
	for member in share_url_members:
		date = date_formatter(member.created_at)
		if not date2share_url_member_set.has_key(date):
			date2share_url_member_set[date] = set()
		
		date2share_url_member_set[date].add(member.member_id)
	
	#处理最终数据
	date2share_url_member_count = {}
	for date in date2share_url_member_set:
		share_url_member_count = len(date2share_url_member_set[date])
		date2share_url_member_count[date] = share_url_member_count
		
	return date2share_url_member_count


def get_share_url_member_count(webapp_id, low_date, high_date):
	"""
	统计发起线上分享的会员数
	"""
	#这里不能像其他数据一样调用get_date2share_url_member_count然后进行加和获取数据
	#要考虑会员滤重问题
	share_url_members = MemberSharedUrlInfo.objects.filter(
							member__webapp_id=webapp_id,
							# member__is_subscribed=True, 
							member__is_for_test=False,
							created_at__range=(low_date, high_date)
						)
	
	#收集数据
	member_set = set()
	for member in share_url_members:
		member_set.add(member.member_id)
		
	return len(member_set)


def get_date2member_from_share_url_count(webapp_id, low_date, high_date, date_formatter = None):
	"""
	统计各个日期通过线上分享新增会员数
	"""
	if not date_formatter:
		date_formatter = TYPE2FORMATTER['day']

	member_id_list = Member.objects.filter(
						webapp_id=webapp_id, 
						source=SOURCE_BY_URL, 
						# is_subscribed=True, 
						is_for_test=False, 
						created_at__range=(low_date, high_date), 
						status__in = (CANCEL_SUBSCRIBED, SUBSCRIBED)
					)
									
	#收集数据
	date2members_from_share_url_set = {}
	for member in member_id_list:
		date = date_formatter(member.created_at)
		if not date2members_from_share_url_set.has_key(date):
			date2members_from_share_url_set[date] = set()
		
		date2members_from_share_url_set[date].add(member.id)
	
	#处理最终数据
	date2member_from_share_url_count = {}
	for date in date2members_from_share_url_set:
		member_from_share_url_count = len(date2members_from_share_url_set[date])
		date2member_from_share_url_count[date] = member_from_share_url_count
		
	return date2member_from_share_url_count


def get_member_from_share_url_count(webapp_id, low_date, high_date):
	"""
	统计通过线上分享新增会员数
	"""
	member_id_list = Member.objects.filter(
						webapp_id=webapp_id, 
						source=SOURCE_BY_URL, 
						# is_subscribed=True, 
						is_for_test=False, 
						created_at__range=(low_date, high_date), 
						status__in = (CANCEL_SUBSCRIBED, SUBSCRIBED)
					)
									
	#收集数据
	members_from_share_url_set = set()
	for member in member_id_list:
		members_from_share_url_set.add(member.id)
	
	return len(members_from_share_url_set)



def get_repeat_buying_member_count(webapp_id, low_date, high_date):
	"""
	获取复购会员数

	检查给定date范围的订单，如果其用户在之前购买过
	"""
	#只统计来源为“本店”的购买订单
	orders = Order.by_webapp_id(webapp_id).filter(
				order_source=ORDER_SOURCE_OWN, 
				created_at__range=(low_date, high_date), 
				status__in=(ORDER_STATUS_PAYED_SUCCESSED, ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED)
			)
	repeat_buying_member_set = set()

	#为了优化查询效率，把所有订单按日期倒序都读出来，然后判断是否有复购订单
	all_orders = Order.by_webapp_id(webapp_id).filter( 
				order_source=ORDER_SOURCE_OWN, 
				#created_at__range=(low_date, high_date), 
				status__in=(ORDER_STATUS_PAYED_SUCCESSED, ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED)
			).order_by('-created_at')
	webapp_user_id2created_at = {}

	# 保留最早时间
	for order in all_orders:
		webapp_user_id2created_at[order.webapp_user_id] = (order.id, order.created_at)

	for order in orders:
		if order.type == 'test':
			continue

		if not order.webapp_user_id in repeat_buying_member_set:
			if order.webapp_user_id != -1 and order.webapp_user_id != 0:
				# webapp_users = WebAppUser.objects.filter(id=order.webapp_user_id)
				# if webapp_users.count() > 0:
				# 	webapp_user = webapp_users[0]
				# member = WebAppUser.get_member_by_webapp_user_id(order.webapp_user_id)
				# if member and member.is_for_test is False:
					#判断在该笔订单前是否有有效订单
				# order_count = Order.objects.filter(
				# 				webapp_user_id=order.webapp_user_id,
				# 				webapp_id=webapp_id, 
				# 				order_source=ORDER_SOURCE_OWN, 
				# 				created_at__lt=order.created_at, 
				# 				status__in=(ORDER_STATUS_PAYED_SUCCESSED, ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED)
				# 			).count()
				# if order_count > 0:
				# 	repeat_buying_member_set.add(order.webapp_user_id)

				(order_id, old_created_at) = webapp_user_id2created_at[order.webapp_user_id]

				if order_id != order.id and old_created_at < order.created_at:
					repeat_buying_member_set.add(order.webapp_user_id)

	return len(repeat_buying_member_set)


def get_date2ori_qrcode_member_count(webapp_id, low_date, high_date, date_formatter = None):
	"""
	获取各个日期发起会员扫码和通过扫码新增的会员数
	"""
	if not date_formatter:
		date_formatter = TYPE2FORMATTER['day']

	qrcode_members = MemberQrcode.objects.filter(
						member__webapp_id=webapp_id,
						# member__is_subscribed=True, 
						member__is_for_test=False, 
						created_at__range=(low_date, high_date)
					)
	
	#初始化数据
	date2ori_qrcode_member = {}
	date2member_from_qrcode = {}

	#收集数据
	for qrcode_member in qrcode_members:
		date = date_formatter(qrcode_member.created_at)
		
		if not date2ori_qrcode_member.has_key(date):
			date2ori_qrcode_member[date] = set()
		
		date2ori_qrcode_member[date].add(qrcode_member.member_id)

	#后处理
	date2qrcode_member_count = {}
	#发起会员扫码用户数
	for date in date2ori_qrcode_member:
		ori_qrcode_member_count = len(date2ori_qrcode_member[date])
		
		if not date2qrcode_member_count.has_key(date):
			date2qrcode_member_count[date] = {}
		if not date2qrcode_member_count[date].has_key('ori_qrcode_member_count'):
			date2qrcode_member_count[date]['ori_qrcode_member_count'] = 0
		date2qrcode_member_count[date]['ori_qrcode_member_count'] = ori_qrcode_member_count

	#处理通过扫码新增的用户列表
	members_from_qrcode = Member.objects.filter(
								webapp_id=webapp_id,
								# is_subscribed=True, 
								is_for_test=False, 
								source=SOURCE_MEMBER_QRCODE, 
								created_at__range=(low_date, high_date)
							)
	for member in members_from_qrcode:
		#计算关注的时间，与发起扫码时间未必在同一天，有可能跨0点
		date = date_formatter(member.created_at)
		if not date2qrcode_member_count.has_key(date):
			date2qrcode_member_count[date] = {}
		if not date2qrcode_member_count[date].has_key('member_from_qrcode_count'):
			date2qrcode_member_count[date]['member_from_qrcode_count'] = 0
		date2qrcode_member_count[date]['member_from_qrcode_count'] += 1
	
	return date2qrcode_member_count


def get_ori_qrcode_member_count(webapp_id, low_date, high_date):
	"""
	获取发起会员扫码和通过会员扫码新增的会员数
	"""
	qrcode_members = MemberQrcode.objects.filter(
						member__webapp_id=webapp_id,
						# member__is_subscribed=True, 
						member__is_for_test=False, 
						member__status__in = (CANCEL_SUBSCRIBED, SUBSCRIBED), 
						created_at__range=(low_date, high_date)
					)

	ori_qrcode_member_set = set()
	member_from_qrcode_count = 0

	#收集数据
	for qrcode_member in qrcode_members:
		ori_qrcode_member_set.add(qrcode_member.member_id)

	#处理通过扫码新增的用户列表
	members_from_qrcode = Member.objects.filter(
								webapp_id=webapp_id,
								# is_subscribed=True, 
								is_for_test=False, 
								source=SOURCE_MEMBER_QRCODE, 
								created_at__range=(low_date, high_date), 
								status__in = (CANCEL_SUBSCRIBED, SUBSCRIBED)
							)
	for member in members_from_qrcode:
		member_from_qrcode_count += 1

	return (len(ori_qrcode_member_set), member_from_qrcode_count)


def get_self_follow_member_count(webapp_id, low_date, high_date):
	"""
	统计直接关注的会员数
	"""
	self_follow_sources = (-1, 0)  #主动关注的来源代码
	self_follow_member_count = Member.objects.filter(
								webapp_id=webapp_id,
								# is_subscribed=True, 
								is_for_test=False, 
								source__in = self_follow_sources, 
								created_at__range=(low_date, high_date), 
								status__in = (CANCEL_SUBSCRIBED, SUBSCRIBED)
							).count()
		
	return self_follow_member_count

def get_date2binding_phone_member_count(webapp_id, low_date, high_date, date_formatter = None):
	"""
	获取各个日期新增的绑定手机会员数
	"""
	if not date_formatter:
		date_formatter = TYPE2FORMATTER['day']

	member_infos = MemberInfo.objects.filter(
						member__webapp_id=webapp_id,
						member__is_for_test=False, 
						binding_time__range=(low_date, high_date)
					)

	date2binding_phone_member_count = {}
	for member_info in member_infos:
		date = date_formatter(member_info.binding_time)
		if not date2binding_phone_member_count.has_key(date):
			date2binding_phone_member_count[date] = 0
		date2binding_phone_member_count[date] += 1

	return date2binding_phone_member_count

def get_binding_phone_member_count(webapp_id, low_date, high_date):
	"""
	获取新增的绑定手机会员数
	"""
	date2binding_phone_member_count = get_date2binding_phone_member_count(webapp_id, low_date, high_date)
	binding_phone_member_count = 0
	for date in date2binding_phone_member_count:
		binding_phone_member_count += date2binding_phone_member_count[date]

	return binding_phone_member_count


####################################################################
#商品统计相关函数
####################################################################
def get_buyer_count(webapp_id, low_date, high_date):
	"""
	获取购买总人数，包括会员、已取消关注的会员和非会员
	"""
	orders = belong_to(webapp_id)
	#使用授权机制后，webapp_user_id对应唯一一个member_id了，不会再有多个webapp_user_idduiying
	buyer_count = orders.filter(
				Q(status__in=(ORDER_STATUS_PAYED_SUCCESSED, ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED)), 
				Q(created_at__range=(low_date, high_date))
			).values('webapp_user_id').distinct().count()
	return buyer_count

def get_order_count(webapp_id, low_date, high_date):
	"""
	获取下单单量
	"""
	orders = belong_to(webapp_id)
	order_count = orders.filter(
				Q(status__in=(ORDER_STATUS_PAYED_SUCCESSED, ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED)), 
				Q(created_at__range=(low_date, high_date))
			).count()
	return order_count

def get_deal_product_count(webapp_id, low_date, high_date):
	"""
	获取总成交件数
	"""
	orders =belong_to(webapp_id).filter(
		status__in=(ORDER_STATUS_PAYED_SUCCESSED, ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED),
		created_at__range=(low_date, high_date))
	order_ids = [order.id for order in orders]

	products = OrderHasProduct.objects.filter(
			order_id__in=order_ids
		)
	deal_product_count = 0
	for product in products:
		deal_product_count += product.number
	return deal_product_count


def get_top10_product(webapp_id, low_date, high_date):
	"""
	获取下单单量排行前10的商品
	"""
	orders =belong_to(webapp_id).filter(
		status__in=(ORDER_STATUS_PAYED_SUCCESSED, ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED),
		created_at__range=(low_date, high_date)
	)
	order_ids = [order.id for order in orders]
	products = OrderHasProduct.objects.filter(
		order_id__in=order_ids
	)

	product_id2num = {}
	for product in products:
		if not product_id2num.has_key(product.product_id):
			product_id2num[product.product_id] = 0
		product_id2num[product.product_id] += 1

	#按下单单量倒序
	sorted_product_id2num = sorted(product_id2num.items(), key=lambda d:d[1], reverse = True)

	top10_product_list = []
	i = 1
	for item in sorted_product_id2num:
		product_id = item[0]
		product_name = ''
		try:
			product = Product.objects.get(id=product_id)
			product_name = product.name
		except:
			pass
		num = item[1]
		top10_product_list.append({
			'rank': i,
			'product_id': product_id,
			'product_name': product_name,
			'num': num
		})
		i += 1
		if i > 10:
			break

	return top10_product_list

####################################################################
#订单统计相关函数
####################################################################


#获取成交订单
def get_transaction_orders(webapp_id,low_date,high_date):
	orders = belong_to(webapp_id)
	transaction_orders = orders.filter(
		Q(created_at__range=(low_date,high_date)),
		Q(status__in=(ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED))
		)
	return transaction_orders

#获取成交金额
def get_transaction_money(transaction_nums):
	transaction_money = 0.00
	for transaction in transaction_nums:
		if transaction.origin_order_id > 0:
			#商户从微众自营商城同步的子订单需要计算采购价
			tmp_transaction_money = round(transaction.total_purchase_price,2)
		else:
			tmp_transaction_money = round(transaction.final_price,2) + round(transaction.weizoom_card_money,2)
		transaction_money += tmp_transaction_money
	return transaction_money

#获取成交金额及成交订单数目
def get_transaction_money_order_count(webapp_id,low_date,high_date):
	orders = get_transaction_orders(webapp_id,low_date,high_date)
	transaction_money = get_transaction_money(orders)
	order_count = orders.count()
	return transaction_money,order_count
