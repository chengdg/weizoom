#coding:utf8
"""
微品牌价值计算命令行工具

用法：
```
python manage.py shell
>> from stats.manage import brand_value_tool as bv
>> reload(bv)
>> bv.get_brand_value_by_account('hongjinding')
```

"""

from brand_value_utils import compute_brand_value, compute_buyer_count
from test import bdd_util
from utils import dateutil as util_dateutil
from stats.utils.Table import Table
import pandas as pd

def get_brand_value_by_account(account_name, date_str=None):
	"""
	根据account name获取微品牌价值
	"""
	# 根据account_name获取webapp_id
	webapp_id = bdd_util.get_webapp_id_for(account_name)
	#print("webapp_id: {}".format(webapp_id))
	date = date_str
	if date_str is None:
		date = util_dateutil.date2string(util_dateutil.now())
	value = compute_brand_value(webapp_id, date)

	print("webapp_id:{}, date:{}, value:{}".format(webapp_id, date, value))
	return value


def analyze_account_brand_values(name, start_date, end_date, freq='MS'):
	"""
	分析给定用户列表的微品牌
	"""
	date_range = pd.date_range(start=start_date, end=end_date, freq=freq)
	values = []
	for date in date_range:
		date_str = util_dateutil.date2string(date.to_datetime())
		values.append( (name, date_str, get_brand_value_by_account(name, date_str)))
	return values


def analyze_buyer_counts(account_name, start_date, period_list):
	"""
	分析已购用户数
	"""
	webapp_id = bdd_util.get_webapp_id_for(account_name)

	values = [(account_name, period, compute_buyer_count(webapp_id, start_date, period)) for period in period_list]
	return values


def generate_buyer_count_report(report_file, account_infos, period_list):
	"""
	生成已购用户报表

	表结构：fans账号、项目起始运营时间、已购客户数（运营日起）

	@param account_info 包括account_name和项目起始时间的二元组，例如 [('hongjinding', '2015-04-20')]

	应用举例：
	```
	account_infos = [('hongjinding','2015-4-20'), ('tianreyifang','2015-6-5'), ('fxkj','2014-11-12'), ('tianmashengwu','2015-6-8'), ('hanjin','2014-11-4'),]
	bvt.generate_buyer_count_report('report2.html', account_infos, [30, 60, 90, 120])
	```
	"""
	table = Table("report")
	counter = 0
	for info in account_infos:
		try:
			account_name = info[0]
			print("account: {}".format(account_name))
			start_date = info[1]
			values = analyze_buyer_counts(account_name, start_date, period_list)
			for value in values:
				period = value[1]
				count = value[2]
				table.put(account_name, 'START', start_date)
				table.put(account_name, period, count)
			counter += 1
		except Exception as e:
			print('Exception: %s' % str(e).strip())
	table.to_html(report_file)
	print("saved to {}, counter={}".format(report_file, counter))
	return



def generate_accounts_BV_report(report_file, name_list, start_date, end_date, freq='MS'):
	"""
	生成分析微品牌的报告数据

	操作举例：比如想导出2015-01-01至2015-07-01之间的微品牌数据
	```
	names=['ainicoffee','gangshanxigu']
	bvt.generate_accounts_BV_report('report.html', names, '2015-01-01', '2015-07-30')
	```
	结果保存到report.html
	"""
	table = Table("report")
	for account in name_list:
		print("####### {} ########".format(account))
		try:
			values = analyze_account_brand_values(account, start_date, end_date, freq)
			for value in values:
				table.put(value[0], value[1], value[2])
		except Exception as e:
			print('Exception: %s' % str(e).strip())

	table.to_html(report_file)
	print("saved to {}".format(report_file))
	return
