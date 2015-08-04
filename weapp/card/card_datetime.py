#! -*- coding:UTF-8 -*-
from datetime import datetime, timedelta
import time

#解析日期函数
date_fmt = '%Y-%m-%d %H:%M:%S'

def get_today_time():
    return time.strftime(date_fmt)


def get_previous_date_range_list(from_date,days):
    if from_date=='today':
        today_date = time.strftime(date_fmt)
        from_date = datetime.strptime(today_date, date_fmt)
        date = from_date - timedelta(int(days))
        return [date.strftime(date_fmt),today_date]


def get_datetime_from_date_interval(date_str):
    if date_str:
        date_interval=date_str.split('|')
        if " " in date_interval[0]:
            date_interval[0] = date_interval[0] +':00'
        else:
            date_interval[0] = date_interval[0] +' 00:00:00'
        if " " in date_interval[1]:
            date_interval[1] = date_interval[1] +':00'
        else:
            date_interval[1] = date_interval[1] +' 23:59:59'
        return date_interval

