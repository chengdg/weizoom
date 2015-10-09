# -*- coding: utf-8 -*-

import json
import util as menu_util

from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from account.models import UserProfile
from core import resource
from core.jsonresponse import create_response
from core.exceptionutil import unicode_full_stack
from tools.customerized_menu import views as menu_tool
from watchdog.utils import *
from weixin.manage.customerized_menu.models import *
from weixin2 import export
from weixin2.models import *
from weixin.mp_decorators import mp_required
from apps.models import CustomizedApp


COUNT_PER_PAGE = 20
FIRST_NAV = export.WEIXIN_HOME_FIRST_NAV

class Menu(resource.Resource):
	app = 'new_weixin'
	resource = 'menu'
	
	@login_required
	@mp_required
	def get(request):
		"""
		自定义菜单页面
		"""
		status = STATUS_OPEN
		try:
			menu_status = CustomerMenuStatus.objects.get(owner=request.user)
			status = menu_status.status
			
		except:
			pass
		
		is_certified_service = False
		try:
			mpuser = get_system_user_binded_mpuser(request.user)
			is_certified_service = (mpuser.is_certified and mpuser.is_service)
		except:
			pass
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_weixin_second_navs(request),
			'second_nav_name': export.WEIXIN_MPUSER_SECOND_NAV,
			'third_nav_name': export.MPUSER_MENU_NAV,
			'status': status,
			'is_weizoom_mall': request.user.is_weizoom_mall,
			'is_certified_service': is_certified_service,
		})
		return render_to_response('weixin/mp_user/menu.html', c)
	
	@login_required
	def api_get(request):
		"""
		获取自定义菜单项json数据
		"""
		if request.user.is_authenticated():
			user = request.user
		else:
			webapp_id = request.GET.get('webapp_id', None)
			if not webapp_id:
				response = create_response(500)
				response.errMsg = u'invalid webapp_id'
				return response.get_response()
				
			user_profile = UserProfile.objects.get(webapp_id=request.GET['webapp_id'])
			user = user_profile.user
			
		menus = menu_util.get_menus_json(user)
	
		response = create_response(200)
		response.data = menus
		return response.get_response()

	@login_required
	def api_post(request):
		"""
		更新本地存储的自定义菜单项
		"""
		try:
			owner = request.user
			menus = json.loads(request.POST['menus'])
			ids = set()
			for menu in menus:
				ids.add(menu['id'])
				for item in menu['items']:
					ids.add(item['id'])
			existed_ids = set([item.id for item in CustomerMenuItem.objects.filter(owner=owner)])
			need_add_ids = ids - existed_ids
			need_delete_ids = existed_ids - ids
			need_update_ids = ids.intersection(existed_ids)
			response = create_response(200).get_response()
			for menu in menus:
				menu_id = menu['id']
				#处理CustomerMenuItem
				if menu_id in need_add_ids:
					menu_model = CustomerMenuItem.objects.create(
						owner = owner,
						name = menu['name'],
						type = MENU_ITEM_TYPE_KEYWORD,
						rule_id = 0,
						father_id = 0,
						url = '',
						is_active = True,
						display_index = menu['index']
					)
					menu_id = menu_model.id
					menu['id'] = menu_id
					rule = menu_util.create_rule(owner, menu)
					CustomerMenuItem.objects.filter(id=menu_id).update(rule_id=rule.id)
				elif menu_id in need_update_ids:
					CustomerMenuItem.objects.filter(id=menu_id).update(
						name = menu['name'],
						display_index = menu['index']
					)
					menu_util.update_rule(owner, menu)
				for menu_item in menu['items']:
					menu_item_id = menu_item['id']
					#处理CustomerMenuItem
					if menu_item_id in need_add_ids:
						menu_item_model = CustomerMenuItem.objects.create(
							owner = owner,
							name = menu_item['name'],
							type = MENU_ITEM_TYPE_KEYWORD,
							rule_id = 0,
							father_id = menu_id,
							url = '',
							is_active = True,
							display_index = menu_item['index']
						)
						menu_item_id = menu_item_model.id
						menu_item['id'] = menu_item_model.id
						rule = menu_util.create_rule(owner, menu_item)
						CustomerMenuItem.objects.filter(id=menu_item_id).update(rule_id=rule.id)
					elif menu_item_id in need_update_ids:
						menu_util.update_rule(owner, menu_item)
						CustomerMenuItem.objects.filter(id=menu_item_id).update(
							name = menu_item['name'],
							display_index = menu_item['index']
						)
			#删除需要删除的菜单
			menu_util.delete_rules(request.user, need_delete_ids)
			CustomerMenuItem.objects.filter(id__in=need_delete_ids).delete()
			#调用微信api
			menu_json_obj = menu_util.get_menus_json_for_weixin(request.user)
			if menu_json_obj.has_key('button') and len(menu_json_obj['button']) > 0:

				post = {
					'menu_json': json.dumps(menu_json_obj, ensure_ascii=False)
					}
				fake_request = menu_util.get_fake_request(request.user, post)
				response = menu_tool.update_customerized_menu(fake_request)
# 			
		except:
			response = create_response(500).get_response()
			error_msg = unicode_full_stack()
			response.innerErrMsg = error_msg
			watchdog_error(error_msg)
			print 'save custom menus: ', error_msg
			
		return response