# -*- coding: utf-8 -*-
from datetime import timedelta, datetime

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
from mall.promotion import models as promotion_models
from .utils import get_to_be_shipped_order_infos, get_purchase_trend
from webapp import models as webapp_models
from webapp import statistics_util as webapp_statistics_util
from weixin2.home.outline import get_unread_message_count
from django.db.models import Sum
from stats import util as stats_util

class Outline(resource.Resource):
    app = 'mall2'
    resource = 'outline'

    @login_required
    def get(request):
        """
        """

        webapp_id = request.user_profile.webapp_id
        if not settings.IS_UNDER_BDD:
            # duhao 20151019 注释
            # if request.manager.id != request.user.id:
            #     # 子账号
            #     if len(request.user.permission_set) == 0:
            #         # 没有权限页面
            #         return render_to_response(
            #             'mall/editor/outline_no_permission.html',
            #             RequestContext(request, {
            #                 'first_nav_name': export.MALL_HOME_FIRST_NAV,
            #                 'second_navs': export.get_mall_home_second_navs(request),
            #                 'second_nav_name': export.MALL_HOME_INTEGRAL_NAV
            #             }))
            #     else:
            #         first_url = export.get_first_navs(request.user)[0]['url']
            #         if first_url.find('/mall2/outline/') < 0:
            #             # 第一个有权限的一面，不是首页
            #             return HttpResponseRedirect(first_url)
            integral_strategy = member_models.IntegralStrategySttings.objects.get(
                webapp_id=webapp_id)
            if integral_strategy.use_ceiling == -1:
                # 需要进入积分引导页
                return HttpResponseRedirect('/mall2/integral_strategy/')

        # 获得昨日订单数据
        today = '%s 23:59:59' % dateutil.get_yesterday_str('today')
        yesterday = '%s 00:00:00' % dateutil.get_yesterday_str('today')

        order_money,order_count = stats_util.get_transaction_money_order_count(webapp_id,yesterday,today)

        # 获取会员数 update by bert at 20150817
        subscribed_member_count = member_models.Member.objects.filter(
            webapp_id=webapp_id, 
            is_subscribed=True, 
            is_for_test=False
        ).count()
        new_member_count = member_models.Member.objects.filter(
            webapp_id=webapp_id, 
            created_at__range=(yesterday, today), 
            status=member_models.SUBSCRIBED, 
            is_for_test=False
        ).count()

        # messages = notices_models.Notice.objects.all().order_by('-id')[:5]

        c = RequestContext(request, {
            'first_nav_name': export.MALL_HOME_FIRST_NAV,
            'second_navs': export.get_mall_home_second_navs(request),
            'second_nav_name': export.MALL_HOME_OUTLINE_NAV,
            'unread_message_count': get_unread_message_count(request.manager),
            'new_member_count': new_member_count,
            'order_count': order_count, 
            'order_money': order_money,
            'subscribed_member_count': subscribed_member_count,
            'shop_hint_data': _get_shop_hint_data(request),
            'tomorrow': dateutil.get_tomorrow_str('today')
        })
        return render_to_response('mall/editor/outline.html', c)

    @login_required
    def api_get(request):
        type = request.GET.get('type', None)
        days = request.GET.get('days', 6)
        webapp_id = request.user_profile.webapp_id
        total_days, low_date, cur_date, high_date = dateutil.get_date_range(dateutil.get_today(), days, 0)

        if type and type == 'purchase_trend':
            try:
                result = get_purchase_trend(webapp_id, low_date, high_date)
                response = create_response(200)
                response.data = result
                return response.get_response()
            except:
                if settings.DEBUG:
                    raise
                else:
                    response = create_response(500)
                    response.innerErrMsg = unicode_full_stack()
                    return response.get_response()

        #duhao 20151026 早就不需要pv uv的统计了
        # elif type and type == 'visit_daily_trend':
        #     """
        #     获得每日pv、uv统计
        #     """

        #     # 对当天的统计结果进行更新
        #     if settings.IS_UPDATE_PV_UV_REALTIME:
        #         # 先删除当天的pv,uv统计结果，然后重新进行统计
        #         today = dateutil.get_today()
        #         webapp_models.PageVisitDailyStatistics.objects.filter(webapp_id=webapp_id, data_date=today).delete()
        #         webapp_statistics_util.count_visit_daily_pv_uv(webapp_id, today)

        #     statisticses = webapp_models.PageVisitDailyStatistics.objects.filter(webapp_id=webapp_id,
        #                                                                          url_type=webapp_models.URL_TYPE_ALL,
        #                                                                          data_date__range=(low_date, high_date))

        #     date2pv = dict([(s.data_date.strftime('%Y-%m-%d'), s.pv_count) for s in statisticses])
        #     date2uv = dict([(s.data_date.strftime('%Y-%m-%d'), s.uv_count) for s in statisticses])

        #     pv_trend_values = []
        #     uv_trend_values = []
        #     for date in date_list:
        #         pv_trend_values.append(date2pv.get(date, 0))
        #         uv_trend_values.append(date2uv.get(date, 0))

        #     return create_line_chart_response(
        #         '',
        #         '',
        #         date_list,
        #         [{
        #             "name": "PV",
        #             "values": pv_trend_values
        #         }, {
        #             "name": "UV",
        #             "values": uv_trend_values
        #         }]
        #     )

