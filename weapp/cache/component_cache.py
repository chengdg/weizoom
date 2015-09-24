# -*- coding: utf-8 -*-
from __future__ import absolute_import


from utils import cache_util
from modules.member import models as member_models
from account.social_account import models as social_account_models
from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_error, watchdog_warning
from weapp.hack_django import post_update_signal
from django.db.models import signals
from datetime import datetime
from weixin.user.models import *
from account.models import * 

def get_component_auth_for_cache(component, appid):
	def inner_func():
		authed_appid = ComponentAuthedAppid.objects.filter(component_info=component, authorizer_appid=appid, is_active=True)[0]
		user_profile = UserProfile.objects.get(user_id= authed_appid.user_id)
		mpuser = WeixinMpUser.objects.get(owner_id=authed_appid.user_id)
		
		default_tag = member_models.MemberTag.get_default_tag(user_profile.webapp_id)
		default_grade = member_models.MemberGrade.get_default_grade(user_profile.webapp_id)
		try:
			integral_strategy_settings = member_models.IntegralStrategySttings.objects.get(webapp_id=user_profile.webapp_id)
		except:
			error_msg = u"获得user('{}')对应的IntegralStrategySttings构建cache失败, cause:\n{}"\
				.format(user_profile.user_id, unicode_full_stack())
			watchdog_error(error_msg, user_id=user_profile.user_id, noraise=True)
			integral_strategy_settings = None

		return {
			'value': {
				'user_profile': user_profile.to_dict(),
				'component_authed_appid': authed_appid.to_dict(),
				'mpuser': mpuser.to_dict(),
				'default_tag': default_tag.to_dict(),
				'default_grade': default_grade.to_dict(),
				'integral_strategy_settings': integral_strategy_settings.to_dict() if integral_strategy_settings else None
			}
		}

	return inner_func

class Object(object):
	def __init__(self):
		pass

def get_component_auth(component, appid):
	# today = datetime.today()
	# date_str = datetime.today().strftime('%Y-%m-%d') 
	key = 'component_{appid:%s}' % appid
	data = cache_util.get_from_cache(key, get_component_auth_for_cache(component, appid))

	obj = Object()
	obj.user_profile = UserProfile.from_dict(data['user_profile'])
	obj.component_authed_appid =  ComponentAuthedAppid.from_dict(data['component_authed_appid'])
	obj.mpuser = WeixinMpUser.from_dict(data['mpuser'])
	if data['integral_strategy_settings']:
		obj.integral_strategy_settings = member_models.IntegralStrategySttings.from_dict(data['integral_strategy_settings'])
	else:
		obj.integral_strategy_settings = None
<<<<<<< HEAD
=======

>>>>>>> 优化 compent
	obj.default_tag = member_models.MemberTag.from_dict(data['default_tag'])
	obj.default_grade = member_models.MemberGrade.from_dict(data['default_grade'])
	return obj


def delete_component_auth_cache(appid):
	today = datetime.today()
	date_str = datetime.today().strftime('%Y-%m-%d') 

	key = 'component_{appid:%s}' % appid
	cache_util.delete_cache(key)

def update_component_cache_for_auther_appid(instance, **kwargs):
	"""
	ComponentAuthedAppid.save时触发信号回调函数

	@param instance ComponentAuthedAppid
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

<<<<<<< HEAD
def update_component_cache_for_integral_settings(instance, **kwargs):
	"""
	IntegralStrategySttings.save or update时触发信号回调函数

	@param instance IntegralStrategySttings
	@param kwargs   其他参数，包括'sender'、'created'、'signal'、'raw'、'using'


	"""
	#print("in update_webapp_order_cache(), kwargs: %s" % kwargs)
	if isinstance(instance, member_models.IntegralStrategySttings):
		try:
			user_profile = UserProfile.objects.get(webapp_id=instance.webapp_id)
			authorizer_appid = ComponentAuthedAppid.objects.get(user_id=user_profile.user_id)
			try:
				delete_component_auth_cache(authorizer_appid.authorizer_appid)
				#get_accounts(openid, webapp_id)
			except:
				pass
		except:
			pass

		
	else:
		instances = list(instance)
		for integral_strategy_settings in instances:
			try:
				user_profile = UserProfile.objects.get(webapp_id=integral_strategy_settings.webapp_id)
				authorizer_appid = ComponentAuthedAppid.objects.get(user_id=user_profile.user_id)
				try:
					delete_component_auth_cache(authorizer_appid.authorizer_appid)
				except:
					pass
			except:
				pass
	return

post_update_signal.connect(update_component_cache_for_auther_appid, sender=ComponentAuthedAppid, dispatch_uid = "ComponentInfo.update")
#signals.post_save.connect(update_component_cache_for_integral_settings, sender=member_models.IntegralStrategySttings, dispatch_uid = "member_models.IntegralStrategySttings.save")
post_update_signal.connect(update_component_cache_for_integral_settings, sender=member_models.IntegralStrategySttings, dispatch_uid = "member_models.IntegralStrategySttings.update")
=======
post_update_signal.connect(update_component_cache, sender=ComponentAuthedAppid, dispatch_uid = "ComponentInfo.update")
signals.post_save.connect(update_component_cache, sender=member_models.IntegralStrategySttings, dispatch_uid = "member_models.IntegralStrategySttings")
>>>>>>> 优化 compent
#signals.post_save.connect(update_webapp_product_cache, sender=mall_models.ProductCategory, dispatch_uid = "product_category.save")
#signals.post_save.connect(update_webapp_product_cache, sender=mall_models.CategoryHasProduct, dispatch_uid = "category_has_product.save")

