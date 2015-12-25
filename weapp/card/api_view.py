# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from core.jsonresponse import create_response
from core.restful_url_route import api
from weixin.user.models import ComponentAuthedAppidInfo, ComponentAuthedAppid

@api(app='card', resource='auth', action='get')
def get_user(request):
    username = request.GET.get('username',[])
    if username:
        username = username.split(',')
    user_id2username = {user.id:user for user in User.objects.filter(username__in=username)}

    authed_appid = ComponentAuthedAppidInfo.objects.filter(auth_appid__user_id__in=user_id2username.keys())
    authed_appids = []
    for a in authed_appid:
        authed_appids.append(a.auth_appid_id)
    auth_appid2auth = {c.id:c for c in ComponentAuthedAppid.objects.filter(id__in=authed_appids)}

    auth = []
    for appid in authed_appid:
        if appid.nick_name:
            if auth_appid2auth.has_key(appid.auth_appid_id):
                auth.append({
                    'user_id':auth_appid2auth[appid.auth_appid_id].user_id,
                    'username': user_id2username[auth_appid2auth[appid.auth_appid_id].user_id].username,
                    'mpuser_name':appid.nick_name
                })
    response = create_response(200)
    response.data = auth
    return response.get_response()

