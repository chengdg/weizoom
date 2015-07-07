# -*- coding: utf-8 -*-
import json
import time

from behave import *

from test import bdd_util
from features.testenv.model_factory import *

from django.test.client import Client
from django.contrib.auth.models import User

from mall.models import *
from modules.member.models import *
from modules.member import module_api
from weixin.user import models as weixn_models
from account import models as account_models
from utils.string_util import byte_to_hex
from utils import url_helper



@When(u'{webapp_user_name}把{webapp_owner_name}的微站链接分享到朋友圈')
def step_impl(context, webapp_user_name, webapp_owner_name):
	context.shared_url = context.last_url


@When(u"{webapp_user_name}把{webapp_owner_name}的微站链接'{shared_url_name}'分享到朋友圈")
def step_impl(context, webapp_user_name, webapp_owner_name, shared_url_name):
	setattr(context, shared_url_name, context.last_url)


def __get_member_by_openid(openid):
	try:
		social_account = SocialAccount.objects.get(openid=openid)
		member = MemberHasSocialAccount.objects.get(account=social_account).member
		return member
	except:
		return None

def __get_fmt_by_sct(sct):
	social_account = SocialAccount.objects.get(token=sct)
	member = MemberHasSocialAccount.objects.get(account=social_account).member
	return member.token

from core import dev_util
@When(u'{webapp_user_name}点击{shared_webapp_user_name}分享链接')
def step_impl(context, webapp_user_name, shared_webapp_user_name):
	time.sleep(1)
	webapp_owner_id = context.webapp_owner_id
	user = User.objects.get(id=webapp_owner_id)
	openid = "%s_%s" % (shared_webapp_user_name, user.username)
	member = module_api.get_member_by_openid(openid, context.webapp_id)

	if member:
		new_url = url_helper.remove_querystr_filed_from_request_path(context.shared_url, 'fmt')
		context.shared_url = "%s&fmt=%s" % (new_url, member.token)
	response = context.client.get(context.shared_url)
	if response.status_code == 302:
		print('[info] redirect by change fmt in shared_url')
		redirect_url = bdd_util.nginx(response['Location'])
		context.last_url = redirect_url
		response = context.client.get(bdd_util.nginx(redirect_url))
	else:
		print('[info] not redirect')
		context.last_url = context.shared_url


@When(u"{webapp_user_name}点击{shared_webapp_user_name}分享链接'{shared_url_name}'")
def step_impl(context, webapp_user_name, shared_webapp_user_name, shared_url_name):
	shared_url = getattr(context, shared_url_name)
	response = context.client.get(shared_url)
	if response.status_code == 302:
		print('[info] redirect by change fmt in shared_url')
		redirect_url = bdd_util.nginx(response['Location'])
		context.last_url = redirect_url
		response = context.client.get(bdd_util.nginx(redirect_url))
	else:
		context.last_url = shared_url


@Then(u'{user}能获取到{webapp_user_name}的好友')
def step_impl(context, user, webapp_user_name):
	if hasattr(context, 'client'):
		context.client.logout()
	context.client = bdd_util.login(user)
	client = context.client
	json_data = json.loads(context.text)
	openid = '%s_%s' % (webapp_user_name, user)
	member = __get_member_by_openid(openid)
	url = '/member/api/follow_relations/get/?member_id=%s' % member.id
	response = client.get(bdd_util.nginx(url))

	items = json.loads(response.content)['data']['items']
	actual_member_rellations = []
	for data_item in items:
		actual_member_rellation = {}
		actual_member_rellation['name'] = data_item['username']
		if str(data_item['source']) == '-1' or str(data_item['source']) == '0':
			actual_member_rellation['source'] = u'直接关注'
		elif str(data_item['source']) == '1':
			actual_member_rellation['source'] = u'推广扫码'
		else:
			actual_member_rellation['source'] = u'会员分享'

		if str(data_item['is_fans']) == '0':
			actual_member_rellation['is_fans'] = u'否'

		if str(data_item['is_fans']) == '1':
			actual_member_rellation['is_fans'] = u'是'

		actual_member_rellations.append(actual_member_rellation)
	bdd_util.assert_list(actual_member_rellations, json_data)

	context.click_member = None
	context.member_clicked = False

