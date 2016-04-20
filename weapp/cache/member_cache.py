# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging

from utils import cache_util
from modules.member import models as member_models
from account.social_account import models as social_account_models
from weapp.hack_django import post_update_signal
from django.db.models import signals
from datetime import datetime

from services import kafka_client

def get_accounts_for_cache(openid, webapp_id):
	def inner_func():
		social_account = member_models.SocialAccount.objects.get(webapp_id=webapp_id, openid=openid)
		member = member_models.Member.objects.get(id=member_models.MemberHasSocialAccount.objects.filter(account=social_account)[0].member.id)
		if member_models.WebAppUser.objects.filter(webapp_id=webapp_id, member_id=member.id, father_id=0).count() == 0:
			webapp_user = member_models.WebAppUser.objects.create(webapp_id=webapp_id, member_id=member.id, father_id=0, token=member.id)
		else:
			webapp_user = member_models.WebAppUser.objects.filter(webapp_id=webapp_id, member_id=member.id, father_id=0)[0]
		today = datetime.today()
		date_str = datetime.today().strftime('%Y-%m-%d') 
		return {
			'value': {
				'member': member.to_dict(),
				'webapp_user': webapp_user.to_dict(),
				'social_account': social_account.to_dict(),
				'date_time':date_str
			}
		}

	return inner_func


def get_accounts(openid, webapp_id):
	today = datetime.today()
	date_str = datetime.today().strftime('%Y-%m-%d') 
	key = 'member_{webapp:%s}_{openid:%s}' % (webapp_id, openid)
	data = cache_util.get_from_cache(key, get_accounts_for_cache(openid, webapp_id))
	if data['date_time'] != date_str:
		delete_member_cache(openid, webapp_id)
		data = cache_util.get_from_cache(key, get_accounts_for_cache(openid, webapp_id))

	member = member_models.Member.from_dict(data['member'])
	webapp_user = member_models.WebAppUser.from_dict(data['webapp_user'])
	social_account = social_account_models.SocialAccount.from_dict(data['social_account'])

	return webapp_user, social_account, member


def delete_member_cache(openid, webapp_id):
	today = datetime.today()
	date_str = datetime.today().strftime('%Y-%m-%d') 

	key = 'member_{webapp:%s}_{openid:%s}' % (webapp_id, openid)

	# print dir(client)	
	# x = json.dumps({'w':'1'})
	
	message = {"webapp": webapp_id, "openid": openid}
	kafka_client.send_message('member', message)


def update_member_cache(instance, **kwargs):
	"""
	Order.save时触发信号回调函数

	@param instance Member的实例
	@param kwargs   其他参数，包括'sender'、'created'、'signal'、'raw'、'using'


	"""
	print("in update_webapp_order_cache(), ------------------------kwargs: %s" % kwargs)
	if isinstance(instance, member_models.Member):
		try:
			openid = member_models.MemberHasSocialAccount.objects.filter(member=instance)[0].account.openid
			delete_member_cache(openid, instance.webapp_id)
			#get_accounts(openid, webapp_id)
		except:
			pass
	else:
		instances = list(instance)
		for member in instances:
			try:

				openid = member_models.MemberHasSocialAccount.objects.filter(member=member)[0].account.openid
				delete_member_cache(openid, member.webapp_id)
				#get_accounts(openid, webapp_id)
			except:
				pass
	return

post_update_signal.connect(update_member_cache, sender=member_models.Member, dispatch_uid = "member.updates")
signals.post_save.connect(update_member_cache, sender=member_models.Member, dispatch_uid = "member.save")
#signals.post_save.connect(update_webapp_product_cache, sender=mall_models.ProductCategory, dispatch_uid = "product_category.save")
#signals.post_save.connect(update_webapp_product_cache, sender=mall_models.CategoryHasProduct, dispatch_uid = "category_has_product.save")

