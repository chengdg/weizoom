# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User

from models import *
from modules.member.models import Member
from  weixin.user.module_api import get_mp_head_img
from account.util import get_binding_weixin_mpuser, get_mpuser_accesstoken
from core.wxapi import get_weixin_api
from core.wxapi.api_create_qrcode_ticket import QrcodeTicket


template_path_items = os.path.dirname(__file__).split(os.sep)
TEMPLATE_DIR = '%s/templates' % template_path_items[-1]

def get_settings(request):
    user_id = request.GET.get('webapp_owner_id', 0)
    ticketid = request.GET.get('ticketid', 0)
    member = request.member
    if user_id == '467':
        if ticketid:
            setting = ChannelQrcodeSettings.objects.get(id=ticketid)
            show_head = False
            if setting.bing_member_id == request.member.id:
                show_head = True
                member = Member.objects.get(id=request.member.id)
                member.user_name = member.username_for_html
                setting.count = ChannelQrcodeHasMember.objects.filter(channel_qrcode_id=setting.id).count()

            c = RequestContext(request, {
                    'page_title': u'首草送好礼，接力扫码等你来传递',
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
    else:
        if request.member:
            setting = ChannelQrcodeSettings.objects.filter(bing_member_id=request.member.id, is_bing_member=True)
            if setting.count() > 0:
                setting = setting[0]
                member = Member.objects.get(id=request.member.id)
                member.user_name = member.username_for_html
                setting.count = ChannelQrcodeHasMember.objects.filter(channel_qrcode_id=setting.id).count()
                c = RequestContext(request, {
                    'page_title': u'代言人二维码',
                    'member': member,
                    'setting': setting,
                    'is_hide_weixin_option_menu': True,
                    'head_img': get_mp_head_img(user_id),
                    'hide_non_member_cover':True
                })
                return render_to_response('%s/channel_qrcode/webapp/channel_qrcode.html' % TEMPLATE_DIR, c)

        c = RequestContext(request, {
                'page_title': u'代言人二维码',})
        return render_to_response('%s/channel_qrcode/webapp/channel_qrcode_context.html' % TEMPLATE_DIR, c)

def get_new_settings(request):
    user_id = request.webapp_owner_id
    ticketid = request.GET.get('ticketid', 0)
    member = request.member
    qrcode_setting = MemberChannelQrcodeSettings.objects.get(owner_id=user_id)
    if ticketid:
        qrcode = MemberChannelQrcode.objects.get(id=ticketid)
        if not qrcode.ticket:
            ticket = _get_ticket(user_id)
            qrcode.ticket = ticket
            qrcode.save()

        show_head = False
        if qrcode.member_id == request.member.id:
            show_head = True
            member = Member.objects.get(id=request.member.id)
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
        if request.member:
            qrcode = MemberChannelQrcode.objects.filter(member_id=request.member.id)
            if qrcode.count() > 0:
                qrcode = qrcode[0]
                new_url = '%s&ticketid=%s' % (request.get_full_path(), qrcode.id)
                return HttpResponseRedirect(new_url)
            else:
                ticket = _get_ticket(user_id)
                new_qrcode = MemberChannelQrcode.objects.create(
                    owner_id=user_id,
                    member_channel_qrcode_setting_id=qrcode_setting.id,
                    member_id=member.id,
                    ticket=ticket
                )
                new_qrcode.count = 0

        c = RequestContext(request, {
                'page_title': u'首草送好礼，接力扫码等你来传递',
                'member': member,
                'qrcode': new_qrcode,
                "qrcode_setting": qrcode_setting,
                'show_head': True,
                'head_img': get_mp_head_img(user_id)
                })
        return render_to_response('%s/channel_qrcode/webapp/new_channel_qrcode_img.html' % TEMPLATE_DIR, c)

def _get_ticket(user_id):
    mp_user = get_binding_weixin_mpuser(user_id)
    mpuser_access_token = get_mpuser_accesstoken(mp_user)
    weixin_api = get_weixin_api(mpuser_access_token)
    if mp_user.is_certified and mp_user.is_service and mpuser_access_token.is_active:
        try:
            qrcode_ticket = weixin_api.create_qrcode_ticket(user_id, QrcodeTicket.PERMANENT)
            return qrcode_ticket.ticket
        except:
            return _get_ticket(user_id)

    else:
        try:
            qrcode_ticket = weixin_api.create_qrcode_ticket(user_id, QrcodeTicket.PERMANENT)
            return qrcode_ticket.ticket
        except:
            return ''