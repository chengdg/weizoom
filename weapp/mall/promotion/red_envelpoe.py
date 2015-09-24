# -*- coding: utf-8 -*-

import json
from datetime import datetime

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from core import resource
from . import models as promotion_models
from mall import export
from core.jsonresponse import create_response
from core import paginator
from core import search_util

from string_util import byte_to_hex
from modules.member import models as member_models

COUNT_PER_PAGE = 20
PROMOTION_TYPE_COUPON = 4
# FIRST_NAV_NAME = export.MALL_PROMOTION_FIRST_NAV

FIRST_NAV_NAME = 'apps'

class RedEnvelopeRuleList(resource.Resource):
    app = "apps/promotion"
    resource = "red_envelope_rule_list"

    @login_required
    def get(request):
        """
        红包规则列表页面
        """
        is_create = int(request.GET.get('is_create', 0))
        rules = promotion_models.RedEnvelopeRule.objects.filter(owner=request.manager).order_by('-id')
        coupon_rule_ids = [rule.coupon_rule_id for rule in rules]
        coupon_rules = promotion_models.CouponRule.objects.filter(id__in=coupon_rule_ids)
        coupon_rule_info = []
        for coupon_rule in coupon_rules:
            info = {
                "id": coupon_rule.id,
                "name": coupon_rule.name
            }
            coupon_rule_info.append(info)

        items = []
        if not is_create:
            rules = promotion_models.RedEnvelopeRule.objects.filter(owner=request.manager, is_delete=False).order_by('-id')
            coupon_rule_ids = []
            rule_ids = []

            for rule in rules:
                rule_ids.append(rule.id)
                coupon_rule_ids.append(rule.coupon_rule_id)

            id2coupon_rule = dict([(coupon_rule.id, coupon_rule) for coupon_rule in
                                   promotion_models.CouponRule.objects.filter(id__in=coupon_rule_ids)])
            records = promotion_models.GetRedEnvelopeRecord.objects.filter(owner=request.manager)
            rule_id2count = {}
            for record in records:
                if rule_id2count.has_key(record.red_envelope_rule_id):
                    rule_id2count[record.red_envelope_rule_id] += 1
                else:
                    rule_id2count[record.red_envelope_rule_id] = 1
            flag = True
            for rule in rules:
                if flag:
                    if id2coupon_rule[rule.coupon_rule_id].remained_count<=20:
                        flag = False
                        is_warring = True
                    else:
                        is_warring = False
                else:
                    is_warring = False

                data = {
                    "id": rule.id,
                    "rule_name": rule.name,
                    "limit_time": rule.limit_time,
                    "start_time": rule.start_time.strftime("%Y/%m/%d %H:%M:%S"),
                    "end_time": rule.end_time.strftime("%Y/%m/%d %H:%M:%S"),
                    "coupon_rule_name": id2coupon_rule[rule.coupon_rule_id].name,
                    "status": rule.status,
                    "get_count": rule_id2count[rule.id] if rule_id2count.has_key(rule.id) else 0,
                    "remained_count": id2coupon_rule[rule.coupon_rule_id].remained_count,
                    "is_timeout": False if rule.end_time > datetime.now() else True,
                    "receive_method": rule.receive_method,
                    "is_warring": is_warring
                }
                items.append(data)

        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV_NAME,
            'second_navs': export.get_customerized_apps(request),
            'second_nav_name': 'orderRedEnvelope',
            "coupon_rule_info": json.dumps(coupon_rule_info),
            "items": items,
            "is_create": is_create
        })
        return render_to_response('mall/editor/red_envelope_rules.html', c)


    @login_required
    def api_get(request):
        """
        获取红包规则列表advanced table
        """
        name = request.GET.get('name', '')
        coupon_rule_id = int(request.GET.get('couponRule', 0))
        start_date = request.GET.get('startDate', '')
        end_date = request.GET.get('endDate', '')

        is_fetch_all_rules = (not name) and (not coupon_rule_id) and (not start_date) and (not end_date)
        rules = promotion_models.RedEnvelopeRule.objects.filter(owner=request.manager, is_delete=False).order_by('-id')

        if coupon_rule_id:
            rules = rules.filter(coupon_rule_id=coupon_rule_id)

        if not is_fetch_all_rules:
            rules = _filter_rules(request, rules)

        count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
        cur_page = int(request.GET.get('page', '1'))
        pageinfo, rules = paginator.paginate(rules, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

        items = []
        coupon_rule_ids = []
        rule_ids = []

        for rule in rules:
            rule_ids.append(rule.id)
            coupon_rule_ids.append(rule.coupon_rule_id)

        id2coupon_rule = dict([(coupon_rule.id, coupon_rule) for coupon_rule in
                               promotion_models.CouponRule.objects.filter(id__in=coupon_rule_ids)])
        records = promotion_models.GetRedEnvelopeRecord.objects.filter(owner=request.manager)
        rule_id2count = {}
        for record in records:
            if rule_id2count.has_key(record.red_envelope_rule_id):
                rule_id2count[record.red_envelope_rule_id] += 1
            else:
                rule_id2count[record.red_envelope_rule_id] = 1
        for rule in rules:

            data = {
                "id": rule.id,
                "rule_name": rule.name,
                "limit_time": rule.limit_time,
                "start_time": rule.start_time.strftime("%Y/%m/%d %H:%M:%S"),
                "end_time": rule.end_time.strftime("%Y/%m/%d %H:%M:%S"),
                "coupon_rule_name": id2coupon_rule[rule.coupon_rule_id].name,
                "status": rule.status,
                "get_count": rule_id2count[rule.id] if rule_id2count.has_key(rule.id) else 0,
                "remained_count": id2coupon_rule[rule.coupon_rule_id].remained_count,
                "is_timeout": False if rule.end_time > datetime.now() else True,
                "receive_method": rule.receive_method,
            }
            items.append(data)
        data = {
            "items": items,
            'pageinfo': paginator.to_dict(pageinfo),
            'sortAttr': 'id',
            'data': {}
        }

        response = create_response(200)
        response.data = data
        return response.get_response()


class RedEnvelopeRule(resource.Resource):
    app = "apps/promotion"
    resource = "red_envelope_rule"

    @login_required
    def get(request):
        """
        红包规则创建、查看页面
        """

        rule_id = request.GET.get('id', None)
        if rule_id:
            red_envelope_rule = promotion_models.RedEnvelopeRule.objects.get(id=rule_id)
            coupon_rule = promotion_models.CouponRule.objects.get(id=red_envelope_rule.coupon_rule_id)
            c = RequestContext(request, {
                'first_nav_name': FIRST_NAV_NAME,
                'second_navs': export.get_customerized_apps(request),
                'second_nav_name': 'orderRedEnvelope',
                'coupon_rule': coupon_rule,
                'red_envelope_rule': red_envelope_rule,
            })
            return render_to_response('mall/editor/create_red_envelope_rule.html', c)
        else:
            coupon_rules = promotion_models.CouponRule.objects.filter(owner=request.manager, is_active=True,
                                                                      end_date__gt=datetime.now(), limit_counts=-1)
            c = RequestContext(request, {
                'first_nav_name': FIRST_NAV_NAME,
                'second_navs': export.get_customerized_apps(request),
                'second_nav_name': 'orderRedEnvelope',
                'coupon_rules': coupon_rules
            })
            return render_to_response('mall/editor/create_red_envelope_rule.html', c)

    @login_required
    def api_post(request):
        """
        开启、关闭、删除红包规则
        """
        id = request.POST.get('id', 0)
        status = request.POST.get('status', None)
        # try:
        if status == 'over':
            promotion_models.RedEnvelopeRule.objects.filter(id=id).update(status=False)
        elif status == 'start':
            #除去图文领取的
            start_rule = promotion_models.RedEnvelopeRule.objects.filter(owner=request.manager, status=True, receive_method=False)
            if start_rule.count() > 0:
                response = create_response(500)
                response.errMsg = "请先关闭其他分享红包活动！"
                return response.get_response()
            promotion_models.RedEnvelopeRule.objects.filter(id=id).update(status=True)
        elif status == 'delete':
            promotion_models.RedEnvelopeRule.objects.filter(id=id).update(status=False, is_delete=True)
        # except:
        #     return create_response(500).get_response()
        return create_response(200).get_response()

    @login_required
    def api_put(request):
        limit_money = request.POST.get('limit_money', 0)
        status = False
        if not limit_money:
            limit_money = 0.0
        if request.POST.get('receive-method-order'):
            receive_method = False #下单领取
        else:
            receive_method = True
            status = True #图文领取-状态默认开启
        if request.POST.get('start_date', None) and request.POST.get('end_date', None):
            promotion_models.RedEnvelopeRule.objects.create(
                owner=request.user,
                name=request.POST.get('name', ''),
                coupon_rule_id=request.POST.get('coupon_rule', 0),
                start_time=request.POST.get('start_date'),
                end_time=request.POST.get('end_date'),
                receive_method = receive_method,
                status = status,
                limit_order_money=limit_money,
                use_info=request.POST.get('detail', ''),
                share_pic=request.POST.get('share_pic', ''),
                share_title=request.POST.get('remark', '')
            )
        else:
            promotion_models.RedEnvelopeRule.objects.create(
                owner=request.user,
                name=request.POST.get('name', ''),
                coupon_rule_id=request.POST.get('coupon_rule', 0),
                limit_time=True,
                receive_method = receive_method,
                status = status,
                limit_order_money=limit_money,
                use_info=request.POST.get('detail', ''),
                share_pic=request.POST.get('share_pic', ''),
                share_title=request.POST.get('remark', '')
            )
        return create_response(200).get_response()


class RedEnvelopeParticipances(resource.Resource):
    app = "apps/promotion"
    resource = "red_envelope_participances"

    @login_required
    def get(request):
        """
        红包分析页面
        """
        rule_id = request.GET.get('id', None)
        has_data = promotion_models.GetRedEnvelopeRecord.objects.filter(red_envelope_rule_id=rule_id).count()
        rule_data = promotion_models.RedEnvelopeRule.objects.get(id=rule_id)
        #TODO 传递正确的数字
        new_member_count = 152
        received_count = 3000
        consumption_sum = 13000.00
        total_use_count = 300
        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV_NAME,
            'second_navs': export.get_customerized_apps(request),
            'second_nav_name': 'orderRedEnvelope',
            'has_data': has_data,
            'new_member_count': new_member_count,
            'received_count': received_count,
            'consumption_sum': consumption_sum,
            'total_use_count': total_use_count,
            'red_envelope_id': rule_id,
            'red_envelope_name': rule_data.name,
            'red_envelope_start_time': rule_data.start_time.strftime("%Y-%m-%d"),
            'red_envelope_end_time': rule_data.end_time.strftime("%Y-%m-%d"),
            'receive_method': rule_data.receive_method
        })
        return render_to_response('mall/editor/red_envelope_participences.html', c)

    @staticmethod
    def get_datas(request):
        name = request.GET.get('participant_name', '')
        webapp_id = request.user_profile.webapp_id
        if name:
            hexstr = byte_to_hex(name)
            members = member_models.Member.objects.filter(webapp_id=webapp_id,username_hexstr__contains=hexstr)

            if name.find(u'非')>=0:
                sub_members = member_models.Member.objects.filter(webapp_id=webapp_id,is_subscribed=False)
                members = members|sub_members
        else:
            members = member_models.Member.objects.filter(webapp_id=webapp_id)
        member_ids = [member.id for member in members]
        # webapp_user_ids = [webapp_user.id for webapp_user in member_models.WebAppUser.objects.filter(member_id__in=member_ids)]
        member_status = request.GET.get('member_status', '')
        red_envelope_status = request.GET.get('red_envelope_status', '')
        params = {'red_envelope_rule_id':request.GET['id']}
        if member_ids:
            params['member__in'] = member_ids
        # if member_status:
        #     params['created_at__gte'] = member_status
        # if red_envelope_status:
        #     params['created_at__lte'] = red_envelope_status
        datas = promotion_models.GetRedEnvelopeRecord.objects.filter(**params).order_by('-id')

        #进行分页
        count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
        cur_page = int(request.GET.get('page', '1'))
        pageinfo, datas = paginator.paginate(datas, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

        return pageinfo, datas

    @login_required
    def api_get(request):
        """
        获取advanced table
        """
        pageinfo, datas = RedEnvelopeParticipances.get_datas(request)
        member2datas = {}
        member_ids = set()
        for data in datas:
            print data
            member2datas.setdefault(data.member_id, []).append(data)
            member_ids.add(data.member_id)
            data.participant_name = u'未知'
            data.participant_icon = '/static/img/user-1.jpg'

        if len(member_ids) > 0:
            for member in member_ids:
                for data in member2datas.get(member, ()):
                    member2data = member_models.Member.objects.get(id=member)
                    if member2data.is_subscribed:
                        data.participant_name = member2data.username_for_html
                        data.participant_icon = member2data.user_icon
                    else:
                        data.participant_name = u'非会员'
                        data.participant_icon = '/static/img/user-1.jpg'

        items = []
        for data in datas:
            red_envelope_participance = promotion_models.GetRedEnvelopeRecord.objects.get(id=data.id)
            items.append({
				'id': str(data.id),
				'participant_name': data.participant_name,
				'participant_icon': data.participant_icon,
				'created_at': data.created_at.strftime("%Y-%m-%d %H:%M:%S"),
			})
        response_data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': 'id',
			'data': {}
		}
        response = create_response(200)
        response.data = response_data
        return response.get_response()

#########################

RULE_FILTERS = {
    'rule': [
        {
            'comparator': lambda rule, filter_value: filter_value in rule.name,
            'query_string_field': 'name'
        }, {
            'comparator': lambda rule, filter_value: int(filter_value) == rule.coupon_rule_id,
            'query_string_field': 'coupon_rule_id'
        }, {
            'comparator': lambda rule, filter_value: filter_value <= rule.start_time.strftime("%Y-%m-%d %H:%M"),
            'query_string_field': 'startDate'
        }, {
            'comparator': lambda rule, filter_value: filter_value >= rule.end_time.strftime("%Y-%m-%d %H:%M"),
            'query_string_field': 'endDate'
        }
    ]
}


def _filter_rules(request, rules):
    has_filter = search_util.init_filters(request, RULE_FILTERS)
    if not has_filter:
        # 没有filter，直接返回
        return rules

    rules = search_util.filter_objects(rules, RULE_FILTERS['rule'])

    return rules
