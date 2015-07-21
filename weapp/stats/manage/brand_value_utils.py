#coding: utf8
#author: Victor

#import json
#from datetime import datetime


from mall.models import *
from utils import dateutil as util_dateutil
import pandas as pd
#from core import dateutil
#from webapp import models as webapp_models
#from webapp import statistics_util as webapp_statistics_util
from core.charts_apis import *
#from django.conf import settings
#import stats.util as stats_util
from stats.models import BrandValueHistory

from core.exceptionutil import unicode_full_stack
#from watchdog.utils import watchdog_error, watchdog_warning
import numpy as np
from stats import order_utils

# 用户有效购买周期(即微品牌统计中，只算一个用户在CPP范围内的订单。单位:自然日)
CUSTOMER_PURCHASE_PERIOD = 360

def compute_brand_value(webapp_id, end_date, period=CUSTOMER_PURCHASE_PERIOD):
	"""
	根据webapp_id计算品牌end_date当天的价值
	"""
	end_date = util_dateutil.parse_datetime(end_date+" 23:59:59")
	start_date = util_dateutil.get_date_after_days(end_date, -period) # 一年前
	print("start_date:{}, end_date:{}".format(start_date, end_date))
	# 获取已经支付过的订单
	orders = order_utils.get_paid_orders(webapp_id, start_date, end_date)
	order_count = orders.count()
	print("order count: {}".format(orders.count()))
	if order_count<1:
		return 0.0
	order_data = [(order.webapp_user_id, order.final_price, order.created_at, order.id) for order in orders]
	df = pd.DataFrame(order_data, columns=['wuid', 'fp', 'at', 'id'])
	# 计算购买用户前20%人的平均消费金额
	head_count= int(order_count*0.2+1)
	user_avg_consumption = df[['wuid', 'fp']].groupby('wuid').sum().sort('fp', ascending=False).head(head_count).mean()['fp']  # type: numpy.float64
	# 计算多次购买的用户数数
	buyer_counts = df[df['fp']>1]['wuid'].value_counts()
	buyer_count = len(buyer_counts.keys())
	print("head_order_cnt:{}, user_avg_consumption:{}, buyer_cnt:{}".format(head_count, user_avg_consumption, buyer_count))
	#print("buyer count: {}".format(buyer_count))
	value = user_avg_consumption * buyer_count
	return value


def compute_buyer_count(webapp_id, start_date, period_days):
	"""
	计算webapp用户的已购客户数
	
	@param start_date 开始日期str(年月日)

	"""
	end_date = util_dateutil.get_date_after_days(util_dateutil.parse_date(start_date), period_days) # 一年前
	#print("start_date:{}, end_date:{}".format(start_date, end_date))
	# 获取已经支付过的订单
	orders = order_utils.get_paid_orders(webapp_id, start_date, end_date)
	order_count = orders.count()
	#print("order count: {}".format(orders.count()))
	if order_count<1:
		return 0
	order_data = [(order.webapp_user_id, order.final_price, order.created_at, order.id) for order in orders]
	df = pd.DataFrame(order_data, columns=['wuid', 'fp', 'at', 'id'])
	# 计算购买用户前20%人的平均消费金额
	#head_count= int(order_count*0.2+1)
	#user_avg_consumption = df[['wuid', 'fp']].groupby('wuid').sum().sort('fp', ascending=False).head(head_count).mean()['fp']  # type: numpy.float64
	# 计算多次购买的用户数数
	buyer_counts = df[df['fp']>0]['wuid'].value_counts()
	buyer_count = len(buyer_counts.keys())
	#print("head_order_cnt:{}, user_avg_consumption:{}, buyer_cnt:{}".format(head_count, user_avg_consumption, buyer_count))
	#print("buyer count: {}".format(buyer_count))
	#value = user_avg_consumption * buyer_count
	return buyer_count


def get_brand_value(webapp_id, date_str):
	"""
	获取品牌价值的接口（如果数据库中有非今日的缓存值，则取出；否则计算并存入数据库）

	@retval brand_value(整型，单位元)
	"""
	cached, created = BrandValueHistory.objects.get_or_create(webapp_id=webapp_id, value_date=date_str)
	today = util_dateutil.date2string(util_dateutil.now())

	# 如果有缓存的数据，从数据库取数据
	#print("date_str: {}, count: {}".format(date_str, cached.count()))
	if date_str != today and not created:
		brand_value = int(cached.value)
	else:
		brand_value = 0
		try:
			brand_value = compute_brand_value(webapp_id, date_str)
			#print("date_str: {}, value: {}".format(date_str, brand_value))
			#BrandValueHistory.objects.create(
			#	webapp_id=webapp_id,
			#	value_date=date_str,
			#	value=brand_value)
			cached.webapp_id = webapp_id
			cached.value_date = date_str
			cached.value = brand_value
			cached.save()
			brand_value = int(brand_value)
		except:
			notify_msg = u"存微品牌数据失败, cause:\n{}".format(unicode_full_stack())
			watchdog_error(notify_msg)
	return brand_value



def get_latest_brand_value(webapp_id):
	"""
	获取当前微品牌值

	@retval today_value 今日微品牌值
	@retval yesterday_value 昨天的微品牌值
	@retval is_increasing True表示上涨，False表示下降
	@retval increase_percent 涨幅比例(%)
	"""
	today = util_dateutil.now()
	date_str = util_dateutil.date2string(today)
	yesterday = util_dateutil.get_date_after_days(today, -1)
	yesterday_date_str = util_dateutil.date2string(yesterday)

	today_value = get_brand_value(webapp_id, date_str)
	yesterday_value = get_brand_value(webapp_id, yesterday_date_str)
	delta = today_value-yesterday_value
	if today_value == 0:
		increase_percent = 0.0
	else:
		increase_percent = abs(round((delta*100.0 / today_value), 2))

	return (today_value, yesterday_value, int(np.sign(delta)), increase_percent)
