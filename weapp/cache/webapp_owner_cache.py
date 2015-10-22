# -*- coding: utf-8 -*-
from __future__ import absolute_import

from utils import cache_util
import cache
from mall import models as mall_models
from mall.promotion import models as promotion_models
from modules.member import models as member_models
from weixin.user import models as weixin_user_models
from webapp import models as webapp_models
from account import models as account_models
from termite2 import models as termite2_models

from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_error, watchdog_warning
from market_tools.tools.weizoom_card.models import AccountHasWeizoomCardPermissions
from weixin.user.module_api import get_mp_qrcode_img

local_cache = {}


def get_webapp_owner_info_from_db(webapp_owner_id):
    def inner_func():
        #user profile
        user_profile = account_models.UserProfile.objects.get(user_id=webapp_owner_id)
        webapp_id = user_profile.webapp_id

        #mpuser preview info
        try:
            mpuser = weixin_user_models.WeixinMpUser.objects.get(owner_id=webapp_owner_id)
            mpuser_preview_info = weixin_user_models.MpuserPreviewInfo.objects.get(mpuser=mpuser)
            try:
                weixin_mp_user_access_token = weixin_user_models.WeixinMpUserAccessToken.objects.get(mpuser=mpuser)
            except:
                weixin_mp_user_access_token = weixin_user_models.WeixinMpUserAccessToken()
        except:
            error_msg = u"获得user('{}')对应的mpuser_preview_info构建cache失败, cause:\n{}"\
                    .format(webapp_owner_id, unicode_full_stack())
            watchdog_warning(error_msg, user_id=webapp_owner_id)
            mpuser_preview_info = weixin_user_models.MpuserPreviewInfo()
            weixin_mp_user_access_token = weixin_user_models.WeixinMpUserAccessToken()
            mpuser = weixin_user_models.WeixinMpUser()

        #webapp
        try:
            webapp = webapp_models.WebApp.objects.get(owner_id=webapp_owner_id)
        except:
            error_msg = u"获得user('{}')对应的webapp构建cache失败, cause:\n{}"\
                    .format(webapp_owner_id, unicode_full_stack())
            watchdog_error(error_msg, user_id=webapp_owner_id, noraise=True)
            webapp = webapp_models.WebApp()

        #integral strategy
        try:
            integral_strategy_settings = member_models.IntegralStrategySttings.objects.get(webapp_id=webapp_id)
        except:
            error_msg = u"获得user('{}')对应的IntegralStrategySttings构建cache失败, cause:\n{}"\
                    .format(webapp_owner_id, unicode_full_stack())
            watchdog_error(error_msg, user_id=webapp_owner_id, noraise=True)
            integral_strategy_settings = member_models.IntegralStrategySttings()

        #member grade
        try:
            member_grades = [member_grade.to_dict() for member_grade in member_models.MemberGrade.objects.filter(webapp_id=webapp_id)]
        except:
            error_msg = u"获得user('{}')对应的MemberGrade构建cache失败, cause:\n{}"\
                    .format(webapp_owner_id, unicode_full_stack())
            watchdog_error(error_msg, user_id=webapp_owner_id, noraise=True)
            member_grades = []

        #pay interface
        try:
            pay_interfaces = [pay_interface.to_dict() for pay_interface in mall_models.PayInterface.objects.filter(owner_id=webapp_owner_id)]
        except:
            error_msg = u"获得user('{}')对应的PayInterface构建cache失败, cause:\n{}"\
                    .format(webapp_owner_id, unicode_full_stack())
            watchdog_error(error_msg, user_id=webapp_owner_id, noraise=True)
            pay_interfaces = []

        # 微众卡权限
        has_permission = AccountHasWeizoomCardPermissions.is_can_use_weizoom_card_by_owner_id(webapp_owner_id)

        # 公众号二维码
        qrcode_img = get_mp_qrcode_img(webapp_owner_id)
        try:
            operation_settings = account_models.OperationSettings.get_settings_for_user(webapp_owner_id)
        except:
            error_msg = u"获得user('{}')对应的OperationSettings构建cache失败, cause:\n{}"\
                    .format(webapp_owner_id, unicode_full_stack())
            watchdog_error(error_msg, user_id=webapp_owner_id, noraise=True)
            operation_settings = account_models.OperationSettings()
        #全局导航 ad by bert
        try:
            global_navbar = termite2_models.TemplateGlobalNavbar.get_object(webapp_owner_id)
        except:
            global_navbar = termite2_models.TemplateGlobalNavbar
        
        return {
            'value': {
                'weixin_mp_user_access_token': weixin_mp_user_access_token.to_dict(),
                "mpuser_preview_info": mpuser_preview_info.to_dict(),
                'webapp': webapp.to_dict(),
                'user_profile': user_profile.to_dict(),
                'mpuser': mpuser.to_dict(),
                'integral_strategy_settings': integral_strategy_settings.to_dict(),
                'member_grades': member_grades,
                'pay_interfaces': pay_interfaces,
                'has_permission': has_permission,
                'operation_settings':  operation_settings.to_dict(),
                'global_navbar': global_navbar.to_dict(),
                'qrcode_img': qrcode_img
            }
        }
    return inner_func

