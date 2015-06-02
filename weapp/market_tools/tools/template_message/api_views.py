# -*- coding: utf-8 -*-

__author__ = 'slzhu'

import random

from core import paginator
from core import apiview_util
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from account.models import *
from webapp.modules.mall.models import * 
from core.jsonresponse import JsonResponse, create_response
from datetime import datetime, timedelta

from models import *

from excel_response import ExcelResponse

def call_api(request):
    api_function = apiview_util.get_api_function(request, globals())
    return api_function(request)


########################################################################
# get_industry: 获取核算信息
########################################################################
@login_required
def get_industry(request):
    response = create_response(200)
    industries = MarketToolsIndustry.objects.all()
    
    items = []
    for industry in industries:
        item = {}
        item['type'] = industry.industry_type
        item['name'] = industry.industry_name
        items.append(item)
    response.data.items = items
        
    return response.get_response()


########################################################################
# get_template: 获取模板信息
########################################################################
@login_required
def get_template(request):
    count_per_page = int(request.GET.get('count_per_page', 15))
    cur_page = int(request.GET.get('page', '1'))
    
    templates = MarketToolsTemplateMessageDetail.objects.filter(owner=request.user)
    pageinfo, templates = paginator.paginate(templates, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
    template_ids = [t.template_message_id for t in templates]
    messages = MarketToolsTemplateMessage.objects.filter(id__in=template_ids)
    id2template = {}
    for message in messages:
        id2template[message.id] = message
    items = []
    for template in templates:
        item = {}
        template_message_id = template.template_message_id
        item['template_detail_id'] = template.id
        item['template_id'] = template.template_id
        item['title'] = id2template[template_message_id].title
        item['industry_name'] = TYPE2INDUSTRY.get(id2template[template_message_id].industry, '')
        if template.status == 1:
            item['status'] = u'已启用'
        else:
            item['status'] = u'未启用'
        if template.type == 0:
            item['type'] = u'主营行业'
        else:
            item['type'] = u'副营行业'
        items.append(item)
    response = create_response(200)
    response.data.items = items
    response.data.pageinfo = paginator.to_dict(pageinfo)
    response.data.sortAttr = ''
        
    return response.get_response()


########################################################################
# create_template: 修改模板信息
########################################################################
@login_required
def create_template(request):
    response = create_response(200)
    major_type = request.POST.get('major_type')
    if major_type == 'None' or len(major_type) == 0:
        return response.get_response()
    industries = []
    major_templates = []
    try:
        major_type = int(major_type)
        majors = MarketToolsTemplateMessageDetail.objects.filter(owner=request.user, industry=major_type)
        if len(majors) > 0:
            majors.update(type=MAJOR_INDUSTRY_TYPE)
        else:
            major_templates = MarketToolsTemplateMessage.objects.filter(industry=major_type)
        industries.append(major_type)
    except:
        pass
    deputy_templates = []
    try:
        deputy_type = int(request.POST.get('deputy_type'))
        deputies = MarketToolsTemplateMessageDetail.objects.filter(owner=request.user, industry=deputy_type)
        if len(deputies) > 0:
            deputies.update(type=DEPUTY_INDUSTRY_TYPE)
        else:
            deputy_templates = MarketToolsTemplateMessage.objects.filter(industry=deputy_type)
        industries.append(deputy_type)
    except:
        pass
    MarketToolsTemplateMessageDetail.objects.filter(owner=request.user).exclude(industry__in=industries).delete()
    if major_templates:
        for template in major_templates:
            MarketToolsTemplateMessageDetail.objects.create(
                owner = request.user,
                template_message = template,
                industry = major_type,
                type = MAJOR_INDUSTRY_TYPE
            )
    if deputy_templates:
        for template in deputy_templates:
            MarketToolsTemplateMessageDetail.objects.create(
                owner = request.user,
                template_message = template,
                industry = deputy_type,
                type = DEPUTY_INDUSTRY_TYPE
            )

        
    return response.get_response()


########################################################################
# update_detail: 保存模板详细信息
########################################################################
@login_required
def update_detail(request):
    id = request.POST.get('id')
    template_id = request.POST.get('template_id', '')
    first_text = request.POST.get('first_text', '')
    remark_text = request.POST.get('remark_text', '')
    action = request.POST.get('action', '')
    
    response = create_response(200)
    if len(first_text) == 0 or len(remark_text) == 0:
        return response.get_response()
    
    message_detail = MarketToolsTemplateMessageDetail.objects.get(id=id)
    message_detail.template_id = template_id
    message_detail.first_text = first_text
    message_detail.remark_text = remark_text
    if action == 'enable':
        status = request.POST.get('status', 0)
        message_detail.status = status
    message_detail.save()

    return response.get_response()


########################################################################
# update_status: 启用/停用
########################################################################
@login_required
def update_status(request):
    id = request.POST.get('id')
    status = request.POST.get('status')
    
    message_detail = MarketToolsTemplateMessageDetail.objects.get(id=id)
    message_detail.status = status
    message_detail.save()

    response = create_response(200)
        
    return response.get_response()