# -*- coding: utf-8 -*-

import json
from datetime import datetime
#from datetime import datetime
#from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
#from django.db.models import F

from stats import export
from core import resource
from core import paginator
from core.jsonresponse import create_response
#from weixin.mp_decorators import mp_required
#from market_tools.tools.channel_qrcode.models import ChannelQrcodeSettings, ChannelQrcodeHasMember
#from market_tools.tools.lottery.models import Lottery, LotteryRecord
#import utils.dateutil as dateutil
#from market_tools.tools.lottery.models import STATUS2TEXT as LOTTERY_STATUS2TEXT
import stats.util as stats_util
from modules.member.models import Member
from mall.models import Order, ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED, ORDER_SOURCE_OWN


FIRST_NAV = export.MANAGEMENT_NAV
DEFAULT_COUNT_PER_PAGE = 20


class ManageSummary(resource.Resource):
    """
    经营概况
    """
    app = 'stats'
    resource = 'manage_summary'

    #@mp_required
    @login_required
    def get(request):
        """
        显示经营概况的页面
        """
        #默认显示今天的日期
        today = datetime.strftime(datetime.now(), '%Y-%m-%d')

        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_management_second_navs(request),
            'second_nav_name': export.MANAGEMENT_SUMMARY_NAV,
            'start_date': today,
            'end_date': today,
        })
        return render_to_response('manage/manage_summary.html', c)


    @login_required
    def api_get(request):
        """
        经营概况分析API  获取店铺经营概况各项统计数据

        """
        low_date, high_date, date_range = stats_util.get_date_range(request)
        webapp_id = request.user_profile.webapp_id


        #商品复购率


        #商品推荐指数
        

        #成交金额
        transaction_money = 0.00
        transaction_nums = get_transaction_orders(webapp_id,low_date,high_date)
        for transaction in transaction_nums:
            tmp_transaction_money = round(transaction.final_price,2) + round(transaction.weizoom_card_money,2)
            transaction_money += tmp_transaction_money

        #成交订单
        transaction_orders = (get_transaction_orders(webapp_id,low_date,high_date)).count()

        #购买总人数
        buyer_count = stats_util.get_buyer_count(webapp_id,low_date,high_date)

        #客单价
        if transaction_orders >0:
            vis_price = transaction_money / transaction_orders
        else:
            vis_price = 0 

        #发起扫码会员和扫码新增会员
        ori_qrcode_member_count, member_from_qrcode_count = stats_util.get_ori_qrcode_member_count(webapp_id, low_date, high_date)

        #发起分享链接会员
        share_url_member_count = stats_util.get_share_url_member_count(webapp_id, low_date, high_date)

        #分享链接新增会员
        member_from_share_url_count = stats_util.get_member_from_share_url_count(webapp_id, low_date, high_date)

        #会员复购率
        bought_member_count = stats_util.get_bought_member_count(webapp_id, low_date, high_date)
        repeat_buying_member_count = stats_util.get_repeat_buying_member_count(webapp_id, low_date, high_date)
        repeat_buying_member_rate = '0.00%'
        if bought_member_count > 0:
            repeat_buying_member_rate = "%.2f%%" % (repeat_buying_member_count * 100.0 / bought_member_count)

        #会员推荐率
        member_recommend_rate = '0.00%'
        total_member_count = stats_util.get_total_member_count(webapp_id,high_date)
        if total_member_count > 0:
            member_recommend_rate = "%.2f%%" % ((share_url_member_count + ori_qrcode_member_count)*100.0 / total_member_count)
        result = {
            'repeat_buying_member_rate': repeat_buying_member_rate,
            'member_recommend_rate': member_recommend_rate,
            'transaction_orders': transaction_orders,
            'ori_qrcode_member_count': ori_qrcode_member_count,
            'member_from_qrcode_count': member_from_qrcode_count,
            'share_url_member_count': share_url_member_count,
            'member_from_share_url_count': member_from_share_url_count,
            'transaction_money': "%.2f" % transaction_money,
            'vis_price': "%.2f" % vis_price,
            'buyer_count': buyer_count
        }

        response = create_response(200)
        response.data = {
            'items':result,
            'sortAttr': ''
        }

        return response.get_response()


#获取成交订单
def get_transaction_orders(webapp_id,low_date,high_date):
    transaction_orders = Order.objects.filter(
        webapp_id=webapp_id,
        order_source=ORDER_SOURCE_OWN,
        created_at__range=(low_date,high_date),
        status__in=(ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED)
        )
    return transaction_orders

#获取来源为“本店”的总订单量
def get_total_buyer(webapp_id,low_date,high_date):
    orders = Order.objects.filter(
                webapp_id=webapp_id, 
                order_source=ORDER_SOURCE_OWN, 
                created_at__range=(low_date, high_date), 
                status__in=(ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED)
            )
    order_dict = {}
    webapp_user_ids = set([order.webapp_user_id for order in orders])
    webappuser2member = Member.members_from_webapp_user_ids(webapp_user_ids)
    member_count = 0
    for order in orders:
        tmp_member = webappuser2member.get(order.webapp_user_id, None)
        if tmp_member:
            if not order_dict.has_key(tmp_member.id):
                member_count += 1
                order_dict[tmp_member.id] = ""
        else:
            member_count += 1

    return member_count