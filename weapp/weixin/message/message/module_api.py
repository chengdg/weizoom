# -*- coding: utf-8 -*-

__author__ = 'chuter'

from models import RealTimeInfo
from weixin.user.models import get_system_user_binded_mpuser

########################################################################
# get_realtime_unread_count: 获取实时未读消息数量
########################################################################
def get_realtime_unread_count(user):
	mpuser = get_system_user_binded_mpuser(user)

	if mpuser is None:
		return 0
	else:
		try:
			return RealTimeInfo.objects.get(mpuser=mpuser).unread_count
		except:
			return 0