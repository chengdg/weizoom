# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

import json
import random, string

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

class CloudReport(resource.Resource):
    """
    云管家登陆
    """
    app = 'cloud_housekeeper'
    resource = 'report'

    @cloud_housekeeper_required
    def get(request):
        """
        记录
        """
        report_id = request.GET.get('id', 0)
        report_type = request.GET.get('type', 'week')
        start_date = request.GET.get('start', '')
        end_date = request.GET.get('end', '')

        owner_user = request.cloud_user.owner
        webapp_id = request.cloud_user.get_webapp_id()


        # 当日微品牌价值数据
        # (today_value, yesterday_value, increase_sign, increase_percent) = brand_value_utils.get_latest_brand_value(webapp_id)

        # 成交额, 成交订单, 客单价
        # transaction_money, transaction_count, vis_price = get_transaction_count(webapp_id, start_date, end_date)

        # #购买总人数
        # buyer_count = stats_util.get_buyer_count(webapp_id, start_date, end_date)

        # #新增会员
        # new_member_count = stats_util.get_new_member_count(webapp_id, start_date, end_date)

        c = RequestContext(request, {
            'page_title': '报告',
            'start_date': start_date,
            'end_date': end_date,
            'report_id': report_id,
            'report_type': report_type
            # 'report': report,
            # 'transaction_money': transaction_money,
            # 'transaction_count': transaction_count,
            # 'vis_price': vis_price,
            # 'buyer_count': buyer_count,
            # 'new_member_count': new_member_count
        })
        return render_to_response('cloud_housekeeper/reportDetails.html', c)


def get_transaction_count(webapp_id, low_date, high_date):
    transaction_count = 0
    transaction_money = 0.00

    low_date = '{} 00:00:00'.format(low_date)
    high_date = '{} 23:59:59'.format(high_date)

    transaction_nums = manage_util.get_transaction_orders(webapp_id, low_date, high_date)
    for transaction in transaction_nums:
        tmp_transaction_money = round(transaction.final_price,2) + round(transaction.weizoom_card_money,2)
        transaction_money += tmp_transaction_money
    transaction_count = transaction_nums.count()

    #客单价
    if transaction_count > 0:
        vis_price = transaction_money / transaction_count
    else:
        vis_price = 0 

    return "%.2f" % transaction_money, transaction_count, "%.2f" % vis_price