# -*- coding: utf-8 -*-

import json

from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.db.models import F

from weixin2 import export
import weixin2.models as weixin_models
import weixin2.module_api as weixin_module_api
from core import resource
from core import paginator
from core.jsonresponse import create_response
from apps.models import CustomizedApp

COUNT_PER_PAGE = 20
FIRST_NAV = export.WEIXIN_HOME_FIRST_NAV

class SingleNews(resource.Resource):
	"""
	单图文资源
	"""
	app = 'new_weixin'
	resource = 'single_news'

	@login_required
	def get(request):
		"""
		获取单图文编辑页面
		"""
		material_id = request.GET.get('id', None)
		if material_id:
			newses = list(weixin_models.News.objects.filter(material_id=material_id))
			news_count, newses_object = weixin_module_api.get_newses_object(newses)
		else:
			newses_object = []

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_weixin_second_navs(request),
			'second_nav_name': export.WEIXIN_ADVANCE_SECOND_NAV,
			'third_nav_name': export.ADVANCE_MANAGE_MATERIAL_NAV,
			'material_id': material_id,
			'newses': json.dumps(newses_object)
		})

		return render_to_response('weixin/advance_manage/edit_single_news.html', c)

	def api_put(request):
		"""
		创建新的图文
		"""
		newses = json.loads(request.POST['data'])
		material = weixin_models.Material.objects.create(owner=request.user, type=weixin_models.SINGLE_NEWS_TYPE)

		for news in newses:
			weixin_models.News.objects.create(
				material = material,
				display_index = news['display_index'],
				title = news['title'].strip(),
				summary = news['summary'].strip(),
				text = news['text'],
				pic_url = news['pic_url'],
				url = news['url'],
				link_target = news['link_target'],
				is_show_cover_pic = True if (news.get('is_show_cover_pic', True) in ('true', 'yes', 'True', 'Yes', True)) else False
			)

		response = create_response(200)
		response.data.id = material.id
		return response.get_response()

	def api_post(request):
		"""
		修改的图文
		"""
		newses = json.loads(request.POST['data'])
		material_id = int(request.POST['material_id'])
		material = weixin_models.Material.objects.get(id=material_id)

		for index, news in enumerate(newses):
			link_target = news['link_target']
			if type(link_target) != unicode:
				link_target = json.dumps(link_target)

			if int(news['id']) > 0:
				new = weixin_models.News.objects.get(id=news['id'])
				new.display_index = index+1
				new.title = news['title'].strip()
				new.summary = news['summary'].strip()
				new.text = news['text']

				if news['url']:
					new.url = news['url']
					new.link_target = link_target
				else:
					new.url = ''
					new.link_target = ''

				new.pic_url = news['pic_url']
				
				new.is_show_cover_pic = True if (news.get('is_show_cover_pic', True) in ('true', 'yes', 'True', 'Yes', True)) else False
				new.save()
			else:
				weixin_models.News.objects.create(
					material = material,
					display_index = index+1,
					title = news['title'].strip(),
					summary = news['summary'].strip(),
					text = news['text'],
					pic_url = news['pic_url'],
					url = news['url'],
					link_target = link_target,
					is_show_cover_pic = True if (news.get('is_show_cover_pic', True) in ('true', 'yes', 'True', 'Yes', True)) else False
				)
		response = create_response(200)
		response.data.id = material.id
		return response.get_response()

	def api_delete(request):
		"""
		删除商品
		"""
		weixin_models.Material.objects.filter(owner=request.user, id=request.POST['id']).update(is_deleted=True)
		return create_response(200).get_response()


class MultiNews(resource.Resource):
	"""
	多图文资源
	"""
	app = 'new_weixin'
	resource = 'multi_news'

	@login_required
	def get(request):
		"""
		获取多图文编辑页面
		"""
		material_id = request.GET.get('id', None)
		if material_id:
			newses = list(weixin_models.News.objects.filter(material_id=material_id))
			news_count, newses_object = weixin_module_api.get_newses_object(newses)
		else:
			newses_object = []

		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_weixin_second_navs(request),
			'second_nav_name': export.WEIXIN_ADVANCE_SECOND_NAV,
			'third_nav_name': export.ADVANCE_MANAGE_MATERIAL_NAV,
			'material_id': material_id,
			'newses': json.dumps(newses_object)
		})

		return render_to_response('weixin/advance_manage/edit_multi_news.html', c)

	def api_put(request):
		"""
		创建新的图文
		"""
		newses = json.loads(request.POST['data'])
		material = weixin_models.Material.objects.create(owner=request.user, type=weixin_models.MULTI_NEWS_TYPE)

		for news in newses:
			weixin_models.News.objects.create(
				material = material,
				display_index = news['display_index'],
				title = news['title'].strip(),
				summary = news['summary'].strip(),
				text = news['text'],
				pic_url = news['pic_url'],
				url = news['url'],
				link_target = news['link_target'],
				is_show_cover_pic = True if (news.get('is_show_cover_pic', True) in ('true', 'yes', 'True', 'Yes', True)) else False
			)

		response = create_response(200)
		response.data.id = material.id
		return response.get_response()

	def api_post(request):
		"""
		修改多图文
		"""
		newses = json.loads(request.POST['data'])
		material_id = int(request.POST['material_id'])
		
		delete_ids = request.POST.get('delete_ids', None)
		if delete_ids:
			weixin_models.News.objects.filter(id__in=delete_ids.split(',')).delete()
		
		material = weixin_models.Material.objects.get(id=material_id)

		for index, news in enumerate(newses):
			link_target = news['link_target']
			if type(link_target) != unicode:
				link_target = json.dumps(link_target)

			if int(news['id']) > 0:
				new = weixin_models.News.objects.get(id=news['id'])
				new.display_index = index+1
				new.title = news['title'].strip()
				new.summary = news['summary'].strip()
				new.text = news['text']

				if news['url']:
					new.url = news['url']
					new.link_target = link_target
				else:
					new.url = ''
					new.link_target = ''

				new.pic_url = news['pic_url']
				
				new.is_show_cover_pic = True if (news.get('is_show_cover_pic', True) in ('true', 'yes', 'True', 'Yes', True)) else False
				new.save()
			else:
				weixin_models.News.objects.create(
					material = material,
					display_index = index+1,
					title = news['title'].strip(),
					summary = news['summary'].strip(),
					text = news['text'],
					pic_url = news['pic_url'],
					url = news['url'],
					link_target = link_target,
					is_show_cover_pic = True if (news.get('is_show_cover_pic', True) in ('true', 'yes', 'True', 'Yes', True)) else False
				)

		response = create_response(200)
		response.data.id = material.id
		return response.get_response()


	def api_delete(request):
		"""
		删除商品
		"""
		weixin_models.Material.objects.filter(owner=request.user, id=request.POST['id']).update(is_deleted=True)
		return create_response(200).get_response()

