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

#COUNT_PER_PAGE = 2
COUNT_PER_PAGE = 50
FIRST_NAV = export.WEIXIN_HOME_FIRST_NAV

DEFAULT_CATEGORY_NAME=u"未分组"

# 粉丝分组名称最大长度
FAN_CATEGORY_NAME_MAX_LENGTH = 6

class FansCategory(resource.Resource):
	"""
	粉丝的分组资源
	"""
	app = 'new_weixin'
	resource = 'fans_category'

	@login_required
	def api_get(request):
		"""
		获取分组列表
		"""
		if request.user_profile:
			webapp_id = request.user_profile.webapp_id
			objects = FanCategory.objects.filter(webapp_id=webapp_id).distinct()
			response = create_response(200)
			categories = [{
				'name': DEFAULT_CATEGORY_NAME,
				'id': 0,
				'is_editable': False,
			}]
			for obj in objects:
				categories.append({
					'name': obj.name,
					'id': obj.id,
					'is_editable': True,
					})

			fan_id = int(request.GET.get('fan_id', -1))
			fan_has_category_id = 0
			if fan_id != -1:
				try:
					fan_has_category = FanHasCategory.objects.get(fan_id = fan_id)
					fan_has_category_id = fan_has_category.category_id
				except Exception, e:
					pass


			response.data = {
				'categories': categories,
				'fan_has_category_id': fan_has_category_id
			}
		else:
			response = create_response(400)
			response.errMsg = u'获取分组列表失败'
		return response.get_response()

	@staticmethod
	def check_category_name(category_name):
		"""
		检查category_name是否合法
		"""
		is_valid = True
		response = None
		# 检查长度
		if len(category_name)<1:
			is_valid = False
			response = create_response(501)
			response.errMsg = u'分组名称不能为空'
		elif len(category_name)>FAN_CATEGORY_NAME_MAX_LENGTH:
			is_valid = False
			response = create_response(502)
			response.errMsg = u'名称长度不能超过{}'.format(FAN_CATEGORY_NAME_MAX_LENGTH)
		elif category_name == DEFAULT_CATEGORY_NAME:
			is_valid = False
			# 不允许创建名为"未分类"的分组
			response = create_response(503)
			response.errMsg = u'无法创建此分类'
		if response is not None:
			response = response.get_response()
		return (is_valid, response)


	@login_required
	def api_put(request):
		"""
		创建粉丝分组

		@param category_name 分类名(不能重复)

		@retval category_id 分类ID
		"""
		#assert 'category_id' in request.POST
		if 'category_name' in request.POST:
			# 分组不允许重复
			category_name = request.POST['category_name']
			webapp_id = request.user_profile.webapp_id
			
			# 检查分类名是否合法
			(is_valid, response) = FansCategory.check_category_name(category_name)
			if is_valid:
				try:
					category = FanCategory(webapp_id=webapp_id, name=category_name)
					category.save()
					response = create_response(200)
					response.data = {
						'category_id': category.id
					}
					response = response.get_response()
				except:
					response = create_response(500)
					#error_code = error.error_response.errcode
					#response.errMsg = weixin_error_codes.code2msg.get(error_code, error.error_response.errmsg)
							#response.innerErrMsg = error.error_response.detail
					response.errMsg = u'创建分类失败'
					response.innerErrMsg = unicode_full_stack()
					response = response.get_response()
		else:
			response = create_response(400).get_response()
		return response


	@login_required
	def api_delete(request):
		"""
		删除粉丝分组
		"""
		if 'category_id' in request.POST:
			# 只能删除本webapp下的分组
			webapp_id = request.user_profile.webapp_id
			try:
				category_id = int(request.POST['category_id'])
				if category_id>0:
					FanCategory.objects.filter(webapp_id=webapp_id, id=category_id).delete()
					response = create_response(200).get_response()
				else:
					response = create_response(500)
					response.errMsg = u'无法删除此分组'
					response = response.get_response()
			except:
				response = create_response(500)
				response.errMsg = u'删除分组失败'
				response.innerErrMsg = unicode_full_stack()
				response = response.get_response()
		else:
			response = create_response(400)
			response.errMsg = u"请指定分组ID"
			response = response.get_response()
		return response


	@login_required
	def api_post(request):
		"""
		编辑分组名称
		"""
		if 'category_id' in request.POST and 'category_name' in request.POST:
			# 只能删除本webapp下的分组
			webapp_id = request.user_profile.webapp_id
			category_name = request.POST['category_name']

			# 检查分类名是否合法
			(is_valid, response) = FansCategory.check_category_name(category_name)
			if is_valid:
				try:
					category_id = request.POST['category_id']
					# 确保只能删除本webapp账号的分类才使用 (webapp_id, id) 查询
					category = FanCategory.objects.get(webapp_id=webapp_id, id=category_id)
					category.name = category_name
					category.save()
					response = create_response(200).get_response()
				except:
					response = create_response(500)
					response.errMsg = u'分类名更新失败(错误的ID?)'
					response.innerErrMsg = unicode_full_stack()
					response = response.get_response()
		else:
			response = create_response(400)
			response.errMsg = u"需要指定category_id和category_name"
			response = response.get_response()
		return response



class FansCategoryRelation(resource.Resource):
	"""
	粉丝分组的关系
	"""
	app = 'new_weixin'
	resource = 'fans_category_relation'

	@staticmethod
	def change_fan_category(fan_id, category_id):
		"""
		将fan_id调整到category_id

		@todo 待优化。如果大量地调整分组？
		"""
		relations = FanHasCategory.objects.filter(fan_id=fan_id).distinct()
		ret = False
		if category_id<=0:
			# 删除关系，表示未分组
			relations.delete()
			#response = create_response(200)
			#response.errMsg = u"置为未分组"
			#response = response.get_response()
			ret = True
		else:	
			if relations.count()>0:
				# TODO: 应该不超过1个
				relation = relations[0]
				relation.category_id = category_id
			else:
				# 添加一条关系
				relation = FanHasCategory(fan_id=fan_id, category_id=category_id)
			relation.save()
			#response = create_response(200).get_response()
			ret = True
		return ret


	@login_required
	def api_post(request):
		"""
		将粉丝加入分组
		@param fan_id 粉丝ID
		@param category_id 分类ID (如果category_id<=0，则置为"未分组")

		@todo 检查category_id是否为当前webapp_id所拥有
		"""
		#assert 'fan_id' in request.POST
		#assert 'category_id' in request.POST

		if 'fan_ids' in request.POST and 'category_id' in request.POST:
			try:
				fan_ids = request.POST['fan_ids']
				ids = fan_ids.split(',')
				category_id = int(request.POST['category_id'])
				#print("category_id={}".format(category_id))

				success_list = []
				for fan_id in ids:
					try:
						if FansCategoryRelation.change_fan_category(fan_id, category_id):
							success_list.append(fan_id)
					except:
						print(unicode_full_stack())

				if len(success_list)>0:
					response = create_response(200)
					response.data = {
						"success_ids": success_list
					}
				else:
					response = create_response(400)
					response.errMsg = u'修改分类失败'
				response = response.get_response()
			except:
				response = create_response(500)
				response.errMsg = u'修改分类失败'
				response.innerErrMsg = unicode_full_stack()
				response = response.get_response()
		else:
			response = create_response(400)
			response.errMsg = u"需要指定category_id和category_name"
			response = response.get_response()
		# TODO: 将API处理的框架统一: 参数齐全，则更新，成功返回A，失败返回B；缺少参数返回C。
		return response
