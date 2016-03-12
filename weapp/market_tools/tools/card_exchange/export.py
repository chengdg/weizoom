# -*- coding: utf-8 -*-

__author__ = 'paco bert'

from django.conf import settings

from core.jsonresponse import JsonResponse, create_response

from mall.promotion.models import CardExchange


########################################################################
# get_link_targets: 获取可链接的目标
########################################################################
def get_link_targets(request):
	response = create_response(200)

	return response.get_response()


def get_card_exchange_link(request):
	"""
	获取微众卡兑换手机页面链接
	@param request:
	@return:
	"""
	webapp_id = request.user_profile.webapp_id
	if CardExchange.objects.filter(webapp_id=webapp_id).count() > 0 and webapp_id:
		return '/mall2/m_card_exchange/?webapp_id=%s' % webapp_id
	return None
