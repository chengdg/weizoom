#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from core import resource
from mall import export
from account.models import OperationSettings, UserOrderNotifySettings
from utils import cache_util
from core.jsonresponse import create_response

COUNT_PER_PAGE = 20
FIRST_NAV = export.MALL_CONFIG_FIRST_NAV

class EmailNotifyList(resource.Resource):
    app = "mall2"
    resource = "email_notify_list"

    @login_required
    def get(request):
        operation_settings_objs = OperationSettings.objects.filter(owner=request.manager)
        if operation_settings_objs.count() == 0:
            operation_settings = OperationSettings.objects.create(owner=request.manager)
        else:
            operation_settings = operation_settings_objs[0]

        if UserOrderNotifySettings.objects.filter(user=request.manager).count() == 0:
            for index in range(5):
                user_order_setting = UserOrderNotifySettings.objects.create(user=request.manager, status=index)
                notify_setting_key = "notify_settings_{wo:%s}_{status:%s}" % (request.user.id,index)
                cache_util.add_mhash_to_redis(notify_setting_key,user_order_setting.to_dict())
        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_config_second_navs(request),
            'second_nav_name': export.MALL_CONFIG_MAIL_NOTIFY_NAV,
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
        notify_setting_key = "notify_settings_{wo:%s}_{status:%s}" % (request.manager.id,status)
        if UserOrderNotifySettings.objects.filter(user=request.manager, status=status).count() > 0:
            UserOrderNotifySettings.objects.filter(user=request.manager, status=status).update(emails=emails, black_member_ids=member_ids)
        else:
			UserOrderNotifySettings.objects.create(status=status, black_member_ids=member_ids, emails=emails, user=request.manager)
        user_order_setting = UserOrderNotifySettings.objects.filter(user=request.manager, status=status).get()
        # todo zhaolei 兼容性写法，本来可以只同步字段的，但是因为创建的时候不一定都存在
        cache_util.add_mhash_to_redis(notify_setting_key,user_order_setting.to_dict())
        return HttpResponseRedirect('/mall2/email_notify_list/')

    @login_required
    def api_put(request):
        id = request.POST.get('id', None)
        status = request.POST.get('status', None)
        if id and status and status in ("1","0"):
            user_notify_setting = UserOrderNotifySettings.objects.filter(id=id).get()
            if user_notify_setting:
                user_notify_setting.is_active= True if status=="1" else False
                notify_setting_key = "notify_settings_{wo:%s}_{status:%s}" % (user_notify_setting.user_id,user_notify_setting.status)
                cache_util.add_mhash_to_redis(notify_setting_key,user_notify_setting.to_dict())
                user_notify_setting.save()
                response = create_response(200)
            else:
                response = create_response(500)
        else:
            response = create_response(500)
        return response.get_response()