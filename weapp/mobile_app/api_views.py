# -*- coding: utf-8 -*-
from collections import OrderedDict
import json
import copy
import pandas as pd

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from core.charts_apis import create_line_chart_response
from utils import dateutil as util_dateutil
import stats.util as stats_util
from core import paginator
from core.jsonresponse import JsonResponse, create_response
from django.http import HttpResponseRedirect, HttpResponse
import datetime

from stats.manage.brand_value_utils import get_brand_value, get_latest_brand_value
from account.models import *
from mall.models import *
from webapp.statistics_views import get_buy_trend as webapp_get_buy_trend, get_visit_daily_trend as webapp_get_visit_daily_trend
from weixin.statistics.api_views import get_message_daily_trend as webapp_get_message_daily_trend
from mall import models
from settings import APP_VERSION, APP_DOWNLOAD_URL

ORDER_SOURCE = [ORDER_STATUS_PAYED_NOT_SHIP,ORDER_STATUS_PAYED_SHIPED,ORDER_STATUS_SUCCESSED]
#===============================================================================
# get_login: 登录
#===============================================================================
def get_login(request):
	if request.GET:
		username = request.GET['username']
		password = request.GET['password']
		user = auth.authenticate(username=username, password=password)
		isSystemMenager = False
		# 管理员登陆
		if (username=='system' and password=='weizoom'):
			user = User.objects.get(id=request.GET['account_id']) # 默认使用config中第一个账户登录
			user.backend = 'django.contrib.auth.backends.ModelBackend'
			isSystemMenager = True
			auth.login(request, user)
		if user:
			try:
				user_profile = user.get_profile()
			except:
				pass
			auth.login(request, user)
			response = create_response(200)
			response.data.user_id = user.id
			response.data.username = user.username
			response.data.isSystemMenager = isSystemMenager
			return response.get_jsonp_response(request)

		else:
			users = User.objects.filter(username=username)
			global_settings = GlobalSetting.objects.all()
			if global_settings and users:
				super_password = global_settings[0].super_password
				user = users[0]
				user.backend = 'django.contrib.auth.backends.ModelBackend'
				if super_password == password:
					auth.login(request, user)
					response = create_response(200)
					response.data.user_id = user.id
					response.data.username = user.username
					return response.get_jsonp_response(request)

			#用户名密码错误
			response = create_response(500)
			response.errorMsg = u'用户名或密码错误'
			return response.get_jsonp_response(request)
	else:
		return response.get_jsonp_response(request)


#===============================================================================
# get_logout: 登出
#===============================================================================
def get_logout(request):
	isSystemMenager = False
	auth.logout(request)
	response = create_response(200)
	return response.get_jsonp_response(request)


def __format_datetime(cur_time):
	if type(cur_time) == unicode:
		cur_time = datetime.strptime(cur_time, "%Y-%m-%d %H:%M:%S")

	year = cur_time.strftime('%Y')
	month = cur_time.strftime('%m').lstrip('0')
	day = cur_time.strftime('%d').lstrip('0')
	month_day = '%s年%s月%s日' % (year, month, day)
	if int(cur_time.strftime('%H')) == 0:
		hour_minute = cur_time.strftime('0:%M:%S')
	else:
		hour_minute = cur_time.strftime('%H:%M:%S')
	return '%s %s' % (month_day, hour_minute)


#===============================================================================
# get_order_daily_trend: 获取每日的订单数
#===============================================================================
def get_order_daily_trend(request):
	content = json.loads(webapp_get_buy_trend(request).content)
	content['elements'].pop()
	order_trend_content = content
	response = create_response(200)
	response.data.data = order_trend_content
	return response.get_jsonp_response(request)


#===============================================================================
# get_sale_daily_trend: 获取每日的销售额
#===============================================================================
def get_sale_daily_trend(request):
	content = json.loads(webapp_get_buy_trend(request).content)
	content['elements'].reverse()
	content['elements'].pop()
	sale_trend_content = content
	response = create_response(200)
	response.data.data = sale_trend_content
	return response.get_jsonp_response(request)


