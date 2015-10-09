# -*- coding: utf-8 -*-
import os

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from excel_response import ExcelResponse
from django.contrib.auth.decorators import login_required

from core import resource
from mall import export
from mall.models import *
from modules.member.models import WebAppUser
from modules.member.module_api import get_member_by_id_list
from core import paginator
from models import *
from core.jsonresponse import create_response, JsonResponse
from core import search_util
from mall.promotion.utils import create_coupons

COUNT_PER_PAGE = 20
PROMOTION_TYPE_COUPON = 4
FIRST_NAV_NAME = export.MALL_PROMOTION_AND_APPS_FIRST_NAV


class CouponList(resource.Resource):
    app = "mall2"
    resource = "coupon_list"

    @login_required
    def get(request):
        """
        优惠券列表
        """
        rule_id = request.GET.get('rule_id')
        if rule_id:
            # 导出
            rule_id = request.GET.get('rule_id')
            coupons = [
                [u'优惠码', u'金额', u'创建时间', u'领取时间', u'领取人', u'使用时间', u'使用人', u'订单号', u'状态']
            ]

            coupon_list = Coupon.objects.filter(owner=request.manager, coupon_rule_id=rule_id)

            member_ids = [c.member_id for c in coupon_list]
            members = get_member_by_id_list(member_ids)
            member_id2member = dict([(m.id, m) for m in members])

            # 获取被使用的优惠券使用者信息
            coupon_ids = [c.id for c in coupon_list if c.status == COUPON_STATUS_USED]
            orders = Order.get_orders_by_coupon_ids(coupon_ids)
            user_ids = []
            if orders:
                coupon_id2webapp_user_id = dict([(o.coupon_id, \
                                                  {'id': o.id, 'user': o.webapp_user_id, 'order_id': o.order_id,
                                                   'created_at': o.created_at}) \
                                                 for o in orders])
                user_ids.append(o.webapp_user_id)
            else:
                coupon_id2webapp_user_id = {}

            #获取使用优惠券会员的信息
            webapp_user_id2member_id = dict(
                [(user.id, user.member_id ) for user in WebAppUser.objects.filter(id__in=user_ids) if
                 (user.member_id != 0 and user.member_id != -1)])
            member_ids = webapp_user_id2member_id.values()
            members = get_member_by_id_list(member_ids)
            for member in members:
                if not member_id2member.has_key(member.id):
                    member_id2member[member.id] = member

            now = datetime.today()
            for coupon in coupon_list:
                coupon.consumer_name = ''
                coupon.use_time = ''
                coupon.order_fullid = ''

                member_id = int(coupon.member_id)
                if member_id in member_id2member:
                    member = member_id2member[member_id]
                    coupon.member_name = member.username_for_html
                else:
                    coupon.member_name = ''

                if coupon.status == COUPON_STATUS_USED:
                    if coupon.id in coupon_id2webapp_user_id:
                        order = coupon_id2webapp_user_id[coupon.id]
                        coupon.order_id = order['id']
                        coupon.order_fullid = order['order_id']
                        coupon.use_time = order['created_at'].strftime("%Y-%m-%d %H:%M")
                        webapp_user_id = order['user']
                        if webapp_user_id2member_id.has_key(webapp_user_id) and member_id2member.has_key(
                                webapp_user_id2member_id[webapp_user_id]):
                            member = member_id2member[webapp_user_id2member_id[webapp_user_id]]
                        else:
                            member = None
                        if member:
                            coupon.consumer_name = member.username_for_html
                        else:
                            consumer.consumer_name = '未知'
                    else:
                        consumer.consumer_name = '未知'

                    coupon.status = COUPONSTATUS.get(coupon.status)['name']
                elif coupon.expired_time <= now:
                    coupon.status = COUPONSTATUS.get(COUPON_STATUS_EXPIRED)['name']
                else:
                    coupon.status = COUPONSTATUS.get(coupon.status)['name']

                coupons.append([
                    coupon.coupon_id,
                    coupon.money,
                    coupon.created_at,
                    coupon.provided_time if coupon.member_name else '',
                    coupon.member_name,
                    coupon.use_time,
                    coupon.consumer_name,
                    coupon.order_fullid,
                    coupon.status
                ])

            return ExcelResponse(coupons, output_name=u'优惠券详情'.encode('utf8'), force_csv=False)
        else:
            rule_id = request.GET.get('id', '0')
            #是否显示最后一页
            is_max_page = int(request.GET.get('is_max_page', 0))
            if is_max_page:
                page = "true"
            else:
                page = 1
            can_add_coupon = 1
            if rule_id:
                coupon_rule = CouponRule.objects.get(id=rule_id)
                if not coupon_rule.is_active or coupon_rule.end_date < datetime.now():
                    can_add_coupon = 0

            c = RequestContext(request, {
                'first_nav_name': FIRST_NAV_NAME,
                'second_navs': export.get_promotion_and_apps_second_navs(request),
                'second_nav_name': export.MALL_PROMOTION_SECOND_NAV,
                'third_nav_name': export.MALL_PROMOTION_COUPON_NAV,
                'rule_id': rule_id,
                'can_add_coupon': can_add_coupon,
                'is_max_page': is_max_page,
                'page': page
            })
            return render_to_response('mall/editor/promotion/coupons.html', c)

    @login_required
    def api_get(request):
        """
        获取优惠券advanced table
        """
        coupon_code = request.GET.get('couponCode', '')
        use_status = request.GET.get('useStatus', '')
        member_name = request.GET.get('memberName', '')
        #是否显示最后一页
        is_max_page = int(request.GET.get('is_max_page', 0))

        is_fetch_all_coupon = (not coupon_code) and (use_status == 'all') and (not member_name)
        # 处理排序
        sort_attr = request.GET.get('sort_attr', '-id')
        coupon_rule_id = request.GET.get('id')
        if coupon_rule_id:
            coupons = Coupon.objects.filter(owner=request.manager, coupon_rule_id=coupon_rule_id).order_by(sort_attr)

        # 获取coupon所属的rule的name
        id2rule = dict([(rule.id, rule) for rule in CouponRule.objects.filter(owner=request.manager)])

        if is_fetch_all_coupon:
            # 进行分页
            count_per_page = int(request.GET.get('count_per_page', 15))
            cur_page = int(request.GET.get('page', '1'))
            pageinfo, coupons = paginator.paginate(coupons, cur_page, count_per_page,
                                                   query_string=request.META['QUERY_STRING'])
        else:
            coupons_data = _filter_reviews(request, coupons)
            count_per_page = int(request.GET.get('count_per_page', 15))
            cur_page = request.GET.get('page', '1')
            t_max_page = False
            if cur_page == "true":
                t_max_page = True
                cur_page = 1
            pageinfo, coupons = paginator.paginate(coupons_data, cur_page, count_per_page,
                                                   query_string=request.META['QUERY_STRING'])

            ##是否从最后一页开始显示
            if is_max_page:
                max_page = int(pageinfo.max_page)
                if max_page != cur_page and t_max_page:
                    cur_page = max_page
                pageinfo, coupons = paginator.paginate(coupons_data, cur_page, count_per_page,
                                                   query_string=request.META['QUERY_STRING'])



        # 避免便利整个优惠券列表
        member_ids = [c.member_id for c in coupons]
        members = get_member_by_id_list(member_ids)
        member_id2member = dict([(m.id, m) for m in members])

        # 获取被使用的优惠券使用者信息
        coupon_ids = [c.id for c in coupons if c.status == COUPON_STATUS_USED]
        orders = Order.get_orders_by_coupon_ids(coupon_ids)
        if orders:
            coupon_id2webapp_user_id = dict([(o.coupon_id, \
                                              {'id': o.id, 'user': o.webapp_user_id, 'order_id': o.order_id,
                                               'created_at': o.created_at}) \
                                             for o in orders])
        else:
            coupon_id2webapp_user_id = {}

        response = create_response(200)
        response.data.items = []
        #统计是否有active的coupon
        # has_active_coupon = False
        now = datetime.today()
        for coupon in coupons:
            cur_coupon = JsonResponse()
            cur_coupon.id = coupon.id
            cur_coupon.coupon_id = coupon.coupon_id
            cur_coupon.provided_time = coupon.provided_time.strftime("%Y-%m-%d %H:%M")
            cur_coupon.created_at = coupon.created_at.strftime("%Y-%m-%d %H:%M")
            cur_coupon.money = str(coupon.money)
            cur_coupon.is_manual_generated = coupon.is_manual_generated
            cur_member = JsonResponse()
            member_id = int(coupon.member_id)
            # if coupon.status == COUPON_STATUS_UNUSED:
            # has_active_coupon = True
            if member_id in member_id2member:
                member = member_id2member[member_id]
                cur_member.username_for_html = member.username_for_html
            else:
                member = ''
                cur_member.username_for_html = ''
            cur_member.id = member_id

            consumer = JsonResponse()
            consumer.username_for_html = ''
            if coupon.status == COUPON_STATUS_USED:
                if coupon.id in coupon_id2webapp_user_id:
                    order = coupon_id2webapp_user_id[coupon.id]
                    cur_coupon.order_id = order['id']
                    cur_coupon.order_fullid = order['order_id']
                    cur_coupon.use_time = order['created_at'].strftime("%Y-%m-%d %H:%M")
                    webapp_user_id = order['user']
                    member = WebAppUser.get_member_by_webapp_user_id(webapp_user_id)
                    if member:
                        consumer.username_for_html = member.username_for_html
                        consumer.id = member.id
                    else:
                        consumer.username_for_html = '未知'
                else:
                    consumer.username_for_html = '未知'
                cur_coupon.status = COUPONSTATUS.get(coupon.status)['name']
            elif coupon.expired_time <= now:
                cur_coupon.status = COUPONSTATUS.get(COUPON_STATUS_EXPIRED)['name']
            else:
                cur_coupon.status = COUPONSTATUS.get(coupon.status)['name']

            cur_coupon.member = cur_member
            cur_coupon.consumer = consumer
            cur_coupon.rule_name = id2rule[coupon.coupon_rule_id].name
            response.data.items.append(cur_coupon)

        response.data.sortAttr = request.GET.get('sort_attr', '-created_at')
        response.data.pageinfo = paginator.to_dict(pageinfo)
        return response.get_response()

    @login_required
    def api_delete(request):
        """
        删除优惠券
        """
        ids = request.POST.getlist('ids[]')
        Coupon.objects.filter(owner=request.manager, id__in=ids).delete()

        response = create_response(200)
        return response.get_response()


