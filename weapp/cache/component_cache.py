# -*- coding: utf-8 -*-
from __future__ import absolute_import


from utils import cache_util
from modules.member import models as member_models
from account.social_account import models as social_account_models
from weapp.hack_django import post_update_signal
from django.db.models import signals
from datetime import datetime
from weixin.user.models import *
from account.models import * 

def get_component_auth_for_cache(component, appid):
	def inner_func():
		authed_appid = ComponentAuthedAppid.objects.filter(component_info=component, authorizer_appid=appid, is_active=True)[0]
		user_profile = UserProfile.objects.get(user_id= authed_appid.user_id)
		return {
			'value': {
				'user_profile': user_profile.to_dict(),
				'component_authed_appid': authed_appid.to_dict(),
			}
		}

	return inner_func


def get_component_auth(component, appid):
	# today = datetime.today()
	# date_str = datetime.today().strftime('%Y-%m-%d') 
	key = 'component_{appid:%s}' % appid
	data = cache_util.get_from_cache(key, get_component_auth_for_cache(component, appid))

	user_profile = UserProfile.from_dict(data['user_profile'])
	component_authed_appid = ComponentAuthedAppid.from_dict(data['component_authed_appid'])

	return user_profile, component_authed_appid

def delete_component_auth_cache(appid):
	today = datetime.today()
	date_str = datetime.today().strftime('%Y-%m-%d') 

	key = 'component_{appid:%s}' % appid
	cache_util.delete(key)

def update_component_cache(instance, **kwargs):
	"""
	ComponentAuthedAppid.save时触发信号回调函数

	@param instance Member的实例
	@param kwargs   其他参数，包括'sender'、'created'、'signal'、'raw'、'using'


	"""
	#print("in update_webapp_order_cache(), kwargs: %s" % kwargs)
	if isinstance(instance, ComponentAuthedAppid):
		try:
			delete_component_auth_cache(instance.authorizer_appid)
			#get_accounts(openid, webapp_id)
		except:
			pass
	else:
		instances = list(instance)
		for authed_appid in instances:
			try:
				delete_component_auth_cache(authed_appid.authorizer_appid)
				#get_accounts(openid, webapp_id)
			except:
				pass
	return

post_update_signal.connect(update_component_cache, sender=ComponentAuthedAppid, dispatch_uid = "ComponentInfo.update")
signals.post_save.connect(update_component_cache, sender=ComponentAuthedAppid, dispatch_uid = "ComponentInfo.save")
#signals.post_save.connect(update_webapp_product_cache, sender=mall_models.ProductCategory, dispatch_uid = "product_category.save")
#signals.post_save.connect(update_webapp_product_cache, sender=mall_models.CategoryHasProduct, dispatch_uid = "category_has_product.save")