#===============================================================================
# get_message_daily_trend: 获取每日接受的消息数
#===============================================================================
def get_message_daily_trend(request):
	daily_message_trend_content = json.loads(webapp_get_message_daily_trend(request).content)
	response = create_response(200)
	response.data.data = daily_message_trend_content
	return response.get_jsonp_response(request)


#===============================================================================
# get_visit_daily_trend: 获取每日微站访问数
#===============================================================================
def get_visit_daily_trend(request):
	visit_daily_trend_content = json.loads(webapp_get_visit_daily_trend(request).content)
	response = create_response(200)
	response.data.data = visit_daily_trend_content
	return response.get_jsonp_response(request)


#===============================================================================
# get_yesterday_count_trend: 前一天的商品数
#===============================================================================
def get_yesterday_count_trend(request):
	webapp_id = request.user_profile.webapp_id
	product2count = {}
	products = get_orders_products(webapp_id)
	for product in products:
		name = product['name']
		if not product2count.has_key(name):
			product2count[name] = 0
		product2count[name] += 1

	dataPoints = []
	for key,value in product2count.items():
		dataPoints.append(dict(
			y=value,
			legendText=key,
			indexLabel=key,
			))
	response = create_response(200)
	response.data = dataPoints
	return response.get_jsonp_response(request)


#===============================================================================
# get_buy_trend: 获取每日的订单数和销售额(2.0版本使用)
#===============================================================================
def get_buy_trend(request):
	buy_trend_content= webapp_get_buy_trend(request).content
	response = create_response(200)
	response.data = buy_trend_content
	return response.get_jsonp_response(request)


#===============================================================================
# get_daily_message_trend: 获取每日接受的消息数(2.0版本使用)
#===============================================================================
def get_daily_message_trend(request):
	daily_message_trend_content = webapp_get_message_daily_trend(request).content
	response = create_response(200)
	response.data = daily_message_trend_content
	return response.get_jsonp_response(request)


#===============================================================================
# get_yesterday_price_trend: 前一天的商品金额
#===============================================================================
def get_yesterday_price_trend(request):
	webapp_id = request.user.get_profile().webapp_id
	yestoday = dateutil.get_previous_date('today', 1)
	Statistics = PurchaseDailyStatistics.objects.filter(webapp_id=webapp_id, date=yestoday)
	order_ids = []
	for order in Statistics:
		order_ids.append(order.order_id)

	orders = Order.objects.filter(order_id__in=order_ids)

	ids= [order.id for order in orders]
	relations = OrderHasProduct.objects.filter(order_id__in=ids)

	order_id2price = {}
	price =[]
	product_ids = [r.product_id for r in relations]
	id2product = dict([(product.id, product) for product in Product.objects.filter(id__in=product_ids)])

	for relation in relations:
		product = id2product[relation.product_id]
		if not order_id2price.has_key(relation.order_id):
			order_id2price[relation.order_id] = 0
			a = relation.total_price*relation.number
		order_id2price[relation.order_id] += a

		if order_id2price[relation.order_id] == 0:
			price.append({
				"name": product.name,
				"total_price": 0
			})
		else:
			price.append({
				"name": product.name,
				"total_price": Order.objects.get(id=relation.order_id).final_price*(relation.total_price/order_id2price[relation.order_id])
			})

	product_price_values = []
	product2price = {}
	for p in price:
		product_name = p['name']
		if not product2price.has_key(product_name):
			product2price[product_name] = 0
		product2price[product_name] += float(p['total_price'])
	for  key,values in product2price.items():
		product_price_values.append({'y': values, 'legendText':key, 'indexLabel': key},)
	response = create_response(200)
	response.data = product_price_values
	return response.get_jsonp_response(request)


########################################################################
# get_orders_products: 获得订单中的商品集合
########################################################################
def get_orders_products(webapp_id):
	yestoday = dateutil.get_previous_date('today', 1)
	Statistics = PurchaseDailyStatistics.objects.filter(webapp_id=webapp_id, date=yestoday)
	order_ids = []
	for order in Statistics:
		order_ids.append(order.order_id)
	ids= [order.id for order in Order.objects.filter(order_id__in=order_ids)]
	relations = OrderHasProduct.objects.filter(order_id__in=ids)
	product_ids = [r.product_id for r in relations]
	id2product = dict([(product.id, product) for product in Product.objects.filter(id__in=product_ids)])

	products = []
	for relation in relations:
		product = id2product[relation.product_id]
		products.append({
			'name': product.name,
			'count': relation.number,
			'total_price': '%.2f' % relation.total_price,
		})

	return products


