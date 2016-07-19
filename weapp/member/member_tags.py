# -*- coding: utf-8 -*-
import json

from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

import export
from core import resource
from modules.member.models import *
from core.jsonresponse import create_response
from webapp import models as webapp_models
from weixin.user.models import DEFAULT_ICON, get_system_user_binded_mpuser
from member.util import zeus_req


def get_should_show_authorize_cover(request):
    mpuser = get_system_user_binded_mpuser(request.user)

    if (mpuser is None) or (not mpuser.is_certified) or (not mpuser.is_service):
        return True
    else:
        return False

class MemberTags(resource.Resource):
    app = "member"
    resource = "member_tags"


    @login_required
    def get(request):
        webapp_id = request.user_profile.webapp_id
        default_tag_id = MemberTag.get_default_tag(webapp_id).id
        member_tags = MemberTag.get_member_tags(webapp_id)
        #调整排序，将为分组放在最前面
        tags = []
        for tag in member_tags:
            if tag.name == '未分组':
                tags = [tag] + tags
            else:
                tags.append(tag)
        member_tags = tags
        is_can_send = False
        from weixin.user.models import WeixinMpUser
        try:
            mp_user = WeixinMpUser.objects.get(owner_id=request.user_profile.user_id)
            if mp_user and mp_user.is_certified:
                is_can_send = True
        except:
            pass
        ids = [str(tag.id) for tag in MemberTag.objects.filter(webapp_id=webapp_id)]
        if ids:
            ids = '_'.join(ids)
        else:
            ids = ''
        for member_tag in member_tags:
            member_tag.count = MemberHasTag.get_tag_has_member_count(member_tag)
        c = RequestContext(request, {
            'first_nav_name': export.MEMBER_FIRST_NAV,
            'second_navs': export.get_second_navs(request),
            'second_nav_name': export.MEMBER_TAG,
            'member_tags': member_tags,
            'should_show_authorize_cover': get_should_show_authorize_cover(request),
            'success_count': UserSentMassMsgLog.success_count(webapp_id),
            'is_can_send': is_can_send,
            'ids':ids
            #'pageinfo': json.dumps(paginator.to_dict(pageinfo))
            })
        return render_to_response('member/editor/member_tags.html', c)

    @login_required
    def api_post(request):
        webapp_id = request.user_profile.webapp_id
        default_tag_id = MemberTag.get_default_tag(webapp_id).id
        member_tags = MemberTag.get_member_tags(webapp_id)
        # print '========================================'
        # print request.POST
        # print webapp_id
        # print '========================================'
        #调整排序，将为分组放在最前面
        tags = []
        for tag in member_tags:
            if tag.name == '未分组':
                tags = [tag] + tags
            else:
                tags.append(tag)
        member_tags = tags
        member_tag_ids = [member_tag.id for member_tag in member_tags]
        id_values = {}
        tags_dict = request.POST.dict()
        if tags_dict.has_key('timestamp'):
            tags_dict.pop('timestamp')
        if tags_dict.has_key('_ids'):
            tags_dict.pop('_ids')
        for key, value in tags_dict.items():
            id = key.split('_')[2]
            id_values[int(id)] = value
        for id in id_values.keys():
            value = id_values[id]
            #不能添加和更新名为‘未分组’的组名
            if value != '未分组':
                zeus_resp = zeus_req('get', {
                    'resource': 'member.member_tags',
                    'data': {
                        'webapp_id': webapp_id,
                        'id': id
                    }
                })        
                if len(zeus_resp['member_tags']) > 0:
                    zeus_req('put', {
                        'resource': 'member.member_tags',
                        'data': {
                            'webapp_id': webapp_id,
                            'name': value ,
                            'id': id
                        }
                    })
                else:
                    zeus_resp = zeus_req('get', {
                        'resource': 'member.member_tags',
                        'data': {
                            'id': id
                        }
                    }) 
                    if len(zeus_resp['member_tags']) == 0 :
                        params =  {
                                'webapp_id': webapp_id,
                                'name': value ,
                                'id': id
                            }
                    else:
                        params ={
                            'webapp_id': webapp_id,
                            'name': value ,
                        }
                    zeus_req('post', {
                        'resource': 'member.member_tags',
                        'data': params
                    })                                              
                # if MemberTag.objects.filter(id=id, webapp_id=webapp_id).count() > 0:
                #     MemberTag.objects.filter(id=id, webapp_id=webapp_id).update(name=value)
                # else:
                #     if MemberTag.objects.filter(id=id).count() == 0:
                #         MemberTag.objects.create(id=id, name=value, webapp_id=webapp_id)
                #     else:
                #         MemberTag.objects.create(name=value, webapp_id=webapp_id)


        delete_ids = list(set(member_tag_ids).difference(set(id_values.keys())))
        if default_tag_id in delete_ids:
            delete_ids.remove(default_tag_id)
        zeus_req('delete', {
            'resource': 'member.member_tags',
            'data': {
                'webapp_id': webapp_id,
                'member_tag_ids': ','.join([str(id) for id in delete_ids]),
            }
        })
        # members = [m.member for m in MemberHasTag.objects.filter(member_tag_id__in=delete_ids)]
        # MemberTag.objects.filter(id__in=delete_ids).delete()
        # for m in members:
        #     if MemberHasTag.objects.filter(member=m).count() == 0:
        #         MemberHasTag.objects.create(member=m, member_tag_id=default_tag_id)

        #########################################################
        # 数据库有的
        # member_tag_ids = [member_tag.id for member_tag in member_tags]
        # id_values = {}  # post传入的

        # tags_dict = request.POST.dict()
        # if tags_dict.has_key('timestamp'):
        #     tags_dict.pop('timestamp')
        # if tags_dict.has_key('_ids'):
        #     tags_dict.pop('_ids')
        # for key, value in tags_dict.items():
        #     id = key.split('_')[2]
        #     id_values[int(id)] = value


        # delete_ids = list(set(member_tag_ids).difference(set(id_values.keys())))
        # diff_tag_ids = list(set(id_values.keys()).difference(set(member_tag_ids)))

        # print '==============ddddddd=========================='
        # print id_values.keys()
        # print delete_ids
        # print diff_tag_ids
        # print member_tag_ids
        # print '==============ddddddd=========================='


        # if diff_tag_ids: # post
            # zeus_req('post', {
            #     'resource': 'member.member_tags',
            #     'data': {
            #         'webapp_id': webapp_id,
            #         'name': json.dumps(id_values) ,
            #         'id': ','.join(str(id) for id in diff_tag_ids)
            #     }
            # })
        # elif delete_ids : # delete
            # zeus_req('delete', {
            #     'resource': 'member.member_tags',
            #     'data': {
            #         'webapp_id': webapp_id,
            #         'member_tag_ids': ','.join([str(id) for id in delete_ids]),
            #     }
            # })
        # else: # put
        #     zeus_req('put', {
        #         'resource': 'member.member_tags',
        #         'data': {
        #             'member_tag_ids': ','.join([str(id) for id in id_values.keys()]),
        #             'name': json.dumps(id_values),
        #             'weapp_id': webapp_id
        #         }
        #     }) 

        response = create_response(200)
        return response.get_response()