@When(u'{user}分享{shared_user}分享{webapp_owner_name}的微站链接到朋友圈')
def step_impl(context, user, shared_user, webapp_owner_name):
	openid = '%s_%s' % (user, webapp_owner_name)
	member = __get_member_by_openid(openid)
	if member:
		fmt = member.token
		webapp_owner_id = bdd_util.get_user_id_for(webapp_owner_name)
		url = '/workbench/jqm/preview/?module=mall&model=products&action=list&category_id=0&workspace_id=mall&webapp_owner_id=%d&fmt=%s' % (webapp_owner_id, fmt)
		context.shared_url = url


@When(u'{shared_url}把{webapp_owner_name}的商品"{product_name}"的链接分享到朋友圈')
def step_impl(context, shared_url, webapp_owner_name, product_name):
	openid = '%s_%s' % (shared_url, webapp_owner_name)
	member = __get_member_by_openid(openid)
	if member:
		fmt = member.token
		webapp_owner_id = bdd_util.get_user_id_for(webapp_owner_name)
		product_id = Product.objects.get(name=product_name).id
		url = '/workbench/jqm/preview/?module=mall&model=product&action=get&rid=%d&workspace_id=mall&webapp_owner_id=%d&fmt=%s' % (product_id, webapp_owner_id, fmt)
		context.shared_url = url


@When('{user}通过{shared_user}分享的链接购买{webapp_owner_name}的商品')
def step_impl(context, user, shared_user, webapp_owner_name):
	context.execute_steps(u"when %s购买%s的商品" % (user, webapp_owner_name))


@When(u'{webapp_owner_name}关闭消费返积分')
def step_impl(context, webapp_owner_name):
	webapp_owner_id = bdd_util.get_user_id_for(webapp_owner_name)
	user_profile = account_models.UserProfile.objects.get(user_id=webapp_owner_id)
	IntegralStrategySttingsDetail.objects.filter(webapp_id=user_profile.webapp_id).update(is_used=False)


@When(u'{webapp_owner_name}开启消费返积分')
def step_impl(context, webapp_owner_name):
	webapp_owner_id = bdd_util.get_user_id_for(webapp_owner_name)
	user_profile = account_models.UserProfile.objects.get(user_id=webapp_owner_id)
	IntegralStrategySttingsDetail.objects.filter(webapp_id=user_profile.webapp_id).update(is_used=True)


@When(u'{user}通过{shared_user}分享链接关注{webapp_owner_name}的公众号')
def step_impl(context, user, shared_user, webapp_owner_name):
	context.execute_steps(u"When 清空浏览器")
	context.execute_steps(u"When %s访问%s的webapp" % (shared_user, webapp_owner_name))
	context.execute_steps(u"When %s把%s的微站链接分享到朋友圈" % (shared_user, webapp_owner_name))
	
	context.execute_steps(u"When 清空浏览器")
	context.execute_steps(u"When %s点击%s分享链接" % (user, shared_user))
	context.execute_steps(u"When %s关注%s的公众号" % (user, webapp_owner_name))


@When(u'{user}通过{shared_user}分享链接关注{webapp_owner_name}的公众号于{followed_date}')
def step_impl(context, user, shared_user, webapp_owner_name, followed_date):
	context.execute_steps(u"When 清空浏览器")
	context.execute_steps(u"When %s访问%s的webapp" % (shared_user, webapp_owner_name))
	context.execute_steps(u"When %s把%s的微站链接分享到朋友圈" % (shared_user, webapp_owner_name))

	context.execute_steps(u"When 清空浏览器")
	context.execute_steps(u"When %s点击%s分享链接" % (user, shared_user))
	context.execute_steps(u"When %s关注%s的公众号于%s" % (user, webapp_owner_name, followed_date))