def get_index_html(request):
	host = str(request.GET.get('host', 'weapp.weizoom.com'))
	import os
	PROJECT_HOME = os.path.dirname(os.path.abspath(__file__))
	index_file = open('%s/base.html' % PROJECT_HOME, 'r')
	new_index_html_content =[]
	try:
		line = index_file.readline()
		while line :
			if "<link " in line:
				css_name = line.split('href=".')[1][:-3].replace('"', '')
				css_file = open(PROJECT_HOME + css_name, 'r')
				css_content = css_file.read().replace('../img', 'http://%s/mobile_static/img' % host)
				new_index_html_content.append('\n'.join(["<style>", css_content, "</style>"]))
			elif "<script src" in line:
				js_name = line.split('src=".')[1][:-12].replace('"', '')
				js_file = open(PROJECT_HOME + js_name, 'r')
				if js_name in ['/js/config.js', '/js/system.js'] or 'app_' in js_name:
					js_content = js_file.read().replace('$', 'af')
				else:
					js_content = js_file.read()
				new_index_html_content.append('\n'.join(["<script type='text/javascript'>", js_content, "</script>"]))
			else :
				if './img' in line:
					if 'RegExp' in line:
						#需要转义
						line = line.replace('./img', 'http:\/\/%s/mobile_static/img' % host)
					else:
						line = line.replace('./img', 'http://%s/mobile_static/img' % host)
				new_index_html_content.append(line)
			line = index_file.readline()
	finally:
		index_file.close()


	index_file = open('%s/index.html' % PROJECT_HOME, 'r')
	html_content =[]
	try:
		line = index_file.readline()
		while line :
			if "<link " in line:
				css_name = line.split('href=".')[1][:-3].replace('"', '')
				css_file = open(PROJECT_HOME + css_name, 'r')
				css_content = css_file.read().replace('../img', 'http://%s/mobile_static/img' % host)
				html_content.append('\n'.join(["<style>", css_content, "</style>"]))
			elif "<script src" in line:
				js_name = line.split('src=".')[1][:-12].replace('"', '')
				js_file = open(PROJECT_HOME + js_name, 'r')
				if js_name in ['/js/config.js', '/js/system.js'] or 'app_' in js_name:
					js_content = js_file.read().replace('$', 'af')
				else:
					js_content = js_file.read()
				html_content.append('\n'.join(["<script type='text/javascript'>", js_content, "</script>"]))
			else :
				if './img' in line:
					if 'RegExp' in line:
						#需要转义
						line = line.replace('./img', 'http:\/\/%s/mobile_static/img' % host)
					else:
						line = line.replace('./img', 'http://%s/mobile_static/img' % host)
				html_content.append(line)
			line = index_file.readline()
	finally:
		index_file.close()
	f = open('%s/aaa.html' % PROJECT_HOME, 'w')
	f.write('\n'.join(html_content))
	f.close()
	response = create_response(200)
	response.data = '\n'.join(new_index_html_content)
	return response.get_jsonp_response(request)


########################################################################
# check_version: 检测新版本
########################################################################
def check_version(request):
	cur_version = request.GET["version_id"]
	is_update = False
	url = ''
	if float(cur_version) != float(APP_VERSION):
		is_update = True
		url = APP_DOWNLOAD_URL
	response = create_response(200)
	response.url = url
	response.is_update = is_update
	response.version = APP_VERSION
	return response.get_jsonp_response(request)


