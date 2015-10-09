# -*- coding: utf-8 -*-

import json
from datetime import datetime
import os

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from core import resource
from . import models as promotion_models
from mall import export
from core.jsonresponse import create_response
from core import paginator
from core import search_util
from mall.models import Order
from mall.promotion.models import Coupon,COUPONSTATUS,COUPON_STATUS_USED
from modules.member.models import MemberTag, MemberGrade

from string_util import byte_to_hex
from modules.member import models as member_models
from weapp import settings

COUNT_PER_PAGE = 20
PROMOTION_TYPE_COUPON = 4

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
            flag = True
            for rule in rules:
                if flag:
                    if rule.limit_time and rule.status:
                        if id2coupon_rule[rule.coupon_rule_id].remained_count<=20:
                            flag = False
                            is_warring = True
                        else:
                            is_warring = False
                    else:
                        is_timeout = False if rule.end_time > datetime.now() else True

                        if id2coupon_rule[rule.coupon_rule_id].remained_count<=20 and not is_timeout  :
                            flag = False
                            is_warring = True
                        else:
                            is_warring = False
                else:
                    is_warring = False
                is_timeout = False if rule.end_time > datetime.now() else True
                data = {
                    "id": rule.id,
                    "rule_name": rule.name,
                    "limit_time": rule.limit_time,
                    "start_time": rule.start_time.strftime("%Y/%m/%d %H:%M:%S"),
                    "end_time": rule.end_time.strftime("%Y/%m/%d %H:%M:%S"),
                    "coupon_rule_name": id2coupon_rule[rule.coupon_rule_id].name,
                    "status": rule.status,
                    "remained_count": id2coupon_rule[rule.coupon_rule_id].remained_count,
                    "is_timeout": is_timeout,
                    "receive_method": rule.receive_method,
                    "is_warring": is_warring,
                }
                items.append(data)
        endDate = request.GET.get('endDate', '')
        if endDate:
            endDate +=' 00:00'
        promotion_status = request.GET.get('status', '-1')
        limit_time = 1
        if int(promotion_status) > 0:
            limit_time = 0
        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV_NAME,
            'second_navs': export.get_promotion_and_apps_second_navs(request),
            'third_nav_name': export.MALL_PROMOTION_ORDER_RED_ENVELOPE,
            'second_nav_name': 'orderRedEnvelope',
            "coupon_rule_info": json.dumps(coupon_rule_info),
            "items": items,
            'endDate': endDate,
            "is_create": is_create,
            'promotion_status': promotion_status,
            'limit_time': limit_time
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
                'second_navs': export.get_promotion_and_apps_second_navs(request),
                'second_nav_name': export.MALL_APPS_SECOND_NAV,
                'third_nav_name': export.MALL_PROMOTION_ORDER_RED_ENVELOPE,
                'coupon_rule': coupon_rule,
                'red_envelope_rule': red_envelope_rule,
            })
            return render_to_response('mall/editor/create_red_envelope_rule.html', c)
        else:
            coupon_rules = promotion_models.CouponRule.objects.filter(owner=request.manager, is_active=True,
                                                                      end_date__gt=datetime.now(), limit_counts=-1)
            c = RequestContext(request, {
                'first_nav_name': FIRST_NAV_NAME,
                'second_navs': export.get_promotion_and_apps_second_navs(request),
                'second_nav_name': export.MALL_APPS_SECOND_NAV,
                'third_nav_name': export.MALL_PROMOTION_ORDER_RED_ENVELOPE,
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
        coupon_rule = promotion_models.CouponRule.objects.get(id=rule_data.coupon_rule_id)
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
            'receive_method': rule_data.receive_method,
            'coupon_rule_id': coupon_rule.id
        })
        return render_to_response('mall/editor/red_envelope_participences.html', c)

    @login_required
    def api_get(request):
        """
        获取advanced table
        """
        receive_method = request.GET.get('receive_method',0)
        pageinfo, items = get_datas(request)
        sort_attr = request.GET.get('sort_attr', 'id')
        response_data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': sort_attr,
			'data': {}
		}
        response = create_response(200)
        response.data = response_data
        return response.get_response()

