# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json

from django.shortcuts import render_to_response, redirect
from django.core.cache import cache

from webapp.modules.mall import request_util
from webapp.modules.mall.models import *
from apps.register import mobile_view_func
from weshop.models import WeshipMemberRelation

from weixin.user.models import WeixinMpUser, WeixinMpUserAccessToken, WeixinUser

from account.social_account.models import SocialAccount
from account.models import UserProfile, OperationSettings
from modules.member.models import Member, MemberHasSocialAccount
from modules.member.member_identity_util import get_uuid

template_path_items = os.path.dirname(__file__).split(os.sep)
#TEMPLATE_DIR = '%s/templates/webapp' % template_path_items[-1]
TEMPLATE_DIR = 'weshop/templates/mall'


########################################################################
# get_productcategory: 显示“商品分类”页面
########################################################################
def get_productcategory(request):
	request.template_dir = TEMPLATE_DIR
	return request_util.get_productcategory(request)


########################################################################
# list_products: 显示"商品列表"页面
########################################################################
@mobile_view_func(resource='products', action='list')
def list_products(request):
	request.template_dir = TEMPLATE_DIR
	request.is_return_context = True
	context = request_util.list_products(request)
	# 按商品价格由低到高排序
	context.get('products').sort(lambda x,y: cmp(x.display_price, y.display_price))
	return render_to_response('%s/products.html' % request.template_dir, context)	


########################################################################
# get_product: 显示“商品详情”页面
########################################################################
@mobile_view_func(resource='product', action='get')
def get_product(request):
	rid = request.GET.get('rid', -1)
	product = Product.objects.filter(id=rid)

	if len(product) != 1:# 没有对应商品
		print 'len(product) is ', len(product)
		return _get_product_response(request)
	product = product[0]

	owner_id = request.webapp_owner_id
	if owner_id == product.owner_id:# 商城商品
		return _get_product_response(request)
	owner_id = product.owner_id
	request.not_weshop_product = True

	sessionid = get_uuid(request)
	openid = cache.get('%s_%s_openid' % (owner_id, sessionid))
	# print owner_id, sessionid, openid
	if not openid and request.user.is_from_weixin:# 第一次访问商户商品，需要获取商户openid
		mpuser = WeixinMpUser.objects.filter(owner_id = owner_id)[0]
		if not mpuser.is_certified or not mpuser.is_service:
			return _get_product_response(request)
		token = WeixinMpUserAccessToken.objects.filter(mpuser = mpuser)[0]
		code = request.GET.get('code', None)
		if not code:# 没有code需要跳转至微信授权页面
			redirect_url = 'http://%s%s?%s' % \
				(request.META.get('HTTP_HOST'), request.META.get('PATH_INFO'), request.META.get('QUERY_STRING'))
			# redirect_url = redirect_url.replace('/termite', '')
			weixin_auth_url = 'https://open.weixin.qq.com/connect/oauth2/authorize' \
				+ '?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=123#wechat_redirect' \
				% (token.app_id, urllib.quote(redirect_url).replace('/','%2F'))
			# print 'redirect to weixin_auth_url ', weixin_auth_url
			return redirect(weixin_auth_url)
		else:# 从微信认证接口跳回，从微信服务器去openid
			data = {
				'appid': token.app_id,
				'secret': token.app_secret,
				'code': code,
				'grant_type': 'authorization_code'
			}
			# print 'get openid param ', urllib.urlencode(data)
			url = 'https://api.weixin.qq.com/sns/oauth2/access_token?'
			try:
				req = urllib2.urlopen(url, urllib.urlencode(data))
				response_data = eval(req.read())
				# print 'get openid data ', response_data
				# response_data = response_data
				openid = response_data['openid']
				if request.social_account:
					if not WeshipMemberRelation.objects.filter(weshop_openid=request.social_account.openid,
						tenant_openid=openid, tenant_user_id=owner_id).count():
						print 'get new openid', openid, ';weshop openid', request.social_account.openid
						WeshipMemberRelation.objects.create(weshop_openid=request.social_account.openid,
							tenant_openid=openid, tenant_user_id=owner_id)
				else:
					print 'get new openid', openid, ';weshop openid None'
			except:
				print 'get openid error'
	if openid and len(openid) > 1:# openid正常获取
		# userprofile = UserProfile.objects.filter(user_id=owner_id)
		# if len(userprofile) != 1:
		# 	print 'weixin author middleware len(userprofile) = ', len(userprofile),\
		# 		';owner_id ', owner_id
		# 	return _get_product_response(request)
		# webapp_id = userprofile[0].webapp_id

		# weixin_user = WeixinUser.objects.filter(username=openid, webapp_id=webapp_id)
		# if len(weixin_user) == 1 and weixin_user[0].is_subscribed:# 已关注会员，直接优惠购买
		# 	social_account = SocialAccount.objects.filter(openid=openid, webapp_id=webapp_id)
		# 	return redirect('/workbench/jqm/preview/?woid=%s&module=apps:weshop:mall&model=product&action=get&rid=%s&sct=%s'\
		# 		% (owner_id, rid, social_account[0].token))
		# 未关注会员，需要引导关注
		cache_key = 'from_weshop_%s' % openid
		# print 'jz1---', cache_key, rid
		cache.set(cache_key, rid, 5 * 60)
	else:# openid 获取异常
		openid = '0'
	cache.set('%s_%s_openid' % (owner_id, sessionid), openid)
	return _get_product_response(request)