def _get_shop_hint_data(request):
    """
    获取首页店铺提醒数据
    """
    onshelf_products = mall_models.Product.objects.filter(
        owner=request.manager,
        shelve_type=mall_models.PRODUCT_SHELVE_TYPE_ON,
        is_deleted=False)
    #在售商品数
    onshelf_product_count = len(onshelf_products)
    sellout_products = []
    mall_models.Product.fill_details(request.manager, onshelf_products, {
        "with_product_model": True
    })
    for product in onshelf_products:
        for model in product.models:
            if model and model['stock_type'] == mall_models.PRODUCT_STOCK_TYPE_LIMIT and model['stocks'] <= 0:
                sellout_products.append(product)
                break
    #库存不足商品数
    sellout_product_count = len(sellout_products)

    #待发货订单数
    to_be_shipped_order_count = mall_models.Order.objects.belong_to(request.user_profile.webapp_id).filter(
        status=mall_models.ORDER_STATUS_PAYED_NOT_SHIP
    ).count()
    #退款中订单数
    refunding_order_count = mall_models.Order.objects.belong_to(request.user_profile.webapp_id).filter(
        status__in=[mall_models.ORDER_STATUS_REFUNDING, mall_models.ORDER_STATUS_GROUP_REFUNDING]
    ).count()

    #即将到期的限时抢购活动数
    flash_sale_count = _get_expiring_promotion_count(request, promotion_models.PROMOTION_TYPE_FLASH_SALE)
    #即将到期的买赠活动数
    premium_sale_count = _get_expiring_promotion_count(request, promotion_models.PROMOTION_TYPE_PREMIUM_SALE)
    #即将到期的积分应用活动数
    integral_sale_count = _get_expiring_promotion_count(request, promotion_models.PROMOTION_TYPE_INTEGRAL_SALE)
    #即将到期的优惠券活动数
    coupon_count = _get_expiring_promotion_count(request, promotion_models.PROMOTION_TYPE_COUPON)
    #即将到期的分享红包活动数
    red_envelopes = promotion_models.RedEnvelopeRule.objects.filter(
        owner=request.manager, 
        status=True, 
        limit_time=False,
        is_delete=False, 
        end_time__lte=dateutil.get_tomorrow_str('today')
    )
    red_envelope_ids = []
    for red in red_envelopes:
        is_timeout = False if red.end_time > datetime.now() else True
        if not is_timeout:
            red_envelope_ids.append(red.id)

    return {
        'onshelf_product_count': onshelf_product_count,
        'sellout_product_count': sellout_product_count,
        'to_be_shipped_order_count': to_be_shipped_order_count,
        'refunding_order_count': refunding_order_count,
        'flash_sale_count': flash_sale_count,
        'premium_sale_count': premium_sale_count,
        'integral_sale_count': integral_sale_count,
        'coupon_count': coupon_count,
        'red_envelope_count': len(red_envelope_ids)
    }


def _get_expiring_promotion_count(request, promotion_type):
    """
    即将到期的促销活动数
    """
    return promotion_models.Promotion.objects.filter(
        owner=request.manager,
        status=promotion_models.PROMOTION_STATUS_STARTED,
        type=promotion_type,
        end_date__lte=dateutil.get_tomorrow_str('today')
    ).count()