def get_datas(request):
    receive_method = request.GET.get('receive_method','')
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
    grade_id = request.GET.get('grade_id', '')
    coupon_status = request.GET.get('coupon_status', '')
    params = {'red_envelope_rule_id':request.GET['id']}
    datas = promotion_models.GetRedEnvelopeRecord.objects.filter(**params).order_by('-id')
    if member_ids:
        params['member__in'] = member_ids
        datas = datas.filter(**params)
    if grade_id:
        member_ids = set()
        for data in datas:
            if grade_id == str(data.member.grade.id):
                member_ids.add(data.member_id)
        datas = datas.filter(member__in=list(member_ids))
    if coupon_status:
        coupon_ids = set()
        new_coupon_ids = set()
        for data in datas:
            coupon_ids.add(data.coupon_id)
        for coupon in Coupon.objects.filter(id__in=list(coupon_ids)):
            if coupon_status == '0':
                if 1 != coupon.status:
                    new_coupon_ids.add(coupon.id)
            else:
                if coupon_status == str(coupon.status):
                   new_coupon_ids.add(coupon.id)
        datas = datas.filter(coupon_id__in=list(new_coupon_ids))

    member2datas = {}
    member_ids = set()
    coupon_ids = set()
    for data in datas:
        coupon_ids.add(data.coupon_id)
        member2datas.setdefault(data.member_id, []).append(data)
        member_ids.add(data.member_id)
        data.participant_name = u'未知'
        data.participant_icon = '/static/img/user-1.jpg'
    id2Coupon = {}
    coupon_list = Coupon.objects.filter(id__in=list(coupon_ids))
    for coupon in coupon_list:
        id2Coupon[str(coupon.id)] = {
            'status_id': coupon.status,
            'status_name': COUPONSTATUS[coupon.status]['name']
        }
    print id2Coupon,"id2Coupon"
    # 获取被使用的优惠券使用者信息
    coupon_ids = [c.id for c in coupon_list if c.status == COUPON_STATUS_USED]
    orders = Order.get_orders_by_coupon_ids(coupon_ids)
    if orders:
        coupon_id2order_id = dict([(str(o.coupon_id), \
                                          {'order_id': o.id,})\
                                         for o in orders])
    else:
        coupon_id2order_id = {}

    if len(member_ids) > 0:
        member2data = {}
        for m in member_models.Member.objects.filter(id__in=member_ids):
            member2data[m.id]={
                'is_subscribed': m.is_subscribed,
                'username_for_html': m.username_for_html,
                'user_icon': m.user_icon,
                'grade': m.grade.name
            }
        for member in member_ids:
            for data in member2datas.get(member, ()):
                member_data = member2data[member]
                if member_data['is_subscribed']:
                    data.participant_name = member_data['username_for_html']
                    data.participant_icon = member_data['user_icon'] if member_data['user_icon'] else '/static/img/user-1.jpg'
                    if member_data['grade']:
                        grade_name = member_data['grade']
                    else:
                        if receive_method:
                            grade_name = u'会员'
                        else:
                            grade_name = u''
                    data.grade = grade_name
                else:
                    data.participant_name = u''
                    data.participant_icon = '/static/img/user-1.jpg'
                    if receive_method:
                        grade_name = u'会员'
                    else:
                        grade_name = u'非会员'
                    data.grade = grade_name

    #处理排序
    sort_attr = request.GET.get('sort_attr', 'id')
    if '-' in sort_attr:
        sort_attr = sort_attr.replace('-', '')
        datas = sorted(datas, key=lambda x: x['id'], reverse=True)
        datas = sorted(datas, key=lambda x: x[sort_attr], reverse=True)
        sort_attr = '-' + sort_attr
    else:
        datas = sorted(datas, key=lambda x: x['id'])
        datas = sorted(datas, key=lambda x: x[sort_attr])

    #进行分页
    count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
    cur_page = int(request.GET.get('page', '1'))
    pageinfo, datas = paginator.paginate(datas, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

    items = []
    for data in datas:
        red_envelope_participance = promotion_models.GetRedEnvelopeRecord.objects.get(id=data.id)
        items.append({
            'id': data.id,
            'member_id': data.member_id,
            'participant_name': data.participant_name,
            'participant_icon': data.participant_icon,
            'created_at': data.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'coupon_status_id': id2Coupon[data.coupon_id]['status_id'],
            'coupon_status': id2Coupon[data.coupon_id]['status_name'],
            'order_id': coupon_id2order_id[data.coupon_id]['order_id'] if coupon_id2order_id.has_key(data.coupon_id) else '',
            'grade': data.grade
        })

    return pageinfo, items

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
            'comparator': lambda promotion, filter_value: (int(filter_value) == -1) or (int(filter_value) == promotion.status),
            'query_string_field': 'promotionStatus'
        }, {
            'comparator': lambda promotion, filter_value: (int(filter_value) == -1) or (int(filter_value) == promotion.limit_time),
            'query_string_field': 'limitTime'
        }, {
            'comparator': lambda rule, filter_value: filter_value <= rule.start_time.strftime("%Y-%m-%d %H:%M"),
            'query_string_field': 'startDate'
        }, {
            'comparator': lambda rule, filter_value: filter_value >= rule.end_time.strftime("%Y-%m-%d %H:%M") or filter_value == '',
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

########################################################################
# get_red_members_filter_params: 获取过滤参数
########################################################################
class RedEnvelopeParticipancesFilter(resource.Resource):
    app = "apps/promotion"
    resource = "red_members_filter_params"

    @login_required
    def api_get(request):
        webapp_id = request.user_profile.webapp_id
        print webapp_id
        coupon_status = [{
            "id": 0,
            "name": u'未使用'
        },{
            "id": 1,
            "name": u'已使用'
        }]

        grades = []
        for grade in MemberGrade.get_all_grades_list(webapp_id):
            grades.append({
                "id": grade.id,
                "name": grade.name
            })

        response = create_response(200)
        response.data = {
            'coupon_status': coupon_status,
            'grades': grades
        }
        return response.get_response()

class redParticipances_Export(resource.Resource):
    '''
	批量导出
	'''
    app = 'apps/promotion'
    resource = 'red_participances_export'

    @login_required
    def api_get(request):
        """
        分析导出
        """
        export_id = request.GET.get('export_id')
        download_excel_file_name = u'红包分析详情.xls'
        excel_file_name = 'red_details.xls'
        export_file_path = os.path.join(settings.UPLOAD_DIR,excel_file_name)

        #Excel Process Part
        try:
            import xlwt
            name = request.GET.get('name', '')
            selected_ids = request.GET.get('selected_ids', '')
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
            grade_id = request.GET.get('grade_id', '')
            coupon_status = request.GET.get('coupon_status', '')
            params = {'red_envelope_rule_id':export_id}
            datas = promotion_models.GetRedEnvelopeRecord.objects.filter(**params).order_by('-id')
            if member_ids:
                params['member__in'] = member_ids
                datas = datas.filter(**params)
            if grade_id != '-1':
                member_ids = set()
                for data in datas:
                    if grade_id == str(data.member.grade.id):
                        member_ids.add(data.member_id)
                datas = datas.filter(member__in=list(member_ids))
            if coupon_status != '-1':
                coupon_ids = set()
                new_coupon_ids = set()
                for data in datas:
                    coupon_ids.add(data.coupon_id)
                for coupon in Coupon.objects.filter(id__in=list(coupon_ids)):
                    if coupon_status == str(coupon.status):
                       new_coupon_ids.add(coupon.id)
                datas = datas.filter(coupon_id__in=list(new_coupon_ids))
            if selected_ids:
                data_ids = set()
                for data in datas:
                    if str(data.id) in selected_ids:
                        data_ids.add(data.id)
                datas = datas.filter(id__in=list(data_ids))
            fields_pure = []
            export_data = []

            #from sample to get fields4excel_file
            fields_pure.append(u'编号')
            fields_pure.append(u'下单会员')
            fields_pure.append(u'会员状态')
            fields_pure.append(u'引入领取人数')
            fields_pure.append(u'引入使用人数')
            fields_pure.append(u'引入新关注')
            fields_pure.append(u'引入消费额')
            fields_pure.append(u'领取时间')
            fields_pure.append(u'使用状态')

            #username(member_id)
            member_ids = [record['member_id'] for record in datas ]
            members = member_models.Member.objects.filter(id__in = member_ids)
            member_id2name = {}
            for member in members:
                m_id = member.id
                if member.is_subscribed == True:
                    u_name = member.username
                else:
                    u_name = u'非会员'
                if m_id not in member_id2name:
                    member_id2name[m_id] = u_name
                else:
                    member_id2name[m_id] = u_name

            member_id2grade = {}
            for member in members:
                m_id = member.id
                member_id2grade[m_id] = member.grade.name

            coupon_ids = [record['coupon_id'] for record in datas ]
            coupons = Coupon.objects.filter(id__in = list(coupon_ids))
            coupon_id2status = {}
            for coupon in coupons:
                c_id = coupon.id
                if coupon.status == 1:
                    coupon.status = u'已使用'
                else:
                    coupon.status = u'未使用'
                coupon_id2status[c_id] = coupon.status
            #processing data
            num = 0
            for record in datas:
                export_record = []
                num = num+1
                name = member_id2name[record['member_id']]
                grade_name = member_id2grade[record['member_id']]
                created_at = record['created_at'].strftime("%Y-%m-%d %H:%M:%S")
                status = coupon_id2status[int(record['coupon_id'])]
                # don't change the order
                export_record.append(num)
                export_record.append(name)
                #TODO 显示正确数字
                export_record.append(grade_name)
                export_record.append('')
                export_record.append('')
                export_record.append('')
                export_record.append('')
                export_record.append(created_at)
                export_record.append(status)
                export_data.append(export_record)

            #workbook/sheet
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('id%s'%export_id)
            header_style = xlwt.XFStyle()

            ##write fields
            row = col = 0
            for h in fields_pure:
                ws.write(row,col,h)
                col += 1

            ##write data
            if export_data:
                row = 1
                lens = len(export_data[0])
                for record in export_data:
                    row_l = []
                    for col in range(lens):
                        record_col= record[col]
                        if type(record_col)==list:
                            row_l.append(len(record_col))
                            for n in range(len(record_col)):
                                data = record_col[n]
                                ws.write(row+n,col,data)
                        else:
                            ws.write(row,col,record[col])
                    if row_l:
                        row = row + max(row_l)
                    else:
                        row += 1
                try:
                    wb.save(export_file_path)
                except Exception, e:
                    print 'EXPORT EXCEL FILE SAVE ERROR'
                    print e
                    print '/static/upload/%s'%excel_file_name
            else:
                ws.write(1,0,'')
                wb.save(export_file_path)
            response = create_response(200)
            response.data = {'download_path':'/static/upload/%s'%excel_file_name,'filename':download_excel_file_name,'code':200}
        except Exception, e:
            print e
            response = create_response(500)

        return response.get_response()
