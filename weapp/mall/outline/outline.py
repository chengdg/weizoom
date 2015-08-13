# -*- coding: utf-8 -*-
from datetime import timedelta

from django.http import HttpResponseRedirect
from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from modules.member import models as member_models
from core import resource, dateutil
from core.exceptionutil import unicode_full_stack
from core.charts_apis import create_line_chart_response
from core.jsonresponse import create_response
from core.exceptionutil import unicode_full_stack
from mall import export, notices_models
from mall import models as mall_models
from .utils import get_to_be_shipped_order_infos
from webapp import models as webapp_models
from webapp import statistics_util as webapp_statistics_util


class Outline(resource.Resource):
    app = 'mall2'
    resource = 'outline'

    @login_required
    def get(request):
        """
        """

        webapp_id = request.user_profile.webapp_id
        if not settings.IS_UNDER_BDD:
            if request.manager.id != request.user.id:
                # 子账号
                if len(request.user.permission_set) == 0:
                    # 没有权限页面
                    return render_to_response(
                        'mall/editor/outline_no_permission.html',
                        RequestContext(request, {
                            'first_nav_name': export.MALL_HOME_FIRST_NAV,
                            'second_navs': export.get_home_second_navs(request),
                            'second_nav_name': export.MALL_HOME_INTEGRAL_NAV
                            }))
                else:
                    first_url = export.get_first_navs(request.user)[0]['url']
                    if first_url.find('/mall2/outline/') < 0:
                        # 第一个有权限的一面，不是首页
                        return HttpResponseRedirect(first_url)
            integral_strategy = member_models.IntegralStrategySttings.objects.get(
                webapp_id=webapp_id)
            if integral_strategy.use_ceiling == -1:
                # 需要进入积分引导页
                return HttpResponseRedirect('/mall2/integral_strategy/')

        # 获取待支付订单
        to_be_shipped_orders = get_to_be_shipped_order_infos(request)

        # 获得昨日订单数据
        today = '%s 00:00:00' % dateutil.get_today()
        yesterday = '%s 00:00:00' % dateutil.get_yesterday_str('today')
        orders = mall_models.Order.objects.belong_to(webapp_id).filter(
            created_at__range=(yesterday, today))
        statuses = set([
            mall_models.ORDER_STATUS_PAYED_SUCCESSED,
            mall_models.ORDER_STATUS_PAYED_NOT_SHIP,
            mall_models.ORDER_STATUS_PAYED_SHIPED,
            mall_models.ORDER_STATUS_SUCCESSED])
        orders = [order for order in orders if (
            order.type != 'test') and (order.status in statuses)]
        order_money = 0.0
        for order in orders:
            order_money += order.final_price + order.weizoom_card_money

        # 获取会员数
        total_member_count = member_models.Member.objects.filter(
            webapp_id=webapp_id, is_subscribed=True).count()
        members = member_models.Member.objects.filter(
            webapp_id=webapp_id, created_at__range=(yesterday, today))
        members = [member for member in members if member.is_subscribed]

        outline_counts = [{
            "count": len(orders),
            "description": "昨日下单数"
        }, {
            "count": order_money,
            "description": "昨日成交额"
        }, {
            "count": len(members),
            "description": "昨日新增会员"
        }, {
            "count": total_member_count,
            "description": "店铺会员总数"
        }]

        messages = notices_models.Notice.objects.all().order_by('-id')[:5]

        c = RequestContext(request, {
            'first_nav_name': export.MALL_HOME_FIRST_NAV,
            'second_navs': export.get_home_second_navs(request),
            'second_nav_name': export.MALL_HOME_OUTLINE_NAV,
            'order_info': to_be_shipped_orders,
            'outline_counts': outline_counts,
            'system_messages': messages
        })
        return render_to_response('mall/editor/outline.html', c)

    @login_required
    def api_get(request):
        type = request.GET.get('type', None)
        days = request.GET.get('days', 6)
        webapp_id = request.user_profile.webapp_id
        total_days, low_date, cur_date, high_date = dateutil.get_date_range(dateutil.get_today(), days, 0)
        high_date -= timedelta(days=1)
        date_list = [date.strftime("%Y-%m-%d") for date in dateutil.get_date_range_list(low_date, high_date)]


        if type and type == 'purchase_trend':
            try:
                date2count = dict()
                date2price = dict()

                # 11.20从查询mall_purchase_daily_statistics变更为直接统计订单表，解决mall_purchase_daily_statistics遗漏统计订单与统计时间不一样导致的统计结果不同的问题。
                orders = mall_models.Order.objects.belong_to(webapp_id).filter(created_at__range=(low_date, (high_date)+timedelta(days=1)))
                statuses = set([mall_models.ORDER_STATUS_PAYED_SUCCESSED, mall_models.ORDER_STATUS_PAYED_NOT_SHIP, mall_models.ORDER_STATUS_PAYED_SHIPED, mall_models.ORDER_STATUS_SUCCESSED])
                orders = [order for order in orders if (order.type != 'test') and (order.status in statuses)]
                for order in orders:
                    # date = dateutil.normalize_date(order.created_at)
                    date = order.created_at.strftime("%Y-%m-%d")
                    if order.webapp_id != webapp_id:
                        order_price = mall_models.Order.get_order_has_price_number(order) + order.postage
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
                    price_trend_values.append(round(date2price.get(date, 0.0), 2))
                print(len(count_trend_values))
                return create_line_chart_response(
                        '',
                        '',
                        date_list,
                        [{
                            "name": "订单数",
                            "values": count_trend_values
                        }, {
                            "name": "销售额",
                            "values": price_trend_values
                        }]
                    )
            except:
                if settings.DEBUG:
                    raise
                else:
                    response = create_response(500)
                    response.innerErrMsg = unicode_full_stack()
                    return response.get_response()
        elif type and type == 'visit_daily_trend':
            """
            获得每日pv、uv统计
            """

            #对当天的统计结果进行更新
            if settings.IS_UPDATE_PV_UV_REALTIME:
                #先删除当天的pv,uv统计结果，然后重新进行统计
                today = dateutil.get_today()
                webapp_models.PageVisitDailyStatistics.objects.filter(webapp_id=webapp_id, data_date=today).delete()
                webapp_statistics_util.count_visit_daily_pv_uv(webapp_id, today)

            statisticses = webapp_models.PageVisitDailyStatistics.objects.filter(webapp_id=webapp_id, url_type=webapp_models.URL_TYPE_ALL, data_date__range=(low_date, high_date))

            date2pv = dict([(s.data_date.strftime('%Y-%m-%d'), s.pv_count) for s in statisticses])
            date2uv = dict([(s.data_date.strftime('%Y-%m-%d'), s.uv_count) for s in statisticses])

            pv_trend_values = []
            uv_trend_values = []
            for date in date_list:
                pv_trend_values.append(date2pv.get(date, 0))
                uv_trend_values.append(date2uv.get(date, 0))

            return create_line_chart_response(
                '',
                '',
                date_list,
                [{
                    "name": "PV",
                    "values": pv_trend_values
                }, {
                    "name": "UV",
                    "values": uv_trend_values
                }]
            )
