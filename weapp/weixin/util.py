# -*- coding: utf-8 -*-

__author__ = 'Eugene'

import hashlib
import datetime
from BeautifulSoup import BeautifulSoup

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404
from django.contrib.auth.models import User
from django.db.models import Q

from core.exceptionutil import unicode_full_stack
from core.upyun_util import upload_qrcode_url_to_upyun
from watchdog.utils import watchdog_fatal, watchdog_error
from weixin.user.models import *
from weixin.user.util import get_component_info_from
from weixin.message_util.WXBizMsgCrypt import WXBizMsgCrypt
from account.models import UserProfile


def get_query_auth(weixin_api=None, component_info=None, auth_code=None):
    """
    使用授权码换取公众号的授权信息
    """
    try:
        result = weixin_api.api_query_auth(component_info.app_id, auth_code)
        mp_user = None
        if result.has_key('authorization_info'):
            authorization_info = result['authorization_info']
            func_info_ids = []
            func_info = authorization_info['func_info']
            if isinstance(func_info, list):
                for funcscope_category in func_info:
                    funcscope_category_id = funcscope_category.get('funcscope_category', None)
                    if funcscope_category_id:
                        func_info_ids.append(str(funcscope_category_id.get('id')))
            authorizer_appid = authorization_info['authorizer_appid']
            authorizer_access_token=authorization_info['authorizer_access_token']
            authorizer_refresh_token=authorization_info['authorizer_refresh_token']

            if authorizer_appid:
                ComponentAuthedAppid.objects.filter(user_id=user_id).update(
                    authorizer_appid=authorizer_appid,
                    authorizer_access_token=authorizer_access_token,
                    authorizer_refresh_token=authorizer_refresh_token,
                    last_update_time=datetime.now(),
                    func_info = ','.join(func_info_ids),
                    is_active = True
                    )

                if WeixinMpUser.objects.filter(owner_id=user_id).count() > 0:
                    mp_user = WeixinMpUser.objects.filter(owner_id=user_id)[0]
                else:
                    mp_user = WeixinMpUser.objects.create(owner_id=user_id)

                if WeixinMpUserAccessToken.objects.filter(mpuser = mp_user).count() > 0:
                    WeixinMpUserAccessToken.objects.filter(mpuser = mp_user).update(update_time=datetime.datetime.now(), access_token=authorizer_access_token, is_active=True)
                else:
                    WeixinMpUserAccessToken.objects.create(
                        mpuser = mp_user,
                        app_id = authorizer_appid,
                        app_secret = '',
                        access_token = authorizer_access_token,
                        update_time=datetime.now()
                    )
                """
                处理公众号绑定过其它系统帐号情况
                """
                component_authed_appids = ComponentAuthedAppid.objects.filter(~Q(user_id=request.user.id), authorizer_appid=authorizer_appid)
                update_user_ids = [appid.user_id for appid in component_authed_appids]
                component_authed_appids.update(is_active=False)
                UserProfile.objects.filter(user_id__in=update_user_ids).update(is_mp_registered=False)
                return "success", mp_user
    except:
        return "error", None

def refresh_auth_token(auth_appid=None, weixin_api=None, component=None):
    """
    获取（刷新）授权公众号的令牌
    """
    user_id = auth_appid.user_id
    if auth_appid.is_active is False:
        UserProfile.objects.filter(user_id=user_id).update(is_mp_registered=False)
        return False, None

    result = weixin_api.api_authorizer_token(component.app_id, auth_appid.authorizer_appid, auth_appid.authorizer_refresh_token)

    if result.has_key('errcode') and (result['errcode'] == -1 or result['errcode'] == 995995):
        return 'error', None
    if result.has_key('authorizer_access_token'):
        authorizer_access_token = result['authorizer_access_token']
        auth_appid.authorizer_access_token = result['authorizer_access_token']
        auth_appid.authorizer_refresh_token = result['authorizer_refresh_token']
        auth_appid.last_update_time = datetime.now()
        auth_appid.save()

        if WeixinMpUser.objects.filter(owner_id=user_id).count() > 0:
            mp_user = WeixinMpUser.objects.filter(owner_id=user_id)[0]
        else:
            mp_user = WeixinMpUser.objects.create(owner_id=user_id)

        if WeixinMpUserAccessToken.objects.filter(mpuser = mp_user).count() > 0:
            WeixinMpUserAccessToken.objects.filter(mpuser = mp_user).update(update_time=datetime.now(), access_token=authorizer_access_token, is_active=True, app_id = auth_appid.authorizer_appid)
        else:
            WeixinMpUserAccessToken.objects.filter(mpuser = mp_user).create(
                mpuser = mp_user,
                app_id = auth_appid.authorizer_appid,
                app_secret = '',
                access_token = authorizer_access_token
            )
        return True, mp_user
    else:
        print "----111-----", result
        return False, None

