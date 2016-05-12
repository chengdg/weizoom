# -*- coding: utf-8 -*-

"""@package mall.product_pay_interface_views
支付接口模块的页面的实现文件

目前有以下三种支付接口
 - 货到付款
 - 微信支付
 - 微众卡

每一种类型的支付接口都有两部分信息:
 - 支付接口的通用信息：这部分在PayInterface model中实现
 - 支付接口的特定信息：比如微信支付需要微信的一些认证信息，这些信息在各自的Config model中实现，比如对于微信支付，就是UserWeixinPayOrderConfig，在PayInterface model中，有一个属性related_config_id，指向特定的信息
"""

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from mall.models import PayInterface, PAY_INTERFACE_WEIXIN_PAY, UserWeixinPayOrderConfig, PAY_INTERFACE_ALIPAY, \
    UserAlipayOrderConfig, VALID_PAY_INTERFACES, PAYTYPE2NAME, PAY_INTERFACE_WEIZOOM_COIN
from mall import export
from core import resource
from core.jsonresponse import create_response
from weixin.user.models import ComponentAuthedAppid

COUNT_PER_PAGE = 20
FIRST_NAV = export.MALL_CONFIG_FIRST_NAV


class PayInterfaceList(resource.Resource):
    """
    支付接口列表
    """
    app = "mall2"
    resource = "pay_interface_list"

    @login_required
    def get(request):
        """
        支付接口列表页面
        """
        # if PayInterface.objects.filter(owner=request.manager).count() == 0:
        # #初始化所有的支付接口
        # for pay_interface_type in VALID_PAY_INTERFACES:
        # PayInterface.objects.create(
        # owner = request.manager,
        # type = pay_interface_type,
        # description = '',
        # 			is_active = False
        # 		)
        # else:

        pay_interface_types = [pay_interface.type for pay_interface in
                               PayInterface.objects.filter(owner=request.manager)]

        for pay_type_id in VALID_PAY_INTERFACES:
            if pay_type_id not in pay_interface_types:
                PayInterface.objects.create(
                    owner=request.manager,
                    type=pay_type_id,
                    description='',
                    is_active=False
                )

        pay_interfaces = list(PayInterface.objects.filter(owner=request.manager).exclude(type=PAY_INTERFACE_WEIZOOM_COIN))

        # pay_interfaces = filter(lambda pay_interface: pay_interface.type != PAY_INTERFACE_WEIZOOM_COIN, pay_interfaces)

        for pay_interface in pay_interfaces:
            pay_interface.name = PAYTYPE2NAME[pay_interface.type]
            if pay_interface.type in [PAY_INTERFACE_WEIXIN_PAY,
                                      PAY_INTERFACE_ALIPAY] and pay_interface.related_config_id == 0:
                pay_interface.should_create_related_config = True
            else:
                pay_interface.should_create_related_config = False

            #获取接口对应的配置项
            if pay_interface.type == PAY_INTERFACE_WEIXIN_PAY and pay_interface.related_config_id != 0:
                related_config = UserWeixinPayOrderConfig.objects.get(owner=request.manager,
                                                                      id=pay_interface.related_config_id)
                configs = []
                if related_config.pay_version == 0:
                    configs = [{
                                   "name": u"接口版本", "value": "v2"
                               }, {
                                   "name": u"AppID", "value": related_config.app_id
                               }, {
                                   "name": u"合作商户ID", "value": related_config.partner_id
                               }, {
                                   "name": u"合作商户密钥", "value": related_config.partner_key
                               }, {
                                   "name": u"支付专用签名串", "value": related_config.paysign_key
                               }]
                else:
                    configs = [{
                                   "name": u"接口版本", "value": "v3"
                               }, {
                                   "name": u"AppID", "value": related_config.app_id
                               }, {
                                   "name": u"商户号MCHID", "value": related_config.partner_id
                               }, {
                                   "name": u"APIKEY密钥", "value": related_config.partner_key
                               }]
                pay_interface.configs = configs

            if pay_interface.type == PAY_INTERFACE_ALIPAY and pay_interface.related_config_id != 0:
                related_config = UserAlipayOrderConfig.objects.get(owner=request.manager,
                                                                   id=pay_interface.related_config_id)
                print "",related_config.get_pay_version_display()
                configs = [
                           {
                               "name": u"接口版本", "value": related_config.get_pay_version_display()
                           },
                           {
                               "name": u"合作者身份ID", "value": related_config.partner
                           }, {
                               "name": u"交易安全检验码", "value": related_config.key
                           }, {
                               "name": u"支付宝公钥", "value": related_config.ali_public_key
                           }, {
                               "name": u"商户私钥", "value": related_config.private_key
                           }, {
                               "name": u"邮箱", "value": related_config.seller_email
                           }]
                pay_interface.configs = configs

        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_config_second_navs(request),
            'second_nav_name': export.MALL_CONFIG_PAYINTERFACE_NAV,
            'pay_interfaces': pay_interfaces,

        })

        return render_to_response('mall/editor/pay_interfaces.html', c)


