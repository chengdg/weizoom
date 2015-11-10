# -*- coding: utf-8 -*-
from datetime import datetime

from django.template import RequestContext
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from weixin.mp_decorators import mp_required
from django.shortcuts import render_to_response

from core import resource
from core import paginator
from utils.string_util import byte_to_hex
from weixin2 import export

from modules.member import models as member_model
from core.jsonresponse import JsonResponse, create_response, decode_json_str
from weixin.user.models import DEFAULT_ICON, get_system_user_binded_mpuser
from market_tools.tools.coupon.util import get_coupon_rules, get_my_coupons
from market_tools.tools.channel_qrcode.models import MemberChannelQrcodeSettings, MemberChannelQrcode, MemberChannelQrcodeHasMember, MemberChannelQrcodeAwardContent
from modules.member.module_api import get_member_by_id_list, get_member_by_id
from modules.member import models as member_model

from core.wxapi import get_weixin_api
from account.util import get_binding_weixin_mpuser, get_mpuser_accesstoken
from core.wxapi.api_create_qrcode_ticket import QrcodeTicket


COUNT_PER_PAGE = 50
FIRST_NAV = export.WEIXIN_HOME_FIRST_NAV

class ChannelQrcode(resource.Resource):
    app = 'new_weixin'
    resource = 'channel_qrcode'

    @login_required
    @mp_required
    def get(request):
        mpuser = get_system_user_binded_mpuser(request.manager)

        if (mpuser is None) or (not mpuser.is_certified) or (not mpuser.is_service):
            should_show_authorize_cover = True
        else:
            should_show_authorize_cover = False

        coupon_rules = get_coupon_rules(request.manager)
        try:
            member_qrcode_setting = MemberChannelQrcodeSettings.objects.get(owner=request.manager)
        except:
            member_qrcode_setting = None

        if member_qrcode_setting:
            try:
                award_content = MemberChannelQrcodeAwardContent.objects.get(owner=request.manager)
            except:
                award_content = None
        else:
            award_content = None

        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_weixin_second_navs(request),
            'second_nav_name': export.WEIXIN_ADVANCE_SECOND_NAV,
            'third_nav_name': export.ADVANCE_MANAGE_MEMBER_CHANNEL_QRCODE_NAV,
            'member_qrcode_settings': member_qrcode_setting,
            'coupon_rules': coupon_rules,
            'award_content': award_content,
            'should_show_authorize_cover': should_show_authorize_cover,
            'is_hide_weixin_option_menu': True
        })

        return render_to_response('weixin/advance_manage/edit_member_channel_qrcode.html', c)

    @login_required
    @mp_required
    def api_post(request):
        id = int(request.POST.get('id', 0))
        reward = request.POST.get('reward', '')
        detail = request.POST.get('detail', '').strip()

        if reward == '':
            response = create_response(400)
            return response.get_response()

        if reward == '1':
            scanner_award_content = request.POST.get('prize_source|0', '')
            scanner_award_type = request.POST.get('prize_type|0', '')

            share_award_content = request.POST.get('prize_source|1', '')
            share_award_type = request.POST.get('prize_type|1', '')

            if scanner_award_content == '' or scanner_award_content == '' or \
            share_award_content == '' or share_award_type == '':
                response = create_response(400)
                return response.get_response()

            if id:
                MemberChannelQrcodeSettings.objects.filter(id=id).update(
                    award_member_type=int(reward),
                    detail=detail
                )
                MemberChannelQrcodeAwardContent.objects.filter(owner=request.manager).delete()
                MemberChannelQrcodeAwardContent.objects.create(
                        owner=request.manager,
                        member_channel_qrcode_settings_id=id,
                        scanner_award_type=scanner_award_type,
                        scanner_award_content=scanner_award_content,
                        share_award_content=share_award_content,
                        share_award_type=share_award_type
                )
            else:
                member_qrcode_settings = MemberChannelQrcodeSettings.objects.create(
                        owner=request.manager,
                        award_member_type=int(reward),
                        detail=detail
                    )

                MemberChannelQrcodeAwardContent.objects.create(
                        owner=request.manager,
                        member_channel_qrcode_settings=member_qrcode_settings,
                        scanner_award_type=scanner_award_type,
                        scanner_award_content=scanner_award_content,
                        share_award_content=share_award_content,
                        share_award_type=share_award_type
                    )

        response = create_response(200)
        return response.get_response()

