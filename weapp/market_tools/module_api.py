# -*- coding: utf-8 -*-

__author__ = 'robert'

from models import MarketToolAuthority


################################################################
# enable_market_tool_authority_for: 为用户user启用market tool
################################################################
def enable_market_tool_authority_for(user):
	if MarketToolAuthority.objects.filter(owner=user).count() == 0:
		MarketToolAuthority.objects.create(
			owner = user,
			is_enable_market_tool = True
		)	
	else:
		MarketToolAuthority.objects.filter(owner=user).update(
			is_enable_market_tool = True
			)

################################################################
# enable_market_tool_authority_for: 为用户user关闭market tool
################################################################
def disable_market_tool_authority_for(user):
	MarketToolAuthority.objects.filter(owner=user).update(
			is_enable_market_tool = False
			)
	
	
################################################################
# delete_user_market_tool_data: 清除user对应market tool产生的数据
################################################################
def delete_user_market_tool_data(user_profile):
	#由于目前营销工具所有数据信息都与owner相关（ForeignKey）
	#故删除User信息后，对应的信息都会被删除，本方法暂不提供额外操作。
	pass
	
	
		