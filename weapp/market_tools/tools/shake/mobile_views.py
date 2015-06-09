# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from datetime import datetime

from models import *
from modules.member import util as member_util
from modules.member.models import Member

def __get_current_user_info(request, member):
    """
    获取当前用户的头像和名称信息
    """
    member_util.member_basic_info_updater(request.user_profile, member)
    return Member.objects.get(id = member.id)
    
########################################################################
# get_shake: 获取红包页面
########################################################################
def get_shake(request):
    webapp_user = request.webapp_user
    member = request.member
    shake_id = request.GET.get('shake_id', None)
    #try:
    member = __get_current_user_info(request, member)
    #member = Member.objects.get(id = member.id)
    shake = Shake.objects.get(id=shake_id)
    if member:
    #是否已经参加领红包
        is_participated = False
        now = datetime.now()
        shake_details = ShakeDetail.objects.filter(shake=shake, start_at__lte=now, end_at__gte=now)
        shake_detail_ids = [detail.id for detail in shake_details]

        if shake_details.count() > 0:
            shake_detail = shake_details[0]
            if ShakeRecord.objects.filter(member_id=member.id, shake_detail=shake_detail).count() >= shake_detail.play_count:
                shake_records = ShakeRecord.objects.filter(member_id=member.id, shake_detail=shake_detail)
                is_participated = True
        else:
            shake_detail = None

        if shake_detail is None:
            next_shake_details = ShakeDetail.objects.filter(shake=shake, start_at__gte=now).order_by('start_at')
            if next_shake_details.count() > 0:
                next_shake_detail = next_shake_details[0]
            else:
                next_shake_detail = None
        else:
            next_shake_detail = None

        c = RequestContext(request, {
            'page_title': shake_detail.shake.name if shake_detail else u'摇一摇', #红包名称
            'is_participated': is_participated,
            'shake_detail': shake_detail,
            'hide_non_member_cover': True,
            'next_shake_detail': next_shake_detail,
            'shake':shake,
            'is_hide_weixin_option_menu':True,
            'cur_request_member': member
        })
    else:
        c = RequestContext(request, {
                'page_title': u'没有会员信息请关注', #红包名称
                'is_participated': False,
                'shake_detail': None,
                'hide_non_member_cover': True,
                'is_hide_weixin_option_menu':True ,
                'shake':shake,
                'cur_request_member': member
            })

    # except:
    #     c = RequestContext(request, {
    #         'is_deleted_data': True,
    #         'is_hide_weixin_option_menu':True
    #     })
    return render_to_response('shake/webapp/shake.html', c)



#######################################################################
#get_usage: 获取“我的”红包列表
#######################################################################
def get_usage(request):
    profile = request.user_profile
    member = request.member
    shake_records = ShakeRecord.objects.filter(member_id=member.id, shake_detail=shake_detail)
    
    
    # red_envelope_records = RedEnvelopeRecord.objects.filter(webapp_user_id=webapp_user.id)
    # red_envelopes = list(RedEnvelope.objects.filter(id__in=red_envelope_ids, is_deleted=False))
    # workspace_template_info = 'workspace_id=market_tool:red_envelope&webapp_owner_id=%d&project_id=0' % request.project.owner_id
    # for red_envelope_record in red_envelope_records:
    #     red_envelope_record.red_envelope.target_link = './?module=market_tool:red_envelope&model=red_envelope&action=get&red_envelope_id=%d&%s' % (red_envelope_record.red_envelope.id, workspace_template_info)

    c = RequestContext(request, {
        'page_title': u'我的摇一摇',
        'shake_records': shake_records,
        'is_hide_weixin_option_menu':True,
    })
    return render_to_response('shake/webapp/my_shakes.html', c)