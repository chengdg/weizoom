# jz 2015-10-28
# # -*- coding: utf-8 -*-

# __author__ = 'bert'

# from utils import cache_util
# from models import *
# #from account.models import UserProfile

# def get_user_profile_from_db(**kwargs):
# 	def inner_func():
# 		try:
# 			user_profile = UserProfile.objects.get(**kwargs)
# 			return {
# 				'keys': [
# 					'user_profile_%s' % user_profile.id,
# 					'user_profile_webapp_id_%s' % user_profile.webapp_id,
# 					'user_profile_owner_id_%s' % user_profile.user_id
# 				],
# 				'value': user_profile
# 			}
# 		except:
# 			return None
# 	return inner_func
	

# def get_user_profile_by_owner_id(owner_id):
# 	key = 'user_profile_owner_id_%s' % owner_id
# 	return cache_util.get_from_cache(key, get_user_profile_from_db(user_id=owner_id))


# def get_user_profile_by_webapp_id(webapp_id):
# 	key = 'user_profile_webapp_id_%s' % webapp_id
# 	return cache_util.get_from_cache(key, get_user_profile_from_db(webapp_id=webapp_id))