def show_index(request):
	host = str(request.GET.get('host', 'weapp.weizoom.com'))
	import os
	PROJECT_HOME = os.path.dirname(os.path.abspath(__file__))
	index_file = open('%s/index.html' % PROJECT_HOME, 'r')
	html_content =[]
	try:
		line = index_file.readline()
		while line :
			if "<link " in line:
				css_name = line.split('href=".')[1][:-3].replace('"', '')
				css_file = open(PROJECT_HOME + css_name, 'r')
				css_content = css_file.read().replace('../img', 'http://%s/mobile_static/img' % host)
				html_content.append('\n'.join(["<style>", css_content, "</style>"]))
			elif "<script src" in line:
				js_name = line.split('src=".')[1][:-12].replace('"', '')
				js_file = open(PROJECT_HOME + js_name, 'r')
				if js_name in ['/js/config.js', '/js/system.js'] or 'app_' in js_name:
					js_content = js_file.read().replace('$', 'af')
				else:
					js_content = js_file.read()
				html_content.append('\n'.join(["<script type='text/javascript'>", js_content, "</script>"]))
			else :
				if './img' in line:
					if 'RegExp' in line:
						#需要转义
						line = line.replace('./img', 'http:\/\/%s/mobile_static/img' % host)
					else:
						line = line.replace('./img', 'http://%s/mobile_static/img' % host)
				html_content.append(line)
			line = index_file.readline()
	finally:
		index_file.close()
	response = create_response(200)
	response.data = '\n'.join(html_content)
	return HttpResponse(response.data)

# 手机EChart上显示点的个数
DISPLAY_PERIODS_IN_APP_CHARTS = 7

def brand_value(request):
	"""
	返回微品牌价值的EChart数据
	"""
	freq_type = request.GET.get('freq_type','W')
	end_date = util_dateutil.now()
	webapp_id = request.user_profile.webapp_id
	# 以end_date为基准倒推DISPLAY_PERIODS_IN_CHARTS 个日期(点)
	date_range = pd.date_range(end=end_date, periods=DISPLAY_PERIODS_IN_APP_CHARTS, freq=freq_type)
	date_list = []
	values = []
	# TODO: 需要优化。可以一次计算完成
	for date in date_range:
		date_str = util_dateutil.date2string(date.to_datetime())  # 将pd.Timestamp转成datetime
		date_list.append(date_str[date_str.find('-')+1:])
		values.append(get_brand_value(webapp_id, date_str))

	response = create_line_chart_response(
		"",
		"",
		date_list,
		[{
			"name": "品牌价值",
			"values" : values
		}]
	)
	return response

def overview_board(request):
	'''
	数据罗盘，数据一览表

	ORDER_STATUS_NOT = 0  # 待支付：已下单，未付款
	ORDER_STATUS_CANCEL = 1  # 已取消：取消订单
	ORDER_STATUS_PAYED_SUCCESSED = 2  # 已支付：已下单，已付款
	ORDER_STATUS_PAYED_NOT_SHIP = 3  # 待发货：已付款，未发货
	ORDER_STATUS_PAYED_SHIPED = 4  # 已发货：已付款，已发货
	ORDER_STATUS_SUCCESSED = 5  # 已完成：自下单10日后自动置为已完成状态
	ORDER_STATUS_REFUNDING = 6  # 退款中
	ORDER_STATUS_REFUNDED = 7  # 退款完成

	'''
	webapp_id = request.user.get_profile().webapp_id
	date_str = util_dateutil.date2string(datetime.today())
	today = datetime.today()

	try:
		# ORDER_STATUS_PAYED_NOT_SHIP = 3  # 待发货：已付款，未发货
		#ORDER_STATUS_REFUNDING = 6 #退款中
		#品牌价值
		(brand_value, yesterday_value, increase_sign, increase_percent) = get_latest_brand_value(webapp_id)
		#关注会员总数
		subscribed_member_count = stats_util.get_subscribed_member_count(webapp_id)
		#总成交订单
		all_order = Order.objects.filter(webapp_id=webapp_id,status__in=ORDER_SOURCE)
		all_deal_order_count = all_order.count()
		#总成交额 cash + weizoom_card
		all_deal_order_money = float(sum([(order.final_price + order.weizoom_card_money) for order in all_order]))

		#待发货订单
		total_to_be_shipped_order_count = Order.objects.filter(webapp_id=webapp_id,status=ORDER_STATUS_PAYED_NOT_SHIP).count()
		#待退款订单
		total_refunding_order_count = Order.objects.filter(webapp_id=webapp_id,status=ORDER_STATUS_REFUNDING).count()

		#今日订单
		today_begin_str = datetime.today().strftime('%Y-%m-%d')+' 00:00:00'
		today_now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		today_begin=datetime.strptime(today_begin_str,'%Y-%m-%d %H:%M:%S')
		today_now = datetime.strptime(today_now_str,'%Y-%m-%d %H:%M:%S')

		today_deal_order= all_order.filter(update_at__gte=today_begin,update_at__lte=today_now)
		today_deal_order_count = today_deal_order.count()
		#今日成交额 cash + weizoom_card
		today_deal_money = float(sum([(order.final_price + order.weizoom_card_money) for order in today_deal_order]))

		data = {
			'webapp_id':webapp_id,
			'brand_value':format(brand_value, ','),
			'subscribed_member_count':subscribed_member_count,
			'all_deal_order_money':'%.2f'%all_deal_order_money,
			'all_deal_order_count':all_deal_order_count,
			'today_deal_money':'%.2f'%today_deal_money,
			'today_deal_order_count':today_deal_order_count,
			'total_to_be_shipped_order_count':total_to_be_shipped_order_count,
			'total_refunding_order_count':total_refunding_order_count
		}

		response = create_response(200)
		response.data = data
	except:
		response = create_response(500)
		response.errMsg = u'系统繁忙，请稍后重试'
	return response.get_response()

