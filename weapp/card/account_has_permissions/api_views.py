# -*- coding: utf-8 -*-

from core.jsonresponse import create_response
from django.contrib.auth.models import User
from core.restful_url_route import api
from market_tools.tools.weizoom_card.models import AccountHasWeizoomCardPermissions

#===============================================================================
# get_user_all : 获取所有账号信息
#===============================================================================
@api(app='card', resource='user_all', action='get')
def get_user_all(request):
    users = User.objects.exclude(username__in=['admin'])

    items = []
    for user in users:
        items.append({
            'id': user.id,
            'name': user.username
        })

    response = create_response(200)
    response.data = {
        'items': items,
    }
    return response.get_response()


#===============================================================================
# get_has_weizoom_card_permissions_user : 获取有微众卡权限的用户
#===============================================================================
@api(app='card', resource='has_weizoom_card_permissions_user', action='get')
def get_has_weizoom_card_permissions_user(request):
    permissions = AccountHasWeizoomCardPermissions.objects.filter(is_can_use_weizoom_card=True)
    user2id = dict([(u.id, u) for u in User.objects.all()])

    items = []
    for permission in permissions:
        user = user2id.get(permission.owner_id)
        items.append({
            'id': user.id,
            'name': user.username
        })

    response = create_response(200)
    response.data = {
        'items': items,
    }
    return response.get_response()


#===============================================================================
# update_weizoom_card_account_permission : 更新用户使用微众卡的权限
#===============================================================================
@api(app='card', resource='weizoom_card_account_permission', action='update')
def update_weizoom_card_account_permission(request):
    owner_ids = request.GET['owner_ids']
    if not owner_ids or (owner_ids is ''):
        for permission in AccountHasWeizoomCardPermissions.objects.filter(is_can_use_weizoom_card=True):
            permission.is_can_use_weizoom_card=False
            permission.save()
    else:
        ids = owner_ids.split(',')
        accounts_relation2permission = AccountHasWeizoomCardPermissions.objects.filter(owner_id__in=ids)
        permission_owner_ids = [int(a.owner_id) for a in accounts_relation2permission]
        create_account_list = []
        for id in ids:
            if int(id) not in permission_owner_ids:
                AccountHasWeizoomCardPermissions.objects.create(
                    owner_id=id,
                    is_can_use_weizoom_card=True
                )
        for permission in set(accounts_relation2permission):
            if not permission.is_can_use_weizoom_card:
                permission.is_can_use_weizoom_card=True
                permission.save()
        for permission in AccountHasWeizoomCardPermissions.objects.exclude(owner_id__in=ids).filter(is_can_use_weizoom_card=True):
            permission.is_can_use_weizoom_card=False
            permission.save()
    response = create_response(200)
    return response.get_response()
