# -*- coding: utf-8 -*-
import json
import copy

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from core import apiview_util, dateutil
from core import paginator
from core.jsonresponse import JsonResponse, create_response
from django.http import HttpResponseRedirect, HttpResponse

from account.models import *
from webapp.modules.mall.models import *
from webapp.statistics_views import get_buy_trend as webapp_get_buy_trend, get_visit_daily_trend as webapp_get_visit_daily_trend
from weixin.statistics.api_views import get_message_daily_trend as webapp_get_message_daily_trend
from webapp.modules.mall import models
from settings import APP_VERSION, APP_DOWNLOAD_URL


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
