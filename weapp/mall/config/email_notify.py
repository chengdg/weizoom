#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from core import resource
from mall import export
from modules.member.models import IntegralStrategySttings
from account.models import OperationSettings, UserOrderNotifySettings

COUNT_PER_PAGE = 20
FIRST_NAV = export.MALL_CONFIG_FIRST_NAV

class EmailNotifyList(resource.Resource):
    app = "mall2"
    resource = "email_notify_list"

    @login_required
    def get(request):
        interal_strategy_settings = IntegralStrategySttings.objects.get(webapp_id=request.user_profile.webapp_id)
        operation_settings_objs = OperationSettings.objects.filter(owner=request.manager)
        if operation_settings_objs.count() == 0:
            operation_settings = OperationSettings.objects.create(owner=request.manager)
        else:
            operation_settings = operation_settings_objs[0]

        if UserOrderNotifySettings.objects.filter(user=request.manager).count() == 0:
            for index in range(5):
                UserOrderNotifySettings.objects.create(user=request.manager, status=index)

        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_config_second_navs(request),
            'second_nav_name': export.MALL_CONFIG_MAIL_NOTIFY_NAV,

            'interal_strategy_settings': interal_strategy_settings,
            'operation_settings': operation_settings,
            'notify_settings': UserOrderNotifySettings.objects.filter(user=request.manager)
        })

        return render_to_response('mall/editor/email_notify.html', c)


class EmailNotify(resource.Resource):
    app = "mall2"
    resource = "email_notify"

    @login_required
    def get(request):
        status = request.GET.get('status', None)
        notify_settings = UserOrderNotifySettings.objects.filter(user=request.manager, status=status)
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

    @login_required
    def post(request):
        status = request.GET.get('status', None)
        emails = request.POST.get('emails', '')
        member_ids = request.POST.get('member_ids', '')
        if UserOrderNotifySettings.objects.filter(user=request.manager, status=status).count() > 0:
            UserOrderNotifySettings.objects.filter(user=request.manager, status=status).update(emails=emails, black_member_ids=member_ids)
        else:
            UserOrderNotifySettings.objects.create(status=status, black_member_ids=member_ids, emails=emails, user=request.manager)

        return HttpResponseRedirect('/mall2/email_notify_list/')