# -*- coding: utf-8 -*-

__author__ = 'chuter'

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404
from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from django.conf import settings

from mall.models import Order, OrderHasProduct, PayInterface, Product
from account.models import UserWeixinPayOrderConfig
from weixin.user.models import WeixinMpUserAccessToken,ComponentAuthedAppid

def wxpay_index(request):
	order_id = request.GET.get('order_id', None)
	pay_interface_id = request.GET.get('pay_id', None)
	if not order_id or not pay_interface_id:
		return HttpResponse('invalid order_id')

	pay_interface = PayInterface.objects.get(id=pay_interface_id)
	weixin_pay_config = UserWeixinPayOrderConfig.objects.get(id=pay_interface.related_config_id)

	order = Order.objects.get(order_id=order_id)
	product_ids = [r.product_id for r in OrderHasProduct.objects.filter(order_id=order.id)]
	product_names = ','.join([product.name for product in Product.objects.filter(id__in=product_ids)])
	if len(product_names) > 127:
		product_names = product_names[:127]
	#add by bert 
	appid = weixin_pay_config.app_id
	try:
		component_authed_appid = ComponentAuthedAppid.objects.filter(authorizer_appid=appid, user_id=request.user_profile.user_id)[0]
		component_info = component_authed_appid.component_info
		component_appid = component_info.app_id
	except:
		component_appid = None
	

	c = RequestContext(request, {
		'domain': request.user_profile.host,
		'order_id': order_id,
		'webapp_owner_id': request.webapp_owner_id,
		'pay_interface_type': pay_interface.type,
		'pay_interface_related_config_id': pay_interface.related_config_id,
		'app_id': weixin_pay_config.app_id,
		'partner_id': weixin_pay_config.partner_id,
		'partner_key': weixin_pay_config.partner_key,
		'paysign_key': weixin_pay_config.paysign_key,
		'product_names': product_names,
		'user_ip': request.META['REMOTE_ADDR'],
		'total_fee_display': order.final_price,
		'total_fee': int(order.final_price * 100),	
		'app_secret': weixin_pay_config.app_secret,
		'hide_non_member_cover' : True,
		'callback_module': request.GET.get('callback_module', None),
		'component_appid': component_appid
	})
	if weixin_pay_config.pay_version == 0:
		return render_to_response('webapp/index.html', c)
	else:
		return render_to_response('webapp/index_v3.html', c)
	