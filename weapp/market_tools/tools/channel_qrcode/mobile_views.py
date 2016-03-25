# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User

from models import *
from modules.member.models import *
from  weixin.user.module_api import get_mp_head_img, get_mp_qrcode_img
from account.util import get_binding_weixin_mpuser, get_mpuser_accesstoken
from core.wxapi import get_weixin_api
from core.wxapi.api_create_qrcode_ticket import QrcodeTicket
from mall.models import *

template_path_items = os.path.dirname(__file__).split(os.sep)
TEMPLATE_DIR = '%s/templates' % template_path_items[-1]

def get_settings(request):
    user_id = request.GET.get('webapp_owner_id', 0)
    ticketid = request.GET.get('ticketid', 0)
    member = request.member
    #if user_id == '467':
    if ticketid:
        setting = ChannelQrcodeSettings.objects.get(id=ticketid)
        show_head = False
        if setting.bing_member_id == request.member.id:
            show_head = True
            member = Member.objects.get(id=request.member.id)
            member.user_name = member.username_for_html
            setting.count = ChannelQrcodeHasMember.objects.filter(channel_qrcode_id=setting.id).count()

        c = RequestContext(request, {
                'page_title': u'代言人二维码',
                'member': member,
                'setting': setting,
                'is_hide_weixin_option_menu': False,
                'head_img': get_mp_head_img(user_id),
                'show_head': show_head,
                'hide_non_member_cover':True
            })
        return render_to_response('%s/channel_qrcode/webapp/channel_qrcode_img.html' % TEMPLATE_DIR, c)
    else:
        if request.member:
            setting = ChannelQrcodeSettings.objects.filter(bing_member_id=request.member.id, is_bing_member=True)
            if setting.count() > 0:
                setting = setting[0]
                new_url = '%s&ticketid=%s' % (request.get_full_path(), setting.id)
                return HttpResponseRedirect(new_url)
        c = RequestContext(request, {
                'page_title': u'代言人二维码',})
        return render_to_response('%s/channel_qrcode/webapp/channel_qrcode_context.html' % TEMPLATE_DIR, c)
    # else:
    #     if request.member:
    #         setting = ChannelQrcodeSettings.objects.filter(bing_member_id=request.member.id, is_bing_member=True)

    #         if setting.count() > 0:
    #             setting = setting[0]
    #             member = Member.objects.get(id=request.member.id)
    #             member.user_name = member.username_for_html
    #             setting.count = ChannelQrcodeHasMember.objects.filter(channel_qrcode_id=setting.id).count()
    #             c = RequestContext(request, {
    #                 'page_title': u'代言人二维码',
    #                 'member': member,
    #                 'setting': setting,
    #                 'is_hide_weixin_option_menu': False,
    #                 'head_img': get_mp_head_img(user_id),
    #                 'hide_non_member_cover':True
    #             })
    #             return render_to_response('%s/channel_qrcode/webapp/channel_qrcode.html' % TEMPLATE_DIR, c)

    #     c = RequestContext(request, {
    #             'page_title': u'代言人二维码',})
    #     return render_to_response('%s/channel_qrcode/webapp/channel_qrcode_context.html' % TEMPLATE_DIR, c)

def get_new_settings(request):
    user_id = request.webapp_owner_id
    ticketid = request.GET.get('ticketid', 0)
    member = request.member
    member = Member.objects.get(id=request.member.id)
    qrcode_setting = MemberChannelQrcodeSettings.objects.get(owner_id=user_id)
    if ticketid:
        qrcode = MemberChannelQrcode.objects.get(id=ticketid)
        if not qrcode.ticket:
            ticket = _get_ticket(user_id, qrcode.id)
            qrcode.ticket = ticket
            qrcode.save()

        show_head = False
        if qrcode.member_id == member.id:
            show_head = True
            member.user_name = member.username_for_html
            qrcode.count = MemberChannelQrcodeHasMember.objects.filter(member_channel_qrcode_id=qrcode.id).count()


        c = RequestContext(request, {
                'page_title': u'首草送好礼，接力扫码等你来传递',
                'member': member,
                'qrcode': qrcode,
                "qrcode_setting": qrcode_setting,
                'is_hide_weixin_option_menu': False,
                'head_img': get_mp_head_img(user_id),
                'show_head': show_head,
                'hide_non_member_cover':True
            })
        return render_to_response('%s/channel_qrcode/webapp/new_channel_qrcode_img.html' % TEMPLATE_DIR, c)
    else:
        content_dict = {}
        if member and member.is_subscribed:
            member.user_name = member.username_for_html
            qrcode = MemberChannelQrcode.objects.filter(member_id=request.member.id)
            if qrcode.count() > 0:
                qrcode = qrcode[0]
                new_url = '%s&ticketid=%s' % (request.get_full_path(), qrcode.id)
                return HttpResponseRedirect(new_url)
            else:
                new_qrcode = MemberChannelQrcode.objects.create(
                    owner_id=user_id,
                    member_channel_qrcode_setting_id=qrcode_setting.id,
                    member_id=member.id,
                    ticket=''
                )
                ticket = _get_ticket(user_id, new_qrcode.id)
                new_qrcode.ticket = ticket
                new_qrcode.save()
                new_qrcode.count = 0
                content_dict = {
                    'page_title': u'首草送好礼，接力扫码等你来传递',
                    'member': member,
                    'qrcode': new_qrcode,
                    "qrcode_setting": qrcode_setting,
                    'show_head': True,
                    'head_img': get_mp_head_img(user_id)
                }
                c = RequestContext(request, content_dict)
                return render_to_response('%s/channel_qrcode/webapp/new_channel_qrcode_img.html' % TEMPLATE_DIR, c)

        qrcode_img = get_mp_qrcode_img(user_id)
        content_dict = {
            'page_title': u'首草送好礼，欢迎关注！',
            'qrcode_img': qrcode_img
        }
        c = RequestContext(request, content_dict)
        return render_to_response('%s/channel_qrcode/webapp/new_channel_qrcode_error.html' % TEMPLATE_DIR, c)