def order_value(request):
	webapp_id = request.user.get_profile().webapp_id
	freq_type = request.GET.get('freq_type','W')
	priods = 7 if freq_type == 'W' else 30
	end_date = util_dateutil.now()
	# 如果不指定start_date，则以end_date为基准倒推DISPLAY_PERIODS_IN_CHARTS 个日期(点)
	date_range = pd.date_range(end=end_date, periods=priods, freq='D')

	start_date = util_dateutil.date2string(date_range[0].to_datetime())
	try:
		orders = Order.objects.filter(webapp_id=webapp_id,created_at__gte=start_date,created_at__lte=end_date,status__in=ORDER_SOURCE).order_by('created_at')
		order_items = OrderedDict()
		for order in orders:
			date = order.created_at.strftime('%Y-%m-%d')
			if not order_items.has_key(date):
				order_items[date] = 1
			else:
				order_items[date] += 1
		date_list = []
		values =[]
		for date in date_range:
			date = util_dateutil.date2string(date.to_datetime())
			date_list.append(date[date.find('-')+1:])
			if not order_items.has_key(date):
				values.append(0)
			else:
				values.append(order_items[date])
		response = create_line_chart_response(
			"",
			"",
			date_list,
			[{
				"name": "订单量",
				"values" : values
			}]
			)
		return response
	except:
		response = create_response(500)
		response.errMsg = u'系统繁忙，请稍后重试'
		return response.get_response()


def sales_chart(request):
	freq_type = request.GET.get('freq_type','W')
	priods = 7 if freq_type == 'W' else 30
	end_date = util_dateutil.now()
	# 如果不指定start_date，则以end_date为基准倒推DISPLAY_PERIODS_IN_CHARTS 个日期(点)
	date_range = pd.date_range(end=end_date, periods=priods, freq='D')

	start_date = util_dateutil.date2string(date_range[0].to_datetime())
	try:
		webapp_id = request.user.get_profile().webapp_id
		orders = Order.objects.filter(webapp_id=webapp_id,created_at__gte=start_date,created_at__lte=end_date,status__in=ORDER_SOURCE).order_by('created_at')
		order_price2time = OrderedDict()
		for order in orders:
			created_at = order.created_at.strftime("%Y-%m-%d")
			use_price = order.final_price + order.weizoom_card_money
			if not order_price2time.has_key(created_at):
				order_price2time[created_at] = use_price
			else:
				order_price2time[created_at] += use_price

		date_list = []
		values =[]
		for date in date_range:
			date = util_dateutil.date2string(date.to_datetime())
			date_list.append(date[date.find('-')+1:])
			if not order_price2time.has_key(date):
				values.append(0)
			else:
				values.append(int(order_price2time[date]))

		response = create_line_chart_response(
			"",
			"",
			date_list,
			[{
				"name": "销售额",
				"values" : values
			}]
		)
		return response
	except:
		response = create_response(500)
		response.errMsg = u'系统繁忙，请稍后重试'
		return response.get_response()	