class ChannelQrcodes(resource.Resource):
    app = 'new_weixin'
    resource = 'channel_qrcodes'

    @login_required
    @mp_required
    def get(request):
        """
        会员渠道扫码列表页面
        """
        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_weixin_second_navs(request),
            'second_nav_name': export.WEIXIN_ADVANCE_SECOND_NAV,
            'third_nav_name': export.ADVANCE_MANAGE_MEMBER_CHANNEL_QRCODE_NAV,
        })
        return render_to_response('weixin/advance_manage/channel_qrcodes.html', c)

    @login_required
    @mp_required
    def api_get(request):
        sort_attr = request.GET.get('sort_attr', '-created_at')
        items = _get_channel_qrcode_items(request)

        #进行分页
        if 'created_at' not in  sort_attr:
            if '-' in sort_attr:
                sorter = sort_attr[1:]
                is_reverse = True
            else:
                sorter = sort_attr
                is_reverse = False

            # items = sorted(items, reverse=is_reverse, key=lambda b : getattr(b, sorter))
            items = sorted(items, reverse=is_reverse, key=lambda x:getattr(x, sorter))
        count_per_page = int(request.GET.get('count_per_page', 15))
        cur_page = int(request.GET.get('page', '1'))
        pageinfo, items = paginator.paginate(items, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

        new_items = []
        for item in items:
            new_items.append(item.__dict__)

        response = create_response(200)
        response.data = {
            'items': new_items,
            'pageinfo': paginator.to_dict(pageinfo),
            'sortAttr': sort_attr,
            'data': {}
        }
        return response.get_response()

def _get_channel_qrcode_items(request):
    #处理搜索
    from mall.models import *
    query = request.GET.get('query', '').strip()
    sort_attr = request.GET.get('sort_attr', '-created_at')
    created_at = '-created_at'
    if 'created_at' in  sort_attr:
        created_at = sort_attr

    setting = MemberChannelQrcodeSettings.objects.filter(owner=request.manager)

    if setting.count() > 0:
        member_channel_qrcodes = MemberChannelQrcode.objects.filter(
            member_channel_qrcode_setting=setting[0])
        if query:
            member_ids = [qrcode.member_id for qrcode in member_channel_qrcodes]
            query_hex = byte_to_hex(query)
            members = member_model.Member.objects.filter(id__in=member_ids).filter(username_hexstr__contains=query_hex)
            member_ids = [m.id for m in members]
            member_channel_qrcodes = member_channel_qrcodes.filter(member_id__in=member_ids)
    else:
        return create_response(500).get_response()

    member_channel_qrcode_ids = [qrcode.id for qrcode in member_channel_qrcodes]

    relations = MemberChannelQrcodeHasMember.objects.filter(member_channel_qrcode__in=member_channel_qrcode_ids)
    member_channel_qrcode_id2count = {}
    member_id2member_channel_qrcode_id = {}
    member_id2relation = {}
    member_ids = []
    for r in relations:
        member_ids.append(r.member_id)
        member_id2member_channel_qrcode_id[r.member_id] = r.member_channel_qrcode_id
        member_id2relation[r.member_id] = r
        if r.member_channel_qrcode_id in member_channel_qrcode_id2count:
            member_channel_qrcode_id2count[r.member_channel_qrcode_id] += 1
        else:
            member_channel_qrcode_id2count[r.member_channel_qrcode_id] = 1

    webapp_users = member_model.WebAppUser.objects.filter(member_id__in=member_ids)
    webapp_user_id2member_id = dict([(u.id, u.member_id) for u in webapp_users])
    webapp_user_ids = set(webapp_user_id2member_id.keys())
    orders = Order.by_webapp_user_id(webapp_user_ids).filter(status__in=(ORDER_STATUS_PAYED_SUCCESSED, ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED))

    member_id2total_final_price = {}
    member_id2cash_money = {}
    member_id2weizoom_card_money = {}
    for order in orders:
        member_id = webapp_user_id2member_id[order.webapp_user_id]
        if member_id2relation[member_id].is_new or member_id2relation[member_id].created_at <= order.created_at:
            if member_id in member_id2total_final_price:
                member_id2total_final_price[member_id] += order.final_price + order.weizoom_card_money
                member_id2cash_money[member_id] += order.final_price
                member_id2weizoom_card_money[member_id] += order.weizoom_card_money
            else:
                member_id2total_final_price[member_id] = order.final_price + order.weizoom_card_money
                member_id2cash_money[member_id] = order.final_price
                member_id2weizoom_card_money[member_id] = order.weizoom_card_money

    member_channel_qrcode_id2total_final_price = {}
    member_channel_qrcode_id2cash_money = {}
    member_channel_qrcode_id2weizoom_card_money = {}
    for member_id in member_id2total_final_price.keys():
        final_price = member_id2total_final_price[member_id]
        cash_money = member_id2cash_money[member_id]
        weizoom_card_money = member_id2weizoom_card_money[member_id]
        member_channel_qrcode_id = member_id2member_channel_qrcode_id[member_id]
        if member_channel_qrcode_id in member_channel_qrcode_id2total_final_price:
            member_channel_qrcode_id2total_final_price[member_channel_qrcode_id] += final_price
            member_channel_qrcode_id2cash_money[member_channel_qrcode_id] += cash_money
            member_channel_qrcode_id2weizoom_card_money[member_channel_qrcode_id] += weizoom_card_money
        else:
            member_channel_qrcode_id2total_final_price[member_channel_qrcode_id] = final_price
            member_channel_qrcode_id2cash_money[member_channel_qrcode_id] = cash_money
            member_channel_qrcode_id2weizoom_card_money[member_channel_qrcode_id] = weizoom_card_money



    response = create_response(200)
    #response.data.items = []
    items = []

    mp_user = get_binding_weixin_mpuser(request.manager)
    mpuser_access_token = get_mpuser_accesstoken(mp_user)

    for qrcode in member_channel_qrcodes:
        current_qrcode = JsonResponse()

        if qrcode.id in member_channel_qrcode_id2count:
            qrcode.count = member_channel_qrcode_id2count[qrcode.id]
        else:
            qrcode.count = 0
        if qrcode.id in member_channel_qrcode_id2total_final_price:
            qrcode.total_final_price = member_channel_qrcode_id2total_final_price[qrcode.id]
            qrcode.cash_money = member_channel_qrcode_id2cash_money[qrcode.id]
            qrcode.weizoom_card_money = member_channel_qrcode_id2weizoom_card_money[qrcode.id]
        else:
            qrcode.total_final_price = 0
            qrcode.cash_money = 0
            qrcode.weizoom_card_money = 0

        #如果没有ticket信息则获取ticket信息
        if not qrcode.ticket:
            try:
                if mp_user.is_certified and mp_user.is_service and mpuser_access_token.is_active:
                    weixin_api = get_weixin_api(mpuser_access_token)
                    qrcode_ticket = weixin_api.create_qrcode_ticket(int(qrcode.id), QrcodeTicket.PERMANENT)

                    try:
                        ticket = qrcode_ticket.ticket
                    except:
                        ticket = ''
                    qrcode.ticket = ticket
                    qrcode.save()
            except:
                pass
        current_qrcode.id = qrcode.id
        current_qrcode.name = qrcode.member.username_for_html
        current_qrcode.count = qrcode.count
        current_qrcode.total_final_price = round(qrcode.total_final_price,2)
        current_qrcode.ticket = qrcode.ticket
        current_qrcode.created_at = qrcode.created_at.strftime('%Y-%m-%d %H:%M:%S')

        items.append(current_qrcode)
    return items

class ChannelQrcodeMember(resource.Resource):
    app = 'new_weixin'
    resource = 'channel_qrcode_member'

    @login_required
    @mp_required
    def get(request):
        """
        带参数二维码
        """
        qrcode_id = request.GET.get('qrcode_id', None)
        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_weixin_second_navs(request),
            'second_nav_name': export.ADVANCE_MANAGE_MEMBER_CHANNEL_QRCODE_NAV,
            'qrcode_id': qrcode_id
        })

        return render_to_response('weixin/advance_manage/channel_qrcode_member.html', c)

    @login_required
    @mp_required
    def api_get(request):
        channel_qrcode_id = int(request.GET['qrcode_id'])
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')
        is_show = request.GET.get('is_show', '0')

        sort_attr = request.GET.get('sort_attr', '-created_at')

        if is_show == '1':
            member_ids = [relation.member_id for relation in \
                MemberChannelQrcodeHasMember.objects.filter(member_channel_qrcode_id=channel_qrcode_id, is_new=True)]
        else:
            member_ids = [relation.member_id for relation in \
                MemberChannelQrcodeHasMember.objects.filter(member_channel_qrcode_id=channel_qrcode_id)]

        filter_data_args = {}
        filter_data_args['id__in'] = member_ids

        if start_date:
            filter_data_args['created_at__gte'] = start_date

        if end_date:
            filter_data_args['created_at__lte'] = end_date

        channel_members = member_model.Member.objects.filter(**filter_data_args).order_by(sort_attr)
        count_per_page = int(request.GET.get('count_per_page', 15))
        cur_page = int(request.GET.get('page', '1'))
        pageinfo, channel_members = paginator.paginate(channel_members, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

        return_channel_members_json_array = []

        for channel_member in channel_members:
            member_info = member_model.MemberInfo.get_member_info(channel_member.id)
            if member_info:
                channel_member.name = member_info.name
            else:
                channel_member.name = ''

            return_channel_members_json_array.append(build_member_basic_json(channel_member))

        response = create_response(200)
        response.data = {
            'items': return_channel_members_json_array,
            'pageinfo': paginator.to_dict(pageinfo),
            'sortAttr': sort_attr,
            'data': {}
        }

        return response.get_response()

class ChannelQrcodeOrder(resource.Resource):
    app = 'new_weixin'
    resource = 'channel_qrcode_order'

    @login_required
    @mp_required
    def get(request):
        """
        带参数二维码
        """
        qrcode_id = request.GET.get('qrcode_id', None)
        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_weixin_second_navs(request),
            'second_nav_name': export.ADVANCE_MANAGE_MEMBER_CHANNEL_QRCODE_NAV,
            'qrcode_id': qrcode_id
        })

        return render_to_response('weixin/advance_manage/channel_qrcode_order.html', c)

    @login_required
    @mp_required
    def api_get(request):
        from mall import module_api as mall_api
        from mall.models import *
        channel_qrcode_id = request.GET.get('qrcode_id', None)
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')
        is_show = request.GET.get('is_show', '0')

        filter_data_args = {}

        if start_date:
            filter_data_args['created_at__gte'] = start_date

        if end_date:
            filter_data_args['created_at__lte'] = end_date
        filter_data_args['status__in'] = (ORDER_STATUS_PAYED_SUCCESSED, ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED)

        relations = MemberChannelQrcodeHasMember.objects.filter(member_channel_qrcode_id=channel_qrcode_id)
        setting_id2count = {}
        member_id2setting_id = {}
        member_ids = []

        old_member_id2_create_at = {}
        new_member_id2_create_at = {}
        for r in relations:
            member_ids.append(r.member_id)
            member_id2setting_id[r.member_id] = r.member_channel_qrcode_id
            if r.member_channel_qrcode_id in setting_id2count:
                setting_id2count[r.member_channel_qrcode_id] += 1
            else:
                setting_id2count[r.member_channel_qrcode_id] = 1
            if r.is_new:
                new_member_id2_create_at[r.member_id] = r.created_at
            else:
                old_member_id2_create_at[r.member_id] = r.created_at

        if is_show == '1':
            #获取新会员的webapp_user
            new_webapp_users = member_model.WebAppUser.objects.filter(member_id__in=new_member_id2_create_at.keys())
            new_webapp_user_ids = [u.id for u in new_webapp_users]

            #获取old会员的webapp_user
            old_webapp_users = member_model.WebAppUser.objects.filter(member_id__in=old_member_id2_create_at.keys())
            old_member_order_ids = []
            for webapp_user in old_webapp_users:
                created_at = old_member_id2_create_at[webapp_user.member_id]
                for order in Order.by_webapp_user_id(webapp_user.id).filter(created_at__gte=created_at):
                    old_member_order_ids.append(order.id)

            if new_webapp_user_ids and old_member_order_ids:
                orders = Order.by_webapp_user_id(new_webapp_user_ids, order_id=old_member_order_ids).filter(**filter_data_args).order_by('-created_at')
            elif new_webapp_user_ids:
                orders = Order.by_webapp_user_id(new_webapp_user_ids).filter(**filter_data_args).order_by('-created_at')
            elif old_member_order_ids:
                filter_data_args['id__in'] = old_member_order_ids
                orders = Order.objects.filter(**filter_data_args).order_by('-created_at')
            else:
                orders = []
        else:
            webapp_users = member_model.WebAppUser.objects.filter(member_id__in=member_ids)
            webapp_user_id2member_id = dict([(u.id, u.member_id) for u in webapp_users])
            webapp_user_ids = set(webapp_user_id2member_id.keys())
            if webapp_user_ids:
                orders = Order.by_webapp_user_id(webapp_user_ids).filter(**filter_data_args).order_by('-created_at')
            else:
                orders = []


        #add by duhao 2015-06-29 统计微众卡支付总金额和现金支付总金额
        final_price = 0
        weizoom_card_money = 0
        for order in orders:
            final_price += order.final_price
            weizoom_card_money += order.weizoom_card_money


        #进行分页
        count_per_page = int(request.GET.get('count_per_page', 15))
        cur_page = int(request.GET.get('page', '1'))
        pageinfo, orders = paginator.paginate(orders, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

        #获取order对应的会员
        webapp_user_ids = set([order.webapp_user_id for order in orders])
        webappuser2member = member_model.Member.members_from_webapp_user_ids(webapp_user_ids)

        #获得order对应的商品数量
        order_ids = [order.id for order in orders]
        order2productcount = {}
        for relation in OrderHasProduct.objects.filter(order_id__in=order_ids):
            order_id = relation.order_id
            if order_id in order2productcount:
                order2productcount[order_id] = order2productcount[order_id] + 1
            else:
                order2productcount[order_id] = 1
        #构造返回的order数据
        items = []
        today = datetime.today()
        for order in  orders:
             #获取order对应的member的显示名
             member = webappuser2member.get(order.webapp_user_id, None)
             if member:
                 order.buyer_name = member.username_for_html
                 order.buyer_id = member.id
             else:
                 order.buyer_name = u'未知'

             items.append({
                'id': order.id,
                'source': order.order_source,
                'order_id': order.order_id,
                'status': get_order_status_text(order.status),
                'total_price': order.final_price,
                'ship_name': order.ship_name,
                'buyer_name': order.buyer_name,
                'buyer_id': order.buyer_id,
                'pay_interface_name': PAYTYPE2NAME.get(order.pay_interface_type, u''),
                'created_at': datetime.strftime(order.created_at,'%Y-%m-%d %H:%M'),
                'payment_time':datetime.strftime(order.created_at,'%Y-%m-%d %H:%M'),
                'product_count': order2productcount.get(order.id, 0),
                'products': mall_api.get_order_products(order),
                'customer_message': order.customer_message,
                'order_status':order.status,
                'express_company_name': order.express_company_name,
                'express_number': order.express_number,
                'leader_name': order.leader_name,
                'remark': order.remark,
                'postage': '%.2f' % order.postage,
                'save_money': '%.2f' % (float(Order.get_order_has_price_number(order)) + float(order.postage) - float(order.final_price) - float(order.weizoom_card_money)),
                'weizoom_card_money': float('%.2f' % order.weizoom_card_money),
                'pay_money': '%.2f' % (order.final_price + order.weizoom_card_money)
             })

        response = create_response(200)
        response.data = {
            'items': items,
            'final_price': '%.2f' % final_price,
            'weizoom_card_money': '%.2f' % weizoom_card_money,
            'sortAttr': request.GET.get('sort_attr', '-created_at'),
            'pageinfo': paginator.to_dict(pageinfo),
            'data': {}
        }
        return response.get_response()

def build_member_basic_json(member):
    return {
        'id': member.id,
        'username': member.username_for_html,
        'name': member.name,
        'user_icon': member.user_icon,
        'integral': member.integral,
        'pay_money': '%.2f' % member.pay_money,
        'pay_times': member.pay_times,
        'grade_name': member.grade.name,
        "follow_time": member.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        "is_subscribed": member.is_subscribed
    }

def get_order_status_text(status):
    return STATUS2TEXT[status]