class PayInterfaceInfo(resource.Resource):
    """
    支付接口
    """
    app = "mall2"
    resource = "pay_interface"


    @login_required
    def get(request):
        is_new = request.GET.get("is_new", None)
        pay_interface_id = request.GET['id']
        pay_interface = PayInterface.objects.get(id=pay_interface_id)


        try:
            component_authed_appid = ComponentAuthedAppid.objects.filter(user_id=request.manager.id)[0]
            component_info = component_authed_appid.component_info
            component_appid = component_info.app_id
        except:
            component_appid = ''

        if not is_new:
            if pay_interface.type == PAY_INTERFACE_WEIXIN_PAY:
                related_config = UserWeixinPayOrderConfig.objects.get(owner=request.manager,
                                                                      id=pay_interface.related_config_id)
            elif pay_interface.type == PAY_INTERFACE_ALIPAY:
                related_config = UserAlipayOrderConfig.objects.get(owner=request.manager,
                                                                   id=pay_interface.related_config_id)
            else:
                related_config = None
            pay_interface.related_config = related_config
        data =  {
            'first_nav_name': FIRST_NAV,
            'second_navs': export.get_config_second_navs(request),
            'second_nav_name': export.MALL_CONFIG_PAYINTERFACE_NAV,
            'pay_interface_id': pay_interface_id,
            'pay_interface': pay_interface,
            'is_new': is_new,
        }
        if component_appid != '':
            data['app_id'] = component_appid
        c = RequestContext(request,data)
        return render_to_response('mall/editor/edit_pay_interface.html', c)

    @login_required
    def put(request):
        """
        创建支付接口页面

        不同类型的支付接口需要调用不同的__add_{pay_interface}_config函数进行支付接口特定数据的创建
        """
        pay_interface_id = request.GET['id']
        pay_interface = PayInterface.objects.get(id=pay_interface_id)
        if request.POST:
            if pay_interface.type == PAY_INTERFACE_WEIXIN_PAY:
                related_config_id = _add_weixin_pay_config(request)
            elif pay_interface.type == PAY_INTERFACE_ALIPAY:
                related_config_id = _add_alipay_config(request)
            else:
                related_config_id = 0

            PayInterface.objects.filter(id=pay_interface_id).update(
                is_active=True,
                related_config_id=related_config_id
            )

            return HttpResponseRedirect('/mall2/pay_interface_list/')


    @login_required
    def post(request):
        """
        更新支付接口页面

        不同类型的支付接口需要调用不同的__update_{pay_interface}_config函数进行支付接口特定数据的创建

        @param id 支付接口id
        """
        pay_interface_id = request.GET['id']
        pay_interface = PayInterface.objects.get(id=pay_interface_id)

        if pay_interface.type == PAY_INTERFACE_WEIXIN_PAY:
            _update_weixin_pay_config(request, pay_interface)
        elif pay_interface.type == PAY_INTERFACE_ALIPAY:
            _update_alipay_config(request, pay_interface)
        else:
            pass
        return HttpResponseRedirect('/mall2/pay_interface_list/')

    @login_required
    def api_post(request):
        """
        启用支付接口

        Method: POST

        @param id 支付接口id
        @param is_enable 是否启用
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{.c}
             true: 启用
            false: 禁用
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
        pay_interface_id = int(request.POST['id'])
        is_enable = (request.POST['is_enable'] == 'true')
        PayInterface.objects.filter(id=pay_interface_id).update(is_active=is_enable)

        response = create_response(200)
        return response.get_response()


def _add_weixin_pay_config(request):
    """
    添加微信支付配置
    """
    if int(request.POST.get('pay_version', 0)) == 0:
        config = UserWeixinPayOrderConfig.objects.create(
            owner=request.manager,
            app_id=request.POST.get('app_id', '').strip(),
            pay_version=request.POST.get('pay_version', 0),
            partner_id=request.POST.get('partner_id', '').strip(),
            partner_key=request.POST.get('partner_key', '').strip(),
            paysign_key=request.POST.get('paysign_key', '').strip(),
        )
    else:
        config = UserWeixinPayOrderConfig.objects.create(
            owner=request.manager,
            app_id=request.POST.get('app_id', '').strip(),
            pay_version=request.POST.get('pay_version', 0),
            partner_id=request.POST.get('mch_id', '').strip(),
            partner_key=request.POST.get('api_key', '').strip(),
            paysign_key=request.POST.get('paysign_key', ''),
        )

    return config.id


def _add_alipay_config(request):
    config = UserAlipayOrderConfig.objects.create(
        owner=request.manager,
        partner=request.POST.get('partner', ''),
        key=request.POST.get('key', ''),
        private_key=request.POST.get('private_key', ''),
        ali_public_key=request.POST.get('ali_public_key', ''),
        seller_email=request.POST.get('seller_email', ''),
        pay_version=request.POST.get('ali_pay_version', '')
    )

    return config.id


def _update_weixin_pay_config(request, pay_interface):
    """
    更新微信支付配置
    """
    if int(request.POST.get('pay_version', 0)) == 0:
        UserWeixinPayOrderConfig.objects.filter(owner=request.manager, id=pay_interface.related_config_id).update(
            app_id=request.POST.get('app_id', '').strip(),
            pay_version=request.POST.get('pay_version', 0),
            partner_id=request.POST.get('partner_id', '').strip(),
            partner_key=request.POST.get('partner_key', '').strip(),
            paysign_key=request.POST.get('paysign_key', '').strip()
        )
    else:
        UserWeixinPayOrderConfig.objects.filter(owner=request.manager, id=pay_interface.related_config_id).update(
            app_id=request.POST.get('app_id', '').strip(),
            pay_version=request.POST.get('pay_version', 0),
            partner_id=request.POST.get('mch_id', '').strip(),
            partner_key=request.POST.get('api_key', '').strip(),
            paysign_key=request.POST.get('paysign_key', ''),
        )


def _update_alipay_config(request, pay_interface):
    config = UserAlipayOrderConfig.objects.filter(owner=request.manager, id=pay_interface.related_config_id).update(
        partner=request.POST.get('partner', ''),
        key=request.POST.get('key', ''),
        private_key=request.POST.get('private_key', ''),
        ali_public_key=request.POST.get('ali_public_key', ''),
        seller_email=request.POST.get('seller_email', ''),
        pay_version=request.POST.get('ali_pay_version', '')
    )