class CouponInfo(resource.Resource):
    app = "mall2"
    resource = "coupon"

    @login_required
    def get(request):
        """
        添加库存页面
        """
        rule_id = request.GET.get('rule_id', '0')
        rules = CouponRule.objects.filter(id=rule_id)

        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV_NAME,
            'second_navs': export.get_promotion_and_apps_second_navs(request),
            'second_nav_name': export.MALL_PROMOTION_SECOND_NAV,
            'third_nav_name': export.MALL_PROMOTION_COUPON_NAV,
            'rule': rules[0]
        })
        return render_to_response('mall/editor/promotion/create_coupon.html', c)

    @login_required
    def api_post(request):
        """
        增加库存
        """
        rule_id = request.POST.get('rule_id', '0')
        rules = CouponRule.objects.filter(id=rule_id)
        if len(rules) != 1:
            return create_response(500, '优惠券不存在')
        if rules[0].is_active == 0 or rules[0].end_date < datetime.now():
            return create_response(500, '优惠券已失效或者已过期')
        count = int(request.POST.get('count', '0'))
        create_coupons(rules[0], count)

        if rules[0].remained_count <= 0:
            rules.update(remained_count=0)    
        rules.update(
            count=(rules[0].count + count),
            remained_count=(rules[0].remained_count + count)
        )
        return create_response(200).get_response()


