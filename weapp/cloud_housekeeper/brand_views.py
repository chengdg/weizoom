# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

import json
import datetime

from core import resource
from core.jsonresponse import create_response, JsonResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse

from django.conf import settings
from cloud_required import cloud_housekeeper_required
import models
from stats.manage import manage_summary as manage_util
import stats.util as stats_util
import pandas as pd
from core.charts_apis import MyEcharts

from stats.manage.brand_value_utils import get_brand_value
from core.charts_apis import create_line_chart_response
from mall.models import *
from core import dateutil


def get_mobile_chart_response(date_list, name_2_values_list):    
    myecharts =  MyEcharts()
    map_charts_jsondata = myecharts.create_line_chart_option(            
        "", 
        "", 
        date_list, 
        name_2_values_list,
        None
    )
    map_charts_jsondata['toolbox'] = {'show': False}
    map_charts_jsondata['legend']['show'] = False

    response = create_response(200)
    response.data = map_charts_jsondata
    return response.get_response()


class CloudBrandValues(resource.Resource):
    """
    云管家微品牌价值
    """
    app = 'cloud_housekeeper'
    resource = 'brand_values'

    @cloud_housekeeper_required
    def api_get(request):
        """
        返回微品牌价值的EChart数据
        """        
        webapp_id = request.cloud_user.get_webapp_id()
        periods = 7
        freq = 'W'
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', datetime.now())
        # start_date = '2015-08-09'
        if start_date is not None:
            date_range = pd.date_range(start=start_date, end=end_date, freq=freq)
        else:
            # 如果不指定start_date，则以end_date为基准倒推DISPLAY_PERIODS_IN_CHARTS 个日期(点)
            date_range = pd.date_range(end=end_date, periods=periods, freq=freq)
        date_list = []
        values = []
        for date in date_range:
            date_time = date.to_datetime()
            date_str = date_time.strftime('%Y-%m-%d')  # 将pd.Timestamp转成datetime
            date_list.append(date_time.strftime('%m/%d'))
            values.append(get_brand_value(webapp_id, date_str))

        print("date_list: {}".format(date_list))


        name_2_values_list = [{
            "name": "品牌价值",
            "values" : values
        }]
        response = get_mobile_chart_response(date_list, name_2_values_list)
        return response



class CloudSaleroomValues(resource.Resource):
    """
    云管家销售额
    """
    app = 'cloud_housekeeper'
    resource = 'saleroom_values'

    @cloud_housekeeper_required
    def api_get(request):
        """
        返回销售额的EChart数据
        """        
        low_date, high_date, date_range = stats_util.get_date_range(request)
        webapp_id = request.cloud_user.get_webapp_id()
        date_list = [date.strftime("%m/%d") for date in dateutil.get_date_range_list(low_date, high_date)]

        price_trend_values = get_count_list_by_type(webapp_id, date_list, low_date, high_date, sign="price")

        name_2_values_list = [{
            "name": "销售额",
            "values" : price_trend_values
        }]
        response = get_mobile_chart_response(date_list, name_2_values_list)
        return response



class CloudSaleroomValues(resource.Resource):
    """
    云管家成交订单
    """
    app = 'cloud_housekeeper'
    resource = 'ordernum_values'

    @cloud_housekeeper_required
    def api_get(request):
        """
        返回成交订单的EChart数据
        """        
        low_date, high_date, date_range = stats_util.get_date_range(request)
        webapp_id = request.cloud_user.get_webapp_id()
        date_list = [date.strftime("%m/%d") for date in dateutil.get_date_range_list(low_date, high_date)]

        count_trend_values = get_count_list_by_type(webapp_id, date_list, low_date, high_date, sign="count")

        name_2_values_list = [{
            "name": "订单数",
            "values" : count_trend_values
        }]
        response = get_mobile_chart_response(date_list, name_2_values_list)
        return response


def get_count_list_by_type(webapp_id, date_list, low_date, high_date, sign='price'):
    date2count = dict()
    date2price = dict()


    end_date = datetime.now()
    date_range = pd.date_range(end=end_date, periods=10, freq='W')

    # 11.20从查询mall_purchase_daily_statistics变更为直接统计订单表，解决mall_purchase_daily_statistics遗漏统计订单与统计时间不一样导致的统计结果不同的问题。
    orders = Order.objects.belong_to(webapp_id).filter(created_at__range=(low_date, (high_date+timedelta(days=1))))
    statuses = set([ORDER_STATUS_PAYED_SUCCESSED, ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED])
    orders = [order for order in orders if (order.type != 'test') and (order.status in statuses)]
    for order in orders:
        date = order.created_at.strftime("%m/%d")
        if order.webapp_id != webapp_id:
            order_price =  Order.get_order_has_price_number(order) + order.postage
        else:
            order_price = order.final_price + order.weizoom_card_money

        if date in date2count:
            old_count = date2count[date]
            date2count[date] = old_count + 1
        else:
            date2count[date] = 1

        if date in date2price:
            old_price = date2price[date]
            date2price[date] = old_price + order_price
        else:
            date2price[date] = order_price

    count_trend_values = []
    price_trend_values = []
    for date in date_list:
        count_trend_values.append(date2count.get(date, 0))
        price_trend_values.append("%.2f" % (date2price.get(date, 0.0)))

    if sign == 'price':
        return price_trend_values
    else:
        return count_trend_values


