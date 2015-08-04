# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

import time
from core import resource
from core.jsonresponse import create_response, JsonResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from django.conf import settings
from cloud_required import cloud_housekeeper_required
from models import CloudUser
from core.send_phone_msg import send_phone_captcha as api_send_phone_captcha

from stats.manage import brand_value_utils
from stats import util as stats_util
from weixin2.home import outline 
from stats.manage import manage_summary as manage_util

class CloudHome(resource.Resource):
    """
    云管家主页
    """
    app = 'cloud_housekeeper'
    resource = 'home'

    @cloud_housekeeper_required
    def get(request):
        """
        主页
        """
        owner_user = request.cloud_user.owner
        webapp_id = request.cloud_user.get_webapp_id()
        # 当日微品牌价值数据
        (today_value, yesterday_value, increase_sign, increase_percent) = brand_value_utils.get_latest_brand_value(webapp_id)
        # 关注会员
        subscribed_member_count = stats_util.get_subscribed_member_count(webapp_id)
        # 未读消息数
        unread_message_count = outline._get_unread_message_count(owner_user)

        # 总成交额, 总成交订单
        total_transaction_money, total_order_count = get_transaction_count(webapp_id, 'total')

        # 今日成交额, 今日订单
        today_transaction_money, today_order_count = get_transaction_count(webapp_id, 'today')

        c = RequestContext(request, {
            'page_title': '微众云管家',
            # 当日微品牌价值数据
            'brand_value': format(today_value, ','),
            'value_sign': increase_sign,
            'increase_percent': increase_percent, # 相比昨天增长(下降)百分比
            'bv_diff': abs(today_value-yesterday_value), # 品牌价值差值

            'subscribed_member_count': subscribed_member_count,
            'unread_message_count': unread_message_count,
            'total_transaction_money': total_transaction_money,
            'total_order_count': total_order_count,
            'today_transaction_money': today_transaction_money,
            'today_order_count': today_order_count
        })
        return render_to_response('cloud_housekeeper/statistics.html', c)



def get_transaction_count(webapp_id, sign):    
    transaction_count = 0
    transaction_money = 0.00

    if sign == 'total':
        low_date = '2000-01-01'
        high_date = '3000-01-01'

    if sign == 'today':
        low_date = '{} 00:00:00'.format(time.strftime("%Y-%m-%d"))
        high_date = '{} 23:59:59'.format(time.strftime("%Y-%m-%d"))

    transaction_nums = manage_util.get_transaction_orders(webapp_id,low_date,high_date)
    for transaction in transaction_nums:
        tmp_transaction_money = round(transaction.final_price,2) + round(transaction.weizoom_card_money,2)
        transaction_money += tmp_transaction_money
    transaction_count = transaction_nums.count()

    return transaction_money, transaction_count

