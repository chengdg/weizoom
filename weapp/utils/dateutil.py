#coding=utf8

# 时间、日期计算的工具
# 参考自 com.wintim.common.util.DateUtil

import datetime as dt
import time


DATETIME_FORMAT="%Y-%m-%d %H:%M:%S"
DATE_FORMAT="%Y-%m-%d"


# 获得当前的时刻的字符串
def get_current_datetime():
	return dt.datetime.now().strftime(DATETIME_FORMAT)

def now():
	return dt.datetime.now()

# 获得当前日期
def get_current_date():
	return dt.datetime.now().strftime(DATE_FORMAT)

# 将Date转成"yyyy-MM-dd HH:mm:ss"字符串
def datetime2string(at):
	if at == None:
		return None
	if isinstance(at,str):
		return at
	return at.strftime(DATETIME_FORMAT)

# 将Date转成"yyyy-MM-dd"字符串
def date2string(at):
	if at == None:
		return None
	if isinstance(at, str):
		return at
	return at.strftime(DATE_FORMAT)

# 将"yyyy-MM-dd HH:mm:ss"字符串转成datetime
def parse_datetime(str):
	if str == None:
		return None
	return dt.datetime.strptime(str, DATETIME_FORMAT)

def parse_date(str):
	if str == None:
		return None
	return dt.datetime.strptime(str, DATE_FORMAT)

# 得到n天后的时间
def get_date_after_days(date, days):
	return date + dt.timedelta(days=days)

def get_first_day_of_month():
	now = dt.date.today()
	monday = dt.timedelta(0 - now.weekday()) + now
	sunday = dt.timedelta(6 - now.weekday()) + now

	get_first_day_of_month = time.strftime('%Y-%m-01 00:00:00',time.localtime(time.time()))
	return get_first_day_of_month

def get_week_bounds():
	now = dt.date.today()
	monday = dt.timedelta(0 - now.weekday()) + now
	sunday = dt.timedelta(6 - now.weekday()) + now

	return monday.strftime(DATETIME_FORMAT), sunday.strftime(DATETIME_FORMAT)