class CouponQrcode(resource.Resource):
    """
    优惠券二维码
    """

    app = "mall2"
    resource = "coupon_qrcode"

    @login_required
    def get(request):

        """
        下载优惠券二维码
        """
        coupon_id = request.GET["id"]
        dir_path = os.path.join(settings.UPLOAD_DIR, '../coupon_qrcode/')
        filename = dir_path + coupon_id + '.png'
        try:
            response = HttpResponse(open(filename, "rb").read(), mimetype='application/x-msdownload')
            response['Content-Disposition'] = 'attachment; filename="qrcode.png"'
        except:
            response = HttpResponse('')
        return response


# 筛选数据构造
COUPON_FILTERS = {
    'coupon': [
        {
            'comparator': lambda coupon, filter_value: (filter_value == coupon.coupon_id),
            'query_string_field': 'couponCode'
        }, {
            'comparator': lambda coupon, filter_value: (filter_value == 'all') or (filter_value == str(coupon.status)),
            'query_string_field': 'useStatus'
        }
    ],
    'member': [
        {
            'comparator': lambda member, filter_value: (filter_value in member.username_for_html),
            'query_string_field': 'memberName'
        }
    ]
}


def _filter_reviews(request, coupons):
    has_filter = search_util.init_filters(request, COUPON_FILTERS)
    if not has_filter:
        # 没有filter，直接返回
        return coupons

    coupons = search_util.filter_objects(coupons, COUPON_FILTERS['coupon'])

    # 处理领取人
    member_name = request.GET.get('memberName', '')
    filter_coupons = coupons
    if member_name:
        member_ids = [c.member_id for c in coupons]
        members = get_member_by_id_list(member_ids)
        members = search_util.filter_objects(members, COUPON_FILTERS['member'])
        member_ids = [member.id for member in members]
        filter_coupons = []
        for coupon in coupons:
            if coupon.member_id in member_ids:
                filter_coupons.append(coupon)
    return filter_coupons
