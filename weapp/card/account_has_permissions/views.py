# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from core.restful_url_route import view

from card import export

########################################################################
# edit_weizoom_card_account_permission: 编辑使用微众卡用户的权限
########################################################################
@login_required
@view(app='card', resource='permissions', action='get')
def edit_weizoom_card_account_permission(request):
    c = RequestContext(request, {
        'first_nav_name': export.MALL_CARD_FIRST_NAV,
        'second_navs': export.get_card_second_navs(request),
        'second_nav_name': export.MALL_CARD_MANAGER_NAV
    })
    return render_to_response('card/editor/edit_account_has_permissions.html', c)