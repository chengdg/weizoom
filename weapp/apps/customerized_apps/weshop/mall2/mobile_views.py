# -*- coding: utf-8 -*-

import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json

from django.shortcuts import render_to_response, redirect
from django.core.cache import cache

from webapp.modules.mall import request_util
from mall.models import *
from apps.register import mobile_view_func
from weshop.models import WeshipMemberRelation

from weixin.user.models import WeixinMpUser, WeixinMpUserAccessToken, WeixinUser

from account.social_account.models import SocialAccount
from account.models import UserProfile, OperationSettings
from modules.member.models import Member, MemberHasSocialAccount
from modules.member.member_identity_util import get_uuid

template_path_items = os.path.dirname(__file__).split(os.sep)
TEMPLATE_DIR = 'weshop/templates/mall'

########################################################################
# list_products: 显示"商品列表"页面
########################################################################
@mobile_view_func(resource='products', action='list')
def list_products(request):
	request.template_dir = TEMPLATE_DIR
	request.is_return_context = True
	context = request_util.list_products(request)
	for product in context.get('products'):
		if product.weshop_sync == 2:
			product.display_price = round(product.display_price * 1.1, 2)
	# 按商品价格由低到高排序
	context.get('products').sort(lambda x,y: cmp(x.display_price, y.display_price))
	return render_to_response('%s/products.html' % request.template_dir, context)	


########################################################################
# get_product: 显示“商品详情”页面
########################################################################
@mobile_view_func(resource='product', action='get')
def get_product(request):
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
