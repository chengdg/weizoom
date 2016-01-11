# -*- coding: utf-8 -*-

__author__ = 'chuter'


import json
import weixin

from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from models import *
from utils.json_util import string_json
from weixin.message.qa.models import Rule, TEXT_TYPE, NEWS_TYPE
from weixin.user.models import get_system_user_binded_mpuser

import util as menu_util

FIRSTT_NAV_NAME = weixin.NAV_NAME
WEIXIN_SECOND_NAVS = weixin.get_weixin_second_navs()


########################################################################
# edit_customerized_menu: 编辑自定义菜单
########################################################################
@login_required
def edit_customerized_menu(request):
	mpuser = get_system_user_binded_mpuser(request.user)

	if (mpuser is None) or (not mpuser.is_service and not mpuser.is_certified):
		should_show_authorize_cover = True
	else:
		should_show_authorize_cover = False
	c = RequestContext(request, {
		'first_nav_name' : FIRSTT_NAV_NAME,
		'second_navs' : WEIXIN_SECOND_NAVS,
		'second_nav_name' : weixin.WEIXIN_MANAGE_MENU_NAV_NAME,
		'menu_items': menu_util.get_menus_json(request.user),
		'should_show_authorize_cover': should_show_authorize_cover
	})

	return render_to_response('editor/edit_customer_menu.html', c)