def _get_product_response(request):
	request.template_dir = TEMPLATE_DIR
	request.is_return_context = True
	context, product = request_util.get_product(request)
	op_settings = OperationSettings.objects.get(owner_id = product.owner_id)
	if not op_settings.weshop_followurl or not op_settings.weshop_followurl.startswith('http://mp.weixin.qq.com'):
		context['non_member_followurl'] = None
	if product.is_use_custom_model:
		return render_to_response('%s/custom_model_product_detail.html' % request.template_dir, context)
	return render_to_response('%s/product_detail.html' % request.template_dir, context)


########################################################################
# get_order_list: 获取订单列表
########################################################################
@mobile_view_func(resource='order_list', action='get')
def get_order_list(request):
	request.template_dir = TEMPLATE_DIR
	return request_util.get_order_list(request)


########################################################################
# edit_order: 编辑订单
########################################################################
@mobile_view_func(resource='order', action='edit')
def edit_order(request):
	if request.webapp_user.ship_info and request.webapp_user.ship_info.ship_name:
		request.template_dir = TEMPLATE_DIR
		request.is_return_context = True

		context = request_util.edit_order(request)
		order = context['order']
		if str(order.products[0].owner_id) != request.GET['woid']:
			request.not_weshop_product = True
		else:
			request.not_weshop_product = False
		return render_to_response('%s/edit_order.html' % request.template_dir, context)
	else:
		request.redirect_url_query_string = request.META.get('QUERY_STRING', '')
		request.template_dir = 'webapp/default'
		request.action = 'add'
		return request_util.edit_address(request)
	#return request_util.edit_order(request)


########################################################################
# edit_address: 编辑订单
########################################################################
@mobile_view_func(resource='address', action='edit')
def edit_address(request):
	request.template_dir = TEMPLATE_DIR
	return request_util.edit_address(request)


########################################################################
# pay_order: 支付订单页面
########################################################################
@mobile_view_func(resource='order', action='pay')
def pay_order(request):
	request.template_dir = TEMPLATE_DIR
	request.is_return_context = True
	context = request_util.pay_order(request)
	#_update_status(context)
	return render_to_response('%s/order_payment.html' % request.template_dir, context)


########################################################################
# get_pay_result: 支付结果，在支付宝完成支付后支付宝访问
# 携带的参数中主要使用：
# out_trade_no 订单号
########################################################################
@mobile_view_func(resource='pay_result', action='get')
def get_pay_result(request):
	request.template_dir = TEMPLATE_DIR
	request.is_return_context = True
	context = request_util.get_pay_result(request)
	#_update_status(context)
	return render_to_response('%s/order_payment.html' % request.template_dir, context)


########################################################################
# get_pay_notify_result : 支付宝异步 回调接口
########################################################################
@mobile_view_func(resource='pay_notify_result', action='get')
def get_pay_notify_result(request):
	request.template_dir = TEMPLATE_DIR
	return request_util.get_pay_notify_result(request)