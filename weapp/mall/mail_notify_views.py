# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group, Permission

import models as mall_models
from models import *
import export
from core.restful_url_route import *

from modules.member.models import IntegralStrategySttings, IntegralStrategySttingsDetail
from account.models import OperationSettings, UserOrderNotifySettings


COUNT_PER_PAGE = 20
FIRST_NAV = export.MALL_CONFIG_FIRST_NAV


########################################################################
# get_email_notify: 获得运营邮件通知配置列表
########################################################################
@view(app='mall', resource='email_notify', action='get')
@login_required
def get_email_notify(request):
    interal_strategy_settings = IntegralStrategySttings.objects.get(webapp_id=request.user_profile.webapp_id)
    operation_settings_objs = OperationSettings.objects.filter(owner=request.user)
    if operation_settings_objs.count() == 0:
        operation_settings = OperationSettings.objects.create(owner=request.user)
    else:
        operation_settings = operation_settings_objs[0]

    if UserOrderNotifySettings.objects.filter(user=request.user).count() == 0:
        for index in range(5):
            UserOrderNotifySettings.objects.create(user=request.user, status=index)

    c = RequestContext(request, {
        'first_nav_name': FIRST_NAV,
        'second_navs': export.get_config_second_navs(request),
        'second_nav_name': export.MALL_CONFIG_MAIL_NOTIFY_NAV,

        'interal_strategy_settings': interal_strategy_settings,
        'operation_settings': operation_settings,
        'notify_settings': UserOrderNotifySettings.objects.filter(user=request.user)
    })

    return render_to_response('mall/editor/email_notify.html', c)

########################################################################
# edit_email_notify: 配置运营邮件通知信息
########################################################################
@view(app='mall', resource='email_notify', action='edit')
@login_required
def edit_email_notify(request):
    status = request.GET.get('status', None)
    if request.method == 'POST':
        emails = request.POST.get('emails', '')
        member_ids = request.POST.get('member_ids', '')
        if UserOrderNotifySettings.objects.filter(user=request.user, status=status).count() > 0:
            UserOrderNotifySettings.objects.filter(user=request.user, status=status).update(emails=emails, black_member_ids=member_ids)
        else:
            UserOrderNotifySettings.objects.create(status=status, black_member_ids=member_ids, emails=emails, user=request.user)

        return HttpResponseRedirect('/mall/email_notify/get/')
    else:
        notify_settings = UserOrderNotifySettings.objects.filter(user=request.user, status=status)
        if notify_settings.count() > 0:
            notify_setting = notify_settings[0]
        else:
            notify_setting = None

    c = RequestContext(request, {
        'first_nav_name': FIRST_NAV,
        'second_navs': export.get_config_second_navs(request),
        'second_nav_name': export.MALL_CONFIG_MAIL_NOTIFY_NAV,
        'notify_setting': notify_setting,
    })
    return render_to_response('mall/editor/edit_email_notify_setting.html', c)