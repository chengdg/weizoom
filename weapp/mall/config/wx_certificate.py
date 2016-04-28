# -*- coding: utf-8 -*-
__author__ = 'zhaolei'

from core import resource
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from core.jsonresponse import create_response, JsonResponse
from mall import export
from mall.models import WxCertSettings
from core.upyun_util import upload_static_file
from datetime import datetime

import os,sys

FIRST_NAV = export.MALL_CONFIG_FIRST_NAV
class WXCertificate(resource.Resource):

    app = "mall2" # 资源所属的app名称
    resource = "weixin_certificate" # 资源名称

    @login_required
    def get(request):
        """
        响应GET
        """
        cert_name = key_name = False
        cert_setting = WxCertSettings.objects.filter(owner_id=request.manager.id)
        if cert_setting.count() > 0:
            cert_setting = cert_setting.first()
            cert_name = u'  (文件名：apiclient_cert.pem)' if cert_setting.cert_path != '' else ''
            key_name = u'  (文件名：apiclient_key.pem)' if cert_setting.key_path != '' else ''
        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_config_second_navs(request),
            'second_nav_name': export.MAIL_CONFIG_WEIXIN_NAV,
            'cert_name': cert_name,
            'key_name': key_name
        })
        return render_to_response('mall/editor/wx_cert_setting.html', c)


    @login_required
    def post(request):
        """
        处理上传文件
        @param request:
        @return:
        """
        upload_file = request.FILES.get('Filedata', None)
        owner_id = request.POST.get('owner_id', None)
        file_cat = request.POST.get('cat', None)
        response = create_response(500)
        if upload_file:
            try:
                file_path,up_path = WXCertificate.__save_cert_file( upload_file, owner_id)
            except:
                response.errMsg = u'保存文件出错'
                return response.get_response()
            cert_setting = WxCertSettings.objects.filter(owner_id=owner_id)
            if cert_setting.count() > 0:
                cert_setting = cert_setting.first()
                if 'cert_file' == file_cat:
                    cert_setting.cert_path=file_path
                    cert_setting.up_cert_path=up_path
                    cert_setting.save()
                elif 'key_file' == file_cat:
                    cert_setting.key_path=file_path
                    cert_setting.up_key_path=up_path
                    cert_setting.save()
            else:
                cert_setting = WxCertSettings.objects.create(
                    owner = request.user
                )
                if 'cert_file' == file_cat:
                    cert_setting.cert_path = file_path
                    cert_setting.up_cert_path=up_path
                elif 'key_file' == file_cat:
                    cert_setting.key_path = file_path
                    cert_setting.up_key_path=up_path
                cert_setting.save()
            response = create_response(200)
            response.data = file_path
        else:
            response.errMsg = u'文件错误'
        return response.get_response()

    @staticmethod
    def __save_cert_file( file, owner_id):
        """
        将上传的文件保存在每个resource的upload目录下
        @param res: 资源名
        @param file: 文件
        @param owner_id: webapp_owner_id
        @return: 文件保存路径
        """
        content = []
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        if file:
            for chunk in file.chunks():
                content.append(chunk)

        if settings.MODE == 'develop' or settings.MODE == 'test':
            dir_path = os.path.join(curr_dir,'upload','weixin_cert', 'owner_id_test'+owner_id)
        else:
            dir_path = os.path.join(curr_dir,'upload','weixin_cert', 'owner_id'+owner_id)


        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        file_path = os.path.join(dir_path, file.name)

        dst_file = open(file_path, 'wb')
        print >> dst_file, ''.join(content)
        dst_file.close()
         # upload_static_file(file_path, upyun_path, check_exist=False):
        try:
            up_path = upload_static_file(file_path,"/cert_files/owner_id"+ owner_id +"/"+ file.name,False)
        except:
            up_path = upload_static_file(file_path,"/cert_files/owner_id"+ owner_id +"/"+ file.name,False)
        return file_path,up_path