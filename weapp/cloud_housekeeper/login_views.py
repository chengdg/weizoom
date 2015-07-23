# -*- coding: utf-8 -*-

__author__ = 'liupeiyu'

import json
import random, string

from core import resource
from core.jsonresponse import create_response, JsonResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse

from django.conf import settings
from cloud_required import cloud_housekeeper_required
from models import CloudUser
from core.send_phone_msg import send_phone_captcha as api_send_phone_captcha
import cloud_user_util as cloud_user_util

class CloudLogin(resource.Resource):
    """
    云管家登陆
    """
    app = 'cloud_housekeeper'
    resource = 'login'

    # @cloud_housekeeper_required
    def get(request):
        """
        登陆页面
        """
        c = RequestContext(request, {
            'page_title': '云管家'
        })
        return render_to_response('cloud_housekeeper/login.html', c)


    def api_post(request):
        phone_number = request.POST.get('phone_number', '')
        captcha = request.POST.get('captcha', '')
        data = CloudUser(phone_number=phone_number, captcha=captcha).is_login_success()
        
        response = create_response(data['code'])
        response.data = {
            "msg" : data['msg']
        }
        response = response.get_response()
        if data['code'] == 200:
            cloud_user_util.save_session_cloud_user(response, data['user_id'])

        return response


class CloudLogout(resource.Resource):
    """
    云管家退出
    """
    app = 'cloud_housekeeper'
    resource = 'logout'

    # @cloud_housekeeper_required
    def get(request):
        """
        退出
        """
        response = HttpResponseRedirect('/cloud_housekeeper/login/')
        cloud_user_util.logout_cloud_user(response)
        return response




class CloudLoginCaptcha(resource.Resource):
    """
    云管家验证码
    """
    app = 'cloud_housekeeper'
    resource = 'captcha'

    def api_get(request):
        """
        获取验证码
        """
        phone_number = request.GET.get('phone_number', '')
        try:
            user = CloudUser.objects.get(phone_number=phone_number)
        except:
            response = create_response(501)
            response.data = {
                "msg" : u'手机号码不存在'
            }
            return response.get_response()


        result, captcha = send_phone_msg(phone_number)
        if result:
            user.captcha = captcha
            user.save()
            request.cloud_user = user
            response = create_response(200)
            response.data = {
                "msg" : u'发送成功！'
            }
        else:
            response = create_response(502)
            response.data = {
                "msg" : u'验证吗发送失败！'
            }
        return response.get_response()
        


MSG_CONTENT = u"您的验证码为[%s]，请不要泄露给任何人【%s】"
def send_phone_msg(phone_number, company_name=u'微众传媒'):
    """
    send_phone_msg: 发送手机验证码
    """
    captcha = ''.join(random.sample(string.digits, 5))
    content = MSG_CONTENT % (captcha, company_name)
    result = api_send_phone_captcha(phone_number, content)
    return result, captcha