def _get_ticket(user_id, screen_id):
    mp_user = get_binding_weixin_mpuser(user_id)
    mpuser_access_token = get_mpuser_accesstoken(mp_user)
    weixin_api = get_weixin_api(mpuser_access_token)
    if mp_user.is_certified and mp_user.is_service and mpuser_access_token.is_active:
        try:
            qrcode_ticket = weixin_api.create_qrcode_ticket(screen_id, QrcodeTicket.PERMANENT)
            return qrcode_ticket.ticket
        except:
            return _get_ticket(user_id, screen_id)

    else:
        try:
            qrcode_ticket = weixin_api.create_qrcode_ticket(screen_id, QrcodeTicket.PERMANENT)
            return qrcode_ticket.ticket
        except:
            return ''

def get_settings_detail(request):
    sid = request.GET.get('sid', 0)
    member = request.member
    user_id = request.webapp_owner_id
    startDate = request.GET.get('startDate', None)
    endDate = request.GET.get('endDate', None)
    if sid:
        setting = ChannelQrcodeSettings.objects.get(id=sid)

        if setting.bing_member_id == request.member.id:
            relations = ChannelQrcodeHasMember.objects.filter(channel_qrcode_id=setting.id)
            if startDate and endDate:
                relations = relations.filter(created_at__gte = startDate,created_at__lte = endDate)
            payed_count = 0
            pay_money = 0
            payed_member = []
            setting_id2count = {}
            member_id2setting_id = {}
            member_ids = []
            filter_data_args = {}
            filter_data_args['status__in'] = (ORDER_STATUS_PAYED_SUCCESSED, ORDER_STATUS_PAYED_NOT_SHIP, ORDER_STATUS_PAYED_SHIPED, ORDER_STATUS_SUCCESSED)
            old_member_id2_create_at = {}
            new_member_id2_create_at = {}
            for r in relations:
                member_ids.append(r.member_id)
                member_id2setting_id[r.member_id] = r.channel_qrcode_id
                if r.channel_qrcode_id in setting_id2count:
                    setting_id2count[r.channel_qrcode_id] += 1
                else:
                    setting_id2count[r.channel_qrcode_id] = 1
                if r.is_new:
                    new_member_id2_create_at[r.member_id] = r.created_at
                    if r.member.pay_times > 0:
                        payed_member.append(r.member_id)

                else:
                    old_member_id2_create_at[r.member_id] = r.created_at

            bind_phone_members = MemberInfo.objects.filter(member_id__in = member_ids,is_binded = 1)

            new_webapp_users = WebAppUser.objects.filter(member_id__in=new_member_id2_create_at.keys())
            new_webapp_user_ids = [u.id for u in new_webapp_users]

            #获取old会员的webapp_user
            old_webapp_users = WebAppUser.objects.filter(member_id__in=old_member_id2_create_at.keys())
            old_member_order_ids = []

            for webapp_user in old_webapp_users:
                created_at = old_member_id2_create_at[webapp_user.member_id]
                for order in Order.by_webapp_user_id(webapp_user.id).filter(created_at__gte=created_at):
                    old_member_order_ids.append(order.id)
                    payed_member.append(webapp_user.member_id)

            if new_webapp_user_ids and old_member_order_ids:
                orders = Order.by_webapp_user_id(new_webapp_user_ids, order_id=old_member_order_ids).filter(**filter_data_args).order_by('-created_at')
            elif new_webapp_user_ids:
                orders = Order.by_webapp_user_id(new_webapp_user_ids).filter(**filter_data_args).order_by('-created_at')
            elif old_member_order_ids:
                filter_data_args['id__in'] = old_member_order_ids
                orders = Order.objects.filter(**filter_data_args).order_by('-created_at')
            else:
                orders = []

            for order in orders:
                pay_money += (order.final_price + order.weizoom_card_money)

            c = RequestContext(request, {
                    'page_title': u'推荐详情',
                    'member': member,
                    'setting': setting,
                    'is_hide_weixin_option_menu': True,
                    'head_img': get_mp_head_img(user_id),
                    'hide_non_member_cover':True,
                    'channel_qrcode_members':relations,
                    'channel_qrcode_members_count':relations.count(),
                    'pay_money': '%.2f' %  pay_money,
                    'payed_count': len(set(payed_member)),
                    'bind_phone_members_count': len(bind_phone_members),
                    'startDate': startDate,
                    'endDate': endDate
                })
            return render_to_response('%s/channel_qrcode/webapp/channel_qrcode_members.html' % TEMPLATE_DIR, c)


    c = RequestContext(request, {
                'page_title': u'代言人二维码',})
    return render_to_response('%s/channel_qrcode/webapp/channel_qrcode_context.html' % TEMPLATE_DIR, c)