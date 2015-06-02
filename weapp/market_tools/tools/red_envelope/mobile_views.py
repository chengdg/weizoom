# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import Context, RequestContext
from django.shortcuts import render_to_response

from models import *
from modules.member import util as member_util


########################################################################
# get_red_envelope: 获取红包页面
########################################################################
def get_red_envelope(request):
    webapp_user = request.webapp_user
    red_envelope_id = int(request.GET['red_envelope_id'])
    try:
        #是否已经参加领红包
        is_participated = False
        red_envelope = RedEnvelope.objects.get(id=red_envelope_id)
        
        is_participated = (RedEnvelopeRecord.objects.filter(red_envelope=red_envelope, webapp_user_id=webapp_user.id).count() > 0)
        
        if is_participated:
            red_envelope_record = RedEnvelopeRecord.objects.filter(red_envelope=red_envelope, webapp_user_id=webapp_user.id)[0]
        else:
            if red_envelope.is_deleted:
                c = RequestContext(request, {
                    'is_deleted_data': True,
                    'is_hide_weixin_option_menu':False
                })
                return render_to_response('red_envelope/webapp/red_envelope.html', c)
            red_envelope_record = None 
            
        hide_non_member_cover = red_envelope.is_non_member
            
        
        c = RequestContext(request, {
            'page_title': red_envelope.name, #红包名称
            'is_participated': is_participated,
            'red_envelope': red_envelope,
            'prize': red_envelope_record,
            'hide_non_member_cover': hide_non_member_cover
        })
    except:
        c = RequestContext(request, {
            'is_deleted_data': True,
            'is_hide_weixin_option_menu':False
        })
        return render_to_response('red_envelope/webapp/red_envelope.html', c)
    return render_to_response('red_envelope/webapp/red_envelope.html', c)



########################################################################
# get_usage: 获取“我的”红包列表
########################################################################
def get_usage(request):
    profile = request.user_profile
    webapp_user = request.webapp_user
    red_envelope_ids = RedEnvelopeRecord.objects.values_list('red_envelope', flat=True).filter(webapp_user_id=webapp_user.id)
    
    red_envelope_records = RedEnvelopeRecord.objects.filter(webapp_user_id=webapp_user.id)
    red_envelopes = list(RedEnvelope.objects.filter(id__in=red_envelope_ids, is_deleted=False))
    workspace_template_info = 'workspace_id=market_tool:red_envelope&webapp_owner_id=%d&project_id=0' % request.project.owner_id
    for red_envelope_record in red_envelope_records:
        red_envelope_record.red_envelope.target_link = './?module=market_tool:red_envelope&model=red_envelope&action=get&red_envelope_id=%d&%s' % (red_envelope_record.red_envelope.id, workspace_template_info)

    c = RequestContext(request, {
        'page_title': u'我的红包列表',
        'red_envelopes': red_envelopes,
        'is_hide_weixin_option_menu':False,
        'red_envelope_records': red_envelope_records
    })
    return render_to_response('red_envelope/webapp/my_red_envelopes.html', c)