class Object(object):
    def __init__(self):
        pass


def __get_unship_order_count_from_db(key, webapp_id):
    from mall.models import belong_to, ORDER_STATUS_PAYED_NOT_SHIP

    def inner_func():
        count = belong_to(webapp_id).filter(status=ORDER_STATUS_PAYED_NOT_SHIP).count()
        return {
            'keys': [key],
            'value': count
        }
    return inner_func


def update_unship_order_count(instance, **kwargs):
    webapp_id = None
    if isinstance(instance, mall_models.Order):
        webapp_id = instance.webapp_id
    else:
        for order in instance:
            webapp_id = order.webapp_id
            break
    if webapp_id:
        key = 'webapp_unread_order_count_{wa:%s}' % webapp_id
        cache_util.delete_cache(key)


def get_unship_order_count_from_cache(webapp_id):
    key = 'webapp_unread_order_count_{wa:%s}' % webapp_id
    count = cache_util.get_from_cache(key, __get_unship_order_count_from_db(key, webapp_id))
    return count


def get_webapp_owner_info(webapp_owner_id):
    webapp_owner_info_key = 'webapp_owner_info_{wo:%s}' % webapp_owner_id
    red_envelope_key = 'red_envelope_{wo:%s}' % webapp_owner_id
    key_infos = [{
        'key': webapp_owner_info_key,
        'on_miss': get_webapp_owner_info_from_db(webapp_owner_id)
    },{
        'key': red_envelope_key,
        'on_miss': get_red_envelope_for_cache(webapp_owner_id)

    }]
    data = cache_util.get_many_from_cache(key_infos)
    red_envelope = data[red_envelope_key]
    if red_envelope != '1':
        red_envelope = promotion_models.RedEnvelopeRule.from_dict(red_envelope)
        # coupon_rule = red_envelope.coupon_rule
        # if coupon_rule:
        #     red_envelope.coupon_rule = promotion_models.CouponRule.from_dict(coupon_rule)
    data = data[webapp_owner_info_key]
    # data = cache_util.get_from_cache(key, get_webapp_owner_info_from_db(webapp_owner_id))

    obj = Object()
    obj.mpuser_preview_info = weixin_user_models.MpuserPreviewInfo.from_dict(data['mpuser_preview_info'])
    obj.app = webapp_models.WebApp.from_dict(data['webapp'])

    obj.user_profile = account_models.UserProfile.from_dict(data['user_profile'])
    obj.mpuser = weixin_user_models.WeixinMpUser.from_dict(data['mpuser'])
    obj.weixin_mp_user_access_token = weixin_user_models.WeixinMpUserAccessToken.from_dict(data['weixin_mp_user_access_token'])
    obj.integral_strategy_settings = member_models.IntegralStrategySttings.from_dict(data['integral_strategy_settings'])
    obj.member_grades = member_models.MemberGrade.from_list(data['member_grades'])
    obj.member2grade = dict([(grade.id, grade) for grade in obj.member_grades])
    obj.pay_interfaces = mall_models.PayInterface.from_list(data['pay_interfaces'])
    obj.is_weizoom_card_permission = data['has_permission']
    obj.qrcode_img = data['qrcode_img']
    obj.operation_settings = account_models.OperationSettings.from_dict(data['operation_settings'])
    obj.red_envelope = red_envelope
    obj.global_navbar = termite2_models.TemplateGlobalNavbar.from_dict(data['global_navbar'])
    return obj



from django.dispatch.dispatcher import receiver
from django.db.models import signals
from weapp.hack_django import post_update_signal
#######################################################################
# update_webapp_owner_info_cache: 更新webapp_owner_info cache
#     该函数会在后台编辑时被调用
#######################################################################
def update_webapp_owner_info_cache_with_login(instance, **kwargs):
    if isinstance(instance, account_models.UserProfile):
        webapp_owner_id = instance.user_id
    elif isinstance(instance, AccountHasWeizoomCardPermissions):
        webapp_owner_id = instance.owner_id
    else:
        if cache.request.user_profile:
            webapp_owner_id = cache.request.user_profile.user_id
        else:
            return
    key = 'webapp_owner_info_{wo:%s}' % webapp_owner_id
    cache_util.delete_cache(key)
    get_webapp_owner_info(webapp_owner_id)


