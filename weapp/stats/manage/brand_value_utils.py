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

def compute_brand_value(webapp_id, end_date):
	"""
	根据webapp_id计算品牌end_date当天的价值
	"""
	end_date = util_dateutil.parse_datetime(end_date+" 23:59:59")
	start_date = util_dateutil.get_date_after_days(end_date, -365) # 一年前
	print("start_date:{}, end_date:{}".format(start_date, end_date))
	orders = Order.objects.filter(webapp_id=webapp_id, created_at__range=(start_date, end_date))
	order_count = orders.count()
	print("order count: {}".format(orders.count()))
	if order_count<1:
		return 0.0
	order_data = [(order.webapp_user_id, order.final_price, order.created_at, order.id) for order in orders]
	df = pd.DataFrame(order_data, columns=['wuid', 'fp', 'at', 'id'])
	# 计算购买用户前1000人的平均消费金额
	user_avg_consumption = df[['wuid', 'fp']].groupby('wuid').sum().sort('fp', ascending=False).head(1000).mean()['fp']  # type: numpy.float64
	print("user average consumption: {}".format(user_avg_consumption))
	# 计算多次购买的用户数数
	buyer_counts = df[df['fp']>1]['wuid'].value_counts()
	buyer_count = len(buyer_counts.keys())
	print("buyer count: {}".format(buyer_count))
	value = user_avg_consumption * buyer_count
	return value


def get_brand_value(webapp_id, date_str):
	"""
	获取品牌价值的接口（如果数据库中有非今日的缓存值，则取出；否则计算并存入数据库）

	@retval brand_value(整型，单位元)
	"""
	cached = BrandValueHistory.objects.filter(webapp_id=webapp_id, value_date=date_str)
	today = util_dateutil.date2string(util_dateutil.now())

	# 如果有缓存的数据，从数据库取数据
	#print("date_str: {}, count: {}".format(date_str, cached.count()))
	if date_str != today and cached.count()>0:
		brand_value = int(cached[0].value)
	else:
		if cached.count()>0:
			cached.delete()
		brand_value = compute_brand_value(webapp_id, date_str)
		#print("date_str: {}, value: {}".format(date_str, brand_value))
		try:
			BrandValueHistory.objects.create(
				webapp_id=webapp_id,
				value_date=date_str,
				value=brand_value)
		except:
			notify_msg = u"存微品牌数据失败, cause:\n{}".format(unicode_full_stack())
			watchdog_error(notify_msg)
		brand_value = int(brand_value)
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
