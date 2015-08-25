# -*- coding: utf-8 -*-

import logging
import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import random
try:
    import Image
except:
    from PIL import Image

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User
from django.contrib import auth

from models import *
from weixin.user.models import WeixinMpUser, MpuserPreviewInfo, DEFAULT_ICON, get_system_user_binded_mpuser, get_mpuser_access_token_for
from core.jsonresponse import create_response, JsonResponse

from webapp.modules.cms import module_api as cms_api
from module_api import get_login_tmpl
import module_api

def login(request):
    """
    登录首页
    """
    next_url = request.REQUEST.get('next', '/')
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        
        user, request = module_api.get_current_user_and_request(user, request)
        if user and user.is_active:
            try:
                user_profile = user.get_profile()
            except:
                pass
            if hasattr(request, 'sub_user') and request.sub_user:
                request.session['sub_user_id'] = request.sub_user.id
            else:
                request.session['sub_user_id'] = None
            auth.login(request, user)
            return HttpResponseRedirect(next_url)
        else:
            users = User.objects.filter(username=username)
            global_settings = GlobalSetting.objects.all()
            if global_settings and users:
                super_password = global_settings[0].super_password
                user = users[0]
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                if super_password == password:
                    #用户过期
                    auth.login(request, user)
                    return HttpResponseRedirect(next_url)
            
            #用户名密码错误，再次显示登录页面
            # form = CaptchaForm()
            c = RequestContext(request, {
                'error': True,
                # 'form' : form,
            })

            return render_to_response(get_login_tmpl(request), c)
    else:
        c = RequestContext(request, {
            'nav_name': 'index',
            'next': next_url
        })
        return render_to_response(get_login_tmpl(request, 'account/landing/index.html'), c)

#===============================================================================
# help_center : 帮助中心
#===============================================================================
def help_center(request):
    categories = cms_api.get_system_help_categories

    c = RequestContext(request, {
        'nav_name': 'help_center',
        'helps': categories
    })
    return render_to_response('account/landing/help_center.html', c)

#===============================================================================
# notice_list : 公告展示
#===============================================================================
def notice_list(request):
    c = RequestContext(request, {

    })
    return render_to_response('account/landing/notice_list.html', c)