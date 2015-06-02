# -*- coding: utf-8 -*-

#from django.template import RequestContext
from django.contrib.auth.decorators import login_required
#from django.shortcuts import render_to_response

from weixin2 import export
from core.exceptionutil import unicode_full_stack
from core import resource
from core.jsonresponse import create_response
from weixin2.models import FanCategory,FanHasCategory
from modules.member.models import *
#from .util import get_members

from fans_category import DEFAULT_CATEGORY_NAME

class FansInfo(resource.Resource):
	"""
	粉丝的介绍信息
	"""
	app = 'new_weixin'
	resource = 'fans_info'

	@staticmethod
	def check_params(request):
		is_valid = True
		response = None
		if not 'id' in request.GET:
			is_valid = False
			response = create_response(500)
			response.errMsg = "缺少参数: id"
		return (is_valid, response)

	@login_required
	def api_get(request):
		"""
		获取粉丝(会员)的介绍信息

		~~~~~~~~~~{.c}
		info = {
			"nickname": u"昵称",
			"remark": u"备注",
			"location": u"北京",
			"signature": u"签名",
			"category": u"未分组",
		}
		~~~~~~~~~~
		"""

		#assert 'id' in request.GET
		(is_valid, response) = FansInfo.check_params(request)

		if is_valid:
			fan_id = request.GET.get('id')
			response = create_response(200)

			# 获取粉丝(会员)信息
			try:
				social_member = Member.objects.get(id=fan_id)
				social_member_info = MemberInfo.objects.get(member=social_member)
			
				categories = FanHasCategory.objects.filter(fan_id=fan_id)
				if len(categories)>0:
					category_name = categories[0].category.name
					category_id = categories[0].category.id
				else:
					category_name = DEFAULT_CATEGORY_NAME
					category_id = -1
				
				address = "%s %s %s" % (social_member.country, social_member.province, social_member.city) 
				info = {
					'nickname': social_member.username_for_html,
					'remark': social_member_info.name,
					'location': address,
					'signature': '', # where to get?
					'category': category_name,
					'category_id': category_id,
				}
				response.data = {
					'info': info
				}
			except Member.DoesNotExist:
				response = create_response(501)
				response.errMsg = u'无效id'
				#response.innerErrMsg = unicode_full_stack()
			except MemberInfo.DoesNotExist:
				response = create_response(502)
				response.errMsg = u'无有效用户信息'
			except:
				response = create_response(500)
				response.errMsg = u'获取粉丝详情失败(如无效ID)'
				response.innerErrMsg = unicode_full_stack()
		return response.get_response()
