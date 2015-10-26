# -*- coding: utf-8 -*-

import json
import util as menu_util

from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response, decode_json_str
from tools.customerized_menu import views as menu_tool
from weixin.manage.customerized_menu.models import *
from weixin2 import export
from weixin2.models import *


COUNT_PER_PAGE = 20
FIRST_NAV = export.WEIXIN_HOME_FIRST_NAV

class MenuStatus(resource.Resource):
	app = 'new_weixin'
	resource = 'menu_status'

	@login_required
	def api_post(request):
		"""
		更新自定义菜单项状态
		"""
		owner = request.manager
		status= int(request.POST['status'])
		
		#开启自定义菜单
		if status == STATUS_OPEN:
			#调用微信api
			menu_json_obj = menu_util.get_menus_json_for_weixin(request.manager)
			post = {
				'menu_json': json.dumps(menu_json_obj, ensure_ascii=False)
			}
			fake_request = menu_util.get_fake_request(request.manager, post)
			response = menu_tool.update_customerized_menu(fake_request)
		#禁用自定义菜单
		if status == STATUS_STOP:
			response = menu_tool.delete_customerized_menu(request)
 		
# 		response = create_response(200).get_response()
		result = decode_json_str(response.content)
		try:
			if int(result['code']) == 200:
				try:
					menu_status = CustomerMenuStatus.objects.get(owner=owner)
				except:
					menu_status = CustomerMenuStatus()
					menu_status.owner = owner
				menu_status.status = status
				menu_status.save()
		except:
			pass
		
		return response