post_update_signal.connect(update_webapp_owner_info_cache_with_login, sender=weixin_user_models.MpuserPreviewInfo, dispatch_uid = "mpuser_preview_info.update")
signals.post_save.connect(update_webapp_owner_info_cache_with_login, sender=weixin_user_models.MpuserPreviewInfo, dispatch_uid = "mpuser_preview_info.save")
post_update_signal.connect(update_webapp_owner_info_cache_with_login, sender=member_models.IntegralStrategySttings, dispatch_uid = "integral_strategy_settings.update")
signals.post_save.connect(update_webapp_owner_info_cache_with_login, sender=member_models.IntegralStrategySttings, dispatch_uid = "integral_strategy_settings.save")
post_update_signal.connect(update_webapp_owner_info_cache_with_login, sender=member_models.MemberGrade, dispatch_uid = "member_grade.update")
signals.post_save.connect(update_webapp_owner_info_cache_with_login, sender=member_models.MemberGrade, dispatch_uid = "member_grade.save")
post_update_signal.connect(update_webapp_owner_info_cache_with_login, sender=webapp_models.WebApp, dispatch_uid = "webapp.update")
post_update_signal.connect(update_webapp_owner_info_cache_with_login, sender=account_models.UserProfile, dispatch_uid = "user_profile.update")
post_update_signal.connect(update_webapp_owner_info_cache_with_login, sender=weixin_user_models.WeixinMpUser, dispatch_uid = "weixin_mp_user.update")
#pay interface
post_update_signal.connect(update_webapp_owner_info_cache_with_login, sender=mall_models.PayInterface, dispatch_uid = "PayInterface.update")
signals.post_save.connect(update_webapp_owner_info_cache_with_login, sender=mall_models.PayInterface, dispatch_uid = "PayInterface.save")

post_update_signal.connect(update_webapp_owner_info_cache_with_login, sender=account_models.OperationSettings, dispatch_uid = "OperationSettings.update")
signals.post_save.connect(update_webapp_owner_info_cache_with_login, sender=account_models.OperationSettings, dispatch_uid = "OperationSettings.save")
signals.post_save.connect(
                          update_webapp_owner_info_cache_with_login,
                          sender=AccountHasWeizoomCardPermissions,
                          dispatch_uid="accounthwzcp.save")
post_update_signal.connect(update_webapp_owner_info_cache_with_login,
                           sender=AccountHasWeizoomCardPermissions,
                           dispatch_uid="accountwzcp.update")

post_update_signal.connect(update_unship_order_count, sender=mall_models.Order,
                           dispatch_uid="webapp_unread_order_count.update")
signals.post_save.connect(update_unship_order_count, sender=mall_models.Order,
                          dispatch_uid="webapp_unread_order_count.save")

post_update_signal.connect(update_webapp_owner_info_cache_with_login, sender=termite2_models.TemplateGlobalNavbar,
                           dispatch_uid="termite2_models.TemplateGlobalNavbar.update")
signals.post_save.connect(update_webapp_owner_info_cache_with_login, sender=termite2_models.TemplateGlobalNavbar,
                          dispatch_uid="termite2_models.TemplateGlobalNavbar.save")


def get_red_envelope_for_cache(owner_id):
    def inner_func():
        red_envelope = promotion_models.RedEnvelopeRule.objects.filter(owner_id=owner_id, status=True,receive_method=False)
        result = {}
        if len(red_envelope):
            red_envelope = red_envelope[0]
            coupon_rule = promotion_models.CouponRule.objects.filter(id=red_envelope.coupon_rule_id)
            if len(coupon_rule) and coupon_rule[0].remained_count > 0:
                red_envelope.coupon_rule = {'end_date': coupon_rule[0].end_date}
            else:
                red_envelope.coupon_rule = None
            result = red_envelope.to_dict('coupon_rule')
        return { 'value' : result }
    return inner_func

def update_red_envelope_cache(instance, **kwargs):
    if not instance:
        return
    key = None
    if len(instance):
        if isinstance(instance[0], promotion_models.RedEnvelopeRule):
            # 更新红包分享规则状态时，清空红包分享缓存
            key = 'red_envelope_{wo:%s}' % instance[0].owner_id
        elif isinstance(instance[0], promotion_models.CouponRule) and (
            instance[0].remained_count <= 0 or not instance[0].is_active):
            # 更新优惠券规则库存数量小于等于0时，清空红包分享缓存
            key = 'red_envelope_{wo:%s}' % instance[0].owner_id
    if key:
        cache_util.delete_cache(key)
    # if instance.status:

post_update_signal.connect(update_red_envelope_cache, sender=promotion_models.CouponRule, dispatch_uid="coupon_rule.update_red_envelope.save")
# 新建红包规则，默认状态为关闭
# signals.post_save.connect(update_red_envelope_cache, sender=promotion_models.RedEnvelopeRule, dispatch_uid="red_envelope.save")
post_update_signal.connect(update_red_envelope_cache, sender=promotion_models.RedEnvelopeRule, dispatch_uid="red_envelope.update")