def get_authorizer_info(auth_appid=None, weixin_api=None, component=None, mp_user=None):
    """
    获取授权方信息
    """
    user_id = auth_appid.user_id
    try:
        result = weixin_api.api_get_authorizer_info(component.app_id,auth_appid.authorizer_appid)

        if result.has_key('authorizer_info'):
            nick_name = result['authorizer_info'].get('nick_name', '')
            head_img = result['authorizer_info'].get('head_img', '')
            service_type_info = result['authorizer_info']['service_type_info'].get('id', '')
            verify_type_info = result['authorizer_info']['verify_type_info'].get('id', '')
            user_name = result['authorizer_info'].get('user_name', '')
            alias = result['authorizer_info'].get('alias', '')
            qrcode_url = result['authorizer_info'].get('qrcode_url','')

            #authorization_info
            appid = result['authorization_info'].get('authorizer_appid', '')

            func_info_ids = []
            func_info = result['authorization_info'].get('func_info')
            if  isinstance(func_info, list):
                for funcscope_category in func_info:
                    funcscope_category_id = funcscope_category.get('funcscope_category', None)
                    if funcscope_category_id:
                        func_info_ids.append(str(funcscope_category_id.get('id')))


            if ComponentAuthedAppidInfo.objects.filter(auth_appid=auth_appid).count() > 0:
                auth_appid_info = ComponentAuthedAppidInfo.objects.filter(auth_appid=auth_appid)[0]
                if auth_appid_info.qrcode_url.find('mmbiz.qpic.cn') > -1 or auth_appid_info.nick_name != nick_name:
                    try:
                        qrcode_url = upload_qrcode_url_to_upyun(qrcode_url, auth_appid.authorizer_appid)
                    except:
                        print '>>>>>>>>>>>>>>>>>>>>upload_qrcode_url_to_upyun error'
                else:
                    qrcode_url = auth_appid_info.qrcode_url

                ComponentAuthedAppidInfo.objects.filter(auth_appid=auth_appid).update(
                    nick_name=nick_name,
                    head_img=head_img,
                    service_type_info=service_type_info,
                    verify_type_info=verify_type_info,
                    user_name=user_name,
                    alias=alias,
                    qrcode_url=qrcode_url,
                    appid=appid,
                    func_info=','.join(func_info_ids)
                    )

            else:
                try:
                    watchdog_info('call weixin api: api_get_authorizer_info , result:{}'.format(result))
                    qrcode_url = upload_qrcode_url_to_upyun(qrcode_url, auth_appid.authorizer_appid)
                except:
                    print '>>>>>>>>>>>>>>>>>>>>upload_qrcode_url_to_upyun error'
                ComponentAuthedAppidInfo.objects.create(
                    auth_appid=auth_appid,
                    nick_name=nick_name,
                    head_img=head_img,
                    service_type_info=service_type_info,
                    verify_type_info=verify_type_info,
                    user_name=user_name,
                    alias=alias,
                    qrcode_url=qrcode_url,
                    appid=appid,
                    func_info=','.join(func_info_ids)
                    )

            is_service = False

            if int(service_type_info) > 1:
                is_service = True
            is_certified = False
            if int(verify_type_info) > -1:
                is_certified = True

            WeixinMpUser.objects.filter(owner_id=user_id).update(is_service=is_service, is_certified=is_certified, is_active=True)

            if mp_user:
                if MpuserPreviewInfo.objects.filter(mpuser=mp_user).count() > 0:
                    MpuserPreviewInfo.objects.filter(mpuser=mp_user).update(image_path=head_img, name=nick_name)
                else:
                    MpuserPreviewInfo.objects.create(mpuser=mp_user,image_path=head_img, name=nick_name)
            user_profile = UserProfile.objects.get(user_id=user_id)
            if is_service:
                if (user_profile.is_mp_registered is False) or (user_profile.is_oauth is False):
                    UserProfile.objects.filter(user_id=user_id).update(is_mp_registered=True, is_oauth=True)
            else:
                if user_profile.is_oauth:
                    UserProfile.objects.filter(user_id=user_id).update(is_mp_registered=True, is_oauth=False)
    except:
        notify_msg = u"处理公众号mp相关信息, cause:\n{}".format(unicode_full_stack())
        watchdog_error(notify_msg)